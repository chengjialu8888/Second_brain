#!/usr/bin/env python3
"""Search the installed Agency Agents roster."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "agents" / "agency-agents" / "roster.json"


def tokenize(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.lower())


def score_agent(agent: dict[str, str], terms: list[str]) -> int:
    haystacks = {
        "name": agent.get("name", ""),
        "id": agent.get("id", ""),
        "division": agent.get("division", ""),
        "description": agent.get("description", ""),
        "vibe": agent.get("vibe", ""),
    }
    score = 0
    for term in terms:
        for field, value in haystacks.items():
            value_l = value.lower()
            if term not in value_l:
                continue
            score += {
                "name": 8,
                "id": 7,
                "division": 5,
                "description": 3,
                "vibe": 2,
            }[field]
    return score


def load_roster() -> dict:
    if not ROSTER.exists():
        raise SystemExit(f"Missing roster: {ROSTER}")
    return json.loads(ROSTER.read_text(encoding="utf-8"))


def print_agent(agent: dict[str, str]) -> None:
    print(f"{agent['id']}  [{agent['division']}]")
    print(f"  name: {agent['name']}")
    if agent.get("description"):
        print(f"  desc: {agent['description']}")
    if agent.get("vibe"):
        print(f"  vibe: {agent['vibe']}")
    print(f"  file: {agent['source_path']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="Search terms, such as product strategy or Feishu integration")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of matches to print")
    parser.add_argument("--division", help="Restrict results to one division")
    args = parser.parse_args()

    data = load_roster()
    agents = data["agents"]
    if args.division:
        agents = [a for a in agents if a["division"] == args.division]

    query = " ".join(args.query).strip()
    if not query:
        divisions: dict[str, int] = {}
        for agent in agents:
            divisions[agent["division"]] = divisions.get(agent["division"], 0) + 1
        print(f"{len(agents)} installed Agency Agents")
        for division, count in sorted(divisions.items()):
            print(f"- {division}: {count}")
        print("\nUsage: scripts/second_brain.sh agents \"product strategy\"")
        return 0

    terms = tokenize(query)
    ranked = [(score_agent(agent, terms), agent) for agent in agents]
    ranked = [(score, agent) for score, agent in ranked if score > 0]
    ranked.sort(key=lambda item: (-item[0], item[1]["division"], item[1]["id"]))

    if not ranked:
        print(f"No Agency Agent matches for: {query}")
        return 1

    for index, (score, agent) in enumerate(ranked[: args.limit], start=1):
        print(f"{index}. score={score}")
        print_agent(agent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
