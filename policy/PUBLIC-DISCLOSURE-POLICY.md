# Public Disclosure Policy

Status: BOOTSTRAP CANDIDATE — NOT OWNER-ACCEPTED UNTIL BOOTSTRAP GATE CLOSES

The Review Ledger is public by explicit owner decision `PUBLIC_VISIBILITY_OWNER_OVERRIDE_001`.

## Allowed
- Evidence and review artifacts explicitly intended for public disclosure.
- Deterministic manifests, SHA-256/SHA-512 identities, test outputs, and review records that contain no secrets, credentials, confidential/clearance-blocked material, or restricted third-party content.
- Publicly releasable verifier and CI source.

## Prohibited
- Secrets, tokens, passwords, private keys, or repository secrets.
- Confidential, privileged, export-controlled, clearance-blocked, or otherwise non-public material.
- Evidence whose disclosure status is unresolved.
- Publication of an artifact merely because it passed CI or review; public disclosure and technical/owner acceptance are separate states.

## Fail-closed rule
If public-disclosure status is ambiguous, the artifact must not be committed to this repository. It remains on the legacy/private transfer path until an explicit owner release decision exists.
