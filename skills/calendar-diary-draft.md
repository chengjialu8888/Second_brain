---
name: calendar-diary-draft
mutating: true
writes_pages: true
writes_to:
  - brain/sources/calendar/
  - brain/diary/
---

# Calendar Diary Draft

## Contract

Use Feishu calendar as factual scaffolding for a daily diary draft. The output remains `status: draft` until the user adds subjective context.

## Prerequisite

The user must authorize:

```bash
lark-cli auth login --scope "calendar:calendar.event:read"
```

## Command

```bash
scripts/calendar_diary_draft.sh YYYY-MM-DD
```

## Phases

1. Fetch daily agenda with `lark-cli calendar +agenda`.
2. Save raw JSON and pretty agenda under `brain/sources/calendar/`.
3. Generate `brain/diary/YYYY-MM-DD.md`.
4. Add questions for user reflection.
5. Later, use lint/enrichment to update people, projects, and places.

## Anti-Patterns

- Do not pretend calendar facts are feelings.
- Do not mark diary as confirmed without user input.
- Do not ingest private calendar data into public artifacts.
