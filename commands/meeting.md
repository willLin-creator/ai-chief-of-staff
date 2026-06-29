# /meeting — Post-Meeting Processing

## Description
Process a meeting after it ends: pull transcripts from Granola and/or Fireflies,
cross-reference both sources into one comprehensive summary, extract action items,
draft follow-up messages to owners, and save to your context library.

## Usage
- `/meeting` — choose mode interactively
- `/meeting recent` — process the most recent meeting
- `/meeting [name or partial title]` — process a specific meeting by name
- `/meeting add [Granola URL]` — process a specific shared meeting by URL
- `/meeting all` — process all unprocessed meetings in batch

---

## Instructions

### Step 0: Determine Mode

If no argument is provided, ask:
```
How would you like to run this?

[1] Most recent meeting
[2] Specific meeting — I'll search by name
[3] All unprocessed meetings (batch mode)

Type 1, 2, or 3.
```

**For mode [2]:** Ask "Which meeting?" and search Granola/Fireflies by title or date.

**For mode `add [URL]`:** Extract the meeting UUID from the Granola URL path (`/d/[UUID]`), fetch via Granola `get_meeting_transcript`, and proceed through Steps 1–7. If the transcript response does not include a date, look up the share email in Gmail (`from:granola.ai [title]`) to determine the meeting date before saving. The pre-save duplication check in Step 6 still applies — never skip it on this path.

**For mode [3] — Batch mode:**
- Default lookback window: **3 days** (today minus 3 days). Only fetch meetings within this range.
- If the user passes a number after `all` (e.g., `/meeting all 7`), use that as the lookback in days instead.
- If the user passes `all-time`, fetch all meetings with no date limit.
- Fetch meetings from Granola (and Fireflies if connected) within the lookback window
- Check `~/.claude/meeting-notes/` to see which meetings have already been processed
  (a file exists for that meeting date + title slug)
- Build a list of unprocessed meetings within the window, sorted oldest → newest
- Show the window used and confirm before processing:
  ```
  UNPROCESSED MEETINGS ([count]) — last [N] days ([start date] → today)
  1. [Date] — [Title]
  2. [Date] — [Title]
  ...

  Process all [count] meetings? This will create summaries, extract action items,
  and draft follow-up messages for each. [Y/N]
  (To extend the window, reply with a number of days or "all-time".)
  ```
- Process each meeting sequentially through Steps 1–6
- After each meeting, show a compact summary and pause:
  ```
  ✅ [Title] — done. ([n] of [total])
  Action items: [count] | Tasks added: [count] | Messages drafted: [count]

  Continue to next? [Y] or stop here [N]
  ```
- After all meetings processed, show a combined final summary (Step 7 batch version)
- Collect ALL draft messages across all meetings and present them together for approval at the end

---

### Step 1: Fetch from All Available Sources

Attempt to pull content from every connected source in parallel. Collect whatever is available.

**Source A — Granola (preferred, AI-enhanced notes):**
- If Granola MCP is connected: fetch the most recent meeting (or named meeting)
- Extract: title, date, attendees, Granola summary, Granola notes, chapters if available

**Source B — Fireflies (full transcript):**
- If Fireflies MCP or API is connected: fetch the matching meeting transcript
- Match by: meeting title, date, or attendee overlap
- Extract: full transcript, Fireflies AI summary, action items Fireflies detected, speaker labels

**Source C — Manual paste (fallback):**
- If neither MCP is connected, or if only one source found, ask:
  "I found [X] from [source]. Do you have a [Granola/Fireflies] transcript to paste as well? Or should I proceed with what I have?"
- Accept paste and proceed

**Source availability summary — state clearly what was found:**
```
SOURCES FOUND
- Granola: ✅ [meeting title] / ❌ not found / ⚠️ not connected
- Fireflies: ✅ [meeting title] / ❌ not found / ⚠️ not connected
- Slack context: (set in Step 1b)
- Manual: [if paste provided]
```

---

### Step 1b: Pull Interpreted Slack Context (high-signal meetings only)

For meetings where org context would meaningfully change synthesis, pull *interpreted*
discussion arcs (decisions, constraints, dissent) — not raw messages. If you use a
session-history / knowledge-compounding tool that can research Slack, invoke it here;
otherwise do a targeted Slack search on the key topics.

**When to run:**
| Meeting type | Pull Slack context? |
|---|---|
| Customer / external stakeholder | Yes |
| Product / strategy / roadmap / architecture | Yes |
| Sprint / standup / status sync | No |
| 1:1 / personal | No |

**How:**
1. Extract 2-3 key topics from the Granola/Fireflies summary (e.g., a feature name, a customer account, a deal)
2. Search Slack for those topics over the last 14 days
3. Treat the digest as a third source feeding Step 2's synthesis

**Update the SOURCES FOUND block:**
- Slack context: ✅ [N topics researched, last 14d] / ⏭️ skipped (not high-signal)

If skipped, state why in one line so future-you knows it wasn't an oversight.

---

### Step 2: Cross-Reference and Synthesize

If content from multiple sources is available, merge them into one comprehensive summary.
Each source captures different things — use both to fill gaps:

| Granola strengths | Fireflies strengths |
|---|---|
| AI-enhanced notes, key themes | Verbatim transcript, speaker attribution |
| Decisions and highlights | Exact quotes, tone, nuance |
| Structured chapters | Full chronological record |

**Synthesis rules:**
- Use Granola's structure as the base (it's cleaner)
- Fill in gaps, missed items, or extra detail from Fireflies transcript
- Where sources conflict, flag it: "⚠️ Granola says X; Fireflies transcript says Y"
- Capture anything in the Fireflies transcript that Granola missed entirely
- Note any action items Fireflies auto-detected that aren't in Granola notes
- If only one source available, note which one and proceed

---

### Step 3: Extract Action Items

From the synthesized content, identify every action item. For each one:
- **What:** The specific task or deliverable
- **Who:** The owner (name or role)
- **When:** Due date or timeline if mentioned
- **Source:** Which source surfaced it (Granola / Fireflies / Both)
- **Context:** One sentence of why it matters

```
ACTION ITEMS — [Meeting Title] ([Date])

1. [What] → Owner: [Who] | Due: [When] | Source: [Granola/Fireflies/Both]
   Context: [why]

2. ...
```

Flag any action items where:
- Owner is {{YOUR_NAME}} → goes to my-tasks.yaml
- Owner is unclear → ask {{YOUR_NAME}} to confirm
- No due date → use judgment (urgent = 2-3 days, normal = 1 week)
- Fireflies detected it but Granola missed it → worth extra attention

---

### Step 3b: Classify Action Items for the Task Tracker

Review every action item and tag each one as **product-change** or **non-product**.

**FIRST — route product-change items by destination:**

Product work splits into two tracks. Decide which before creating anything:

- **Intelligence-layer / aspirational product items → your product doc (DEFAULT).** Any item that belongs to your AI/intelligence layer, an agent capability, embedded data work, or a forward-looking product idea goes into your living **product doc** ({{DOC_ID}}), **NOT the task tracker**. Append a new entry to the correct section using the doc's existing entry format (an `ID. Title -- Status (Testing: Y/N)` line + description paragraph + `Refs:` line works well). Section meanings and current highest IDs live in the doc — read it first. **Show the drafted entry/entries to {{YOUR_NAME}} before writing.** Preserve the ENTIRE existing doc and insert the new entries at the end of their section. If an existing entry already covers the item, **update it** (add a `Refs:` line / status change) rather than duplicating.
- **Core app dev-team work → the task tracker ({{JIRA_PROJECT}}).** Only items the engineering team must build or fix in the core app (non-intelligence-layer): app UI changes, auth/permissions in the app, app bugs, app data model/API, integrations. These follow the task-tracker flow below.

If an item is genuinely both (an intelligence-layer feature that also needs a core-app change to land), capture the product-doc entry **and** the app slice in the task tracker, cross-referencing each.

Then, for items on the **task-tracker track only**, tag each as **product-change** or **non-product**.

**Product-change** — create a task-tracker ticket:
- Feature work or new capability to build
- Bug or defect that needs a code fix
- UX/UI change or design decision needed
- Data model, schema, or API work
- Integration or third-party connection work
- Any product decision that blocks engineering from moving forward

**Non-product** — do NOT create a ticket:
- Administrative follow-ups ("{{YOUR_NAME}} to send the contract")
- Scheduling tasks ("Set up a call with X")
- Internal PM work ("Update the roadmap", "Review the PRD")
- Communication tasks ("Draft email to customer")
- Research or exploration tasks owned by {{YOUR_NAME}} only

Show the classification before creating any tickets:
```
TASK-TRACKER CLASSIFICATION — [Meeting Title]

Product-change items ([count]) — will create tickets:
✅ [item] → Owner: [who] | [1-line reason it's product-change]
✅ [item] → Owner: [who] | [reason]

Non-product items ([count]) — no ticket:
⛔ [item] → Owner: [who] | [reason: admin/scheduling/PM task/etc.]
```

**If any classification is ambiguous**, flag it:
```
⚠️ [item] — unclear if product-change. Create a ticket? [Y/N]
```

Wait for confirmation on any flagged items before proceeding.

For confirmed product-change items, create tickets via your task tracker's MCP/API. **All ticket creation must follow your standing task-tracker rules in `CLAUDE.md`** — a good default set: `(DRAFT)` title prefix, leave **unassigned** (assignment is curated separately, do NOT auto-assign to the action-item owner), apply your team's review label, use plain ASCII dashes (`--` and `->`, never unicode dashes), write product-requirements-only descriptions (no schema/enum/API contract details), show the full writeup to {{YOUR_NAME}} before pushing, and fold any DB/migration work into the parent ticket rather than creating standalone ones.

Skill-specific configuration (fill in your own):

**Project:** {{JIRA_PROJECT}}
**Board:** {{JIRA_BOARD_URL}}
**Sprint:** none -- leave unassigned so the ticket lands in the backlog

**Issue type mapping:**
| Product-change type | Issue type |
|---|---|
| New feature, new capability, UX/UI change | Story |
| Bug, defect, broken behavior | Bug |
| Technical task (schema, API, integration, data model) | Task |

Each ticket must include:
- Title: action-oriented with `(DRAFT)` prefix (not "discuss X" -- use "(DRAFT) Implement X", "(DRAFT) Fix Y", "(DRAFT) Add Z")
- Assignee: unassigned
- Labels: your team's review label always; add a "small/unconnected" label if applicable
- No sprint assignment (backlog placement is automatic)

**Description format — use Given/When/Then for every ticket:**
```
**Given** [precondition — current state or context when this was raised]
**When** [the action, trigger, or scenario being addressed]
**Then** [expected outcome after the work is done]
**And** [additional behavioral or system requirement — repeat as needed]

### Context & Strategy

[2-3 sentences: why this came up, what problem it solves, any constraints or decisions from the meeting]

### Acceptance Criteria

1. **[Requirement Group]**
   - [specific, testable criterion]
   - Validation: [edge case, if applicable]

### Technical Notes

[Technical constraints, dependencies, or notes mentioned in the meeting. Omit section if none.]
```

---

### Step 4: Update my-tasks.yaml

For any action items owned by {{YOUR_NAME}}:
- Add to `~/.claude/my-tasks.yaml` with appropriate priority and due date
- Tag a goal alignment that maps to your own goals.yaml categories
- Note which source the task came from in the notes field
- Ask: "Should I mark [task] complete?" for anything already done

---

### Step 5: Draft Follow-up Messages

Two types of outbound communication come out of every meeting:
**A) Individual follow-ups** — one-to-one messages to action item owners
**B) Structured broadcast** — one-to-many update to leadership or team

Both use the connected Slack and Gmail MCPs for delivery. Never send without explicit approval.

---

#### 5A: Individual Follow-ups

For each action item owned by someone else, draft a follow-up message.

**Channel routing:**
- Internal (teammates, your manager, the team) → Slack DM via `slack_send_message_draft`
- External (customers, vendors, partners) → Email via `gmail_draft`

**Message format — short, warm, specific:**
```
Hey [Name] — quick follow-up from [Meeting].

You're down to [action item] by [due date]. Let me know if you need anything from me.

{{YOUR_NAME}}
```

For Slack messages, no sign-off needed — just the content.

---

#### 5B: Structured Broadcast

After every meeting, assess whether a structured broadcast is warranted based on meeting type:

| Meeting type | Broadcast format | Channel |
|---|---|---|
| Customer / external stakeholder | Leadership update to {{MANAGER}} | Slack DM or Email |
| Product / roadmap discussion | 3P update (Progress / Plans / Problems) | Slack — relevant channel |
| Sprint / engineering sync | Project update | Slack — team channel |
| One-off or low-signal internal | No broadcast needed | — |

**If a broadcast is warranted:**

Structure the message using whatever internal-comms patterns you keep:
- **Leadership update** (to {{MANAGER}}) → general update format: 3-5 bullets, what happened, what it means, any asks
- **3P update** (team) → Progress, Plans, Problems — concise, scannable
- **Project update** → status, decisions made, next steps, blockers

Draft the broadcast and add it to the approval queue with the individual follow-ups.

**Delivery:**
- Slack broadcasts → `slack_send_message_draft` (sends to specified channel or DM)
- Email broadcasts → `gmail_draft` (creates draft, user sends)

---

**Present ALL drafts (5A + 5B) together before sending anything:**
```
DRAFT MESSAGES — ready to send?

INDIVIDUAL FOLLOW-UPS
[1] To: [Name] via Slack DM
[message]

[2] To: [Name] via Email
[message]

BROADCAST
[3] To: [{{MANAGER}} / #channel] via [Slack/Email] — [Leadership Update / 3P Update / Project Update]
[message]

Type "send all", "send 1,3", or "edit [number]" to proceed.
```

**Never send without explicit approval.**

---

### Step 6: Save to Context Library

**Before writing — duplication check (all modes, no exceptions):**

Compute the target filename `YYYY-MM-DD-[meeting-title-slugified].md` and check `~/.claude/meeting-notes/` for an existing match. If a file exists for this meeting:

```
DUPLICATE DETECTED
~/.claude/meeting-notes/[existing-filename].md already exists for this meeting.

[1] Overwrite — replace existing file
[2] Append — add a new "## Reprocessed YYYY-MM-DD" section to the existing file
[3] Skip — leave existing file untouched and exit (still surface the action items / drafts in chat)

Type 1, 2, or 3.
```

Wait for explicit user choice before writing. Never silently overwrite.

Save the comprehensive summary to:
`~/.claude/meeting-notes/YYYY-MM-DD-[meeting-title-slugified].md`

```markdown
# [Meeting Title]
**Date:** MM/DD/YYYY
**Attendees:** [list]
**Duration:** [if known]
**Sources:** Granola ✅ | Fireflies ✅ (or whichever were available)

## Summary
[3-5 sentence synthesis from both sources — more complete than either alone]

## Key Decisions
- [decision 1]
- [decision 2]

## Action Items
| Item | Owner | Due | Source | Status |
|------|-------|-----|--------|--------|
| [task] | [who] | [when] | Granola/Fireflies/Both | pending |

## Product Signals & Context
[Customer pain points, product feedback, strategic signals, open questions —
anything worth surfacing in future sessions or triage]

## Relationship Notes
[Anything notable about attendees — tone, concerns, follow-up needed]

## Source Notes
[Any conflicts or gaps between Granola and Fireflies worth flagging]

## Raw Transcripts
### Granola Notes
[Granola content if available]

### Fireflies Transcript
[Fireflies content if available]
```

Also update `~/.claude/contacts/[person].md` for any external attendees with a brief
interaction note and date.

---

### Step 6b: Compound Learnings Check

Scan Key Decisions and Product Signals for compound-worthy patterns:
- A recurring problem just resolved ("third time this came up — finally decided X")
- A reusable pattern, framework, or principle worth team-wide reuse
- A premise you've been operating under that just shifted

If any qualify, prompt {{YOUR_NAME}}:
```
COMPOUND CANDIDATE — [Meeting Title]
[1-line summary of the pattern/decision]

Convert this into a learning doc? [Y/N]
```
(optional, if you use a session-history / knowledge-compounding tool — otherwise just
capture the learning in your notes.)

**Never auto-fire.** Compounding is high-value but the call on what's worth
documenting is {{YOUR_NAME}}'s. One prompt per qualifying pattern; if multiple, list them
and let {{YOUR_NAME}} pick which to compound.

If nothing qualifies, skip silently — most meetings won't have a compound moment,
and that's fine.

---

### Step 7: Present Summary

**Single meeting:**
```
✅ [Meeting Title] processed — [Date]

SOURCES USED
- Granola: ✅ / ❌
- Fireflies: ✅ / ❌

ACTION ITEMS ([count])
- [item] → [owner] by [date] ([source])
- ...

YOUR TASKS ADDED ([count])
- [task] added to my-tasks.yaml

TICKETS CREATED ([count] of [total action items] qualified as product-change)
- [ticket ID] — [title] → [assignee]
- (or "No product-change items found")

MESSAGES DRAFTED ([count] individual + [count] broadcast)
- [ready to review above]

SAVED TO
~/.claude/meeting-notes/[filename].md

Want me to send the follow-up messages?
```

**Batch mode — final summary after all meetings processed:**
```
BATCH COMPLETE — [count] meetings processed

MEETINGS PROCESSED
✅ [Date] — [Title] | [n] action items | [n] tasks added
✅ [Date] — [Title] | [n] action items | [n] tasks added
...

TOTAL ACTION ITEMS: [count]
TOTAL TASKS ADDED TO my-tasks.yaml: [count]
FILES SAVED TO ~/.claude/meeting-notes/

ALL DRAFT MESSAGES ([count] total)
──────────────────────────────────
[1] To: [Name] via Slack — re: [Meeting]
[message]

[2] To: [Name] via Email — re: [Meeting]
[message]
──────────────────────────────────

Type "send all", "send [numbers]", or "edit [number]" to proceed.
Nothing sends without your approval.
```

---

## Guidelines

- Two sources > one — always try both before falling back to manual
- If sources conflict, surface it — don't silently pick one
- Customer meetings: prioritize product signals and pain points in the context section
- Internal meetings: prioritize decisions and ownership
- Be specific on action items — vague tasks don't get done
- Flag blockers and risks explicitly
- The context library compounds — write notes as if you'll need them in 6 months
