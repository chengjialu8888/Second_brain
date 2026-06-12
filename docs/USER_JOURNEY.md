# User Journey

Second Brain is designed around a loop: capture, structure, use, improve.

<p align="center">
  <img src="../assets/user-journey.svg" alt="Second Brain user journey from capture to improvement" width="100%">
</p>

## 1. Capture

The user drops in a raw source:

- chat export
- Feishu document
- daily Feishu calendar
- web link
- personal note

The system preserves the source before interpretation.

## 2. Structure

The agent reads:

- `brain/RESOLVER.md`
- `brain/schema.md`
- the relevant skill under `skills/`

Then it creates or updates canonical pages.

## 3. Use

The user asks:

- "What do I need to know before this meeting?"
- "Why did I decide not to start with vector search?"
- "Who has been mentioned repeatedly in this project?"
- "What happened today, and what should I write in my diary?"

The agent searches the brain, reads pages, and returns a synthesized answer with sources and gaps.

## 4. Improve

`wiki_lint` finds:

- broken links
- missing Timeline sections
- duplicate entities
- empty source refs
- diary drafts awaiting subjective context
- open questions worth asking

The brain improves because gaps become prompts for the user.

## Daily Diary Example

```text
lark-cli calendar +agenda
  -> brain/sources/calendar/YYYY-MM-DD.json
  -> brain/sources/calendar/YYYY-MM-DD.txt
  -> brain/diary/YYYY-MM-DD.md
  -> user adds what it meant
  -> entity pages get richer over time
```
