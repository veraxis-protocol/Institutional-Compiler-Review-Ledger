# M1-S2 Infrastructure Diagnostic — Final Return

Decision: `M1_S2_INFRASTRUCTURE_DIAGNOSTIC_READY_FOR_INDEPENDENT_REVIEW`

Diagnostic disposition: `ROOT_CAUSE_NARROWED`

## Evidence-grounded finding

The normal standalone `import readline` reproduced the frozen `EXC_BAD_ACCESS / SIGSEGV / KERN_INVALID_ADDRESS at 0x0` at the same `_platform_strlen → _rl_init_locale → _rl_init_eightbit → rl_initialize → setup_readline → PyInit_readline` boundary. This establishes that pytest and project tests are not required to reproduce the infrastructure failure.

The authorized locale-only probe changed `LANG`, `LC_ALL`, and `LC_CTYPE` from `C.UTF-8` to `C`; all other inherited variables were unchanged. It exited `0` and printed `READLINE_IMPORT_OK`. The probe ladder therefore stopped after two probes.

This materially narrows the failure to a locale-dependent readline-initialization interaction. It does not identify whether the underlying mechanism is unsupported locale-name handling, a readline defect, a CPython-extension/library interaction, or which individual locale variable is necessary. No root-cause-identification claim is made.

## Boundaries preserved

- probes executed: `2`
- pytest runs: `0`
- project-test runs: `0`
- M1-S2 measurement reruns: `0`
- canonical-source mutations: `0`
- remediation executed: `false`
- full environment captured: `false`
- H1: `UNADJUDICATED_DUE_TO_INFRASTRUCTURE_BLOCK`

No remediation, environment replacement, package modification, source change, M1-S2-R1, M1-R, M2, Stage B1, semantic implementation, or Golden Mission is authorized or performed.
