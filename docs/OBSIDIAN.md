# Obsidian Setup

Second Brain is still filesystem-first. Obsidian is the recommended human interface for browsing, reviewing, and lightly editing the Markdown vault.

## Open The Vault

Open this repository root as the vault, not only `brain/`. That lets Obsidian see `README.md`, `docs/`, `brain/`, and the `.obsidian/` configuration.

Recommended first page:

- `brain/dashboards/home.md`

## What This Adds

- `brain/dashboards/home.md`: human review cockpit
- `brain/dashboards/open-questions.md`: missing context worth answering
- `brain/dashboards/review-queue.md`: claims needing human confirmation
- `brain/dashboards/recent-changes.md`: dated change feed
- `brain/workspace/README.md`: task-scoped active workspace entry
- `brain/templates/`: Obsidian template files for people, projects, concepts, diary entries, source notes, and structured meeting summaries
- `.obsidian/snippets/second-brain.css`: subtle reading polish for headings, tables, quotes, and task lists
- `.obsidian/graph.json`: graph color groups for people, projects, concepts, dashboards, and sources

## Human Review Loop

1. Open `brain/dashboards/home.md`.
2. Read `recent-changes` for what changed.
3. Confirm or reject items in `review-queue`.
4. Answer one useful item in `open-questions`.
5. Move confirmed insight into the relevant canonical page.
6. Keep raw evidence in `brain/sources/`.

For strategy reports or other date-bounded synthesis, open `brain/workspace/current.md` after running the workspace command. Treat it as a temporary whiteboard, not as a permanent note.

## Agent Maintenance Rules

Agents should update dashboards after large source ingests, diary generation, entity enrichment, or specialist-agent deliverables.

- Add missing human context to `open-questions`.
- Add uncertain agent claims to `review-queue`.
- Add meaningful page/source/output changes to `recent-changes`.
- Keep dashboards short. They are navigation surfaces, not source archives.

## Optional Plugins

No plugin is required. These are useful if the user wants a richer UI:

- Templates: use `brain/templates/`
- Backlinks and outgoing links: inspect entity connections
- Graph view: use the included graph color groups
- Dataview: optional future dashboard automation

Do not make any plugin mandatory for agent workflows. Markdown remains the source of truth.
