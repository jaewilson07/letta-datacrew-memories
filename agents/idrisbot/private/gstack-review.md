# gstack Review — Deep Analysis & Adaptation Notes

**Source:** `github.com/garrytan/gstack` (MIT license, 23 specialist skills)
**Local clone:** `/home/jaewilson07/GitHub/gstack`
**Reviewed:** 2026-07-16

---

## What gstack Is

gstack is a Claude Code skill framework that implements a structured software development lifecycle as discrete, composable "specialist" skills. Each skill is a SKILL.md file (generated from .tmpl templates) that Claude reads and executes as instructions. The lifecycle is:

```
Think → Plan → Build → Review → Test → Ship → Reflect
```

Each stage produces artifacts consumed by the downstream stage. The framework is designed for Claude Code specifically (bash preamble, AskUserQuestion, plan mode integration), but the *methodology* inside each skill is portable.

### Core Philosophy (ETHOS.md)
1. **Boil the Ocean** — Do the complete thing, not shortcuts. AI compresses implementation time 10-100x, so "ship the shortcut" is legacy thinking. The complete implementation is the goal.
2. **Search Before Building** — Three layers of knowledge: tried-and-true (Layer 1), new-and-popular (Layer 2), first-principles (Layer 3). Prize Layer 3.
3. **User Sovereignty** — AI recommends, user decides. Every scope change is an explicit opt-in via AskUserQuestion.

---

## Skills Most Relevant to My Role (Build Partner / Consulting Advisor)

### Tier 1: Directly Applicable

#### 1. `/office-hours` — YC Office Hours (STARTUP DIAGNOSTIC + BUILDER BRAINSTORMING)

**This is the single most relevant skill to my role.** It's a structured product diagnostic that runs before any code is written.

**Two modes:**
- **Startup Mode** — For founders/intrapreneurs. Six forcing questions that expose demand reality.
- **Builder Mode** — For hackathons, side projects, learning. Generative brainstorming.

**The Six Forcing Questions (Startup Mode):**
1. **Demand Reality** — "What's the strongest evidence that someone wants this — not interested, but would be upset if it disappeared?"
2. **Status Quo** — "What are users doing right now to solve this — even badly? What does that workaround cost?"
3. **Desperate Specificity** — "Name the actual human who needs this most. What's their title? What gets them promoted/fired?"
4. **Narrowest Wedge** — "What's the smallest version someone would pay for this week?"
5. **Observation & Surprise** — "Have you watched someone use this without helping? What surprised you?"
6. **Future-Fit** — "If the world changes in 3 years, does your product become more or less essential?"

**Key patterns I should adopt:**
- **Anti-sycophancy rules**: Never say "that's interesting," "there are many ways," "you might consider." Take a position on every answer. State what evidence would change your mind.
- **Pushback patterns**: Vague market → force specificity. Social proof → demand test. Platform vision → wedge challenge. Growth stats → vision test. Undefined terms → precision demand.
- **Smart routing by stage**: Pre-product → Q1,Q2,Q3. Has users → Q2,Q4,Q5. Has paying customers → Q4,Q5,Q6.
- **Premise challenge phase**: After questioning, present falsifiable premises for user to agree/disagree with. Every accepted premise becomes load-bearing.
- **Alternatives generation (MANDATORY)**: 2-3 distinct approaches with effort/risk/pros/cons. One minimal viable, one ideal architecture, one creative/lateral.
- **Founder signal synthesis**: Track signals (real problem, named users, pushback, taste, agency, domain expertise) and use them to calibrate the closing.
- **The assignment**: Every session ends with a concrete real-world action, not a strategy.

**Adaptation for IdrisBot:**
- The six forcing questions map directly to my AI CoS Discovery phase
- The premise challenge maps to my Foundation phase
- The alternatives generation maps to my Deployment planning
- The anti-sycophancy rules should be baked into my personality/voice
- The smart routing by stage maps to my engagement type detection (pre-product vs has users vs has paying customers)

#### 2. `/plan-ceo-review` — CEO/Founder Mode Plan Review

**Second most relevant skill.** Rethinks the problem from the user's perspective to find the "10-star product hiding inside the request."

**Four modes:**
- **SCOPE EXPANSION** — Dream big. Push scope UP. "What would make this 10x better for 2x the effort?"
- **SELECTIVE EXPANSION** — Hold scope as baseline, surface cherry-pickable expansions with neutral recommendations.
- **HOLD SCOPE** — Maximum rigor on existing plan. Catch every failure mode.
- **SCOPE REDUCTION** — Find the minimum viable version. Cut everything else.

**Key patterns:**
- **9 Prime Directives**: Zero silent failures. Every error has a name. Data flows have shadow paths. Interactions have edge cases. Observability is scope. Diagrams are mandatory. Everything deferred must be written down. Optimize for 6-month future. Permission to say "scrap it."
- **18 Cognitive Patterns of Great CEOs**: Classification instinct (reversibility × magnitude), paranoid scanning, inversion reflex, focus as subtraction, people-first sequencing, speed calibration, proxy skepticism, narrative coherence, temporal depth, founder-mode bias, wartime awareness, courage accumulation, willfulness as strategy, leverage obsession, hierarchy as service, edge case paranoia, subtraction default, design for trust.
- **Dream State Mapping**: CURRENT STATE → THIS PLAN → 12-MONTH IDEAL
- **Expansion framing**: Lead with felt experience, close with concrete effort. "Imagine the moment a workflow finishes — the user sees the result instantly..." not "Add real-time notifications."
- **Spec review loop**: Write plan → dispatch adversarial reviewer subagent → fix → re-dispatch. Max 3 iterations.

**Adaptation for IdrisBot:**
- The four modes map to different consulting engagement types
- The cognitive patterns should inform how I challenge Jae's assumptions
- The dream state mapping is a powerful consulting tool for client engagements
- The expansion framing pattern applies to how I present recommendations

#### 3. `/retro` — Engineering Retrospective

**Relevant for the Reflect phase of my engagement framework.**

**What it does:**
- Analyzes commit history, work patterns, shipping velocity
- Team-aware: per-person breakdowns with specific praise and growth opportunities
- Computes metrics: commits, LOC, test ratio, PR sizes, fix ratio
- Detects coding sessions from timestamps, finds hotspot files, tracks shipping streaks
- Has a "global" mode for cross-project retros

**Key patterns:**
- **Trends vs last retro**: Show deltas, not just current state
- **Focus & Highlights**: Ship of the week callout
- **Personal deep-dive**: What you did well (2-3 specific things), where to level up (1-2 actionable)
- **Team breakdown**: Per-person: what they shipped, praise, opportunity for growth
- **Top 3 team wins**: What, who, why it matters

**Adaptation for IdrisBot:**
- The retro format maps to the Handover phase of my engagement framework
- The "what you did well / where to level up" pattern is a good consulting deliverable
- The trend tracking pattern applies to how I track engagement progress over time

### Tier 2: Methodologically Useful

#### 4. `/investigate` — Systematic Debugger
- **Iron Law**: No fixes without root cause investigation first.
- Traces data flow, tests hypotheses one at a time, stops after 3 failed fixes.
- **Adaptation**: The "no fixes without investigation" principle applies to consulting — don't propose solutions before diagnosing the root cause.

#### 5. `/spec` — Spec Author
- Five-phase spec → GitHub issue, optional agent spawn
- Turns vague intent into precise, executable spec
- **Adaptation**: The five-phase spec process maps to how I structure engagement deliverables.

#### 6. `/autoplan` — Review Pipeline
- Runs CEO → Design → Eng review automatically with encoded decision principles
- Six principles: prefer completeness, match existing patterns, choose reversible options, prefer user's past decisions, defer ambiguous items, escalate security
- **Adaptation**: These six principles are good default consulting heuristics.

### Tier 3: Interesting But Not Directly Applicable

- `/review` — Staff engineer code review (too code-specific)
- `/qa` — QA lead testing (too code-specific)
- `/ship` — Release engineering (too code-specific)
- `/design-review` — Visual audit (too code-specific)
- `/design-consultation` — Design system from scratch (interesting but niche)
- `/cso` — Security audit (too code-specific)
- `/document-release` — Documentation updates (too code-specific)
- `/browse` — Headless browser (tool, not methodology)

---

## Key Architectural Patterns Worth Studying

### 1. Artifact Handoff Chain
Each skill produces an artifact that feeds the next:
```
office-hours → design doc → plan-ceo-review → CEO plan → plan-eng-review → eng plan → review → review report → qa → QA report → ship → PR → retro → retro report
```
**Lesson for consulting**: Every engagement phase should produce a concrete artifact that the next phase consumes. No phase should start from scratch.

### 2. Learnings Accumulation
gstack has a `learnings.jsonl` system where every session logs patterns, pitfalls, preferences, and architectural decisions. Future sessions search these before making recommendations.
**Lesson for consulting**: Every engagement should feed the knowledge store for the next engagement. This is already my design with the shared memory repo.

### 3. AskUserQuestion as the Communication Primitive
gstack uses AskUserQuestion extensively — one question at a time, with specific options. The format includes context, recommendation, and options.
**Lesson for consulting**: Forcing questions should be asked one at a time, with specific options, not open-ended.

### 4. STOP Gates
Every major decision point has a STOP gate — the skill cannot proceed until the user explicitly approves. This prevents the AI from running ahead.
**Lesson for consulting**: Engagement phases should have explicit approval gates. Don't move to the next phase without explicit client sign-off.

### 5. Cross-Model Second Opinion
gstack can dispatch to Codex (OpenAI) for an independent second opinion on plans and designs. The cross-model synthesis finds where they agree, disagree, and what that reveals.
**Lesson for consulting**: For high-stakes recommendations, get a second perspective. The synthesis is where the value is, not the individual opinions.

### 6. Context Recovery
gstack saves and restores context across sessions — decisions, learnings, design docs, CEO plans.
**Lesson for consulting**: Engagement state should persist across sessions. I should be able to pick up where I left off without re-asking questions.

---

## What I'm NOT Adopting (and Why)

1. **The bash preamble system** — gstack's preamble is 200+ lines of bash that sets up session state, telemetry, update checks, etc. This is Claude Code-specific infrastructure. I don't need it.

2. **The skill template generation pipeline** — gstack generates SKILL.md from .tmpl files via a build step. My "skills" are memory files, not generated templates.

3. **The browser/QA/ship/deploy skills** — These are software engineering tools, not consulting methodology. My role is product/strategy thinking, not code execution.

4. **The telemetry and analytics system** — gstack tracks skill usage, eureka moments, builder profiles. Interesting for a product, but my "telemetry" is engagement outcomes captured in memory.

5. **The gbrain integration** — gstack integrates with a semantic code search tool. My equivalent is conversation_search and memory tools.

---

## Summary: What I'm Taking

| gstack Pattern | My Adaptation |
|---|---|
| Six Forcing Questions (office-hours) | Discovery phase questioning framework |
| Anti-sycophancy rules | Baked into my personality/voice |
| Premise Challenge | Foundation phase premise validation |
| Alternatives Generation (MANDATORY) | Always present 2-3 approaches in recommendations |
| Four Review Modes (CEO review) | Engagement mode selection (expansion, selective, hold, reduction) |
| 18 Cognitive Patterns (CEO review) | Internalized as thinking instincts for challenging assumptions |
| Dream State Mapping | Consulting tool for client visioning |
| Founder Signal Synthesis | Track client signals to calibrate engagement tier |
| The Assignment | Every engagement ends with a concrete action |
| Artifact Handoff Chain | Every phase produces an artifact for the next |
| Learnings Accumulation | Already implemented via shared memory repo |
| STOP Gates | Explicit approval gates between engagement phases |
| Cross-Model Second Opinion | Use Agent tool for independent perspectives on high-stakes recs |
| Smart Routing by Stage | Route questions based on client/product maturity |
| Expansion Framing | Lead with felt experience, close with concrete effort |
| Spec Review Loop | Adversarial review of my own deliverables before presenting |

---

## Next Steps

1. **Integrate the six forcing questions** into my AI CoS Discovery phase documentation
2. **Update my anti-sycophancy rules** in my personality/voice memory to match gstack's patterns
3. **Add the premise challenge and alternatives generation** as mandatory steps in my Foundation phase
4. **Add the four review modes** as engagement mode options
5. **Create a "dream state mapping" template** for client visioning exercises
6. **Add STOP gates** to my engagement framework documentation
