#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: scripts/extract_links.sh <file>" >&2
  exit 2
fi

file="$1"
if [[ ! -f "$file" ]]; then
  echo "File not found: $file" >&2
  exit 1
fi

if command -v rg >/dev/null 2>&1; then
  rg -o 'https?://[^ )>\]]+' "$file" | sed 's/[`"'"'"'),.;]*$//' | sort -u
else
  grep -Eo 'https?://[^ )>\]]+' "$file" | sed 's/[`"'"'"'),.;]*$//' | sort -u
fi
