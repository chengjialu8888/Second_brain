# Multi-Agent Sandbox Playbook

## Contents

1. Topology
2. Role selection
3. Branch design
4. Round protocol
5. Adjudication
6. Memory and context
7. Failure recovery
8. Evaluation
9. Scenario patterns

## 1. Topology

Use a hierarchical fan-out/fan-in topology:

```text
evidence -> orchestrator/world keeper -> actor wave(s)
                  |                         |
                  +---- auditor <-----------+
                  +---- observer -----------+
                  -> checkpoint -> next round or report
```

The orchestrator owns task framing, role assignment, immutable event recording, state transitions, branch creation, stop decisions, and synthesis. Actors own local choices only. The auditor checks evidence and contract compliance. The observer measures patterns without changing the world.

Avoid a mesh unless negotiation itself is the subject. If a mesh is necessary, impose a moderator, a maximum of three exchange rounds, a shared message schema, and a deadlock exit.

## 2. Role selection

Select roles by causal influence, not job-title completeness. Include:

- the decision maker or operator
- the most affected stakeholder
- the strongest credible opponent or substitute
- one gatekeeper with veto or delay power
- one information amplifier when narrative spread matters
- one observer or auditor that does not act in-world

Test diversity across:

- incentives: growth, safety, cost, status, mission, control
- resources: authority, money, data, distribution, attention
- information: early knowledge, delayed knowledge, uncertainty
- tempo: immediate reaction, slow deliberation, periodic review
- risk posture: conservative, neutral, opportunistic

Merge roles whose choices would be materially identical. Split a role only when its distinct incentives change the causal path.

## 3. Branch design

Start with three branches when useful:

- `baseline`: current best estimate of external conditions
- `adverse`: one high-impact assumption fails
- `upside`: one enabling condition improves

Change one or two variables per branch. Keep role cards, evidence, and world rules constant unless the branch explicitly changes them. Name the intervention and the expected causal pathway before the run.

Use a branch matrix:

| Branch | Changed variable | Fixed variables | Expected mechanism | Falsifying signal |
|-|-|-|-|-|
| baseline | none | all | reference path | material deviation |
| adverse | procurement delay | price, product | cash pressure | fast approvals |
| upside | channel adoption | product, price | lower acquisition cost | weak partner activation |

## 4. Round protocol

Use this sequence:

### Seed

Broadcast a compact snapshot containing branch ID, simulated time, public state, relevant evidence IDs, prior accepted event IDs, and the decision point. Do not include other roles' private constraints.

### Independent turns

Run actors in parallel when they have no dependency. When capacity is limited, use waves and freeze the snapshot so later waves do not gain accidental information.

### Adjudication

Reject malformed turns, impossible actions, leaked knowledge, and side effects outside the sandbox. Apply accepted actions using declared world rules. When rules do not determine the outcome, record the adjudication as an assumption and lower confidence.

### Audit

Check:

- every observation has evidence or a prior event ID
- no role uses information outside its read scope
- the same assumption is applied consistently across branches
- confidence is not disguised probability
- synthetic quotations are labeled
- no external write or irreversible action occurred

### Observe

Track only decision-relevant indicators, such as coalition formation, adoption intent, delay, sentiment direction, resource depletion, veto risk, information spread, and unresolved contradictions.

### Checkpoint

Write a round checkpoint and a compact per-role memory summary. The next round receives the checkpoint, not the full transcript.

## 5. Adjudication

Prefer deterministic rules:

1. Explicit scenario rule
2. Sourced institutional constraint
3. Stable branch assumption
4. Conservative default
5. Human decision when the consequence is high impact

When actor actions conflict, resolve by authority, resource, timing, and dependency rules rather than prose persuasiveness. Record rejected actions and why.

Do not let the orchestrator both advocate a preferred outcome and adjudicate in its favor. If bias risk is high, assign adjudication to an independent role and have the evidence auditor review it.

## 6. Memory and context

Maintain three layers inside the run:

- immutable event log: exact accepted/rejected actions and audits
- branch state: current variables, relationships, and uncertainties
- role memory summary: what that role observed, decided, and still does not know

Use stable IDs. Keep source facts separate from simulation events. Preserve exact numbers, dates, constraints, and decisions when compressing; summarize narrative prose.

## 7. Failure recovery

| Failure | Detection | Recovery |
|-|-|-|
| Agent timeout | no result by deadline | retry once with narrower scope, then use a conservative no-action turn |
| Schema failure | invalid ActorTurn | request missing fields once, then reject and log |
| Hallucinated fact | missing evidence ref | relabel as assumption or reject |
| Contradiction | incompatible accepted turns | record conflict, adjudicate by rules, retain dissent |
| Context leak | role knows hidden state | reject turn and rerun from scoped snapshot |
| Loop | no novelty for two rounds | stop and report convergence |
| Budget exhaustion | hard limit reached | checkpoint and produce a degraded report |
| Unsafe action | policy or blast-radius trigger | block and request human review |

Always produce a structured degraded result containing completed rounds, missing branches, unresolved conflicts, and the next safe step.

Define a wall-clock deadline before the first actor call. When it expires, stop all actor work, preserve completed events, create a checkpoint, write a degraded report, and finalize. After the last allowed round or any stop condition, the orchestrator must not start new interviews or role calls.

## 8. Evaluation

Evaluate the run on:

- evidence coverage: accepted non-system events with at least one evidence/event reference
- assumption visibility: important modeled conditions explicitly logged
- branch isolation: changed variables are controlled and documented
- role distinctiveness: roles take causally different actions for clear reasons
- contradiction retention: disagreement is preserved instead of averaged away
- decision usefulness: report contains triggers, reversible moves, and falsifiers
- reproducibility: another agent can resume from the checkpoint

Treat high unsupported confidence, identical actor outputs, and untraceable state changes as failures.

## 9. Scenario patterns

### Product launch

Roles: target buyer, existing user, operator, incumbent competitor, channel partner, procurement/security gatekeeper.

Indicators: trial intent, switching friction, objections, time-to-value, channel conflict, incumbent response.

### Policy or public-opinion exercise

Roles: affected citizen archetypes, implementing agency, opposition group, media/amplifier, domain expert, regulator.

Indicators: misunderstanding, compliance friction, narrative mutation, trust, organized resistance, implementation capacity.

Use archetypes and public evidence. Do not assert how a named private person will behave.

### Competitive war game

Roles: focal operator, incumbent, fast follower, substitute, buyer, distributor, regulator.

Indicators: price response, bundling, distribution lock-in, imitation time, differentiation durability.

### Organizational decision

Roles: executive sponsor, operating team, dependent team, finance, security/legal, skeptical employee archetype.

Indicators: execution load, hidden dependencies, veto points, morale risk, time-to-decision.
