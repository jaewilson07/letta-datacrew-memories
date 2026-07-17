# datacrew-private-memories

Shared durable knowledge store for DataCrew agents. See [[README]] for the full standard and [[system/governance]] for write access rules.

## What This Repo Is

A git-versioned knowledge store shared across DataCrew agents. Complements each agent's MemFS (live system prompt blocks) with durable knowledge that benefits from history, collaboration, and curation.

## Structure

```
datacrew-private-memories/
├── system/                          ← Shared, always-pinned (all agents read)
│   ├── index.md                     ← Memory routing map
│   ├── governance.md                ← Who can write where, placement test
│   └── platform/                    ← Shared platform knowledge (infra, Letta)
├── reference/                       ← Shared, on-demand (all agents can read)
│   ├── index.md
│   ├── clients/                     ← Industry research, pain points, pattern analysis
│   ├── domo/                        ← Domo API patterns, crew-dcs templates
│   ├── patterns/                    ← Generalized lessons, second brain research
│   └── project/                     ← Project-specific reference docs
├── users/                           ← DUG community member profiles (shared)
├── agents/                          ← Per-agent private namespace
│   ├── datacrew/                    ← DataCrew agent (agent-55e609e7)
│   │   └── clients/                 ← Real customer data (private — contact, pipeline, outreach)
│   ├── idrisbot/                    ← IdrisBot agent (agent-0604eb6c)
│   └── emmabot/                     ← EmmaBot agent (agent-5afcfa48)
├── proposals/                       ← Feature proposals (shared)
├── archives/                        ← Archived content (by month)
├── datacrew-public/                 ← Legacy EmmaBot workspace (to be migrated)
├── .agents/                         ← Skills, runbooks (gitignored)
└── .gitignore
```

## Privacy Rules

- **Shared** (`system/`, `reference/`, `users/`, `proposals/`): All agents read/write
- **Private** (`agents/<name>/`): Only the named agent reads/writes. Do NOT read other agents' private directories.
- See [[system/governance]] for the full rules.

## File Format

All memory files use markdown with YAML frontmatter:
- `description` field required (drives discovery)
- `[[path/to/file]]` cross-references
- `kebab-case` for topics, `camelCase` for user profiles
- `index.md` in every directory with 3+ files

## Placement Test

Before adding to `system/`, ask: Is it durable? Is it frequent? Is it global?
If any answer is no, it goes to `reference/` or `agents/<name>/`.

## Existing Infrastructure

### .agents/ (gitignored)
- `skills/` — Reusable agent skills (create-skill, sync-memory, etc.)
- `runbooks/` — SOP-style runbooks with executable scripts
- `env_loader.py` — Environment variable loader

### datacrew-public/ (legacy)
EmmaBot's existing workspace. Content should be migrated to the new structure:
- `memories/reference/` → `reference/` (shared)
- `memories/users/` → `users/` (shared)
- `memories/system/persona/` → `agents/emmabot/system/` (private)
- `articles/` → `agents/emmabot/articles/` (private)
- `query_domo_docs.py` / `sync_domo_docs.py` — utilities (stay in place)

### Memory Sync
Existing sync infrastructure (`.agents/runbooks/sync-memory-stores/`) syncs to git and Domo fileset. This should be updated to sync the new structure.

## Hard Rules

1. **Never share private information** — no client names, rates, pipeline details, or financial data in shared directories
2. **Use mdrag for research** — don't fall back to generic web search when mdrag has the capability
3. **Check skills before implementing** — always look in `.agents/skills/` first
4. **Fail hard, fail loud** — never swallow exceptions or gracefully skip errors
5. **No `TYPE_CHECKING`** — refactor for separation of concerns instead
6. **No naked `except`** — always catch specific exceptions
7. **Use `uv`** — never `pip`
8. **Config in `config.yaml`** — `.env`/Infisical for secrets only
9. **Never use standard `logging`** — use `async ColoredLogger` from `utils.logging`
