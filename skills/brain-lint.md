---
name: brain-lint
mutating: false
writes_pages: false
---

# Brain Lint

## Contract

Find structural and evidence-quality problems. Do not silently rewrite semantic content.

## Checks

- Missing frontmatter.
- Missing `---` divider.
- Missing `## Timeline`.
- Broken wikilinks.
- Duplicate titles.
- Empty source refs.
- Diary drafts waiting for user context.

## Command

```bash
python3 scripts/wiki_lint.py
```

## Output Format

- Error: must fix.
- Warning: should review.
- Open question: ask user.

## Anti-Patterns

- Do not auto-fix subjective meaning.
- Do not delete pages during lint.
