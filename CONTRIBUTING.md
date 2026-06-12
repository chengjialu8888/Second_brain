# Contributing to Second Brain

Thanks for helping make local-first personal memory better.

## Good First Contributions

- Improve docs or examples.
- Add eval cases under `evals/`.
- Add safer lint checks in `scripts/wiki_lint.py`.
- Improve diary draft generation without leaking private calendar data.
- Improve Obsidian-friendly templates.
- Add source ingestion workflows for common exports.

## Development Setup

```bash
git clone https://github.com/chengjialu8888/Second_brain.git
cd Second_brain
```

There are no required runtime dependencies beyond Bash and Python 3 for the current MVP.

## Validation

Run:

```bash
bash -n scripts/*.sh
python3 -c "import ast, pathlib; [ast.parse(p.read_text()) for p in pathlib.Path('scripts').glob('*.py')]; print('python ast ok')"
python3 scripts/wiki_lint.py
python3 scripts/brain_search.py "second brain"
```

## Pull Requests

Please include:

- what changed
- why it matters
- how you validated it
- whether the change touches private-memory handling

## Privacy

Do not commit private calendar data, chat exports, API keys, access tokens, or personal raw sources. Keep examples synthetic.

## Style

- Keep core docs readable by both humans and agents.
- Prefer small deterministic scripts over large hidden workflows.
- Preserve the distinction between raw evidence and synthesized memory.
