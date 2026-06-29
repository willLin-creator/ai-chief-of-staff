# Deadline nudges

A deadline nudge is a short Slack message that surfaces a specific deliverable with a looming deadline, names where {{YOUR_NAME}} is vs. where they need to be, and proposes the single next block of work that moves it most. The goal is to make it harder for important things to slip and easier to re-enter a deliverable without friction.

## When to send a nudge

Send a nudge for a tracked deliverable when ALL of these are true:

1. There's a deadline or anchor event — an absolute date, or a meeting where the deliverable is expected.
2. The deadline is close enough to matter but not so close that a nudge is useless. Rule of thumb:
   - Deliverable due today/this meeting → nudge 2-4 hours before, if progress isn't ~done.
   - Deliverable due tomorrow → nudge once today, early (morning), if progress is <70%.
   - Deliverable due in 2-3 days → nudge if progress is <40% and there's no recent activity.
   - Deliverable due in >3 days → usually no nudge yet; let it appear in focus recs.
3. There's a specific, concrete next action {{YOUR_NAME}} can take. If the deliverable is blocked on someone else, it's not a nudge — it's a pending-ask reminder (handled separately, in focus recs).
4. No nudge for this same deliverable has gone out today. One nudge per deliverable per day unless it escalates to "due in <4 hours and barely started."

If any condition fails, don't nudge.

## How to assess progress

To decide whether a nudge is warranted, look at signals for the deliverable:

- Drive: when was the doc last edited? How substantively (page count, named sections)?
- Slack: has {{YOUR_NAME}} mentioned it recently? Shared a draft? Said "almost done"?
- Gmail: has it been sent to anyone?
- State file: what's the last tracked status?

From these, produce a rough progress estimate. Don't over-engineer it — "not started," "in progress," "mostly there," "ready to ship" is enough granularity. The goal is directional, not precise.

## Nudge template

```
⏰ *[Deliverable title]* — due [when], for [meeting or person]

Current state: [rough estimate]
Last activity: [when, what]

Next 30-60 min to move it:
[One specific concrete action]

Want me to: [offer one thing, e.g., "pull together the data for section 2", "draft the outline"]?
```

The offer at the bottom is important. {{YOUR_NAME}} is overloaded — a nudge that ends with "get to it" lands badly. A nudge that ends with "want me to draft section 2 while you're in the 3pm?" turns the nudge into momentum.

## Calibration

- Keep it under 80 words.
- Name the specific meeting or deadline, not "soon."
- Specify the exact next action — "finish section 3" beats "keep working on it."
- If {{YOUR_NAME}} has <2 hours before the deadline and is nowhere near done, flag it as a risk rather than a normal nudge: propose either a cut-down version or moving the deadline.

## Worked examples

### Example 1: Deliverable due tomorrow, ~50% done

```
⏰ *Hiring plan for Eng* — due Friday 4/24, for Riley

Current state: headcount by team done, rationale section not started.
Last activity: 4/20 (wrote headcount table).

Next 45 min to move it:
Draft the rationale section — 3 paragraphs on why this shape. You already have the logic; it's in your 4/15 1:1 notes with Riley.

Want me to pull the relevant quotes from those notes so you can just paste and edit?
```

### Example 2: Deliverable due today, meeting in 3 hours, barely started

```
⏰ *Pricing feedback for Jordan* — they're expecting it at the 3pm

Current state: not started.
Last activity: none — you replied "will do" on Monday.

Three hours is enough if you triage:
Give them directional feedback (bullets) instead of a full review. The pricing doc is 12 pages; you don't need to rewrite it. Focus on 2-3 load-bearing assumptions.

Want me to draft the bullet version for you to edit?
```

### Example 3: Risk escalation — deliverable due in 90 min, barely touched

```
🚨 *Board prep slides* — due to Lila at 4pm (90 min)

Current state: outline only, no slides drafted.
Last activity: 4/18 (outline).

Realistically not shippable at full fidelity in 90 min. Options:
• Send Lila the outline + 2 key slides, note full deck by EOD
• Push the deadline — she's usually flexible; want me to draft the message?
• Drop everything and sprint — I can draft 3 of the 6 slides in parallel

Which?
```

### Example 4: Blocked deliverable (don't nudge — surface differently)

If the deliverable is blocked (e.g., waiting on someone else's input), don't send a deadline nudge for it. Instead, in the next focus recommendation, include a "waiting on" line so {{YOUR_NAME}} can unblock:

```
You're blocked on the Q2 OKR doc — waiting for Riley's inputs since Monday. Want me to follow up with them?
```

## After sending

Record in the state file: deliverable name, nudge sent timestamp, deadline. Don't re-nudge the same deliverable today. If {{YOUR_NAME}} engages (responds with "I'll do that" or actually acts), mark it as "nudged and actioned." If the deadline passes with no progress, escalate in the next check-in: "X missed its deadline yesterday — still relevant, or retiring?"

## The discipline

Nudges degrade fast if they're frequent. One overlooked nudge is fine; a stream of them becomes noise {{YOUR_NAME}} tunes out. The best nudge is the one that lands at the moment {{YOUR_NAME}} has 45 minutes and is about to scroll Slack anyway. Aim for that window.
