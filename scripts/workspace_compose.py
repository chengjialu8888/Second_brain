#!/usr/bin/env python3
"""Compose a task-scoped active workspace from local Second Brain search."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from dataclasses import dataclass
from pathlib import Path

from knowledge import freshness, pages, read_page, summary, verification, window_status


ROOT = Path(__file__).resolve().parents[1]
BRAIN = ROOT / "brain"


@dataclass
class SearchHit:
    score: int
    path: Path
    snippets: list[str]
    dates: list[str]
    window_status: str
    trust: str = "unverified"
    freshness: str = "unknown"
    date_basis: str = "event"
    lifecycle: str = "unknown"


def split_terms(query: str) -> list[str]:
    return [term for term in re.split(r"\s+", query.strip()) if term]


def score_text(text: str, terms: list[str]) -> int:
    lower = text.lower()
    return sum(lower.count(term.lower()) for term in terms)


def parse_iso_date(value: str | None) -> dt.date | None:
    if not value:
        return None
    return dt.date.fromisoformat(value)


def search(query: str, limit: int, start: dt.date | None, end: dt.date | None,
           basis: str = "event", as_of: dt.date | None = None,
           include_sources: bool = False) -> list[SearchHit]:
    terms = split_terms(query)
    hits: list[SearchHit] = []
    if not terms:
        return hits

    for path in pages(BRAIN, include_sources):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        score = score_text(text, terms)
        if score <= 0:
            continue
        try:
            meta, body = read_page(path)
            snippets = list(summary(path, meta, body))
            trust = verification(meta, body)
        except ValueError:
            meta, trust = {}, "needs-review"
            snippets = ["Invalid metadata; inspect page before use."]
        dates = [f"{key}={meta[key]}" for key in ("event_date", "published_at", "captured_at") if meta.get(key)]
        hits.append(
            SearchHit(
                score=score,
                path=path.relative_to(ROOT),
                snippets=snippets,
                dates=dates,
                window_status=window_status(meta, start, end, basis, as_of),
                trust=trust,
                freshness=freshness(meta),
                date_basis=basis,
                lifecycle=str(meta.get("knowledge_status") or "unknown"),
            )
        )

    # Outside evidence must not crowd out eligible candidates before truncation.
    priority = {"inside": 0, "unbounded": 0, "unknown": 1, "outside": 2, "after-cutoff": 2}
    hits.sort(key=lambda item: (priority[item.window_status], -item.score, str(item.path)))
    candidates = [h for h in hits if h.window_status not in {"outside", "after-cutoff"}]
    excluded = [h for h in hits if h.window_status in {"outside", "after-cutoff"}]
    return candidates[:limit] + excluded[:limit]


def yaml_list_field(name: str, values: list[str], indent: int = 2) -> str:
    pad = " " * indent
    if not values:
        return f"{name}: []"
    items = "\n".join(f"{pad}- {json.dumps(value, ensure_ascii=False)}" for value in values)
    return f"{name}:\n{items}"


def coverage_rows(mode: str) -> list[tuple[str, str]]:
    if mode == "strategy-report":
        return [
            ("Market / category", "What changed in the category during the source window?"),
            ("Customer / user", "What user need, behavior, or pain is evidenced?"),
            ("Product / capability", "What product fact, roadmap item, or capability matters?"),
            ("Competitor / alternatives", "What competitor move is confirmed, stale, or speculative?"),
            ("GTM / distribution", "What channel, partnership, or growth loop matters?"),
            ("Commercial / financial", "What pricing, revenue, cost, margin, or conversion evidence exists?"),
            ("Execution / org", "What team, resource, dependency, or operating constraint matters?"),
            ("Risk / regulation", "What can break the recommendation or constrain deployment?"),
        ]
    return [
        ("People", "Who matters to this task?"),
        ("Projects", "Which project decisions or constraints matter?"),
        ("Concepts", "Which frameworks or definitions matter?"),
        ("Sources", "Which raw evidence should be read?"),
        ("Assumptions", "What is inferred rather than sourced?"),
        ("Open questions", "What must the user confirm?"),
    ]


def render(args: argparse.Namespace, hits: list[SearchHit]) -> str:
    today = dt.date.today().isoformat()
    as_of = args.as_of or today
    source_refs = [str(hit.path) for hit in hits]
    title = args.title or ("Strategy Report Workspace" if args.mode == "strategy-report" else "Active Workspace")

    evidence_rows = []
    excluded_rows = []
    for hit in hits:
        date_label = ", ".join(hit.dates) if hit.dates else "unknown"
        snippet = " / ".join(hit.snippets).replace("|", "\\|")
        row = f"| `{hit.path}` | {hit.score} | {hit.window_status} | {date_label} | {hit.trust} / {hit.freshness} / {hit.lifecycle} | {snippet} |"
        if hit.window_status in {"outside", "after-cutoff"}:
            excluded_rows.append(row)
        else:
            evidence_rows.append(row)

    if not evidence_rows:
        evidence_rows.append("|  |  |  |  |  | No candidate evidence found yet. |")
    if not excluded_rows:
        excluded_rows.append("|  |  |  |  |  | No dated exclusions found; unknown dates still need review. |")

    coverage = "\n".join(
        f"| {area} | missing |  | {question} |" for area, question in coverage_rows(args.mode)
    )

    return f"""---
type: workspace
title: {json.dumps(title, ensure_ascii=False)}
aliases: []
updated: {today}
as_of: {as_of}
source_window:
  start: {args.start or "unknown"}
  end: {args.end or as_of}
task: {json.dumps(args.query, ensure_ascii=False)}
mode: {args.mode}
status: draft
confidence: low
{yaml_list_field("source_refs", source_refs)}
---

# {title}

> Task-scoped working context. Not canonical memory.

## Operating Rule

This workspace is inspired by the Global Workspace / J-space pattern: keep the active context reportable, controllable, reasoning-coupled, broadcastable across specialist lenses, and capacity-limited.

## Task Frame

- Query: {args.query}
- Mode: {args.mode}
- Audience:
- Decision this should support:
- Final output format:

## Date Boundary

- As of: {as_of}
- Source window start: {args.start or "unknown"}
- Source window end: {args.end or as_of}
- Date basis: {args.date_basis}; known-by requires an event in the window and publication on/before as_of.
- Unknown dates stay unknown. Filename, capture, and edit dates do not establish event time.
- Freshness is evaluated now, independently of the historical report window.
- Freshness rule: primary claims should come from inside the source window or be explicitly marked as background context.

## Capacity Budget

- Active claims target: 5-12
- Open questions target: 3-8
- Specialist lenses target: 1-2 after evidence review

## Asset Loadout

Check `brain/assets.yaml` before final synthesis. Add only assets that materially help this task.

| Asset | Type | Why included | Injection policy |
|-|-|-|-|
|  |  |  |  |

## Candidate Evidence

| Evidence | Score | Window | Explicit dates | Verification / Freshness / Lifecycle | Summary |
|-|-:|-|-|-|-|
{chr(10).join(evidence_rows)}

## Active Context

Pin only the claims needed for this task.
Open each selected page and its sources first. Unknown, stale, deprecated, or needs-review candidates are not approved current facts.

1.
2.
3.
4.
5.

## Coverage Matrix

| Area | Status | Evidence refs | Gap / question |
|-|-|-|-|
{coverage}

## Claim Audit

| Claim ID | Atom / Scene | Source ID + locator | Event date | Published at | Captured at | Verification / version | Validity / caveat |
|-|-|-|-|-|-|-|-|
|  |  |  |  |  |  |  |  |

## Retrieval Coverage

- Topic directories checked:
- Full-text fallback queries:
- Missing dates, contradictions, and omitted branches:

## Metric Calculations

| Metric | Input sources | Formula / script | Units and population | Period | Result / receipt | Review |
|-|-|-|-|-|-|-|
|  |  |  |  |  |  |  |

## Specialist Lens Routing

After evidence review, use one or two lenses if useful:

```bash
scripts/second_brain.sh agents "product strategy"
scripts/second_brain.sh agents "finance strategy"
scripts/second_brain.sh agents "risk review"
```

## Output Contract

- State `as_of` and the source window in the final deliverable.
- Cite local source paths or URLs for important claims.
- Preserve atom / scene refs when a compact memory layer backs a claim.
- Separate facts, assumptions, recommendations, and open questions.
- List important excluded or out-of-window evidence in the appendix.

## Excluded / Out Of Window

| Evidence | Score | Window | Explicit dates | Verification / Freshness / Lifecycle | Summary |
|-|-:|-|-|-|-|
{chr(10).join(excluded_rows)}

---

## Timeline

- **{today}** | System - Generated workspace draft for `{args.query}`.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--title")
    parser.add_argument("--as-of", dest="as_of")
    parser.add_argument("--from", dest="start")
    parser.add_argument("--to", dest="end")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--date-basis", choices=["event", "published", "known-by"], default="event")
    parser.add_argument("--include-sources", action="store_true")
    parser.add_argument("--mode", choices=["active-workspace", "strategy-report"], default="active-workspace")
    parser.add_argument("--output", default="brain/workspace/current.md")
    args = parser.parse_args()

    try:
        as_of = parse_iso_date(args.as_of) or dt.date.today()
        start = parse_iso_date(args.start)
        end = parse_iso_date(args.end) or as_of
    except ValueError:
        parser.error("Dates must be valid YYYY-MM-DD values")
    if args.limit < 1 or (start and start > end) or end > as_of:
        parser.error("Require limit > 0 and from <= to <= as-of")
    if args.mode == "strategy-report" and not (args.start and args.end):
        parser.error("Strategy reports require both --from and --to")
    hits = search(args.query, args.limit, start, end, args.date_basis, as_of, args.include_sources)

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(args, hits), encoding="utf-8")

    rel = output.relative_to(ROOT) if output.is_relative_to(ROOT) else output
    print(f"Workspace draft written: {rel}")
    print(f"Candidate evidence: {len(hits)} hit(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
