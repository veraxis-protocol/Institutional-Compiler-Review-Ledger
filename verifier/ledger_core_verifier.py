#!/usr/bin/env python3
"""Secrets-free mechanical verifier for the Institutional Compiler Review Ledger.

Git identities are transport/lineage references only. Artifact governing identity
is bytes + SHA-256 + SHA-512 (+ manifest binding when applicable).
"""
from __future__ import annotations
import argparse, fnmatch, hashlib, json, os, re, stat, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INFRA_PATTERNS = [
    '.github/**','verifier/**','schemas/**','policy/**','CODEOWNERS',
    'ROLE-IDENTITY-MAP.json','LEDGER-INVARIANTS.md','README.md'
]
# RETIRED authority class. BOOTSTRAP was temporary initial-installation authority
# and is decommissioned (RL-15). The name survives here only as a detection marker
# so the guard below can fail closed if the retired authority is ever reinstalled.
# It is never resolved to an executable role.
RETIRED_ROLE = 'BOOTSTRAP'
RETIRED_BRANCH_PREFIX = 'bootstrap/'
RETIRED_AUTHORITY_KEY = 'bootstrap_authority'
HEX40 = re.compile(r'^[0-9a-f]{40}$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')
HEX128 = re.compile(r'^[0-9a-f]{128}$')

class Failure(RuntimeError): pass

def load_json(path: Path):
    try: return json.loads(path.read_text())
    except Exception as e: raise Failure(f'cannot parse {path}: {e}')

def match(path: str, pattern: str) -> bool:
    if pattern == 'stage-*/**':
        return bool(re.match(r'^stage-[^/]+/.+', path))
    if pattern.endswith('/**'):
        prefix = pattern[:-3]
        return path == prefix.rstrip('/') or path.startswith(prefix)
    return fnmatch.fnmatch(path, pattern)

def matches_any(path: str, patterns: list[str]) -> bool:
    return any(match(path,p) for p in patterns)

def git(*args: str) -> str:
    p=subprocess.run(['git',*args],cwd=ROOT,text=True,capture_output=True)
    if p.returncode: raise Failure(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout.strip()

def changed_files(base: str, head: str) -> list[str]:
    out=git('diff','--name-only',f'{base}...{head}')
    return [x for x in out.splitlines() if x]

def role_for_branch(branch: str, policy: dict) -> str:
    matches=[role for prefix,role in policy['branch_role_prefixes'].items() if branch.startswith(prefix)]
    if len(matches)!=1: raise Failure(f'branch {branch!r} does not bind exactly one role')
    return matches[0]

def verify_retired_bootstrap_absent():
    """RL-15: the retired BOOTSTRAP authority may never be silently revived.

    Fails closed if any active authority configuration reinstalls the retired
    class. Historical prose in README.md, LEDGER-INVARIANTS.md, and bootstrap/**
    is evidence, not authority, and is deliberately not inspected here.
    """
    role_map=load_json(ROOT/'ROLE-IDENTITY-MAP.json')
    policy=load_json(ROOT/'policy/PATH-AUTHORITY.json')
    found=[]
    for p in role_map.get('principals',[]):
        if RETIRED_ROLE in p.get('roles',[]):
            found.append(f"principal {p.get('principal_id')!r} declares retired role {RETIRED_ROLE}")
    if RETIRED_AUTHORITY_KEY in role_map:
        found.append(f'ROLE-IDENTITY-MAP.json declares retired {RETIRED_AUTHORITY_KEY}')
    if RETIRED_ROLE in policy.get('role_paths',{}):
        found.append(f'policy role_paths declares retired class {RETIRED_ROLE}')
    prefixes=policy.get('branch_role_prefixes',{})
    if RETIRED_BRANCH_PREFIX in prefixes:
        found.append(f'policy branch_role_prefixes declares retired prefix {RETIRED_BRANCH_PREFIX!r}')
    for prefix,role in prefixes.items():
        if role==RETIRED_ROLE:
            found.append(f'policy branch_role_prefixes maps {prefix!r} to retired role {RETIRED_ROLE}')
    if RETIRED_AUTHORITY_KEY in policy:
        found.append(f'policy declares retired {RETIRED_AUTHORITY_KEY}')
    if found:
        raise Failure(f'retired BOOTSTRAP authority is present in active configuration: {found}')
    return {'retired_role':RETIRED_ROLE,'active_declarations':0}

def principal_for_actor(actor: str, role_map: dict, role: str) -> dict:
    found=[]
    for p in role_map['principals']:
        if p.get('github_account') == actor and role in p.get('roles',[]): found.append(p)
    if role=='INFRASTRUCTURE' and actor in role_map['infrastructure_authority']['github_accounts']:
        return {'principal_id':'INFRASTRUCTURE_AUTHORITY','github_account':actor,'roles':['INFRASTRUCTURE']}
    if len(found)!=1:
        raise Failure(f'actor {actor!r} is not uniquely bound to role {role}; reviewer identity may still be pending')
    return found[0]

def verify_path_authority(actor: str, branch: str, base: str, head: str):
    policy=load_json(ROOT/'policy/PATH-AUTHORITY.json')
    role_map=load_json(ROOT/'ROLE-IDENTITY-MAP.json')
    verify_retired_bootstrap_absent()
    role=role_for_branch(branch,policy)
    principal=principal_for_actor(actor,role_map,role).get('principal_id')
    files=changed_files(base,head)
    if not files: raise Failure('PR changes no files')
    allowed=policy['role_paths'][role]
    bad=[p for p in files if not matches_any(p,allowed)]
    if bad: raise Failure(f'unauthorized paths for role {role}: {bad}')
    # Steady state: only INFRASTRUCTURE may alter protected infrastructure paths.
    if role!='INFRASTRUCTURE':
        infra=[p for p in files if matches_any(p,INFRA_PATTERNS)]
        if infra: raise Failure(f'non-infrastructure PR alters protected verifier/policy paths: {infra}')
    return {'role':role,'principal':actor,'principal_id':principal,'changed_files':files}

def verify_checkpoint_pin():
    pin=load_json(ROOT/'verifier/CHECKPOINT-VERIFIER-PIN.json')
    p=ROOT/pin['path']
    b=p.read_bytes()
    got=(len(b),hashlib.sha256(b).hexdigest(),hashlib.sha512(b).hexdigest())
    exp=(pin['bytes'],pin['sha256'],pin['sha512'])
    if got!=exp: raise Failure(f'checkpoint verifier identity mismatch: got={got} expected={exp}')
    if not HEX64.fullmatch(pin['sha256']) or not HEX128.fullmatch(pin['sha512']):
        raise Failure('checkpoint pin contains malformed cryptographic digest')
    return {'path':pin['path'],'bytes':got[0],'sha256':got[1],'sha512':got[2]}

def verify_workflow_supply_chain():
    files=list((ROOT/'.github/workflows').glob('*.yml'))+list((ROOT/'.github/workflows').glob('*.yaml'))
    if not files: raise Failure('no workflows found')
    uses_re=re.compile(r'^\s*-?\s*uses:\s*([^\s#]+)')
    bad=[]
    secrets=[]
    for f in files:
        for n,line in enumerate(f.read_text().splitlines(),1):
            if 'secrets.' in line or '${{ secrets' in line: secrets.append(f'{f.relative_to(ROOT)}:{n}')
            m=uses_re.match(line)
            if not m: continue
            target=m.group(1)
            if target.startswith('./'): continue
            if '@' not in target: bad.append((str(f.relative_to(ROOT)),n,target)); continue
            ref=target.rsplit('@',1)[1]
            if not HEX40.fullmatch(ref): bad.append((str(f.relative_to(ROOT)),n,target))
    if secrets: raise Failure(f'CI must be secrets-free; secret references found: {secrets}')
    if bad: raise Failure(f'third-party actions not full-SHA pinned: {bad}')
    return {'workflow_files':[str(f.relative_to(ROOT)) for f in files],'secrets_references':0,'unpinned_actions':0}

def verify_regular_files():
    bad=[]
    for p in ROOT.rglob('*'):
        if '.git' in p.parts or not p.exists(): continue
        if p.is_symlink(): bad.append(str(p.relative_to(ROOT)))
        elif p.is_file() and not stat.S_ISREG(p.stat().st_mode): bad.append(str(p.relative_to(ROOT)))
    if bad: raise Failure(f'non-regular/symlink repository members forbidden: {bad}')
    return {'bad_entries':0}

def verify_manifest(path: Path):
    m=load_json(path)
    members=m.get('members')
    if not isinstance(members,list): raise Failure(f'{path}: members must be array')
    seen=set()
    for x in members:
        rp=x.get('path')
        if not isinstance(rp,str) or not rp or rp in seen: raise Failure(f'{path}: duplicate/missing member path {rp!r}')
        seen.add(rp); p=path.parent/rp
        if not p.is_file(): raise Failure(f'{path}: missing member {rp}')
        b=p.read_bytes()
        if x.get('bytes')!=len(b): raise Failure(f'{path}: byte mismatch {rp}')
        s256=hashlib.sha256(b).hexdigest(); s512=hashlib.sha512(b).hexdigest()
        if x.get('sha256')!=s256 or x.get('sha512')!=s512: raise Failure(f'{path}: digest mismatch {rp}')
    return {'manifest':str(path.relative_to(ROOT)),'members':len(members)}

def verify_manifests():
    results=[]
    for p in ROOT.rglob('*MANIFEST*.json'):
        if p.name in {'CHECKPOINT-VERIFIER-PIN.json'}: continue
        results.append(verify_manifest(p))
    return results

def verify_identity_map():
    verify_retired_bootstrap_absent()
    m=load_json(ROOT/'ROLE-IDENTITY-MAP.json')
    if not m.get('principals'): raise Failure('identity map has no principals')
    ids=[p.get('principal_id') for p in m['principals']]
    if len(ids)!=len(set(ids)) or any(not x for x in ids): raise Failure('principal IDs missing/duplicated')
    # Pending reviewer identity is allowed during bootstrap candidate state only.
    if m.get('status')!='BOOTSTRAP_CANDIDATE_NOT_ACTIVE':
        for p in m['principals']:
            if 'INDEPENDENT_REVIEWER' in p.get('roles',[]):
                if not p.get('github_account') or not p.get('transport_identity',{}).get('fingerprint'):
                    raise Failure('active ledger has unresolved reviewer identity')
    return {'status':m.get('status'),'principals':len(m['principals'])}

def run_all(args):
    result={}
    if args.actor and args.branch and args.base and args.head:
        # Run authority first so adversarial tests prove the intended deny branch
        # rather than failing incidentally in a later content check.
        result['path_authority']=verify_path_authority(args.actor,args.branch,args.base,args.head)
    result.update({
      'retired_bootstrap_absent':verify_retired_bootstrap_absent(),
      'identity_map':verify_identity_map(),
      'checkpoint_pin':verify_checkpoint_pin(),
      'workflow_supply_chain':verify_workflow_supply_chain(),
      'regular_files':verify_regular_files(),
      'manifests':verify_manifests(),
    })
    print(json.dumps({'decision':'MECHANICAL_VERIFICATION_PASS','result':result},indent=2))

def main():
    ap=argparse.ArgumentParser()
    sp=ap.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('verify-all')
    for flag in ('actor','branch','base','head'): a.add_argument(f'--{flag}')
    b=sp.add_parser('verify-pr')
    for flag in ('actor','branch','base','head'): b.add_argument(f'--{flag}',required=True)
    c=sp.add_parser('verify-checkpoint-pin')
    d=sp.add_parser('verify-workflow')
    e=sp.add_parser('verify-identity-map')
    args=ap.parse_args()
    try:
        if args.cmd=='verify-all': run_all(args)
        elif args.cmd=='verify-pr':
            run_all(args)
        elif args.cmd=='verify-checkpoint-pin': print(json.dumps(verify_checkpoint_pin(),indent=2))
        elif args.cmd=='verify-workflow': print(json.dumps(verify_workflow_supply_chain(),indent=2))
        elif args.cmd=='verify-identity-map': print(json.dumps(verify_identity_map(),indent=2))
    except Failure as e:
        print(json.dumps({'decision':'MECHANICAL_VERIFICATION_FAIL','error':str(e)},indent=2),file=sys.stderr)
        sys.exit(1)
if __name__=='__main__': main()
