# /roadmap — Epic Pipeline & Quarterly Priority

## Description
Synthesizes signals from meeting notes, the product insights doc, and governing contract/SOW documents
to produce an **epic-level** roadmap. Outputs:
- **Planning doc** (e.g. a shared Google Doc) — full epic detail (deep, rich, narrative)
- **Project board** — quick snapshot for team collaboration, ranked top-to-bottom

Each entry on the roadmap is an **epic** (varying size, contains multiple ideas + tickets).
One-off bugs do NOT appear on the roadmap — they live in your issue tracker and are referenced
from inside the epic that contains them.

## Usage
- `/roadmap` -- run full evaluation; update planning doc + sync project board
- `/roadmap market-scan` -- run the recurring competitive + market scan; write to the Market Pulse Doc only (does NOT touch the main roadmap doc or project board). See your market-scan reference doc (e.g. `~/.claude/skills/work-tracker/references/market-pulse.md`) if you maintain one.

---

## Configuration

Fill these in for your own setup. Anything in `{{...}}` is a placeholder.

**Planning Doc ID:** `{{PLANNING_DOC_ID}}`
**Planning Doc URL:** `{{PLANNING_DOC_URL}}` (your roadmap doc)

**Insights Synthesis Doc ID:** `{{INSIGHTS_DOC_ID}}`

**Governing contract/SOW Doc ID(s):** `{{SOW_DOC_ID}}`
(Add other governing SOW/contract docs here as they're created.)

**STRATEGY.md path:** `~/.claude/STRATEGY.md`
The durable product spine — target problem, approach, users, key metrics, work tracks.
Maintained via your strategy skill (optionally `compound-engineering:ce-strategy` if installed).
The roadmap operationalizes strategy; it does not replace it. Every epic should map to a track
defined here.

**Market Pulse Doc ID:** `{{MARKET_PULSE_DOC_ID}}`
**Market Pulse Doc URL:** `{{MARKET_PULSE_DOC_URL}}`
(Created on first `/roadmap market-scan` run. Updated by `/roadmap market-scan` on your chosen cadence. Subsequent runs use `python3 ~/.claude/scripts/gdocs.py write` to replace contents -- always re-include all prior dated entries with the new entry stacked on top.)

**Product Ideas backlog (YAML):** `~/.claude/product-ideas.yaml`
Managed by the `/idea` skill (see `~/.claude/commands/idea.md`). Holds pre-roadmap product idea candidates with structured fields: source meeting + verbatim quote, target_icp, p_lever, impact, 4-lens score, status. The roadmap reads `captured` and `scoped` ideas as a signal source (Source F in Step 3) and, when an idea is incorporated into an epic, writes back to update `status: in_roadmap` and `related.epic_id`. Dropped/shipped items archive to `~/.claude/product-ideas-archive/<YYYY-MM>.yaml`.

**Project board (idea/feature prioritization board):**
- Project key: `{{BOARD_PROJECT_KEY}}`
- Board / view URL: `{{BOARD_URL}}` (your project board)
- Issue type: `Idea` (or your tool's equivalent)
- Purpose: collaboration layer; reflects priority top-to-bottom; sort the view by **Priority Score** desc

**Board prioritization fields** (map these to whatever your tracker calls them):
| Field name | Field ref | Type | Scale | Use |
|------------|-----------|------|-------|-----|
| **Priority Score** | `{{PRIORITY_SCORE_FIELD}}` | float | 0–99 | **PRIMARY ranking field — write the adjusted RICE score here. Contract-committed work = 99.0 to force top placement. Sort the board view by this field desc.** |
| Impact | `{{IMPACT_FIELD}}` | rating | 1 (Low), 2 (Medium), 3 (High) | Board dimension — actual RICE Impact semantic only |
| Value | `{{VALUE_FIELD}}` | rating | 1, 2, 3 | Board dimension — customer value |
| Effort | `{{EFFORT_FIELD}}` | rating | 1 (Low cost), 2, 3 (High cost) | Board dimension — actual RICE Effort semantic only |
| Confidence | `{{CONFIDENCE_FIELD}}` | slider | 0–100 | Board dimension — direct from RICE Confidence % |
| Auto Impact score | `{{IMPACT_SCORE_FIELD}}` | formula | auto | Tool auto-computed; NOT for overall priority — do not conflate |
| Archived | `{{ARCHIVED_FIELD}}` | option | "Yes" / null | "Yes" hides from boards. **Never auto-unarchive — see rule below.** |
| Rank | `{{RANK_FIELD}}` | tool-managed | — | Often not editable via API |

**Critical separation:** Priority Score is the rolled-up RICE-derived rank. The Impact/Value/Effort/Confidence dimensions *feed* RICE — never use them as proxies for overall priority.

**A standard tracker `priority` field** (Highest/High/Medium/Low) may also be set, but typically does NOT show as a sortable column in idea-board views.

**Contract/SOW override:** Any idea tied to a contractual deliverable gets `Priority Score = 99.0` regardless of its natural RICE score. This forces committed work to the top of the Priority Score sort.

**Never auto-unarchive:** If the Archived field = "Yes" on an idea that appears related to active scope, surface it as a question — do not flip the archive flag without explicit confirmation. Archive is intentional curation.

---

## Core Concepts

### What is an epic?
An epic is a body of related work that delivers a coherent capability. It contains multiple
ideas, tickets, and customer/source signals. Epics vary in size from M (~1 month) to
XXL (multi-quarter). Epic items are NOT individual features — features roll up into epics.

### What does NOT belong on the roadmap?
- One-off bugs → issue tracker as Bug tickets
- Discrete UX fixes (single narrow interaction) → issue tracker as Story
- Tactical tasks tied to a specific customer onboarding → not roadmap material
- Anything that doesn't represent a coherent capability or initiative

When in doubt: if it's standalone and self-contained, it's a tracker ticket. If it groups multiple
related deliverables, it's an epic.

### Two priority dimensions
1. **Committed work** — contractual deliverables OR explicit product commitments from
   leadership. These take precedence over RICE scoring.
2. **RICE-ranked work** — everything else, scored and stack-ranked.

The board ranking (top-to-bottom) reflects: Committed first, RICE next.

---

## Scoring Framework (RICE — applied to epics, not features)

### RICE Formula
```
RICE Score = (Reach × Impact × Confidence) / Effort
Adjusted Score = RICE Score × Leadership Multiplier
```

### Reach (1–10)
% of your user base affected per quarter.
| Score | Meaning |
|-------|---------|
| 1–2 | Niche — affects <10% |
| 3–4 | Moderate — 10–30% |
| 5–6 | Common — 30–60% |
| 7–8 | Broad — 60–80% |
| 9–10 | Universal — >80% |

### Impact (0.25 / 0.5 / 1 / 2 / 3)
Effect on engagement, retention, or expansion revenue.
| Score | Meaning |
|-------|---------|
| 0.25 | Minimal |
| 0.5 | Low |
| 1 | Medium |
| 2 | High |
| 3 | Massive — transformative for product or key segment |

### Confidence (30% / 50% / 80% / 100%)
| Score | Meaning |
|-------|---------|
| 100% | Strong — multi-source customer + leadership confirmed |
| 80% | 2+ meeting mentions or insights items |
| 50% | Single source |
| 30% | Speculative |

**Boosters** (cap at 100%): 2+ meeting notes (+10%) | external customer asked (+10%) |
in insights doc (+10%) | both your manager + eng lead raised it (+10%).

### Effort (epic-level, 1–20)
Engineering complexity for the entire epic, not individual features inside it.
| Size | Units | Meaning |
|------|-------|---------|
| M | 5 | ~1 month epic |
| L | 10 | 1–2 months |
| XL | 15 | 2–3 months |
| XXL | 20 | 3+ months / multi-quarter |

### Leadership Multiplier
| Signal | Multiplier |
|--------|-----------|
| Manager + Eng Lead explicit | ×2.0 |
| Manager OR Eng Lead explicit | ×1.5 |
| Neither | ×1.0 |

---

## Instructions

### Step 0: Prerequisites
```bash
test -f ~/.claude/scripts/gdocs.py && echo "gdocs.py: READY" || echo "gdocs.py: MISSING"
```
(`gdocs.py` is the Google Docs read/write helper. Swap in whatever doc tooling you use.)

---

### Mode dispatch

If invoked as `/roadmap market-scan` -> jump to **MARKET SCAN MODE** below and exit after completion. Do NOT continue to Step 1.

If invoked as `/roadmap` -> proceed to Step 1.

---

## MARKET SCAN MODE

This is the recurring "grind while you sleep" routine. If you keep a full spec (e.g. a market-pulse reference doc), follow it. Brief execution:

1. **Read state.** Check your current top deliverables (e.g. a work-tracker state file, if you maintain one). Determine which competitor categories to focus on.
2. **Select 3-5 competitors:**
   - Always include your 1-2 primary named competitors
   - Add 1-2 from the category aligned with current top deliverables
   - Add 1 wildcard not scanned in 30+ days (read prior Market Pulse entries to avoid repeats)
   - Cap at 5
3. **Scan each competitor** via web search:
   - Recent product announcements / blog posts / press releases (search `"[competitor]" [year] launch OR announcement OR feature`)
   - Review-site mentions, review trajectory
   - Job postings (signal direction)
   - Funding/M&A
4. **Scan market signals:** regulatory changes in your domain, AI/industry trends, funding in adjacent space, partnership announcements.
5. **Customer mention sweep** (meeting notes, Slack, last 48h): verbatim quotes where customers named competitors or alternatives.
6. **Synthesize 1-3 actionable implications:** what should bump/demote/be added in the roadmap.
7. **Write to Market Pulse Doc** (ID in Configuration). Append a dated entry at the top; keep prior entries intact.
   - On first run, create the doc: `python3 ~/.claude/scripts/gdocs.py create --title "{{COMPANY}} -- Market Pulse" --file [staged file]`, capture the new doc ID, and update this command file's Configuration block.
   - Subsequent runs: write via `python3 ~/.claude/scripts/gdocs.py write --doc-id [ID] --file [staged file]`. The write replaces the doc, so re-include all prior entries with the new entry on top.
8. **Do NOT touch:** the main planning doc, the project board, your task list, or send any messages. The morning planning routine reads the Market Pulse doc and decides if anything needs to surface.
9. **Exit.** Print summary:
   ```
   MARKET PULSE UPDATED -- [MM/DD/YYYY]
   Competitors scanned: [list]
   Implications: [count]
   Doc: [link]
   ```

---

### Step 1: Read Existing Planning Doc + Existing Board Ideas (parallel)

**1a. Existing planning doc:**
Fetch via `python3 ~/.claude/scripts/gdocs.py read --doc-id {{PLANNING_DOC_ID}}`. Extract current epic list with names, scores, ranks, contained ideas.

**1b. Board ideas:**
Query your board for all Ideas (e.g. `project = {{BOARD_PROJECT_KEY}} AND issuetype = Idea ORDER BY created DESC`).
Build lookup: idea-key → summary → existing labels → existing priority.

State:
```
PLANNING DOC STATUS — [N epics found / first run]
BOARD IDEAS LOADED — [N ideas]
```

---

### Step 1c: Read Strategy (durable spine)

Read `~/.claude/STRATEGY.md` for the product's target problem, approach, users, and current
work tracks. Every epic should map to a track defined here.

**If STRATEGY.md does not exist:**
Prompt: "STRATEGY.md not found. Create one (e.g. via your strategy skill) before
proceeding? Without it the roadmap has no durable spine to anchor against. [Y/N/skip]"

- Y → create the strategy doc, then resume Step 1c
- N or skip → proceed, but flag in Step 11 final summary: "Strategy alignment not validated"

**If STRATEGY.md exists:**
- Treat its work tracks as canonical groupings — epics should align to these tracks
- In Step 8, flag any epic that doesn't map to a track as "orphan from strategy"
- If a track has zero active epics, ask: "Track [X] has no epics. Strategy stale, or roadmap missing it?"

State:
```
STRATEGY: [N tracks loaded] / not found, proceeding without alignment check
```

---

### Step 2: Read Governing Contract/SOW Documents

For each contract/SOW doc in Configuration, fetch via gdocs.py and extract:
- Contractual deliverables (numbered sections like 3.2.1, 4.2.1, etc.)
- Acceptance criteria
- Timeline / hard deadlines (e.g., trade show or launch dates)
- Dependencies on your team
- Any "Appendix B / What's Next / Post-deliverable roadmap" sections (these become future epics, not committed)

Group contract deliverables into 1-2 committed epics (e.g., "{{PRODUCT}} V1 Foundation", "{{PRODUCT}} V2 Launch").

State:
```
CONTRACT DOCS READ — [N docs]
COMMITTED EPICS — [N committed epics with M deliverables total]
```

---

### Step 3: Gather All Signals (parallel)

**Source A — Meeting notes** (`~/.claude/meeting-notes/`)
Read all files. Extract from `## Product Signals & Context`, `## Key Decisions`, `## Action Items`, `## Summary`. Note who raised each signal (manager / eng lead).

**Source B — Insights synthesis**
Fetch the insights synthesis doc. Extract all insight items with full content.

**Source C — Product-committed sequencing**
Capture any explicit sequencing commitments from leadership conversations
(e.g., "RBAC next, then Notifications"). These override RICE order.

**Source D — Market Pulse (competitive + market scan)**
Fetch the latest dated entry from the Market Pulse Doc (ID in Configuration).
Extract:
- Competitor moves with implications for your product
- Market signals (regulatory, funding, trends)
- "Actionable Implications" -- direct hooks into roadmap scoring
- Any items in a "ROADMAP HOOKS" section -- these are explicit instructions to bump/demote/add epics

If no Market Pulse Doc exists yet, skip this source. The market scan seeds it.

**Source E — Product Pulse (behavioral signals)**
Pull the most recent weekly behavioral digest from your analytics stack
(product analytics + event router + web analytics). Every new ticket can carry
`metric considerations` defining what to capture; the pulse aggregates that
instrumentation into a roadmap signal.

**How to fetch (in priority order):**
1. **Email search** -- look for the latest analytics weekly/board digest email (last 7d).
2. **Saved dashboard** -- if a shared dashboard URL is in `~/.claude/STRATEGY.md`
   under Operating Context, fetch it.
3. **Manual paste** -- if neither found, ask: "Paste this week's analytics summary,
   or skip the behavioral source for this run?"
4. **Future** -- a deterministic analytics-API fetch script would replace steps 1-3.

**Extract:**
- Top usage patterns -- what users actually do (not what they say)
- Quality regressions or error spikes (cross-reference error monitoring if available)
- Adoption deltas on shipped features (especially anything from the last release)
- Signals worth investigating that no meeting has surfaced yet

Behavior data complements reported feedback. Discrepancies are the highest-signal:
"users say X but do Y" → real roadmap input. If the pulse flags a regression on a recently
shipped epic, surface it in Step 8 changelog regardless of RICE math.

If pulse data isn't available, skip gracefully and note "Product Pulse: unavailable -- relying
on reported feedback only" in the SOURCES LOADED block.

**Source F — Product Ideas backlog** (`~/.claude/product-ideas.yaml`)
Read the YAML. Filter to ideas where `status` is `captured` or `scoped` (skip
`in_roadmap`, `in_prd`, `shipped`, `dropped` — those are already accounted for or out).
For each captured idea, extract:
- `id`, `title`, `rationale`, `source.reference`, `source.quote`, `target_icp`
- `p_lever`, `impact`, `score.composite`
- `related.metric_suggestion_id` (cross-link to any metric suggestions)

These ideas were captured by the `/idea` skill — pre-vetted, structured product
candidates with verbatim quotes back to source meetings. They should be treated
with similar weight to insights doc items: high-signal, low-noise. High
`score.composite` ideas (≥15 out of 20) are candidates for promotion to an epic
this run.

In Step 6 (Build Epic List), when a captured idea aligns with a new or existing
epic, include the `idea-XXX` reference in the epic's source signals. The idea's
status will be updated in the new Step 9.5 (write-back) once the epic stack is
confirmed.

If `~/.claude/product-ideas.yaml` doesn't exist or has no ideas, skip gracefully.

State:
```
SOURCES LOADED
Meeting notes: [N]
Insights: [N items]
Committed sequence: [list, if any]
Market Pulse: [date of latest entry] | [N actionable implications]
Product Pulse: [date range] | [N behavioral signals]
Product Ideas backlog: [N captured/scoped ideas] | [N high-score candidates ≥15]
```

---

### Step 4: Identify One-Off Issues for Triage (Bugs → tracker, NOT roadmap)

Scan signals for items that are:
- Broken behavior (bug, defect, data error)
- Specific narrow UX fix
- Self-contained, single customer

These go to your issue tracker as Bug or Story (NOT to roadmap, NOT to the idea board).

```
ONE-OFF ISSUES FOUND — [N items]
[description] — [source] → Bug
[description] — [source] → Story (UX fix)

Create tickets in the tracker? [Y/N]
```

If confirmed, file in your tracker with Given/When/Then format:
```
**Given** [precondition]
**When** [trigger]
**Then** [expected behavior]

### Context & Strategy
[2-3 sentences with insight or meeting reference]

### Acceptance Criteria
1. **[Fix Requirement]**
   - [testable criterion]

### Technical Notes
[Optional]
```

Apply your team's standard labels and review conventions (e.g. a "needs-review" label, a
DRAFT title prefix, unassigned by default). Adapt to your own workflow.

---

### Step 5: Cross-Reference Existing Board Ideas Against Roadmap

For each existing board idea, determine:
1. **Belongs in an epic** — group it under the right epic (many ideas per epic is expected)
2. **Truly orphan** — no clear epic match → flag for triage
3. **Actually a bug** — should migrate to the issue tracker

A single epic typically contains 2-10 ideas. Some epics may contain 1; very large epics
may contain 10+.

---

### Step 6: Build Epic List

Extract or update the epic list. Each epic has:
- **Number + Name** (e.g., "Epic 8 — Project Management Platform")
- **Description** (2-3 sentences)
- **Contained board ideas** (list of keys)
- **Contained tracker tickets** (key references)
- **Leadership signals**
- **Customer signals** (which external accounts mentioned)
- **Source signals** (meetings + insight items + **idea-XXX captures** from `product-ideas.yaml`)
- **Originating ideas** (subset of source signals) — list of idea IDs from the Product Ideas backlog that were absorbed into this epic. These get their YAML `status` updated to `in_roadmap` in Step 9.5.

Epic numbering: committed/contract epics use C1, C2, etc. Non-committed epics use 1, 2, 3...

**When deciding whether a captured idea fits an existing epic vs. seeds a new one:**
- High `score.composite` (≥15) + clear thematic match to existing epic → absorb into existing epic, add idea-XXX to Source signals
- High score + no match to any existing epic → propose new epic with idea-XXX as the primary signal
- Lower score → leave in `captured` status; surface in changelog as "candidate considered, deferred"

---

### Step 7: Score Each Non-Committed Epic

Apply RICE at the epic level. Show reasoning:
```
Epic [N] — [Name]
Reach: [score] — [rationale]
Impact: [score] — [rationale]
Confidence: [score]% — [rationale + boosters]
Effort: [score] — [size + rationale]
RICE: ([R] × [I] × [C]) / [E] = [base]
Leadership: [Mgr+Eng / Mgr / Eng / —] × [multiplier]
Adjusted: [final]
```

Committed/contract epics don't get scored — they're contractual.

---

### Step 8: Build the Stack Rank

**Top to bottom:**
1. **Committed Epics (contract + product commitments)** — in order of: contract deliverable order, then explicit product commitments (e.g., "RBAC next, then Notifications")
2. **Non-committed Epics ranked by Adjusted Score** (highest first)

For ties at the same score, use product-committed sequence as tiebreaker.

Compare to previous run. Show changelog:
```
NEW [Epic] — new at #[rank] (score [x])
UP  [Epic] — moved #[old] → #[new] (score change: [why])
DN  [Epic] — moved #[old] → #[new]
[N epics unchanged]
REMOVE [Epic] — flag for removal review (no recent signals)

Proceed? [Y/N]
```

Wait for confirmation.

---

### Step 9: Sync Project Board

For every board idea:

**A. Apply labels:**
- `epic-NN-shortname` (e.g., `epic-01-rbac`, `epic-08-project-mgmt-platform`)
- `contract-committed` if part of a committed epic
- `needs-triage` if it should migrate to the tracker or doesn't fit any epic

**B. Write Priority Score — PRIMARY ranking field:**

This is the single field that drives board top-to-bottom ordering. Sort the view by this field desc.

| Epic | Priority Score |
|------|----------------|
| Contract-committed (any contractual deliverable) | **99.0** |
| Non-committed epic | The epic's Adjusted RICE Score, e.g. `5.40`, `4.80`, `2.16`, `0.54` |

Use the same numeric value across every idea inside an epic — they share the epic's score.

**C. Set board dimension fields (Impact, Value, Effort, Confidence) to actual semantic values:**

These feed any auto-computed `Impact score` formula and serve as user-facing dimension data. They are NOT proxies for overall priority — that's what Priority Score is for.

| Field | Source | Mapping |
|-------|--------|---------|
| Impact | RICE Impact | 0.25/0.5 → 1, 1 → 2, 2/3 → 3 |
| Value | Customer-value judgment | 1/2/3 (independent of RICE Impact) |
| Effort | RICE Effort (T-shirt) | XS/S → 1, M → 2, L/XL → 3 |
| Confidence | RICE Confidence % | direct passthrough (30/50/80/100) |

**Effort semantics on the board:** lower = less effort (better).

**Archived ideas — DO NOT auto-unarchive.** Archive is intentional curation: when a newer ticket supersedes an older one, or scope shifts elsewhere, the old idea gets archived. Auto-unarchiving disrespects that decision. Instead:

1. Search archived ideas (e.g. `Archived = "Yes"`) for visibility only
2. Surface them in the changelog with the question: "These archived ideas overlap epics [N] — they look related to current scope. Were they intentionally archived (e.g., superseded by a newer idea)? Want them un-archived, or skip?"
3. Wait for explicit confirmation before changing the Archived flag
4. Default behavior: leave archived. Skip them when applying labels/scores.

**D. Add roadmap-update comment:**
```
Roadmap Update -- [MM/DD/YYYY]

**Epic: [N — Name]** (#[rank] non-committed | or "Committed (contract [section])")
Adjusted Score: [x] | Leadership: [Mgr+Eng / Mgr / Eng / —]

Role in Epic: [1-2 sentences on what this idea covers within the epic]

Full roadmap: [planning doc link]
```

**E. Board view configuration (manual, one-time):**
The board view should be sorted by **Priority Score** desc — this is the field that holds the actual RICE-derived rank with contract override at 99.0. A standard tracker priority does NOT sort idea-board views. To set this up:
1. Open the view
2. Add "Priority Score" as a column
3. Set sort to "Priority Score" descending

Do NOT sort by any auto-computed "Impact score" — that field conflates priority with the Impact dimension. Use Priority Score for ranking.

Some tools' Rank field is tool-managed and not directly settable via API. Sorting by Priority Score is the supported path.

---

### Step 9.5: Update Product Ideas backlog (write-back)

For each idea-XXX referenced as an originating signal in any of this run's epics
(committed or non-committed), update the corresponding entry in
`~/.claude/product-ideas.yaml`:

- Set `status: in_roadmap`
- Set `related.epic_id` to the epic shortname (e.g., `epic-08-project-mgmt-platform`)
- If the idea also became a board idea (its content was material enough to file), set `related.epic_id` to that idea key

For ideas that were CONSIDERED but DEFERRED (in Step 6 they were lower-score
captures that didn't make an epic this run), leave their status as `captured`
but add a `notes` line: `Considered in /roadmap run [MM/DD/YYYY], deferred — [reason]`.

Use Python's `pyyaml` to read/write to preserve formatting and comments:
```python
import yaml
from pathlib import Path
p = Path.home() / ".claude" / "product-ideas.yaml"
data = yaml.safe_load(p.read_text())
for idea in data["ideas"]:
    if idea["id"] in promoted_ids:
        idea["status"] = "in_roadmap"
        idea["related"]["epic_id"] = epic_shortname_map[idea["id"]]
    elif idea["id"] in deferred_ids:
        idea["notes"] = (idea.get("notes", "") + "\n" +
                        f"Considered in /roadmap {today}, deferred — {reason_map[idea['id']]}").strip()
p.write_text(yaml.safe_dump(data, sort_keys=False, default_flow_style=False))
```

State:
```
PRODUCT IDEAS WRITE-BACK
Promoted to in_roadmap: [N ideas] — [idea-001, idea-003, ...]
Deferred (annotated): [N ideas] — [idea-002, ...]
Untouched (not referenced this run): [N ideas]
```

If `~/.claude/product-ideas.yaml` was not read in Step 3 (file missing or empty),
skip this step.

---

### Step 10: Write the Roadmap Planning Doc

Save to a temp file, then:
```bash
python3 ~/.claude/scripts/gdocs.py write \
  --doc-id {{PLANNING_DOC_ID}} \
  --file /tmp/roadmap-output.txt
```

**Document structure:**
```
{{COMPANY}} — Epic Roadmap
Last updated: [MM/DD/YYYY]
Sources: [N] meeting notes | Insights ([N] items) | [contract name + version]

============================================
PRODUCT COMMITTED SEQUENCE (from [source])
============================================

1. [Item] — [why committed]
2. [Item] — [why committed]
...

============================================
COMMITTED EPICS — [CONTRACT NAME] (CONTRACTUAL)
============================================

--------------------------------------------
EPIC C1 — [Name]
--------------------------------------------
Status: [In progress / pending acceptance / etc.]
Owner: [Name(s)]
Gate: [Acceptance condition]

Deliverables:
- [3.2.1] [Name] — [1-line description] ([tracker refs])
- [3.2.2] [Name] — ...

Board ideas contained: [idea-x, idea-y, ...]

--------------------------------------------
[Repeat for each committed epic]

============================================
NON-COMMITTED EPIC STACK RANK
============================================

| #  | Epic | Score | R | I | C | E | Lead | Ideas in Epic |
|----|------|-------|---|---|---|---|------|----------------|
| 1  | [Name] | [score] | [r] | [i] | [c]% | [e] | [Mgr+Eng] | idea-x, idea-y |
...

============================================
EPIC DETAILS
============================================

--------------------------------------------
EPIC 1 — [Name]
--------------------------------------------
Score: [x] | Leadership: [Mgr+Eng]
Ideas: [list]

Description:
[2-3 sentences]

In-scope features:
- [item]
- [item]
- [item with tracker ref if applicable]

Scoring:
  Reach: [r] — [rationale]
  Impact: [i] — [rationale]
  Confidence: [c]% — [rationale]
  Effort: [e] — [rationale]
  Leadership: [Mgr+Eng ×2.0]

Signals: [meetings + insight items + customer accounts]

[Repeat for each non-committed epic]

============================================
CHANGELOG — [MM/DD/YYYY] run
============================================

[List of changes — NEW / UP / DN / unchanged]

Tracker tickets filed this run (NOT on roadmap, listed for reference):
- [TICKET-xxxx] — [title]
```

---

### Step 11: Final Summary
```
EPIC ROADMAP UPDATED

Epics: [N total] = [committed count] committed + [non-committed count] ranked
Board ideas synced: [N]
Project board: labels + priority + comments updated
Board view sort recommendation: by Priority desc

Tracker tickets filed: [N]

TOP 5 EPICS (after committed)
#1 [Epic] — score [x]
#2 [Epic] — score [x]
...

[Planning doc link]
[Board view link]
```

---

## Quality Guidelines

- **Epic-level only** — if the work is a single feature or fix, it doesn't belong on the roadmap. It either goes inside an epic or to the issue tracker.
- **No bugs on the roadmap** — bugs live in the tracker. Reference them from inside an epic; never as a standalone roadmap item.
- **Contract commitments are non-negotiable** — they're contractual. Always above RICE.
- **Product-committed sequence overrides RICE within tiers** — when leadership says "X next, then Y", honor it as the tiebreaker.
- **An epic contains many ideas** — many-to-one is expected. Don't create an idea per feature inside an epic; reference existing ideas as components.
- **Score conservatively** — under-score and move up rather than inflating.
- **Effort is for the epic** — not a feature within it.
- **Triage old ideas** — if a legacy idea turns out to be a bug, label it `needs-triage` and recommend migration to the tracker.
- **Board is the snapshot, Doc is the depth** — collaborators see the board first; full context lives in the Doc.
- **Re-scoring is the point** — every run reflects new information.
