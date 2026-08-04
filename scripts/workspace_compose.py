#!/usr/bin/env python3
"""Compose a task-scoped active workspace from local Second Brain search."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRAIN = ROOT / "brain"
ISO_DATE_RE = re.compile(r"\b(20\d{2})[-/](\d{1,2})[-/](\d{1,2})\b")
COMPACT_DATE_RE = re.compile(r"\b(20\d{2})(\d{2})(\d{2})\b")


@dataclass
class SearchHit:
    score: int
    path: Path
    snippets: list[str]
    dates: list[str]
    window_status: str


def split_terms(query: str) -> list[str]:
    return [term for term in re.split(r"\s+", query.strip()) if term]


def score_text(text: str, terms: list[str]) -> int:
    lower = text.lower()
    return sum(lower.count(term.lower()) for term in terms)


def parse_iso_date(value: str | None) -> dt.date | None:
    if not value:
        return None
    return dt.date.fromisoformat(value)


def extract_dates(text: str) -> list[str]:
    found: set[str] = set()
    for match in ISO_DATE_RE.finditer(text):
        year, month, day = match.groups()
        try:
            found.add(dt.date(int(year), int(month), int(day)).isoformat())
        except ValueError:
            pass
    for match in COMPACT_DATE_RE.finditer(text):
        year, month, day = match.groups()
        try:
            found.add(dt.date(int(year), int(month), int(day)).isoformat())
        except ValueError:
            pass
    return sorted(found)


def classify_window(dates: list[str], start: dt.date | None, end: dt.date | None) -> str:
    if not dates:
        return "unknown"
    parsed = [dt.date.fromisoformat(value) for value in dates]
    if not start and not end:
        return "unbounded"
    inside = [
        value
        for value in parsed
        if (start is None or value >= start) and (end is None or value <= end)
    ]
    if len(inside) == len(parsed):
        return "inside"
    if inside:
        return "mixed"
    return "outside"


def iter_markdown(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*.md"):
        if ".raw" in path.parts:
            continue
        if "templates" in path.parts:
            continue
        if "workspace" in path.parts:
            continue
        paths.append(path)
    return paths


def search(query: str, limit: int, start: dt.date | None, end: dt.date | None) -> list[SearchHit]:
    terms = split_terms(query)
    hits: list[SearchHit] = []
    if not terms:
        return hits

    for path in iter_markdown(BRAIN):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        score = score_text(text, terms)
        if score <= 0:
            continue
        snippets: list[str] = []
        for line in text.splitlines():
            if any(term.lower() in line.lower() for term in terms):
                snippets.append(line.strip())
            if len(snippets) >= 3:
                break
        date_text = f"{path} " + "\n".join(snippets[:5])
        dates = extract_dates(date_text)
        hits.append(
            SearchHit(
                score=score,
                path=path.relative_to(ROOT),
                snippets=snippets,
                dates=dates,
                window_status=classify_window(dates, start, end),
            )
        )

    hits.sort(key=lambda item: (-item.score, str(item.path)))
    return hits[:limit]


def yaml_list_field(name: str, values: list[str], indent: int = 2) -> str:
    pad = " " * indent
    if not values:
        return f"{name}: []"
    items = "\n".join(f"{pad}- {value}" for value in values)
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
        row = f"| `{hit.path}` | {hit.score} | {hit.window_status} | {date_label} | {snippet} |"
        if hit.window_status == "outside":
            excluded_rows.append(row)
        else:
            evidence_rows.append(row)

    if not evidence_rows:
        evidence_rows.append("|  |  |  |  | No matching in-window evidence found yet. |")
    if not excluded_rows:
        excluded_rows.append("|  |  |  |  | No out-of-window evidence detected by the simple date scan. |")

    coverage = "\n".join(
        f"| {area} | missing |  | {question} |" for area, question in coverage_rows(args.mode)
    )

    return f"""---
type: workspace
title: "{title}"
aliases: []
updated: {today}
as_of: {as_of}
source_window:
  start: {args.start or "unknown"}
  end: {args.end or as_of}
task: "{args.query}"
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

| Evidence | Score | Window | Detected dates | Snippet |
|-|-:|-|-|-|
{chr(10).join(evidence_rows)}

## Active Context

Pin only the claims needed for this task.

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

| Claim | Atom / Scene | Source | Event/published date | Captured date | Confidence | Caveat |
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

| Evidence | Score | Window | Detected dates | Snippet |
|-|-:|-|-|-|
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
    parser.add_argument("--mode", choices=["active-workspace", "strategy-report"], default="active-workspace")
    parser.add_argument("--output", default="brain/workspace/current.md")
    args = parser.parse_args()

    start = parse_iso_date(args.start)
    end = parse_iso_date(args.end)
    hits = search(args.query, args.limit, start, end)

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
