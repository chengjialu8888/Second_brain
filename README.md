# Second Brain

Local-first personal memory for humans and agents.

Second Brain stores memory as plain Markdown files, keeps raw sources immutable, and gives agents a disciplined way to capture, ingest, search, think, lint, and draft daily notes. Obsidian can open `brain/` as a vault, but the filesystem is the source of truth.

## What Is Included

- `SKILL.md`: agent-facing workflow entrypoint.
- `AGENTS.md`: operating rules for Codex, Claude Code, and other coding agents.
- `brain/`: local Markdown brain with resolver, schema, index, logs, entities, sources, and diary drafts.
- `skills/`: task-specific workflow docs for ingestion, query, enrichment, lint, and calendar diary drafting.
- `scripts/`: small deterministic tools for link extraction, Feishu doc snapshots, calendar diary drafts, search, and lint.
- `evals/`: seed examples for routing, filing, query, and lint checks.
- `second-brain-product-plan.md`: v0.2 product plan.

## Quick Start

```bash
# Search local memory
python3 scripts/brain_search.py "llm-wiki"

# Lint the brain structure
python3 scripts/wiki_lint.py

# Extract links from a source file
scripts/extract_links.sh /path/to/chat.md

# Fetch a Feishu doc or wiki snapshot
scripts/fetch_feishu_doc.sh "https://example.feishu.cn/docx/..." 

# Generate today's diary draft from Feishu calendar
scripts/calendar_diary_draft.sh 2026-06-12
```

For the calendar flow, the minimal Feishu scope is:

```bash
lark-cli auth login --scope "calendar:calendar.event:read"
```

## Daily Diary Flow

```text
Feishu calendar
  -> brain/sources/calendar/YYYY-MM-DD.json
  -> brain/sources/calendar/YYYY-MM-DD.txt
  -> brain/diary/YYYY-MM-DD.md
  -> user adds subjective notes
  -> brain lint/enrichment updates people, projects, places, and open threads
```

The generated diary remains `status: draft` until the user adds personal context. Calendar knows what happened; the user supplies what it meant.

## Storage Principle

Use a local folder as the source of truth:

```text
File-system first, Obsidian-friendly, Agent-maintained.
```

Obsidian is a human interface for backlinks, graph view, and review. Agents should read and write the Markdown files directly through the resolver and schema rules.
