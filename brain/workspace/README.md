---
type: dashboard
title: Active Workspace
aliases:
  - Workspace
  - Current Task Whiteboard
updated: 2026-07-14
confidence: medium
---

# Active Workspace

> A task-scoped working surface for agents. It is not long-term memory and should not be treated as canonical truth.

## Purpose

Use this folder when a task needs accurate, date-bounded, source-backed synthesis before a final deliverable.

The workspace sits between retrieval and output:

```text
raw sources -> canonical memory -> retrieval candidates -> active workspace -> specialist output
```

## Rules

- Keep workspace contents small enough to inspect.
- Pin only the evidence, assumptions, constraints, and open questions needed for the current task.
- Preserve date boundaries: `as_of`, `source_window.start`, and `source_window.end`.
- Mark every important claim as sourced, inferred, or unresolved.
- Use workspace pages to broadcast context across specialist lenses; do not let them replace source pages.
- Move durable confirmed facts into canonical entity pages later.

## Generated Files

`scripts/workspace_compose.py` writes local task workspaces such as:

- `brain/workspace/current.md`
- `brain/workspace/sessions/YYYY-MM-DD-topic.md`

`skills/multi-agent-sandbox/scripts/sandbox.py` writes bounded scenario runs under:

- `brain/workspace/simulations/<run-id>/`

These files may contain private retrieved context, so they are ignored by git by default.

## Commands

```bash
scripts/second_brain.sh workspace "query" --from 2026-07-01 --to 2026-07-14
scripts/second_brain.sh strategy-report "Coze competitor strategy" --from 2026-07-01 --to 2026-07-14
scripts/second_brain.sh sandbox init --title "Launch stress test" --question "How might stakeholders react?" --horizon "90 days" --wiki-query "project customer competitor"
```

---

## Timeline

- **2026-07-14** | System - Added a J-space-inspired active workspace layer for task-scoped synthesis.
- **2026-08-06** | System - Added private, evidence-grounded multi-Agent sandbox workspaces with append-only synthetic events.
