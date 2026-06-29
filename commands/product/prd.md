# /prd — Product Requirements Document Generator

## Description
Generate a PRD from your meeting notes library. Searches `~/.claude/meeting-notes/` for relevant
context, synthesizes product signals and decisions, and produces a structured, send-ready PRD draft.
Saves locally and to Google Drive (when connected).

## Usage
- `/prd` — interactive mode (asks for topic)
- `/prd [topic]` — generate PRD for a specific feature or topic
- `/prd [topic] from [meeting name or date]` — scope to one or more specific meetings

## Sources
This skill pulls context from two sources — use both every time:
1. **Meeting notes** — `~/.claude/meeting-notes/*.md` (decisions, action items, product signals)
2. **Product insights synthesis** — the Synthesis Doc written by `/insights`
   (`{{DOC_ID}}`) — customer feedback, feature requests,
   bug reports synthesized from the Customer Feedback Doc. If the doc is empty, note it and
   proceed with meeting notes only.

---

## Instructions

### Step 0: Identify Topic and Scope

If no argument provided, ask:
```
What should this PRD cover?

Provide a feature name, problem area, or topic (e.g., "Google Drive integration", "billing flow", "onboarding workflow").
You can also scope it to specific meetings: "Google Drive integration from the Acme kickoff meeting"
```

Confirm the topic back before proceeding:
```
Generating PRD: [Topic]
Searching meeting notes for relevant context...
```

---

### Step 0.5: Brainstorm Scope (collaborative dialogue)

Before searching meeting notes, run a scope-brainstorm pass (optional, if you use a brainstorming
tool) to pressure-test the problem framing through dialogue:
- What specific problem does this PRD actually solve?
- Who is the user? Which segment, which workflow?
- What's the simplest version that would ship value?
- What's tempting to include but actually scope creep?

This catches premise drift before you spend time mining meeting notes for a fuzzy topic.

**Skip Step 0.5 if:**
- The topic is highly scoped already (a single ticket, a single customer ask)
- {{YOUR_NAME}} explicitly says "skip brainstorm" or "I already know the scope"
- Otherwise: run it. The 5 minutes of dialogue saves 30 minutes of PRD revision.

Output: a refined topic statement + 3-5 framing bullets. Carry these into Step 1's search.

---

### Step 1: Source Relevant Meeting Notes

Scan ALL files in `~/.claude/meeting-notes/` for relevance to the topic.

**Search strategy — check these sections in each file (in order of relevance):**
1. `## Product Signals & Context` — highest signal, most PRD-relevant
2. `## Key Decisions` — captures resolved directions
3. `## Summary` — topic-level relevance check
4. `## Action Items` — surfaces commitments and next steps
5. `## Relationship Notes` — stakeholder context for requirements
6. `## Raw Transcripts` — verbatim detail if signals are thin

**Relevance scoring — include a file if it contains:**
- Direct mentions of the topic/feature
- Related pain points or user feedback
- Decisions that affect this feature area
- Action items related to this topic
- Stakeholder signals relevant to the feature

**If scope was specified** (e.g., "from the Acme kickoff meeting"), include that file plus any others
that have overlapping signals on the topic.

**Present source matches before generating:**
```
SOURCES FOUND — [count] relevant meeting notes

✅ [Date] — [Meeting Title]
   Relevance: [1-2 sentence explanation of what this meeting contributes]

✅ [Date] — [Meeting Title]
   Relevance: [...]

❌ [count] meetings scanned, no relevant signals found

Proceed with these sources? [Y] or adjust scope [specify]
```

Wait for confirmation before generating.

---

### Step 1b: Read Customer Feedback Synthesis

Fetch the insights Google Doc and extract any signals relevant to the PRD topic.

**Fetch via WebFetch:**
`https://docs.google.com/document/d/{{DOC_ID}}/export?format=txt`

- Follow any redirect and fetch the redirected URL
- Locate the `📊 Product Insights Synthesis` section (written by `/insights`)
- Scan for items relevant to the PRD topic — match by theme name, product area, item content, or customer mention
- Extract matching items (full content — do not truncate)

**If Synthesis tab is found and has relevant items:**
```
INSIGHTS DOC — [count] relevant items found

✅ INS-xxx — [type] — [customer/source] — [1-line summary]
✅ INS-xxx — [type] — [customer/source] — [1-line summary]
```

**If Synthesis tab is not found or doc is empty:**
```
⚠️ Insights doc has no Synthesis tab yet — run /insights to generate one.
Proceeding with meeting notes only.
```

**If no relevant items for this topic:**
```
Insights doc checked — no items matched "[topic]". Proceeding with meeting notes only.
```

---

### Step 1c: Supplementary Context (Optional)

Before generating, ask if there's context not captured in meeting notes:

```
SUPPLEMENTARY CONTEXT (optional)

Meeting notes loaded. Any additional context I should know before generating?

Examples: background you haven't written down, org dynamics, stakeholder concerns,
constraints, decisions that were made offline.

[Dump anything] or [Skip — proceed with meeting notes only]
```

If the user provides context, incorporate it into Step 2 synthesis alongside meeting notes.
If the user skips, proceed directly to Step 2.

---

### Step 2: Synthesize PRD Content

From confirmed meeting notes (Step 1) **and** insights items (Step 1b), extract and synthesize:

**Background & Problem:**
- What user pain points or friction were raised?
- What is the current state / what's broken?
- What triggered this feature discussion? (customer request, internal need, competitive signal)
- Which customers or personas were mentioned?

**Goals & Scope:**
- What outcomes were discussed?
- What success would look like?
- What was explicitly ruled out or descoped?

**Requirements:**
- What specific functionality was described or requested?
- What were the implementation options discussed?
- What technical constraints or dependencies were surfaced?

**Open Questions:**
- What was flagged as unresolved?
- What decisions are still pending?
- What clarifications were needed before committing?

**Stakeholders:**
- Who surfaced this need?
- Who owns it?
- Who needs to be consulted ({{ENG_LEAD}}, {{MANAGER}}, customers)?

---

### Step 3: Generate the PRD

Produce the full PRD document using this template:

```markdown
# PRD: [Feature Name]

**Status:** Draft
**Owner:** {{YOUR_NAME}}, [your role] — {{COMPANY}}
**Date:** [today's date MM/DD/YYYY]
**Last Updated:** [today's date]

---

## Background

[2-4 sentences: why this feature matters, what triggered it, and the current state.
Ground this in specific meeting context — not generic filler.]

## Problem Statement

[Clear, specific statement of the problem being solved.
Format: "Currently, [user/persona] experiences [problem] when [context]. This causes [impact]."
Pull from Product Signals & Context sections of meeting notes.]

## Goals

- [Goal 1 — specific and measurable where possible]
- [Goal 2]
- [Goal 3]

## Success Metrics

| Metric | Baseline | Target | Timeframe |
|--------|----------|--------|-----------|
| [metric] | [current state if known] | [goal] | [timeframe] |

[Note: Fill in baselines/targets with meeting context where available. Use TBD where unknown.]

## Scope

### In Scope
- [specific capability or behavior]
- [...]

### Out of Scope
- [explicit exclusion — especially things that came up but were deprioritized]
- [...]

## User Stories

### P0 — Must Have
- As a [user type], I want [capability] so that [outcome].
- [...]

### P1 — Should Have
- As a [user type], I want [capability] so that [outcome].
- [...]

### P2 — Nice to Have
- [...]

## Requirements

### Functional Requirements
| # | Requirement | Priority | Notes |
|---|-------------|----------|-------|
| F1 | [requirement] | P0/P1/P2 | [context from meeting] |
| F2 | [...] | | |

### Non-Functional Requirements
- [Performance, security, reliability, compatibility constraints if surfaced]

## Open Questions

| # | Question | Owner | Due | Context |
|---|----------|-------|-----|---------|
| 1 | [question] | [who] | [date] | [why it matters] |
| 2 | [...] | | | |

## Stakeholders

| Name | Role | Involvement |
|------|------|-------------|
| {{YOUR_NAME}} | PM / Owner | Author, decision-maker |
| [{{ENG_LEAD}}/{{MANAGER}}/other] | [role] | [Consulted / Informed / Approver] |
| [External stakeholder] | [role/company] | [relationship to this feature] |

## Meeting References

| Meeting | Date | Key Contribution |
|---------|------|-----------------|
| [Meeting Title] | [Date] | [What this meeting contributed to the PRD] |
| [...] | | |

## Appendix: Key Signals from Meetings

[Pull the most important direct quotes or signals from Product Signals & Context sections.
These ground the PRD in real customer/stakeholder voice rather than PM interpretation.]

> "[Direct quote or paraphrased signal]" — [Meeting Title], [Date]

> "[...]"
```

---

### Step 3.5: Persona Review (parallel sub-agents)

Before presenting the draft, run a multi-persona doc review (optional, if you use such a tool) to
surface role-specific holes the single-PM perspective misses.

**Reviewers to invoke:**
- **Engineer ({{ENG_LEAD}}'s lens)** — feasibility, dependencies, missing technical constraints
- **Designer** — UX flows that aren't specified, edge cases on the happy path
- **Customer-facing PM ({{MANAGER}}'s lens)** — does this actually solve the user pain? Strategic fit?
- **QA / support** — what breaks? What's the support load implication?

Each reviewer reads the draft cold and surfaces 2-3 issues. Output: a consolidated issue list
with confidence scores.

Present to {{YOUR_NAME}} before Step 4:
```
PERSONA REVIEW — [count] issues surfaced

🔴 BLOCKING ([count])
- [issue] — [reviewer] | [why it blocks]

🟡 WORTH ADDRESSING ([count])
- [issue] — [reviewer] | [recommendation]

🟢 NICE-TO-HAVE ([count])
- [issue] — [reviewer]

Address blocking issues before saving? [Y/N/skip]
```

If Y → loop back to Step 2 to incorporate fixes, then re-run Step 3.
If N or skip → proceed to Step 4 with issues noted in PRD's Open Questions table.

---

### Step 4: Review and Confirm

Present the full PRD draft and ask:
```
PRD DRAFT — [Feature Name]
[full document above]

---

Ready to save? Options:
[1] Save as-is
[2] Quick edit — tell me what to change
[3] Collaborative refinement — refine section by section (brainstorming + reader testing)
[4] Discard
```

Wait for explicit direction.

**If user selects [3] — Collaborative Refinement:**

Follow a doc-coauthoring workflow (Stage 2 + Stage 3):

**Stage 2 — Refinement & Structure:**
Work through each PRD section in order. For each section:
1. Ask 3-5 clarifying questions about what to include
2. Brainstorm 5-10 options/angles for that section
3. Ask which to keep, remove, or combine (shorthand ok: "1,3,5" or "drop 2 — already covered")
4. Check for gaps: "Anything important missing for [section]?"
5. Draft the section using `str_replace` — never reprint the whole doc
6. Refine iteratively based on feedback until the user is satisfied

Start with the section that has the most unknowns (usually Problem Statement or Requirements),
then work through the rest. Save summary/exec sections for last.

When 80%+ of sections are done, re-read the full doc and check for:
- Flow and consistency
- Redundancy or contradictions
- Any generic filler that doesn't add value

**Stage 3 — Reader Testing:**
After all sections are refined, launch a sub-agent with just the PRD content and ask it:
1. Generate 5-8 questions a reader would realistically ask about this feature
2. For each question, have the sub-agent answer using only the PRD (no conversation context)
3. Report what Reader Claude got right/wrong/misunderstood
4. Fix any gaps — loop back to Stage 2 for problematic sections
5. Repeat until Reader Claude consistently answers correctly

When reader testing passes, ask if ready to save or if any final changes are needed.
Then proceed to Step 5 (Save).

---

### Step 5: Save the PRD

**Always save locally first:**

Save to: `~/.claude/prds/YYYY-MM-DD-[feature-slug].md`

Create the `~/.claude/prds/` directory if it doesn't exist.

**Save to Google Docs via API:**

1. Save the full PRD content to a temp file: `/tmp/prd-[feature-slug].txt`
2. Run via Bash:
   ```
   python3 ~/.claude/scripts/gdocs.py create \
     --title "PRD: [Feature Name] — [MM/DD/YYYY]" \
     --file /tmp/prd-[feature-slug].txt
   ```
   The script prints the new doc URL on success.
   **First run only:** a browser window will open asking you to authorize Google Docs access. Log in and approve — the token is saved for all future runs.
3. Delete the temp file: `rm /tmp/prd-[feature-slug].txt`

**If the script fails:**
```
⚠️ Google Docs API error — saved locally only.
Local file: ~/.claude/prds/[filename].md
```

---

### Step 5.5: Generate Jira Epics and Stories

After saving the PRD, ask:
```
PRD saved. Generate Jira Epics and Stories in the {{JIRA_PROJECT}} backlog? [Y/N]
Creates one Epic per capability area + individual Stories for all P0/P1 requirements.
```

If confirmed, use a spec-to-backlog tool with this configuration:

**Project:** {{JIRA_PROJECT}}
**Board:** {{JIRA_BOARD_URL}}
**Sprint:** none — backlog only

#### Epic structure
One Epic per major In Scope capability area from the PRD.
- **Title:** [Feature Name] — [Capability Area]
- **Description:** PRD summary for this area + Google Docs PRD link

#### Story structure
One Story per P0/P1 user story or functional requirement. Link each to its parent Epic.

Every Story description must follow this format exactly:

```
**Given** [precondition — user context or current state]
**When** [user action or system trigger]
**Then** [expected user-facing outcome]
**And** [additional behavioral or system requirement — repeat as needed]

### Context & Strategy

[2-3 sentences: why this requirement matters, what problem it solves, PRD alignment]
PRD: [Google Docs URL]

### Acceptance Criteria

1. **[Requirement Group]**
   - [specific, testable requirement from PRD functional requirements]
   - Validation: [edge case handling]

2. **[Requirement Group]**
   - [specific requirement]

### Technical Notes

[Technical constraints, dependencies, or non-functional requirements from the PRD. Omit section if none.]
```

**Issue type mapping:**
| PRD requirement | Jira type |
|---|---|
| P0 / P1 user story or functional requirement | Story |
| Non-functional or infrastructure requirement | Task |

P2 requirements → skip (create manually if prioritized later).

After creating, report results and update the PRD's local file header with the Epic issue key:
```
JIRA BACKLOG CREATED — [count] issues

Epic: {{JIRA_PROJECT}}-xx — [Epic Title]
  ✅ {{JIRA_PROJECT}}-xx — [Story title] (P0)
  ✅ {{JIRA_PROJECT}}-xx — [Story title] (P0)
  ✅ {{JIRA_PROJECT}}-xx — [Story title] (P1)
  ...
```

---

### Step 6: Present Final Summary

```
✅ PRD CREATED — [Feature Name]

SOURCES USED
- [count] meeting notes synthesized
- [list of meetings]
- [count] insights items from Customer Feedback Doc (or "Insights doc not yet synthesized")

SAVED TO
- Local: ~/.claude/prds/[filename].md
- Google Drive: [link] ← (if connected)

OPEN QUESTIONS ([count])
[list the open questions with owners]

SUGGESTED NEXT STEPS
- [e.g., "Review with {{ENG_LEAD}} before sharing — F2 has a technical dependency on the current file system"]
- [e.g., "Confirm success metrics with {{MANAGER}}"]
- [e.g., "Schedule follow-up with the customer for requirements validation"]

Want me to add any open question follow-ups to my-tasks.yaml?
```

---

## PRD Quality Guidelines

- **Ground everything in meeting context** — no generic PM boilerplate. Every requirement should trace to a signal.
- **Name the customer** — if a specific customer raised it, say so. Specificity builds credibility.
- **Be explicit about tradeoffs** — if three implementation options were discussed, include them. Don't collapse decisions prematurely.
- **Flag assumptions** — if you're inferring a requirement rather than reading it directly, mark it ⚠️ Inferred.
- **Leave open questions open** — don't paper over unresolved issues. Surface them clearly with owners.
- **P0 should be small** — if everything is P0, nothing is. Push toward a tight must-have set.
- **Keep the background honest** — if this feature came from one customer request, say that. Don't over-index its importance.
