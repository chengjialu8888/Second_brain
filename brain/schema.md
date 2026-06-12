# Brain Schema

All entity pages use:

```markdown
---
type:
title:
aliases: []
source_refs: []
created:
updated:
confidence: low
---

# Title

> Executive summary.

## State
## Assessment
## Open Threads
## See Also

---

## Timeline

- **YYYY-MM-DD** | Source - What happened.
```

## Required Concepts

- **Compiled Truth**: Everything above `---`. It is the current synthesized view and can be rewritten.
- **Timeline**: Everything below `---`. It is append-only evidence.
- **Source refs**: Relative paths or URLs that back claims.
- **Open Threads**: Unresolved questions, follow-ups, or missing context.

## Person Page

```yaml
type: person
title:
aliases: []
relationship:
importance: tier1 | tier2 | tier3 | unknown
first_seen:
last_seen:
source_refs: []
confidence: low | medium | high
open_threads: []
```

Recommended sections:

- State
- What They Believe
- What They're Building
- Relationship
- Communication Style
- Assessment
- Network
- Open Threads
- See Also
- Timeline

Judgment sections should mark claims as observed, self-described, or inferred.

## Concept Page

```yaml
type: concept
title:
aliases: []
status: emerging | established | validated
source_refs: []
related: []
confidence: low | medium | high
```

Recommended sections:

- Definition
- Why It Matters
- My Current Read
- Counterexamples / Risks
- Related
- Timeline

## Project Page

```yaml
type: project
title:
status: idea | mvp | active | paused
goal:
success_metrics: []
source_refs: []
open_threads: []
```

Recommended sections:

- Goal
- Current State
- Decisions
- Open Threads
- Success Metrics
- Related
- Timeline

## Diary Page

```yaml
type: diary
date:
status: draft | confirmed
source_refs: []
people: []
projects: []
places: []
```

Recommended sections:

- Timeline
- Highlights
- People / Projects / Places
- What I Felt
- Open Questions
- Diary Draft

Diary pages generated from calendar are `draft` until the user adds subjective context.
