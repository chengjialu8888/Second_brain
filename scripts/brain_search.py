#!/usr/bin/env python3
"""Simple local search over brain markdown files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def score_text(text: str, terms: list[str]) -> int:
    lower = text.lower()
    return sum(lower.count(term.lower()) for term in terms)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--root", default="brain")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    root = Path(args.root)
    terms = [term for term in re.split(r"\s+", args.query.strip()) if term]
    if not terms:
        print("Empty query")
        return 2

    results: list[tuple[int, Path, list[str]]] = []
    for path in root.rglob("*.md"):
        if ".raw" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        score = score_text(text, terms)
        if score <= 0:
            continue
        snippets = []
        for line in text.splitlines():
            if any(term.lower() in line.lower() for term in terms):
                snippets.append(line.strip())
            if len(snippets) >= 3:
                break
        results.append((score, path, snippets))

    results.sort(key=lambda item: (-item[0], str(item[1])))
    for score, path, snippets in results[: args.limit]:
        print(f"{path}  score={score}")
        for snippet in snippets:
            print(f"  {snippet}")
    if not results:
        print("No matches.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
