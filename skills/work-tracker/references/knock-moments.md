# Knock moments — reading the room

This file is the heart of the skill's judgment. Before saying anything, the skill reads {{YOUR_NAME}}'s current state and decides whether now is a good moment to interrupt — the way a real chief of staff would. Most of a CoS's value is in timing; the content is almost secondary.

## {{YOUR_NAME}}'s possible states

Model {{YOUR_NAME}} as being in one of these states at any moment:

- **In a meeting** — actively on a call or in a scheduled meeting
- **Meeting wrapping up** — final ~5 min of a meeting, natural moment for a knock right after
- **In a gap** — between meetings, no imminent deep work
- **Deep work** — heads-down on something, typically signaled by a long stretch off Slack/email
- **Reactive mode** — Slack/email active, bouncing between messages, not in flow
- **Off-hours** — end of day, weekend, vacation
- **Pre-meeting window** — 15-30 min before a meeting starts; good time to brief

Different states call for different behavior. In a meeting: never interrupt (unless the meeting itself is ending). In deep work: almost never interrupt; the cost of breaking flow is high. In a gap: knock if there's something useful. In reactive mode: knock if it helps route attention; skip if it adds to the scatter.

## Signals to infer state

State isn't directly observable, but it's readable from signals:

**Meetings (is he in one?)**
- Meeting-notes tool (Granola): is there an in-progress meeting? When does it end?
- Calendar / Gmail invites: is there a meeting on the calendar for right now?
- Slack presence: Slack often shows "in a meeting" status for people with calendar sync
- Slack activity: if {{YOUR_NAME}} is replying in Slack, almost certainly not in a meeting

**Deep work (is he heads-down?)**
- No Slack sends from {{YOUR_NAME}} in the last ~30-45 min
- Active Drive editing on a single doc (file updated within the last 15 min, same doc)
- No read receipts on DMs directed at him
- Local time is a typical deep-work window (mornings, post-lunch — learn this over time)

**Gap (is he between things?)**
- Just finished a meeting (meeting-notes tool shows meeting ended in last ~5 min)
- No meeting for the next 20+ min
- Slack is active but not deeply so — replying to messages, not sending long ones

**Reactive mode**
- Many short Slack messages in quick succession
- Fast email triage pattern (several replies in a row)
- Context switching visible across tools

**Off-hours**
- Local time is evening / weekend / known vacation
- Config quiet hours apply

If signals are ambiguous, default to "don't knock." Missing a knock is much cheaper than interrupting at a bad time.

## Good knock moments

Knock when any of these is true:

- **Meeting just ended** (last ~10 min). Especially valuable because {{YOUR_NAME}} is naturally re-entering his workflow and a good CoS would grab him here.
- **15-30 min before a scheduled meeting.** Enough time to read and think, close enough that the context stays loaded.
- **Gap opens with >20 min before next commitment.** Good moment for a focus rec.
- **Deliverable just hit a risk threshold** (e.g., due in 4 hours, <50% done) AND {{YOUR_NAME}} is NOT in deep work or a meeting.
- **Morning re-entry.** First time {{YOUR_NAME}} appears online after a night or weekend, before the day gets hijacked.
- **{{YOUR_NAME}} directly asked.** Always respond if he asked — no knock judgment needed.

## Bad knock moments

Do NOT knock when any of these is true:

- **In a meeting** — unless he asked, stay out.
- **Deep work in progress** — the cost of breaking flow usually exceeds the value of the nudge.
- **Just got an interruption from something else** — if {{YOUR_NAME}}'s Slack or inbox is blowing up right now, adding a knock makes it worse, not better.
- **Off-hours** unless it's a meeting briefing for a meeting that starts within the hour.
- **A knock for the same thing was sent recently** — check the Sent log.

When in doubt, don't knock. The skill's value compounds when it's trustworthy; one poorly-timed knock sets back weeks of trust.

## Post-meeting knocks specifically

The "meeting just ended" moment is the skill's best opportunity. A real CoS would walk up and say: "before you jump into the next thing — you committed to send Marcus something by Friday; want me to queue a draft? Also your 3pm is Jenna from Beta Corp, quick primer?"

When a meeting {{YOUR_NAME}} attended just ended:

1. Pull the transcript from the meeting-notes tool (if available within ~2 min of end).
2. Extract commitments {{YOUR_NAME}} made in the meeting. Add to state.
3. Check: is there another meeting starting within the next 30-45 min? If yes, include a brief primer.
4. If commitments are urgent (due today, or the next meeting will re-raise them), surface them now.
5. Compose one message: either a brief "here's what came out of that + your next is X" or a standalone briefing for the next meeting if commitments were light.

This is high-leverage. Bias toward knocking here.

## Pre-meeting knocks specifically

The "15-30 min before a meeting" moment is the second highest-leverage window. Three guardrails:

1. Only one briefing per meeting — check Sent log.
2. Don't brief if {{YOUR_NAME}} is clearly mid-flow on something else — let him stay in it; the briefing will be less useful if he hasn't mentally shifted yet. Wait until 10-15 min before, then re-evaluate.
3. Skip routine meetings that don't need prep (recurring 1:1s with no new activity, large meetings where {{YOUR_NAME}} just listens).

## Detecting transitions

The most interesting moments are transitions — not "is {{YOUR_NAME}} free right now" but "did {{YOUR_NAME}} just become free." Transitions are the natural knock points.

Transitions to watch for:

- **In-meeting → free** (meeting ended)
- **Deep work → reactive** (started replying after a long silent block)
- **Free → pre-meeting** (a meeting is approaching in the next 30 min)
- **Online → offline** (end of day)
- **Offline → online** (start of day, after lunch)

Each one is a potential knock moment. Transitions from busy → free are especially good; transitions from free → busy (e.g., pre-meeting) are good for briefings.

Since the skill doesn't run continuously, it has to detect transitions at the moment of invocation — by looking at the last signals and inferring what changed since the last run. E.g., "last scan was 45 min ago, {{YOUR_NAME}} was in a meeting, now the meeting is over and he's replied to 2 messages — transition detected, knock window open."

## Handling false negatives

Sometimes the skill will decide "not a knock moment" and be wrong — {{YOUR_NAME}} was actually free and would have welcomed the knock. That's OK. The skill should err toward silence, and {{YOUR_NAME}} can ask if he wants something. The asymmetry is: missed knocks cost him 5 minutes of him-initiated asking; bad knocks cost him trust in the system.

## When {{YOUR_NAME}} directly asks

If {{YOUR_NAME}}'s query triggers this skill ("what should I work on", "brief me on my next meeting"), skip knock-moment evaluation entirely. He's asking — respond. The knock-moment logic only governs proactive sends.

## Re-evaluating when a scheduled knock fires

Every knock was planned at 9:13am based on the day as it looked then. By the time the knock fires, the world has moved. Before acting, re-evaluate in this order:

1. **Is the knock's original intent still valid?**
   - Briefing: is the meeting still happening? (check calendar — if canceled, cancel the knock)
   - Nudge: is the deliverable still open? (if signals suggest it shipped, don't nudge — send a confirmation question instead or skip)
   - Focus rec: does the free block the knock was planned for still exist? (if a meeting got added, the gap may be gone)
   - Post-meeting follow-up: did the meeting actually happen? (it may have been canceled or rescheduled)

2. **Is this a good moment in terms of {{YOUR_NAME}}'s state?** (use the "Good knock moments" / "Bad knock moments" lists above)
   - Is he in a meeting that ran long?
   - Did he just start deep work?
   - Is there evidence of a crisis/interrupt storm happening?

3. **Has the content changed?** Since the plan was made, new signals may have arrived (commitments from morning meetings, new asks in Slack). If so, the knock's message may need updating — don't send the old plan verbatim; re-compose with the latest context.

Three outcomes:

- **Proceed** — intent valid, moment good, content fresh → compose and send.
- **Defer** — intent valid and moment is the only problem → create a new scheduled task for 15 min later; mark this knock as deferred in state.
- **Cancel** — intent no longer valid → mark canceled in state, do not send, do not defer.

The discipline: trust your re-evaluation over the morning's plan. The plan was a hypothesis; the knock time is when you actually decide.

## Scheduling additional knocks mid-day

After a knock fires (whether it sent or not), scan briefly for new context. If something landed that warrants a new knock, schedule it:

- New meeting added to calendar → schedule a briefing knock for 25 min before it
- New urgent deliverable/commitment → schedule a nudge if deadline is near and there's a free block
- Big deliverable just completed → maybe schedule a focus rec for the freed-up time

Don't stack — if you're about to schedule a 4th knock within 90 min, reconsider. Respect the day's overall knock budget.

## Config per person

Some of {{YOUR_NAME}}'s state signals depend on his working style. On first use, ask him to help tune:

- "How can I tell when you're in deep work vs. just quiet? Time-of-day rules? Specific apps?"
- "Are there days or times when I should never send you things?" (these become quiet hours)
- "Are there days or times when you actively want me to be more proactive?" (e.g., Monday mornings for week-planning)

Save responses to Config in the memory file. Revise over time as {{YOUR_NAME}} gives feedback.
