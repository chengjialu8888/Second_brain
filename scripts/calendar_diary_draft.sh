#!/usr/bin/env bash
set -euo pipefail

date_arg="${1:-$(date +%F)}"
out_dir="brain/sources/calendar"
diary_dir="brain/diary"
mkdir -p "$out_dir" "$diary_dir"

json_out="$out_dir/${date_arg}.json"
pretty_out="$out_dir/${date_arg}.txt"
diary_out="$diary_dir/${date_arg}.md"

lark-cli calendar +agenda --start "$date_arg" --end "$date_arg" > "$json_out"
lark-cli calendar +agenda --start "$date_arg" --end "$date_arg" --format pretty > "$pretty_out"

python3 scripts/generate_diary_from_agenda.py "$date_arg" "$json_out" "$pretty_out" "$diary_out"

echo "Diary draft written: $diary_out"
