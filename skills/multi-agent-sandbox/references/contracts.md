# Multi-Agent Sandbox Contracts

Use these contracts so actor outputs can be traced, validated, and compared across branches. Keep exact IDs, evidence references, decisions, and constraints when compressing context.

## Run workspace

```text
brain/workspace/simulations/<run-id>/
├── scenario.md          human-readable task frame and assumptions
├── state.json           current machine-readable world state
├── agents.json          role cards and access scopes
├── evidence-ledger.md   facts, assumptions, and source references
├── events.jsonl         append-only event and audit log
├── metrics.json         deterministic run summary, when generated
├── report.md            decision report draft
└── rounds/              immutable round checkpoints
```

`scenario.md`, `report.md`, and the evidence ledger are human review surfaces. JSON and JSONL files are orchestration state, not canonical memory.

`state.json` must keep one shared `world_seed` and a separate `branch_states` object keyed by branch ID. Each branch state owns its variables, relations, uncertainties, round, and accepted event IDs. Never share a mutable state object across branches.

## Role card

Each object in `agents.json` must contain:

```json
{
  "role_id": "buyer",
  "name": "Pragmatic enterprise buyer",
  "role_type": "actor",
  "objective": "Reduce switching risk while improving value",
  "incentives": ["reliability", "budget control"],
  "constraints": ["annual procurement cycle"],
  "resources": ["vendor comparisons"],
  "allowed_actions": ["ask", "delay", "pilot", "buy", "reject"],
  "observed_evidence_refs": ["E1", "E3"],
  "unknowns": ["migration effort"],
  "read_scope": ["world_snapshot", "public_events"],
  "write_scope": ["actor_turn"],
  "prohibited_actions": ["invent private facts", "execute external side effects"]
}
```

Use `role_type` values `orchestrator`, `actor`, `auditor`, or `observer`. The root agent normally performs the orchestrator role and should not impersonate an actor.

## ActorTurn

Actor agents must return one JSON object and no hidden reasoning trace:

```json
{
  "round": 1,
  "branch_id": "baseline",
  "role_id": "buyer",
  "observations": [
    {"statement": "The launch price is 20% above the current plan", "evidence_refs": ["E3"]}
  ],
  "interpretation": "The savings claim is not yet credible enough to offset switching risk.",
  "action": {
    "kind": "request_pilot",
    "target": "operator",
    "summary": "Request a 30-day pilot with rollback terms."
  },
  "brief_rationale": "A reversible test preserves option value.",
  "expected_effects": ["slower contract close", "better evidence"],
  "assumptions": ["the buyer can negotiate a pilot"],
  "confidence": 0.66,
  "state_updates": [],
  "follow_up_triggers": ["migration plan published"]
}
```

Requirements:

- `confidence` is between `0` and `1` and reflects confidence in the action logic, not a forecast probability.
- Observations must reference the evidence ledger or a prior event ID.
- Assumptions must remain explicit.
- `brief_rationale` is a short justification, not chain-of-thought.
- Actors may not update global state directly; they only propose `state_updates`.

## Event record

`events.jsonl` uses one JSON object per line:

```json
{
  "schema_version": 1,
  "event_id": "evt-...",
  "trace_id": "trace-...",
  "timestamp": "2026-08-06T10:00:00+08:00",
  "round": 1,
  "branch_id": "baseline",
  "actor_id": "buyer",
  "kind": "action",
  "summary": "Requested a reversible pilot.",
  "brief_rationale": "Reduces switching risk.",
  "evidence_refs": ["E3"],
  "assumptions": ["Pilot capacity exists"],
  "confidence": 0.66,
  "effects": {"sales_cycle_days": 30},
  "status": "accepted"
}
```

Allowed `kind` values:

- `run_initialized`
- `observation`
- `intention`
- `action`
- `reaction`
- `world_update`
- `audit`
- `interview`
- `decision`

Allowed `status` values are `proposed`, `accepted`, `rejected`, and `flagged`.

Do not add keys such as `chain_of_thought`, `hidden_reasoning`, or `private_reasoning`.

## World update

The orchestrator converts accepted turns into one compact delta:

```json
{
  "branch_id": "baseline",
  "round": 1,
  "accepted_events": ["evt-a", "evt-b"],
  "facts_added": [],
  "variables_changed": {"buyer_interest": {"from": "medium", "to": "high"}},
  "relations_changed": [],
  "conflicts": [],
  "open_uncertainties": ["pilot capacity"],
  "rationale": "Only consequences supported by declared rules were applied."
}
```

Simulated facts belong to the branch state only. Never place them in the evidence ledger's sourced-fact rows.

## Evidence ledger

Use four claim classes:

| Class | Meaning | May seed actors? | May become canonical memory? |
|-|-|-|-|
| fact | Backed by a real source reference | yes | only through normal brain ingestion/enrichment |
| assumption | Chosen modeling condition | yes, labeled | no |
| simulated | Produced inside a branch | yes, within that branch | no |
| unknown | Missing information | as a question | no |

Every important report statement should cite an evidence ID, event ID, or state explicitly that it is a synthesis judgment.

## Report contract

`report.md` should include:

1. Decision implication
2. Simulation boundary and horizon
3. Branch comparison
4. Stable patterns across branches
5. Disagreements and causal mechanisms
6. Early indicators and trigger thresholds
7. Evidence and assumption audit
8. Failure modes and reversible next moves
9. Confidence and limitations

Do not report a numerical probability unless it comes from a calibrated external model. Agent vote shares and branch counts are not real-world probabilities.
