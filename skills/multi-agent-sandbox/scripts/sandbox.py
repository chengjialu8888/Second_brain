#!/usr/bin/env python3
"""Initialize, record, checkpoint, validate, summarize, and finalize sandbox runs."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import uuid
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
BRAIN_ROOT = REPO_ROOT / "brain"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "brain" / "workspace" / "simulations"
SCHEMA_VERSION = 1

REQUIRED_FILES = (
    "scenario.md",
    "state.json",
    "agents.json",
    "evidence-ledger.md",
    "events.jsonl",
    "report.md",
)

EVENT_KINDS = {
    "run_initialized",
    "observation",
    "intention",
    "action",
    "reaction",
    "world_update",
    "audit",
    "interview",
    "decision",
}
EVENT_STATUSES = {"proposed", "accepted", "rejected", "flagged"}
ROLE_TYPES = {"orchestrator", "actor", "auditor", "observer"}
FORBIDDEN_REASONING_FIELDS = {
    "chain_of_thought",
    "hidden_reasoning",
    "private_reasoning",
    "full_reasoning",
}
EVIDENCE_REQUIRED_KINDS = {
    "observation",
    "intention",
    "action",
    "reaction",
    "interview",
    "decision",
}


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def today_iso() -> str:
    return dt.date.today().isoformat()


def slugify(value: str) -> str:
    normalized = value.lower().strip()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    return normalized[:48] or "sandbox"


def stable_role_id(value: str) -> str:
    role_id = slugify(value)
    if not role_id:
        raise ValueError(f"Cannot derive a role ID from {value!r}")
    return role_id


def search_wiki_sources(query: str, limit: int) -> list[str]:
    """Return canonical brain pages that best match a Wiki seed query."""
    terms = [term for term in re.split(r"\s+", query.strip()) if term]
    if not terms:
        return []

    canonical_roots = {
        "people",
        "places",
        "concepts",
        "projects",
        "ideas",
        "diary",
        "resources",
        "memory",
    }
    hits: list[tuple[int, str]] = []
    for path in BRAIN_ROOT.rglob("*.md"):
        relative_to_brain = path.relative_to(BRAIN_ROOT)
        if relative_to_brain.parts[0] not in canonical_roots and relative_to_brain.name != "profile.md":
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lower = content.lower()
        score = sum(lower.count(term.lower()) for term in terms)
        score += sum(path.stem.lower().count(term.lower()) * 3 for term in terms)
        if score > 0:
            hits.append((score, str(path.relative_to(REPO_ROOT))))

    hits.sort(key=lambda item: (-item[0], item[1]))
    return [path for _, path in hits[:limit]]


def json_dump(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def json_load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_list(name: str, values: list[str]) -> str:
    if not values:
        return f"{name}: []"
    rendered = "\n".join(f"  - {yaml_scalar(item)}" for item in values)
    return f"{name}:\n{rendered}"


def resolve_output_root(value: str | None) -> Path:
    if not value:
        return DEFAULT_OUTPUT_ROOT
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    return candidate.resolve()


def make_trace_id(run_id: str, question: str) -> str:
    digest = hashlib.sha256(f"{run_id}\n{question}".encode("utf-8")).hexdigest()[:16]
    return f"trace-{digest}"


def make_role_card(role_id: str, role_type: str, name: str) -> dict[str, Any]:
    if role_type == "orchestrator":
        objective = "Maintain the bounded world, contracts, trace, branches, and stop conditions."
        actions = ["broadcast", "adjudicate", "checkpoint", "stop"]
        write_scope = ["world_update", "decision"]
    elif role_type == "auditor":
        objective = "Detect unsupported claims, contradictions, leaked knowledge, and contract violations."
        actions = ["inspect", "flag", "request_correction"]
        write_scope = ["audit"]
    elif role_type == "observer":
        objective = "Measure branch deltas, novelty, indicators, and unresolved disagreement without acting in-world."
        actions = ["measure", "compare", "summarize"]
        write_scope = ["observation"]
    else:
        objective = f"Act consistently as the {name} stakeholder within declared evidence and constraints."
        actions = ["observe", "ask", "propose", "act", "react"]
        write_scope = ["actor_turn"]

    return {
        "role_id": role_id,
        "name": name,
        "role_type": role_type,
        "objective": objective,
        "incentives": [],
        "constraints": [],
        "resources": [],
        "allowed_actions": actions,
        "observed_evidence_refs": [],
        "unknowns": [],
        "read_scope": ["world_snapshot", "scoped_evidence", "public_events"],
        "write_scope": write_scope,
        "prohibited_actions": [
            "invent private facts",
            "execute external side effects",
            "treat simulated events as real evidence",
        ],
    }


def scenario_markdown(
    *,
    run_id: str,
    title: str,
    question: str,
    horizon: str,
    max_rounds: int,
    wall_clock_minutes: int,
    actor_timeout_seconds: int,
    wiki_query: str,
    branches: list[str],
    roles: list[str],
    source_refs: list[str],
) -> str:
    branch_rows = "\n".join(
        f"| `{branch}` |  |  |  |" for branch in branches
    )
    role_rows = "\n".join(f"| `{role}` | actor |  |  |" for role in roles)
    return f"""---
type: workspace
title: {yaml_scalar(title)}
aliases: []
updated: {today_iso()}
as_of: {today_iso()}
source_window:
  start: unknown
  end: {today_iso()}
task: {yaml_scalar(question)}
mode: multi-agent-sandbox
status: draft
confidence: low
run_id: {run_id}
{yaml_list("source_refs", source_refs)}
---

# {title}

> A bounded scenario experiment, not a factual forecast or canonical memory.

## Task Frame

- Decision question: {question}
- Decision owner:
- Simulation horizon: {horizon}
- Wiki seed query: {wiki_query or "not provided"}
- Out of scope:
- Output contract: decision implication, branch comparison, indicators, triggers, and limitations

## Experiment Boundary

- Maximum rounds: {max_rounds}
- Wall-clock deadline: {wall_clock_minutes} minutes
- Actor timeout: {actor_timeout_seconds} seconds; retry once with narrower scope, then degrade
- Agent outputs are synthetic unless linked to a real source.
- Simulated events remain inside this workspace.
- External side effects are prohibited.

## Branches

| Branch | Changed variables | Fixed variables | Falsifying signal |
|-|-|-|-|
{branch_rows}

## Roles

| Role | Type | Objective | Important constraints |
|-|-|-|-|
{role_rows}

## World Rules

1. Sourced institutional constraints outrank actor preference.
2. Actors may propose state changes; only the orchestrator may apply them.
3. Missing information remains unknown or becomes an explicit assumption.
4. High-impact or irreversible outcomes require human review.

## Hypotheses and Variables

| ID | Class | Statement | Branch | Source / owner | Confidence |
|-|-|-|-|-|-:|
| H1 | hypothesis |  | all |  |  |

## Stop Conditions

- Maximum rounds reached.
- Two consecutive rounds add no decision-relevant novelty.
- Branches converge enough that another round will not change the decision.
- Evidence weakness or a human gate blocks safe continuation.

## Human Gates

| Trigger | Gate | Default on timeout | Owner |
|-|-|-|-|
| Legal, medical, financial, personnel, security, or public-impact decision | blocking review | stop |  |
| Low confidence or unresolved contradiction affects the recommendation | blocking review | stop |  |

## Timeline

- **{today_iso()}** | System - Initialized run `{run_id}`.
"""


def evidence_ledger_markdown(run_id: str, source_refs: list[str]) -> str:
    source_rows = "\n".join(
        f"| E{index} | fact candidate |  | `{source}` | unreviewed |  |"
        for index, source in enumerate(source_refs, start=1)
    )
    if not source_rows:
        source_rows = "| E1 | unknown | No evidence added yet. |  | low | Add sources before high-confidence claims. |"
    return f"""# Evidence Ledger — {run_id}

This ledger separates real evidence from modeling assumptions and simulated events.

| ID | Class | Claim | Source ref | Confidence | Caveat |
|-|-|-|-|-|-|
{source_rows}

## Rules

- `fact`: backed by a real source reference.
- `assumption`: a chosen modeling condition, never a fact.
- `simulated`: produced inside a branch and cited by event ID.
- `unknown`: missing information that may change the result.

Do not add simulated events to sourced-fact rows.
"""


def report_markdown(title: str, run_id: str) -> str:
    return f"""# {title} — Decision Report

> Simulation, not a forecast. All outcomes are conditional on the declared evidence, assumptions, roles, and world rules in run `{run_id}`.

## Decision Implication

Draft after validation.

## Boundary and Horizon

## Branch Comparison

| Branch | Outcome pattern | Mechanism | Evidence / event refs | Confidence | Falsifier |
|-|-|-|-|-|-|
|  |  |  |  |  |  |

## Stable Patterns

## Decisive Disagreements

## Early Indicators and Triggers

## Evidence and Assumption Audit

## Failure Modes and Reversible Next Moves

## Confidence and Limitations
"""


def command_init(args: argparse.Namespace) -> int:
    if not 1 <= args.max_rounds <= 20:
        raise ValueError("--max-rounds must be between 1 and 20")
    if not 1 <= args.wall_clock_minutes <= 240:
        raise ValueError("--wall-clock-minutes must be between 1 and 240")
    if not 15 <= args.actor_timeout_seconds <= 600:
        raise ValueError("--actor-timeout-seconds must be between 15 and 600")
    if not 1 <= args.wiki_limit <= 50:
        raise ValueError("--wiki-limit must be between 1 and 50")

    branches = [stable_role_id(branch) for branch in (args.branch or ["baseline", "adverse", "upside"])]
    branches = list(dict.fromkeys(branches))
    roles = [stable_role_id(role) for role in (args.role or ["affected-user", "operator", "challenger"])]
    roles = list(dict.fromkeys(roles))
    if not roles:
        raise ValueError("At least one actor role is required")
    if len(roles) > 12:
        raise ValueError("At most 12 actor roles are allowed; use waves or merge similar roles")
    if len(branches) > 8:
        raise ValueError("At most 8 branches are allowed")
    reserved_roles = {"orchestrator", "evidence-auditor", "scenario-observer"}
    conflicts = reserved_roles & set(roles)
    if conflicts:
        raise ValueError(f"Actor role IDs conflict with system roles: {sorted(conflicts)}")

    date_prefix = dt.date.today().strftime("%Y%m%d")
    run_id = args.run_id or f"{date_prefix}-{slugify(args.title)}-{uuid.uuid4().hex[:6]}"
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{2,95}", run_id):
        raise ValueError("--run-id must be 3-96 characters using letters, digits, '_' or '-'")

    run_dir = resolve_output_root(args.output_root) / run_id
    if run_dir.exists():
        raise FileExistsError(f"Run already exists: {run_dir}")
    run_dir.mkdir(parents=True)
    (run_dir / "rounds").mkdir()

    wiki_refs = search_wiki_sources(args.wiki_query, args.wiki_limit) if args.wiki_query else []
    source_refs = list(dict.fromkeys([*(args.source_ref or []), *wiki_refs]))
    trace_id = make_trace_id(run_id, args.question)
    created_at = now_iso()

    state = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "trace_id": trace_id,
        "status": "initialized",
        "title": args.title,
        "question": args.question,
        "horizon": args.horizon,
        "wiki_seed": {
            "query": args.wiki_query,
            "limit": args.wiki_limit,
            "matched_refs": wiki_refs,
        },
        "current_round": 0,
        "max_rounds": args.max_rounds,
        "branches": [
            {
                "branch_id": branch,
                "label": branch.replace("-", " ").title(),
                "status": "queued",
                "changed_variables": {},
            }
            for branch in branches
        ],
        "world_seed": {
            "facts": [],
            "variables": {},
            "relations": [],
            "open_uncertainties": [],
        },
        "branch_states": {
            branch: {
                "round": 0,
                "facts": [],
                "variables": {},
                "relations": [],
                "open_uncertainties": [],
                "accepted_event_ids": [],
            }
            for branch in branches
        },
        "termination": {
            "max_rounds": args.max_rounds,
            "wall_clock_minutes": args.wall_clock_minutes,
            "actor_timeout_seconds": args.actor_timeout_seconds,
            "no_novelty_rounds": 2,
            "budget_exhausted": False,
            "human_stop": False,
        },
        "source_refs": source_refs,
        "created_at": created_at,
        "updated_at": created_at,
    }

    role_cards = [
        make_role_card("orchestrator", "orchestrator", "World keeper and orchestrator"),
        make_role_card("evidence-auditor", "auditor", "Evidence and contradiction auditor"),
        make_role_card("scenario-observer", "observer", "Cross-branch scenario observer"),
    ]
    role_cards.extend(
        make_role_card(role, "actor", role.replace("-", " ").title()) for role in roles
    )

    init_event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": f"evt-{uuid.uuid4().hex[:12]}",
        "trace_id": trace_id,
        "timestamp": created_at,
        "round": 0,
        "branch_id": branches[0],
        "actor_id": "orchestrator",
        "kind": "run_initialized",
        "summary": f"Initialized sandbox run {run_id}.",
        "brief_rationale": "Created a bounded, traceable workspace before simulation.",
        "evidence_refs": source_refs,
        "assumptions": [],
        "confidence": 1.0,
        "effects": {},
        "status": "accepted",
    }

    (run_dir / "scenario.md").write_text(
        scenario_markdown(
            run_id=run_id,
            title=args.title,
            question=args.question,
            horizon=args.horizon,
            max_rounds=args.max_rounds,
            wall_clock_minutes=args.wall_clock_minutes,
            actor_timeout_seconds=args.actor_timeout_seconds,
            wiki_query=args.wiki_query,
            branches=branches,
            roles=roles,
            source_refs=source_refs,
        ),
        encoding="utf-8",
    )
    json_dump(run_dir / "state.json", state)
    json_dump(run_dir / "agents.json", role_cards)
    (run_dir / "evidence-ledger.md").write_text(
        evidence_ledger_markdown(run_id, source_refs), encoding="utf-8"
    )
    (run_dir / "events.jsonl").write_text(
        json.dumps(init_event, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (run_dir / "report.md").write_text(
        report_markdown(args.title, run_id), encoding="utf-8"
    )

    print(run_dir)
    return 0


def parse_effects(values: list[str]) -> dict[str, Any]:
    effects: dict[str, Any] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"Effect must use key=value syntax: {value!r}")
        key, raw = value.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError("Effect key cannot be empty")
        try:
            effects[key] = json.loads(raw)
        except json.JSONDecodeError:
            effects[key] = raw
    return effects


def load_run(run_dir_value: str) -> tuple[Path, dict[str, Any], list[dict[str, Any]]]:
    run_dir = Path(run_dir_value).expanduser().resolve()
    if not run_dir.is_dir():
        raise FileNotFoundError(f"Run directory not found: {run_dir}")
    return run_dir, json_load(run_dir / "state.json"), json_load(run_dir / "agents.json")


def command_record(args: argparse.Namespace) -> int:
    run_dir, state, agents = load_run(args.run_dir)
    if not 0 <= args.round <= state["max_rounds"]:
        raise ValueError(f"--round must be between 0 and {state['max_rounds']}")

    actor_ids = {agent["role_id"] for agent in agents}
    branch_ids = {branch["branch_id"] for branch in state["branches"]}
    if args.actor not in actor_ids:
        raise ValueError(f"Unknown actor {args.actor!r}; choose one of {sorted(actor_ids)}")
    if args.branch not in branch_ids:
        raise ValueError(f"Unknown branch {args.branch!r}; choose one of {sorted(branch_ids)}")
    if not 0.0 <= args.confidence <= 1.0:
        raise ValueError("--confidence must be between 0 and 1")

    event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": args.event_id or f"evt-{uuid.uuid4().hex[:12]}",
        "trace_id": state["trace_id"],
        "timestamp": now_iso(),
        "round": args.round,
        "branch_id": args.branch,
        "actor_id": args.actor,
        "kind": args.kind,
        "summary": args.summary,
        "brief_rationale": args.brief_rationale,
        "evidence_refs": list(dict.fromkeys(args.evidence_ref or [])),
        "assumptions": list(dict.fromkeys(args.assumption or [])),
        "confidence": args.confidence,
        "effects": parse_effects(args.effect or []),
        "status": args.status,
    }

    with (run_dir / "events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")

    state["current_round"] = max(state["current_round"], args.round)
    state["status"] = "running"
    state["updated_at"] = now_iso()
    branch_state = state.setdefault("branch_states", {}).setdefault(
        args.branch,
        {
            "round": 0,
            "facts": [],
            "variables": {},
            "relations": [],
            "open_uncertainties": [],
            "accepted_event_ids": [],
        },
    )
    branch_state["round"] = max(branch_state.get("round", 0), args.round)
    if args.status == "accepted":
        branch_state.setdefault("accepted_event_ids", []).append(event["event_id"])
    if args.kind == "world_update" and args.status == "accepted":
        branch_state.setdefault("variables", {}).update(event["effects"])
    for branch in state["branches"]:
        if branch["branch_id"] == args.branch and branch["status"] == "queued":
            branch["status"] = "running"
    json_dump(run_dir / "state.json", state)
    print(event["event_id"])
    return 0


def read_events(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    events: list[dict[str, Any]] = []
    errors: list[str] = []
    if not path.exists():
        return events, [f"missing {path.name}"]
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"events.jsonl:{line_number}: invalid JSON: {error.msg}")
            continue
        if not isinstance(value, dict):
            errors.append(f"events.jsonl:{line_number}: event must be an object")
            continue
        value["_line"] = line_number
        events.append(value)
    return events, errors


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def command_checkpoint(args: argparse.Namespace) -> int:
    run_dir, state, _ = load_run(args.run_dir)
    round_number = args.round if args.round is not None else state["current_round"]
    if not 0 <= round_number <= state["max_rounds"]:
        raise ValueError(f"round must be between 0 and {state['max_rounds']}")

    events, parse_errors = read_events(run_dir / "events.jsonl")
    if parse_errors:
        raise ValueError("; ".join(parse_errors))
    round_events = [event for event in events if event.get("round") == round_number]
    checkpoint_path = run_dir / "rounds" / f"round-{round_number:02d}.md"
    if checkpoint_path.exists():
        raise FileExistsError(f"Checkpoint is immutable and already exists: {checkpoint_path}")

    rows = []
    for event in round_events:
        refs = ", ".join(event.get("evidence_refs", [])) or "—"
        rows.append(
            "| {event_id} | {branch} | {actor} | {kind} | {summary} | {refs} | {confidence:.2f} | {status} |".format(
                event_id=md_escape(event.get("event_id", "")),
                branch=md_escape(event.get("branch_id", "")),
                actor=md_escape(event.get("actor_id", "")),
                kind=md_escape(event.get("kind", "")),
                summary=md_escape(event.get("summary", "")),
                refs=md_escape(refs),
                confidence=float(event.get("confidence", 0.0)),
                status=md_escape(event.get("status", "")),
            )
        )
    if not rows:
        rows.append("|  |  |  |  | No events recorded for this round. | — |  |  |")

    accepted = sum(event.get("status") == "accepted" for event in round_events)
    flagged = sum(event.get("status") == "flagged" for event in round_events)
    unsupported = sum(
        event.get("kind") in EVIDENCE_REQUIRED_KINDS
        and event.get("confidence", 0) >= 0.7
        and not event.get("evidence_refs")
        for event in round_events
    )
    branch_state_snapshot = {
        branch_id: branch_state
        for branch_id, branch_state in state.get("branch_states", {}).items()
        if branch_state.get("round", 0) >= round_number
    }
    content = f"""# Round {round_number} Checkpoint

- Run: `{state['run_id']}`
- Trace: `{state['trace_id']}`
- Created: {now_iso()}
- Events: {len(round_events)}
- Accepted: {accepted}
- Flagged: {flagged}
- Unsupported high-confidence events: {unsupported}

| Event | Branch | Actor | Kind | Summary | Evidence | Confidence | Status |
|-|-|-|-|-|-|-:|-|
{chr(10).join(rows)}

## World Delta

```json
{json.dumps(branch_state_snapshot, ensure_ascii=False, indent=2)}
```

This is simulated branch state, not real evidence.

## Contradictions and Open Uncertainties

Retain unresolved disagreement for the next round or report.

## Next Broadcast

Summarize only public state, stable IDs, and scoped evidence needed by the next actor wave.
"""
    checkpoint_path.write_text(content, encoding="utf-8")
    state["current_round"] = max(state["current_round"], round_number)
    state["status"] = "running"
    state["updated_at"] = now_iso()
    json_dump(run_dir / "state.json", state)
    print(checkpoint_path)
    return 0


def build_metrics(run_dir: Path, state: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    relevant_events = [event for event in events if event.get("kind") != "run_initialized"]
    evidence_events = [
        event for event in relevant_events if event.get("kind") in EVIDENCE_REQUIRED_KINDS
    ]
    events_with_evidence = sum(bool(event.get("evidence_refs")) for event in evidence_events)
    events_with_assumptions = sum(bool(event.get("assumptions")) for event in relevant_events)
    confidences = [
        float(event["confidence"])
        for event in relevant_events
        if isinstance(event.get("confidence"), (int, float))
    ]
    high_conf_unsupported = [
        event.get("event_id")
        for event in evidence_events
        if float(event.get("confidence", 0.0)) >= 0.7 and not event.get("evidence_refs")
    ]
    branch_ids = [branch["branch_id"] for branch in state.get("branches", [])]
    branches_with_events = {event.get("branch_id") for event in relevant_events}

    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": state.get("run_id"),
        "trace_id": state.get("trace_id"),
        "generated_at": now_iso(),
        "events_total": len(relevant_events),
        "events_accepted": sum(event.get("status") == "accepted" for event in relevant_events),
        "events_flagged": sum(event.get("status") == "flagged" for event in relevant_events),
        "events_by_kind": dict(sorted(Counter(event.get("kind", "unknown") for event in relevant_events).items())),
        "events_by_actor": dict(sorted(Counter(event.get("actor_id", "unknown") for event in relevant_events).items())),
        "events_by_branch": dict(sorted(Counter(event.get("branch_id", "unknown") for event in relevant_events).items())),
        "rounds_observed": sorted({event.get("round") for event in relevant_events if isinstance(event.get("round"), int)}),
        "evidence_coverage": round(events_with_evidence / len(evidence_events), 4) if evidence_events else None,
        "assumption_visibility": round(events_with_assumptions / len(relevant_events), 4) if relevant_events else None,
        "mean_confidence": round(sum(confidences) / len(confidences), 4) if confidences else None,
        "unsupported_high_confidence_event_ids": high_conf_unsupported,
        "branches_without_events": [branch for branch in branch_ids if branch not in branches_with_events],
        "run_dir": str(run_dir),
    }


def command_summarize(args: argparse.Namespace) -> int:
    run_dir, state, _ = load_run(args.run_dir)
    events, errors = read_events(run_dir / "events.jsonl")
    if errors:
        raise ValueError("; ".join(errors))
    for event in events:
        event.pop("_line", None)
    metrics = build_metrics(run_dir, state, events)
    if args.write:
        json_dump(run_dir / "metrics.json", metrics)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


def command_validate(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not run_dir.is_dir():
        print(f"ERROR: run directory not found: {run_dir}")
        return 1

    for name in REQUIRED_FILES:
        if not (run_dir / name).is_file():
            errors.append(f"missing required file: {name}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    try:
        state = json_load(run_dir / "state.json")
    except (json.JSONDecodeError, OSError) as error:
        print(f"ERROR: invalid state.json: {error}")
        return 1
    try:
        agents = json_load(run_dir / "agents.json")
    except (json.JSONDecodeError, OSError) as error:
        print(f"ERROR: invalid agents.json: {error}")
        return 1

    if state.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"state schema_version must be {SCHEMA_VERSION}")
    if not isinstance(state.get("max_rounds"), int) or not 1 <= state["max_rounds"] <= 20:
        errors.append("state max_rounds must be an integer between 1 and 20")
    termination = state.get("termination")
    if not isinstance(termination, dict):
        errors.append("state termination must be an object")
    else:
        wall_clock_minutes = termination.get("wall_clock_minutes")
        actor_timeout_seconds = termination.get("actor_timeout_seconds")
        if not isinstance(wall_clock_minutes, int) or not 1 <= wall_clock_minutes <= 240:
            errors.append("termination wall_clock_minutes must be between 1 and 240")
        if not isinstance(actor_timeout_seconds, int) or not 15 <= actor_timeout_seconds <= 600:
            errors.append("termination actor_timeout_seconds must be between 15 and 600")
    if not isinstance(state.get("world_seed"), dict):
        errors.append("state world_seed must be an object")
    wiki_seed = state.get("wiki_seed")
    if not isinstance(wiki_seed, dict):
        errors.append("state wiki_seed must be an object")
    elif wiki_seed.get("query") and not wiki_seed.get("matched_refs"):
        warnings.append("Wiki seed query matched no canonical brain pages")
    if not isinstance(agents, list) or not agents:
        errors.append("agents.json must contain a non-empty array")
        agents = []

    role_ids: list[str] = []
    role_types: list[str] = []
    required_role_fields = {
        "role_id",
        "name",
        "role_type",
        "objective",
        "allowed_actions",
        "read_scope",
        "write_scope",
        "prohibited_actions",
    }
    for index, agent in enumerate(agents):
        if not isinstance(agent, dict):
            errors.append(f"agent {index} must be an object")
            continue
        missing = required_role_fields - set(agent)
        if missing:
            errors.append(f"agent {index} missing fields: {sorted(missing)}")
        role_id = agent.get("role_id")
        if isinstance(role_id, str):
            role_ids.append(role_id)
        else:
            errors.append(f"agent {index} role_id must be a string")
        role_type = agent.get("role_type")
        if role_type not in ROLE_TYPES:
            errors.append(f"agent {role_id or index} has invalid role_type {role_type!r}")
        else:
            role_types.append(role_type)

    duplicate_roles = sorted(role for role, count in Counter(role_ids).items() if count > 1)
    if duplicate_roles:
        errors.append(f"duplicate role IDs: {duplicate_roles}")
    for required_type in ("orchestrator", "auditor", "observer"):
        if required_type not in role_types:
            errors.append(f"missing required {required_type} role")
    if "actor" not in role_types:
        errors.append("at least one actor role is required")

    branches = state.get("branches", [])
    if not isinstance(branches, list) or not branches:
        errors.append("state branches must be a non-empty array")
        branch_ids: list[str] = []
    else:
        branch_ids = [branch.get("branch_id") for branch in branches if isinstance(branch, dict)]
        if len(branch_ids) != len(branches) or any(not isinstance(value, str) or not value for value in branch_ids):
            errors.append("every branch must have a non-empty branch_id")
        duplicate_branches = sorted(
            branch for branch, count in Counter(branch_ids).items() if count > 1
        )
        if duplicate_branches:
            errors.append(f"duplicate branch IDs: {duplicate_branches}")

    branch_states = state.get("branch_states")
    if not isinstance(branch_states, dict):
        errors.append("state branch_states must be an object")
    elif set(branch_states) != set(branch_ids):
        errors.append("state branch_states keys must exactly match branch IDs")
    else:
        for branch_id, branch_state in branch_states.items():
            if not isinstance(branch_state, dict):
                errors.append(f"branch state {branch_id!r} must be an object")
                continue
            for field in ("facts", "variables", "relations", "open_uncertainties", "accepted_event_ids"):
                if field not in branch_state:
                    errors.append(f"branch state {branch_id!r} missing field {field!r}")

    events, parse_errors = read_events(run_dir / "events.jsonl")
    errors.extend(parse_errors)
    seen_event_ids: set[str] = set()
    required_event_fields = {
        "schema_version",
        "event_id",
        "trace_id",
        "timestamp",
        "round",
        "branch_id",
        "actor_id",
        "kind",
        "summary",
        "evidence_refs",
        "assumptions",
        "confidence",
        "effects",
        "status",
    }
    for event in events:
        line = event.get("_line", "?")
        missing = required_event_fields - set(event)
        if missing:
            errors.append(f"events.jsonl:{line}: missing fields {sorted(missing)}")
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            errors.append(f"events.jsonl:{line}: event_id must be a non-empty string")
        elif event_id in seen_event_ids:
            errors.append(f"events.jsonl:{line}: duplicate event_id {event_id}")
        else:
            seen_event_ids.add(event_id)
        if event.get("schema_version") != SCHEMA_VERSION:
            errors.append(f"events.jsonl:{line}: schema_version must be {SCHEMA_VERSION}")
        if event.get("trace_id") != state.get("trace_id"):
            errors.append(f"events.jsonl:{line}: trace_id does not match state")
        if event.get("kind") not in EVENT_KINDS:
            errors.append(f"events.jsonl:{line}: invalid kind {event.get('kind')!r}")
        if event.get("status") not in EVENT_STATUSES:
            errors.append(f"events.jsonl:{line}: invalid status {event.get('status')!r}")
        if event.get("actor_id") not in set(role_ids):
            errors.append(f"events.jsonl:{line}: unknown actor_id {event.get('actor_id')!r}")
        if event.get("branch_id") not in set(branch_ids):
            errors.append(f"events.jsonl:{line}: unknown branch_id {event.get('branch_id')!r}")
        round_value = event.get("round")
        if not isinstance(round_value, int) or not 0 <= round_value <= state.get("max_rounds", -1):
            errors.append(f"events.jsonl:{line}: round is outside run bounds")
        confidence = event.get("confidence")
        if not isinstance(confidence, (int, float)) or not 0.0 <= float(confidence) <= 1.0:
            errors.append(f"events.jsonl:{line}: confidence must be between 0 and 1")
        forbidden = FORBIDDEN_REASONING_FIELDS & set(event)
        if forbidden:
            errors.append(f"events.jsonl:{line}: forbidden reasoning fields {sorted(forbidden)}")
        if (
            event.get("kind") in EVIDENCE_REQUIRED_KINDS
            and isinstance(confidence, (int, float))
            and float(confidence) >= 0.7
            and not event.get("evidence_refs")
        ):
            warnings.append(f"events.jsonl:{line}: high-confidence event has no evidence refs")

    current_round = state.get("current_round", 0)
    if isinstance(current_round, int) and current_round > 0:
        for round_number in range(1, current_round + 1):
            if not (run_dir / "rounds" / f"round-{round_number:02d}.md").is_file():
                warnings.append(f"missing checkpoint for round {round_number}")

    source_refs = state.get("source_refs", [])
    if not source_refs:
        warnings.append("run has no source references; keep conclusions low confidence")
    for source_ref in source_refs:
        if not isinstance(source_ref, str):
            errors.append("state source_refs must contain strings")
            continue
        if re.match(r"https?://", source_ref):
            continue
        source_path = Path(source_ref)
        if not source_path.is_absolute():
            source_path = REPO_ROOT / source_path
        if not source_path.exists():
            warnings.append(f"local source ref does not exist: {source_ref}")

    report_text = (run_dir / "report.md").read_text(encoding="utf-8")
    if "Simulation, not a forecast" not in report_text:
        warnings.append("report.md is missing the simulation boundary notice")

    for error in errors:
        print(f"ERROR: {error}")
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        return 1
    if warnings and args.strict:
        return 1
    print(f"OK: valid sandbox run ({len(events)} events, {len(warnings)} warnings)")
    return 0


def command_finalize(args: argparse.Namespace) -> int:
    run_dir, state, _ = load_run(args.run_dir)
    validation_status = command_validate(
        argparse.Namespace(run_dir=str(run_dir), strict=False)
    )
    if validation_status != 0:
        return validation_status

    events, parse_errors = read_events(run_dir / "events.jsonl")
    if parse_errors:
        raise ValueError("; ".join(parse_errors))
    if state.get("current_round", 0) < 1:
        raise ValueError("Cannot finalize before at least one simulation round")
    checkpoint = run_dir / "rounds" / f"round-{state['current_round']:02d}.md"
    if not checkpoint.is_file():
        raise ValueError(f"Final checkpoint is missing: {checkpoint}")
    if args.status == "completed" and not any(
        event.get("kind") == "decision" and event.get("status") == "accepted"
        for event in events
    ):
        raise ValueError("A completed run requires at least one accepted decision event")

    report_text = (run_dir / "report.md").read_text(encoding="utf-8")
    if args.status == "completed" and "Draft after validation." in report_text:
        raise ValueError("Replace the report draft marker before finalizing a completed run")

    completed_at = now_iso()
    state["status"] = args.status
    state["updated_at"] = completed_at
    state["completed_at"] = completed_at
    for branch in state.get("branches", []):
        branch["status"] = args.status
    json_dump(run_dir / "state.json", state)

    for event in events:
        event.pop("_line", None)
    metrics = build_metrics(run_dir, state, events)
    metrics["final_status"] = args.status
    json_dump(run_dir / "metrics.json", metrics)
    print(run_dir)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage a traceable multi-agent sandbox workspace."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a new run workspace")
    init_parser.add_argument("--title", required=True)
    init_parser.add_argument("--question", required=True)
    init_parser.add_argument("--horizon", default="unspecified")
    init_parser.add_argument("--max-rounds", type=int, default=3)
    init_parser.add_argument("--wall-clock-minutes", type=int, default=20)
    init_parser.add_argument("--actor-timeout-seconds", type=int, default=120)
    init_parser.add_argument(
        "--wiki-query",
        default="",
        help="Search canonical brain Wiki pages and seed source refs automatically",
    )
    init_parser.add_argument("--wiki-limit", type=int, default=8)
    init_parser.add_argument("--branch", action="append", help="Repeat for each branch")
    init_parser.add_argument("--role", action="append", help="Repeat for each actor role")
    init_parser.add_argument("--source-ref", action="append", help="Repeat for each source")
    init_parser.add_argument("--run-id")
    init_parser.add_argument("--output-root")
    init_parser.set_defaults(func=command_init)

    record_parser = subparsers.add_parser("record", help="Append one event")
    record_parser.add_argument("run_dir")
    record_parser.add_argument("--round", type=int, required=True)
    record_parser.add_argument("--branch", required=True)
    record_parser.add_argument("--actor", required=True)
    record_parser.add_argument("--kind", choices=sorted(EVENT_KINDS), required=True)
    record_parser.add_argument("--summary", required=True)
    record_parser.add_argument("--brief-rationale", default="")
    record_parser.add_argument("--evidence-ref", action="append")
    record_parser.add_argument("--assumption", action="append")
    record_parser.add_argument("--confidence", type=float, default=0.5)
    record_parser.add_argument("--effect", action="append", help="key=value; repeatable")
    record_parser.add_argument("--status", choices=sorted(EVENT_STATUSES), default="accepted")
    record_parser.add_argument("--event-id")
    record_parser.set_defaults(func=command_record)

    checkpoint_parser = subparsers.add_parser(
        "checkpoint", help="Write an immutable round checkpoint"
    )
    checkpoint_parser.add_argument("run_dir")
    checkpoint_parser.add_argument("--round", type=int)
    checkpoint_parser.set_defaults(func=command_checkpoint)

    validate_parser = subparsers.add_parser("validate", help="Validate contracts")
    validate_parser.add_argument("run_dir")
    validate_parser.add_argument("--strict", action="store_true")
    validate_parser.set_defaults(func=command_validate)

    summarize_parser = subparsers.add_parser("summarize", help="Compute run metrics")
    summarize_parser.add_argument("run_dir")
    summarize_parser.add_argument("--write", action="store_true")
    summarize_parser.set_defaults(func=command_summarize)

    finalize_parser = subparsers.add_parser(
        "finalize", help="Validate and close a run after its final report"
    )
    finalize_parser.add_argument("run_dir")
    finalize_parser.add_argument(
        "--status",
        choices=["completed", "degraded", "stopped"],
        default="completed",
    )
    finalize_parser.set_defaults(func=command_finalize)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (FileNotFoundError, FileExistsError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
