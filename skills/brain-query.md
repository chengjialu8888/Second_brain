---
name: brain-query
mutating: false
writes_pages: false
---

# Brain Query

## Contract

Search finds evidence. Think synthesizes evidence.

## Phases

1. Read `brain/index.md`.
2. Read `docs/MEMORY_LAYERS.md` if recall depth or asset loadout matters.
3. Inspect `scripts/second_brain.sh catalog --query "topic"`, then run `python3 scripts/brain_search.py "query"` for full-text recall with summary output. Use `--view snippets` when needed; `--include-sources` explicitly includes L0. Keep fallback queries for missing topic branches.
4. Read the top relevant pages.
5. Follow one-hop wikilinks when useful.
6. Use `brain/assets.yaml` when the task needs reusable memory, skill, wiki, or source-pack context.
7. Answer with conclusion, sources, confidence, and gaps.

## Output Format

```text
Conclusion:

Sources:
- path: reason

Confidence:

What the brain does not know yet:

Suggested updates:
```

## Anti-Patterns

- Do not answer personal history questions from model memory alone.
- Do not cite a page you did not read.
- Do not hide uncertainty.
- Inspect verification and freshness separately; a summary or a high keyword score is not validated evidence.
- Do not treat `brain/assets.yaml` as evidence.
- Do not read L0 raw sources when L1/L2 context is sufficient.
