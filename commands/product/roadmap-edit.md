# /roadmap-edit — Roadmap Editor

## Description
Lightweight roadmap editing tool with an orchestration layer. Just describe what you know
or want to change in plain language — the skill determines the right action(s) automatically.

Handles: adding new features, updating scores with new signals, manual overrides, linking PRDs,
archiving features, and batch edits across multiple features in a single pass.

Use this when:
- A customer call surfaces a new feature request
- A new signal changes confidence or leadership status for an existing feature
- You want to manually override a score component
- You want to link a PRD, mark something complete, or remove a feature
- You have a mix of updates from a meeting or conversation

Use `/roadmap` (full run) instead when:
- New meeting notes have been added to `~/.claude/meeting-notes/`
- The insights synthesis doc has been updated
- Significant time has passed and you want a full re-evaluation from all sources

## Usage
```
/roadmap-edit [anything — plain language or explicit sub-command]
```

**Plain language (orchestrated):**
- "Just got off a call with a customer — they said GL codes are blocking their Q2 expansion"
- "My manager wants to bump Mobile to Q2 and confirmed it's now a joint priority with the eng lead"
- "Remove the proof-of-concept — we decided not to move forward. Link PRD to {{PRODUCT}}: https://..."
- "New feature: auto-renewal reminders for expiring contracts. Low effort, the eng lead mentioned it."

**Explicit sub-commands (optional shortcuts):**
- `/roadmap-edit add [description]`
- `/roadmap-edit update [feature]: [signal]`
- `/roadmap-edit set [feature]: [field] = [value]`
- `/roadmap-edit link-prd [feature]: [URL]`
- `/roadmap-edit remove [feature]: [reason]`
- `/roadmap-edit` (no args) — show current stack rank

---

## Configuration

Fill these in for your own setup. Anything in `{{...}}` is a placeholder.

**Planning Doc ID:** `{{PLANNING_DOC_ID}}`
**Planning Doc URL:** `{{PLANNING_DOC_URL}}` (your roadmap doc)

**Ideas board (idea/feature tracker):**
- Project key: `{{BOARD_PROJECT_KEY}}`
- Issue type: Idea (or your tool's equivalent)
- Board URL: `{{BOARD_URL}}` (your project board)

---

## Scoring Framework (same as /roadmap)

### RICE Formula
```
RICE Score = (Reach × Impact × Confidence) / Effort
Adjusted Score = RICE Score × Leadership Multiplier
```

### Reach (1–10)
| Score | Meaning |
|-------|---------|
| 1–2 | Niche — affects <10% of users |
| 3–4 | Moderate — affects 10–30% |
| 5–6 | Common — affects 30–60% |
| 7–8 | Broad — affects 60–80% |
| 9–10 | Universal — affects >80% |

### Impact (0.25 / 0.5 / 1 / 2 / 3)
| Score | Meaning |
|-------|---------|
| 0.25 | Minimal |
| 0.5 | Low |
| 1 | Medium |
| 2 | High |
| 3 | Massive |

### Confidence (30% / 50% / 80% / 100%)
| Score | Meaning |
|-------|---------|
| 100% | Strong — multiple sources, customer-confirmed, leadership-aligned |
| 80% | Good — 2+ meeting mentions or insights entries |
| 50% | Hypothesis — single source |
| 30% | Speculative — assumed need |

Boosters (+10% each, cap at 100%):
- Mentioned in 2+ sources
- External customer explicitly requested it
- Appeared in product insights doc
- Both manager and eng lead mentioned it

### Effort (1–20)
| Size | Units |
|------|-------|
| XS | 1 |
| S | 2 |
| M | 5 |
| L | 10 |
| XL | 20 |

### Leadership Multiplier
| Signal | Multiplier |
|--------|-----------|
| Both manager AND eng lead | ×2.0 |
| Manager OR eng lead | ×1.5 |
| Neither | ×1.0 |

---

## Instructions

### Step 0: Orchestrate

Read the user's full input (everything after `/roadmap-edit`) and produce an operation plan
before doing anything else.

#### 0a — Classify each operation

Parse the input for distinct operations. A single input may contain multiple:

| Operation | Trigger signals |
|-----------|----------------|
| **add** | New feature not on current roadmap; "new feature", "add", unknown feature name |
| **update** | Existing feature + new signal (customer feedback, leadership mention, new source) |
| **set** | Explicit field change ("bump effort to M", "set confidence to 80%", "change reach to 7") |
| **link-prd** | URL provided alongside a feature name |
| **remove** | "remove", "archive", "deprioritize permanently", "we're not doing X" |
| **view** | No args, or "show me", "what's the current rank" |

#### 0b — Flag if a full `/roadmap` run is more appropriate

Recommend `/roadmap` instead if the user's input indicates:
- Multiple new meeting notes exist that haven't been processed
- The insights synthesis doc has been updated
- "A lot has changed" or "re-evaluate everything"

If flagging, say:
```
This sounds like it warrants a full /roadmap run rather than a targeted edit.
Reason: [why — e.g., "you mentioned 3 new meeting notes"]
Proceed with /roadmap-edit anyway? [Y/N]
```

Wait for confirmation before continuing.

#### 0c — Confirm the operation plan

Before reading the roadmap doc or doing any scoring, output the plan and wait for approval:

```
OPERATION PLAN
--------------
[count] operation(s) detected:

1. [OPERATION TYPE] -> [Feature name or "new feature"]
   "[quoted excerpt of the relevant input that triggered this]"

2. [OPERATION TYPE] -> [Feature name]
   "[quoted excerpt]"

Correct? [Y] to proceed / [N] to adjust
```

If any operation is ambiguous (e.g., feature name not clearly identifiable, unclear if
add vs. update), flag it inline:
```
Ambiguous: "[excerpt]"
   Interpreted as: [operation] on [feature]
   Correct this before confirming if wrong.
```

**Do not read the roadmap doc or do any scoring until the user confirms the plan.**
If the user corrects an interpretation, update the plan and show it again before proceeding.

---

### Step 1: Read Existing Roadmap

Fetch the current roadmap doc (e.g. via `python3 ~/.claude/scripts/gdocs.py read --doc-id {{PLANNING_DOC_ID}}`, or your tracker's export URL).

Extract:
- Full stack rank table (all features, scores, ranks)
- Feature details for the specific feature(s) being edited (existing scores, sources, descriptions)

State what you found:
```
ROADMAP LOADED — [count] features, last updated [date]
Target feature: [name] at #[rank] (score: [x]) — OR — New feature: [name]
```

---

### Step 2: Apply the Edit

#### For `add`:
Score the new feature using the RICE framework. Use ONLY the context provided by the user
in their command — do not read meeting notes or the insights doc.

Show the scoring reasoning explicitly:
```
NEW FEATURE: [Name]
-------------------------------------
Description: [what it does, from user context]

Reach: [score] — [rationale]
Impact: [score] — [rationale]
Confidence: [score]% — [rationale + any boosters applied]
Effort: [score] — [T-shirt size + rationale]

RICE Score: ([R] × [I] × [C]) / [E] = [score]
Leadership: [Manager / Eng Lead / Both / Neither]
Multiplier: [×2.0 / ×1.5 / ×1.0]
Adjusted Score: [final]

Inserts at: #[rank] (between [feature above] and [feature below])
```

#### For `update`:
Show the before and after for every field that changes:
```
UPDATING: [Feature Name] (currently #[rank], score: [x])
-------------------------------------
New signal: [what the user provided]

Changes:
  [Field]: [old value] → [new value]
    Reason: [why this signal changes this field]
  [Field]: [old] → [new]
    ...

Old score:  [old adjusted score]
New score:  [new adjusted score]
Rank move:  #[old] → #[new] (or "unchanged")
```

#### For `set`:
Apply the override directly. Show the change:
```
OVERRIDE: [Feature Name]
  [Field] set to [value] (was [old value])
  New score: [recalculated adjusted score]
  Rank move: #[old] → #[new]
```

#### For `link-prd`:
Update the PRD field for the feature:
```
PRD LINKED: [Feature Name]
  PRD: [URL]
```
No re-scoring needed. Update the PRD field in the Feature Details section only.

#### For `remove`:
```
REMOVING: [Feature Name] (currently #[rank], score: [x])
Reason: [user-provided reason]
This feature will be struck from the stack rank and moved to an ARCHIVED section.
```

#### For `view`:
Print the current stack rank table from the doc. No edits.

---

### Step 3: Show Proposed Changes

Before writing, summarize ALL operations in one consolidated diff. Never write to the doc
without showing this first and getting confirmation.

```
PROPOSED CHANGES — [count] operation(s)
----------------------------------------
1. [ACTION] [Feature name]
   Score: [old] → [new] | Rank: #[old] → #[new]
   [or: PRD linked | or: Archived]

2. [ACTION] [Feature name]
   Score: [old] → [new] | Rank: #[old] → #[new]

[Any ambiguity flags from Step 0c, restated here]

Proceed? [Y] to write all / [N] to adjust
```

Wait for confirmation before writing. If the user corrects an interpretation, re-apply
that operation with the correction and show the updated proposed change before writing.

---

### Step 3.5: Sync to Ideas Board

After the user confirms, sync the affected feature(s) to the ideas board in parallel
with Step 4 — do not block the planning-doc write on the board sync.

**For `add`:**
Search existing ideas for a title match first (e.g. `project = {{BOARD_PROJECT_KEY}} AND issuetype = Idea`).
- If a match exists: add a comment with the new score context
- If no match: create a new Idea
  - Summary: [feature name — concise]
  - Description: what it does, why it was added, RICE score, signal source
  - Priority: score ≥ 6 → High | 3–6 → Medium | <3 → Low
- Record the idea key and include it in the planning-doc stack rank table (board key column)

**For `update` or `set`:**
If the feature already has a board key in the doc:
- Add a comment to that idea with the updated score and reason for change
If no key is recorded yet:
- Search for a match and add a comment, or create if not found

**For `remove`:**
If the feature has a linked idea, add a comment: "Removed from roadmap — [reason]"
Do not delete or archive the idea — that's a manual decision.

**For `link-prd`:**
No board action needed — PRD link is planning-doc only.

---

### Step 4: Write Updated Doc

Reconstruct the full document with the edit applied:

1. **Stack rank table** — re-sorted by adjusted score; update rank numbers and scores
2. **Changelog** — append a new entry for this edit:
   ```
   ============================================
   CHANGELOG — [MM/DD/YYYY] edit
   ============================================
   [action] [Feature] — [what changed] (score: [old →] [new], rank: #[old] → #[new])
   Source: [user-provided context summary]
   ```
3. **Feature Details** — update the affected feature's entry; add new entry for new features;
   strike through or move to ARCHIVED section for removed features

Save to a temp file, then:
```
python3 ~/.claude/scripts/gdocs.py write \
  --doc-id {{PLANNING_DOC_ID}} \
  --file /tmp/roadmap-edit-output.txt
```

Delete the temp file after: `rm /tmp/roadmap-edit-output.txt`

---

### Step 5: Confirm

```
ROADMAP UPDATED — [count] change(s)

[action] [Feature name] — [one-line summary]
   [Score: x → y | Rank: #old → #new] OR [PRD linked] OR [Archived]

[action] [Feature name] — [one-line summary]
   [...]

[Doc link]
```

---

## Quality Guidelines

- **Only use user-provided context** — do not read meeting notes or the insights doc.
  If the user references a customer or meeting, use their description as the signal source.
- **State your assumptions** — if the user's context is thin, flag what you're estimating
  and suggest they validate before the next `/roadmap` full run.
- **Score conservatively** — better to under-score and move up on new evidence.
- **Re-sort the full table** — even if only one feature changes score, all rank numbers
  must be correct in the output.
- **Preserve all existing feature details** — only modify the section(s) relevant to the edit.
  Do not truncate, summarize, or rewrite untouched features.
- **Leadership signal is explicit only** — "my manager mentioned it" in user context counts.
  Do not infer leadership endorsement.
