---
name: pattern-hunter
description: >
  Run McKinsey-style market research on a small business or industry to surface operator pain points,
  gaps, and high-leverage opportunities. Use for: "pattern hunter", "research [business type]",
  "understand [industry] problems", "market research", "operator pain points", "small business audit".
metadata:
  version: 1.2.0
  updated: 2026-06-23
---

# Pattern Hunter

## Overview

Pattern Hunter automates the research phase of small-business consulting by running a four-node
agentic workflow: understand the industry, scrape operator reality from public sources, synthesize
a hypothesis with actionable fixes, then adversarially red-team the output against the operator's
actual fears and risks before surfacing it.

The goal is operator-first research that avoids McKinsey abstraction — every output should be
something a sub-20-person company can act on tomorrow, not a slide deck.

## Core Capabilities

- **Context Parser** — maps the physical and economic reality of an industry (assets, cash flow, local fragmentation, regulatory friction)
- **Pain Point Scraper** — searches Reddit (niche + general subs), association blogs, Glassdoor, and industry forums for recurring operator complaints
- **Hypothesis Engine** — synthesizes findings into a bottleneck hypothesis with targeted interview questions to confirm with the operator
- **Integrator** — converts validated hypotheses into done-for-you assets (templates, scripts, SOP starters) the operator can use immediately
- **Red Team Node** — adversarial review that checks every recommendation against operator fears (asset loss, cash-flow interruption, legal exposure) before delivery

## When to Use

- You want to understand the pain points of a specific trade or "boring business" (HVAC, arborists, trailer rental, waste management, landscaping, etc.)
- You are preparing for a consulting conversation and want operator-specific questions ready
- You need to position a product or service against a company's known weaknesses
- You want to generate a done-for-you asset (quoting form, SOP, asset tracker) for a specific operator
- You are auditing a company's public presence for an identity crisis or positioning gap

## Quick Start

```
/pattern-hunter [business type or company URL]
```

**Examples:**
```
/pattern-hunter trailer rental company
/pattern-hunter solopreneur arborist
/pattern-hunter https://www.onemagnify.com/
```

The skill runs all four nodes in sequence, saves the brief to `EXPORTS/`, ingests it into the
mdrag KB, and upserts a tab in the shared Pattern Hunter GDoc.

### Publish to GDoc + KB manually

```bash
# GDoc tab upsert (PATTERN_HUNTER_DOC_ID already in .env after first --create-doc run)
uv run python .agents/skills/pattern-hunter/scripts/publish_to_gdoc.py \
  --brief-file .agents/skills/pattern-hunter/EXPORTS/<slug>-brief-<date>.md \
  --tab-title "<Operator Name> <YYYY-MM-DD>"

# mdrag KB ingest
uv run python .agents/skills/pattern-hunter/scripts/ingest_to_kb.py \
  --brief-file .agents/skills/pattern-hunter/EXPORTS/<slug>-brief-<date>.md \
  --title "Pattern Hunter Brief: <Operator Name> (<YYYY-MM-DD>)" \
  --operator "<Operator Name>" \
  --url "https://operator-url.com"

# First GDoc run only — create the doc + share with jae@datacrew.space
uv run python .agents/skills/pattern-hunter/scripts/publish_to_gdoc.py \
  --brief-file ... --tab-title "..." --create-doc

# Dry run either script
uv run python .agents/skills/pattern-hunter/scripts/publish_to_gdoc.py \
  --brief-file ... --tab-title "..." --dry-run
uv run python .agents/skills/pattern-hunter/scripts/ingest_to_kb.py \
  --brief-file ... --title "..." --operator "..." --url "..." --dry-run
```

## Detailed Workflow

### Node 1: Context Parser (Understand)

**Goal:** Establish the physical and economic reality of the industry *before* talking to the operator.

Inputs: business type or URL

Instructions:
1. Identify the core asset class (equipment, vehicles, real estate, labor hours)
2. Map the cash-flow model (day-rate rental, project-based, retainer, SaaS)
3. Identify local market fragmentation signals (number of competitors in a 50-mile radius, Yelp/Google Maps density)
4. Flag regulatory friction points (licensing, insurance requirements, environmental rules)
5. Note typical team size and org structure at <20 employees

Output: 1-page industry snapshot with asset map, cash-flow model, fragmentation score

---

### Node 2: Pattern Scraper (Operator Reality)

**Goal:** Surface recurring complaints and bottlenecks from public operator communities.

Sources to search (see `references/source-guide.md` for sub-specific guidance):
- Reddit: `r/sweatystartup`, `r/smallbusiness`, `r/Entrepreneur` + niche subs (e.g. `r/arborists`, `r/WasteManagement`, `r/HVAC`)
- Industry association blogs and forums
- Glassdoor reviews for companies in the niche (employee complaints reveal operational friction)
- Local Facebook groups (search via mdrag web collector)
- Google "site:reddit.com [industry] problems OR frustrations OR nightmare"

Pattern categories to extract:
- **Cash-flow bottlenecks** (late payments, seasonal troughs, upfront capital)
- **Asset utilization gaps** (idle equipment, theft, maintenance cost spikes)
- **Hiring/labor nightmares** (no-shows, certification gaps, turnover)
- **Customer acquisition friction** (word-of-mouth only, no quoting system, pricing opacity)
- **Compliance/insurance exposure** (uninsured drivers, permit gaps)

Output: Top 5-7 operator pain points ranked by frequency and severity, each with 2-3 verbatim quotes as evidence

---

### Node 3: Hypothesis Engine + Integrator

**Goal:** Synthesize pain points into a bottleneck hypothesis, then hand the operator a finished asset — not advice.

Steps:
1. Pick the top 2-3 bottlenecks from Node 2
2. For each, formulate:
   - **Hypothesis:** "The biggest constraint on [operator]'s growth is [X] because [Y evidence]"
   - **Confirmation questions:** 3-5 targeted questions to validate with the operator face-to-face
   - **Done-for-you fix:** A concrete asset they can use immediately (template, script, checklist, form)

Done-for-you asset types:
- Quoting filter (Google Form → Sheet with auto-pricing logic)
- Asset tracking spreadsheet (equipment, maintenance schedule, depreciation)
- Job briefing SOP (pre-job checklist, crew sign-off)
- Upsell script for common add-ons
- Intake form for emergency/rush jobs with premium pricing logic

Output: 2-3 hypothesis cards, each with questions + one ready-to-deploy asset

---

### Node 4: Red Team (Adversarial Review)

**Goal:** Attack every recommendation before delivery. Fear of loss > desire for gain for small operators.

For each hypothesis card from Node 3, the Red Team must challenge:
- **Does this address the operator's primary FEAR?** (asset loss, bankruptcy, lawsuit, employee injury)
- **Does this require time the operator doesn't have?** If yes, simplify or pre-build it
- **Does this assume resources (money, tech skills, staff) the operator lacks?** If yes, strip it out
- **What happens if this advice is wrong?** What's the downside scenario?
- **Is there a compliance or insurance angle we missed?**

Red Team pass criteria — each recommendation must:
- [ ] Be actionable within 48 hours with zero new hires
- [ ] Cost <$200 to implement OR require only tools the operator already uses
- [ ] Address at least one fear, not just one opportunity
- [ ] Have a clear "what to say to the operator" opening line

Output: Red-teamed brief — recommendations that passed, ones that were cut, and the replacement for any that failed

---

### Output Format

Deliver a single **Pattern Hunter Brief** with:

```
# Pattern Hunter Brief: [Business / Operator]
Generated: [date]

## Industry Snapshot (Node 1)
...

## Top Operator Pain Points (Node 2)
...

## Hypothesis Cards (Node 3)
### Hypothesis 1: [Title]
- Bottleneck: ...
- Evidence: ...
- Confirmation Questions: ...
- Done-For-You Asset: ...

### Hypothesis 2: [Title]
...

## Red Team Sign-Off (Node 4)
- Passed: ...
- Cut: ... (replaced by: ...)
- Opening line for operator conversation: "..."
```

Outputs go to `EXPORTS/[operator-slug]-brief-[date].md`.

---

### Node 5: Publish to GDoc + mdrag KB

**Goal:** Persist the red-teamed brief so it's retrievable in future sessions.

Two sinks, always both:

1. **GDoc tab upsert** — one persistent "Pattern Hunter — Prospect Research" doc, one tab per
   operator run (tab title = `"<Operator Name> YYYY-MM-DD"`). Shared with jae@datacrew.space.
   Uses `scripts/publish_to_gdoc.py` via cboti `GoogleDriveService.docs_api.create_tab_with_content`
   with `mode="replace"` so re-runs on the same operator overwrite the stale tab.

2. **mdrag KB ingest** — POST to `https://wiki.datacrew.space/mcp/` with `X-DC-Token` header,
   tool `save_text_to_knowledge`, collection `datacrew`, source_label `pattern_hunter`.

```bash
# 1. GDoc tab (GDOC_CLIENT + GDOC_TOKEN from Infisical /datacrew, homeserver project)
uv run python .agents/skills/pattern-hunter/scripts/publish_to_gdoc.py \
  --brief-file EXPORTS/<slug>-brief-<date>.md \
  --tab-title "<Operator> <YYYY-MM-DD>"

# 2. mdrag KB (DATACREW_API_TOKEN from Infisical /datacrew, homeserver project)
uv run python .agents/skills/pattern-hunter/scripts/ingest_to_kb.py \
  --brief-file EXPORTS/<slug>-brief-<date>.md \
  --title "Pattern Hunter Brief: <Operator Name> (<YYYY-MM-DD>)" \
  --operator "<Operator Name>" \
  --url "https://operator-url.com"
```

**Known gotchas (already handled by the scripts):**
- MCP endpoint is `wiki.datacrew.space/mcp/` (one 'k' — `wikki` 301-redirects and breaks session)
- Auth header is `X-DC-Token`, NOT `Authorization: Bearer` (Cloudflare Access intercepts Bearer)
- `tools/call` requires `Accept: application/json, text/event-stream` or returns `-32600`
- `save_text_to_knowledge` requires both `text` AND `title` — missing `title` returns `-32602`
- `DATACREW_API_TOKEN` is the key name (NOT `DC_TOKEN`), at `/datacrew` path in homeserver Infisical project
- Neo4j `Map{}` error on ingest is a pre-existing mdrag bug — MongoDB ingest succeeds; ignore it
- GDoc creds: `GDOC_CLIENT` + `GDOC_TOKEN` at `/datacrew` path in homeserver Infisical project

### Node 6: Write to Memory Store

**Goal:** Persist industry research as shared context in the shared memory store so all agents can recall it.

Pattern Hunter output is **research**, not customer data. It goes in the shared `reference/` namespace so any agent (DataCrew, IdrisBot) can read it. Real customer information (contact details, pipeline status, outreach strategy) belongs in `agents/datacrew/clients/` — see the customer-dossier skill for that.

After the brief is produced, write (or update) a research file at:

```
/home/jaewilson07/GitHub/datacrew-private-memories/reference/clients/<slug>.md
```

**Format** (YAML frontmatter + structured content):

```markdown
---
description: <Operator Name> — industry research, pain points, and recommended fixes.
---
# <Operator Name> — Pattern Hunter Research

**Generated:** <YYYY-MM-DD>
**Source:** Pattern Hunter run on <business type or URL>
**Full brief:** EXPORTS/<slug>-brief-<date>.md

## Industry Snapshot
<1-2 paragraph summary from Node 1>

## Top Pain Points
<bullet list of top 3-5 pain points from Node 2>

## Hypotheses
<2-3 hypothesis summaries with done-for-you asset references>

## Red Team Notes
<key risks/fears addressed, anything cut and why>

## Links
- GDoc tab: <link if created>
- mdrag KB: <link if ingested>
- [[reference/clients/<slug>]] — this file
```

**Rules:**
- Use kebab-case for the slug (e.g., `blueyeti`, `trailer-rental-co`)
- If a file already exists, **update it** — don't create a duplicate
- Pull before writing and push after (shared repo is collaborative)
- Include `[[path]]` cross-references to related research or reference docs
- This is **shared research** — no real customer contact details, rates, or pipeline status here. Those go in `agents/datacrew/clients/` via the customer-dossier skill.

```bash
# Pull latest, write the file, commit and push
cd /home/jaewilson07/GitHub/datacrew-private-memories
git pull
# ... write/update reference/clients/<slug>.md ...
git add reference/clients/<slug>.md
git commit -m "feat: pattern hunter research for <Operator Name> (<YYYY-MM-DD>)"
git push
```

---

## References

- **[references/source-guide.md](./references/source-guide.md)** — Reddit subs, association sites, and search patterns by industry vertical
- **[scripts/publish_to_gdoc.py](./scripts/publish_to_gdoc.py)** — Upsert brief as GDoc tab via cboti `GoogleDriveService`; reads `GDOC_CLIENT` + `GDOC_TOKEN` from env
- **[scripts/ingest_to_kb.py](./scripts/ingest_to_kb.py)** — Ingest brief into mdrag KB via MCP `save_text_to_knowledge`; reads `DATACREW_API_TOKEN` from env
- **Env var `PATTERN_HUNTER_DOC_ID`** — Google Doc ID of the shared "Pattern Hunter — Prospect Research" doc (set after first `--create-doc` run)
- **Infisical path** — All three vars (`GDOC_CLIENT`, `GDOC_TOKEN`, `DATACREW_API_TOKEN`) at `/datacrew` in homeserver Infisical project (`3fbb4296-d4e6-4c17-83ee-b852a57a5e50`), env `prod`
- **cboti** — `libraries/cboti/src/cboti/integrations/google/drive/google_docs.py` → `create_tab_with_content`

## Related Skills

- `research-and-archive` — deep mdrag search + KB ingest for a topic
- `write-a-prd` — convert a pattern hunter brief into a product PRD
- `verified-analyst` — source-cited research with confidence scores
- `grill-me` — adversarial Q&A to stress-test a hypothesis before an operator meeting
