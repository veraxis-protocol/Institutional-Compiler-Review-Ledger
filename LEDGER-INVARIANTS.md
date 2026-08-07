# Review Ledger Invariants

Status: **BOOTSTRAP CANDIDATE — owner-authorized for construction, not yet accepted for operational use.**

## RL-01 — Source / Evidence Separation
`Institutional-Compiler` remains the governed system. This ledger contains evidence about that system. Evidence commits do not mutate the governed system.

## RL-02 — Cryptographic Identity
SHA-256 + SHA-512 remain governing artifact identities. Git commit/blob identities are transport and lineage references only.

## RL-03 — Role Identity Map
Every active principal has a role, transport identity, authorized path class, effective-from state, and revocation state. Missing identity data fails closed. Signing identities are established explicitly; they are not presumed.

## RL-04 — Path Authority
Implementer evidence is confined to `stage-*/**`; reviewer records to `reviews/**`; owner decisions to `owner-decisions/**`; infrastructure to the protected infrastructure set. Unauthorized actor × branch × path combinations fail.

## RL-05 — PR-Only Accepted Branch
The accepted/default branch is PR-only, force-push prohibited, deletion prohibited, and linear history required.

## RL-06 — Merge ≠ Acceptance
Commit existence, CI PASS, reviewer acceptance, owner acceptance, and accepted-state persistence are distinct state transitions.

## RL-07 — CI Immutability
Evidence/review PRs may not alter `.github/**`, `verifier/ledger_core_verifier.py`, `schemas/**`, `policy/**`, `CODEOWNERS`, `ROLE-IDENTITY-MAP.json`, or this invariant file. Infrastructure changes require an owner-controlled infrastructure PR and independent review by a non-author.

## RL-08 — Self-Verification Prohibited
An artifact author may not change the mechanism evaluating the same artifact. A bootstrap/infrastructure author may not independently approve that authored infrastructure.

## RL-09 — Verifier Pinning
Every checkpoint verifier is identified by exact bytes, SHA-256, SHA-512, version/review state, and ledger path.

## RL-10 — Third-Party Action Pinning
Every third-party GitHub Action is pinned to a full immutable commit SHA. Floating tags and branches are prohibited.

## RL-11 — Append-Only Accepted Lineage
Accepted history advances only. Any exceptional rebind/rewrite requires an explicit owner event preserving prior state identity, replacement identity, reason, and historical record.

## RL-12 — Independent Reviewer Separation
The principal producing an independent-review acceptance must differ from the principal that authored the reviewed artifact. Shared transport credentials cannot be treated as proof of institutional independence.

## RL-13 — Accepted-State Reference
Every closed gate receives an accepted-state reference binding owner decision, independent review, evidence identities, and governing cryptographic hashes. Signing keys for accepted-state references are a bootstrap requirement before signed-tag claims are made.

## RL-14 — Fail Closed
Missing identity, ambiguous role, unauthorized path, changed verifier, malformed manifest, unresolved provenance, or failed mechanical verification cannot degrade to a warning.

## RL-15 — Temporary Bootstrap Authority
Initial installation of this ledger legitimately spans bootstrap-governance, owner-decision, and infrastructure paths at once, which no steady-state role covers. A single temporary authority class, `BOOTSTRAP`, exists solely for that initial installation. It does not relax RL-01 through RL-14; it is constrained by them.

`BOOTSTRAP` is bound as follows:

- **Branch.** Only the `bootstrap/` branch prefix maps to `BOOTSTRAP`.
- **Window.** Authority exists only while `ROLE-IDENTITY-MAP.json.status` is exactly `BOOTSTRAP_CANDIDATE_NOT_ACTIVE`. Once ledger status leaves that state the authority lapses permanently and every `bootstrap/*` PR fails closed under RL-14. A missing or altered status gate is itself a failure.
- **Principal.** Authority is explicit, never inferred. The acting account must be owner-bound in `ROLE-IDENTITY-MAP.json.bootstrap_authority`, carry the `BOOTSTRAP` role, and be unrevoked. Repository write access confers nothing. An unbound actor on a `bootstrap/` branch fails closed.
- **Paths.** Only the initial-installation classes enumerated in `policy/PATH-AUTHORITY.json` under `role_paths.BOOTSTRAP`. `stage-*/**` and `reviews/**` are never installation paths and are never writable under `BOOTSTRAP`. Paths listed in `bootstrap_authority.removal_only_paths` may be removed but never created or modified.
- **Non-grant.** `BOOTSTRAP` grants no evidence, review, or acceptance authority, and supplies no independent review. RL-08 and RL-12 continue to apply in full: the bootstrap author may not accept the bootstrap.

`BOOTSTRAP` expires at `ACCEPT_REVIEW_LEDGER_BOOTSTRAP`. Any later use of an initial-installation authority requires a fresh owner event, not the reuse of this one.
