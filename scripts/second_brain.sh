#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

cmd="${1:-help}"
shift || true

usage() {
  cat <<'EOF'
Second Brain skill-style entry

Usage:
  scripts/second_brain.sh help
  scripts/second_brain.sh prompt
  scripts/second_brain.sh search "query"
  scripts/second_brain.sh workspace "query" [--from YYYY-MM-DD --to YYYY-MM-DD]
  scripts/second_brain.sh strategy-report "topic" --from YYYY-MM-DD --to YYYY-MM-DD
  scripts/second_brain.sh agents ["query"]
  scripts/second_brain.sh dashboard
  scripts/second_brain.sh lint
  scripts/second_brain.sh diary [YYYY-MM-DD|today]
  scripts/second_brain.sh links <file>
  scripts/second_brain.sh feishu <url>

Core files for agents:
  AGENTS.md
  SKILL.md
  brain/RESOLVER.md
  brain/schema.md
  skills/RESOLVER.md
EOF
}

case "$cmd" in
  help|-h|--help)
    usage
    ;;
  prompt)
    cat <<'EOF'
Use this repository as the $second-brain skill.
Read AGENTS.md, SKILL.md, brain/RESOLVER.md, brain/schema.md, and skills/RESOLVER.md.
When output needs a specialist lens, also read skills/agency-agent-routing.md and use agents/agency-agents/ after searching Second Brain evidence.
For accurate, comprehensive, date-bounded synthesis, create an active workspace before the final deliverable.
Then help me capture, ingest, search, think, compose workspaces, lint, route specialist agents, or generate diary drafts without committing private source data.
EOF
    ;;
  search)
    if [[ $# -lt 1 ]]; then
      echo "Usage: scripts/second_brain.sh search \"query\"" >&2
      exit 2
    fi
    python3 scripts/brain_search.py "$*"
    ;;
  agents)
    python3 scripts/agency_agent_search.py "$@"
    ;;
  workspace)
    if [[ $# -lt 1 ]]; then
      echo "Usage: scripts/second_brain.sh workspace \"query\" [--from YYYY-MM-DD --to YYYY-MM-DD]" >&2
      exit 2
    fi
    python3 scripts/workspace_compose.py "$@"
    ;;
  strategy-report)
    if [[ $# -lt 1 ]]; then
      echo "Usage: scripts/second_brain.sh strategy-report \"topic\" --from YYYY-MM-DD --to YYYY-MM-DD" >&2
      exit 2
    fi
    python3 scripts/workspace_compose.py --mode strategy-report "$@"
    ;;
  dashboard)
    cat <<'EOF'
Open these in Obsidian:
  brain/dashboards/home.md
  brain/workspace/README.md
  brain/dashboards/open-questions.md
  brain/dashboards/review-queue.md
  brain/dashboards/recent-changes.md

Guide:
  docs/OBSIDIAN.md
EOF
    ;;
  lint)
    python3 scripts/wiki_lint.py
    ;;
  diary)
    date_arg="${1:-today}"
    if [[ "$date_arg" == "today" ]]; then
      date_arg="$(date +%F)"
    fi
    scripts/calendar_diary_draft.sh "$date_arg"
    ;;
  links)
    if [[ $# -lt 1 ]]; then
      echo "Usage: scripts/second_brain.sh links <file>" >&2
      exit 2
    fi
    scripts/extract_links.sh "$1"
    ;;
  feishu)
    if [[ $# -lt 1 ]]; then
      echo "Usage: scripts/second_brain.sh feishu <url>" >&2
      exit 2
    fi
    scripts/fetch_feishu_doc.sh "$1"
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    usage >&2
    exit 2
    ;;
esac
