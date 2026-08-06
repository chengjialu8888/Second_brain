# MiroFish Architecture Adaptation

This skill takes architectural inspiration from [MiroFish](https://github.com/666ghj/MiroFish), reviewed at commit `b5b53acc57189a4a42e44a23e149dc655c98fe82` on 2026-08-06. It is an independent, lightweight workflow designed for a Markdown-first Second Brain and Codex subagents; it does not copy MiroFish code.

MiroFish is licensed under AGPL-3.0. Keep this implementation concept-level unless the repository owner deliberately chooses to incorporate AGPL-covered code and accepts the resulting obligations.

## Architectural mapping

| MiroFish stage | Core idea | This skill |
|-|-|-|
| Seed extraction and graph building | Build a structured world from source material | Search Second Brain, create an evidence ledger, and model actors/relations in Markdown and JSON |
| Persona and environment setup | Turn entities into agents with behavior parameters | Create scoped role cards with incentives, constraints, allowed actions, and unknowns |
| Parallel social simulation | Advance interacting agents over simulated time | Execute hierarchical actor waves across bounded rounds and branches |
| Dynamic temporal memory | Feed actions back into the evolving graph | Append events to JSONL, update branch state, and checkpoint role memories |
| ReportAgent | Query the simulated environment before synthesizing | Inspect events, compare branches, interview roles, audit evidence, then write a decision report |
| Deep interaction | Continue questioning agents and the report | Resume from checkpoints and record focused interviews as new append-only events |

## What is intentionally different

- No Zep or GraphRAG dependency. Markdown source references and compact JSON state are enough for the repository's current scale.
- No OASIS social-media environment. The sandbox is domain-general and uses decision-relevant actions instead of Twitter/Reddit mechanics.
- No claim of high-fidelity prediction. Results are conditional scenario outputs with explicit uncertainty.
- Hierarchical orchestration is the default. Free-form mesh interaction is avoided for traceability and context control.
- World state and evidence are separate. Simulated events can never become real source evidence by feedback.
- Deterministic validation checks schemas, event references, confidence bounds, and unsupported high-confidence claims.

## Reusable lessons

The most useful MiroFish ideas are the lifecycle separation, evidence-to-world transformation, role-specific behavior, time-bounded rounds, dynamic memory, queryable post-run artifacts, and dedicated reporting phase. The most important additions for Second Brain are provenance boundaries, branch isolation, role-level access scopes, human gates, and the rule that simulation artifacts remain non-canonical.
