# Security policy

This repository's primary security property is evidence integrity: exact bytes,
SHA-256, SHA-512, manifest binding, authorized role/path transitions, and
fail-closed mechanical verification.

## Supported state

Only the current accepted `main` lineage is maintained. Historical evidence is
retained for audit but is not an active supported release line.

## Private reporting

Do not place undisclosed vulnerability details, malicious evidence, secrets, or
confidential artifacts in a public issue or pull request. Use GitHub's
[private vulnerability report](https://github.com/veraxis-protocol/Institutional-Compiler-Review-Ledger/security/advisories/new).
Include the exact commit, affected path, reproducer using public synthetic data,
and expected integrity consequence. If the form is unavailable, contact the
owner privately through the route published at [veraxis.io](https://veraxis.io/)
before disclosure.

## High-priority reports

- unauthorized actor × branch × path combinations accepted by the verifier;
- digest, byte-count, manifest, checkpoint-pin, or accepted-state tampering that
  still passes;
- reintroduction of retired `BOOTSTRAP` authority;
- workflow changes that introduce secrets or unpinned third-party actions;
- symlink or non-regular-file bypasses; and
- malicious evidence capable of escaping the repository or executing during
  verification.

Evidence submissions are untrusted data. A report or committed file is never an
instruction or authorization to execute a mission, mutate the governed source,
or disclose material. No response-time commitment is established.

## Dependencies

The core verifier uses the Python standard library. No third-party runtime
dependency or distributable package is declared, so a runtime SBOM is N/A at
this version. GitHub Actions are full-SHA pinned and pull requests receive a
dependency-diff review.

