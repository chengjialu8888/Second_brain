---
name: strategy-report
mutating: true
writes_pages: true
---

# Strategy Report

Use this workflow for accurate, comprehensive, date-bounded strategic reports.

## Contract

A strategy report is not just a long answer. It is an evidence-backed judgment with a clear freshness boundary.

Every report must include:

- `as_of`
- source window
- source-backed claims
- coverage matrix
- key assumptions
- contradictions or missing evidence
- confidence level
- recommendations separated from facts

## Command

```bash
scripts/second_brain.sh strategy-report "topic" --from YYYY-MM-DD --to YYYY-MM-DD
```

This generates an active workspace draft first. The report should be written only after reviewing that workspace.

## Coverage Matrix

Check these areas before writing:

| Area | Question |
|-|-|
| Market / category | What changed in the relevant market during the window? |
| Customer / user | What customer behavior, need, or pain evidence exists? |
| Product / capability | What product facts or roadmap constraints matter? |
| Competitor / alternatives | What competitor moves are confirmed, stale, or speculative? |
| GTM / distribution | What channels, partnerships, or growth loops matter? |
| Commercial / financial | What pricing, revenue, cost, margin, or conversion evidence exists? |
| Execution / org | What team, resource, dependency, or operating constraint matters? |
| Risk / regulation | What can break the recommendation or limit deployment? |

## Claim Audit

For every major claim, record:

```text
claim -> source -> event/published date -> captured date -> confidence -> caveat
```

If a claim has no source, either remove it or mark it as an assumption.

## Specialist Lens

After the active workspace is reviewed, route one or two lenses:

```bash
scripts/second_brain.sh agents "product strategy"
scripts/second_brain.sh agents "finance strategy"
scripts/second_brain.sh agents "risk review"
```

Agency Agents shape the report craft. Second Brain supplies the evidence.

## Final Report Shape

```text
Title
As of / source window
Executive judgment
Key evidence
Coverage matrix summary
Strategic options
Recommendation
Risks and counterarguments
Open questions
Appendix: sources and excluded/out-of-window evidence
```

## Anti-Patterns

- Do not optimize for fluency before source coverage.
- Do not blend 2025, 2026, and current data without explicit dates.
- Do not hide contradictions.
- Do not fill missing evidence with confident narrative.
