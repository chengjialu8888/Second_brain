# Skill Resolver

Read this before choosing a workflow.

| User Intent | Skill Doc |
|-|-|
| "capture this", "remember this", quick thought | `capture` in `../SKILL.md` |
| Ingest chat export | `chat-ingestion.md` |
| Ingest Feishu doc or wiki | `feishu-doc-ingestion.md` |
| Ask a question about memory | `brain-query.md` |
| Produce a source-backed deliverable needing product, engineering, design, growth, sales, security, testing, finance, or other specialist framing | `agency-agent-routing.md` after `brain-query.md` |
| Create/update people, concepts, projects | `entity-enrichment.md` |
| Generate diary from Feishu calendar | `calendar-diary-draft.md` |
| Check broken links, missing fields, stale pages | `brain-lint.md` |

When multiple skills match, prefer the most specific source skill first, then call enrichment/lint after source ingestion. Use Agency Agent Routing only after the relevant Second Brain evidence has been searched and read.
