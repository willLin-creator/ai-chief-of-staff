# State: memory layout and config

State lives in two places. A memory file (Claude-managed) is the source of truth for what's tracked, what's been sent, and skill config. Your task file (you-managed) is your canonical to-do list that this skill reads freely and updates carefully.

## Memory file location

Your auto-memory convention places this file at:

```
{{STATE_DIR}}/work-tracker_state.md
```

(For a typical setup, `{{STATE_DIR}}` is something like `~/.claude/projects/<your-project>/memory/`.)

Add a line to the memory index (`{{STATE_DIR}}/MEMORY.md`) pointing to it under a `## Work Tracker` section.

## File structure

```markdown
# Work Tracker State

## Config
- Slack destination: your own user ID `{{SLACK_USER_ID}}` (DM to self)
- Task file path: ~/.claude/my-tasks.yaml
- Current task pivot: ~/.claude/CURRENT_TASK.md
- Quiet hours: before 8am, after 6:30pm, weekends
- Daily planning schedule: 13 9 * * 1-5 (weekdays 9:13am; off-minute by design)
- Market scan schedule: 17 3 * * 1,3,5 (Mon/Wed/Fri 3:17am; off-minute)
- Top customer domains (renewal-risk weighting): [seed on first run, then cached here]
- Manager Slack ID: [resolved on first run, then cached here]
- Eng lead Slack ID: [resolved on first run, then cached here]
- Last full signal scan: [timestamp]
- Last daily plan run: --
- Last market scan: --

## Today's planned knocks

Today's scheduled knock fires -- written by the daily plan run, read by each knock run, updated as the day evolves.

- **10:35** -- briefing | 11am customer call | task id `work-tracker-knock-20260504-1035` | status: pending
- **12:05** -- focus rec | midday gap, re-emphasize board report | task id `work-tracker-knock-20260504-1205` | status: pending
- **13:35** -- briefing | 2pm roadmap review with eng lead | task id `work-tracker-knock-20260504-1335` | status: pending
- **15:10** -- post-meeting follow-up | roadmap | task id `work-tracker-knock-20260504-1510` | status: pending

## Top 3 today

Highest P-scored deliverables, surfaced in the morning focus rec.

1. **Board report for customer** -- Score: HHHM
2. **Partnership SOW finalization** -- Score: HHMH
3. **Renewal positioning** -- Score: HMHH

## Deliverables

Tracked work you're driving. Each has: title, anchor, P-score, sources, progress, last activity, notes, nudge log.

- **Board report for customer**
  - Anchor: customer meeting 5/14, committee review 5/18
  - Sources: manager email forward (4/28), feature ticket spec, task file
  - Score: HHHM
    - Stakeholder: H -- manager + a premium customer
    - Strategic: H -- maps to a top-priority reporting epic
    - Pressure: H -- 5/14 hard date
    - Leverage: M -- single-customer artifact, but template reusable
  - Auto-rules: manager explicit ask + named deadline (top of stack)
  - Last activity: 4/28 -- draft email saved
  - Notes: feature ticket not yet built; manual assembly expected; awaiting scope confirmation
  - Nudges sent: []

- **Partnership SOW finalization (trade show)**
  - Anchor: 6/2 trade show
  - Sources: SOW doc, manager Slack 4/27, memory observation
  - Score: HHMH
    - Stakeholder: H -- manager, contractual partner
    - Strategic: H -- SOW-committed (high priority score)
    - Pressure: M -- 5+ weeks out, but dependencies stretch
    - Leverage: H -- unblocks partnership, sets product narrative
  - Auto-rules: --
  - Last activity: 4/28 -- SOW trimmed and simplified
  - Notes: scope anchor removed; key terminology preserved
  - Nudges sent: []

- **Renewal positioning**
  - Anchor: ~30 day renewal window (specifics in CRM/memory)
  - Sources: memory observations
  - Score: HMHH
    - Stakeholder: H -- renewal risk ($45-50K)
    - Strategic: M -- positioning artifact, not roadmap epic
    - Pressure: H -- renewal at risk
    - Leverage: H -- board-narrative artifact
  - Auto-rules: Renewal-risk customer ≤30d (top of stack)
  - Last activity: 4/7 -- strategic pivot decisions
  - Notes: project list + cash flow reporting validated as actionable; positioning doc not yet drafted
  - Nudges sent: []

## Upcoming meetings

Detected meetings for the next ~48 hours. Refresh every scan.

- **4/21 3:00pm — 1:1 with a colleague** (source: meeting notes/calendar)
  - Expected deliverables: pricing feedback
  - Briefing sent: [4/21 2:35pm]

- **4/22 10:00am — Board prep**
  - Expected deliverables: slide outline
  - Briefing sent: []

## Commitments

Things you promised someone. Each has: what, to whom, when promised, anchor.

- Send intro → a contact → committed 4/18 in meeting → this week
- Pricing feedback → a colleague → committed 4/19 in Slack → before 3pm today
- Product review feedback → a colleague → committed 4/19 → by Friday

## Pending asks (waiting on you)

Things people are waiting on from you.

- Feedback on onboarding flow doc → a teammate → asked 4/19, pinged 4/21
- Q2 OKR approval → a teammate → asked 4/17 (blocking their planning)

## Sent log

Record of what was sent to Slack and when. Used to avoid duplicate briefings/nudges.

- 4/21 2:35pm — briefing: "1:1 3pm"
- 4/21 8:55am — morning focus rec
- 4/20 3:10pm — nudge: "Hiring plan for Eng"

## Retired (last 30 days)

Items you confirmed done or dropped.

- 4/20 — Pricing model draft (shipped to finance)
- 4/19 — Q1 retro doc (dropped, not doing retro this quarter)
```

## How to read state

At the start of every invocation:

1. Read the memory file top to bottom.
2. Read your task file (use the path in Config; if not set, ask once and save).
3. Note which meetings, deliverables, and commitments are relevant to right now.
4. Look at the Sent log to avoid duplicate outputs.

## How to update state

After any output is sent or you respond:

- **Briefing sent** → log in `Upcoming meetings` and `Sent log`. Mark the corresponding `Today's planned knocks` entry as `status: sent`.
- **Nudge sent** → log in the deliverable's `Nudges sent` list and `Sent log`. Update the planned-knocks entry.
- **Focus rec sent** → log in `Sent log` with which deliverable was surfaced.
- **Knock deferred** → update its `Today's planned knocks` entry to the new time; create a new scheduled task for the new fire time.
- **Knock canceled** → update its entry to `status: canceled` with a one-line reason; disable the original scheduled task via `update_scheduled_task`.
- **New knock added mid-day** → append to `Today's planned knocks` and create the scheduled task.
- **You confirmed something complete** → move to `Retired`; remove from active sections.
- **New commitment found in signals** → add to `Commitments`.
- **New meeting detected** → add to `Upcoming meetings`. Consider scheduling a briefing knock for it.
- **New ask detected** → add to `Pending asks`.

Always refresh the `Last full signal scan` timestamp when a scan completes. Refresh `Last daily plan run` after the morning run.

## End-of-day rollover

At the next day's morning planning run (see `references/daily-plan.md`), yesterday's `Today's planned knocks` section is cleared. Any knocks that didn't fire (bug, server offline, etc.) get their task IDs disabled via `update_scheduled_task`. The day's sent log entries roll into the 7-day retention window.

## Task file conventions

Your task file is yours. Treat it with respect:

- **Read freely.** Every scan. Infer structure from context (sections, checkboxes, priority tags).
- **Write sparingly, with permission.** When you confirm a task is done during an interaction, you can check it off — but only that. Don't reorganize, rewrite, or add new tasks unless asked.
- **Detect conventions.** If it uses `[ ]` and `[x]`, do the same. If it uses `- ` bullets with priority markers, match.
- **Surface the file's own items as tracked deliverables.** If something has a due date in the task file, mirror it into the Deliverables section with the task file cited as the source.

## Size discipline

Keep the memory file lean. Rules of thumb:

- Deliverables: 3-7 active items is healthy. Above 10, prune.
- Upcoming meetings: ~48 hour horizon. Older ones move to the sent log or get dropped.
- Commitments: no cap, but surface anything older than 2 weeks in a focus rec — likely stale.
- Sent log: keep last 7 days. Older entries can be dropped.
- Retired: keep last 30 days. Older items drop.

A small state file makes every run fast and prevents noise accumulation.

## Config changes

If you ask to change Slack destination, quiet hours, or any other config during a session, update the Config section immediately and confirm back: "Updated — I'll send to `{{COS_SLACK_CHANNEL}}` going forward."
