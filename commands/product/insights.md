# /insights — Product Insights Synthesizer

## Description
Reads all source tabs in a {{SOURCE_DOC}} (your customer-feedback Google Doc), groups content
by theme, and writes the full synthesis to a separate {{SYNTHESIS_DOC}} via the Google Docs API.
Source tabs are left untouched.

When adding a new source (`/insights add`), content is written directly to the {{SOURCE_DOC}}
as a new tab — no local staging step.

## Usage
- `/insights` — run full synthesis across all doc tabs, write back to the synthesis doc
- `/insights add [source]` — fetch a source and add it directly to the source doc
  - `[source]` can be: a meeting-notes URL, a Google Doc URL/ID, or omit to paste content manually
- `/insights add` — prompts for source type interactively

---

## Configuration

Set these once for your own workspace. Use placeholder values until you create the docs.

**{{SOURCE_DOC}} (customer-feedback source tabs):**
- ID: `{{DOC_ID}}`
- URL: `https://docs.google.com/document/d/{{DOC_ID}}/edit`

**{{SYNTHESIS_DOC}} (write destination):**
- ID: `{{DOC_ID}}`
- URL: `https://docs.google.com/document/d/{{DOC_ID}}/edit`

**Browser (optional):** a headless-browser tool (e.g. the `browse` skill) — used as a fallback
for any login-gated or JS-rendered pages.

> This skill assumes a small helper script at `~/.claude/scripts/gdocs.py` that can `read`
> and `write` Google Docs via the Docs API. Swap in your own read/write mechanism if you prefer.

---

## ADD MODE — `/insights add [source]`

Fetches external content and writes it directly to the {{SOURCE_DOC}} as a new tab.

### Step A1: Identify Source Type

Detect the source type from the argument:

| If argument is... | Source type |
|---|---|
| Meeting-notes URL or UUID format | Meeting note |
| Google Doc URL (`docs.google.com/...`) or 44-char ID | Google Doc |
| No argument | Ask interactively |

**If no argument**, ask:
```
What would you like to add?

[1] Meeting note — paste a share link or meeting ID
[2] Google Doc — paste a URL or doc ID
[3] Text — I'll paste the content directly
[4] Other URL — I'll paste a link to fetch

Type 1, 2, 3, or 4.
```

---

### Step A2: Fetch the Content

**Meeting note:**
- Extract the meeting UUID from the URL or argument
- First try your meeting-notes tool/MCP with the UUID
- If not found (shared note from another person's space): fetch the share URL directly via
  your browser/fetch tool
- Extract: title, date, attendees, summary, notes

**Google Doc:**
- Extract the doc ID from the URL or use the ID directly
- Fetch via Bash using the gdocs helper:
  ```
  python3 ~/.claude/scripts/gdocs.py read --doc-id "[URL_OR_ID]"
  ```
- Extract: doc title, full content

**Pasted text:**
- Accept the paste
- Ask: "What's the source/title for this content?" (e.g., "{{MANAGER}}'s floor-plan PRD")

**Other URL:**
- Fetch the page content and extract readable text

---

### Step A2b: Duplicate Check

Before writing anything, fetch the current {{SOURCE_DOC}} and check for duplicates.

**Fetch current doc:**
```
https://docs.google.com/document/d/{{DOC_ID}}/export?format=txt
```
Follow any redirect. Save the content — it will be reused in Step A3.

> Note: the `/export?format=txt` URL only works for link-shared docs. For private docs, read via
> the authenticated `gdocs.py read` path instead.

**Check for duplicates by source type:**

| Source | Check for |
|--------|-----------|
| Google Doc | Doc ID anywhere in the existing content |
| Meeting note | Meeting UUID anywhere in the existing content |
| URL | The full URL anywhere in the existing content |
| Pasted text | The title (from `TITLE:` lines) in existing `TITLE:` lines |

**If a match is found — stop:**
```
DUPLICATE DETECTED

This source has already been added:
  Title: [matched title]
  Added: [ADDED: date from existing entry]

Skipping to prevent duplicate. Run /insights to re-synthesize with existing sources.
```

**If no match — proceed to Step A3.**

---

### Step A3: Write Directly to the Source Doc

Format the content and append it to the {{SOURCE_DOC}} using the Google Docs API.

**Section header format** (appended to the end of the doc):
```
[meeting] — [Title] ([Date])
[gdoc] — [Title]
[manual] — [Label]
[url] — [Title]
```

**Content format:**
```
SOURCE: [Meeting / Google Doc / Paste / URL]
ID: [doc ID / meeting UUID / URL — used for duplicate detection]
TITLE: [Title]
DATE: [Date if known, else today]
AUTHOR/ATTENDEES: [If known]
ADDED: [Today's date]

---

[Full content — do not truncate]
```

**Steps to append to the source doc:**
1. Use the doc content already fetched in Step A2b
2. Append the new section header + formatted content to the existing content
3. Save the full updated content to `/tmp/insights-add-[slug].txt`
4. Write back via Bash:
   ```
   python3 ~/.claude/scripts/gdocs.py write \
     --doc-id {{DOC_ID}} \
     --file /tmp/insights-add-[slug].txt
   ```
5. `rm /tmp/insights-add-[slug].txt`

---

### Step A4: Confirm

```
SOURCE ADDED TO DOC

Tab name: [tab name]
Content length: ~[word count] words
Source: [type]

Added directly to: https://docs.google.com/document/d/{{DOC_ID}}/edit

Run synthesis now? [Y/N]
```

If Y → proceed to full synthesis (Step 1 onward).
If N → stop here.

---

## SYNTHESIS MODE — `/insights`

### Step 0: Check Sources

```
SOURCES CHECK
- Source doc: reading via doc export / Docs API
- Synthesis doc: writing via gdocs.py (Google Docs API)
- gdocs.py: [available / not available — synthesis will be saved locally if missing]
```

---

### Step 1: Read All Sources from the Source Doc

Fetch the {{SOURCE_DOC}}:
`https://docs.google.com/document/d/{{DOC_ID}}/export?format=txt`
Follow any redirect and fetch the redirected URL (or use `gdocs.py read` for private docs).

- Identify distinct source sections by their tab-name headers:
  - `[meeting] —` → Meeting note
  - `[gdoc] —` → Google Doc
  - `[manual] —` → Manually added
  - `[url] —` → Fetched URL
  - All other sections → Email (legacy format)
- Skip any section that is a previous "Synthesis" output

State what you found:
```
SOURCES LOADED
Doc tabs found: [count]
  — Email tabs: [count]
  — Meeting tabs: [count]
  — GDoc tabs: [count]
  — Other: [count]

Total sources to process: [count]
```

---

### Step 1.5: Behavioral Pulse Cross-Reference (optional)

Before extracting items from the doc, pull the most recent 14-day behavioral digest from your
product-analytics stack (e.g. a product-analytics tool, an event router, and a web-traffic tool).
If your tickets carry "metric considerations" defining what to capture, the pulse aggregates that
into product-insight signal.

**How to fetch:**
1. Email search: look for the latest weekly analytics digest (e.g. `from:noreply@<your-analytics>.com newer_than:14d`)
2. If a saved analytics-board URL is in your config, fetch it via your browser/fetch tool
3. Manual paste — ask: "Paste the 14d behavioral summary, or skip the behavioral cross-reference for this synthesis?"

**Capture from the pulse:**
- Top usage patterns by feature/area
- Quality regressions or error spikes
- Adoption deltas on recently shipped capabilities
- Behaviors that contradict reported feedback ("users complained X is hard but adoption is high")

**Why this matters for synthesis:**
The strongest insight signal is the *gap* between what users say and what they do.
Customer feedback alone tells you what's salient. Behavior alone tells you what's adopted.
The two together tell you what's true.

**Tag pulse-derived items as a new source type:**
- Source type: `behavior`
- Customer/Source: `Analytics — last 14d` (or whichever stack source the data came from)
- Allow these to be assigned to themes alongside doc-derived items

**If pulse data isn't available** (no digest, no manual paste), skip gracefully and note
"Behavioral pulse: unavailable — synthesis based on customer feedback only" in the SOURCES LOADED block.

---

### Step 2: Extract and Tag Each Item

For every source section, extract a **compact record only** — do NOT reproduce full raw text here.
Raw content is preserved separately in the source doc.

**Item fields:**
- **ID:** Sequential (INS-001, INS-002, ... — a simple, stable numbering convention)
- **Source:** Tab/section name
- **Source type:** `email` / `meeting` / `gdoc` / `manual` / `url` / `behavior`
- **Summary:** 1–2 sentence distillation of the signal — enough to act on
- **Type:** Classify as one of:
  - `feature_request` — something new the product should do
  - `bug_report` — something broken or behaving incorrectly
  - `ux_friction` — friction or confusion, not necessarily a bug
  - `task` — specific action item for the team
  - `feedback` — general feedback, praise, or concern without a clear ask
  - `vision` — future-state or strategic direction items
  - `prd_signal` — structured product requirement or design direction (common in meeting/GDoc sources)
- **Product area:** Best-fit from your own product taxonomy. Define a short list of areas for your
  product (e.g. Core Workflow, Reporting / Analytics, Mobile, Permissions / Access,
  Billing / Subscriptions, UX / UI Polish, Integrations, Other).
- **Customer/Source:** Who raised it (name, company, or "internal")
- **Priority signal:** `high` / `medium` / `low`

**Do not store or re-emit full raw content during this step.**

---

### Step 3: Group by Theme

Group all items into 4–8 themes that emerge from the content.

**Good themes are:**
- Specific enough to be actionable ("Task list interaction patterns" not "UX")
- Named from the customer's perspective, not engineering's
- Scoped so each maps to a potential feature or initiative

Assign every item to its primary theme. An item can appear in multiple themes if genuinely relevant to both.

---

### Step 4: Generate the Synthesis Content

Build the synthesis document using **summaries only** — no raw content. This keeps the synthesis
scannable and token-efficient.

```
Product Insights Synthesis
Last updated: [MM/DD/YYYY]
Sources consolidated: [count] ([email count] emails, [meeting count] meetings, [gdoc count] GDocs)
Total items: [count]
Source doc: https://docs.google.com/document/d/{{DOC_ID}}/edit

---

EXECUTIVE SUMMARY

[3-5 sentences. What are the loudest signals? What themes dominate? Any urgent items?
Write as a PM briefing — narrative, not a list.]

---

========================================
THEMES
========================================

----------------------------------------
Theme: [Name]
Items: [count] | Types: [breakdown] | Signal: High/Medium/Low
----------------------------------------

[2-3 sentence synthesis of what's being said about this theme — pattern, driver, ask.]

ITEMS IN THIS THEME:

> INS-001 | [type] | [customer/source] | [priority]
[1-2 sentence summary of the signal]

> INS-002 | [type] | [customer/source] | [priority]
[1-2 sentence summary]

[repeat for all items in theme]

[...repeat for all themes]

---

========================================
QUICK REFERENCE — ITEMS BY TYPE
========================================

BUG REPORTS ([count])
INS-xxx | [summary] | [source] | [priority] | Theme: [name]

FEATURE REQUESTS ([count])
INS-xxx | [summary] | [source] | [priority] | Theme: [name]

PRD SIGNALS ([count])
INS-xxx | [summary] | [source] | [priority] | Theme: [name]

UX FRICTION ([count])
INS-xxx | [summary] | [source] | [priority] | Theme: [name]

TEAM TASKS ([count])
INS-xxx | [summary] | [source] | [priority] | Theme: [name]

FEEDBACK ([count])
INS-xxx | [summary] | [source] | [priority] | Theme: [name]

VISION ITEMS ([count])
INS-xxx | [summary] | [source] | [priority] | Theme: [name]
```

**Do not include raw source content in the synthesis.** Items carry a summary line only.

---

### Step 5: Write Synthesis to the Synthesis Doc (gdocs.py)

The synthesis is written to a **separate dedicated doc** — the source tabs in the {{SOURCE_DOC}}
are left completely untouched.

1. Save synthesis content to: `/tmp/insights-synthesis.txt`
2. Run via Bash:
   ```
   python3 ~/.claude/scripts/gdocs.py write \
     --doc-id {{DOC_ID}} \
     --file /tmp/insights-synthesis.txt
   ```
   The script prints the doc URL on success.
   **First run only:** a browser window will open asking you to authorize Google Docs access. Log in and approve — the token is saved for all future runs.
3. `rm /tmp/insights-synthesis.txt`

**If the script fails:**
- Save synthesis to `/tmp/insights-synthesis-[date].txt` and tell the user the error.

---

### Step 6: Present Summary

```
INSIGHTS SYNTHESIS COMPLETE

Sources consolidated: [count]
  — [count] email tabs
  — [count] meeting notes
  — [count] Google Docs
Items extracted: [count]
Themes identified: [count]

TOP THEMES
1. [Theme name] — [count] items | [signal]
2. [Theme name] — [count] items | [signal]
3. [Theme name] — [count] items | [signal]

URGENT ITEMS ([count] flagged high)
- INS-xxx: [summary] ([type], [source])

DOC STATUS
Synthesis written to the synthesis doc
Source tabs in the source doc: untouched

https://docs.google.com/document/d/{{DOC_ID}}/edit

Run /prd [topic] to generate a PRD from these insights.
```

---

## Quality Guidelines

- **Summaries only in synthesis** — themes, INS-IDs, and 1-2 sentence items. Never put full raw text in the synthesis doc.
- **Synthesis is not a replacement** — the synthesis paragraph tells the story; the raw items below are the evidence. Both required.
- **Don't collapse nuance** — if two sources said different things, keep both items separately.
- **Flag cross-source frequency** — "Raised in 3 emails + {{MANAGER}}'s 03/03 meeting note" is a strong signal.
- **Attribute source type** — a request from a customer call carries different weight than an internal doc.
- **Be honest about priority** — reserve `high` for explicit urgency, key customers, or repeated mentions.
- **Write for the PRD agent** — full item content is how `/prd` finds relevant signals. Be specific.
- **Name themes from outcomes** — "Users can't find vendor history" beats "Navigation issues."
