# Deliverable detection -- where candidate deliverables come from

The skill does not ask {{YOUR_NAME}} what to track. It detects candidate deliverables by scanning connected systems and synthesizing them into a stack-ranked list using the framework in `prioritization.md`.

This file is the source list and the dedupe rules. Run this scan in plan mode every morning at 9:00am (local time), and re-run a delta scan inside each knock fire if it makes sense.

## Source list (in order of authority)

When the same deliverable is named in multiple sources, the highest-authority source wins for the `Anchor` and `Notes` fields; supporting sources are merged into `Notes` as references.

### 1. {{MANAGER}} / {{ENG_LEAD}} explicit asks (HIGHEST authority)

These override everything. Scan:

- **Gmail** -- threads from {{MANAGER}}'s or {{ENG_LEAD}}'s email in the last 14 days. Look for direct asks, deadlines, escalations. Pay extra attention to forwards (e.g., "Fwd:" -- often hot customer asks).
- **Slack** -- DMs from {{MANAGER}} or {{ENG_LEAD}} in the last 14 days. Search any channels they share with {{YOUR_NAME}}. Use a user-search call to resolve their IDs once and cache in state Config.
- **Meeting notes (Granola/Fireflies)** -- 1:1 transcripts ({{YOUR_NAME}} + {{MANAGER}}, {{YOUR_NAME}} + {{ENG_LEAD}}) from the last 14 days. Action items assigned to {{YOUR_NAME}} go straight into Deliverables.

Anything tagged here gets at minimum `H` on Stakeholder Pull and likely an auto-rule trigger ("{{MANAGER}} explicit ask + named deadline").

### 2. Roadmap-managed sources (strategic anchor)

- **{{PLANNING_DOC}}** (roadmap) -- read top-3 non-committed epics + all contractually committed epics. Each is a candidate strategic deliverable for {{YOUR_NAME}} (own the spec, unblock the eng team, drive the rollout).
- **Product backlog board** -- pull all ideas with a priority score above your threshold OR flagged as contractually committed. For each, check status -- if "Ready for Dev" or "In Progress" without a clear PM owner action, surface as a deliverable.
- **Scope-of-work doc** ({{PLANNING_DOC}}) -- contractual deliverables and trade show / customer-facing dates are deadlines.
- **Insights / customer-synthesis doc** ({{PLANNING_DOC}}) -- top-3 insight items not yet rolled into an epic are candidate "frame it / pitch it" deliverables.
- **Market-scan doc** ({{PLANNING_DOC}}, created by the recurring competitor scan -- see `market-pulse.md`). Latest section's "Actionable implications" rolls into the Strategic Fit lens.
- **Product Ideas backlog** (`~/.claude/product-ideas.yaml`, managed by the `/idea` skill). Read fresh. For each entry where `status` is `captured` or `scoped`:
  - **`score.composite >= 15`** -- surface as a candidate deliverable. Action: "Promote idea-XXX -- run `/idea promote idea-XXX to roadmap`" (small 5-minute action, but high leverage). Lens scoring: pull the idea's existing 4-lens scores directly (the schema mirrors work-tracker's S/F/P/L exactly -- no recomputation needed). Apply a recency bump to Time Pressure: +1 if `captured` date is >14 days ago (idea is rotting), +2 if >30 days ago.
  - **`12 <= score.composite < 15`** -- surface only if also referenced in the last 7 days of meeting notes or Slack (i.e., still topical). Otherwise leave dormant.
  - **`score.composite < 12`** -- ignore.
  - Skip ideas already in `in_roadmap`, `in_prd`, `shipped`, or `dropped` -- they've been handled.
  - Cross-link signal: if an idea has `related.metric_suggestion_id` set, note that in the deliverable's `Notes` -- this is a paired metric/product gap and {{YOUR_NAME}} may want to action both together.

### 3. Customer-driven asks (revenue protection)

- **Gmail** -- threads from top-customer domains in the last 14 days. Maintain a list in state Config (`Top customer domains`). Seed it with your premium and renewal-risk accounts, for example:
  - `acme-example.com` (Acme Holdings -- premium)
  - `example-pm.com` (Example PM Co -- renewal-risk)
  - `example-partner.com` (active partnership)
- **Meeting notes (Granola/Fireflies)** -- transcripts of meetings with external customer attendees. Extract commitments {{YOUR_NAME}} made.
- **Memory observations** -- last 14 days, search for "customer" / "renewal" / "feedback" / "asked".

Customer-driven asks get HIGH stakeholder pull if the customer is on the renewal-risk or premium list.

### 4. {{YOUR_NAME}}'s own task surface

- **`~/.claude/my-tasks.yaml`** -- read fresh. Anything with a due date in the next 14 days is a deliverable; anything older without a date is a candidate but lower priority.
- **`~/.claude/CURRENT_TASK.md`** -- current pivot context, useful for understanding what {{YOUR_NAME}} is mid-flight on.
- **Recent memory observations** -- last 7 days. Look for `🟣feature`, `🔴bugfix`, `🔄refactor` tagged items where {{YOUR_NAME}} is the implicit owner.

### 5. Internal team unblocks

- **Slack** -- last 7 days. Mentions of {{YOUR_NAME}} in product, design, eng channels. "Waiting on {{YOUR_NAME}}" / "PM input" / "@{{YOUR_NAME}}" / "spec from {{YOUR_NAME}}" patterns.
- **Meeting notes (Granola)** -- last 7 days. Internal meeting transcripts where someone said they're blocked on {{YOUR_NAME}}.

These get MED stakeholder pull unless the unblock is for {{MANAGER}} or {{ENG_LEAD}} (then HIGH).

### 6. Calendar pressure

- **Google Calendar** -- next 14 days. Any meeting {{YOUR_NAME}} hosts where they're on the agenda implicitly creates a deliverable ("prepare for X meeting"). Customer-facing meetings get higher weight than internal ones.
- Specific deadline anchors mentioned in calendar event descriptions (e.g., "Customer committee 5/18", "Trade show 6/2") become deliverable anchors.

## Dedup rules

Same deliverable surfaced from multiple sources:

1. **Match by anchor first.** If two candidates share a deadline + topic, they're the same deliverable.
2. **Match by referenced people.** "Acme board report" mentioned by {{MANAGER}}, by a customer contact, and in {{YOUR_NAME}}'s tasks -> one deliverable, three sources.
3. **Match by ticket / backlog reference.** A given ticket ID mentioned in the roadmap doc + Slack + insights -> one deliverable.
4. **When in doubt, merge.** Better to over-merge and split later than fragment a single deliverable into duplicates.

## Pruning rules

After scoring, prune the active list to **5-8 deliverables** max. Above that, the daily focus rec gets diluted.

- Drop anything `MMLL` or below unless it has a hard deadline ≤7 days.
- Move anything that's clearly retired or completed to the `Retired` section.
- Move anything that hasn't moved in 21+ days and isn't blocked on someone else to `Retired -- stale`. Surface the move once: "Dropping X from active tracking -- no movement since [date]. Bring back if it's still alive."
- Combine micro-deliverables that share a parent goal into a single deliverable with sub-items.

## Scoring pass (after detection, before pruning)

For each candidate, walk the four lenses (`prioritization.md`):

```
- **[Deliverable name]**
  - Anchor: [deadline / meeting / commitment]
  - Sources: [{{MANAGER}} email 4/24, meeting notes 4/22 call, my-tasks.yaml]
  - Score: HHHM
    - Stakeholder: H -- {{MANAGER}} + premium customer
    - Strategic: H -- top-priority board reporting epic
    - Pressure: H -- 5/14 meeting, 5/18 committee
    - Leverage: M -- generates artifact for one customer, but template reusable
  - Auto-rules: --
  - Last activity: 4/28 -- draft email to {{MANAGER}} saved
  - Notes: feature not yet built; manual assembly required
  - Nudges sent: []
```

## Special cases

### Renewal-risk accounts

Flag renewal-risk accounts in memory and in state Config. Any email, meeting, or commitment from such a domain auto-flags `H` Stakeholder Pull. Same logic for any account flagged by {{MANAGER}} or {{ENG_LEAD}} as at-risk.

### Contractual (scope-of-work) deliverables

Anything tied to an active scope-of-work agreement auto-scores HIGH on Strategic Fit (top priority score). The contractual gate timing (e.g., trade show date) drives Pressure.

### "I'll think about it" items

{{YOUR_NAME}} sometimes says "I'll think about it" or "let me sit on this." These are deliverables -- the deliverable is the *decision*. Track as `Decision: [topic]` with the soft deadline (when the asker expects a response). Scoring: usually `MMMH` -- M stakeholder, M strategic, M pressure, H leverage (a clear no closes a loop and reclaims time).

### Personal capital concentration

If three or more deliverables in a week all converge on {{MANAGER}} (they asked, they'll review, they'll be visible), surface that pattern in the morning rec: "you're spending a lot of capital with {{MANAGER}} this week -- worth pacing?" The skill should help {{YOUR_NAME}} think about *where* their political capital flows, not just what to ship.

## When detection finds nothing

Rare. If the scan returns zero new signals and existing deliverables haven't moved, the morning rec leads with: "Quiet morning. Best use of time today is X (the highest-leverage existing deliverable)." Don't fabricate work.

## When detection finds too much

Common. If 15+ candidates surface in one scan:

1. Apply pruning rules.
2. Apply auto-rules (compliance, {{MANAGER}} + deadline, renewal-risk).
3. If still >8, demote anything Strategic LOW even if Pressure HIGH -- Pressure-without-Strategy is usually noise (a pushy stakeholder pulling on something that doesn't matter).
4. If still >8, the framework isn't wrong -- {{YOUR_NAME}}'s plate is genuinely overloaded. Surface this explicitly: "I'm tracking 11 active deliverables right now. That's too many. Want to triage which ones to drop?"
