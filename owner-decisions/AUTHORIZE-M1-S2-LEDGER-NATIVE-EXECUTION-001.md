# M1-S2 Ledger-Native Execution — Owner Authorization 001

Document ID: `M1-S2-LEDGER-NATIVE-EXECUTION-OWNER-AUTHORIZATION-001`

Owner / Design Authority: Arkadiy Miteiko

Repository: `veraxis-protocol/Institutional-Compiler-Review-Ledger`

Decision tokens:

- `ACCEPT_N2A_1_M1_S1_SEVEN_FUNCTION_LOCAL_EDITS_MEASUREMENT_OWNER_001`
- `AUTHORIZE_M1_S2_LEDGER_NATIVE_EXECUTION_001`

Status of this document before persistence: **OWNER-AUTHORED CANDIDATE — NOT YET EXECUTABLE**

This owner decision becomes executable authority only after this exact artifact is independently reviewed, mechanically verified at its exact PR head, owner-ratified as that reviewed artifact, and persisted to Review Ledger `main`. A branch commit, CI PASS, independent review, or merge event alone is not execution authority.

## 1. Review Ledger prerequisite

The Review Ledger operational activation is accepted and persisted.

Required activation coordinate:

- ledger `main`: `ecdabc7ba4ca026391f0b64b6d793df67abecc29`
- tree: `25f1cdab32b5e21de0e2d73b69a4a3ea10997042`
- machine state: `REVIEW_LEDGER_ACTIVE`

M1-S2 is the first native ledger-carried experiment. M1-S1 remains historical under the legacy pre-ledger transport channel.

## 2. M1-S1 predecessor disposition

I accept the independently reviewed M1-S1 measurement as the predecessor experimental state for M1-S2.

Owner predecessor decision:

`ACCEPT_N2A_1_M1_S1_SEVEN_FUNCTION_LOCAL_EDITS_MEASUREMENT_OWNER_001`

Frozen M1-S1 measurement:

- artifact: `m1-s1-measurement-001.zip`
- record class: `FROZEN_M1_S1_MEASUREMENT`
- transport class: `LEGACY_PRE_LEDGER`
- bytes: `103189`
- SHA-256: `e9250d1938bbbd5f607add695ce2273c52d00428da26481834b2dd020348d30a`
- SHA-512: `958cf6449f9d7a838bac755e029421ced5de15a5a6bed18f9ce65ed15fafd9b9f77709fbd4e541bedd94fa44055e28dae557a1ce1122ea4331f922320abed5f5`

Independent review return:

- artifact: `OAM-CDC-PROFILE-CORRECTION-M1-S1-SEVEN-FUNCTION-LOCAL-EDITS-MEASUREMENT-INDEPENDENT-REVIEW-RETURN-001.md`
- bytes: `10032`
- SHA-256: `70de1db94b63702a83e6dd0f5377fcdb1795bcb1be6b219fe712f7fd85f4a4d6`
- SHA-512: `21be1bb37b2ae041617ecae3a4a25df248e699c615348d39ddb4fa161cc9e4ecb9894a5879d50d72d15086ddc669e7ec90a02d747d2b3ca58a86e2ba125b1641`
- reviewer: Vitaliy Reznik / GitHub `inventor1975`
- accepted review token: `ACCEPT_N2A_1_M1_S1_SEVEN_FUNCTION_LOCAL_EDITS_MEASUREMENT_001`

Accepted M1-S1 measured state:

- target population: 7 functions / 9 IDs
- authorized local intervention: 7 enumerated edit sites
- functions actually changed: 5
- authorized nine: `7P / 2F`
- module: `85P / 2F`
- full suite: `1009P / 25F / 7S`
- exactly 7 targeted failures resolved
- zero new failures
- `_isolated` unchanged
- fixture callers: 23
- two residual failures are fixture-mediated and trace to the isolated reconstruction lacking AUDIT-004

The §5/§6 discrepancy is owner-disposed as a defective expected metric, not a confinement failure: the seven authorized edit sites exist in five functions. Requiring seven changed functions would require invention of unauthorized edit sites.

This acceptance does not retroactively make M1-S1 ledger-native and does not mutate the governed source.

## 3. Governed-source coordinate

Canonical governed repository coordinate for the experiment:

- accepted HEAD: `9b1754040c3dafa0123c6b13ea9e5f5eaa2b7bd1`
- accepted tree: `8d898a5d69164db1d4d64e08fb7b71facf459e8b`

Canonical governed repository mutation authority:

`NONE`

Canonical governed repository mutated by M1-S2:

`false`

Any mismatch in this accepted source coordinate at execution time is a hard STOP.

The experiment must occur only in a disposable reconstruction derived from this accepted coordinate plus the accepted M1-S1 predecessor state.

## 4. M1-S2 mission authorization

I authorize:

`AUTHORIZE_M1_S2_LEDGER_NATIVE_EXECUTION_001`

Purpose: perform one preregistered causal experiment testing whether the two residual M1-S1 failures are caused by `_isolated` reproducing AUDIT-003 but not the current AUDIT-004 report.

Disposable reconstruction mutation authority:

`EXACTLY_ONE_AUTHORIZED_FIXTURE_LOCAL_EDIT`

Exact intervention:

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
- no helper, import, module-global, production, schema, policy, or canonical governed-source change is authorized.

No second corrective edit is authorized if the hypothesis fails.

## 5. Precondition identity and current-report binding

M1-S1 precondition:

- authorized nine: `7P / 2F`
- module: `85P / 2F`
- suite: `1009P / 25F / 7S`
- S1 test file: 40975 bytes / SHA-256 `8e6f51a1613456f4a52ce37f1da8f999694fb3195da10c7dc78697b1f9c57410`
- `_isolated`: 1109 bytes / SHA-256 `766f1f66e03bb82f043263c60d6a437a2818793bd07a2ba29ed8ff69911e9431`
- `_isolated` callers: 23

AUDIT-004 identity:

- path: `docs/governance/gates/OAM-GATE-SAR-05-CDC-PROFILE-AUDIT-004.json`
- bytes: `13494`
- SHA-256: `0c7143c500d7912dca95cd01301a2d388c3f8c46ffc3427c95e2089e5425e631`
- SHA-512: `7ca118fe5ed9e75926dd3b8efe12a649fa0afc168f0a3b6104356a9e8a83b0797b6fe0e4a22fb64cba066d76316ad63a6b0e86f56c6f9f97e1c1171adb406c7d`

Operational index:

- path: `docs/governance/gates/OAM-GATE-SAR-05-CDC-AUDIT-INDEX.json`
- bytes: `4204`
- SHA-256: `20de3c39d714f392d6511efc9aeb2b49a011c9a168baa1a7d683ee8c202bb376`
- SHA-512: `f28a58aebf2e207c820f93cf47592424395c04fb23a82389ae2ba2d6f7eeb95a3fa545f684fbedd67d1cf44c6f13151c8221fa33d335b1b451f7fd6c1decacf9`
- `current_report_id`: `OAM-GATE-SAR-05-CDC-PROFILE-AUDIT-004`
- reports: 4

The causal intervention is therefore not an arbitrary report substitution. It tests the mismatch between the operational index's declared current report and the file copied into the isolated reconstruction.

## 6. Preregistered hypothesis

H1:

The two remaining M1-S1 failures persist because `_isolated` reproduces AUDIT-003 but does not reproduce AUDIT-004.

Predicted M1-S2 result if H1 is true:

- authorized nine: `9P / 0F`
- module: `87P / 0F`
- suite: `1011P / 23F / 7S`
- new failures: `0`

Required suite failure-set difference:

- `S1 − S2` = exactly:
  - `tests/test_audit_lineage.py::test_governed_success_tokens_are_distinct`
  - `tests/test_audit_lineage.py::test_valid_confined_alternate_index_is_accepted`
- `S2 − S1` = empty

The previously stated `1034P / 0F / 7S` prediction is expressly withdrawn and must not appear in execution evidence.

## 7. Falsification / STOP conditions

H1 is falsified, and no corrective follow-on is authorized, if any of the following occurs:

1. either preregistered residual function still fails;
2. either residual failure's first causal failure is unrelated to AUDIT-004 presence;
3. any new failure appears among the other 21 `_isolated` callers;
4. any of the seven M1-S1-resolved failures regresses;
5. any failure outside `tests/test_audit_lineage.py` changes state in either direction;
6. full-suite failure count is anything other than exactly 23;
7. `S2 − S1` is non-empty;
8. execution requires any mutation beyond the one authorized fixture-local site;
9. canonical governed source is modified.

A falsified result is evidence. It is not permission to modify the experiment until green.

## 8. Ledger-native evidence transport

Authorized evidence branch:

`evidence/m1-s2-001`

Authorized path class:

`stage-m1-s2/**`

Implementer role:

`IMPLEMENTER_EXECUTION`

Independent reviewer:

Vitaliy Reznik / GitHub `inventor1975`

Governing transport:

`LEDGER_COMMIT_PLUS_MANIFEST_PLUS_EXACT_HEAD_CI`

No governing ZIP is required.

The M1-S2 evidence record must include at minimum:

- `01-M1-S2-OWNER-AUTHORIZATION-REFERENCE.json`
- `02-M1-S2-PRECONDITION-AND-S1-IDENTITY.json`
- `03-M1-S2-FIXTURE-PATCH-CONFINEMENT-REPORT.json`
- `04-M1-S2-PREREGISTERED-HYPOTHESIS.json`
- `05-M1-S2-AUTHORIZED-NINE-EVIDENCE.json`
- `06-M1-S2-MODULE-EVIDENCE.json`
- `07-M1-S2-SUITE-EVIDENCE.json`
- `08-M1-S2-S1-TO-S2-DIRECTED-DIFFERENCE-REPORT.json`
- `09-M1-S2-HYPOTHESIS-ADJUDICATION.json`
- `10-M1-S2-VERIFICATION-COMMAND-MATRIX.json`
- `11-M1-S2-RETURN-FINAL.md`
- `12-M1-S2-EVIDENCE-MANIFEST.json`
- corresponding raw evidence under `stage-m1-s2/evidence/**`

`12-M1-S2-EVIDENCE-MANIFEST.json` is self-excluded and every member row must bind `path`, `bytes`, `sha256`, and `sha512`.

`01-M1-S2-OWNER-AUTHORIZATION-REFERENCE.json` must resolve this persisted owner-decision artifact by exact ledger commit, ledger path, bytes, SHA-256, SHA-512, and owner decision identifier. It must use a resolved state. An unresolved authorization reference prohibits execution.

## 9. Review and acceptance boundaries

Before implementer execution begins, this exact owner-authorization artifact must:

1. be committed alone under `owner-decisions/**` on an `owner/` branch;
2. pass Review Ledger mechanical verification at the exact PR head;
3. receive non-author independent review by `inventor1975`;
4. be explicitly owner-ratified at that reviewed head;
5. be persisted without changing the reviewed artifact bytes or commit/tree identity.

After M1-S2 evidence is committed:

- CI PASS is not acceptance;
- independent-review ACCEPT is not owner acceptance;
- merge is not owner acceptance;
- no result becomes an accepted experimental state without a separate owner disposition and persistence event.

## 10. Explicit non-authorizations

This decision does NOT authorize mutation of the canonical governed repository, Stage B1, semantic implementation, Golden Mission execution, M1-R, M2, durable refactoring of `_isolated`, dynamic `current_report_id` derivation, any second experimental edit, signed-tag claims, history rewrite, or force push.

Owner signing identity may remain `PENDING_BOOTSTRAP_SETUP`; no signed-tag claim is made.

## 11. Owner decision

Subject to the review-and-persistence gate in §9, I:

1. accept the independently reviewed M1-S1 measurement as the predecessor state; and
2. authorize the exactly bounded M1-S2 ledger-native experiment described above.

`ACCEPT_N2A_1_M1_S1_SEVEN_FUNCTION_LOCAL_EDITS_MEASUREMENT_OWNER_001`

`AUTHORIZE_M1_S2_LEDGER_NATIVE_EXECUTION_001`

Arkadiy Miteiko
Owner / Design Authority
2026-08-08
