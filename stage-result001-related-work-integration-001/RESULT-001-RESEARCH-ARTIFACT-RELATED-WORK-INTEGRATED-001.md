# From Institutional Rules to Authorized Action: A Measured End-to-End Demonstration of OIC–ZTL–OAM

*A synthetic experiment in preserving logical warrant, currentness, institutional authority, runtime disposition, and reliance as distinct machine-operational states*

**Artifact class:** EVIDENCE_BOUND_TECHNICAL_REPORT
**Artifact id:** OIC-ZTL-OAM-DEMO-SLICE-001-RESULT-001-RESEARCH-ARTIFACT-RELATED-WORK-INTEGRATED-001
**Predecessor:** `88a6df39b20cd3fd4593daae830ba98a242811016d9312ef737100980294080a` (frozen, unmodified)
**Publication status:** DRAFT_NOT_RELEASED
**Contribution level (owner-adjudicated):** INTEGRATION_RESULT_ONLY

---

## Abstract

A system that decides whether an action may be taken has to answer several different questions, and the questions are easy to run together. Is the proposition supported? Is the rule that supports it still the operative one? Does the actor currently have authority? Should the runtime permit the action? Has anything been issued that a downstream party may rely on? These states can diverge — one may fail or remain unresolved while the others hold — and a verdict that carries a single value cannot say which one did.

RESULT-001 is a single owner-authorized, result-bearing execution of an integrated pipeline — an Open Institutional Compiler (OIC) front end, a pinned external logic kernel (ZTL), a currentness gate, an institutional authority gate, an Open Audit Mission (OAM) decision-composition step, a bounded action gate, governed propagation, a separate consumer process, and reliance issuance — over a bounded synthetic grant-disbursement scenario. Five cases were declared before execution, each isolating a different dimension along which the answers can diverge.

All five were measured, not asserted. A logically established proposition was blocked by supersession, with authority never evaluated because the gate did not proceed; the same proposition was refused under a revoked delegation; it was escalated rather than falsified under competing, unresolved authority; and it was substantively refuted under the stricter policy version after currentness and authority had both proceeded successfully. Reliance was issued in exactly one case, and only after a separate consumer revalidated the propagated state, including currentness and authority, before issuance.

The execution produced a hash-resolvable evidence package: 27 canonical artifacts verified with zero mismatches and zero missing files, a 41-file complete evidence freeze whose 40 governed entries verified with zero mismatches and zero missing files, and a case-1 reliance chain in which every reference resolves to persisted bytes. The package reported that the measured condition held; the claim itself became established only through a separately frozen owner adjudication bound to that evidence by digest.

Each stage of this chain has precedent. Evaluation-gated issuance and preserved history under later revocation are demonstrated in a measured system by Rhodes and Kang; a separately addressable judgment over an evidence bundle is normative in SLSA; an insufficient-information verdict distinct from failure, with its cause recorded, is deployed in ETSI EN 319 102-1; norm temporality is modelled in LegalRuleML; the separation of evaluation from enforcement dates to KeyNote. What we did not find in the systems examined is a single executed chain that carries a logical state alongside institutional authorization, execution disposition and a typed basis, in which a downstream consumer re-resolves currentness and re-evaluates authority before reliance is issued, and in which a gate never reached is recorded as such with its cause.

The contribution is therefore an integration result. The established claim is bounded to what was run: a measured internal end-to-end technical demonstration under one frozen synthetic scenario, one implementation commit, one kernel pin. It is not a benchmark, not independently reproduced, not independently assured, and establishes nothing about production readiness or institutional or legal validity.

## 1. The problem

Consider a machine that has been asked whether a particular grant of 40,000 may be disbursed.

It can determine that the conditions in the governing policy are satisfied. That is a claim about logic: given these grounds, the conclusion follows. It is the kind of claim a logic kernel can make and a logic kernel can check.

It is not the same claim as: *the policy that supports this conclusion is the one currently in force*. Policies are superseded. A conclusion can remain logically supported relative to the superseded rule while that rule fails the present-use currentness gate.

Neither of those is the same claim as: *the officer proposing this action currently holds the authority to take it*. Delegations are revoked. Two authority bases can be operative at once with no precedence between them. In this experiment authority is evaluated as a separate institutional condition and is not encoded among the ZTL grounds, so a proof about amounts and evidence says nothing about it.

None of those is the same claim as: *the runtime should permit the action now*. A runtime can be required to refuse for reasons that are not findings about the world at all — an unresolved question, a missing control requirement, a decision mode that forbids automatic disposal.

And none of them is the same as: *something has been issued on which a downstream party may now rely*. Evaluating a property and creating a reliance are different acts with different consequences. A system that treats a successful evaluation as automatically producing reliance has removed the step at which anyone could have declined.

The failure mode this creates is specific. A single verdict that does not separately preserve these states cannot, by that verdict alone, distinguish them: a refusal to act and a finding that the claim is false arrive as the same output. "We are not authorized to disburse this" and "this applicant is not eligible" are different statements about the world, with different consequences for the person on the other side of them, and a verdict that carries only one value cannot say which of them was meant.

The question this work takes up is narrow and mechanical:

> Can a machine-operational institutional pipeline preserve these distinctions through an actual end-to-end execution, rather than reconstructing them afterwards from logs?

Where the states are not separately preserved at the time of decision, the distinction can only be reconstructed afterwards by inference from surrounding records. Such an inference is not the system's own account of itself, and it is not available from the verdict alone.

## 2. Research question and contribution

RESULT-001 tests whether the integrated OIC–ZTL–OAM architecture preserves these states as separate, separately recorded machine-operational values through a synthetic source-to-reliance chain — one that begins with policy text and ends with a persisted reliance record or a persisted, reasoned absence.

The contribution is an integration result, and the qualifier is load-bearing. No component below is presented as ours:

1. **An architecture** in which the epistemic result, the institutional authorization status, the execution disposition and the decision basis are four separately represented fields that are not semantically interchangeable. Richer-than-Boolean dispositions are argued for, with a measured policy core, by Tallam, who enumerates modify, narrow, escalate, defer and roll back as outcomes a Boolean evaluator cannot express; the separation of an evaluation result from an acting system's disposition is KeyNote's advice-not-enforcement split. What is assembled here is the specific four-field set including a preserved epistemic value and a typed decision basis.
2. **A measured execution** of that architecture over five predeclared cases, each isolating one way the answers can diverge.
3. **An evidence discipline** in which the execution's own package is not the claim. A separately addressable judgment issued over an evidence bundle by a party other than the producer is normative in SLSA's Verification Summary Attestation, and Certificate Transparency separates issuance, later inclusion proof and monitor judgment. What is added here is narrow: the adjudication artifact states that it is not the measurement and records the decision as pending.

What this is not: a claim that the architecture is correct in general, that it would hold on real institutional material, or that any institution should rely on it. The scenario is synthetic and declared as such. One execution over one bounded policy family supports the owner-established measured internal end-to-end technical demonstration for exactly that scenario, implementation and kernel pin, and nothing wider. At component level the architecture is preceded throughout; at composition level it is substantially preceded with bounded surviving separations; only the integrated chain carries a distinction, and §14 states precisely which three properties it rests on.

## 3. System under test

**OIC (Open Institutional Compiler)** — the front end. Translating authoritative legal text into an executable artifact is the established territory of Catala and LegalRuleML. It reads a bounded synthetic policy notation and produces the repository's existing object model: a source document with per-line nodes, source anchors, candidate normative units, and — only where an owner-authored admission record names them — an institutional intermediate representation, an authority record, a control envelope and a runtime binding.

The load-bearing property is that extraction confers nothing. Every candidate the parser produces starts as `extracted`. It becomes executable only when an owner-authored admission record names it. The scenario deliberately contains a guidance line that parses cleanly, extracts as an advisory candidate, is never admitted, and never reaches the control envelope. That difference is observable in the evidence rather than asserted in prose.

**ZTL** — an external logic kernel, reached at a pinned commit through exactly one bridge file. The bridge verifies the checkout is at the pinned commit before importing anything, calls one entrypoint, and returns the kernel's result without institutional interpretation. Pin-before-use is ordinary supply-chain discipline. The kernel's vocabulary is its own: EARNED, ON CREDIT, OPEN, REFUTED, with a warranty grade and a raw verdict.

Two properties matter for this experiment.

*A logical warrant is not an institutional warrant.* Supplying a checkable logical argument with a request is proof-carrying authorization, from Appel and Felten onward. The kernel decides whether a formula holds under a marking. It has no clock, no authority model, no notion of an institution, and it is never asked to have one.

*Authority is not a ZTL ground.* The formula names two grounds — that the amount is within the limit, and that signed eligibility evidence is present. It does not name the delegation, the authority basis, or the currentness of the policy. Keeping authority outside the ZTL ground set prevents the logical warrant in this experiment from being treated as the authority determination. Holding the authority of a norm as metadata about the norm, rather than as a proposition inside it, is LegalRuleML's posture. The scenario declares this constraint explicitly and the evidence records the formula that was actually evaluated.

The raw verdict crosses the boundary operationally inert. `T` is not ALLOW.

**Currentness gate** — determines, from separately maintained institutional state, whether a compiled control version is the operative one at a declared instant. Temporal modelling of norms is finer-grained in LegalRuleML, which distinguishes when a norm is in force, when it is efficacious and when it applies; time-varying authorization dates to TRBAC; dated legislative parameters evaluated at an instant are deployed in OpenFisca. What is specific here is that the currentness verdict gates whether the authority evaluation is reached at all. It returns a state (CURRENT, SUPERSEDED, INELIGIBLE, UNKNOWN) and a reason code. There is no parameter through which a caller can assert currency.

**Institutional authority gate** — evaluates, against synthetic authority and admissibility bases, whether the requesting principal may take the action. Its reason codes distinguish, among others, a revoked basis (A10) from competing operative bases with no frozen precedence (A6) from a satisfied basis (A1).

**OAM decision-composition step** — the demo-specific `OAMDecision` composition, a bounded runtime-decision artifact within this synthetic Open Audit Mission (OAM) demonstration. It produces four separately represented fields: `epistemic_status`, `institutional_authorization_status`, `execution_disposition`, `decision_basis`. The kernel-derived epistemic status is carried into the record as its own value and is not rewritten by a currentness or authority outcome. The remaining three are composed: the composition evaluates an appropriate-epistemic-route component alongside currentness, authority, warrant binding, evidence, admission and version bindings, decision mode and action-proposal identity, and the first unmet component in the frozen order supplies the decision basis. The fields are therefore distinct in meaning and are not interchangeable; they are not causally independent of one another.

**Bounded action gate** — emits ACTION_PERMITTED, ACTION_BLOCKED or ACTION_ESCALATED. Three-valued runtime dispositions including escalation are proposed at design level by Racioppi and argued for with a measured core by Tallam. It performs no payment, no disbursement, no external call and no legal act.

**Governed propagation and separate consumer** — where the runtime permitted the action, the producer materializes a propagation envelope, and a *separate operating-system process* under a different principal validates it. The consumer receives paths, not objects. It opens the governed bytes itself, re-resolves currentness at its own instant, and re-evaluates authority before it will consider issuing anything.

**Reliance issuance** — the act that creates something downstream parties may rely on, gated by a single-use issuance authorization claimed by exclusive creation. Issuance as a role distinct from verification is normative in the W3C Verifiable Credentials model, and issuance conditioned on a validity predicate holding is measured in Rhodes and Kang, whose Execution Attestation Certificate is emitted only when their proof-of-execution predicate is satisfied.

**Evidence closure and owner adjudication** — the execution writes a six-stage evidence tree with a manifest and digest list; a separate closure step verifies it; and a separate owner claim decision adjudicates what has been established. Hash-resolvable chain evidence proving authorized parties performed each step is in-toto's contribution; a summary judgment issued over that evidence by a separate authority is SLSA's.

## 4. The synthetic experiment

Everything below is synthetic and declared as such in the scenario file: `synthetic = true`, `derived_from_real_institutional_source = false`. No real institution, programme, policy or disbursement is described, referenced or stood in for.

| element | value |
|---|---|
| scenario_id | `synthetic-grant-authority` |
| policy family | `SYNTH-GRANT-POLICY` |
| actor | `DISBURSING-OFFICER` |
| action | `DISBURSE_GRANT` |
| proposed amount | 40,000 |
| v1 amount limit | 50,000 |
| v2 amount limit | 25,000 |
| v2 supersedes | v1 |
| delegation | `DELEG-2027-014` |
| evidence requirement | signed eligibility evidence |

The ZTL formula, evaluated live:

```
g_amount_within_limit & g_eligibility_evidence_present
```

The 40,000 amount is chosen so that it sits inside the v1 limit and outside the v2 limit. That single fact is what lets one scenario produce both an institutional refusal of a true proposition and a substantive refutation of the same proposed action, depending only on which policy version governs.

Two further design points are worth stating because they shape what the cases can show.

*Evidence is an observation, not an inference.* The scenario carries a separate synthetic evidence artifact with its own bytes, declaring an evidence id, a class and a signature state. The runtime opens it, verifies its identity and digest, reads a state, and only then decides whether the requirement is satisfied. The requirement and its satisfaction are separately represented; the presence of a requirement never stands in for meeting it.

*Absence is not falsity.* The evidence state is not a boolean. SIGNED produces a true mark; explicitly UNSIGNED or INVALID produces a false mark; UNKNOWN and NOT_OBSERVED produce **no mark at all**, leaving the kernel's atom unverified rather than false. Never having looked and having looked and found nothing are different states, and a single boolean alone cannot carry that distinction. The instinct is established: Rego distinguishes undefined from false, defeasible logics distinguish unproven from refuted, and ETSI signature validation carries an insufficient-information verdict beside its pass and fail.

## 5. Predeclared five-case design

The five cases were specified before execution, in the work order that authorized the implementation. Each isolates a different dimension.

**Case 1 — valid rule, valid authority.** The positive control. v1 governs, the amount is within its limit, evidence is signed, the delegation is operative. This is the only path along which reliance can be reached, and its purpose is to show that the pipeline can complete, not merely refuse.

**Case 2 — v1 used after v2 becomes effective.** Isolates *temporal* control. Nothing about the logic changes; the amount is still within v1's limit. What changes is that v1 is no longer the operative version at the evaluation instant. This case asks whether the system can block on currentness without disturbing the epistemic result, and whether it evaluates authority for an operation the gate has already stopped.

**Case 3 — authority revoked.** Isolates *institutional* control, holding logic and currentness fixed. The proposition holds, v1 is current, and the delegation has been revoked. A system that could only express "the claim failed" would have to misdescribe this.

**Case 4 — competing, unresolved authority.** The strongest separation case. Two authority bases are operative for the same principal and scope with no frozen precedence between them. The institution has not resolved which governs. This is not a finding that the claim is false and not a finding that the actor lacks authority; it is an unresolved question, and the case asks whether the system can say so without converting uncertainty into a negative finding.

**Case 5 — the same action under v2.** Isolates *substantive* refutation. v2 is current, the delegation is operative, and the authority basis passes — currentness and authority both proceed. What fails is the proposition itself: 40,000 exceeds v2's 25,000 limit. This case exists to test whether the architecture distinguishes "the institution will not permit this" from "this is not true."

## 6. Measured results

The following is the measured matrix as recorded in the frozen evidence. Values are reproduced as observed; none has been improved, reinterpreted or normalized.

| case | ZTL | epistemic | currentness | authority | institutional | runtime | action | reliance |
|---|---|---|---|---|---|---|---|---|
| 1 | EARNED / T | ESTABLISHED | CURRENT / G1 | A1 | AUTHORIZED | ALLOW | ACTION_PERMITTED | **ISSUED** |
| 2 | EARNED / T | ESTABLISHED | SUPERSEDED / G2 | *not evaluated* | REFUSED | BLOCK | ACTION_BLOCKED | ABSENT |
| 3 | EARNED / T | ESTABLISHED | CURRENT / G1 | A10 | REFUSED | BLOCK | ACTION_BLOCKED | ABSENT |
| 4 | EARNED / T | ESTABLISHED | CURRENT / G1 | A6 | UNRESOLVED | ESCALATE | ACTION_ESCALATED | ABSENT |
| 5 | REFUTED / F | REFUTED | CURRENT / G1 | A1 | REFUSED | BLOCK | ACTION_BLOCKED | ABSENT |

In case 2 the authority observation records `authority_evaluated: false` with `authority_not_evaluated_reason: CURRENTNESS_GATE_DID_NOT_PROCEED` — a value structurally distinct from every authority reason code.

## 7. What the cases demonstrate

**Case 2 — a true proposition, blocked in time, with authority never asked.**

The epistemic status remains ESTABLISHED. The kernel returned EARNED with a hereditary grade; nothing about the logic changed between case 1 and case 2. What changed is the evaluation instant, and at that instant v1 has been superseded. Currentness returns SUPERSEDED with gate code G2, and the institutional authorization status is REFUSED.

The second half of this case is the more interesting one. Authority was **not evaluated at all**. The gate did not proceed, so the authority layer was never reached, and the record says so explicitly rather than carrying a code.

That matters because an authority code recorded for an operation the gate had already stopped would be indistinguishable, on the record, from one produced by an authority evaluation that actually governed the decision. A question the gate did not reach is therefore recorded as NOT_EVALUATED with its reason, rather than as an authority answer.

This is one of the three properties the integration claim rests on, so it is worth being exact about what is and is not new here. Recording *why* a determinate answer could not be reached is normative in ETSI signature validation, whose sub-indications name the cause. Diagnosing the root cause of a *violation* is CMF9 in the compliance-monitoring taxonomy of Ly and colleagues. XACML short-circuits target evaluation but records nothing about what it skipped, and returns applied policies with no counterpart for skipped ones. Among the systems examined — including four contemporary agent-governance systems — none records that a later gate was *not reached because an earlier gate stopped the path*, together with that cause. The narrow property is the gate-ordering one, not the idea of recording a reason.

**Case 3 — current policy, sound logic, revoked authority.**

The proposition holds and v1 is the operative version. The delegation has been revoked, and authority returns A10 (`AUTHORITY_BASIS_REVOKED`). The institutional authorization status is REFUSED and the runtime blocks.

The epistemic status is still ESTABLISHED. The revocation of a delegation is not evidence about the amount or the eligibility documentation; it is a fact about who may act. The record carries both facts side by side, and neither has been adjusted to agree with the other.

**Case 4 — unresolved is not false.**

This is the strongest separation case in the experiment.

Two authority bases are operative with no precedence between them, and authority returns A6 (`AUTHORITY_BASIS_AMBIGUOUS_COMPETING`). The institutional authorization status is **UNRESOLVED** — a third value, neither AUTHORIZED nor REFUSED. The execution disposition is **ESCALATE**, and the decision basis is PRECAUTIONARY: the runtime is failing closed under uncertainty, not on a finding.

The epistemic status remains **ESTABLISHED**. The system does not rewrite the proposition as false because the action is not authorized, and it does not report a determinate institutional answer it does not have. An architecture whose institutional authorization status admits only two values has no place to record this state. That limitation is real but not ours to claim: unresolved normative conflict is long established in defeasible deontic logic, where weak permission is characterised precisely under unresolved conflict, and a deployed three-valued verdict already exists in ETSI EN 319 102-1, whose INDETERMINATE means the checks "have not failed but there is insufficient information to determine". Racioppi proposes PERMIT, ESCALATE and DENY at design level. What case 4 adds is narrower: the unresolved institutional status is carried into a runtime disposition and a typed precautionary basis while the epistemic value is left untouched.

**Case 5 — substantive refutation after currentness and authority both proceeded.**

v2 is current (CURRENT / G1) and the authority basis passes (A1). Neither the currentness gate nor the authority gate refused. The composed institutional authorization status is nonetheless REFUSED — because the proposition itself failed, not because a gate did. A currentness pass and an authority pass do not imply that the substantive predicate holds. Case 5 records a distinct kernel evaluation under the v2 marking, with input and output identities different from case 1. Under v2's stricter limit the amount ground evaluates false. The formula returns REFUTED with a hereditary grade, the epistemic status is REFUTED, and the decision basis is SUBSTANTIVE.

Cases 2, 3 and 5 end in BLOCK for different reasons; case 4 instead ends in ESCALATE under unresolved authority. The record says which is which: SUBSTANTIVE in case 5, PROCEDURAL in cases 2 and 3, and PRECAUTIONARY in case 4, whose disposition is ESCALATE rather than BLOCK.

**Case 1 — evaluation did not create reliance.**

Every gate passes and the runtime permits the action. Reliance is still not a consequence of the evaluation. It appears only after the positive path reaches the issuance stage: the producer materializes an envelope; a *separate operating-system process*, under a different principal, opens the governed bytes itself, re-resolves currentness at its own instant, re-evaluates authority, and runs sixteen frozen checks — all of which passed — before a single-use issuance authorization is claimed by exclusive creation and a reliance record is written.

Reliance appears in exactly one of five cases. In the other four the evidence tree carries a persisted reason for its absence rather than an empty directory.

That evaluation gates issuance is not a distinction this work can claim. Rhodes and Kang issue an Execution Attestation Certificate only when their validity predicate holds, in a measured implementation; the verifiable-credentials model separates issuance from verification by role and states that verification does not imply evaluation of the truth of the claims. What the examined systems do not do is have the downstream party re-resolve the governing rule's currentness and re-evaluate the actor's authority at its own instant before issuing — the second of the three surviving properties.

## 8. Preserved separations

The separations below are stated as design commitments; what follows each is the observation that exercises it.

**EPISTEMIC_STATUS ≠ INSTITUTIONAL_AUTHORIZATION_STATUS ≠ EXECUTION_DISPOSITION ≠ DECISION_BASIS**

Case 4 shows all four taking different values in a single record: ESTABLISHED, UNRESOLVED, ESCALATE, PRECAUTIONARY. None is an alias for another, and the epistemic value is preserved rather than adjusted to match the institutional outcome. This is semantic distinction, not causal independence: the composition that yields the last three does read an appropriate-epistemic-route component derived from the first, alongside currentness, authority and the other control components.

**CURRENTNESS_PASS ≠ AUTHORITY_PASS ≠ PROPAGATION ≠ RELIANCE**

Case 3 passes currentness and fails authority. Case 2 fails currentness and never reaches authority. Case 1 passes both and still does not have reliance until a separate consumer re-resolves currentness and re-evaluates authority and the issuance step is claimed.

**OBSERVATION ≠ CRITERIA ≠ ADJUDICATION ≠ OWNER CLAIM DECISION**

Read artifact by artifact against the frozen package, the layers are these.

*Observations* are recorded as their own artifacts: the raw kernel result under `02-ztl`, the `SYNTHETIC_EVIDENCE_OBSERVATION` opened and digest-verified under `00-source`, and the re-resolved currentness and reliance-time authority values recorded by the separate consumer under `04-reliance`.

*Criteria* are the frozen evaluation rules and predicates against which the observations are tested: the currentness evaluation procedure, the authority evaluation procedure, the warrant requirements carried in the runtime binding, and the component predicates required before ALLOW. Their reason codes — G1, G2, A1, A6, A10 and the rest — are controlled outputs of those evaluations, not the criteria themselves.

*Adjudication* has no separately named artifact in RESULT-001, and this report does not assign that role to anything that did not perform it. The `RESULT_BEARING_EVIDENCE_CLOSURE` record did what its own bytes support: it verified the canonical package against its digest list, re-checked the freeze, and confirmed that the case-1 reliance chain resolves with no unresolved references. It states in its own text that the package's measured flag is not a finding of that record, and it records the owner decision as PENDING.

*The owner claim decision* is the separate act that determined what has been established. It was written after the evidence was frozen and verified, binds that evidence by digest, and records its own basis as adjudication of frozen result-bearing evidence rather than measurement.

**EVALUATION ESTABLISHES THE PROPERTY; ISSUANCE CREATES THE RELIANCE**

Four cases evaluated and issued nothing. One evaluated, propagated, was revalidated by a separate consumer, and only then issued. The principle itself is preceded — see §13 — and what survives is the revalidation step, not the separation.

## 9. Evidence architecture

The execution wrote a six-stage tree:

| stage | contents |
|---|---|
| `00-source` | exact source bytes, source document, source nodes, the evidence observation |
| `01-oic` | candidate normative units, admission records, InstitutionalIR, authority record, control envelope, runtime binding |
| `02-ztl` | exact kernel input, raw kernel result, warrant artifact, kernel execution identity, binding validation |
| `03-runtime` | currentness use-gate decision, authority evaluation *or* an explicit not-evaluated record, evidence observation, OAM decision, action proposal, bounded execution attempt |
| `04-reliance` | envelope, consumer validation, issuance authorization, issuance attempt and reliance record — or a stated reason each is absent |
| `05-evidence` | causal chain, manifest, digest list |

Verification results, all read from the frozen bytes with an external digest utility:

- **Canonical package:** 27 artifacts checked, **0 mismatches, 0 missing**.
- **Complete freeze** (canonical package plus the raw working artifacts and the owner-control records): 41 regular files, of which the checksum list governs 40 — it excludes itself — verifying with **0 mismatches, 0 missing**.
- **Case-1 raw reliance chain:** resolvable, with **0 unresolved references**. Every evidence reference in the propagation envelope resolves to the exact bytes it names by digest; the envelope, authority-decision, consumer-validation and reliance-record protocol digests each recompute; the issuance attempt binds the issuance authorization by digest; and the reliance record binds the attempt, the validation and the envelope.

Two details of that last line are worth separating. Protocol digests and file digests are computed over different bytes and were reported separately throughout; substituting one for the other would have produced a check that looked stronger than it was. And the evidence references carry a locator *and* a digest, so the consumer recomputes rather than trusting an identifier — a reference that carried only an id would resolve a substituted artifact exactly as well as the real one.

Absences are recorded, not implied. Each of cases 2–5 carries a persisted reason for having no reliance record.

## 10. Claim adjudication

The evidence package contains a field reporting that the measured condition held.

That field is not the claim.

It is the package's own report about itself, produced under a validated authorization that permitted that ceiling. Treating it as the claim would make the artifact the judge of its own significance — the system would decide what it had demonstrated by writing down that it had demonstrated it.

The claim became established through a separate act: an owner claim decision, written after the evidence was frozen and verified, binding the evidence by digest, and recording its own basis as adjudication of frozen result-bearing evidence rather than measurement. The canonical record that indexes the evidence states explicitly that it is not a new adjudication and does not supersede the decision.

This is the same separation the architecture enforces internally, applied to itself. Evaluation establishes a property; someone still has to decide what to make of it. A pipeline that preserves that distinction between its layers and then abandons it where the system reports on its own performance would collapse at the reporting boundary the distinction preserved during execution.

The separation of producing evidence from judging it is, however, already normative elsewhere. A SLSA Verification Summary Attestation is issued by an authority with sufficient evidence to make the determination, is addressable independently of the raw provenance, and may be accepted or re-checked by a consumer against the underlying attestations. Certificate Transparency separates a log's promise to append, the later inclusion proof and a monitor's judgement, and places institutional response explicitly outside the protocol. Measured against those, what remains particular here is modest and worth stating as such: the adjudication artifact declares that it is not the measurement, and records the decision as pending until the owner acts.

## 11. Reproducibility and evidence availability

Stated precisely, because the distinctions matter:

- The **implementation and the synthetic scenario are available** in the public repository.
- RESULT-001's historical implementation commit is `a2ece68f013c25e6a3874f20a924e95730c175f0`. That identity is permanent and is not rewritten by later repository activity.
- A **repository evidence pointer** is now on the common baseline, landed through merge `ac52dcde01b0db1fdf8ecac6321db7a4e1efd81a`. That merge is post-result provenance — a record made after the execution — and is not the implementation that produced RESULT-001.
- The **underlying evidence bytes remain owner-held** and are not publicly released.

Because the evidence bytes are not publicly released and no qualifying independent reproduction has been submitted to or established by this record, this artifact makes **no claim of independent reproduction**. The remote CI runs referenced in the repository are project-controlled validation of the project's own test contract; they do not constitute independent assurance.

## 12. Limitations

- **Synthetic scenario only.** No real institution, programme, policy or disbursement is involved, and none is represented.
- **One bounded policy and action family.** A single grant-disbursement family with two versions and one action.
- **Internal execution.** One execution, on owner-controlled infrastructure, under owner authorization.
- **No independent Tier-1 reproduction.** No qualifying independent Tier-1 reproduction is established or evidenced in the RESULT-001 record.
- **No independent assurance.** No qualifying independent external assurance is established for RESULT-001.
- **No real institution.** Authority, delegation, admission and evidence are all synthetic constructs declared as such.
- **No legal-validity determination.** Nothing here bears on whether any decision would be valid in law.
- **No production or non-bypassability finding.** The action gate is a bounded demonstration gate. It performs no real-world effect and is not non-bypassable production enforcement.
- **No domain generalization.** The result says nothing about other institutional domains, other policy structures, or other kernels.
- **Evidence bytes are not yet publicly released.**
- **RESULT-001 is not a benchmark** and is not offered as one.

Related-work positioning is given in §13, from a bounded adversarial search whose completeness is not claimed.

## 13. Related work

This section reports what a bounded, adversarial prior-art search found. It was conducted to defeat this work's candidate distinctions rather than to support them, over 31 primary sources: standards, RFCs, peer-reviewed papers and authoritative project specifications. **Search completeness is not claimed, and absence from a search is not evidence of absence.**

**Rules as code and legal knowledge representation.** Catala compiles statutory law into an executable specification with a proved core, and LegalRuleML models norms with three distinct temporal dimensions — in force, efficacious, applicable — together with `Authority` and `Jurisdiction` as metadata about the norm. OpenFisca evaluates dated legislative parameters at a requested instant. The compilation stage of this work sits inside that tradition and adds nothing to it. LegalRuleML's `Authority` is the power to create, endorse or enforce a norm; it is not a determination that a particular actor may act now, which is why it does not precede this work's authority evaluation.

**Authorization, trust management and policy engines.** XACML has a four-valued result, but `Indeterminate` arises when an error occurs during evaluation, and the specification carries no truth value separate from the decision. KeyNote separates evaluation from enforcement outright — "KeyNote does not directly enforce policy; it only provides advice to the applications that call it" — which precedes the disposition separation used here. Rego distinguishes `undefined` from `false`, and OPA logs every decision, though as transmitted events rather than tamper-evident records. TRBAC establishes time-varying authorization, timing the actor's role rather than the governing rule's version.

**Warrant and proof-carrying systems.** Proof-carrying authorization supplies a checkable logical argument with a request; Nexus Authorization Logic values constructive proofs precisely because they retain the evidence for a conclusion. In both, the proof *is* the authorization argument. This work instead keeps the logical warrant and the institutional authority in separate layers producing separate outcomes.

**Provenance, attestation and supply chain.** W3C PROV is explicitly retrospective and carries no cryptographic integrity. in-toto proves that authorized functionaries performed each step of a chain, with a separate verification step — a separate verifier, not an independent assurance party. SLSA adds a Verification Summary Attestation: a judgment issued over an evidence bundle by an authority distinct from the producer, which a consumer may accept or re-check. Certificate Transparency preserves immutable history under an append-only Merkle tree while the set of trusted logs is "neither unified nor static", so what should be relied upon changes over preserved history; monitors judge later, and institutional response is explicitly out of scope.

**Credentials and reliance.** The W3C Verifiable Credentials model separates issuer and verifier roles and states that verification does not imply evaluation of the truth of the claims. Its lifecycle is issue, verify, validate, rely: the issuer performs no prescribed evaluation, and validation, where reliance attaches, is outside the specification. The ordering here is the reverse — evaluate, then issue — but the ordering itself is preceded, in a measured system, by Rhodes and Kang.

**Signature validation and unresolved verdicts.** ETSI EN 319 102-1 carries TOTAL-PASSED, TOTAL-FAILED and INDETERMINATE, the last meaning verification has not failed but there is insufficient information to decide, with sub-indications naming the cause and a requirement that each constraint justify its contribution. A deployed, three-valued verdict with recorded causes therefore predates this work.

**Compliance monitoring.** The ten compliance-monitoring functionalities of Ly and colleagues cover time, data, resources, non-atomic activities, lifecycles, multiple instances, reactive and proactive detection, root-cause explanation and degree of compliance. None covers a rule left unevaluated because an earlier constraint terminated the path, none models the compliance rule's own validity window, and there is no third state between satisfied and violated.

**Normative conflict.** Defeasible deontic logic treats conflicting norms with a superiority relation and characterises weak permission under unresolved conflict. Unresolved-as-not-false is established there; what is not established there is its carriage into a runtime disposition.

**Contemporary agent governance.** Four recent systems are the nearest neighbours. Rhodes and Kang bind a contract, a causal event stream and a replay context into a measured proof-of-execution predicate, issue an attestation certificate only when it holds, and state that revocation at a later instant does not retrospectively invalidate an execution valid earlier — historical validity is not rewritten, only current acceptability changes. Salfeld-Nebgen requires independently attested facts before a governed action and names the check-to-use gap directly. Tallam argues, with a measured policy core, that Boolean allow/deny cannot express the outcomes production governance needs. Racioppi proposes signed mandates with chained delegation, three-valued decisions and append-only correction; that work states it is a system under construction whose empirical results are a plan rather than a report, and is read here as design.

**What the search did not find.** Among the sources examined, no system carries a logical or epistemic state alongside institutional authorization, execution disposition and a typed basis through one executed chain; no downstream consumer re-resolves the governing rule's currentness and re-evaluates the actor's authority at its own instant before issuing a reliance-bearing artifact; and no persisted record states that a later gate was not reached because an earlier gate stopped the path, together with that cause. Those three, and only those three, are what the contribution here rests on.

## 14. Conclusion

RESULT-001 provides measured internal evidence that the tested OIC–ZTL–OAM architecture preserved logical warrant, temporal currentness, institutional authority, runtime disposition and reliance as distinct machine-operational states through the tested synthetic end-to-end chain.

The contribution is an integration result. Every component of that chain has precedent, and several have strong precedent in measured or deployed systems: evaluation-gated issuance and preserved history under later revocation, a separately addressable judgment over an evidence bundle, a three-valued verdict with recorded causes, norm temporality, the separation of evaluation from enforcement, hash-resolvable chain evidence. None of those is claimed here.

What the examined systems did not do, and what the five cases show together, is carry a logical state alongside institutional authorization, execution disposition and a typed basis through a single executed chain; have a downstream consumer re-resolve currentness and re-evaluate authority before reliance is issued; and record a gate that was never reached, with the cause of its non-evaluation. Remove any one of those three and the position is weak; remove two and there is no distinction to report.

The claim is bounded to what was executed: one frozen synthetic scenario, one implementation commit, one kernel pin, one execution. It is not a claim about institutional systems in general, about real institutional material, or about what would happen under conditions that were not tested.

---

## Appendix A — RESULT-001 evidence identities

| identity | value |
|---|---|
| historical implementation commit | `a2ece68f013c25e6a3874f20a924e95730c175f0` |
| post-result repository provenance merge | `ac52dcde01b0db1fdf8ecac6321db7a4e1efd81a` |
| scenario bundle digest | `sha256:ae72389334d0476421144e7ad42b6ca74b68e65d524ee188cfdbc485e5129bd3` |
| ZTL commit | `56e1ff0510c62b04dbd85bbe08b7a6deacbf276b` |
| repository evidence pointer | `041ba2da543ce5a09b59204c105a3c26df47fb355f2a1b1ae7118cd5e0a73a85` |
| preservation authorization | `1d08df8bdd6e5946172d2f85e81a456ebe33be9e814f26264558aa6f2dc6009c` |
| canonical internal record | `d98f3f5afc17193b21aa684f51af4e902a46b9a98ee75ff2560e670a5dbe8403` |
| owner claim decision | `d14f896c58249394564e8a95b011e2f9f6c843cc29ad9a13f6d62cc0ffb79c5b` |
| evidence closure | `201c5e2274ed96f75a5d7745bda4fbc86bcb422514ffb846167f071dd590a573` |
| complete freeze digest list | `af670b0d691fcd4a1c02476105a40cbb2166c42b1688b645f3201b4f2b2fec4d` |
| case-1 reliance record digest | `21fc11e8861bedd3f77869ef61f7c794c5ec728b7a3dcb0c236b50550f9bcb83` |

## Appendix B — Five-case matrix

| case | ZTL | epistemic | currentness | authority | institutional | runtime | action | basis | reliance |
|---|---|---|---|---|---|---|---|---|---|
| 1 | EARNED / T | ESTABLISHED | CURRENT / G1 | A1 | AUTHORIZED | ALLOW | ACTION_PERMITTED | SUBSTANTIVE | ISSUED |
| 2 | EARNED / T | ESTABLISHED | SUPERSEDED / G2 | not evaluated (`CURRENTNESS_GATE_DID_NOT_PROCEED`) | REFUSED | BLOCK | ACTION_BLOCKED | PROCEDURAL | ABSENT |
| 3 | EARNED / T | ESTABLISHED | CURRENT / G1 | A10 | REFUSED | BLOCK | ACTION_BLOCKED | PROCEDURAL | ABSENT |
| 4 | EARNED / T | ESTABLISHED | CURRENT / G1 | A6 | UNRESOLVED | ESCALATE | ACTION_ESCALATED | PRECAUTIONARY | ABSENT |
| 5 | REFUTED / F | REFUTED | CURRENT / G1 | A1 | REFUSED | BLOCK | ACTION_BLOCKED | SUBSTANTIVE | ABSENT |

## Appendix C — Claim / non-claim register

**Established**

| claim | status |
|---|---|
| MEASURED_INTERNAL_END_TO_END_TECHNICAL_DEMONSTRATION | **ESTABLISHED** by owner claim decision `d14f896c…` |

**Not established**

| | |
|---|---|
| PRODUCTION_READINESS | NOT ESTABLISHED |
| INSTITUTIONAL_VALIDITY | NOT ESTABLISHED |
| LEGAL_VALIDITY | NOT ESTABLISHED |
| NON_BYPASSABLE_PRODUCTION_ENFORCEMENT | NOT ESTABLISHED |
| INDEPENDENT_TIER1_REPRODUCTION | NOT ESTABLISHED |
| INDEPENDENT_ASSURANCE | NOT ESTABLISHED |
| REAL_WORLD_GRANT_AUTHORIZATION | NOT ESTABLISHED |
| GENERALIZATION_TO_OTHER_INSTITUTIONAL_DOMAINS | NOT ESTABLISHED |
| GLOBAL_SEMANTIC_IMPLEMENTATION_GATE_OPEN | CLOSED |
| PROPOSED_CONTRACT_GLOBALLY_ADMITTED | FALSE |
| RUN004 | FALSE |
| RESULT-001 benchmark status | **NOT_A_BENCHMARK** |

This artifact is a representation of adjudicated evidence. It is not an independent source of truth: `downstream_representation_is_independent_source_of_truth = false`.
