# RESULT-001 Capability Matrix 003 — decisive comparison

Restricted to the ten strongest systems after this pass, scored against the ten chain stages of §6 of the work order plus the three adversarial columns. Every YES/PARTIAL carries a source section. Rows marked *(planned)* are design-level and are never compared as measured.

## Chain-stage columns

S1 logical/epistemic support · S2 present rule currentness · S3 present actor authority · S4 institutional authorization status · S5 runtime execution disposition · S6 bounded action consequence · S7 governed propagation · S8 downstream consumer revalidation · S9 separate reliance issuance · S10 preserved historical evidence after governing-state change
**Adversarial:** X1 not-evaluated-with-cause · X2 unresolved third value · X3 measured execution

| System | status | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | S10 | X1 | X2 | X3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Proof of Execution** RW027 | measured impl. | **NO**¹ | PARTIAL² | YES | PARTIAL | YES | YES | YES | **NO**³ | **YES**⁴ | **YES**⁵ | **NO**⁶ | NO⁷ | YES |
| **Mandato** RW030 *(planned)* | design only⁸ | NO | PARTIAL⁹ | YES | PARTIAL | **YES**¹⁰ | YES | YES | NO | PARTIAL | **YES**¹¹ | **NO** | PARTIAL¹² | **NO**⁸ |
| **Governing Actions** RW028 | proof-of-concept | NO | PARTIAL¹³ | YES | PARTIAL | YES | YES | YES | PARTIAL¹⁴ | PARTIAL | PARTIAL | **NO** | NO | PARTIAL |
| **Five-Plane** RW029 | measured core | NO | **NO**¹⁵ | YES | PARTIAL | **YES**¹⁶ | YES | PARTIAL | NO | NO | PARTIAL | **NO** | PARTIAL¹⁶ | PARTIAL |
| **SLSA v1.2** RW019/020 | deployed | NO | NO | YES | PARTIAL | NO | NO | YES | PARTIAL | YES | PARTIAL | NO | NO | YES |
| **Certificate Transparency** RW021 | deployed | NO | PARTIAL | PARTIAL | NO | NO | NO | YES | YES | YES | **YES** | NO | NO | YES |
| **ETSI EN 319 102-1** RW022 | deployed | PARTIAL | PARTIAL | PARTIAL | YES | NO | NO | NO | NO | PARTIAL | NO | PARTIAL¹⁷ | **YES**¹⁸ | YES |
| **VC-DM 2.0** RW012 | deployed | NO | PARTIAL | PARTIAL | NO | NO | NO | YES | YES | YES | NO | NO | NO | YES |
| **BP compliance (CMF)** RW031 | peer-reviewed framework | PARTIAL | **NO**¹⁹ | PARTIAL | PARTIAL | PARTIAL | NO | NO | NO | NO | PARTIAL | **NO**²⁰ | **NO**²¹ | YES |
| **LegalRuleML** RW002 | standard | PARTIAL | **YES** | PARTIAL²² | NO | NO | NO | NO | NO | NO | NO | NO | PARTIAL | NO |
| **RESULT-001** (for reference) | measured | YES | YES | YES | YES | YES | YES | YES | YES | YES | YES | YES | YES | YES |

## Cell notes

1. RW027 full text — regex over 45,880 characters returns **zero** hits for epistemic / truth / logical warrant / belief.
2. RW027 §2 — the contract carries an "applicable policy snapshot" and a validity window; policy identity is pinned, but supersession of the governing rule is not evaluated as a gate.
3. RW027 — **zero** hits for re-verify / re-evaluate / re-resolve / independently.
4. RW027 §7.2 — "An Execution Attestation Certificate (EAC) is issued only when PoE = 1." Issuance strictly downstream of evaluation.
5. RW027 §7.2 — "revocation at t=5 does not retrospectively invalidate an execution that was valid at t=3"; "Historical PoE validity is not rewritten; only current EAC acceptability changes."
6. RW027 — **zero** hits for not-evaluated / skipped / short-circuit.
7. RW027 §2.2 — event decision ∈ {allow, deny, ⊥}, where ⊥ marks non-Gateway events, not institutional non-resolution.
8. RW030 — "MANDATO is a system under construction … empirical results are defined as a falsifiable plan rather than reported."
9. RW030 — mandate validity windows and revocation; per §10 these are credential-validity, not rule currentness.
10. RW030 — δ(c,ℳ) ∈ {PERMIT, ESCALATE, DENY}, deny-by-default.
11. RW030 — "history is corrected by appending, never by editing"; ratification changes legal posture without rewriting the log.
12. RW030 — ESCALATE is an oversight class (human confirmation), not an unresolved-authority finding.
13. RW028 — names the gap directly: "a licence may be revoked, a build superseded, a drug interaction newly identified", bounded by attestation expiry rather than re-resolution.
14. RW028 — "any authorised third party can later inspect and re-verify the decision" — retrospective audit, not pre-issuance revalidation.
15. RW029 — **zero** hits for revocation / supersede / currentness.
16. RW029 — "Production-agent governance requires richer outcomes — modify the arguments, narrow the capability set, escalate to a human, defer pending a condition, roll back a committed effect — that a Boolean evaluator cannot express."
17. RW022 — SubIndications record the cause of a non-determinate outcome, but not that a later check was skipped because an earlier one stopped the path.
18. RW022 — INDETERMINATE: verifications "have not failed but there is insufficient information to determine".
19. RW031 — CMF1 covers time *within* rules; no CMF covers rule lifecycle or validity windows.
20. RW031 — no CMF covers a rule left unevaluated because an earlier constraint terminated the path.
21. RW031 — no third state; CMF10 offers degrees between violation and satisfaction only.
22. RW002 — authority as norm provenance, not an actor's present authority to act.

## Reading of the matrix

Two columns separate RESULT-001 from every row above it: **S8 downstream consumer revalidation** and **X1 not-evaluated-with-cause**, with **S1 logical/epistemic support** a third that no agent-governance system carries at all.

Everything else is now populated somewhere. S9 and S10 are both YES for Proof of Execution — a measured implementation. S5's richness is argued and measured by Five-Plane. X2 is deployed in ETSI. S7 is common across the attestation family.
