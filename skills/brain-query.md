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
3. Run `python3 scripts/brain_search.py "query"`.
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
- Do not treat `brain/assets.yaml` as evidence.
- Do not read L0 raw sources when L1/L2 context is sufficient.
