#!/usr/bin/env python3
"""Browse compact metadata or export explicitly selected public OKF documents."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import quote

from knowledge import content_hash, freshness, pages, read_page, summary, verification, write_page

RESERVED = {"index.md", "log.md"}
FORBIDDEN = {"sources", "workspace", "templates", "inbox", "diary", ".raw"}


def catalog(root: Path, query: str = "") -> str:
    groups: dict[str, list[str]] = {}
    for path in pages(root):
        try:
            meta, body = read_page(path)
        except ValueError:
            groups.setdefault("Metadata requiring repair", []).append(
                f"- {path.relative_to(root)} - Invalid frontmatter; inspect before use."
            )
            continue
        if not meta.get("type"):
            continue
        title, description = summary(path, meta, body)
        rel = path.relative_to(root)
        searchable = f"{rel} {title} {description} {meta.get('tags', [])}".lower()
        if query and not all(term.lower() in searchable for term in query.split()):
            continue
        groups.setdefault(str(rel.parent), []).append(
            f"- [{title}]({quote(rel.as_posix())}) - {description} "
            f"[{verification(meta, body)}; freshness: {freshness(meta)}; lifecycle: {meta.get('knowledge_status', 'unknown')}]"
        )
    return "\n\n".join(f"## {name}\n\n" + "\n".join(entries) for name, entries in groups.items()) or "No matching metadata."


def export_bundle(root: Path, selections: list[str], output: Path) -> int:
    root = root.resolve()
    output = output.resolve()
    if output.exists():
        raise ValueError("Output must be a new directory; existing bundles are never overwritten")
    if output.is_relative_to(root):
        raise ValueError("Output must be outside the source root")
    documents = []
    for value in sorted(set(selections)):
        rel = Path(value)
        if rel.is_absolute() or any(p in FORBIDDEN or p.startswith(".") for p in rel.parts):
            raise ValueError(f"Not an exportable canonical path: {value}")
        path = root / rel
        if not path.resolve().is_relative_to(root) or any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError(f"Path escapes root or is a symlink: {value}")
        if path.suffix != ".md" or path.name in RESERVED:
            raise ValueError(f"Select concept Markdown pages, not reserved files: {value}")
        meta, body = read_page(path)
        if meta.get("visibility") != "public":
            raise ValueError(f"Explicit visibility: public required: {value}")
        if not isinstance(meta.get("type"), str) or not meta["type"].strip():
            raise ValueError(f"Non-empty type required: {value}")
        if "[[" in body:
            raise ValueError(f"Use standard Markdown links in the export source: {value}")
        original_hash = content_hash(meta, body)
        exported = dict(meta)
        exported["sb_status"] = exported.pop("status", None)
        exported["status"] = exported.pop("knowledge_status", None) or "draft"
        if exported["status"] not in {"draft", "stable", "deprecated"}:
            raise ValueError(f"Invalid knowledge_status: {value}")
        # Mapping fields changes the reviewed payload. Do not carry verification
        # over to a different artifact; retain its history under a local extension.
        if "verified" in exported:
            exported["sb_verification_history"] = exported.pop("verified")
        exported["sb_origin_sha256"] = original_hash
        sources = exported.get("sources", [])
        if not isinstance(sources, list) or any(not isinstance(s, dict) or not s.get("resource") for s in sources):
            raise ValueError(f"Each sources entry needs a resource: {value}")
        # Legacy refs stay as extensions. No source is followed or copied.
        documents.append((rel, exported, body))
    if not documents:
        raise ValueError("Select at least one page")
    output.mkdir(parents=True)
    indexes: dict[Path, list[str]] = {Path("."): []}
    for rel, meta, body in documents:
        target = output / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(write_page(meta, body), encoding="utf-8")
        title, description = summary(rel, meta, body)
        indexes.setdefault(rel.parent, []).append(f"- [{title}]({quote(rel.name)}) - {description}")
        parent = rel.parent
        while parent != Path("."):
            entry = f"- [{parent.name}]({quote(parent.name)}/index.md) - Topic directory"
            entries = indexes.setdefault(parent.parent, [])
            if entry not in entries:
                entries.append(entry)
            parent = parent.parent
    for directory, entries in indexes.items():
        prefix = '---\nokf_version: "0.2"\n---\n' if directory == Path(".") else ""
        (output / directory / "index.md").write_text(prefix + "# Knowledge index\n\n" + "\n".join(sorted(entries)) + "\n", encoding="utf-8")
    manifest = {"okf_version": "0.2", "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "pages": [p.as_posix() for p, _, _ in documents],
                "limitations": ["Selected pages only; links may reference omitted pages.",
                                "No privacy redaction, source fetching, or executable content execution.",
                                "Exported content requires its own verification."]}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return len(documents)


def validate_bundle(root: Path) -> list[str]:
    errors = []
    if not root.is_dir():
        return ["Bundle directory does not exist"]
    found = list(root.rglob("*.md"))
    if not found:
        return ["Bundle contains no Markdown files"]
    for path in found:
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            errors.append(f"{path}: symlink or path outside bundle")
            continue
        try:
            meta, body = read_page(path)
            if path.name == "index.md":
                allowed = {"okf_version"} if path.parent == root else set()
                if set(meta) - allowed:
                    errors.append(f"{path}: unsupported index frontmatter")
                if not re.search(r"^#.+", body, re.M) or not re.search(r"^[-*] \[.+\]\(.+\)", body, re.M):
                    errors.append(f"{path}: index needs a heading and Markdown entries")
            elif path.name == "log.md":
                headings = re.findall(r"^## (.+)$", body, re.M)
                if meta or not headings:
                    errors.append(f"{path}: log needs dated headings and no frontmatter")
                for heading in headings:
                    dt.date.fromisoformat(heading)
            elif not isinstance(meta.get("type"), str) or not meta["type"].strip():
                errors.append(f"{path}: missing non-empty type")
        except (ValueError, UnicodeError) as exc:
            errors.append(str(exc))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    browse = sub.add_parser("catalog")
    browse.add_argument("--root", type=Path, default=Path("brain"))
    browse.add_argument("--query", default="")
    export = sub.add_parser("export")
    export.add_argument("--root", type=Path, default=Path("brain"))
    export.add_argument("--page", action="append", required=True)
    export.add_argument("--output", type=Path, required=True)
    check = sub.add_parser("validate")
    check.add_argument("root", type=Path)
    fingerprint = sub.add_parser("fingerprint")
    fingerprint.add_argument("page", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "catalog":
            print(catalog(args.root, args.query))
        elif args.command == "export":
            count = export_bundle(args.root, args.page, args.output)
            print(f"Exported {count} explicitly selected pages to {args.output}. Review before sharing.")
        elif args.command == "fingerprint":
            print(content_hash(*read_page(args.page)))
        else:
            errors = validate_bundle(args.root)
            print("\n".join(errors) if errors else "OKF v0.2 core structure valid (not a factual or execution audit).")
            return int(bool(errors))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"{exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
