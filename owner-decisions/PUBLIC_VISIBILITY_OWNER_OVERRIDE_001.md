# PUBLIC VISIBILITY OWNER OVERRIDE 001

Date: 2026-08-07
Owner / design authority: Arkadiy Miteiko
Repository: `veraxis-protocol/Institutional-Compiler-Review-Ledger`

## Decision

`AUTHORIZE_PUBLIC_REVIEW_LEDGER_VISIBILITY`

The owner requires the Review Ledger to remain **PUBLIC** during bootstrap and initial operation. This decision supersedes the earlier planning assumption of private-by-default visibility.

Public visibility does not imply technical acceptance, independent-review acceptance, owner acceptance, or authorization to publish arbitrary governed evidence.

## Disclosure boundary

No secret, credential, private key, confidential/privileged material, clearance-blocked material, or artifact whose public-disclosure status is unresolved may be committed to this repository.

Mechanical verification must remain secrets-free. Evidence that cannot satisfy the public-disclosure boundary remains on a non-public/legacy transfer path until separately authorized for release.

## Unchanged invariants

This decision does not waive RL-01 through RL-14, source/evidence separation, cryptographic artifact identity, author/reviewer separation, path authority, protected CI infrastructure, fail-closed behavior, or explicit owner acceptance.

Any later repository visibility change requires a separate owner event.
