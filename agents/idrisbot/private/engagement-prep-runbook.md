# Engagement Prep Runbook

**Version:** 1.1
**Purpose:** Define the repeatable process an analyst (or agent) follows to prepare research artifacts for a consulting engagement. The output is a set of support artifacts that an agent uses to guide customer onboarding and assessment. All artifacts are persisted to the mdrag knowledge base for cross-session retrieval.

---

## Overview

Every consulting engagement starts with prep. This runbook defines the five steps that produce structured research artifacts before the first client conversation. The process is repeatable across industries and companies.

```
Industry Assessment → Company Assessment → Industry Pattern Hunter → Company Pattern Hunter → Synthesis
       (Step 1)              (Step 2)              (Step 3)               (Step 4)          (Step 5)
                                                                                              │
                                                                                              ▼
                                                                              Engagement Prep Artifacts
                                                                              (interview guide, worry matrix,
                                                                               hypotheses, wedge, KPI matrix,
                                                                               stakeholder questions)
```

**Inputs:**
- Industry name (e.g., "aerospace-defense supply chain distribution")
- Company name or URL (e.g., "Blue Raven Solutions" or "blueravencorp.com")

**Total time:** 2-4 hours for a new industry. 30-60 minutes for a cached industry (skip Step 1, load cached research).

---

## mdrag Integration

All artifacts produced by this runbook are persisted to the mdrag knowledge base (KB) in the `datacrew` collection. This ensures:
- **Cross-session retrieval** — any agent session can query prior research via RAG
- **Compounding knowledge** — each engagement enriches the KB for the next
- **Source persistence** — crawled URLs are ingested into the KB, not just archived to disk

### mdrag API Reference

**Base URL:** `https://wiki.datacrew.space`
**Auth:** `Authorization: Bearer $DATACREW_API_TOKEN` (dc_ JWT, available in environment)
**Collection:** `datacrew` (collection_id: `6a274087d4b0a3ad1b028ae8`)

**Key endpoints (REST):**

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/searxng/search` | Web search via SearXNG |
| POST | `/api/v1/crawl/url` | Crawl a single URL → markdown |
| POST | `/api/v1/ingest/web` | Ingest a URL into the KB (crawl + chunk + embed) |
| POST | `/api/v1/ingest/text` | Save text directly to the KB |
| POST | `/api/v1/query/` | RAG query against the KB |
| GET | `/api/v1/collections/` | List collections |
| GET | `/api/v1/health` | Health check |

**Required headers for all calls:**
- `Authorization: Bearer $DATACREW_API_TOKEN`
- `Content-Type: application/json` (for POST)
- Use `--location-trusted` with curl (endpoints 307-redirect to trailing slash)

### mdrag Operations Per Step

| Step | mdrag Operation | What Gets Saved |
|------|----------------|-----------------|
| Step 1 | `POST /api/v1/ingest/text` | IndustryResearch artifact (markdown) |
| Step 1 | `POST /api/v1/ingest/web` | Source URLs crawled during research |
| Step 2 | `POST /api/v1/ingest/text` | CompanyDossier artifact (markdown) |
| Step 3 | `POST /api/v1/ingest/text` | IndustryPatterns artifact (markdown) |
| Step 4 | `POST /api/v1/ingest/text` | CompanyPatterns artifact (markdown) |
| Step 5 | `POST /api/v1/ingest/text` | EngagementPrep artifact (markdown) |
| Any step | `POST /api/v1/query/` | Query prior research in the KB |
| Feedback | `POST /api/v1/ingest/text` | Interview findings, updated hypotheses |

### Saving artifacts to mdrag

```bash
# Save a text artifact to the datacrew collection
curl -sS --location-trusted -H "Authorization: Bearer $DATACREW_API_TOKEN" \
  -H "Content-Type: application/json" -X POST \
  "https://wiki.datacrew.space/api/v1/ingest/text" \
  -d '{
    "content": "<markdown content of the artifact>",
    "title": "<descriptive title>",
    "source_type": "text",
    "collection_id": "6a274087d4b0a3ad1b028ae8"
  }'
```

### Ingesting source URLs to mdrag

```bash
# Ingest a crawled URL into the datacrew collection
curl -sS --location-trusted -H "Authorization: Bearer $DATACREW_API_TOKEN" \
  -H "Content-Type: application/json" -X POST \
  "https://wiki.datacrew.space/api/v1/ingest/web" \
  -d '{
    "url": "<source URL>",
    "source_type": "web",
    "source_group": "datacrew"
  }'
```

### Querying the KB for prior research

```bash
# RAG query against the datacrew collection
curl -sS --location-trusted -H "Authorization: Bearer $DATACREW_API_TOKEN" \
  -H "Content-Type: application/json" -X POST \
  "https://wiki.datacrew.space/api/v1/query/" \
  -d '{
    "query": "<natural language question>",
    "source_group": "datacrew",
    "match_count": 5
  }'
```

> **Note:** RAG query results may have indexing lag right after ingest. If a query returns "I don't know" right after saving, wait 30-60 seconds and retry. For immediate synthesis, work from the file on disk.

---

## Step 1: Industry Assessment

**Goal:** Understand the industry — what it is, how it works, what KPIs matter, what benchmarks exist, what trends are shaping it.

**What this is:** Broad, McKinsey-style industry research. Descriptive, not analytical. "What" not "so what."

**How to run:**
1. Check if cached research exists at `/projects/industry-analysis/{industry}/industry_research.md`
2. If cached and <6 months old, load it and skip to Step 2
3. **Query the mdrag KB** for prior industry research: `POST /api/v1/query/` with `"query": "{industry} industry research KPIs benchmarks", "source_group": "datacrew"` — if relevant results exist, use them to supplement cached research
4. If not cached, run the `/industry-analysis` skill (10 source category searches, synthesize into IndustryResearch artifact)
5. Write to disk: `/projects/industry-analysis/{industry}/industry_research.json` + `.md`
6. Copy to shared memory repo: `agents/idrisbot/private/{industry}-industry-research.md`
7. **Save to mdrag KB:** `POST /api/v1/ingest/text` with the IndustryResearch markdown, title `"Industry Research: {industry}"`, `collection_id: "6a274087d4b0a3ad1b028ae8"`
8. **Ingest source URLs to mdrag:** For each key source URL used in the research, `POST /api/v1/ingest/web` with `source_group: "datacrew"` — this makes the original source content searchable in the KB

**Output: IndustryResearch artifact**
- Industry overview (market size, structure, key segments, industry structure)
- Top 10 problems (ranked, with evidence sources)
- Key KPIs (with definitions, benchmarks, SCOR/APQC references, data sources, leading/lagging, priority)
- Industry trends (with implications for operators/distributors)
- Benchmark sources (ranked by usefulness, with access notes)
- Data source mapping template (what systems to ask about)
- KPI feasibility matrix template (blank, to be populated in Step 5)

**Storage:**
- Disk: `/projects/industry-analysis/{industry}/`
- Shared: `agents/idrisbot/private/{industry}-industry-research.md`
- KB: mdrag `datacrew` collection (artifact + source URLs)

**Reuse:** Cached per industry. Multiple companies in the same industry share the same research. Refresh when >6 months old or when major industry shifts occur.

---

## Step 2: Company Assessment

**Goal:** Understand the company — what they do, who the key people are, what systems they use, what their business model is, what their financial position is.

**What this is:** Company-specific research. Descriptive — "what" not "so what." The existing customer dossier workflow, extended with data infrastructure.

**How to run:**
1. Check if a dossier exists at `agents/datacrew/clients/{slug}/`
2. If it exists, load it and verify it's current (check `last_synced` date in frontmatter)
3. **Query the mdrag KB** for prior company research: `POST /api/v1/query/` with `"query": "{company name} company profile dossier", "source_group": "datacrew"`
4. If not, research the company (web search, LinkedIn, Crunchbase, PitchBook, company website)
5. Extend the dossier with a **Data Infrastructure Map** (see below) — this is new and critical
6. **Save to mdrag KB:** `POST /api/v1/ingest/text` with the CompanyDossier markdown, title `"Company Dossier: {company name}"`, `collection_id: "6a274087d4b0a3ad1b028ae8"`

**Output: CompanyDossier artifact**
- Company profile (legal name, website, industry, founded, HQ, employees, ownership, revenue)
- Business model (how they make money, what services they provide, key differentiators)
- Leadership team (names, titles, backgrounds, career trajectories)
- Key contacts (name, title, email, LinkedIn, background, credentials, likely priorities)
- Funding and financial position (funding rounds, investors, revenue estimates, financial health signals)
- Customers and markets
- Competitive landscape
- **Data Infrastructure Map** (NEW):
  - ERP/financial system (what system, what data it holds, export format, API availability)
  - CRM (what system, what data)
  - Inventory management system
  - BI/analytics tools (Domo, Power BI, Tableau, etc.)
  - Proprietary platforms (e.g., SEDNA at Blue Raven)
  - Data warehouse / data lake
  - Spreadsheets (what's in Excel that should be in a system)
  - Manual vs. automated data entry
  - Domo connectivity (native connector, API, file export, manual upload)
- Consulting opportunity assessment (why this company is a target, positioning, risk factors)

**Storage:**
- Shared: `agents/datacrew/clients/{slug}/company-contact-dossier/`
- Synced: GDoc dossier (via `.sync/` directory)

**Reuse:** Per-company. Not reusable across companies. Update after each engagement phase.

---

## Step 3: Industry Pattern Hunter

**Goal:** Find recurring patterns across the industry. What problems do companies in this industry consistently face? What structural issues exist? What KPI gaps are common? What benchmarks can we use for positioning?

**What this is:** Industry-level pattern recognition. Analytical — "so what" at the industry level. Takes the IndustryResearch artifact and asks: "What patterns are actionable for a consulting engagement?"

**This is NOT the existing pattern hunter runbook.** The existing runbook (`/pattern-hunter`) audits a single company's public presence for positioning gaps — that's a competitive positioning audit. This step finds patterns ACROSS the industry, not within a single company.

**How to run:**
1. Load the IndustryResearch artifact from Step 1
2. **Query the mdrag KB** for additional industry context: `POST /api/v1/query/` with `"query": "{industry} recurring problems patterns KPI gaps", "source_group": "datacrew"` — this may surface prior research from other engagements in the same industry
3. For each of the top 10 problems, ask:
   - Is this a structural problem (inherent to the industry) or a company-specific problem?
   - How common is this problem across companies in the industry? (universal, majority, niche)
   - What's the cost of NOT solving this problem? (dollar impact, risk exposure, opportunity cost)
   - What's the typical workaround? (spreadsheets, manual processes, gut feel, ignoring it)
   - Can we benchmark this? (do we have industry median / top quartile numbers?)
3. For each KPI, ask:
   - Do most companies in this industry track this? (universal, common, rare)
   - If they don't track it, what's the cost of not tracking it?
   - What data source is needed? Is it typically available in this industry?
   - Can we say "you're at X, industry median is Y"?
4. Identify industry-specific patterns:
   - Common KPI gaps (what most companies don't track but should)
   - Typical data infrastructure maturity (what systems they typically have vs. lack)
   - Regulatory/compliance patterns (what requirements shape the industry)
   - Competitive dynamics (consolidation, fragmentation, disruption)
   - Technology adoption patterns (what tools are standard, what's emerging)

**Output: IndustryPatterns artifact**
- Recurring problem patterns (ranked by frequency × severity × actionability)
  - Each with: problem, scope (universal/majority/niche), typical workaround, cost of inaction, benchmark availability
- Common KPI gaps
  - Each with: KPI, how many companies track it, cost of not tracking, data source typically available, benchmark available
- Industry structural patterns
  - Regulatory, competitive, technological, workforce
- Benchmark opportunities
  - Where can we say "you're at X, industry median is Y, top quartile is Z"
  - Source for each benchmark
- Industry-specific forcing questions (generic, to be tailored in Step 5)
  - Questions that work for any company in this industry
  - Ranked by which questions most reliably surface pain

**Storage:**
- Disk: `/projects/industry-analysis/{industry}/patterns.md`
- Shared: `agents/idrisbot/private/{industry}-industry-patterns.md`
- KB: mdrag `datacrew` collection — save via `POST /api/v1/ingest/text` with title `"Industry Patterns: {industry}"`, `collection_id: "6a274087d4b0a3ad1b028ae8"`

**Reuse:** Cached per industry alongside the IndustryResearch artifact. Update when industry research is refreshed.

---

## Step 4: Company Pattern Hunter

**Goal:** Find company-specific signals and patterns. What does this company's public footprint reveal about what they're worried about RIGHT NOW? What signals indicate their current priorities, constraints, and concerns?

**What this is:** Company-specific pattern recognition. Analytical — "so what" at the company level. Takes the CompanyDossier and asks: "What signals indicate current concerns, and what patterns does this company's profile reveal?"

**This is NOT the existing pattern hunter runbook.** The existing runbook audits a company's marketing/positioning. This step reads the company's signals for consulting engagement prep.

**How to run:**
1. Load the CompanyDossier from Step 2
2. **Query the mdrag KB** for prior company signals: `POST /api/v1/query/` with `"query": "{company name} recent news signals hiring leadership", "source_group": "datacrew"`
3. Search for recent company news (last 6 months):
   - Contract wins/losses
   - Leadership changes
   - Hiring patterns (what roles are they posting? what does that signal?)
   - Funding/investment news
   - M&A activity
   - Earnings calls or investor presentations (if public or PE-backed)
   - Regulatory actions or compliance news
3. Analyze the leadership team's backgrounds:
   - Where did they come from? (signals what they know and what they value)
   - What did they do at previous companies? (signals what they'll try to replicate)
   - How long have they been in role? (signals tenure, stability, urgency)
   - What's their functional background? (CFO vs. COO vs. CTO — different priorities)
4. Analyze the business stage:
   - Growth mode? (scaling, hiring, expanding)
   - Integration mode? (post-acquisition, consolidating systems)
   - Optimization mode? (cutting costs, improving margins)
   - Preparation mode? (getting ready for sale, audit, contract renewal)
   - What signals support this assessment?
5. Analyze the tech stack signals:
   - What systems do they use? (signals data maturity)
   - What's missing? (signals gaps)
   - What's proprietary vs. off-the-shelf? (signals build vs. buy orientation)
   - What does David C.'s Domo experience at AAR signal? (signals they have in-house Domo expertise)
6. Identify gaps in their public footprint:
   - What would you expect to see but don't? (e.g., no case studies, no pricing, no team page)
   - What does the absence signal?

**Output: CompanyPatterns artifact**
- Recent signals (last 6 months)
  - Each with: signal, source, interpretation, confidence (high/medium/low)
- Leadership signals
  - Each with: person, background signal, what it means for the engagement
- Business stage assessment
  - Stage (growth/integration/optimization/preparation)
  - Evidence supporting this assessment
  - What this stage means for the engagement (what they'll be receptive to)
- Tech stack signals
  - What data they likely have
  - What data they likely lack
  - What Domo connectivity is likely available
  - What the data infrastructure gaps are
- Identified gaps in public footprint
  - What's missing and what it signals
- Contact-specific signals
  - The key contact's background, career trajectory, likely priorities
  - What would make them look good / what would make them look bad
  - What language they speak (financial, operational, technical)

**Storage:**
- Shared: `agents/datacrew/clients/{slug}/patterns.md`
- Synced: GDoc dossier (if synced)
- KB: mdrag `datacrew` collection — save via `POST /api/v1/ingest/text` with title `"Company Patterns: {company name}"`, `collection_id: "6a274087d4b0a3ad1b028ae8"`

**Reuse:** Per-company. Not reusable. Update after each engagement phase.

---

## Step 5: Synthesis

**Goal:** Combine all four artifacts into engagement prep artifacts that an agent uses to guide customer onboarding and assessment.

**What this is:** The synthesis step. Takes IndustryResearch (Step 1) + CompanyDossier (Step 2) + IndustryPatterns (Step 3) + CompanyPatterns (Step 4) and produces actionable engagement prep.

**How to run:**
1. Load all four artifacts
2. **Query the mdrag KB** for relevant prior engagement preps: `POST /api/v1/query/` with `"query": "{company name} OR {industry} engagement prep hypotheses worry matrix", "source_group": "datacrew"` — prior preps may surface patterns or hypotheses relevant to this engagement
3. Build the **Worry Matrix**:
   - For each industry problem (from Step 3), cross with company specifics (from Steps 2 and 4)
   - Ask: "Does this company's profile (size, stage, tech stack, leadership, business model) make this problem more or less likely to be acute for them?"
   - Score each: likelihood (high/medium/low) × impact (high/medium/low) = priority
   - Rank by priority
   - For each high-priority worry, write the evidence chain: industry problem → company amplifier → why this person specifically cares
3. Build **Pre-Interview Hypotheses** (not post-interview premises):
   - For each top worry, write a falsifiable hypothesis: "I think X is true about this company"
   - Each hypothesis has: the claim, the evidence basis, what would confirm it, what would disconfirm it, when to test it in the interview
   - These are tested DURING the interview, not after. If confirmed, go deep. If disconfirmed, pivot.
4. Build **Tailored Forcing Questions**:
   - For each top worry, write a question that's specific to this company (not generic)
   - Stakeholder-specific: CFO questions, ops person questions, IT/data person questions
   - Each question should surface the worry in <2 minutes of conversation
5. Build **The Wedge**:
   - The smallest concrete thing that would demonstrate value
   - What can we deliver in 48 hours that would make them say "I'd use this every day"?
   - What data do we need from them to build it?
   - What's the effort (S/M/L)?
6. Build **KPI Feasibility Matrix** (pre-populated):
   - For each candidate KPI, pre-populate what we know from the dossier:
     - Data source: what we THINK they have (from tech stack signals)
     - Format: what we THINK the format is
     - Quality: what we THINK the quality is
     - Domo connectivity: what we THINK Domo can connect to
   - Mark unknowns with "?" — these are questions for the interview
   - The interview fills in the "?"s, not the entire matrix
7. Build **The Interview Guide**:
   - 6-stage Discovery flow (Context → Status Quo → Data Source Mapping → Gap → Priority → Future-Fit)
   - STOP gates after each stage
   - Pre-interview hypotheses woven into the questions (test early, pivot if wrong)
   - Stakeholder-specific question sets (CFO, ops, IT/data)
   - The assignment (what to ask the client to do next)
8. Build **Outreach / Opening Angle**:
   - What to say in the first contact that would make them want to talk
   - Based on the worry matrix + the wedge + the contact's background

**Output: EngagementPrep artifact** (the actual deliverable)

The engagement prep artifact contains:

### 5.1 Pre-Interview Hypotheses
```
H1: [claim] — Test in Stage 1
  Basis: [evidence from Steps 1-4]
  Confirm if: [what would prove it]
  Disconfirm if: [what would disprove it]
  If confirmed: [which questions to go deep on]
  If disconfirmed: [pivot to which questions]

H2: [claim] — Test in Stage 2
  ...
```

### 5.2 Worry Matrix
| Rank | Worry | Industry Problem | Company Amplifier | Likelihood | Impact | Why This Person Cares |
|------|-------|-----------------|-------------------|------------|--------|----------------------|
| 1 | [worry] | [industry problem] | [company signal] | H/M/L | H/M/L | [contact-specific reason] |
| 2 | ... | | | | | |
| ... | | | | | | |

### 5.3 Tailored Forcing Questions

**For the CFO (Ryan):**
1. [company-specific question that surfaces worry #1]
2. [company-specific question that surfaces worry #2]
...

**For the Operations Person:**
1. [what data exists on the warehouse floor that doesn't reach the CFO's desk?]
2. [what's manual vs. automated in their inventory process?]
...

**For the IT/Data Person (David C.):**
1. [what's the data pipeline from ERP to SEDNA to reporting?]
2. [where does data quality break down?]
...

### 5.4 The Wedge
```
What: [smallest concrete deliverable]
Delivered in: [timeframe — typically 48 hours]
Requires from client: [data / access / time]
Effort: S/M/L
Why this company: [why this wedge works for them specifically]
What success looks like: ["I'd use this every day"]
```

### 5.5 KPI Feasibility Matrix (Pre-Populated)
| KPI | Data Source (from dossier) | Format (guess) | Quality (guess) | Domo Connectable? (guess) | Feasibility | Effort | Open Questions |
|-----|---------------------------|----------------|-----------------|---------------------------|------------|--------|-----------------|
| Cash-to-Cash Cycle | [from dossier: ERP?] | [guess] | [guess] | [guess] | ?/20 | ? | [what to ask in interview] |
| Fill Rate | [from dossier] | [guess] | [guess] | [guess] | ?/20 | ? | [what to ask] |
| ... | | | | | | | |

### 5.6 Interview Guide
- 6-stage Discovery flow (adapted from the Discovery framework)
- Pre-interview hypotheses woven into Stage 1-2 questions
- STOP gates after each stage
- Data source mapping questions (Stage 3) — pre-populated with what we know, ask what we don't
- Stakeholder-specific question sets
- The assignment

### 5.7 Outreach / Opening Angle
```
"[Opening line tailored to this person at this company, based on the worry matrix and their background]"
```

**Storage:**
- Shared: `agents/idrisbot/private/{slug}-engagement-prep.md`
- Also: `agents/idrisbot/private/{slug}-discovery-guide.md` (the interview guide portion)
- KB: mdrag `datacrew` collection — save via `POST /api/v1/ingest/text` with title `"Engagement Prep: {company name}"`, `collection_id: "6a274087d4b0a3ad1b028ae8"` — this makes the full engagement prep searchable for future engagements

**Reuse:** Per-company, per-engagement. Not reusable. Update after the interview with what was learned (see Feedback Loop).

---

## Feedback Loop

After the Discovery interview (or any engagement phase), update the research:

1. **Update the CompanyDossier** with:
   - Data sources confirmed during the interview (ERP, CRM, financial system, etc.)
   - Current metrics being tracked (what they said they track today)
   - Pain points confirmed/disconfirmed (what the interview revealed)
   - Decision-making process (who decides, budget cycle, approval chain)
   - New contacts identified (operations person, IT person)

2. **Update the IndustryResearch** with:
   - Any new benchmarks discovered (e.g., "Ryan said their C2C is 120 days — that's a data point")
   - Any new problems identified that weren't in the original research
   - Problem ranking adjustments (if the interview revealed a different priority order)

3. **Re-run the Synthesis** (Step 5) with updated inputs if:
   - A hypothesis was disconfirmed (pivot — the interview changed the picture)
   - New information was revealed that changes the worry matrix
   - The wedge needs to be adjusted based on what we learned

4. **Capture the interview findings** as a structured note:
   - What was confirmed
   - What was disconfirmed
   - What was surprising
   - What the client committed to (the assignment)
   - Next steps and timeline

5. **Save interview findings to mdrag KB:** `POST /api/v1/ingest/text` with the interview findings markdown, title `"Interview Findings: {company name} — {date}"`, `collection_id: "6a274087d4b0a3ad1b028ae8"` — this makes the findings searchable for future engagements and closes the feedback loop in the KB

This feedback loop ensures the research base compounds over time. Each engagement enriches the industry research and the company dossier, making the next engagement's prep faster and sharper.

---

## Artifact Flow

```
Step 1: IndustryResearch
  │
  ├─→ Step 3: IndustryPatterns
  │       │
  │       └─→ Step 5: Synthesis ──→ EngagementPrep
  │                               ├── Pre-Interview Hypotheses
  │                               ├── Worry Matrix
  │                               ├── Tailored Forcing Questions
  │                               ├── The Wedge
  │                               ├── KPI Feasibility Matrix
  │                               ├── Interview Guide
  │                               └── Outreach / Opening Angle
  │
Step 2: CompanyDossier
  │
  └─→ Step 4: CompanyPatterns
          │
          └─→ Step 5: Synthesis
```

## Storage Map

| Artifact | Disk | Shared Memory Repo | mdrag KB | Reuse |
|----------|------|-------------------|----------|-------|
| IndustryResearch | `/projects/industry-analysis/{industry}/` | `agents/idrisbot/private/{industry}-industry-research.md` | `datacrew` collection + source URLs | Per-industry, cached |
| IndustryPatterns | `/projects/industry-analysis/{industry}/patterns.md` | `agents/idrisbot/private/{industry}-industry-patterns.md` | `datacrew` collection | Per-industry, cached |
| CompanyDossier | — | `agents/datacrew/clients/{slug}/company-contact-dossier/` | `datacrew` collection | Per-company |
| CompanyPatterns | — | `agents/datacrew/clients/{slug}/patterns.md` | `datacrew` collection | Per-company |
| EngagementPrep | — | `agents/idrisbot/private/{slug}-engagement-prep.md` | `datacrew` collection | Per-engagement |
| Interview Guide | — | `agents/idrisbot/private/{slug}-discovery-guide.md` | `datacrew` collection | Per-engagement |
| Interview Findings | — | — | `datacrew` collection | Per-engagement (feedback loop) |

## Relationship to Existing Skills and Runbooks

| Existing | Relationship |
|----------|-------------|
| `/industry-analysis` skill | Produces Step 1 (IndustryResearch) and Step 3 (IndustryPatterns) |
| Customer dossier workflow | Produces Step 2 (CompanyDossier) |
| `/pattern-hunter` runbook | **Renamed to "Positioning Audit."** This is a competitive positioning audit, not engagement prep. Different purpose, different output. The name "pattern hunter" is now used for Steps 3 and 4 (industry and company pattern hunters). |
| Discovery interview framework | Step 5 produces the interview guide using the 6-stage Discovery flow |
| AI CoS framework | Consumes the EngagementPrep artifacts to guide the ongoing engagement |
| mdrag `research-and-archive` runbook | Step 1 uses mdrag for web search (SearXNG), URL crawling (crawl4ai), and KB ingestion |
| mdrag `research-to-wiki-collection` runbook | Reference for collection management — artifacts go to the `datacrew` collection, browsable at `wiki.datacrew.space/collections/6a274087d4b0a3ad1b028ae8` |
| mdrag `calling-mdrag-from-agents` guide | Auth, endpoints, and tool reference for all mdrag API calls in this runbook |

## Versioning

- **v1.0** (2026-07-18): Initial runbook. Based on the Blue Raven Solutions engagement prep, the A&D industry analysis, and the 7-gap audit of the research process.
- **v1.1** (2026-07-19): mdrag integration. All artifacts now persist to the mdrag `datacrew` collection for cross-session RAG retrieval. Source URLs ingested via `/api/v1/ingest/web`. Each step queries the KB for prior research before producing new artifacts. Feedback loop saves interview findings to the KB.
