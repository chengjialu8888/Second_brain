---
name: entity-enrichment
mutating: true
writes_pages: true
writes_to:
  - brain/people/
  - brain/places/
  - brain/concepts/
  - brain/projects/
---

# Entity Enrichment

## Contract

Update canonical entity pages without creating duplicates.

## Phases

1. Read `brain/RESOLVER.md` and `brain/schema.md`.
2. Search existing pages and aliases.
3. Decide create vs update.
4. Update Compiled Truth only with sourced or clearly marked claims.
5. Append Timeline entries with dates and sources.
6. Add open threads for missing context.

## Anti-Patterns

- Do not infer strong personality assessments from one data point.
- Do not create duplicate aliases as separate pages.
- Do not bury important current facts only in Timeline.
