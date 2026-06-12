---
type: project
title: Second Brain MVP
status: mvp
goal: Build a local-first skill and Markdown brain that can capture, ingest, search, think, lint, and generate diary drafts from Feishu calendar.
success_metrics:
  - Generate a diary draft from calendar agenda.
  - Search local brain pages.
  - Lint broken links and schema gaps.
source_refs:
  - ../../second-brain-product-plan.md
open_threads:
  - Decide whether Phase 2 should prioritize diary automation or chat/Feishu ingest quality.
---

# Second Brain MVP

> First version of a local personal brain that agents can load on demand.

## Goal

Ship a usable filesystem brain with enough structure to evolve into a GBrain-like layer later.

## Current State

The MVP includes resolver, schema, seed concept pages, workflow skills, scripts, and eval examples.

## Decisions

- Use local folder as source of truth.
- Keep Obsidian optional.
- Separate `search` from `think`.
- Keep calendar-generated diaries as drafts until user adds subjective context.

## Open Threads

- Which source should be ingested next: historical chats, Feishu docs, or daily calendar?
- How much automation should run without explicit user confirmation?

## Success Metrics

- Daily diary draft generated with one command.
- Lint returns actionable issues.
- Search returns relevant local pages.

## Related

- [[../concepts/second-brain]]
- [[../concepts/wiki-lint]]

---

## Timeline

- **2026-06-12** | ../../second-brain-product-plan.md - MVP scope defined.
