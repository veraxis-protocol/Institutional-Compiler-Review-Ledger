# M1 Closure — ENV-001 Qualification + Conditional M1-S2-R1 Owner Authorization 001

Document ID: `M1-CLOSURE-ENV-001-CONDITIONAL-R1-OWNER-AUTHORIZATION-001`

Owner / Design Authority: Arkadiy Miteiko

Decision token:

`AUTHORIZE_M1_CLOSURE_ENV_001_CONDITIONAL_M1_S2_R1_001`

Status before persistence:

**OWNER-AUTHORED REVISED CANDIDATE — NOT YET EXECUTABLE**

This authorization becomes executable only after exact-head mechanical verification, non-author independent review of this revised head, owner ratification, and exact persistence to Review Ledger `main`.

The prior narrow PR #10 review at head `cb2369b89c736ab4b704fd53eae1cbe59d286515`, review `4889581777`, token `ACCEPT_M1_S2_ENV_001_QUALIFICATION_AUTHORIZATION_001`, is historical evidence only. It reviewed a narrower unpersisted candidate and does not authorize this revised artifact. The prior narrow decision `AUTHORIZE_M1_S2_ENV_001_QUALIFICATION_001` is superseded before persistence and never became executable authority.

## 1. Accepted predecessor

The accepted predecessor is the persisted M1-S2 infrastructure diagnostic evidence:

- ledger commit: `6bbdaf60dea4ddeeeb820a515fa717083211c2fc`
- tree: `2fdd8bcdbe9b856fe5c3fadf78f5c27532ff8e27`
- diagnostic disposition: `ROOT_CAUSE_NARROWED`
- `ROOT_CAUSE_IDENTIFIED = false`
- H1: `UNADJUDICATED_DUE_TO_INFRASTRUCTURE_BLOCK`
- remediation authority: `NONE`
- M1-S2 rerun authority: `NONE`
- M1-S2-R1 authority: `NONE`

Diagnostic evidence manifest:

- path: `stage-m1-s2-diag/12-M1-S2-DIAG-EVIDENCE-MANIFEST.json`
- bytes: `69457`
- SHA-256: `b210ee6cccb622d43d47c62c841aad7ab683b40a4ea9c8a3d10c55f55f8651d4`
- SHA-512: `15f659d331fb9ad1975e4faf801384d182f0eca442f14b138a731435f4663bd985b96b6d8dd89406ddbd73754e934f48542a92cfa969f0fbd36e244de9b473c3`

Accepted diagnostic finding is limited to the following:

- normal standalone `import readline` reproduced the frozen M1-S2 SIGSEGV;
- changing only `LANG`, `LC_ALL`, and `LC_CTYPE` jointly from `C.UTF-8` to `C` produced `READLINE_IMPORT_OK`;
- Probe 3 was not run;
- the evidence supports a locale-dependent readline-initialization interaction;
- the underlying library mechanism and individually necessary locale variable remain unidentified.

Nothing in this authorization upgrades `ROOT_CAUSE_NARROWED` to `ROOT_CAUSE_IDENTIFIED`.

## 2. Purpose and conditional-authority model

I authorize one M1 closure transaction with two phases:

- **Phase A — qualify `M1-S2-ENV-001`** under a fixed process-local locale overlay;
- **Phase B — execute one fresh preregistered `M1-S2-R1` measurement** if and only if every Phase A activation predicate is satisfied.

No additional owner decision, independent review, or persistence event is required between Phase A and Phase B. Phase B authority is pre-authorized here but remains dormant until the objective activation predicate in §6 evaluates true.

If Phase A does not satisfy every activation predicate, Phase B authority remains inactive and the implementer must STOP and publish Phase-A-only evidence for independent review.

This conditional structure exists to eliminate an unnecessary governance round-trip while preserving fail-closed authority.

## 3. Common authority and confinement

Authorized actor role:

`IMPLEMENTER_EXECUTION`

Authorized evidence branch:

`evidence/m1-closure-001`

Authorized ledger path:

`stage-m1-closure/**`

Canonical governed-source mutation authority:

`NONE`

Package / venv / interpreter mutation authority:

`NONE`

Persistent environment mutation authority:

`NONE`

The canonical governed repository must remain byte-preserved and clean throughout both phases.

Canonical repository:

`/Users/arkadiymiteiko/oam-cdc-wo007-clean`

Required coordinate:

- HEAD: `9b1754040c3dafa0123c6b13ea9e5f5eaa2b7bd1`
- tree: `8d898a5d69164db1d4d64e08fb7b71facf459e8b`
- status: CLEAN

Any mismatch before Phase A, before Phase B, or immediately before the evidence commit is a hard STOP.

## 4. M1-S2-ENV-001 definition

`M1-S2-ENV-001` means exactly:

Python invocation:

`/Users/arkadiymiteiko/oam-cdc-reference-publication-candidate/.venv/bin/python`

Execution substrate:

- same existing venv;
- same base interpreter;
- same installed package set;
- same linked readline/library identities;
- no package repair or relinking;
- no new venv;
- no interpreter replacement.

The only intentional process-local environment delta is:

```text
LANG=C
LC_ALL=C
LC_CTYPE=C
```

All other inherited environment variables remain unchanged.

The overlay must be applied per process. It may not be exported into the parent shell, written to shell configuration, or applied as a system locale change.

## 5. Phase A — environment qualification

### A1. Ledger precondition

Before any Phase A command, Review Ledger `main` must equal the exact persisted commit containing this revised authorization.

If not: STOP with `M1_CLOSURE_BLOCKED_AUTHORITY_STATE`.

### A2. Canonical-source preflight

Verify the canonical repository coordinate in §3 exactly.

If not exact: STOP with `M1_CLOSURE_BLOCKED_CANONICAL_DRIFT`.

### A3. Interpreter/venv identity preflight

Without modifying anything, verify and record:

- exact Python executable path;
- resolved executable symlink chain;
- `sys.executable`;
- `sys.prefix`;
- `sys.base_prefix`;
- Python version/build;
- readline extension path, bytes, SHA-256, SHA-512;
- linked libreadline path, bytes, SHA-256, SHA-512.

These identities must remain materially consistent with the persisted diagnostic evidence. Any unexplained drift is a STOP with `M1_CLOSURE_BLOCKED_ENV_IDENTITY_DRIFT`.

No repair is authorized.

### A4. Overlay observation

Run one read-only observation process under exactly:

```text
LANG=C
LC_ALL=C
LC_CTYPE=C
```

with every other inherited environment variable unchanged.

The observation may inspect only environment, locale, and interpreter state and must not import `readline` or invoke project tests.

Record:

- exact argv;
- exact three-variable environment delta;
- effective locale categories;
- Python executable and prefixes;
- start/end timestamps;
- stdout/stderr/exit status;
- confirmation of zero persistent environment mutation.

### A5. Qualification trials

Execute exactly three independent process invocations, in order:

- `QUAL_TRIAL_01`
- `QUAL_TRIAL_02`
- `QUAL_TRIAL_03`

Each trial must use this same argv semantics:

```text
/usr/bin/env
LANG=C
LC_ALL=C
LC_CTYPE=C
/Users/arkadiymiteiko/oam-cdc-reference-publication-candidate/.venv/bin/python
-c
import readline; print('READLINE_IMPORT_OK')
```

No other intentional environment delta is permitted.

For every trial preserve:

- exact argv;
- cwd;
- exact environment delta;
- start/end timestamps;
- stdout;
- stderr;
- exit status;
- any automatically generated crash report.

No warm-up trial, retry, fourth trial, or retry-until-green behavior is authorized.

If a trial fails the criteria below, STOP immediately and do not execute remaining qualification trials.

## 6. Phase B activation predicate

Phase B authority becomes `ACTIVE_BY_PREAUTHORIZED_CONDITION` if and only if all of the following are true and recorded before any Phase B command:

1. Review Ledger `main` equals the persisted commit containing this authorization.
2. Canonical governed source matches the exact HEAD/tree/clean coordinate in §3.
3. Existing interpreter/venv/readline identities have no unexplained material drift from the accepted diagnostic state.
4. The only intentional process environment delta is exactly `LANG=C`, `LC_ALL=C`, `LC_CTYPE=C`.
5. Overlay observation completed successfully without mutation.
6. All three qualification trials were attempted exactly once.
7. All three qualification trials exited `0`.
8. Each trial stdout is exactly `READLINE_IMPORT_OK` followed by its normal terminating newline and contains no other output.
9. Each trial stderr is zero bytes.
10. No qualification trial generated a crash report.
11. `pytest_runs = 0` during Phase A.
12. `project_test_runs = 0` during Phase A.
13. `m1_s2_measurement_runs = 0` during Phase A.
14. `package_mutations = 0`.
15. `venv_mutations = 0`.
16. `interpreter_mutations = 0`.
17. `persistent_environment_mutations = 0`.
18. `canonical_source_mutations = 0`.

Before Phase B begins, create `stage-m1-closure/05-M1-CLOSURE-PHASE-A-ACTIVATION.json` recording each predicate, the Phase A evidence hashes, and exactly one of:

- `phase_b_authority = ACTIVE_BY_PREAUTHORIZED_CONDITION`
- `phase_b_authority = INACTIVE`

After that activation record is written, Phase A raw evidence and governing records are immutable for the remainder of the execution transaction.

If any predicate is false or cannot be proved, Phase B remains `INACTIVE`; do not run pytest; publish Phase-A-only evidence.

## 7. Phase B — M1-S2-R1 scientific instance

### B1. Historical preservation

The original `M1-S2` remains permanently:

`BLOCKED`

because its authorized-nine process terminated with SIGSEGV before producing a test result.

`M1-S2-R1` is a new, separately identified scientific instance. It does not rewrite, replace, or retroactively complete M1-S2.

### B2. Fresh disposable reconstruction

Use a fresh disposable reconstruction. Do not reuse the crashed M1-S2 temporary reconstruction.

Reconstruct the accepted M1-S1 predecessor state from the canonical governed coordinate plus the already accepted M1-S1 intervention state.

Before the R1 fixture edit, require:

- S1 authorized nine predecessor: `7P / 2F`
- S1 module predecessor: `85P / 2F`
- S1 full-suite predecessor: `1009P / 25F / 7S`
- `tests/test_audit_lineage.py`: 40975 bytes
- S1 test-file SHA-256: `8e6f51a1613456f4a52ce37f1da8f999694fb3195da10c7dc78697b1f9c57410`
- `_isolated`: 1109 bytes
- `_isolated` SHA-256: `766f1f66e03bb82f043263c60d6a437a2818793bd07a2ba29ed8ff69911e9431`
- `_isolated` callers: 23

Current-report bindings must remain:

AUDIT-004:

- path: `docs/governance/gates/OAM-GATE-SAR-05-CDC-PROFILE-AUDIT-004.json`
- bytes: `13494`
- SHA-256: `0c7143c500d7912dca95cd01301a2d388c3f8c46ffc3427c95e2089e5425e631`
- SHA-512: `7ca118fe5ed9e75926dd3b8efe12a649fa0afc168f0a3b6104356a9e8a83b0797b6fe0e4a22fb64cba066d76316ad63a6b0e86f56c6f9f97e1c1171adb406c7d`

Operational index:

- path: `docs/governance/gates/OAM-GATE-SAR-05-CDC-AUDIT-INDEX.json`
- bytes: `4204`
- SHA-256: `20de3c39d714f392d6511efc9aeb2b49a011c9a168baa1a7d683ee8c202bb376`
- SHA-512: `f28a58aebf2e207c820f93cf47592424395c04fb23a82389ae2ba2d6f7eeb95a3fa545f684fbedd67d1cf44c6f13151c8221fa33d335b1b451f7fd6c1decacf9`
- current report: `OAM-GATE-SAR-05-CDC-PROFILE-AUDIT-004`

Any mismatch is a STOP before scientific measurement.

### B3. Exact scientific intervention

Path:

`tests/test_audit_lineage.py`

Function:

`_isolated`

Authorized site:

the single `current =` report-path literal inside `_isolated`.

Pre:

`current = "docs/governance/gates/OAM-GATE-SAR-05-CDC-PROFILE-AUDIT-003.json"`

Post:

`current = "docs/governance/gates/OAM-GATE-SAR-05-CDC-PROFILE-AUDIT-004.json"`

Scope:

- exactly one line;
- exactly one character changes;
- byte length remains unchanged;
- no M1-S1 function-local edit may change;
- no second scientific edit is authorized.

After the edit require exact identities already established before the blocked M1-S2 execution:

- `_isolated` post SHA-256: `9a11894fc361911fe9a6273062686e88e9018b2299aa61a1f03373919a4c19d8`
- R1/S2 test file bytes: `40975`
- R1/S2 test file SHA-256: `04bd2679de95ec831ba010d99fee1cb578f70497916951035e9518340371f2cc`
- R1/S2 test file SHA-512: `5c56b9a105122586e1fe1d26855d54d5b695179dbd1d7325a8b1f714f0c2dd397e45361a6dfa5b1b949eb9b1b347e9095477a96eb65e69aa5f0fbed3a0046f9b`

If exact post identities are not obtained with the one authorized edit: STOP. Do not correct or iterate.

### B4. Fixed R1 execution environment

Every R1 Python/pytest process must run using `M1-S2-ENV-001`:

```text
/usr/bin/env LANG=C LC_ALL=C LC_CTYPE=C /Users/arkadiymiteiko/oam-cdc-reference-publication-candidate/.venv/bin/python ...
```

No fourth intentional environment variable change is authorized.

### B5. Preregistered hypothesis preserved unchanged

H1:

The two remaining M1-S1 failures persist because `_isolated` reproduces AUDIT-003 but does not reproduce AUDIT-004.

Predicted R1 result if H1 is supported:

- authorized nine: `9P / 0F`
- module: `87P / 0F`
- full suite: `1011P / 23F / 7S`
- total suite collected: `1041`
- new failures: `0`

Required suite failure-set difference:

`S1 − R1` must equal exactly:

- `tests/test_audit_lineage.py::test_governed_success_tokens_are_distinct`
- `tests/test_audit_lineage.py::test_valid_confined_alternate_index_is_accepted`

`R1 − S1` must be empty.

The withdrawn prediction `1034P / 0F / 7S` remains prohibited.

### B6. Exact authorized-nine population

The first scientific command must target exactly these nine IDs and no others:

1. `tests/test_audit_lineage.py::test_operational_index_validates_and_verifies`
2. `tests/test_audit_lineage.py::test_supersession_lineage_is_a_single_normalized_graph`
3. `tests/test_audit_lineage.py::test_currentness_is_unaffected_by_filesystem_tricks[higher numbered unindexed report]`
4. `tests/test_audit_lineage.py::test_currentness_is_unaffected_by_filesystem_tricks[newer modification time]`
5. `tests/test_audit_lineage.py::test_currentness_is_unaffected_by_filesystem_tricks[lexically later name]`
6. `tests/test_audit_lineage.py::test_governed_success_tokens_are_distinct`
7. `tests/test_audit_lineage.py::test_focused_audit_tests_do_not_mutate_the_reviewed_repository`
8. `tests/test_audit_lineage.py::test_valid_confined_alternate_index_is_accepted`
9. `tests/test_audit_lineage.py::test_lineage_is_a_single_root_injective_linear_chain`

Use `python -m pytest`, `-q`, and a JUnit output written under `stage-m1-closure/evidence/**`.

### B7. Measurement sequence

Run exactly once each, in order:

1. authorized nine;
2. `tests/test_audit_lineage.py` module;
3. full pytest suite.

A scientifically failing pytest result is still evidence and does not authorize correction or rerun.

For this transaction, a command is result-bearing only if pytest returns a normal result-bearing exit (`0` or `1`) and produces a parseable JUnit result for the intended population.

If a measurement process terminates by signal, exits with pytest infrastructure/usage/internal-error status, fails to create a required parseable result, or otherwise fails before a scientific result exists:

- stop subsequent measurement commands;
- set `M1_S2_R1_DISPOSITION = BLOCKED_INFRASTRUCTURE`;
- H1 remains `UNADJUDICATED_DUE_TO_INFRASTRUCTURE_BLOCK`;
- do not rerun.

If authorized nine produces a normal test-failure result (`exit 1` with valid JUnit), continue the preregistered module and full-suite measurements once each so the falsification record is complete.

### B8. Original falsification conditions preserved

If all three measurements are result-bearing, H1 is falsified if any of the following occurs:

1. either preregistered residual function still fails;
2. either residual failure's first causal failure is unrelated to AUDIT-004 presence;
3. any new failure appears among the other 21 `_isolated` callers;
4. any of the seven M1-S1-resolved failures regresses;
5. any failure outside `tests/test_audit_lineage.py` changes state in either direction;
6. full-suite failure count is anything other than exactly 23;
7. `R1 − S1` is non-empty;
8. execution requires any scientific mutation beyond the one authorized fixture-local site;
9. canonical governed source is modified.

A falsified result is evidence. It is not permission to modify the experiment until green.

If all preregistered predictions and directed-difference conditions hold and no falsification condition is met, return:

`M1_S2_R1_DISPOSITION = H1_SUPPORTED_BY_PREREGISTERED_R1`

If complete result-bearing measurements violate one or more falsification conditions, return:

`M1_S2_R1_DISPOSITION = H1_FALSIFIED_BY_PREREGISTERED_R1`

No stronger scientific claim is authorized.

## 8. Combined evidence transaction

Both phases use one evidence branch and one final evidence PR.

Branch:

`evidence/m1-closure-001`

Paths:

`stage-m1-closure/**`

Minimum governing records:

1. `01-M1-CLOSURE-OWNER-AUTHORIZATION-REFERENCE.json`
2. `02-M1-CLOSURE-PREDECESSOR-CHAIN.json`
3. `03-M1-CLOSURE-ENV-IDENTITY-PREFLIGHT.json`
4. `04-M1-CLOSURE-ENV-QUALIFICATION-EVIDENCE.json`
5. `05-M1-CLOSURE-PHASE-A-ACTIVATION.json`
6. `06-M1-CLOSURE-R1-RECONSTRUCTION-CONFINEMENT.json`
7. `07-M1-CLOSURE-R1-PREREGISTERED-HYPOTHESIS.json`
8. `08-M1-CLOSURE-R1-AUTHORIZED-NINE-EVIDENCE.json`
9. `09-M1-CLOSURE-R1-MODULE-EVIDENCE.json`
10. `10-M1-CLOSURE-R1-SUITE-EVIDENCE.json`
11. `11-M1-CLOSURE-R1-DIRECTED-DIFFERENCE.json`
12. `12-M1-CLOSURE-R1-ADJUDICATION.json`
13. `13-M1-CLOSURE-COMMAND-MATRIX.json`
14. `14-M1-CLOSURE-RETURN-FINAL.md`
15. `15-M1-CLOSURE-EVIDENCE-MANIFEST.json`

plus raw evidence under:

`stage-m1-closure/evidence/**`

If Phase A fails or blocks, records 06–12 must explicitly state `NOT_EXECUTED_PHASE_B_INACTIVE` rather than fabricate measurement content.

The manifest is self-excluded and must bind every other persisted member by path, bytes, SHA-256, and SHA-512.

No governing ZIP.

Exactly one evidence commit is authorized after the transaction stops or completes.

The implementer must run Review Ledger mechanical verification at the exact evidence head, push once, open one PR to `main`, request `inventor1975`, and not merge.

## 9. Explicit non-authorizations

This decision does NOT authorize:

- mutation of the canonical governed repository;
- any second scientific edit;
- durable refactoring of `_isolated`;
- dynamic `current_report_id` derivation;
- package installation, upgrade, downgrade, removal, repair, or relinking;
- venv modification, replacement, or creation;
- interpreter replacement;
- persistent shell/environment changes;
- system locale changes;
- any qualification retry;
- any R1 rerun;
- retry-until-green behavior;
- M1-R;
- N2a-2;
- N2b;
- N2c;
- M2;
- Stage B1;
- semantic implementation;
- Golden Mission.

Those later work items are not blocked conceptually by this document; they simply are not executed inside this M1 closure transaction.

## 10. Review and persistence gate

Before execution begins, this exact revised artifact must:

1. pass Review Ledger mechanical verification at its exact revised PR head;
2. receive a fresh non-author independent review by `inventor1975` on that revised head;
3. be explicitly owner-ratified at that reviewed head;
4. be persisted without changing reviewed artifact bytes or commit/tree identity.

The earlier review `4889581777` on `cb2369b89c736ab4b704fd53eae1cbe59d286515` cannot satisfy this gate.

After the combined evidence PR is created:

- CI PASS is not acceptance;
- independent review is not owner acceptance;
- merge is not owner acceptance;
- no M1 closure result becomes accepted state until owner disposition and exact persistence.

## 11. Implementer return

Return exactly:

`M1_CLOSURE_EVIDENCE_READY_FOR_INDEPENDENT_REVIEW`

followed by:

- `phase_a_disposition = QUALIFIED | FAILED | BLOCKED`
- `environment_id = M1-S2-ENV-001`
- `environment_delta = LANG=C, LC_ALL=C, LC_CTYPE=C`
- `qualification_trials_attempted = <n>`
- `qualification_trials_passed = <n>`
- `phase_b_authority = ACTIVE_BY_PREAUTHORIZED_CONDITION | INACTIVE`
- `m1_s2_r1_executed = true | false`
- `m1_s2_r1_disposition = H1_SUPPORTED_BY_PREREGISTERED_R1 | H1_FALSIFIED_BY_PREREGISTERED_R1 | BLOCKED_INFRASTRUCTURE | NOT_EXECUTED_PHASE_B_INACTIVE`
- `authorized_nine = <counts or NOT_EXECUTED>`
- `module = <counts or NOT_EXECUTED>`
- `full_suite = <counts or NOT_EXECUTED>`
- `pytest_runs = <0 or exactly the executed R1 measurement count>`
- `m1_s2_measurement_reruns = 0`
- `r1_reruns = 0`
- `canonical_source_mutations = 0`
- `scientific_edits = <0 if Phase B inactive; exactly 1 if Phase B executed>`
- `package_mutations = 0`
- `venv_mutations = 0`
- `interpreter_mutations = 0`
- `persistent_environment_mutations = 0`
- `original_M1_S2 = BLOCKED`
- `H1 = <supported/falsified/unadjudicated according to §7>`
- evidence commit/tree
- manifest bytes/SHA-256/SHA-512
- exact-head CI run/result
- PR URL

Do not proceed beyond that evidence PR.

## 12. Owner decision

Subject to the fresh exact-head review-and-persistence gate in §10, I authorize:

`AUTHORIZE_M1_CLOSURE_ENV_001_CONDITIONAL_M1_S2_R1_001`

The authority is intentionally conditional:

- Phase A is active after persistence;
- Phase B is dormant after persistence;
- Phase B becomes active automatically only if §6 evaluates true;
- no discretionary governance transaction occurs between Phase A qualification and the preregistered R1 measurement.

Arkadiy Miteiko  
Owner / Design Authority  
2026-08-08
