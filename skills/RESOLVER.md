# Skill Resolver

Read this before choosing a workflow.

| User Intent | Skill Doc |
|-|-|
| "capture this", "remember this", quick thought | `capture` in `../SKILL.md` |
| Ingest chat export | `chat-ingestion.md` |
| Ingest Feishu doc or wiki | `feishu-doc-ingestion.md` |
| Ask a question about memory | `brain-query.md` |
| Compose a task-scoped whiteboard before synthesis | `active-workspace.md` |
| Write an accurate, comprehensive, date-bounded strategy report | `strategy-report.md` after `active-workspace.md` |
| Predict/rehearse future scenarios from Wiki context; run a multi-Agent sandbox, war game, tabletop exercise, or future rehearsal | `multi-agent-sandbox/SKILL.md` after `brain-query.md` and, when high-stakes, `active-workspace.md` |
| Produce a source-backed deliverable needing product, engineering, design, growth, sales, security, testing, finance, or other specialist framing | `agency-agent-routing.md` after `brain-query.md` |
| Create/update people, concepts, projects | `entity-enrichment.md` |
| Generate diary from Feishu calendar | `calendar-diary-draft.md` |
| Check broken links, missing fields, stale pages | `brain-lint.md` |

When multiple skills match, prefer the most specific source skill first, then call enrichment/lint after source ingestion. Use Active Workspace before high-stakes synthesis with strict date boundaries. Multi-Agent Sandbox runs stay inside `brain/workspace/simulations/` and never become canonical evidence. Use Agency Agent Routing only after the relevant Second Brain evidence has been searched/read and, when needed, placed into a workspace.

For tasks that change recall behavior, evidence-ledger shape, atom/scene extraction, or asset loadout, read `../docs/MEMORY_LAYERS.md` before choosing the final workflow.
