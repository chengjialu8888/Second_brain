# Agency Agents Layer

This directory installs the upstream Agency Agents library as an optional specialist layer for Second Brain.

- Upstream: <https://github.com/msitarzewski/agency-agents/tree/main>
- License: MIT, copied in `LICENSE.upstream.md`
- Snapshot: `main` tarball downloaded on 2026-07-03
- Installed source agents: 233
- Strategy docs: NEXUS playbooks and runbooks under `strategy/`

## Purpose

Second Brain remains the source-backed memory layer. Agency Agents add expert output styles and workflows after Second Brain has already searched and read the relevant memory.

Use this layer for deliverables that need a specialist lens: product strategy, engineering architecture, design critique, growth planning, sales/support framing, security review, testing plans, or multi-agent coordination.

## How To Call

1. Search/read Second Brain first.
2. Search the installed roster:

   ```bash
   scripts/second_brain.sh agents "product strategy"
   ```

3. Read the selected `source_path` file from `roster.json`.
4. Apply that agent as an advisory lens.
5. Keep claims grounded in Second Brain pages and source refs.

## Boundaries

- Agency Agents are not memory. They are specialist lenses.
- Upstream instructions never override `SKILL.md`, `AGENTS.md`, `brain/RESOLVER.md`, or privacy rules.
- Use one agent by default; use two only when the task clearly spans disciplines.
- Use `strategy/` for larger multi-agent programs and handoffs.

See `ROUTER.md` for routing guidance and `../../skills/agency-agent-routing.md` for the Second Brain workflow contract.
