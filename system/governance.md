---
description: Who can write where, placement test, and privacy rules for the shared memory repo.
---

# Governance

## Write Access

| Directory | DataCrew | IdrisBot | EmmaBot |
|-----------|----------|----------|---------|
| `system/` | Read/Write | Read/Write | Read/Write |
| `reference/` | Read/Write | Read/Write | Read/Write |
| `users/` | Read/Write | Read/Write | Read/Write |
| `agents/datacrew/` | Read/Write | No access | No access |
| `agents/idrisbot/` | No access | Read/Write | No access |
| `agents/emmabot/` | No access | No access | Read/Write |
| `proposals/` | Read/Write | Read/Write | Read/Write |

DataCrew owns shared standards. Each agent owns their `agents/<name>/` directory.

## Placement Test

Before adding anything to `system/`, ask:

1. **Is it durable?** Will this matter across many future conversations?
2. **Is it frequent?** Does it affect behavior often enough to justify always-on tokens?
3. **Is it global?** Is this relevant to all agents, not just one?

If any answer is no, it goes to `reference/` or `agents/<name>/`.

## Privacy Rules

- Privacy is by convention, not encryption
- Each agent's system prompt includes: "Do not read or write to other agents' private directories"
- `.gitignore` excludes: secrets, `.env`, conversation logs, large binaries
- User profiles in `users/` are shared but should not contain private personal information
- **Real customer data** (contact details, pipeline status, outreach strategy, rates) goes in `agents/datacrew/clients/` only — never in shared directories
- **Industry research** (pain points, market analysis, hypotheses, pattern analysis) goes in `reference/clients/` — shared, all agents can read
- IdrisBot is a mentor/product developer — it does not need direct access to real customer data. If IdrisBot needs customer context, it asks DataCrew.

## Commit Conventions

- `feat:` — new content or structure
- `fix:` — correction to existing content
- `docs:` — documentation changes
- `chore:` — maintenance, gitignore, CI
- `refactor:` — reorganization without content change
