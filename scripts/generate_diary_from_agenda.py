#!/usr/bin/env python3
"""Generate a diary draft from saved Feishu agenda outputs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def find_strings(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in {"summary", "title", "subject", "location", "description"} and isinstance(item, str):
                strings.append(item)
            else:
                strings.extend(find_strings(item))
    elif isinstance(value, list):
        for item in value:
            strings.extend(find_strings(item))
    return strings


def extract_candidates(raw: Any, pretty_text: str) -> tuple[list[str], list[str]]:
    titles: list[str] = []
    if raw is not None:
        for item in find_strings(raw):
            clean = re.sub(r"\s+", " ", item).strip()
            if clean and clean not in titles:
                titles.append(clean)

    if not titles:
        for line in pretty_text.splitlines():
            clean = line.strip()
            if re.search(r"\d{1,2}:\d{2}", clean) and clean not in titles:
                titles.append(clean)

    people_or_projects: list[str] = []
    for title in titles:
        for token in re.findall(r"[\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z0-9_-]{1,24}", title):
            if token not in people_or_projects and token.lower() not in {"http", "https"}:
                people_or_projects.append(token)
    return titles[:20], people_or_projects[:20]


def main() -> int:
    if len(sys.argv) != 5:
        print("Usage: generate_diary_from_agenda.py <date> <agenda.json> <agenda.txt> <diary.md>", file=sys.stderr)
        return 2

    date_arg = sys.argv[1]
    json_path = Path(sys.argv[2])
    pretty_path = Path(sys.argv[3])
    diary_path = Path(sys.argv[4])

    raw = load_json(json_path)
    pretty_text = pretty_path.read_text(encoding="utf-8") if pretty_path.exists() else ""
    titles, candidates = extract_candidates(raw, pretty_text)

    agenda_lines = "\n".join(f"- {item}" for item in titles) if titles else "- （今天日程为空或未能解析日程标题）"
    candidate_lines = "\n".join(f"- [[{item}]]" for item in candidates[:10]) if candidates else "- 暂无候选实体"

    content = f"""---
type: diary
date: {date_arg}
status: draft
source_refs:
  - ../sources/calendar/{date_arg}.json
  - ../sources/calendar/{date_arg}.txt
people: []
projects: []
places: []
---

# {date_arg}

## Timeline

{agenda_lines}

## Highlights

- 今天最值得记住的事：
- 今天推进最多的项目：
- 今天最需要后续跟进的人或事：

## People / Projects / Places

{candidate_lines}

## What I Felt

- 我今天最强烈的感受是：
- 为什么：

## Open Questions

1. 今天哪件事值得进入长期记忆？
2. 哪个人、项目或地点需要补充上下文？
3. 今天有没有一个判断、决定或承诺需要被追踪？

## Diary Draft

今天的日程主要包括上面的时间线。这里还只是事实草稿，需要补充你的主观感受、关键判断和后续动作，才能升级为 confirmed 日记。

---

## Source Snapshot

```text
{pretty_text.strip() or "No pretty agenda output."}
```
"""
    diary_path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
