# REVIEW LEDGER BOOTSTRAP — OWNER AUTHORIZATION 002

Date: 2026-08-07
Owner / design authority: Arkadiy Miteiko

## Decision

`AUTHORIZE_REVIEW_LEDGER_BOOTSTRAP_CONSTRUCTION`

The owner authorizes immediate construction of a separate Review Ledger for Institutional Compiler evidence transport, independent review, owner decisions, manifests, and verification infrastructure.

## Repository target

`veraxis-protocol/Institutional-Compiler-Review-Ledger`

Initial visibility: **PUBLIC**, by explicit owner requirement. Public visibility is not evidence acceptance and may be changed only by a later owner event.


## Boundary

This authorization does **not** mutate `veraxis-protocol/Institutional-Compiler` and grants no governed-source mutation authority.

M1-S1 continues under the pre-ledger transport channel. The ledger is not authorized as the transport for M1-S1. M1-S2 may become the first native ledger-carried experiment only after bootstrap independent review and owner acceptance.

## Constitution

RL-01 through RL-14 in `LEDGER-INVARIANTS.md` are adopted as the bootstrap working constitution.

Additional bootstrap requirements:

1. Mechanical verification is secrets-free.
2. Reviewer transport identity and signing identities are captured explicitly; none are presumed.
3. Repository visibility is public by owner decision. No secret, credential, confidential/clearance-blocked material, or artifact lacking public-disclosure authorization may be committed.
4. An author cannot independently approve their own bootstrap artifact.
5. Infrastructure/self-verification paths require owner-controlled change plus non-author review.

## Role allocation

- Arkadiy: repository creation, public-visibility authorization, protection settings, owner decisions, final acceptance.
- Vitaliy: requirements and reviewer-facing governance artifacts; artifacts he authors must be reviewed by a non-author.
- Claude: CI skeleton / verifier integration; artifacts Claude authors must be reviewed by a non-author.
- Lead: gate design, adjudication, acceptance criteria, and bootstrap candidate/reference construction.

## Activation gates

The ledger is not operational until all are true:

- public repository exists and its public visibility is bound to `PUBLIC_VISIBILITY_OWNER_OVERRIDE_001`;
- role identity map has no active-principal identity ambiguity;
- reviewer GitHub login and SSH fingerprint are owner-bound;
- signing-key setup status is explicitly recorded;
- default branch protections are active;
- force push and branch deletion are prohibited;
- required CI status is configured;
- infrastructure paths are protected from self-verification;
- bootstrap artifacts receive non-author independent review;
- owner issues final `ACCEPT_REVIEW_LEDGER_BOOTSTRAP`.

Until then the repository state is `BOOTSTRAP_CANDIDATE_NOT_ACTIVE`.


## Visibility override

`PUBLIC_VISIBILITY_OWNER_OVERRIDE_001` supersedes the earlier bootstrap planning assumption of private-by-default visibility. The repository is owner-authorized to remain public. This amendment does not waive RL-01 through RL-14 or any acceptance gate.
