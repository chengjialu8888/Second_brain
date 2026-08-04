# Brain Resolver

Read this before creating or moving any page in `brain/`.

## Filing Rule

File by primary subject, not by source format or the skill currently running.

If a note is about a person, it belongs in `people/` even if it came from a meeting, diary, or chat log. If a note is about a project being built, it belongs in `projects/`. If nothing fits, put it in `inbox/` and flag the schema gap.

## Directory Ownership

| Directory | Owner Skill | What Belongs Here | What Does Not |
|-|-|-|-|
| `people/` | `entity-enrichment` | Humans with relationship, interaction, or clear future value | Random names with no identifying context |
| `places/` | `entity-enrichment` | Cities, venues, restaurants, recurring locations | Companies or projects |
| `concepts/` | `entity-enrichment` | Mental models, frameworks, terms you could teach | Buildable ideas or active projects |
| `projects/` | `entity-enrichment` | Things being actively built or planned with goals | Raw possibilities with no action |
| `ideas/` | user-owned | User-originated raw ideas and possibilities | Agent-generated conclusions |
| `diary/` | `calendar-diary-draft` | Daily entries and subjective reflection | Raw calendar dumps |
| `dashboards/` | `brain-lint` / agents | Human review surfaces, open questions, recent changes, review queues | Canonical facts or raw sources |
| `memory/` | `brain-query` / `active-workspace` | Future L1 atomic memories and L2 scene memories with source refs | Raw source archives or final deliverables |
| `workspace/` | `active-workspace` / `strategy-report` | Task-scoped synthesis surfaces, date windows, evidence candidates, claim audits | Canonical facts, raw dumps, permanent source archives |
| `templates/` | humans / agents | Obsidian-ready page templates | Filled-in memory pages |
| `resources/` | `chat-ingestion` | Links, papers, repos, documents as resources | Distilled concepts from those resources |
| `sources/` | source skills | Immutable source snapshots | Curated entity pages |
| `inbox/` | `capture` | Temporary captures and unclassified material | Long-term canonical entities |

`brain/assets.yaml` is the lightweight asset-loadout registry. It is not an evidence page and should not contain private raw content. Use it to say which memory, skill, wiki, source-pack, or future codegraph assets are available to which workflows or agent roles.

## Disambiguation

- Concept vs idea: if you could teach it as a framework, use `concepts/`; if you might build it, use `ideas/`.
- Idea vs project: if work has started or there is a clear plan, use `projects/`; otherwise `ideas/`.
- Person vs company/org: if the page is about a human, use `people/`; if it is about an organization, create a project/resource/concept page as appropriate for this MVP.
- Source vs entity: raw imported material goes in `sources/`; extracted meaning goes in entity directories.
- Atom vs source: a memory atom is one compact, dated, source-backed fact or decision; the raw material still belongs in `sources/`.
- Scene vs project: a memory scene restores a bounded work context or decision thread; a project page remains the durable canonical home for the thing being built.
- Diary vs source: `diary/` is the interpreted daily entry; raw agenda goes under `sources/calendar/`.
- Workspace vs entity: `workspace/` is a temporary reasoning surface for the current task. Confirmed durable facts should move into people, projects, concepts, resources, or diary pages.

## Creation Protocol

1. Search for existing pages and aliases before creating a new page.
2. If a page exists, update it instead of making a duplicate.
3. Every new entity page needs frontmatter, Compiled Truth, `---`, and Timeline.
4. Add the page to `brain/index.md`.
5. Append the change to `brain/log.md`.
6. For substantial changes, update `brain/dashboards/recent-changes.md` and add human-review items when needed.
7. If the page is part of L1/L2 memory, preserve a drill-down chain to L0 source refs.
