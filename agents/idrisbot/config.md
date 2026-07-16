---
description: IdrisBot-specific configuration, tools, and operating rules.
---

# IdrisBot Configuration

## Environment

- **Agent ID:** agent-0604eb6c-85b1-46f9-9c13-fb147d85bf2a
- **Memory Dir:** `$MEMORY_DIR` (Letta MemFS, private per agent)
- **Shared Repo:** `/home/jaewilson07/GitHub/datacrew-private-memories/`
- **My Section:** `agents/idrisbot/` in the shared repo

## Memory Architecture

- **MemFS (system/):** Live system prompt blocks — persona, operating principles, human preferences. Always in context. Private.
- **Shared repo (this directory):** Durable knowledge that benefits from git history. Read on demand, write when I learn something worth keeping.
- **Conversation search:** Use `conversation_search` for historical details. Do not copy whole transcripts into memory.

## Operating Rules

1. **Pull before working** — `git pull` in the shared repo before reading or writing
2. **Write to my section only** — `agents/idrisbot/` is my space. Shared directories (`system/`, `reference/`, `proposals/`) are collaborative.
3. **Commit with conventional messages** — `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`
4. **Push after writing** — `git push` so other agents can pull my updates
5. **Placement test** — durable? frequent? global? If any no, don't put in `system/`
6. **Frontmatter required** — every file gets a `description` field
7. **Cross-reference with `[[path]]`** — link to other files, don't copy content

## Tools Available

- Web search and fetch (research)
- File read/write/edit (local filesystem)
- Bash (git operations, scripts)
- Memory tools (MemFS management)
- Conversation search (recall past interactions)
- Slack messaging (communication with Jae and other agents)
- Paperclip (project/issue tracking)

## What Lives Where

| Content | Location |
|---------|----------|
| My identity, voice, boundaries | `agents/idrisbot/persona.md` |
| My config and operating rules | `agents/idrisbot/config.md` (this file) |
| Consulting playbooks, engagement framework | `agents/idrisbot/private/` |
| Shared consulting reference | `reference/consulting/` (if I create it) |
| Industry patterns, KPI templates | `reference/patterns/` or `agents/idrisbot/private/` |
| Engagement learnings | `agents/idrisbot/private/engagements/` |
