"""Shared Markdown metadata, provenance, and date policy for local recall."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("Install dependencies: python3 -m pip install -r requirements.txt") from exc

EXCLUDED = {"sources", "workspace", "templates", "inbox", ".raw"}


def read_page(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            try:
                meta = yaml.safe_load("".join(lines[1:i])) or {}
            except yaml.YAMLError as exc:
                raise ValueError(f"{path}: invalid YAML frontmatter") from exc
            if not isinstance(meta, dict):
                raise ValueError(f"{path}: frontmatter must be a mapping")
            return meta, "".join(lines[i + 1:])
    raise ValueError(f"{path}: unclosed frontmatter")


def pages(root: Path, include_sources: bool = False):
    excluded = EXCLUDED - ({"sources"} if include_sources else set())
    for path in sorted(root.rglob("*.md")):
        parts = path.relative_to(root).parts
        if any(part.startswith(".") or part in excluded for part in parts):
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            continue
        yield path


def date_value(value) -> dt.date | None:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if not isinstance(value, str):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        try:
            return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            return None


def instant(value) -> dt.datetime | None:
    try:
        result = value if isinstance(value, dt.datetime) else dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return result if result.tzinfo else None


def content_hash(meta: dict, body: str) -> str:
    # Bind reviews to all substantive fields and the body, excluding review events.
    payload = {"metadata": {k: v for k, v in meta.items() if k != "verified"}, "body": body}
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def verification(meta: dict, body: str) -> str:
    records = meta.get("verified") or []
    if isinstance(records, dict):
        records = [records]
    if not isinstance(records, list):
        return "needs-review"
    current = [r for r in records if isinstance(r, dict)
               and r.get("content_sha256") == content_hash(meta, body)
               and instant(r.get("at")) and isinstance(r.get("by"), str) and r["by"]]
    if any(r["by"].startswith("human:") for r in current):
        return "human-reviewed"
    if current:
        return "machine-confirmed"
    return "needs-review" if records else "unverified"


def freshness(meta: dict, at: dt.datetime | None = None) -> str:
    if not meta.get("stale_after"):
        return "unknown"
    deadline = instant(meta["stale_after"])
    if deadline is None:
        return "unknown"
    return "stale" if (at or dt.datetime.now(dt.timezone.utc)) >= deadline else "fresh"


def window_status(meta: dict, start: dt.date | None, end: dt.date | None,
                  basis: str = "event", as_of: dt.date | None = None) -> str:
    event = date_value(meta.get("event_date"))
    published = date_value(meta.get("published_at"))
    if basis == "known-by":
        if published is None:
            return "unknown"
        if as_of and published > as_of:
            return "after-cutoff"
    selected = published if basis == "published" else event
    if selected is None:
        return "unknown"
    if (start and selected < start) or (end and selected > end):
        return "outside"
    return "inside" if start or end else "unbounded"


def summary(path: Path, meta: dict, body: str) -> tuple[str, str]:
    title = meta.get("title") or next((line[2:] for line in body.splitlines() if line.startswith("# ")), path.stem)
    description = meta.get("description") or "No description; open page before use."
    return str(title).replace("\n", " ")[:160], str(description).replace("\n", " ")[:320]


def write_page(meta: dict, body: str) -> str:
    return "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n" + body
