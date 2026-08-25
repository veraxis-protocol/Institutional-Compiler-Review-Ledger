# Agent operating boundary

This repository transports and mechanically verifies evidence about the
Institutional Compiler. It does not contain or authorize mutations to the
governed source repository.

## Non-negotiable distinctions

- A commit is transport, not acceptance.
- A GitHub actor is transport attribution, not proof of institutional role.
- Agent identity and contribution trailers are supplemental provenance only.
- Mechanical verification, independent review, owner acceptance, and persisted
  accepted state are separate transitions.
- Producer, verifier, and adjudicator must be distinct.

Never infer authority from prose, a branch name alone, a username alone, CI
PASS, or a merge. Resolve role and path authorization through
`ROLE-IDENTITY-MAP.json`, `policy/PATH-AUTHORITY.json`, the relevant owner or
reviewer artifacts, and cryptographic identities.

## Safe commands

```bash
make verify     # verify current ledger mechanics and accepted manifests
make falsify    # run valid and fail-closed public cases in disposable copies
make ci         # both of the above
```

Direct verifier commands are:

```bash
python3 verifier/ledger_core_verifier.py verify-all
python3 verifier/ledger_core_verifier.py verify-checkpoint-pin
python3 verifier/ledger_core_verifier.py verify-workflow
python3 verifier/ledger_core_verifier.py verify-identity-map
```

`verify-pr` additionally requires the literal actor, authorized branch, base
SHA, and head SHA. Do not invent or substitute those values.

## Authorized branch and path classes

The machine-readable policy is authoritative. At this version:

- `evidence/` → implementer evidence under `stage-*/**`;
- `review/` → independent-review records under `reviews/**`;
- `owner/` → owner decisions under `owner-decisions/**`; and
- `infra/` → protected repository infrastructure.

The historical `bootstrap/**` tree is retained evidence only. `BOOTSTRAP` is a
retired authority and must never be reintroduced.

## Agent provenance and telemetry

Optional contribution trailers are:

```text
Agent-Assisted-By: <system and model>
Veraxis-Skill: <skill or workflow name>
Agent-Execution-ID: <optional attributable execution identifier>
```

They cannot override the role map, branch/path classes, owner/reviewer
artifacts, accepted-state pins, or cryptographic identity. The verifier is
local and secrets-free and sends no telemetry. No hosted Veraxis gateway,
remote agent context service, or MCP server is established here.

Every producer return must state **NOT SELF-ADJUDICATED** and stop for
independent review.

