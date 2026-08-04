---
name: active-workspace
mutating: true
writes_pages: true
---

# Active Workspace

Use this workflow when a task needs a visible, date-aware working context between search and final output.

## Contract

The workspace is a temporary shared whiteboard, not canonical memory.

It should contain:

- the task frame
- the date boundary
- the selected asset loadout, if any
- candidate evidence
- pinned active context
- assumptions
- coverage gaps
- claim audit
- output contract

It should not contain:

- hidden chain-of-thought
- unsupported facts stated as truth
- private raw dumps intended for commit
- durable facts that never get moved into entity pages

## Command

```bash
scripts/second_brain.sh workspace "query" --from YYYY-MM-DD --to YYYY-MM-DD
```

Useful options:

```bash
scripts/second_brain.sh workspace "query" --title "Workspace title" --limit 12 --output brain/workspace/sessions/YYYY-MM-DD-topic.md
```

## Required Order

1. Read `brain/RESOLVER.md`, `brain/schema.md`, `docs/MEMORY_LAYERS.md`, and this file.
2. Define the task and date window.
3. Check `brain/assets.yaml` for relevant memory, skill, wiki, source-pack, or future codegraph assets.
4. Run the workspace command.
5. Read the generated workspace and the most relevant source pages.
6. Pin only the claims needed for the current task.
7. Mark out-of-window, stale, inferred, or low-confidence items.
8. If a specialist output lens is useful, follow `skills/agency-agent-routing.md`.
9. Move durable confirmed facts into canonical pages later.

## Capacity Rules

- Prefer 5-12 active claims.
- Prefer 3-8 open questions.
- Keep one task per workspace.
- If the workspace grows too large, split by decision or report section.

## Final Answer Discipline

The final answer should state:

- date window
- sources used
- confidence
- gaps
- what was excluded due to time window or weak evidence

## Anti-Patterns

- Do not treat search results as the workspace.
- Do not treat workspace claims as canonical until they are moved into entity pages.
- Do not treat asset-loadout metadata as evidence.
- Do not use old sources in a date-bounded report without marking freshness risk.
- Do not route to specialist agents before evidence is visible.
