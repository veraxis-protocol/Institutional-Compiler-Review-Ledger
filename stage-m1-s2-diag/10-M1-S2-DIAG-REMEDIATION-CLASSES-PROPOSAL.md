# M1-S2 Diagnostic — Remediation Classes Proposal

Status: **PROPOSAL ONLY — REMEDIATION NOT AUTHORIZED**

The evidence supports considering an owner-authorized measurement environment that binds a host-supported locale explicitly and verifies standalone `import readline` before any future M1-S2-R1 authority is considered.

Candidate classes, in increasing scope:

1. Explicit supported-locale binding for a newly authorized diagnostic or measurement process.
2. Fresh isolated venv construction from an owner-selected interpreter with recorded executable, package and linked-library identities.
3. Replacement of the interpreter/readline package set only if later evidence shows locale binding alone is insufficient in the intended environment.

This record does not select or execute a remediation. It does not authorize package changes, environment replacement, M1-S2-R1, pytest, project tests, source mutation, or any inference about H1.
