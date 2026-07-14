# Architecture

Second Brain is intentionally small at the storage layer and disciplined at the workflow layer.

## Design Principles

1. **File-system first**: Markdown files are the source of truth.
2. **Obsidian-friendly**: humans can browse backlinks and graph view without special infrastructure.
3. **Agent-maintained**: agents follow resolver, schema, and skill contracts before writing.
4. **Evidence-first**: raw sources stay preserved; summaries cite sources.
5. **Search then think**: retrieval and synthesis are separate operations.
6. **Workspace-bounded synthesis**: high-stakes outputs pass through a small active workspace before final writing.

## Layers

<p align="center">
  <img src="../assets/product-flow.svg" alt="Second Brain product flow and core architecture" width="100%">
</p>

## Operational Anatomy

Second Brain is best understood as a discontinuous agent experience with continuous memory. The agent session can end at any time; the filesystem carries continuity across sessions.

The July 6, 2026 Anthropic Global Workspace / J-space research is useful as an analogy, not as a dependency. It suggests that flexible reasoning benefits from a small shared space whose contents are reportable, controllable, used in reasoning, broadcast to downstream capabilities, and capacity-limited. Second Brain implements that as an explicit `brain/workspace/` layer between retrieval and final output.

The architecture therefore has organs, not only components:

| Organ | Repository surface | Filter | Fissure |
|-|-|-|-|
| Body | `brain/`, Markdown files, scripts | Treat the filesystem as the source of truth | A file can preserve context without proving it is important |
| Source layer | `brain/sources/` | Preserve raw evidence before synthesis | A captured source can still be incomplete or stale |
| Compiled Truth | Entity pages above `---` | Keep current understanding readable and revisable | A synthesis can overfit the latest evidence |
| Timeline | Entity pages below `---` | Keep dated, append-only evidence | Chronology does not explain causality by itself |
| Resolver | `brain/RESOLVER.md` | Route pages by ownership and future use | Ambiguous material still needs human judgment |
| Schema | `brain/schema.md` | Give agents a stable page shape | Structure cannot decide what is worth remembering |
| Human cockpit | `brain/dashboards/`, Obsidian templates and snippets | Show what changed, what needs review, and what humans should answer next | A dashboard can guide attention without replacing judgment |
| Active workspace | `brain/workspace/`, `skills/active-workspace.md`, `scripts/workspace_compose.py` | Keep the current task's evidence, assumptions, date window, coverage matrix, and claim audit visible | A workspace can organize reasoning without proving the underlying sources are complete |
| Skills | `skills/` and `SKILL.md` | Turn capture, ingest, query, enrichment, lint, and diary into repeatable workflows | Workflow correctness does not guarantee good judgment |
| Search | `scripts/brain_search.py` | Retrieve candidate evidence before synthesis | Search results are evidence, not the answer |
| Immune system | `scripts/wiki_lint.py` and lint workflow | Detect broken structure, stale drafts, and missing evidence | Lint can detect damage, not define the ideal brain |
| Diary | `brain/diary/` and calendar workflow | Convert objective schedule traces into draft memory | Calendar knows what happened; only the user knows what it meant |
| Agent interface | `AGENTS.md`, `llms.txt`, CLI wrapper | Make the brain legible to different agents | Instructions can be followed mechanically without understanding intent |

This framing keeps capabilities honest. Each organ should state both the filter it applies and the fissure it cannot close.

## Memory Loop

```text
external trace
  -> source snapshot
  -> resolver decision
  -> canonical page or diary draft
  -> Compiled Truth update
  -> Timeline evidence
  -> search / think / lint
  -> active workspace for high-stakes synthesis
  -> specialist lens if useful
  -> follow-up questions
  -> human context
```

The loop separates storage, evidence, synthesis, and maintenance. That separation is the main architectural bet: personal memory should be inspectable before it becomes automated.

## Spine, Not Full Knowledge Graph

The MVP should not pretend to be a complete knowledge graph. Its first spine is weaker and more useful:

- wikilinks between people, projects, concepts, diary entries, and sources
- aliases and resolver decisions that reduce duplicate pages
- search results that reveal nearby concepts
- lint findings that expose isolated or underspecified pages
- future optional typed edges once the Markdown corpus is large enough

At this stage, proximity is more important than ontology. The system should notice that concepts are moving closer before it claims to know the exact relationship between them.

## Snapshots, Not Permanent Dashboards

Health numbers should be treated as dated slices:

- source count
- entity count
- diary draft count
- pages missing source references
- stale Compiled Truth pages
- unresolved open questions
- lint warnings
- human review queue size

Every metric should carry a generation time and should be easy to regenerate from local files. No number should be treated as permanent truth.

## Negative Space

The system should explicitly preserve what it does not know:

- subjective meaning that only the user can provide
- claims without source references
- inferred low-confidence notes
- unresolved identity collisions
- private context that should not be committed or published
- questions that emerged from lint, search, or diary drafting

This negative space is part of the architecture. A good personal brain does not only remember; it also marks the boundary where agent inference must stop.

## Active Workspace Layer

The active workspace is the current-task shared whiteboard.

```text
raw sources
  -> canonical memory
  -> retrieval candidates
  -> active workspace
  -> specialist lens
  -> final deliverable
```

It is especially important for strategy reports, competitor analysis, roadmaps, investment-style judgment, and anything with a strict date boundary.

The workspace should expose:

- task frame
- `as_of` and source window
- candidate evidence
- active pinned context
- coverage matrix
- claim audit
- out-of-window evidence
- open questions
- output contract

It should not expose hidden chain-of-thought. The point is to show the high-level active context that the final answer is allowed to use.

Generated workspaces are ignored by git because they may contain private retrieved snippets. The reusable architecture lives in `docs/WORKSPACE.md`, `skills/active-workspace.md`, `skills/strategy-report.md`, and `brain/templates/workspace.md`.

## Page Model

```text
frontmatter

# Title

Compiled Truth
- current state
- assessment
- open threads
- links

---

Timeline
- append-only evidence
- dated source entries
```

This avoids mixing what the brain currently believes with the evidence trail that produced it.

## Why Not Start With a Database?

The MVP optimizes for inspectability and contribution speed. A database layer becomes useful once there are enough pages to require:

- chunk indexing
- identity resolution
- typed edges
- background jobs
- remote MCP access
- multi-user permissions

Until then, Markdown plus scripts is the most debuggable version of the system.
