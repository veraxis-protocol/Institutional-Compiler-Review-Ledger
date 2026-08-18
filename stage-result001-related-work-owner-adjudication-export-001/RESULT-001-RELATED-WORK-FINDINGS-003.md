# RESULT-001 Related-Work Findings 003 — Decisive Gap Closure

**Predecessors preserved.** Manuscript frozen. Publication not authorized.

> **SEARCH_COMPLETENESS_IS_NOT_CLAIMED. ABSENCE_FROM_SEARCH_RESULTS_IS_NOT_PROOF_OF_NOVELTY.**

## 1. Executive decision

The decisive pass cuts both ways, and the net effect is a **narrower but clearer** position.

**Against the manuscript.** Proof of Execution (Rhodes & Kang, AlphaBitCore, April 2026) is a measured implementation that issues an Execution Attestation Certificate **only when its validity predicate holds** — evaluation strictly gating issuance, which is exactly RESULT-001's `EVALUATION ESTABLISHES THE PROPERTY; ISSUANCE CREATES THE RELIANCE`. It also states that "revocation at t=5 does not retrospectively invalidate an execution that was valid at t=3" and that "historical PoE validity is not rewritten; only current EAC acceptability changes." **D5 and D7 are now preceded by a single measured system.** Separately, the Five-Plane architecture argues with a measured core that Boolean allow/deny is structurally insufficient and enumerates escalate and defer as required outcomes, which narrows the four-field framing.

**For the manuscript.** The business-process compliance gap — GAP-CLOSURE-002's highest-priority risk — closed in RESULT-001's favour on the narrow point. The authoritative ten-functionality CMF taxonomy has root-cause analysis for *violations* (CMF9) and no functionality for a rule left unevaluated because an upstream gate stopped the path. And all four contemporary agent-governance sources return **zero** hits for not-evaluated, skipped or short-circuit. Proof of Execution likewise returns **zero** hits for re-verify, re-evaluate, re-resolve, and **zero** for epistemic, truth or logical warrant.

**Determination: INTEGRATED_CHAIN_DISTINCTION_SURVIVES**, resting on three things and nothing more — a preserved epistemic layer that no agent-governance system carries, downstream revalidation that re-resolves currentness and re-evaluates authority before issuance, and a not-evaluated-with-cause record. Five claims remain POTENTIALLY_DISTINCTIVE, one of which (R050) is explicitly demoted to an implementation invariant.

## 2. Sources added / upgraded

**RW027 upgraded** from abstract-only CHALLENGE/WEAK to full-text PARTIAL_PRECEDENT/STRONG; identity and affiliation verified (AlphaBitCore, Inc.). **RW028, RW029, RW030, RW031 newly admitted, all full text.** Consolidated total 31 sources; 20 now at full text or normative sections; 15 STRONG.

## 3. Proof of Execution — full comparison

| RESULT-001 property | PoE | verdict |
|---|---|---|
| evaluation gates issuance | EAC issued only when PoE = 1 | **preceded** |
| history preserved under later revocation | point-in-time predicate; historical validity not rewritten | **preceded** |
| tamper-evident chain evidence | ECES, envelope and event hashing, sealed commit order | **preceded** |
| plane separation | PEM separates planning / enforcement / effect / recordkeeping | **preceded** |
| deny produces no effect | invariant I3, deny-side null effect | **preceded** |
| epistemic layer | **zero** textual hits | **survives** |
| downstream re-resolution | **zero** textual hits | **survives** |
| not-evaluated-with-cause | **zero** textual hits | **survives** |
| unresolved third value | decision ∈ {allow, deny, ⊥}; ⊥ marks non-Gateway events | **survives** |

PoE is the strongest single precedent found in the whole programme. It binds authorization, effect, history and replay in a measured system; it does not carry a logical-warrant layer, does not re-derive governing state downstream, and does not record a question it never asked.

## 4. Governing Actions, Not Agents

A proof-of-concept where a hub issues an intent identifier, oracles supply signed attestations the agent cannot fabricate, a deterministic Cedar policy decides, and the decision plus evidence plus rule are logged so "any authorised third party can later inspect and re-verify the decision." It names the currentness problem more directly than any other examined source — "a licence may be revoked, a build superseded, a drug interaction newly identified" — and bounds it with attestation expiry. Its re-verification is retrospective audit, not pre-issuance revalidation, so it does not reach D6.

## 5. Five-Plane Reference Architecture

Measured policy-engine core. Its critique is directly on point for R019 and R046: "Production-agent governance requires richer outcomes — modify the arguments, narrow the capability set, escalate to a human, defer pending a condition, roll back a committed effect — that a Boolean evaluator cannot express." Zero hits for currentness, epistemic, or not-evaluated. It narrows the disposition-richness framing without touching the chain distinction.

## 6. Mandato

Design-level only, and it says so: "MANDATO is a system under construction … empirical results are defined as a falsifiable plan rather than reported." Read as DESIGNED per §13. It has PERMIT/ESCALATE/DENY, mandate chains with monotone attenuation, revocation, PDP/PEP separation, an append-only hash-chained log, and ratification that changes an action's legal posture "without ever rewriting the log." Its ESCALATE is an oversight class requiring human confirmation, not an unresolved-authority finding. Because it is unimplemented it cannot precede a measured demonstration.

## 7. Business-process compliance closure

The ten CMFs: time, data, resources, non-atomic activities, activity lifecycles, multiple instances, reactive detection, proactive detection, root-cause explanation, degree of compliance.

- **No CMF covers a rule not reached because an earlier constraint terminated the path.** CMF9 diagnoses the root cause of a *violation*.
- **No CMF covers the temporal validity of the compliance rule itself** — CMF1 is time *within* rules.
- **No third compliance state**; CMF10 offers degrees between violation and satisfaction.

The family GAP-CLOSURE-002 flagged as most likely to defeat D9 does not defeat it.

## 8. D6 / downstream revalidation — adversarial test

| system | receives persisted material | re-resolves current state | re-evaluates authority | before issuance |
|---|---|---|---|---|
| PoE | yes | no | no | n/a |
| Governing Actions | yes | no (expiry bound) | no | no — later audit |
| Mandato | yes | design-level | design-level | no |
| SLSA | yes | no | no | consumer may re-check evidence |
| CT | yes | no | no | monitors act later |
| VC-DM | yes | verifies currency of the *statement* | no | validation out of scope |
| in-toto | yes | no | authorized-functionary check | verification, not issuance |

**Disposition: SURVIVES_AS_INTEGRATION.** No examined system has the downstream party re-resolve the governing rule's currentness *and* re-evaluate the actor's authority at its own instant *before* issuing a reliance-bearing artifact. Signature verification, provenance verification, credential verification and policy re-evaluation all appear; fresh currentness resolution paired with authority re-evaluation does not.

## 9. D8 integrated-evidence — adversarial test

| system | authorization | effect | history | policy id | logical state | currentness | authority | decision basis | downstream validation | reliance issuance |
|---|---|---|---|---|---|---|---|---|---|---|
| PoE | yes | yes | yes | yes | **no** | partial | yes | partial | no | yes |
| Mandato *(planned)* | yes | yes | yes | yes | no | partial | yes | partial | no | partial |
| SLSA | yes | partial | yes | yes | no | no | yes | partial | partial | yes |
| CT | partial | no | yes | no | no | partial | partial | no | yes | yes |
| RESULT-001 | yes | yes | yes | yes | **yes** | **yes** | yes | **yes** | **yes** | yes |

**Disposition: PARTIALLY_PRECEDED** (down from SURVIVES_AS_INTEGRATION). PoE persists authorization, effect, history, policy identity and issuance in a measured system. What no examined evidence package preserves is the logical state alongside currentness, authority and a typed decision basis.

## 10. D9 — not-evaluated with cause

Four-way test applied. XACML short-circuits without recording (C). ETSI records the cause of a non-determinate outcome (near-B/D but not gate-ordering). CMF9 explains violations (A). PoE, Governing Actions, Five-Plane and Mandato: zero hits each. **No examined source reaches (D).**

**Disposition: SURVIVES_AS_INTEGRATION**, confidence moderate — raised from moderate-low, because the family most likely to contain it has now been read and does not.

## 11. Currentness versus validity

Kept distinct throughout, per §10. PoE pins a *policy snapshot* and a contract *validity window*; Mandato has *mandate validity*; VC-DM has *credential validity*; Governing Actions has *attestation expiry*. None of these is a determination that the governing rule has been superseded and that a superseding version now governs. LegalRuleML models in-force/efficacious/applicable at the representation layer but never at runtime. **RESULT-001's currentness gate remains distinct from every time-bounding mechanism examined**, though the distinction is narrow and easily overstated.

## 12. Authority versus authorization

Also kept distinct. PoE, Mandato and Governing Actions all bind a *principal* and a *capability set* and check them — actor authorization. None evaluates competing operative authority bases with no precedence (A6) or distinguishes a revoked basis (A10) from an out-of-scope request (A3) as institutional findings. LegalRuleML's Authority is norm provenance. Permit/deny is nowhere mapped to epistemic support in the examined set, which is consistent with RESULT-001's design and means the mapping is not preceded either.

## 13. Updated D1–D10

| # | GAP-CLOSURE-002 | DECISIVE-003 | changed | strongest source | confidence |
|---|---|---|---|---|---|
| D1 | PARTIALLY_PRECEDED | PARTIALLY_PRECEDED | no | RW002, RW004, RW006 | high |
| D2 | PARTIALLY_PRECEDED | PARTIALLY_PRECEDED | no | RW002, RW026, RW028 | high |
| D3 | PARTIALLY_PRECEDED | PARTIALLY_PRECEDED | no | RW022, RW030 | high |
| D4 | PARTIALLY_PRECEDED | PARTIALLY_PRECEDED | no | RW029, RW004 | high |
| D5 | PARTIALLY_PRECEDED | **PRECEDED** | **yes** | **RW027** | high |
| D6 | SURVIVES_AS_INTEGRATION | SURVIVES_AS_INTEGRATION | no | RW028, RW012 | moderate-high |
| D7 | PARTIALLY_PRECEDED | **PRECEDED** | **yes** | **RW027**, RW030, RW021 | high |
| D8 | SURVIVES_AS_INTEGRATION | **PARTIALLY_PRECEDED** | **yes** | RW027 | high |
| D9 | SURVIVES_AS_INTEGRATION | SURVIVES_AS_INTEGRATION | no | RW031, RW022 | moderate |
| D10 | PARTIALLY_PRECEDED | PARTIALLY_PRECEDED | no | RW022, RW017 | high |

## 14. Top-five strongest precedents

1. **Proof of Execution (RW027)** — measured. Covers S3–S7, S9, S10. Missing S1, S8, X1, X2. Preserves authorization/effect/history/policy identity; collapses epistemic and institutional status into allow/deny. No downstream revalidation. EAC is a genuine reliance artifact gated on evaluation.
2. **SLSA v1.2 (RW019/020)** — deployed. Covers S3, S7, S9, partial S8/S10. Missing S1, S2, S5, X1, X2. Collapses to PASSED/FAILED. Consumers may re-check evidence.
3. **Certificate Transparency (RW021)** — deployed. Covers S7–S10 strongly. Missing S1–S6, X1, X2. Preserved history with changing reliance; response excluded from protocol.
4. **ETSI EN 319 102-1 (RW022)** — deployed. Covers S4 and X2 uniquely well, partial S1/S2/S3. Missing S6–S10, X1.
5. **Business-process compliance / CMF (RW031)** — peer-reviewed framework. Covers runtime detection and root-cause of violations. Missing rule lifecycle, third state, X1, S9, S10.

**Strongest combined set: RW027 + RW019 + RW021 + RW022.** Together these cover every chain stage except S1, S8 and X1.

## 15. Component-level determination (LEVEL 1)

**Clearly preceded:** rule representation from authoritative source; logical warrant as a checkable object; temporal applicability of norms; delegation; revocation; runtime authorization; separation of decision from enforcement; fail-closed on unknown; governed propagation; hash-resolvable evidence; issuance as a controlled act; preserved history under later change; a third non-determinate verdict; richer-than-Boolean dispositions; separate judgment over an evidence package.

**Nothing at component level survives as distinctive.**

## 16. Composition-level determination (LEVEL 2)

**Preceded:** evaluation→issuance (RW027); evidence→separate judgment→consumer re-check (RW019); issuance→immutable history→later changed reliance (RW021, RW027); decision→enforcement separation (RW004, RW030); verdict→recorded cause (RW022).

**Surviving compositions:** epistemic status preserved *alongside* institutional authorization and execution disposition and a typed basis in one record; and currentness gating *whether authority is evaluated at all*, with that non-evaluation recorded.

## 17. Integrated-chain determination (LEVEL 3)

**INTEGRATED_CHAIN_DISTINCTION_SURVIVES.**

Resting on exactly three properties, all measured in RESULT-001 and absent from every examined system: **S1** a preserved logical/epistemic state carried through an institutional decision chain; **S8** downstream revalidation that re-resolves currentness and re-evaluates authority before issuance; **X1** a not-evaluated-with-cause record. Remove any one and the position is weak; remove two and there is no publishable distinction.

## 18. Claims requiring narrowing

R004, R019, R025, R031, R039, R053, R007, R028, R051 — with R019 and R039 the most affected by Five-Plane's measured critique of Boolean dispositions, and R053 by PoE's validator/attestation/record separation.

## 19. Claims requiring citation or context

R010 and R052 must now cite RW027 explicitly rather than being narrowed. R043 must be stated against PoE's EAC and SLSA's VSA. R029 against CMF9. R046 against Five-Plane. Twenty-two PARTIALLY_PRECEDED claims carry CITE.

## 20. Publication contribution recommendation

Present RESULT-001 as an **integration result with a measured execution**, positioned explicitly against Proof of Execution as the nearest neighbour. The defensible sentence is roughly: *among the systems examined, none preserves a logical/epistemic state alongside institutional authorization, execution disposition and a typed basis through one executed chain in which a downstream consumer re-resolves currentness and re-evaluates authority before reliance is issued, and in which a gate not reached is recorded as such with its cause.*

Do not lead with reliance issuance (preceded), history preservation (preceded), hash-resolvable evidence (preceded) or R050.

## 21. Remaining material gaps

1. **Patents — DEFERRED** by §17 to a separate IP analysis. Not blocking.
2. **DMN and Blawx — NOT BLOCKING**; nothing examined shows either threatens D6, D8 or the chain determination.
3. **Contemporary preprint velocity** — three of the four agent-governance sources appeared within five months of this search. This area will need re-checking immediately before submission, not because of a known gap but because the gap rate is high.
4. **PoE follow-on work** unexamined; a successor adding downstream revalidation would defeat the surviving distinction.
5. No dedicated academic database queried directly; no non-English sources.

## 22. Recommendation

**READY_FOR_OWNER_RELATED_WORK_ADJUDICATION.**

Every acceptance-gate item is met: RW027 resolved and read in full, all three named contemporary sources fully reviewed, the business-process full-text gap closed, D6/D8/D9 re-adjudicated, the top-five ranking reissued, the contribution classified at three levels, R050 demoted, and no material near-precedent left at abstract-only status.

The claim ceiling is untouched. `MEASURED_INTERNAL_END_TO_END_TECHNICAL_DEMONSTRATION` remains established by owner adjudication. What has changed is that the paper's defensible contribution is now precisely three properties wide, and the nearest neighbour is a measured system published four months before this search.
