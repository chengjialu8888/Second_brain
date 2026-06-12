---
name: feishu-doc-ingestion
mutating: true
writes_pages: true
writes_to:
  - brain/sources/feishu-docs/
  - brain/concepts/
  - brain/projects/
  - brain/resources/
---

# Feishu Doc Ingestion

## Contract

Fetch Feishu docs and wikis through `lark-cli`, preserve snapshots, and extract durable concepts or project updates.

## Phases

1. Fetch outline first:

```bash
lark-cli docs +fetch --api-version v2 --doc "$URL" --scope outline --max-depth 3 --detail with-ids
```

2. Fetch selected sections:

```bash
lark-cli docs +fetch --api-version v2 --doc "$URL" --doc-format markdown --scope section --start-block-id "$BLOCK_ID"
```

3. Use `scripts/fetch_feishu_doc.sh "$URL"` for a simple whole-document snapshot.
4. Save snapshot under `brain/sources/feishu-docs/`.
5. Extract durable content into canonical pages.
6. Run lint.

## Anti-Patterns

- Do not blindly full-fetch huge docs when outline + sections are enough.
- Do not store methodology only as a resource if it should become a concept.
- Do not omit source URL or fetch date.
