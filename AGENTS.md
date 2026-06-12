# Agent Operating Protocol

Use this file when working on this repository.

## Startup Order

1. Read `llms.txt` for the compact repository map.
2. Read `SKILL.md` for the workflow contract.
3. Read `brain/RESOLVER.md` before creating or moving any brain page.
4. Read `brain/schema.md` before changing page shape.
5. Read `skills/RESOLVER.md` before choosing a task workflow.

## Brain-first Rules

1. Before creating or moving any brain page, read `brain/RESOLVER.md`.
2. Before changing page shape or required metadata, read `brain/schema.md`.
3. For workflow-specific work, read `skills/RESOLVER.md` and then the matching skill doc.
4. Raw source files under `brain/sources/` are append-only snapshots. Do not rewrite them unless the user explicitly asks.
5. `brain/ideas/` is user-authored by default. Agents may suggest edits, but should not overwrite raw ideas silently.
6. Any claim in Compiled Truth should have a source reference or be marked as a user-provided/inferred low-confidence note.

## Common Commands

```bash
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

## More Detail

- Human overview: `README.md`
- Architecture: `docs/ARCHITECTURE.md`
- User journey: `docs/USER_JOURNEY.md`
- Agent guide: `docs/AGENT_GUIDE.md`
