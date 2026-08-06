# Memory Layers and Asset Loadout

Second Brain stays Markdown-first, but it now names memory layers explicitly so agents can recall less while recalling better.

This design is inspired by TencentDB Agent Memory's L0-L3 layering, memory assets, and agent loadout model:

- https://github.com/TencentCloud/TencentDB-Agent-Memory
- https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/main/MemoryCore/README.md
- https://github.com/TencentCloud/TencentDB-Agent-Memory/blob/main/MemoryKnowledge/README.md

The lesson we adopt is operational, not infrastructural: keep upper layers compact and usable, while preserving a deterministic drill-down path to raw evidence.

## Layer Model

| Layer | Second Brain Surface | Job | Recall Default |
|-|-|-|-|
| L0 Raw Evidence | `brain/sources/` | Preserve original chats, docs, PDFs, calendar dumps, and web snapshots | Read only when exact wording, provenance, or conflict resolution matters |
| L1 Atomic Memory | `brain/templates/memory-atom.md`, future `brain/memory/atoms/` | Store small dated facts, decisions, constraints, preferences, and numeric signals | Retrieve for precise claims, dates, status, and contradiction checks |
| L2 Scene Memory | `brain/templates/memory-scene.md`, future `brain/memory/scenes/` | Restore a project, decision thread, user-research theme, or recurring work scenario | Inject as a short scene index, then drill down only when useful |
| L3 Operating Memory | canonical pages, `brain/profile.md` when introduced | Keep stable preferences, working style, strategic frames, and durable context | Inject sparingly as stable background |
| Active Workspace | `brain/workspace/` | Hold the current task's small active context, coverage matrix, claim audit, or bounded scenario simulation | Use for high-stakes, date-bounded, or multi-Agent synthesis |

Compiled Truth and Timeline remain the human-readable canonical page model. L0-L3 names are the agent recall model that sits beside it:

```text
L0 source
  -> L1 atom
  -> L2 scene
  -> L3 operating memory
  -> active workspace
  -> final deliverable
```

## Drill-Down Contract

Every upper-layer memory should be expandable:

```text
L3 operating memory
  -> L2 scene
  -> L1 atom
  -> L0 source ref
```

When a claim is important, the agent should be able to answer:

- What is the compact claim?
- What exact source backs it?
- What date did the event happen?
- When was it captured?
- Is it current, historical, planned, cancelled, or conflicting?
- What would change the conclusion?

If that chain is missing, mark the claim as inferred or low confidence.

## Asset Loadout

`brain/assets.yaml` is the lightest possible control plane. It does not store memory content. It registers which reusable assets exist and which agents or workflows should receive them.

Asset types:

- `memory`: profile, atom set, scene set, source pack, or workspace template
- `skill`: reusable workflow or output lens
- `wiki`: human-readable knowledge surface
- `codegraph`: future code graph or impact map
- `source-pack`: bounded set of source snapshots for a task

Loadout rules:

- Keep assets private by default.
- Bind assets to workflows or agent roles only when useful.
- Prefer a small scene index plus tools over raw source injection.
- Track status and version so stale assets are not treated as current truth.

## Recall Assembly

For ordinary lookup:

```text
query
  -> search canonical pages and L1 atoms
  -> read relevant pages
  -> answer with source refs and gaps
```

For high-stakes synthesis:

```text
task
  -> choose asset loadout
  -> generate recall plan
  -> retrieve L1/L2 evidence
  -> build evidence ledger
  -> compose active workspace
  -> apply specialist lens
  -> write final deliverable
  -> move durable facts back into canonical pages
```

The goal is not automatic memory everywhere. The goal is explicit, bounded context assembly.

Simulation outputs under `brain/workspace/simulations/` are synthetic active-workspace state. They may cite L0-L3 evidence, but they never flow back into L0-L3 as facts. Only independently confirmed real-world information may enter canonical memory through the normal ingestion and enrichment workflow.

## Implementation Posture

Do not add a database until Markdown search becomes the bottleneck. The near-term upgrades are:

1. Use templates for atoms and scenes.
2. Add source IDs and atom IDs to claim audits.
3. Keep `brain/assets.yaml` reviewed and small.
4. Add optional SQLite FTS5 later for speed, not as the source of truth.
5. Add vector search only when keyword and graph-like Markdown links stop being enough.
