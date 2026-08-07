# Institutional Compiler Review Ledger

Status: **BOOTSTRAP CANDIDATE — NOT YET ACTIVE**

This repository is the transport and evidence-lineage layer for independent review of the Institutional Compiler. It is intentionally separate from the governed source repository. A commit here records evidence *about* the governed system; it does not mutate the system under review.

## Governing identity model

Git object IDs and commit IDs are transport and lineage references only. They are never governing artifact identities.

Governing artifact identity is the tuple:

- exact bytes;
- SHA-256;
- SHA-512;
- manifest binding where a manifest applies.

Git supplies transport location, ancestry, and tamper evidence under enforced repository controls. Accepted state is therefore described as **tamper-evident, append-only under enforced controls**, not as absolutely immutable.

## State transitions

No transition is implicit:

`EVIDENCE_COMMITTED → MECHANICAL_VERIFICATION_PASS → INDEPENDENT_REVIEW_ACCEPT → OWNER_ACCEPT → ACCEPTED_STATE_PERSISTED`

A commit is not acceptance. CI PASS is not acceptance. Independent review is not owner acceptance. Merge is not owner acceptance.

## Repository separation

- `veraxis-protocol/Institutional-Compiler`: governed system/source.
- `veraxis-protocol/Institutional-Compiler-Review-Ledger`: review evidence, review returns, owner decisions, manifests, and verification infrastructure.

The ledger must never be used to mutate the governed source repository during an evidence gate.

## Path classes

- `stage-*/**` — implementer evidence.
- `reviews/**` — independent-review records.
- `owner-decisions/**` — owner authorizations and acceptances.
- `.github/**`, `verifier/**`, `schemas/**`, `policy/**`, `CODEOWNERS`, `ROLE-IDENTITY-MAP.json`, `LEDGER-INVARIANTS.md` — protected infrastructure.

Path authorization is enforced by repository protection plus fail-closed CI. CODEOWNERS is a review-control mechanism, not a filesystem ACL.

## Identity separation

The GitHub principal `veraxis-protocol` is currently an owner-controlled execution principal and may represent both owner actions and Claude/implementer execution. The ledger therefore must not infer institutional role solely from a GitHub username. Role is additionally constrained by branch class, path class, and explicit owner/reviewer artifacts.

The independent reviewer transport identity must be bound before review-path activation. The reviewer has declared local transport handle `inventor1975`; the exact GitHub login and SSH public-key fingerprint remain **PENDING_BOOTSTRAP_CAPTURE** and must not be guessed.

Commit/tag signing keys are not assumed to exist. Establishing signing identities for accepted-state tags is a bootstrap task.

## Mechanical verification

Mechanical verification is secrets-free. Pull requests from forks receive no privileged verification path. No mechanical check may depend on repository secrets.

The verifier architecture has two layers:

1. `verifier/ledger_core_verifier.py` — stable ledger mechanics and authority checks.
2. Exact checkpoint verifiers pinned by bytes + SHA-256 + SHA-512. The first pinned checkpoint verifier is the already accepted Checkpoint B Verifier V3.

The accepted Checkpoint B Verifier V3 identity is recorded in `verifier/CHECKPOINT-VERIFIER-PIN.json`.

## Bootstrap cutover

M1-S1 continues through the pre-ledger transport channel. The ledger is not an authorized transport for M1-S1. M1-S2 may become the first native ledger-carried experiment only after the bootstrap itself has been independently reviewed and owner-accepted.

See `LEDGER-INVARIANTS.md` for RL-01 through RL-14 and `owner-decisions/REVIEW-LEDGER-BOOTSTRAP-OWNER-AUTHORIZATION-002.md` for the bootstrap authorization.


## Public visibility decision

The repository is intentionally **PUBLIC** by explicit owner decision dated 2026-08-07. Public visibility is a repository-state choice, not an acceptance signal. A later visibility change requires a separate owner decision.

Because the ledger is public, no secret, credential, confidential/clearance-blocked material, or artifact lacking public-disclosure authorization may be committed. Mechanical verification remains secrets-free. Governing artifact identity remains bytes + SHA-256 + SHA-512; Git identities remain transport/lineage only.
