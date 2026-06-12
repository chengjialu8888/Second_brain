#!/usr/bin/env python3
"""Structural lint for the local Second Brain."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path


ROOT = Path("brain")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") and "\n---\n" in text[4:]


def page_title(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def candidate_targets(link: str, source: Path) -> list[Path]:
    normalized = link.strip().strip("/")
    candidates = []
    if normalized.endswith(".md"):
        candidates.append(ROOT / normalized)
    else:
        candidates.append(ROOT / f"{normalized}.md")
        candidates.append(source.parent / f"{normalized}.md")
        candidates.append(ROOT / normalized / "index.md")
    return candidates


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    titles: dict[str, list[Path]] = defaultdict(list)

    if not ROOT.exists():
        errors.append("brain/ directory is missing")
    else:
        for path in ROOT.rglob("*.md"):
            if ".raw" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(Path("."))

            title = page_title(text)
            if title:
                titles[title.lower()].append(rel)

            if path.name != "README.md" and path.name not in {"RESOLVER.md", "schema.md", "index.md", "log.md"}:
                if not has_frontmatter(text):
                    errors.append(f"{rel}: missing frontmatter")
                if "\n---\n" not in text:
                    warnings.append(f"{rel}: missing Compiled Truth / Timeline divider")
                if "## Timeline" not in text:
                    warnings.append(f"{rel}: missing ## Timeline")

            for link in WIKILINK_RE.findall(text):
                if link in {"RESOLVER", "schema"}:
                    possible = [ROOT / f"{link}.md"]
                else:
                    possible = candidate_targets(link, path)
                if not any(target.exists() for target in possible):
                    warnings.append(f"{rel}: broken wikilink [[{link}]]")

            if path.name != "schema.md" and "source_refs:" in text and re.search(r"source_refs:\s*\[\s*\]", text):
                warnings.append(f"{rel}: empty source_refs")

            if path.name != "README.md" and path.parts[-2:-1] == ("diary",) and "status: draft" in text:
                warnings.append(f"{rel}: diary is still draft; user context needed")

    for title, paths in titles.items():
        if len(paths) > 1:
            warnings.append(f"duplicate title '{title}': {', '.join(map(str, paths))}")

    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")

    print(f"Lint complete: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
