# /idea — Product Idea Capture

## Description

Capture, score, and shepherd product ideas through the pipeline. Lives in the gap
between raw meeting notes and `/roadmap-edit` — ideas get a structured home so they
don't disappear into the void between conversations and the roadmap board.

Plain-language orchestration: just describe what you know or want to change. The
skill figures out the right action(s) automatically.

## Storage

**File:** `~/.claude/product-ideas.yaml`
**Archive:** `~/.claude/product-ideas-archive/<YYYY-MM>.yaml` (dropped / shipped items, mirrors my-tasks.yaml pattern)

## Schema (per idea)

```yaml
- id: "idea-001"                # auto-assigned, monotonic
  title: "Add financing-plan funnel"
  captured: "2026-06-15"        # ISO date
  source:                       # where this came from
    type: "meeting"             # meeting | slack | email | customer_call | own_thought | external
    reference: "2026-06-08-team-sync.md"   # filename, URL, or descriptor
    quote: "Revenue = success fees on approved plans."  # verbatim if applicable
  rationale: |
    Financing planning emerged as the primary customer ask and a new monetization
    model in our largest segment. No existing product surface for it yet.
  target_icp: "segment-a"       # segment-a | segment-b | enterprise | smb | greenfield | all
  p_lever: "revenue"            # revenue | retention | expansion | margin | activation
  impact: "large"               # small | medium | large
  status: "captured"            # captured | scoped | in_roadmap | in_prd | shipped | dropped
  score:                        # 4-lens P-score
    stakeholder_pull: 5         # 1-5
    strategic_fit: 5
    time_pressure: 4
    leverage_multiplier: 5
    composite: 19               # sum, auto-computed
  related:
    epic_id: null               # optional roadmap epic link
    prd_url: null               # optional PRD URL once promoted
    metric_suggestion_id: null  # optional cross-link to a metrics-suggestions file
  notes: |
    Pairs with a related metric suggestion. Ties into your standing strategy rules
    in CLAUDE.md.
```

## Usage

```
/idea [anything — plain language or explicit sub-command]
```

The skill detects intent automatically. Examples that all work:

- `/idea add financing-plan funnel`
- `/idea our manager wants us to track approval rates`
- `/idea from-meeting 2026-06-08-team-sync.md`
- `/idea sweep` — scan last 14 days of meeting notes for new ideas
- `/idea promote idea-001 to roadmap` — feed into `/roadmap-edit`
- `/idea promote idea-001 to PRD` — call `/prd` with that idea as scope
- `/idea score idea-001` — re-evaluate scoring
- `/idea drop idea-007: too speculative for now`
- `/idea search financing` — find matching ideas
- `/idea` (no args) — show current ranked backlog

## Sub-command behaviors

### `add` (or implicit from natural-language description)
1. Parse the description for: title, source (if a meeting/slack reference is mentioned), rationale, ICP, P&L lever, impact size
2. Ask for any missing required field interactively (or proceed with sensible defaults flagged as `inferred`)
3. Auto-assign next `id` (idea-XXX)
4. Auto-compute initial `score` from heuristics (high stakeholder = founder ask, customer ask; high strategic_fit = aligned with your standing strategy rules in CLAUDE.md; high time_pressure = explicit deadline; high leverage_multiplier = compounds with existing work)
5. Write to `product-ideas.yaml`
6. Echo the captured entry back for review

### `sweep`
1. Read all `~/.claude/meeting-notes/*.md` from the last 14 days
2. Look for product-idea signals (NOT customer-feedback — that's /insights). Signals:
   - Explicit phrases: "we should build", "what if we", "could we do", "needs a feature for", "missing capability"
   - Decisions that imply new product work
   - Customer asks that point at a new surface
   - Strategic shifts that demand new functionality
3. Deduplicate against existing entries in `product-ideas.yaml` (compare by title similarity)
4. Propose 1-5 high-quality new captures with verbatim quotes — every proposal MUST have a quote, or it's dropped
5. Show the proposals; user confirms which to add

### `promote <id> to roadmap`
1. Read the idea
2. Hand off to `/roadmap-edit add <title> — <rationale>` with the idea's metadata as input
3. Update idea `status: in_roadmap` and link `related.epic_id` to the roadmap entry

### `promote <id> to PRD`
1. Read the idea
2. Hand off to `/prd <title>` with the idea's rationale and source meeting as scope
3. Update idea `status: in_prd` and link `related.prd_url`

### `score <id>`
Re-evaluate the 4-lens score using current strategy / goals context. Useful when:
- A new customer signal raises stakeholder_pull
- A strategy update changes strategic_fit
- A deadline becomes explicit (raises time_pressure)
- A new dependency clears (raises leverage_multiplier)

### `drop <id>: <reason>`
Move to `~/.claude/product-ideas-archive/<YYYY-MM>.yaml` with `closed_at` + `close_reason`. Removes from live list.

### `(no args)` / list mode
Show top 10 ideas by `score.composite`, with: id, title, source, status, score. Optionally filter by status (`/idea in_roadmap`, `/idea captured`).

## Quality guardrails

1. **Every idea must trace to a source.** If you can't cite a meeting / customer call / explicit thought-source, the idea isn't ready. The schema requires `source`.
2. **Sweep mode requires verbatim quotes.** No quote, no auto-proposal.
3. **Dedupe is on.** Before adding, check existing titles for similarity. Don't create idea-007 if idea-002 already covers it — instead, update idea-002.
4. **Confirm before writing on `sweep`.** Auto-proposals always show user for accept/reject before disk write.
5. **Ideas are not Jira tickets.** They are pre-roadmap candidates. The path to delivery is: idea → roadmap (epic) → PRD → Jira.

## Connections to other skills

| Skill | How it connects |
|---|---|
| `/meeting` | Writes meeting notes that `/idea sweep` reads |
| `/insights` | Customer feedback synthesis. Different lane — feedback informs ideas but doesn't replace them. |
| `/roadmap` | Reads `~/.claude/product-ideas.yaml` as one of its input sources during full epic runs |
| `/roadmap-edit` | Target of `/idea promote idea-X to roadmap` |
| `/prd` | Target of `/idea promote idea-X to PRD` |
| Metric Scoreboard | Parallel pipeline for METRICS, not ideas. Cross-links via `related.metric_suggestion_id` when an idea also implies a measurement gap. |
| `work-tracker` | Reads `product-ideas.yaml` to surface high-score `captured` ideas during daily planning |

## How `/roadmap` should treat the ideas file

When `/roadmap` runs (full epic refresh), it should:
1. Read `~/.claude/product-ideas.yaml` alongside meeting notes + Synthesis Doc
2. Group ideas under candidate epics by theme / target_icp / lever
3. Surface high-composite-score `captured` ideas as candidates for promotion to the roadmap board
4. If a `captured` idea already maps to an existing roadmap epic, suggest linking (don't auto-link)

(This integration requires a small update to `/roadmap` to read the new file. Flag to {{YOUR_NAME}} when first invoking.)

## Defaults & conventions

- `id`: auto-incremented `idea-001`, `idea-002`, ...
- `captured`: ISO date (today)
- `source.type`: required; if missing from natural language, default to `own_thought` and flag
- `target_icp`: required; if missing, default to `all` and flag
- `p_lever`: required; one of the 5 explicit values (mirrors your P&L lens)
- `impact`: required; small / medium / large
- `status`: defaults to `captured`
- `score.composite`: auto-computed from the four 1-5 sub-scores (sum)

## What this skill does NOT do

- It does NOT write Jira tickets. That's downstream of /prd.
- It does NOT auto-promote to /roadmap-edit. The user must say "promote idea-X."
- It does NOT capture metric suggestions. That's the scoreboard's job.
- It does NOT capture customer feedback. That's `/insights add`.
- It does NOT replace the strategic-thinking layer. It's a structured capture point, not a decision-maker.
