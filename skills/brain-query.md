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
2. Run `python3 scripts/brain_search.py "query"`.
3. Read the top relevant pages.
4. Follow one-hop wikilinks when useful.
5. Answer with conclusion, sources, confidence, and gaps.

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
