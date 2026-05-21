---
name: create-runbook
description: Creates SOP-style runbooks for recurring tasks with executable scripts. Use for: "create runbook", "turn this into SOP", "standardize recurring task".
metadata:
  version: 2.1.0
  updated: 2026-05-20
---

# create-runbook

Create action-first runbooks with runnable scripts. Link to existing documentation within the same repository, avoiding duplication of content.

## Runbook location

Runbooks live in the **nearest** `.agents/runbooks/` to the package they serve.

| Runbook primarily serves | Store in |
|--------------------------|---------|
| One library (`libraries/mdrag`, `libraries/cboti`, etc.) | `<library>/.agents/runbooks/<verb-noun>/` |
| One app (`datacrew`, `alix`, `indb_discordbot`, etc.) | `<app>/.agents/runbooks/<verb-noun>/` |
| VPS infrastructure | `infrastructure/vps/.agents/runbooks/<verb-noun>/` |
| Multiple packages / monorepo-wide | `.agents/runbooks/<verb-noun>/` (root) |

When in doubt: ask "which package's developers would need to run this?" That package owns it.

## Runbook Structure

```
<package>/.agents/runbooks/<verb-noun>/
├── SKILL.md           ← Minimal docs, crosslinks
├── scripts/
│   └── main.py        ← Executable CLI
├── references/        ← Optional: detailed design/planning guides
├── prompts/           ← Optional: canonical LLM system prompts the scripts call
├── assets/            ← Optional: templates / canonical examples
├── EXPORTS/           ← Optional: disposable output (gitignore)
└── research/          ← Optional: experiment trail that grounds the runbook's rules
    └── <topic>/
        ├── README.md           ← what we were testing + why
        ├── <slug>.brief.yaml   ← input spec (reproducible)
        ├── <slug>_findings.md  ← per-experiment evaluation
        ├── findings-summary.md ← durable knowledge synthesized from all experiments
        ├── reproducibility.md  ← how to re-run; what's disposable vs durable
        └── research-log.md     ← (when topic has active experiment cycles) current state — what's done, queued, blocked; where to pick up cold
```

### One runbook per domain

There should be **one runbook per domain**, not one per sub-feature. If `runbook-A` and `runbook-B` operate on the same domain (same scripts directory, same input/output types, same shared knowledge), they belong as one runbook with multiple commands.

Signs you should merge two runbooks: shared scripts, shared output directory, planning docs in one that apply to the other, agents tend to need to read both to do anything useful.

### Research lives in runbooks

When a runbook's rules come from experiments, those experiments live in `research/<topic>/` inside the runbook itself, not in a separate research tree. This colocates the rule with its evidence and ensures any agent reading the runbook can trace any claim back to a finding doc.

**The rule:** the SKILL.md and references/ contain the durable rules; research/ contains the trail that produced them. A finding doc earns its rule a line in the planning guide / SKILL.md. When a finding is superseded, mark the old finding doc archived but keep it — the audit trail is part of the runbook.

#### Hierarchy of authority

Every agent-facing rule should be traceable to its grounding artifact:

```
SKILL.md / references/<guide>.md    (agent-facing rules)
    ↓ cites
research/<topic>/findings-summary.md   (durable synthesis with citations)
    ↓ cites
research/<topic>/<artifact>            (per-experiment evidence: briefs, findings, source notes)
```

A rule should never appear in the agent-facing docs unless `findings-summary.md` says so. A `findings-summary.md` entry should never appear without citing the per-experiment artifact that grounds it. The runbook gets stronger every time someone runs an experiment and the chain extends.

#### A "topic" is the unit of organization inside research/

A topic is a coherent body of investigation — typically ≥2 distinct experiments, or a focused web-research lane. Each topic gets its own folder with these files:

| File | Required? | Purpose |
|---|---|---|
| `README.md` | always | topic intro + file map + cross-topic relationships |
| `findings-summary.md` | always | durable synthesis with citations back to per-experiment artifacts |
| `reproducibility.md` | always | how to re-run, what's disposable vs durable, agent-dispatch prompts if web-search-based |
| `research-log.md` | when topic has an active experiment cycle | current state — done / queued / blocked, where to pick up cold, chronological log |
| `<NN>_<slug>.brief.yaml` | per experiment | input spec (re-runnable) |
| `<NN>_<slug>_findings.md` | per experiment | per-run evaluation + lessons |

The numeric prefix on per-experiment files sorts them in run order. Variants of a single experiment add a letter (`02_x`, `02b_x`, `02c_x`).

#### Cross-topic relationships

Topics sometimes share boundaries. When findings in one topic revise a rule from another:

1. The revising rule **explicitly cites the rule it's superseding**
2. The original `findings-summary.md` adds a forward-pointer ("see [other-topic] §rule X for the 2026-MM-DD revision")
3. Don't silently overwrite — the audit trail matters more than tidiness

#### Worked example to copy from

See `alix/.agents/runbooks/image-generation/research/` for the canonical implementation: four topics (`identity-fidelity`, `creativity`, `pose-library`, `thirst-trap`), each with the canonical file set, with cross-topic citations between them and an agent-facing planning guide that cites the findings.

### EXPORTS is disposable; reproducibility lives in briefs + findings

`EXPORTS/` holds rendered/generated output that takes compute to produce (images, video clips, audio, expensive query results). It is gitignored.

What survives a `rm -rf EXPORTS/`:
- The **brief** (YAML/JSON input spec) — committed under `research/<topic>/`. Re-running the script with the same brief reproduces the output deterministically (or close to it, modulo seed).
- The **findings doc** — what we learned from looking at the output. The conclusion outlives the artifact.
- The **manifest** — auto-generated record of `(brief, output_path, params)` per run; may live in EXPORTS but is reproducible from the brief.

What does NOT survive:
- The PNGs, audio files, large JSON dumps. Don't commit these. If a specific output is important enough to keep, promote it out of EXPORTS to a non-gitignored `assets/` or `research/<topic>/golden/` location.

Add an `EXPORTS/.gitignore` or contribute to root `.gitignore` per runbook.

## Templates

See: `assets/templates/runbook-skeleton.md`

## Rules

Rules are listed in priority order; when conflicts arise, rules earlier in the list take precedence.

- **Verb-first naming**: `sync-models`, `launch-ssh`, not `model-sync-guide`
- **One runbook per domain**: don't fragment into per-feature runbooks. If two runbooks share scripts, share an output dir, or agents have to read both to be useful, merge them. See `## Runbook Structure → One runbook per domain` above.
- **Script-backed**: Every step runs via script. If a step cannot be automated, provide detailed manual instructions in the SKILL.md file instead.
- **Crosslink**: Link to existing docs within the same repository, don't copy
- **Minimal markdown**: Use minimal markdown in the SKILL.md file: focus on commands and avoid explanatory prose.
- **API-first**: Scripts call FastAPI REST routes or FastMCP endpoints — never import library internals.
  See: `.agents/skills/microservices-api-first/SKILL.md` for the thin-script pattern.
  If the service doesn't exist yet, document the missing service, provide a placeholder script with a clear TODO comment, and add a `⚠️ temporary` note in the runbook.
- **Research lives in the runbook**: if the runbook's rules come from experiments, put the experiments under `research/<topic>/` inside the runbook (briefs + findings docs). Synthesize the durable knowledge into a `findings-summary.md` and reflect the rules in `references/` or the SKILL.md itself. Don't park experiments in a parallel research tree.
- **EXPORTS is disposable**: any generated output (images, audio, large data dumps) goes in `EXPORTS/` and is gitignored. Reproducibility comes from the brief that produced it plus the findings doc that captured what we learned — not from the artifact.

## FastAPI vs FastMCP (quick rule)

| Script triggers a | Use |
|---|---|
| Deterministic workflow / CRUD | **FastAPI** `POST http://localhost:{PORT}/v1/{route}` |
| Letta agent tool invocation | **FastMCP** tool call |

## Related Skills

- `microservices-api-first` — Thin-script pattern, port registry, FastAPI vs FastMCP decision table
- `refresh-documentation` — Update docs after changes
- `creating-skill` — Create new skills
- `review-documentation` — Read-before/write-after conventions
- `create-chronjob` — Document scheduled maintenance jobs with runbook-backed recovery
- `.agents/plans/microservices-architecture/PLAN.md` — Authoritative design principles
