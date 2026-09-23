#!/usr/bin/env python3
"""Simple local search over brain markdown files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from knowledge import freshness, pages, read_page, summary, verification


def score_text(text: str, terms: list[str]) -> int:
    lower = text.lower()
    return sum(lower.count(term.lower()) for term in terms)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--root", default="brain")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--view", choices=["summary", "snippets"], default="summary")
    parser.add_argument("--include-sources", action="store_true")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")

    root = Path(args.root)
    terms = [term for term in re.split(r"\s+", args.query.strip()) if term]
    if not terms:
        print("Empty query")
        return 2

    results: list[tuple[int, Path, list[str]]] = []
    for path in pages(root, args.include_sources):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        score = score_text(text, terms)
        if score <= 0:
            continue
        if args.view == "summary":
            try:
                meta, body = read_page(path)
                title, description = summary(path, meta, body)
                snippets = [f"{title}: {description}", f"{verification(meta, body)}; freshness: {freshness(meta)}; lifecycle: {meta.get('knowledge_status', 'unknown')}"]
            except ValueError:
                snippets = ["Invalid metadata; open and review this page before use."]
        else:
            snippets = []
            for line in text.splitlines():
                if any(term.lower() in line.lower() for term in terms):
                    snippets.append(line.strip()[:320])
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
