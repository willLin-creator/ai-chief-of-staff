# Market Pulse -- 3am Mon/Wed/Fri competitive + market scan

This is the "grind while you sleep" routine. Three times a week at 3:00am (your timezone), the roadmap skill runs in **market-scan mode** (see `/roadmap market-scan` in `~/.claude/commands/roadmap.md`) and writes a dated section to the **Market Pulse Doc**.

The work-tracker skill reads the latest Market Pulse section as part of the Strategic Fit lens (see `prioritization.md`). When market shifts make a deliverable more or less strategic, the next morning plan reflects it.

## The Market Pulse Doc

**Location:** Google Doc, ID stored in the roadmap skill Configuration block as `Market Pulse Doc ID` ({{DOC_ID}}). Created on first run via `gdocs.py create`.

**Structure:** dated entries newest at top. Each entry caps at ~1 page so the doc stays scannable across months of runs.

```
{{COMPANY}} -- Market Pulse
Last run: [MM/DD/YYYY 3:00am]

═══════════════════════════════════════════════
[MM/DD/YYYY] -- Market Pulse Run
═══════════════════════════════════════════════

Competitors scanned: [3-5 names this run]
Selection rationale: [1 line on why these vs others]

────────────────────────────────────────────
COMPETITOR MOVES
────────────────────────────────────────────

• [Competitor name] -- [observed move]
  Source: [URL or "press release", "G2 listing", "LinkedIn announcement"]
  Implication for {{COMPANY}}: [1-2 sentences]
  Action candidate: [if any -- e.g., "bump epic 4 priority", "frame counter-positioning"]

[Repeat for each notable move]

────────────────────────────────────────────
MARKET SIGNALS
────────────────────────────────────────────

• [Trend / regulatory / funding / category shift]
  Source: [URL]
  Implication for {{COMPANY}}: [1-2 sentences]
  Action candidate: [if any]

────────────────────────────────────────────
CUSTOMER MENTIONS (internal)
────────────────────────────────────────────

[Anything from meeting notes/Slack last 48h where customers named competitors or "we're also looking at" -- raw mentions, no editorializing]

• [Customer / source] -- "[quote]"

────────────────────────────────────────────
ACTIONABLE IMPLICATIONS FOR {{YOUR_NAME}}
────────────────────────────────────────────

Top 1-3 for the day's plan run. Each one is a one-liner suitable for the Strategic Fit lens to read.

1. [Implication] -- bump/demote/add: [what work this affects]
2. [...]
3. [...]

────────────────────────────────────────────
ROADMAP SKILL HOOKS
────────────────────────────────────────────

Items that should be reflected in the next /roadmap full run:

• [Epic name] -- [score adjustment / new insight item / new candidate]
```

## Dynamic competitor selection -- not a static list

The skill picks **3-5 competitors per run** based on what {{YOUR_NAME}} is actually working on right now. The selection changes. Nothing is forced into every run -- the active watch list below is prioritized in rotation, not pinned.

### Active watch (prioritized in rotation -- none forced every run)

Companies {{YOUR_NAME}} wants kept an eye on. Prioritize these in candidate selection (ahead of category picks); each should be scanned at least once every 2-3 runs. They share the 5-cap, so not all appear in any single run. Until a company is characterized, prioritize the uncharacterized ones; placeholder descriptions get replaced on first scan (positioning, product surface, funding).

> Seed this list with your own watch list. Each entry: name, one-line positioning, and what to watch. Examples below are illustrative placeholders -- replace them.

- **{{COMPETITOR}} A** -- market-adjacent incumbent in your category.
- **{{COMPETITOR}} B** -- newer entrant in your core space.
- **{{COMPETITOR}} C** -- AI-driven player; closest functional overlap with your core product thesis. Watch product surface, customer wins, and positioning language.
- **{{COMPETITOR}} D** -- flagged recently; characterize on first scan (likely adjacent).
- **{{COMPETITOR}} E** -- a platform that is both a potential partner AND building competing capability. Watch: feature velocity, how partner-vs-competitor tension evolves.

### Categories to draw from

The skill should expand the candidate pool by category and pick the 3-5 most relevant for *this run*. Replace these category labels with the ones that fit your market:

1. **Traditional incumbents (your category's established firms):** list 5-7 names.
2. **Newcomers / AI-first players:** newly-funded entrants in the last 12 months -- search `"[your category] software" + recent funding`.
3. **Adjacent platform software:** tools your buyers already use that could expand into your space.
4. **Adjacent operational/asset tooling:** the neighboring category one step removed from yours.
5. **Where-the-puck-is-going AI plays:** anything new applying AI to your domain in the last 6 months.
6. **Adjacent financial / partner tooling:** players in the money-movement or fiduciary layer near your product.

### Selection logic per run

Read `~/.claude/skills/work-tracker/references/state.md` (or fall back to the {{PLANNING_DOC}} top epics) to determine current focus. Then:

1. **Rotate in 2-3 from the active watch list.** Prioritize the ones not scanned in the last 2-3 runs, and any not yet characterized. Nothing is pinned to every run.
2. **Add 1-2 from the category most aligned with {{YOUR_NAME}}'s current top-3 deliverables.** Example: if the top deliverable is a board-facing report, include 1 traditional incumbent (their current reporting capability is the benchmark customers implicitly compare to). If the top deliverable is {{PRODUCT}}-related, include 1-2 AI plays.
3. **Add 1 wildcard** -- a competitor or category {{COMPANY}} hasn't looked at in 30+ days, found by reading prior Market Pulse entries. This forces breadth over time.
4. **Cap at 5.** A focused scan beats a broad one. Expect to rotate -- not every watched company appears every run.

State the selection rationale in the doc so it's auditable: "This run focused on traditional incumbents because {{YOUR_NAME}} is mid-flight on board reporting; included {{COMPETITOR}} C from the active watch (not scanned in 2 runs) and a PropTech-AI wildcard since we haven't checked that category in 4 weeks."

## What to scan for each competitor

For each of the 3-5 competitors selected:

1. **Recent product announcements** -- scan their website, blog, LinkedIn company page, press releases. WebSearch with `"[competitor name]" announcement 2026` or `"[competitor name]" launches`.
2. **G2 / Capterra / TrustRadius listings** -- new feature mentions in reviews, recent review themes, rating trajectory.
3. **Job postings** -- LinkedIn or careers page. Hiring signals direction (e.g., "hiring 5 ML engineers" = AI investment).
4. **Funding / M&A news** -- Crunchbase, PitchBook free tier, SEC filings if public-adjacent.
5. **Customer overlap signals** -- have any of their customers been mentioned in {{YOUR_NAME}}'s pipeline or churned-from list?

Don't go deep on every dimension for every competitor. Pick what's *moving* this run.

## Market signals (non-competitor)

Beyond competitors, scan:

1. **Regulatory:** any law or mandate that shapes demand in your category. Search by region/state if {{COMPANY}} has known geographic concentration.
2. **Industry analyst takes:** relevant research firms and trade-association publications in your space.
3. **Adjacent funding:** who raised in your category and adjacent ones, what stage, what thesis.
4. **AI in your domain:** general category trend -- press, podcasts, conferences. Where is the puck going?
5. **Partnership/integration signals:** if a major platform in your space announces an integration with someone, that's signal.

## Customer mention sweep

In addition to web scanning, pull internal signals -- last 48h of:

- **Meeting-notes transcripts** -- customers naming competitors or "we evaluated X" or "your competitor does Y"
- **Slack customer-feedback channels** (if any) -- mentions of other tools
- **Gmail customer threads** -- "you also offer" / "I saw [competitor] launched"

These are gold because they're customers self-reporting their alternatives. Quote verbatim, attribute to source, no editorializing.

## Actionable implications -- the synthesis

The Market Pulse doc is only useful if it tells {{YOUR_NAME}} what to **do**. End each entry with 1-3 actionable implications:

- "{{COMPETITOR}} shipped X -> our roadmap item needs to add Y to stay credible" -- bumps a deliverable's strategic fit
- "{{COMPETITOR}} raised seed and is hiring 3 PMs -> they're going to ship fast; tighten our {{PRODUCT}} differentiation messaging in next board update" -- adds a positioning deliverable
- "Regulatory change requires Z by [date] -> add a compliance epic" -- creates a new roadmap candidate
- "Customer X said '[competitor] does inline approvals' -> add inline approval to feature priority list"

Each implication is one line, action-oriented, and tagged to either a roadmap epic, a tracked deliverable, or a new candidate.

## Integration points

### Into the roadmap skill (`~/.claude/commands/roadmap.md`)

The roadmap skill gains a new mode: `/roadmap market-scan`. It runs the scan, writes to the Market Pulse Doc, and exits. (Full `/roadmap` runs read the Market Pulse Doc as Source D in Step 3.)

Trigger: scheduled remote agent at 3:00am Mon/Wed/Fri (your timezone) via the `schedule` skill.

### Into the work-tracker (this skill)

The morning plan run reads the latest Market Pulse entry (from the Google Doc) before scoring deliverables. The Strategic Fit lens uses the "Actionable implications for {{YOUR_NAME}}" section to:

- Bump deliverables flagged as more strategic
- Demote deliverables that the market just made less relevant
- Surface new candidate deliverables (e.g., "Add a positioning deliverable in response to {{COMPETITOR}}'s seed round")

### Into the insights doc

If the scan surfaces something that meets the bar for an insight item (multi-source customer signal, validated theme), surface it as a "candidate insight item" in the Roadmap Skill Hooks section so the next `/insights` run can pick it up.

## Failure modes to avoid

- **Don't fabricate moves.** If WebSearch returns nothing for a competitor this run, write "no notable moves observed since [date]" -- not "they may be working on X."
- **Don't editorialize customer quotes.** Verbatim only.
- **Don't surface every implication as urgent.** Most market shifts are slow. Only bump scores or surface new deliverables when the signal is strong.
- **Don't over-scan.** 3-5 competitors per run. The breadth comes from rotation across runs, not depth on every run.
- **Don't bury {{YOUR_NAME}} in noise.** The Slack/work-tracker layer should NEVER send a Slack message just because the market scan ran. The scan writes to the doc; the morning plan reads the doc; only if the morning plan generates an actionable shift does {{YOUR_NAME}} get pinged.

## First-run behavior

On the very first run:

1. Create the Market Pulse Google Doc via `python3 ~/.claude/scripts/gdocs.py create --title "{{COMPANY}} -- Market Pulse"`. Capture the returned doc ID.
2. Write the doc ID into `~/.claude/commands/roadmap.md` Configuration block as `Market Pulse Doc ID`.
3. Run the first scan and seed the doc with one entry.
4. Confirm to {{YOUR_NAME}} that the recurring schedule is live.
