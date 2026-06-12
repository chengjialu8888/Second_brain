---
type: concept
title: Second Brain
aliases: ["personal brain", "个人第二大脑"]
status: emerging
source_refs:
  - ../../second-brain-product-plan.md
confidence: medium
---

# Second Brain

> A local-first personal memory system where agents preserve raw sources, maintain Markdown entity pages, and answer with cited synthesis plus known gaps.

## Definition

Second Brain is not a generic knowledge base. It stores personal memory, relationships, decisions, projects, and open threads in a form both humans and agents can read.

## Why It Matters

The useful unit is not a pile of notes. It is a maintained context layer that can be loaded on demand when an agent needs to understand the user's history.

## My Current Read

The first version should be a skill and local folder, not an app. It should stay Obsidian-friendly while treating the filesystem as the source of truth.

## Counterexamples / Risks

- If it only retrieves snippets, it is search rather than brain.
- If it lacks resolver rules, duplicate and stale pages will accumulate.
- If it writes subjective conclusions without user input, it pollutes personal memory.

## Related

- [[llm-wiki]]
- [[wiki-lint]]
- [[compiled-truth]]

---

## Timeline

- **2026-06-12** | ../../second-brain-product-plan.md - Defined v0.2 as skill-first, brain-ready.
