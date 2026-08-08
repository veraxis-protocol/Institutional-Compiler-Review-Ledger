# M1-S2-ENV-001 Qualification — Owner Authorization 001

Document ID: `M1-S2-ENV-001-QUALIFICATION-OWNER-AUTHORIZATION-001`

Owner / Design Authority: Arkadiy Miteiko

Decision token:

`AUTHORIZE_M1_S2_ENV_001_QUALIFICATION_001`

Status before persistence:

**OWNER-AUTHORED CANDIDATE — NOT YET EXECUTABLE**

This authorization becomes executable only after exact-head mechanical verification, non-author independent review, owner ratification, and exact persistence to Review Ledger `main`.

## 1. Accepted predecessor

The accepted predecessor is the persisted M1-S2 infrastructure diagnostic evidence:

- ledger commit: `6bbdaf60dea4ddeeeb820a515fa717083211c2fc`
- tree: `2fdd8bcdbe9b856fe5c3fadf78f5c27532ff8e27`
- diagnostic disposition: `ROOT_CAUSE_NARROWED`
- `ROOT_CAUSE_IDENTIFIED = false`
- H1: `UNADJUDICATED_DUE_TO_INFRASTRUCTURE_BLOCK`
- remediation authority: `NONE`
- M1-S2 rerun authority: `NONE`
- M1-S2-R1 authority: `NONE`

Diagnostic evidence manifest:

- path: `stage-m1-s2-diag/12-M1-S2-DIAG-EVIDENCE-MANIFEST.json`
- bytes: `69457`
- SHA-256: `b210ee6cccb622d43d47c62c841aad7ab683b40a4ea9c8a3d10c55f55f8651d4`
- SHA-512: `15f659d331fb9ad1975e4faf801384d182f0eca442f14b138a731435f4663bd985b96b6d8dd89406ddbd73754e934f48542a92cfa969f0fbd36e244de9b473c3`

Accepted diagnostic finding:

- normal standalone `import readline` reproduced the frozen SIGSEGV;
- changing only `LANG`, `LC_ALL`, and `LC_CTYPE` jointly from `C.UTF-8` to `C` produced `READLINE_IMPORT_OK`;
- Probe 3 was not run;
- the evidence supports a locale-dependent readline-initialization interaction;
- the underlying library mechanism and individually necessary locale variable remain unidentified.

## 2. Purpose

I authorize one bounded environment-qualification mission to determine whether the exact existing M1-S2 interpreter/venv can be used as a candidate future measurement environment when and only when the following process-local locale overlay is applied:

```text
LANG=C
LC_ALL=C
LC_CTYPE=C
```

This mission does not repair packages, does not replace the interpreter, does not mutate the venv, and does not execute M1-S2.

Its sole question is:

**Does the existing frozen interpreter/venv, under the exact three-variable process-local `C` locale overlay and no other intentional environment change, satisfy the bounded qualification criteria defined below?**

## 3. Candidate environment identifier

If qualification succeeds, the resulting candidate environment identifier is:

`M1-S2-ENV-001`

`M1-S2-ENV-001` means exactly:

- Python invocation:
  `/Users/arkadiymiteiko/oam-cdc-reference-publication-candidate/.venv/bin/python`
- existing venv: unchanged
- base interpreter/package set: unchanged
- process-local environment delta:
  - `LANG=C`
  - `LC_ALL=C`
  - `LC_CTYPE=C`
- all other inherited environment variables: unchanged
- package mutations: `0`
- persistent environment mutations: `0`
- canonical governed-source mutations: `0`

Qualification of `M1-S2-ENV-001` does not authorize its use for M1-S2-R1. It only makes the environment eligible for a separate owner authorization decision.

## 4. Authority

Authorized actor role:

`IMPLEMENTER_EXECUTION`

Authorized evidence branch:

`evidence/m1-s2-env-001`

Authorized ledger path:

`stage-m1-s2-env-001/**`

Canonical governed-source mutation authority:

`NONE`

Package/environment repair authority:

`NONE`

M1-S2-R1 authority:

`NONE`

pytest/project-test authority:

`NONE`

The implementer may:

1. inspect the persisted diagnostic evidence and accepted authorization state;
2. verify the canonical governed repository coordinates and cleanliness;
3. verify the existing venv/interpreter identity without modification;
4. record the exact process-local environment overlay;
5. execute the exact qualification commands in §6;
6. preserve command argv, environment delta, timestamps, stdout, stderr, exit status, and any automatically generated crash diagnostics;
7. create ledger evidence only under `stage-m1-s2-env-001/**`;
8. propose, but not execute, the next governance step.

## 5. Absolute prohibitions

This authorization does NOT permit:

- running `pytest`;
- invoking any project test or `tests/**`;
- invoking any M1-S2 test ID;
- rerunning authorized-nine;
- running the M1-S2 module;
- running the full suite;
- executing M1-S2-R1;
- inferring anything about H1;
- modifying canonical governed source;
- modifying the S1/S2 test file;
- modifying `_isolated`;
- modifying AUDIT-004;
- modifying the operational index;
- installing, upgrading, downgrading, removing, repairing, or relinking packages;
- modifying the venv;
- creating a new venv;
- replacing the interpreter;
- changing persistent shell configuration;
- changing system locale configuration;
- exporting the locale overlay into the parent shell;
- changing any environment variable other than the three process-local variables explicitly authorized;
- retrying failed qualification commands until success;
- more than the three qualification trials authorized below;
- M1-R, M2, Stage B1, semantic implementation, or Golden Mission.

## 6. Required qualification sequence

### A. Ledger precondition

Before qualification:

Review Ledger `main` must equal the persisted commit containing this authorization.

If not: STOP.

### B. Canonical governed source

Require:

- repository: `/Users/arkadiymiteiko/oam-cdc-wo007-clean`
- HEAD: `9b1754040c3dafa0123c6b13ea9e5f5eaa2b7bd1`
- tree: `8d898a5d69164db1d4d64e08fb7b71facf459e8b`
- status: CLEAN

If any differs: STOP.

### C. Existing interpreter/venv identity

Without modification, verify and record:

- exact Python executable path;
- resolved symlink chain;
- `sys.executable`;
- `sys.prefix`;
- `sys.base_prefix`;
- Python version/build;
- readline extension identity;
- linked libreadline identity.

These observations must remain consistent with the persisted diagnostic evidence, or the mission must STOP as `QUALIFICATION_BLOCKED_IDENTITY_DRIFT`.

### D. Overlay observation

Run an observation command under exactly:

```text
LANG=C
LC_ALL=C
LC_CTYPE=C
```

with all other inherited environment variables unchanged.

The command may inspect only environment/locale/interpreter state and must not import `readline`.

Record:

- the three overlaid values;
- effective locale categories;
- Python executable/prefixes;
- confirmation that no persistent environment mutation occurred.

### E. Standalone readline qualification trials

Execute exactly three independent process invocations.

Each trial must use the exact same Python invocation and code:

```text
/usr/bin/env
LANG=C
LC_ALL=C
LC_CTYPE=C
/Users/arkadiymiteiko/oam-cdc-reference-publication-candidate/.venv/bin/python
-c
import readline; print('READLINE_IMPORT_OK')
```

No other intentional environment delta is permitted.

Trials are:

- `QUAL_TRIAL_01`
- `QUAL_TRIAL_02`
- `QUAL_TRIAL_03`

For every trial preserve:

- exact argv;
- cwd;
- process-local environment delta;
- started-at timestamp;
- completed-at timestamp;
- stdout;
- stderr;
- exit status;
- any automatically generated crash report.

No hidden warm-up trial is authorized.

No retry is authorized.

If any trial does not exit `0` with stdout exactly `READLINE_IMPORT_OK` and zero stderr bytes:

STOP immediately.

Do not execute any remaining trial after the first failed qualification trial.

## 7. Qualification criteria

Return:

`QUALIFIED_FOR_R1_AUTHORIZATION_CONSIDERATION`

if and only if all are true:

1. canonical governed-source coordinates and cleanliness match exactly;
2. existing interpreter/venv identity has not drifted materially from the accepted diagnostic evidence;
3. the only intentional process environment delta is exactly:
   - `LANG=C`
   - `LC_ALL=C`
   - `LC_CTYPE=C`;
4. overlay observation succeeds;
5. all three authorized readline qualification trials execute;
6. each trial exits `0`;
7. each trial stdout is exactly `READLINE_IMPORT_OK`;
8. each trial stderr is zero bytes;
9. no crash report is generated by any qualification trial;
10. pytest/project-test/M1-S2 runs equal zero;
11. package/venv/source/persistent-environment mutations equal zero.

Otherwise return exactly one of:

- `QUALIFICATION_FAILED`
- `QUALIFICATION_BLOCKED_IDENTITY_DRIFT`
- `QUALIFICATION_BLOCKED_AUTHORITY_OR_EVIDENCE`

Qualification means only that `M1-S2-ENV-001` is eligible to be considered in a new owner authorization for M1-S2-R1.

It is not a claim of universal stability, production suitability, or root-cause identification.

## 8. Evidence

Persist only evidence produced under this authorization, confined to:

`stage-m1-s2-env-001/**`

Minimum governing records:

- `01-M1-S2-ENV-001-OWNER-AUTHORIZATION-REFERENCE.json`
- `02-M1-S2-ENV-001-DIAGNOSTIC-PREDECESSOR-REFERENCE.json`
- `03-M1-S2-ENV-001-IDENTITY-PREFLIGHT.json`
- `04-M1-S2-ENV-001-OVERLAY-DEFINITION.json`
- `05-M1-S2-ENV-001-OVERLAY-OBSERVATION.json`
- `06-M1-S2-ENV-001-QUALIFICATION-TRIALS.json`
- `07-M1-S2-ENV-001-QUALIFICATION-ADJUDICATION.json`
- `08-M1-S2-ENV-001-NEXT-STEP-PROPOSAL.md`
- `09-M1-S2-ENV-001-RETURN-FINAL.md`
- `10-M1-S2-ENV-001-EVIDENCE-MANIFEST.json`

plus raw evidence under:

`stage-m1-s2-env-001/evidence/**`

Manifest requirements:

- self-excluded;
- every other persisted member bound by:
  - path
  - bytes
  - SHA-256
  - SHA-512
- no governing ZIP.

## 9. Commit / review gate

The implementer must:

1. use one evidence commit only;
2. commit on `evidence/m1-s2-env-001`;
3. run Review Ledger mechanical verification against the exact persisted authorization base;
4. push only after mechanical PASS;
5. open a PR to `main`;
6. request `inventor1975`;
7. not merge.

## 10. Return

Return exactly:

`M1_S2_ENV_001_QUALIFICATION_READY_FOR_INDEPENDENT_REVIEW`

followed by:

- `qualification_disposition`
- `environment_id = M1-S2-ENV-001`
- exact environment delta
- qualification trials attempted
- qualification trials passed
- `pytest_runs = 0`
- `project_test_runs = 0`
- `m1_s2_measurement_reruns = 0`
- `canonical_source_mutations = 0`
- `package_mutations = 0`
- `venv_mutations = 0`
- `persistent_environment_mutations = 0`
- `H1 = UNADJUDICATED_DUE_TO_INFRASTRUCTURE_BLOCK`
- evidence commit/tree
- manifest bytes/SHA-256/SHA-512
- exact-head CI run/result
- PR URL

Do not proceed beyond that PR.

## 11. Owner decision

Subject to exact-head independent review, owner ratification, and exact persistence:

`AUTHORIZE_M1_S2_ENV_001_QUALIFICATION_001`

Arkadiy Miteiko  
Owner / Design Authority  
2026-08-08
