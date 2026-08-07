# Bootstrap Work Orders

## VITALIY-BOOTSTRAP-WO-001
Author: Vitaliy
Scope: reviewer-facing governance artifacts only.

Prepare/revise:
- `README.md`
- `ROLE-IDENTITY-MAP.json`
- `LEDGER-INVARIANTS.md`

Required additions before review-path activation:
- exact Vitaliy GitHub login;
- exact SSH public-key fingerprint used for ledger transport;
- explicit signing-key status;
- confirmation that Git identity is transport/lineage only;
- no secrets in CI assumptions.

Reviewer: Claude or another non-author.
Vitaliy may not independently accept these authored artifacts.

## CLAUDE-BOOTSTRAP-WO-001
Author: Claude / owner-controlled implementation principal
Scope: CI and verifier infrastructure only.

Prepare/revise:
- `.github/workflows/mechanical-verification.yml`
- `verifier/ledger_core_verifier.py`
- `verifier/CHECKPOINT-VERIFIER-PIN.json`
- `schemas/**`
- `policy/**`
- `CODEOWNERS`

Requirements:
- secrets-free;
- `pull_request`, never privileged fork execution;
- third-party actions full-SHA pinned;
- exact V3 pin verification;
- actor × branch × path enforcement;
- fail closed on missing reviewer identity when a review PR is attempted;
- deny mixed-role PRs;
- deny infrastructure modification from evidence/review/owner PR classes;
- manifest hash/accounting checks;
- no claim that CI alone supplies independent review.

Reviewer: Vitaliy.
Claude may not independently accept these authored artifacts.

## CLAUDE-BOOTSTRAP-WO-002 — Bootstrap Authority Correction 001
Author: Claude / owner-controlled implementation principal
Scope: bootstrap authority binding only.

Defect corrected: `.github/workflows/mechanical-verification.yml` invokes `ledger_core_verifier.py verify-pr`, but the verifier bound only the `owner/`, `evidence/`, `review/`, and `infra/` prefixes. The bootstrap branch `bootstrap/review-ledger-001` therefore failed to bind any role, so the bootstrap PR could not mechanically verify the bootstrap. Renaming the branch to `infra/*` is not a correction, because initial installation legitimately spans bootstrap-governance, owner-decision, and infrastructure paths in one change.

Correction: introduce the temporary `BOOTSTRAP` authority class defined in RL-15.

Revised:
- `policy/PATH-AUTHORITY.json`
- `ROLE-IDENTITY-MAP.json`
- `verifier/ledger_core_verifier.py`
- `LEDGER-INVARIANTS.md`
- `bootstrap/BOOTSTRAP-WORK-ORDERS.md`

Constraints held:
- `bootstrap/` binds `BOOTSTRAP` and nothing else;
- authority open only while ledger status is exactly `BOOTSTRAP_CANDIDATE_NOT_ACTIVE`;
- acting principal explicitly owner-bound in `ROLE-IDENTITY-MAP.json.bootstrap_authority`; write access alone grants nothing;
- path authority limited to the enumerated initial-installation classes;
- `stage-*/**` and `reviews/**` rejected under `BOOTSTRAP` before any other path evaluation;
- `.DS_Store` removal permitted as removal-only; creation or modification of it is not authorized under any role;
- OWNER / IMPLEMENTER_EXECUTION / INDEPENDENT_REVIEWER / INFRASTRUCTURE semantics unchanged;
- RL-01 through RL-14 unweakened; RL-15 added as a constrained, expiring class;
- no secrets, no tokens, no privileged workflow paths, no floating Action versions, no bypass semantics;
- Checkpoint B V3 pin untouched.

Expiry: `BOOTSTRAP` lapses at `ACCEPT_REVIEW_LEDGER_BOOTSTRAP`. Removing the class after acceptance is a follow-up infrastructure work order.

Reviewer: Vitaliy or another non-author.
Claude may not independently accept these authored artifacts (RL-08, RL-12).

## OWNER-BOOTSTRAP-WO-001
Owner: Arkadiy

Create public repository `veraxis-protocol/Institutional-Compiler-Review-Ledger` and configure, before operational activation:
- default branch `main`;
- PR-only changes to `main`;
- force pushes disabled;
- deletions disabled;
- linear history required;
- required mechanical-verification status;
- CODEOWNERS review requirement for protected infrastructure;
- no automatic merge-to-acceptance semantics;
- public visibility is owner-authorized under `PUBLIC_VISIBILITY_OWNER_OVERRIDE_001`; any later visibility change requires a separate owner event.

Final state after reviews: either `ACCEPT_REVIEW_LEDGER_BOOTSTRAP` or revision/blocker.
