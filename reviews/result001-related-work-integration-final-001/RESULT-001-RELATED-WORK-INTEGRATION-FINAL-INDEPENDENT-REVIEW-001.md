# RESULT-001 RELATED-WORK INTEGRATION — FINAL CANDIDATE INDEPENDENT REVIEW 001

```
record_class            INDEPENDENT_REVIEW_RECORD
role                    INDEPENDENT_REVIEWER
principal_id            INDEPENDENT_REVIEWER_001
reviewed_repository     veraxis-protocol/Institutional-Compiler-Review-Ledger
reviewed_pull_request   13
reviewed_head           bf0882b2f3dad4719633d5c31737244bcf2ecf27
publication_authorized  FALSE
owner_decision_authored FALSE
evidence_modified       FALSE
stage_paths_modified    FALSE
```

## 0. Declared conflict of interest — read before the findings

I previously executed a competing correction of the same four artifacts
(`VITALIY-CORRECTION-001`). Under this order that work is admissible **only** as
adversarial comparison material, and it is used here in exactly one way: as a
source of checks to run against the candidate. No byte of it is the object under
review, and no finding below is stated because the candidate differs from it.

Two findings in this review are places where I looked for a defect I had myself
flagged, ran the check, and the candidate passed — §5.7 and §5.5. I record those
explicitly, because a reviewer who has authored a rival artifact owes the reader
the cases where the rival's concern did not survive contact with the candidate.

```
reviewer_authored_a_competing_candidate  TRUE
competing_candidate_reviewed_as_object   FALSE
```

## 1. Identity gate — all six governing identities

Fetched `refs/pull/13/head` and verified bytes at the exact head. Every declared
identity reproduced:

```
PR #13 head                     bf0882b2f3dad4719633d5c31737244bcf2ecf27   exact
manuscript                      eafbb450a9ef37f04e15c9c68f72dfefd371771a033a2b965505357fe0256ece  exact  (51027 B)
claim map                       69b8b50f097dd195ead08c5e0d4e5f514838e160b0d7a917de4f71d4762929db  exact  (58332 B)
architecture (.mmd)             67041c972469959e77b9cc2fdc36bef274035b62736c1dcdac3de8e47b6466d7  exact  ( 6702 B)
citation audit                  e1da4ddd373257dc6bd2b0eeb037fb2b817054295971a1490c14f645a1101970  exact  (12624 B)
public-review projection        9610395079d2db102a6c57eb93dd5d3b0cbcae3d90fa2e1d29d49f527951b750  exact  ( 8164 B)
transport manifest              2e8789b66381145a0e900b05ad78102aa6baa7c65bfbf4e03abf9d1e8a9629fc  exact  ( 4593 B)

LEDGER-SHA256SUMS  6/6 OK
LEDGER-SHA512SUMS  6/6 OK
```

Byte identity is a precondition, not a finding. Everything below is content.

## 2. Review questions 1–5 — contribution structure and reporting boundary

**Q1 — does §2 present exactly ONE contribution: measured integration of
S1 + S8 + X1?  YES.**

§2 opens: *"The one scientific contribution is **the measured integration
result**. It rests only on the integrated combination of S1 … S8 … and X1 …"*
All three are stated inline with their operative content. There is no enumerated
list of contributions anywhere in the manuscript, and no second candidate
contribution is advanced in §7, §10, §13 or §14.

**Q2 — are component mechanisms and broader compositions correctly demoted?
YES.**

The demotion is explicit and typed in one sentence: *"The architecture is the
tested substrate, the five predeclared cases are the method, and the observed
field values, gate paths and evidence identities are measured implementation
properties."* Component precedent is then cited rather than asserted — Tallam
[21], KeyNote [4], SLSA [14], Certificate Transparency [15] — and the paragraph
closes the door: *"None of those mechanisms, and neither the three-act reporting
separation nor R050, is an independent contribution."* R050 is named in the text
itself, not left to the claim map.

**Q3 — does §10 distinguish the three acts?  YES.**

§10 opens by naming them and keeps them apart operationally, not just
typographically: the package *reports*; the closure record *verified the frozen
package, digest list, complete freeze and case-1 reliance-chain bindings*; the
owner *issued the separately frozen, digest-bound decision*. Each is given a
distinct verb over a distinct object. §2 carries the same three-act sequence, so
the two sections agree.

**Q4 — is it clear the owner decision HAS occurred?  YES.**

§2: *"the owner then issued the separate claim decision that establishes
`MEASURED_INTERNAL_END_TO_END_TECHNICAL_DEMONSTRATION = ESTABLISHED` for bounded
RESULT-001."* §10 states the same. Appendix C records it as **ESTABLISHED** by
owner claim decision `d14f896c…`. Measured: the manuscript contains **zero**
occurrences of *pending*, *awaiting*, *until the owner acts* or any equivalent.

**Q5 — is the closure artifact's historical status faithful without being
mistaken for current owner-decision state?  YES.**

§8: *"Its historical status field predates the separate owner decision and is not
the current owner-decision state."* The candidate takes the conservative route —
it asserts that a historical status field exists and that it is not current
state, without restating the superseded value. That neither misdescribes the
frozen bytes nor lets a stale value read as live. The heading of that paragraph
was also changed from *Adjudication* to *Evidence closure*, which stops the
closure record from being read as an adjudication act; see observation O1 for the
one loose end this leaves.

## 3. Q6 — R043

```
R043 = ACCEPTABLE_HISTORICAL_DESCRIPTION
```

Claim text under review, verbatim:

> "RESULT-001 instantiates no separately named adjudication artifact; the
> evidence closure record verified the package and recorded the owner decision as
> pending."

Three things decide this, and none of them is charity toward the candidate.

The grammar is past-tense and reports an act: *the record recorded X as Y*. It
does not predicate *pending* of the present state of the owner decision; it
predicates it of what a specific artifact wrote at the time it was written. That
statement is true of the frozen bytes and remains true forever.

The claim map disambiguates itself structurally. Every claim in the file,
including R043, carries `owner_claim_decision_sha256 = d14f896c…`. A record that
binds the owner decision by digest on the same object is not asserting that the
decision is outstanding.

And the claim map is not the current-state register. Appendix C of the manuscript
is, and it reads ESTABLISHED.

**Recorded reservation, not a blocking defect.** §8 of the manuscript was given an
explicit *"is not the current owner-decision state"* qualifier; R043 was not, and
carries the word *pending* unqualified. The asymmetry is real. It is not
correctable within this order — `claim_text` is adjudication content, and both
this order and the correction order forbid altering it — so it is recorded for a
future owner-authorized pass rather than raised as a blocker.

## 4. Q7 — RW024

```
RW024 use = WITHIN_LEDGER_SUPPORTED_SCOPE
```

Manuscript text, §3 currentness-gate paragraph:

> "valid-time and transaction-time distinctions are established in bitemporal
> data models [17]"

SOURCE-LEDGER-003 records for RW024, under `exact_capabilities_supported`:

> "valid time versus transaction time as distinct temporal dimensions"

The manuscript proposition is the recorded capability, near verbatim. It is
background attribution placed among four precedents; it carries no strength
adverb, no *proved*, no *measured*, and nothing in the contribution rests on it —
RW024 appears in no S1/S8/X1 argument.

The ledger's limitation reads: *"Located and read at summary level; chapter PDF
not extracted. FULL_TEXT_UNAVAILABLE for strong findings."* The operative
qualifier is **for strong findings**. This is not one. `evidence_strength` is
MODERATE and `comparison_status` is PARTIAL_PRECEDENT; a MODERATE background
attribution is precisely the weight the ledger will carry.

I raised, and then withdrew, a disclosure objection here. My concern was that a
reader of the manuscript cannot see that [17] was never retrieved in full. I
checked the audit rather than asserting it: the candidate's citation audit records
`evidence_depth: FULL_TEXT_UNAVAILABLE` for RW024 at **both** sites where it is
cited, and does the same for RW006, RW009, RW011 and RW017. The disclosure exists
at the audit layer, which is where per-source evidence depth belongs. The
objection does not survive.

## 5. Q8–Q12, Q15 — measured verification

Every number below was computed against the candidate bytes. I did not accept the
audit's own booleans as the finding.

**5.1 Q8 — visible citations for external substantive claims.  VERIFIED.**

```
independent paragraph scan of the manuscript body, 26 named external systems,
requiring a visible [n] marker in the same paragraph
  paragraphs naming an external system with no marker      0

candidate audit external_comparison_claims                 27
  entries whose declared labels do not map to the declared
  RW ids via the manuscript's own bibliography              0
  declared labels absent from the manuscript                0
```

The audit's `manuscript_location` is prose (`"§3, currentness-gate paragraph"`)
rather than a line number. My first pass treated it as a line number and produced
27 spurious failures; that was my check's wrong assumption, not a defect. Re-run
correctly against label→source mapping, it is clean — and prose anchors are the
more durable choice, since line numbers drift on any edit.

**5.2 Q9 — bibliography mapping.  VERIFIED.**

```
bibliography entries                                       23
entries carrying an (RWxxx) ledger tag                     23
tagged sources absent from SOURCE-LEDGER-003                0
labels cited in the body but absent from the bibliography    0
bibliography entries never cited in the body                 0
RW018 (NOT_RELEVANT_AFTER_REVIEW) cited                     no
source_ledger_sha256 declared by the audit
  = 49bb905028872b79280854056a34716d88eee634d8f28b998a89c2c289f0630f  reproduced
```

Ranged markers (`[5–7]`, `[19–22]`, `[1–23]`) were expanded before checking, so no
member of a range escaped the mapping test.

**5.3 Q10 — prohibited vocabulary.  VERIFIED.**

```
\bno prior work\b 0 · \bnovel\b 0 · \bunique\b 0
\bunprecedented\b 0 · \bwe are the first\b 0 · state of the art 0
```

`\bfirst\b` occurs twice, both structural and neither a priority claim: *"the
first unmet component in the frozen order"* and *"derived from the first"*.

**5.4 Q11 — Proof of Execution, D5 and D7.  VERIFIED.**

PoE (RW027, `[19]`) leads the precedent statement in the abstract, in §7, in §10
and in §13's *Contemporary agent governance*, and is the strongest source in
FINDINGS-003 §14. It remains the nearest technical precedent in the text.

D5 — evaluation gates issuance, adjudicated **PRECEDED** by RW027 — is disclaimed
in the manuscript's own words: *"That evaluation gates issuance is not a
distinction this work can claim."*

D7 — preserved history under later revocation, adjudicated **PRECEDED** by RW027,
RW030, RW021 — is attributed to Rhodes and Kang in §13 (*"revocation at a later
instant does not retrospectively invalidate an execution valid earlier"*) and
listed in §14 among the precedents closed with *"None of those is claimed here."*

Neither appears in S1, S8 or X1.

**5.5 Q12 — the surviving distinction and its bounding.  VERIFIED.**

S1 + S8 + X1 are the only distinction advanced, in §2, §7, §13 and §14, and §2
adds *"only the integrated S1 + S8 + X1 chain carries the contribution."* The
bounding is not left to a single disclaimer: the abstract phrases it as *"what we
did not find in the systems examined"*; §13 opens with **"Search completeness is
not claimed, and absence from a search is not evidence of absence"**; §13's
closing paragraph and §14 both say *"Among the sources examined"*; and §12 points
back to *"a bounded adversarial search whose completeness is not claimed."*

This is the second place I looked for a defect and did not find one. The negative
finding is carried consistently as *not found in a bounded set*, never as absence
in the world.

**5.6 Q15 — claims and ceiling.  VERIFIED.**

```
claims                                       57
claim_ceiling_compatible = false               0
claim map sha256                             69b8b50f…  byte-identical to the
                                             pre-correction baseline
owner_intellectual_adjudication              unchanged; surviving properties
                                             S1_PRESERVED_EPISTEMIC_STATE,
                                             S8_DOWNSTREAM_…_BEFORE_RELIANCE,
                                             X1_NOT_EVALUATED_WITH_CAUSAL_GATE_PRESERVED
```

The claim map was not touched. Given that claims carry no manuscript-location and
no citation-binding fields, nothing in the correction order's §7 trigger applied,
and leaving the bytes alone is the correct outcome rather than an omission.

**5.7 Quotations — checked independently because the audit no longer checks them.**

The candidate audit drops the predecessor audit's `quotations` block. I verified
all three verbatim quotations myself against SOURCE-LEDGER-003:

```
"have not failed but there is insufficient information to determine"   RW022  verbatim present
"KeyNote does not directly enforce policy; it only provides advice
 to the applications that call it"                                     RW004  verbatim present
"neither unified nor static"                                           RW021  verbatim present
```

Each occurs exactly once in the manuscript and each is verbatim in the ledger. The
manuscript is sound. The audit's coverage narrowed; see O2.

## 6. Q13 — independent render

Rendering was possible. Performed with a real Mermaid parser, not asserted.

```
renderer     @mermaid-js/mermaid-cli (mmdc) with puppeteer/Chromium
command      mmdc -i RESULT-001-ARCHITECTURE-RELATED-WORK-001.mmd -o cand-arch.svg
exit code    0
output       65243 B
output sha256 96b1b5b23bda87789781ddc7ec2d1329782821c4ff95711d8d4dad025f8fdacb
rendered from candidate .mmd sha256 67041c97…  (fetched from PR #13 head, unmodified)
```

```
top-level flowchart declarations       1
subgraphs                              A, B, C, with INPUTS and OUTPUTS nested in B
rendered nodes / clusters              69 / 14
"Syntax error" graphic in output       absent
```

**Semantic equivalence against the frozen predecessor `1f110c80…`** — eighteen
load-bearing tokens present in predecessor, candidate and rendered SVG alike:

```
Semantic separation is not causal independence · CURRENTNESS_GATE_DID_NOT_PROCEED
NO EXAMINED PRECEDENT FOUND · INTEGRATION_RESULT_ONLY · NOT a novelty claim
Search completeness · epistemic_status · institutional_authorization_status
execution_disposition · decision_basis · PRECAUTIONARY · first unmet component
not rewritten by currentness · Publication: NOT AUTHORIZED · 31 examined sources
pinned external kernel · separate OS process · single-use, exclusive creation

classDef statements   5 → 5     class assignments   5 → 5
```

The three former top-level parts became subgraphs A, B and C with no loss of
node, edge, annotation or styling semantics. The predecessor's own render defect —
five content-free `%%` lines that the installed Mermaid comment regex (`[^\n]+`)
does not strip, and which therefore reach the parser — is absent from the
candidate: it contains zero bare `%%` lines. That defect was independent of the
three-flowchart problem and would have blocked rendering on its own.

## 7. Q14 — public-review projection, disclosure review

```
SOURCE_PROJECTION_DERIVATION_INDEPENDENTLY_VERIFIED = FALSE
```

I do not possess `RESULT-001-RESEARCH-ARTIFACT-SOURCE-MANIFEST-RELATED-WORK-001.json`
(`556477c5…`, 8072 B). It is withheld by design and recorded as such in the
transport manifest. I therefore make **no** claim that the projection was
correctly derived from those bytes, that `$.internal_source_locations` was its
only occurrence of that field, or that all other data is equivalent. Those
propositions are untested here.

What I could check on the projection bytes themselves, I did:

```
actual JSON keys named internal_source_locations              0
occurrences of that string                                    1 — inside
                                                              projection_metadata.omitted_json_paths
                                                              i.e. the declaration, not the data
local filesystem paths (/home, /media, /tmp, /Users, X:\,
  file://)                                                    0
projection_metadata present and complete                      yes
  source_artifact_filename / source_artifact_sha256           declared;
                                                              sha matches 556477c5…
  projection_rule                                             OMIT_INTERNAL_SOURCE_LOCATIONS_ONLY
  omitted_json_paths                                          ["$.internal_source_locations"]
  projection_is_source_artifact                               false
  public_review_projection                                    true
transport manifest consistency                                created 6 / transported 5;
                                                              withheld entry names 556477c5…, 8072 B,
                                                              artifact_edited_to_enable_publication = false
```

No disclosure defect is found in the bytes available to me. Observation O3 records
one internal contradiction that is a consequence of the omit-only rule, not a
violation of it.

## 8. Observations — recorded, none blocking

**O1 — §8 header/body term mismatch.** The bold separation at §8 enumerates
`OBSERVATION ≠ CRITERIA ≠ ADJUDICATION ≠ OWNER CLAIM DECISION`, but the body now
explains *Observations*, *Criteria*, *Evidence closure* and *The owner claim
decision*. The term ADJUDICATION in the header is no longer defined below it, and
the predecessor's statement that *RESULT-001 instantiates no separately named
adjudication artifact* has been dropped — while claim-map R043 still asserts
exactly that. The rename itself is an improvement, since it stops the closure
record from reading as an adjudication act; what is left is an undefined header
term and a claim whose manuscript support is gone. Editorial, not a claim-integrity
defect: nothing false is asserted, and R043 remains true independently of the
manuscript.

**O2 — narrowed audit coverage.** The candidate audit drops the predecessor's
`quotations` verification block and its `prohibited_vocabulary_occurrences`
counter. Both properties still hold — I verified them in §5.3 and §5.7 — but they
are no longer machine-recorded in the artifact that exists to record them.
Verbatim quotation is where fabrication risk is highest; a successor audit should
carry that block again.

**O3 — projection `$comment` contradicts the projection.** The public-review
projection carries the source artifact's `$comment` verbatim: *"INTERNAL. …
Retains internal source locations for drafting…"* — which is false of the
projection, and labels a public-review artifact INTERNAL. No value is disclosed.
This is the **correct** output under `OMIT_INTERNAL_SOURCE_LOCATIONS_ONLY`:
editing `$comment` would have breached *omit only*. The contradiction is produced
by the projection rule, not by the implementer, and `projection_metadata` is the
authoritative disambiguator. A future owner-authorized pass may either add a
projection note or authorize `$.$comment` as a second omitted path; neither is
available under the present rule.

**O4 — R043 lacks §8's qualifier.** Recorded in §3 above.

## 9. Claim ceiling — unchanged by this review

```
this review establishes                 NOTHING about RESULT-001's technical content
independent reproduction                NOT ESTABLISHED
independent assurance                   NOT ESTABLISHED
production readiness                    NOT ESTABLISHED
institutional or legal validity         NOT ESTABLISHED
publication                             NOT AUTHORIZED
```

This record reviews artifacts for internal consistency, citation integrity,
disclosure safety and conformance to the owner's adjudicated intellectual
position. It does not re-adjudicate the science, re-open the related-work search,
or verify the underlying RESULT-001 evidence bytes, which remain owner-held and
which this reviewer has never held.

## 10. Decision

```
ACCEPT_EXACT_HEAD_BF0882B2
```

Fifteen review questions answered; twelve verified by computation against the
candidate bytes, one (Q14 derivation) explicitly recorded as not independently
verifiable, and R043 adjudicated ACCEPTABLE_HISTORICAL_DESCRIPTION. Four
observations recorded, none blocking. No concrete defect was found that is tied to
candidate text or artifact identity and that would make an artifact false, unsafe
to disclose, or inconsistent with the owner's adjudicated position.

```
reviewed_head            bf0882b2f3dad4719633d5c31737244bcf2ecf27
evidence_modified        FALSE
stage_paths_modified     FALSE
owner_decisions_authored FALSE
publication_authorized   FALSE
```
