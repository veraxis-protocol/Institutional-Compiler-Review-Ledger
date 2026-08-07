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
