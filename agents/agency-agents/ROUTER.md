# Agency Agent Router

Use this router only after Second Brain search/read has established the memory context.

## Quick Commands

```bash
scripts/second_brain.sh agents
scripts/second_brain.sh agents "Feishu integration"
scripts/second_brain.sh agents "product roadmap"
scripts/second_brain.sh agents "security review"
```

## Routing Heuristics

| Need | Start With |
|-|-|
| Product plan, PRD, roadmap, prioritization | `product` division |
| Frontend, backend, data, AI, Feishu, architecture | `engineering` division |
| UI, UX, brand, visual prompts, user research | `design` division |
| Growth, lifecycle, content, community, SEO | `marketing` division |
| Paid acquisition, tracking, campaign audits | `paid-media` division |
| Discovery, deal strategy, proposals, sales coaching | `sales` division |
| Support operations, customer success, knowledge base | `support` division |
| Threat modeling, compliance, incident review | `security` division |
| QA, test planning, automation, edge cases | `testing` division |
| Finance, tax, investment, bookkeeping | `finance` division |
| Spatial, GIS, mapping, 3D scenes | `gis` or `spatial-computing` divisions |
| Research framing or humanities-style analysis | `academic` division |
| Unusual deliverables or meta-workflows | `specialized` division |
| Multi-phase, multi-agent project | `strategy/` NEXUS docs |

## Output Rule

Name the specialist lens only when it materially affects the answer. The normal shape is:

1. Second Brain evidence summary.
2. Specialist-framed recommendation or deliverable.
3. Risks, confidence, and missing context.
4. Suggested brain updates, if useful.
