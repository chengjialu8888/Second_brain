---
name: chat-ingestion
mutating: true
writes_pages: true
writes_to:
  - brain/sources/chats/
  - brain/people/
  - brain/concepts/
  - brain/projects/
  - brain/resources/
---

# Chat Ingestion

## Contract

Preserve the source chat, then extract durable entities, claims, resources, decisions, and open questions.

## Phases

1. Save the raw chat under `brain/sources/chats/`.
2. Extract links with `scripts/extract_links.sh`.
3. Read `brain/RESOLVER.md`.
4. Sample several messages before bulk extraction.
5. Create/update pages with source refs and Timeline entries.
6. Update `brain/index.md` and `brain/log.md`.
7. Run `python3 scripts/wiki_lint.py`.

## Output Format

- Source snapshot path.
- Pages created.
- Pages updated.
- Open questions.
- Lint summary.

## Anti-Patterns

- Do not create person pages for unsupported one-off names.
- Do not lose aliases or relationship clues.
- Do not summarize away source links.
