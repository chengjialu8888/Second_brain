# Active Workspace

Second Brain now includes a task-scoped active workspace layer inspired by Anthropic's July 6, 2026 Global Workspace / J-space research:

- Anthropic research post: https://www.anthropic.com/research/global-workspace
- Full Transformer Circuits paper: https://transformer-circuits.pub/2026/workspace/index.html

This project does not claim to reproduce model internals. It borrows the operational lesson: flexible reasoning benefits from a small, inspectable, controllable shared space between raw computation and final output.

## Why Add This Layer

Long-term memory and active reasoning have different jobs.

```text
brain/sources/          raw evidence
brain/* entity pages    durable memory
search results          candidates
active workspace        current task context
specialist agents       output craft
final deliverable       user-facing answer/report
```

The active workspace prevents a common failure mode: retrieval returns many plausible snippets, then the final answer silently mixes old evidence, current assumptions, and unsupported judgment.

## J-space-Inspired Properties

| Research property | Second Brain implementation |
|-|-|
| Reportable | Workspace pages expose the current active context, assumptions, and gaps. |
| Controllable | The user or agent can pin, remove, or mark evidence out-of-window. |
| Used for reasoning | Final deliverables should cite workspace claims and source paths. |
| Broadcast across tasks | Product, strategy, engineering, finance, or risk lenses read the same workspace. |
| Capacity-limited | Workspaces should hold a small number of pinned claims, not every retrieved snippet. |
| Selective | Automatic lookup can skip the workspace; high-stakes synthesis should use it. |

## When To Use It

Use `active-workspace` for:

- strategy reports
- competitor analysis
- roadmap or PRD synthesis
- investment or business judgment
- cross-source contradiction handling
- any deliverable with a strict date window

Skip it for:

- quick lookup
- raw capture
- simple lint
- one-file mechanical edits

## Date-Bounded Report Discipline

Every strategic workspace should make time explicit:

- `as_of`: the date of the judgment
- `source_window.start`: earliest allowed source date
- `source_window.end`: latest allowed source date
- `captured_at`: when a source entered the brain, if known
- `event_date` or `published_at`: when the source claim originally happened

If a source is useful but outside the window, keep it in `Excluded / Out Of Window` and do not use it as a primary claim.

## Strategy Report Flow

```text
1. Define topic, audience, and date window.
2. Search local Second Brain evidence.
3. Compose an active workspace with candidate evidence.
4. Fill the coverage matrix.
5. Audit major claims for source, date, and confidence.
6. Route specialist lenses only after evidence is visible.
7. Produce the report with citations, caveats, and gaps.
```

Use:

```bash
scripts/second_brain.sh strategy-report "Coze competitor strategy" --from 2026-07-01 --to 2026-07-14
```

The command creates a workspace draft. It does not claim the report is complete.

## Privacy

Generated workspaces may include private source snippets, so `brain/workspace/current.md` and `brain/workspace/sessions/*.md` are ignored by git. Commit durable rules and templates; review task workspaces before sharing.
