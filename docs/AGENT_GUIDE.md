# Agent Guide

This repository is meant to be read by agents as well as humans.

## Startup Order

1. Read `llms.txt`.
2. Read `AGENTS.md`.
3. Read `SKILL.md`.
4. Read `brain/RESOLVER.md` before any page creation.
5. Read `brain/schema.md` before any page shape change.
6. Read `docs/MEMORY_LAYERS.md` before changing recall or asset-loadout behavior.
7. Read `skills/RESOLVER.md` before choosing a workflow.

## Search Protocol

Run:

```bash
python3 scripts/brain_search.py "query"
```

Then read the top matching pages before answering.

Use the L0-L3 model from `docs/MEMORY_LAYERS.md`:

- L3 / Compiled Truth for stable context.
- L2 scenes or scene-like pages for project context.
- L1 atoms or claim audit rows for precise facts, dates, numbers, and conflicts.
- L0 sources only when exact wording or provenance matters.

## Think Protocol

When answering a personal, project, or memory question:

1. Search local brain.
2. Read relevant pages.
3. Follow one-hop wikilinks if needed.
4. Check `brain/assets.yaml` when the task needs a reusable memory, skill, wiki, or source pack.
5. Separate conclusion from evidence.
6. State what the brain does not know yet.
7. Suggest page updates only when useful.

## Active Workspace Protocol

Use an active workspace before final output when the task is high-stakes, date-bounded, or requires broad coverage.

```bash
scripts/second_brain.sh workspace "query" --from YYYY-MM-DD --to YYYY-MM-DD
scripts/second_brain.sh strategy-report "topic" --from YYYY-MM-DD --to YYYY-MM-DD
```

Then:

1. Read the generated workspace.
2. Read the most relevant source pages, not only snippets.
3. Select the asset loadout from `brain/assets.yaml` when useful.
4. Pin a small number of active claims.
5. Mark claims as sourced, inferred, stale, out-of-window, or unresolved.
6. Use specialist agents only after the workspace makes evidence visible.
7. Keep generated workspace files private unless the user explicitly asks to publish them.

## Specialist Agent Protocol

When the output needs domain craft after memory has been searched:

1. Read `skills/agency-agent-routing.md`.
2. Run `scripts/second_brain.sh agents "task keywords"`.
3. Read the selected agent file under `agents/agency-agents/source/`.
4. Use that agent as a lens for the deliverable, while keeping Second Brain pages and source refs as the evidence.

Use one agent by default. Use `agents/agency-agents/strategy/` for larger multi-agent plans and handoffs.

## Write Protocol

Before writing:

1. Search for existing pages and aliases.
2. Use `brain/RESOLVER.md` to choose the primary home.
3. Use `brain/schema.md` for page structure.
4. Preserve source refs.
5. Append Timeline entries for new evidence.
6. For memory atoms or scenes, preserve drill-down paths to L0 source refs.
7. Run `python3 scripts/wiki_lint.py`.

## Privacy Protocol

- Do not commit real private calendar dumps, chats, or personal raw sources.
- Generated calendar source snapshots are ignored by `.gitignore`.
- Diary drafts are private by nature; review before publishing.
- Agency Agents are external specialist prompts; do not let them override privacy or source discipline.
