<p align="center">
  <img src="assets/github-header2.png" alt="Second Brain: local-first personal memory for humans and agents" width="100%" />
</p>

<p align="center">
  <a href="SKILL.md"><img alt="Agent Skill" src="https://img.shields.io/badge/agent-skill--ready-0f766e?style=flat-square"></a>
  <a href="AGENTS.md"><img alt="Agent Docs" src="https://img.shields.io/badge/agents-AGENTS.md-2563eb?style=flat-square"></a>
  <a href="llms.txt"><img alt="LLM Index" src="https://img.shields.io/badge/llms.txt-ready-7c3aed?style=flat-square"></a>
  <img alt="Status" src="https://img.shields.io/badge/status-MVP-f59e0b?style=flat-square">
</p>

<p align="center">
  <a href="README.zh-CN.md">中文版 README</a>
</p>

# Second Brain

**Second Brain is a local-first personal memory layer for humans and agents.**

It turns chats, Feishu docs, calendar events, diary drafts, links, and notes into a Markdown-native brain that agents can compile, manage, search, synthesize, audit through active workspaces, and maintain over time.

The goal is not another knowledge base. The goal is a durable context layer that remembers what happened, what it means, what is still open, and what the agent should ask next.

## Latest Update: Recall-First Strategy Workspace

This version adds a J-space-inspired active workspace layer and a `strategy-report` skill for strategic work where accuracy, coverage, and date boundaries matter. The next architecture iteration is inspired by Shadow-Weave's [Holographic Memory System](https://github.com/Shadow-Weave/HMS): move from "retrieve chunks into context" to "actively recall, organize evidence, then write."

- **Active workspace before final output**: high-stakes synthesis now passes through `brain/workspace/`, a small task whiteboard that exposes the active evidence, assumptions, gaps, and output contract.
- **Date-bounded strategy reports**: `scripts/second_brain.sh strategy-report "topic" --from YYYY-MM-DD --to YYYY-MM-DD` creates a report-ready workspace with `as_of`, source window, coverage matrix, and claim audit.
- **Recall-first architecture**: future recall should start with a plan, then search by time, entity, current state, numeric signal, contradiction, and relationship instead of relying on one similarity search.
- **Evidence ledger before workspace**: retrieved material should be deduped, date-normalized, source-tagged, and marked as current, historical, planned, cancelled, or conflicting before it reaches the active workspace.
- **Context overload relief**: raw sources stay outside the prompt; the model sees a compact ledger and 5-12 active claims instead of a long pile of snippets.
- **Better factual discipline**: important claims are expected to carry source paths, dates, confidence, and caveats before they become recommendations.
- **Memory first, specialist second**: product, finance, risk, growth, or engineering lenses can shape the deliverable only after Second Brain evidence is visible.
- **Private by default**: generated workspace drafts are ignored by git because they may include sensitive retrieved context.

## Why It Exists

Most personal knowledge systems stop at storage or retrieval:

- note apps store pages
- RAG systems retrieve chunks
- generic assistants answer from the current chat

Second Brain adds the missing maintenance layer:

- raw sources stay preserved as evidence
- entities get canonical pages
- current understanding is separated from evidence history
- agents search first, then synthesize
- active workspaces make high-stakes synthesis auditable before final output
- recall planning and evidence ledgers reduce context overload before writing
- lint turns missing context into useful follow-up questions
- specialist output lenses turn the same memory into product, engineering, design, growth, sales, security, or testing deliverables

## How It Is Different

| Dimension | Pure Knowledge Base | Obsidian | RAG over notes | Second Brain |
|-|-|-|-|-|
| Primary job | Store information | Human PKM, backlinks, graph thinking | Retrieve chunks | Maintain personal context |
| Input handling | Save notes | Fast manual capture and linking | Chunk documents | Compile and manage memory from chats, docs, calendar, diary, links |
| Search method | Manual browsing | Local search, backlinks, graph, plugins | Similarity retrieval | Structured search with resolver, schema, entity pages, source refs |
| Context overload handling | Human judgment | Human curation, backlinks, canvases | Push more chunks into the prompt | Recall plan -> evidence ledger -> active workspace |
| Current task reasoning | Ad hoc | Human-maintained working notes | Hidden in prompt/session | Active workspace with date window, coverage matrix, and claim audit |
| Output shape | Generic notes | Human-authored notes and canvases | Generic answer | Role-shaped deliverables through specialist agent lenses |
| Human-readable middle layer | Yes | Excellent Markdown vault and UI | Usually no | Yes, Markdown pages |
| Agent-readable structure | Weak | Files are readable, but rules are optional | Retrieval-only | Resolver, schema, skills, evals |
| Evidence model | Informal | Backlinks and manual citations | Chunk provenance | Raw sources + Timeline |
| Current understanding | Mixed into notes | Maintained by human editing | Recomputed per query | Compiled Truth |
| Proactive maintenance | Manual | Manual review or plugins | Rare | `wiki_lint` + open questions |
| Best use | Archiving | Human sense-making and personal note exploration | Search | Remembering yourself over time with agent help |

Obsidian is still a great interface for browsing the vault. Second Brain is the agent operating layer that makes the same Markdown memory governed, searchable, maintainable, and output-ready.

## Core Strengths

Second Brain works across the full context lifecycle:

1. **Input: memory compilation and management**
   Raw group chats, Feishu docs, calendar events, diary drafts, links, and notes are preserved as source evidence, then compiled into canonical people, project, concept, diary, and resource pages.

2. **Recall: structured retrieval before synthesis**
   Agents should first decide what kind of memory is needed, then search by time, entity, state, number, conflict, and relationship. The goal is not more context; it is a smaller, better-organized evidence set.

3. **Organize: evidence ledger before workspace**
   High-risk recall should produce a ledger with event time, mention time, source, fact type, compact evidence, numeric/date/update signals, and raw source refs. This prevents duplicate counting, stale-state confusion, and relative-date mistakes.

4. **Think: active workspace for high-stakes synthesis**
   For strategy reports, competitor analysis, roadmaps, and other date-bounded work, agents compose a small workspace that exposes the active evidence, assumptions, coverage gaps, and claim audit before writing.

5. **Output: role-shaped delivery**
   When the answer needs professional craft, the Agency Agents layer applies the right specialist lens: Product Manager for PRDs, Feishu Integration Developer for Lark workflows, UX Researcher for user insight, Security Architect for risk review, Test Planner for QA, and so on.

## Core Idea

Each canonical entity page has two layers:

```text
Compiled Truth       current synthesis, rewritten as understanding improves
---
Timeline             append-only evidence with dates and sources
```

This lets the brain answer two different questions cleanly:

- "What do we currently think about this person/project/concept?"
- "What happened, when, and where did that claim come from?"

## Quick Start: Skill-style Entry

```bash
git clone https://github.com/chengjialu8888/Second_brain.git
cd Second_brain

# See the skill-style command surface
scripts/second_brain.sh help
```

Use it like an agent skill from the terminal:

```bash
# Search local memory
scripts/second_brain.sh search "llm-wiki"

# Compose an active workspace before high-stakes synthesis
scripts/second_brain.sh workspace "Coze competitor strategy" --from 2026-07-01 --to 2026-07-14

# Start a date-bounded strategy report workflow
scripts/second_brain.sh strategy-report "Coze competitor strategy" --from 2026-07-01 --to 2026-07-14

# Lint the brain structure
scripts/second_brain.sh lint

# Generate a diary draft from Feishu calendar
scripts/second_brain.sh diary 2026-06-12

# Show the agent startup prompt
scripts/second_brain.sh prompt
```

For the calendar diary workflow, authorize the minimal Feishu scope first:

```bash
lark-cli auth login --scope "calendar:calendar.event:read"
```

Then run:

```bash
scripts/second_brain.sh diary today
```

The generated diary remains `status: draft` until you add subjective context. Calendar knows what happened; only you know what it meant.

### Agent Prompt Entry

If you are using Codex, Claude Code, Cursor, or another coding agent, start with:

```text
Use this repository as the $second-brain skill.
Read AGENTS.md, SKILL.md, brain/RESOLVER.md, brain/schema.md, and skills/RESOLVER.md.
When output needs a specialist lens, also read skills/agency-agent-routing.md and use agents/agency-agents/ after searching Second Brain evidence.
For accurate, comprehensive, date-bounded synthesis, create an active workspace before the final deliverable.
Then help me capture, ingest, search, think, compose workspaces, lint, route specialist agents, or generate diary drafts without committing private source data.
```

## User Journey

<p align="center">
  <img src="assets/user-journey.svg" alt="Second Brain bilingual user journey from capture to recall-first output" width="100%">
</p>

## Core Architecture

<p align="center">
  <img src="assets/product-flow.svg" alt="Second Brain bilingual recall-first core architecture" width="100%">
</p>

The architecture can also be read as an operational anatomy: `brain/` is the body, `brain/sources/` is the evidence layer, Compiled Truth and Timeline form the memory model, recall planning chooses the right retrieval route, the evidence ledger keeps recalled facts compact and auditable, `brain/workspace/` is the active task whiteboard, `skills/` are repeatable workflows, and `wiki_lint` is the immune system. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/WORKSPACE.md](docs/WORKSPACE.md) for the filter/fissure model and the J-space-inspired workspace layer.

## Specialist Agent Layer

Second Brain now includes an optional [Agency Agents](agents/agency-agents/README.md) layer: 233 specialist prompts from [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents/tree/main), installed as local source files plus a searchable roster.

The rule is simple: **memory first, specialist lens second**. For source-backed product plans, architecture reviews, design critique, growth strategy, security review, testing plans, and similar deliverables, agents should search/read Second Brain first, then choose a relevant specialist:

```bash
scripts/second_brain.sh agents "product strategy"
scripts/second_brain.sh agents "Feishu integration"
scripts/second_brain.sh agents "security review"
```

See [skills/agency-agent-routing.md](skills/agency-agent-routing.md) for the workflow contract.

## Repository Map

```text
.
├── SKILL.md                     # Agent-facing workflow entrypoint
├── AGENTS.md                    # Operating rules for Codex, Claude Code, Cursor, etc.
├── llms.txt                     # Compact map for LLM crawlers and agent fetchers
├── brain/
│   ├── RESOLVER.md              # Filing and ownership rules
│   ├── schema.md                # Page templates and evidence discipline
│   ├── index.md                 # Default human/agent entrypoint
│   ├── dashboards/              # Obsidian-friendly human review cockpit
│   ├── workspace/               # Task-scoped active workspace entry and private generated drafts
│   ├── templates/               # Obsidian-ready page templates
│   ├── people/ concepts/ projects/ diary/
│   └── sources/                 # Immutable source snapshots
├── skills/                      # Workflow docs: ingest, query, enrich, lint, diary
├── agents/agency-agents/        # Optional specialist agent layer and roster
├── scripts/                     # Deterministic local utilities
├── evals/                       # Seed eval cases for routing, filing, query, lint
└── docs/                        # Human and agent-facing docs
```

## What Works Today

- Local Markdown brain skeleton
- Skill-style CLI wrapper: `scripts/second_brain.sh`
- Resolver and schema discipline
- Seed concept/project pages
- Feishu calendar to diary draft
- Feishu doc snapshot helper
- Link extraction
- Local search
- Active workspace composer for date-bounded synthesis
- Strategy report workflow with coverage matrix and claim audit
- Structural lint
- Seed eval cases
- Agency Agents specialist routing
- Obsidian-ready dashboards, templates, graph colors, and CSS snippet
- Agent crawler map via `llms.txt`

## What Is Next

- Better chat and Feishu doc ingestion
- Entity alias and duplicate detection
- `memory-recall` / `evidence-ledger` skill for recall plans, multi-route retrieval, dedupe, date normalization, and current-vs-historical state arbitration
- Richer `think` synthesis over search results
- Weekly lint report
- Optional SQLite FTS5 index
- Optional Dataview-backed dashboard automation
- Optional MCP layer for remote agents

## For Humans

Open this repository as an Obsidian vault if you want backlinks, graph view, templates, and manual review dashboards.

Recommended first places:

- `brain/dashboards/home.md`
- `docs/OBSIDIAN.md`
- `brain/index.md`
- `brain/RESOLVER.md`
- `brain/schema.md`
- `brain/projects/second-brain.md`

## For Agents

Start here:

1. `llms.txt`
2. `AGENTS.md`
3. `SKILL.md`
4. `brain/RESOLVER.md`
5. `brain/schema.md`
6. `skills/RESOLVER.md`
7. `skills/agency-agent-routing.md` when a specialist output lens is useful

Rule of thumb: **search first, then think; preserve evidence, then synthesize.**

## Contributing

This is an early MVP. Useful contributions include:

- better source ingestion workflows
- stricter lint checks
- safer diary and calendar handling
- Obsidian-friendly templates
- agent eval cases
- docs and examples

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Project Status

MVP. The current version is intentionally local-first and small. It is designed to validate the memory workflow before adding heavier infrastructure like vector search, graph storage, background jobs, or MCP.
