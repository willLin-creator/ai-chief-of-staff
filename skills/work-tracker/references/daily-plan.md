# Daily plan -- the 9:00am morning run

Once a day on weekdays, a recurring scheduled task fires this skill in "plan mode." That's when the day gets its shape: deliverables get detected and scored, a morning focus rec gets sent to {{YOUR_NAME}}, and a set of scheduled one-time knocks gets spread through the day.

The plan is a hypothesis, not a contract. As the day unfolds, each knock re-evaluates and may add, defer, or cancel other knocks.

## What the morning run does, in order

### Step 0: Read the latest market scan

Fetch the most recent dated entry from the market-scan doc ({{PLANNING_DOC}}, ID stored in the roadmap skill's Configuration block). Capture the "Actionable Implications" -- they feed the Strategic Fit lens.

If no market-scan doc exists yet, skip and continue. The recurring competitor scan seeds it.

### Step 1: Housekeeping

Clean up stale state from yesterday:

- List scheduled tasks. Find any `work-tracker-knock-*` tasks still enabled with fire times in the past (they should have fired, but check). Disable any that didn't run.
- Clear the "Today's planned knocks" section in state from yesterday.
- Roll yesterday's sent log into the retained 7-day history; anything older drops.

### Step 2: Detect candidate deliverables

Run the full sweep per `references/deliverable-detection.md`:

1. {{MANAGER}} / {{ENG_LEAD}} explicit asks (Gmail, Slack DMs, 1:1 transcripts last 14 days)
2. Roadmap-managed sources (roadmap doc, product backlog board, scope-of-work doc, insights synthesis, market scan)
3. Customer-driven asks (top customer domains in Gmail + meeting notes last 14 days)
4. {{YOUR_NAME}}'s own task surface (`~/.claude/my-tasks.yaml`, `~/.claude/CURRENT_TASK.md`, recent memory observations)
5. Internal team unblocks (Slack mentions / "blocked on {{YOUR_NAME}}" patterns last 7 days)
6. Calendar pressure (next 14 days hosted meetings / external customer meetings)

Dedupe and merge per detection rules.

### Step 3: Score every active deliverable

Apply the 4-lens P-score per `references/prioritization.md`:

- **S** -- Stakeholder Pull (HIGH/MED/LOW)
- **F** -- Strategic Fit (HIGH/MED/LOW) -- read roadmap docs + market-scan implications
- **P** -- Time Pressure (HIGH/MED/LOW)
- **L** -- Leverage Multiplier (HIGH/MED/LOW)

Apply auto-rules (compliance, {{MANAGER}} + deadline, renewal-risk, two-way doors, one-way doors).

Sort. Apply pruning rules to keep the active list at 5-8 deliverables.

Surface the top 3.

### Step 4: Gather today's inputs

Pull the raw material for the day's plan:

- **Calendar/meeting notes:** every meeting today with time, duration, attendees, type (external/internal, 1:1/group, recurring/one-off).
- **State -> Deliverables:** today's top 3 (just scored), plus everything tracked with deadlines this week.
- **State -> Commitments and Pending asks:** open items.
- **Overnight activity:** Slack, Gmail since last scan. New asks? New meetings that landed? Completions?

### Step 5: Send the morning focus rec

Before scheduling any knocks, send {{YOUR_NAME}} the morning message. Use the focus rec template from `references/focus.md` -- frame as "today's shape." Structure:

- One-line summary of the day (meeting count, biggest free block)
- The top scored deliverable as primary recommendation, with its 1-line P-score rationale
- Optionally, the second top deliverable as "if you finish early"
- A "skipping" line covering the third top deliverable so {{YOUR_NAME}} knows you considered alternatives

Send this immediately when the run fires.

### Step 6: Plan the day's knocks

Walk through the day's meetings and the top-scored deliverables and decide where to place knocks. For each candidate:

**Pre-meeting briefings** -- for each meeting on today's calendar:
- Does it warrant a briefing? Skip routine 1:1s with no new activity, standing team meetings {{YOUR_NAME}} doesn't drive, large meetings where they just listen.
- If yes, schedule a briefing knock ~25 minutes before start time. Adjust earlier if {{YOUR_NAME}} has back-to-backs (in which case brief during the gap before them, or in the morning).
- External meetings, high-stakes reviews, customer calls, and meetings tied to a top-3 deliverable get priority.

**Deadline nudges** -- for each top-3 deliverable with time pressure:
- If Pressure is HIGH and the deliverable has slipped (no movement in 2+ days OR scored at risk), schedule a nudge.
- Pick a time of day when {{YOUR_NAME}} is most likely free to act -- look at the calendar for gaps. Good nudge moments are after morning meetings finish (~11am/12pm) or mid-afternoon (~2-3pm).
- Max one nudge per deliverable per day unless it escalates.

**Mid-day focus recs** -- for large gaps in {{YOUR_NAME}}'s calendar:
- Morning focus was already sent. Add a mid-day focus rec only if there's a genuinely large unstructured block (>90 min) where a re-emphasis of priorities would be useful.
- Typical day has 0-1 additional focus recs.

**Post-meeting follow-ups** -- for high-stakes or high-signal meetings {{YOUR_NAME}} attended:
- If the meeting is likely to produce commitments worth surfacing (external calls, 1:1s with direct reports, leadership discussions), schedule a knock ~5 min after the meeting ends.
- Don't do this for every meeting -- only ones likely to generate action items.

### Step 7: Budget the knocks

A calm day: 2-4 knocks. A busy day: 4-6. A truly packed day: 6-8 max. If you're about to schedule 10+ knocks, something is wrong -- you're over-serving.

Rules of thumb:

- Spread knocks so no two fire within 20 min of each other.
- Never schedule a knock inside a meeting -- the knock-mode evaluation would cancel it anyway.
- If {{YOUR_NAME}} has dense back-to-back meetings, place 1-2 knocks in the gaps that exist, not during the meetings.
- Protect the morning focus message as the day's lead -- don't overshadow it with multiple knocks before 11am.
- Respect quiet hours: nothing before 8am, nothing after 6:30pm (a hard constraint -- HOME by 6:30pm; tune per person in Config).

### Step 8: Schedule each knock

For each planned knock, use the `schedule` skill (or local CronCreate if appropriate) to create a one-time scheduled task with:

- Unique identifier: `work-tracker-knock-<YYYYMMDD>-<HHMM>`
- Fire time: exact ISO timestamp
- Self-contained prompt that tells the future knock-mode run exactly what to do, e.g.:

> *"Run the work-tracker skill in knock mode. You're the 2:35pm briefing for the 3pm 1:1 with {{TEAMMATE}}. Today's planned knocks are in memory; look yours up by fire time. Re-evaluate whether this is still a good moment to knock (check {{TEAMMATE}}'s meeting isn't canceled, {{YOUR_NAME}} isn't in another meeting, briefing hasn't already been sent). If good, compose and send the briefing to Slack per references/slack.md. Then scan for new context and update the day's plan if needed."*

Include in the description the specific intent of this knock -- briefing topic, deliverable name, focus rationale -- so the future run has what it needs without re-deriving it.

### Step 9: Write today's plan to state

Update the state file's "Today's planned knocks" section with the full list: time, type, intent, target (meeting/deliverable), and the scheduled task ID. Each knock-mode run reads this to know what it was planned to do.

Also update:
- "Top 3 today" -- the three top-scored deliverables with their P-scores
- "Deliverables" -- the full re-scored active list
- "Last daily plan run" -- timestamp

## Strategic-narrative test (weekly, on Mondays)

On Mondays, before sending the morning rec, ask: "do this week's top-3 deliverables ladder up to a story we can tell investors?"

If yes -- carry on, surface in the morning rec briefly: "this week's top-3 ladders into [narrative thread]."

If no -- and this is the third Monday in a row without a narrative artifact in the top-3 -- surface that gap explicitly in the morning rec:

> *"3 weeks now without a board-narrative artifact in your top-3. Worth carving time this week to ship one (e.g., positioning doc, market thesis, product differentiation one-pager)?"*

This is the skill thinking about {{YOUR_NAME}}'s career arc, not just their weekly throughput.

## Example morning run output

Suppose it's Monday, 5/4, 9:13am. {{YOUR_NAME}} has:

- 10:00am -- 1:1 with {{MANAGER}} (weekly recurring)
- 11:00am -- external call with a contact at Acme Holdings
- 2:00pm -- {{PRODUCT}} roadmap review with {{ENG_LEAD}} and {{TEAMMATE}}
- Top 3 from detection + scoring:
  1. **Acme board report** -- HHHM ({{MANAGER}} + customer, top board-reporting epic, 5/14 deadline, single customer artifact)
  2. **Scope-of-work finalization** -- HHMH ({{MANAGER}} asked, contractually committed, 6/2 trade show, unblocks partnership)
  3. **Renewal positioning** -- HMHH (renewal risk, top strategic fit, ~30d window, board-narrative artifact)

The morning run:

1. Sends the morning focus rec at 9:13am:
   ```
   🎯 *Monday shape* -- 3 meetings, biggest block 12-2pm

   *Work on:* Acme board report (5/14).
   _Why this:_ {{MANAGER}} + customer both pulling, no movement since Friday, 11am call is the perfect chance to confirm scope before manual assembly.

   *If you finish early:* Scope-of-work finalization -- partnership dependency, 6/2 trade show.

   _Skipping:_ Renewal positioning -- needs 90+ min, save for tomorrow morning's block.
   ```

2. Plans and schedules these knocks:
   - **10:35am** -- Briefing for 11am Acme call (high-stakes external, top deliverable)
   - **12:05pm** -- Mid-day focus rec for the 12-2 block (re-emphasize Acme report assembly)
   - **1:35pm** -- Briefing for 2pm {{PRODUCT}} roadmap review ({{ENG_LEAD}} coordinating, scope-of-work deliverables on agenda)
   - **3:10pm** -- Post-meeting follow-up for the roadmap review (capture commitments + {{TEAMMATE}}'s input on differentiation)

3. Writes all four to state's "Today's planned knocks" section, plus the scored top-3 to "Top 3 today."

## What each knock does when it fires

See knock mode in the main `SKILL.md` and `references/knock-moments.md`. Brief version: re-read state, re-evaluate whether to knock, send if appropriate, scan for new context, optionally schedule additional knocks, log.

## The feedback loop

Over time, the morning plan gets smarter because each knock logs outcomes:

- Which knocks did {{YOUR_NAME}} engage with (replied, took action)?
- Which did they ignore?
- Which landed at bad times (replied grumpily or not at all)?
- Which deliverables consistently scored top-3 but never moved (suggests the score is wrong or the work is blocked)?

The morning run can inspect this log across recent days and adjust: avoid the times {{YOUR_NAME}} consistently misses, emphasize the kinds of knocks they engage with most, surface stuck deliverables for {{YOUR_NAME}} to triage.

If {{YOUR_NAME}} overrides the recommended top-3 three times in a week, the next Monday morning rec calls it out explicitly per `references/prioritization.md`'s "When the framework gets it wrong" section.

## When the morning run should skip

- **Weekend** -- skip entirely. The cron is `13 9 * * 1-5`, so this should never fire on weekends, but defensively: if the day-of-week is Sat or Sun, exit.
- **{{YOUR_NAME}}'s vacation / off-day** flagged in Config -- skip.
- **Zero meetings, zero active deliverables** (rare) -- send a brief "nothing on the plate today, enjoy the open runway" message and schedule no knocks.

## Quiet hours

Per {{YOUR_NAME}}'s hard constraints (tune in Config):

- Nothing before 8am (the 9:13am plan run is the day's first signal)
- Nothing after 6:30pm (HOME for dinner)
- Nothing on weekends

If a knock would fire outside these windows, defer to the next allowed window or cancel.
