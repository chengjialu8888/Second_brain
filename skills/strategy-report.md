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
- selected asset loadout when useful
- atom / scene refs when compact memory layers back a claim
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

Before writing, check `brain/assets.yaml` for relevant memory, skill, wiki, source-pack, or future codegraph assets. Use `docs/MEMORY_LAYERS.md` to decide whether to rely on L3 operating memory, L2 scenes, L1 atoms, or L0 raw sources.

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

Declare `--date-basis`: `event` for retrospective events, `published` for a
publication survey, or `known-by` to require events in the window and publication
on/before `--as-of`. The latter still needs archived sources when current pages
have changed. Unknown metadata never establishes an in-window fact.

Bind each claim to stable source IDs and locators. Keep event, publication,
capture, verification, and validity dates distinct. Recheck a source when a
review no longer matches the page fingerprint or when freshness has expired.
For computed numbers, record input source IDs, population, units, formula,
period, result and receipt in the workspace's Metric Calculations ledger.
Arithmetic checks do not establish methodological comparability.

For every major claim, record:

```text
claim ID -> atom/scene -> source ID + locator -> event date -> publication -> capture -> current review -> validity/caveat
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
- Do not treat asset metadata as evidence.
