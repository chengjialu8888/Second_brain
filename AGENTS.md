# Agent Operating Protocol

Use this file when working on this repository.

## Startup Order

1. Read `llms.txt` for the compact repository map.
2. Read `SKILL.md` for the workflow contract.
3. Read `brain/RESOLVER.md` before creating or moving any brain page.
4. Read `brain/schema.md` before changing page shape.
5. Read `skills/RESOLVER.md` before choosing a task workflow.
6. If the output needs specialist craft, read `skills/agency-agent-routing.md` after the relevant Second Brain evidence has been searched/read.

## Brain-first Rules

1. Before creating or moving any brain page, read `brain/RESOLVER.md`.
2. Before changing page shape or required metadata, read `brain/schema.md`.
3. For workflow-specific work, read `skills/RESOLVER.md` and then the matching skill doc.
4. Raw source files under `brain/sources/` are append-only snapshots. Do not rewrite them unless the user explicitly asks.
5. `brain/ideas/` is user-authored by default. Agents may suggest edits, but should not overwrite raw ideas silently.
6. Any claim in Compiled Truth should have a source reference or be marked as a user-provided/inferred low-confidence note.
7. Agency Agents under `agents/agency-agents/` are specialist lenses, not memory. They may shape outputs only after Second Brain evidence is read.
8. Use `brain/dashboards/` as human-facing review surfaces. Do not put canonical facts only in dashboards; move confirmed facts into entity pages.

## Common Commands

```bash
scripts/second_brain.sh help
scripts/second_brain.sh prompt
scripts/second_brain.sh search "query"
scripts/second_brain.sh agents "product strategy"
scripts/second_brain.sh dashboard
scripts/second_brain.sh lint
scripts/second_brain.sh diary 2026-06-12
python3 scripts/brain_search.py "query"
python3 scripts/wiki_lint.py
scripts/calendar_diary_draft.sh 2026-06-12
scripts/extract_links.sh file.md
scripts/fetch_feishu_doc.sh "https://..."
```

## Before Publishing

Run:

```bash
python3 scripts/wiki_lint.py
python3 scripts/brain_search.py "second brain"
```

If scripts change, also run shell syntax checks:

```bash
bash -n scripts/*.sh
python3 -c "import ast, pathlib; [ast.parse(p.read_text()) for p in pathlib.Path('scripts').glob('*.py')]; print('python ast ok')"
```

## Dashboard Maintenance

After large ingests, diary generation, entity enrichment, or specialist-agent outputs:

1. Update `brain/dashboards/recent-changes.md` with a dated summary.
2. Add uncertain claims to `brain/dashboards/review-queue.md`.
3. Add missing human context to `brain/dashboards/open-questions.md`.
4. Keep dashboards short and link to canonical pages.

## More Detail

- Human overview: `README.md`
- Chinese overview: `README.zh-CN.md`
- Architecture: `docs/ARCHITECTURE.md`
- Obsidian setup: `docs/OBSIDIAN.md`
- User journey: `docs/USER_JOURNEY.md`
- Agent guide: `docs/AGENT_GUIDE.md`
