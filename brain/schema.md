# Brain Schema

All entity pages use:

```markdown
---
type:
title:
aliases: []
source_refs: []
created:
updated:
confidence: low
---

# Title

> Executive summary.

## State
## Assessment
## Open Threads
## See Also

---

## Timeline

- **YYYY-MM-DD** | Source - What happened.
```

## Required Concepts

- **Compiled Truth**: Everything above `---`. It is the current synthesized view and can be rewritten.
- **Timeline**: Everything below `---`. It is append-only evidence.
- **Source refs**: Relative paths or URLs that back claims.
- **Open Threads**: Unresolved questions, follow-ups, or missing context.
- **L0 Raw Evidence**: Original source snapshots in `brain/sources/`.
- **L1 Atomic Memory**: One compact source-backed fact, decision, constraint, preference, or numeric signal.
- **L2 Scene Memory**: A compact scenario block that restores a project, decision thread, user-research theme, or recurring work context.
- **L3 Operating Memory**: Stable user, team, preference, or strategic context that should be used sparingly.
- **Asset Loadout**: `brain/assets.yaml` records which reusable assets are available to workflows and agent roles. It is not evidence.

## Person Page

```yaml
type: person
title:
aliases: []
relationship:
importance: tier1 | tier2 | tier3 | unknown
first_seen:
last_seen:
source_refs: []
confidence: low | medium | high
open_threads: []
```

Recommended sections:

- State
- What They Believe
- What They're Building
- Relationship
- Communication Style
- Assessment
- Network
- Open Threads
- See Also
- Timeline

Judgment sections should mark claims as observed, self-described, or inferred.

## Concept Page

```yaml
type: concept
title:
aliases: []
status: emerging | established | validated
source_refs: []
related: []
confidence: low | medium | high
```

Recommended sections:

- Definition
- Why It Matters
- My Current Read
- Counterexamples / Risks
- Related
- Timeline

## Project Page

```yaml
type: project
title:
status: idea | mvp | active | paused
goal:
success_metrics: []
source_refs: []
open_threads: []
```

Recommended sections:

- Goal
- Current State
- Decisions
- Open Threads
- Success Metrics
- Related
- Timeline

## Diary Page

```yaml
type: diary
date:
status: draft | confirmed
source_refs: []
people: []
projects: []
places: []
```

Recommended sections:

- Timeline
- Highlights
- People / Projects / Places
- What I Felt
- Open Questions
- Diary Draft

Diary pages generated from calendar are `draft` until the user adds subjective context.

## Dashboard Page

```yaml
type: dashboard
title:
aliases: []
updated:
confidence: low | medium | high
```

Recommended sections:

- At A Glance
- Review Items
- Agent Maintenance Rules
- Timeline

Dashboard pages are navigation surfaces for humans. They should summarize what to inspect next, not duplicate raw sources or canonical entity pages.

## Workspace Page

```yaml
type: workspace
title:
aliases: []
updated:
as_of:
source_window:
  start:
  end:
task:
mode: active-workspace | strategy-report | multi-agent-sandbox
status: draft | reviewed | archived
confidence: low | medium | high
source_refs: []
```

Recommended sections:

- Task Frame
- Date Boundary
- Capacity Budget
- Candidate Evidence
- Active Context
- Coverage Matrix
- Claim Audit
- Specialist Lens Routing
- Output Contract
- Excluded / Out Of Window
- Timeline

Workspace pages are task-scoped reasoning surfaces. They make active context inspectable before final output, but they are not canonical facts. Move durable confirmed claims into entity pages.

Multi-Agent Sandbox workspaces may use a run directory containing `scenario.md`, machine-readable state, an append-only event log, round checkpoints, and `report.md`. Simulated events and quotes are never evidence and must not be moved into canonical pages.

## Memory Atom Page

```yaml
type: memory_atom
title:
aliases: []
atom_id:
status: current | historical | planned | cancelled | conflicting
event_date:
captured_at:
source_refs: []
entities: []
projects: []
confidence: low | medium | high
visibility: private | project | public
```

Recommended sections:

- Claim
- Evidence
- Status
- See Also
- Timeline

Each atom should carry one compact claim and enough source metadata to drill down to L0 evidence.

## Memory Scene Page

```yaml
type: memory_scene
title:
aliases: []
scene_id:
status: active | stale | archived
created:
updated:
source_refs: []
atom_refs: []
entities: []
projects: []
confidence: low | medium | high
visibility: private | project | public
```

Recommended sections:

- Scene Summary
- Active Facts
- Decisions / Constraints
- Open Threads
- Recall Guide
- See Also
- Timeline

Scene pages are L2 recall surfaces. They should be short enough to index and skim, but rich enough to restore a work context without rereading every raw source.

## Templates

Obsidian-ready templates live in `brain/templates/`. They are starter files, not memory pages, and are skipped by structural lint.
