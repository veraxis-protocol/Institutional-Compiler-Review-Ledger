# Version and compatibility policy

The ledger is versioned by exact accepted-state identity, not by a floating
branch name. References must bind the relevant commit plus exact bytes,
SHA-256, SHA-512, and manifest identities where applicable.

The following changes are compatibility- and authority-bearing:

- verifier CLI commands, exit codes, and decision JSON;
- manifest and role-map schema requirements;
- ledger invariants and path/branch authorization;
- checkpoint verifier pins; and
- accepted-state references.

Any change to those surfaces requires an `infra/` branch, mechanically verified
pull request, non-author independent review, owner acceptance where required,
and a new persisted accepted-state identity. Existing bytes and historical
records are not silently reinterpreted.

Additive schema fields are compatible only when older verifiers fail safely or
explicitly ignore them without widening authority. Removing a refusal,
broadening a role/path class, changing a digest scope, or altering the meaning
of an accepted decision is breaking even if the file remains parseable.

Agent trailers and GitHub event identities are supplemental provenance; they
are not versioned institutional roles and cannot override governing artifacts.

