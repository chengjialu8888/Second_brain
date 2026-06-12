#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: scripts/fetch_feishu_doc.sh <feishu-doc-or-wiki-url> [output-dir]" >&2
  exit 2
fi

url="$1"
out_dir="${2:-brain/sources/feishu-docs}"
mkdir -p "$out_dir"

stamp="$(date +%Y%m%d-%H%M%S)"
slug="$(printf '%s' "$url" | sed -E 's#https?://##; s#[^A-Za-z0-9._-]+#-#g; s#-+$##' | cut -c1-80)"
base="$out_dir/${stamp}-${slug}"

lark-cli docs +fetch --api-version v2 --doc "$url" --scope outline --max-depth 3 --detail with-ids > "${base}.outline.json"
lark-cli docs +fetch --api-version v2 --doc "$url" --doc-format markdown > "${base}.md.json"

echo "Saved:"
echo "- ${base}.outline.json"
echo "- ${base}.md.json"
