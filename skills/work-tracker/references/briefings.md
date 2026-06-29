# Pre-meeting briefings

A briefing lands in {{YOUR_NAME}}'s Slack roughly 20-30 minutes before a meeting. Its job is to make them the most prepared person in the room with 2 minutes of reading.

## What makes a good briefing

A briefing is not a meeting prep doc. It's a cheat sheet. The goal is to transfer just enough context that {{YOUR_NAME}} walks in knowing (a) what the meeting is actually about, (b) who they're talking to and what they care about, (c) what they own or need to drive, and (d) one or two specific things that would be easy to miss without prep.

Good briefings feel like a trusted EA leaning over your shoulder: "Hey, before you walk in — here's the thing." Bad briefings read like a Wikipedia entry about the meeting.

## Briefing template

Use this structure. Adapt length to meeting weight — a 1:1 with someone {{YOUR_NAME}} talks to daily needs 3 lines; a board prep session might need the full template.

```
📋 *[Meeting title]* — [time] with [attendees]

*Why it matters*
[1-2 lines: what's the real purpose, what's at stake]

*What you owe*
[Things {{YOUR_NAME}} specifically needs to bring: a decision, an update, a doc, an intro]

*Recent context*
[2-4 bullets: latest relevant Slack thread, doc edits, prior meeting outcomes, commitments made]

*Watch for*
[1-2 specific things {{YOUR_NAME}} might otherwise miss: a concern someone raised, a deadline that shifted, a person's priorities]

*Suggested ask/push*
[Optional: one concrete thing {{YOUR_NAME}} should push for or propose]
```

## How to fill each section

**Why it matters** — Not "this is a 1:1 with Jordan." That's the title. The real purpose: "Jordan wants to align on Q3 before the leadership offsite — they're pushing for the GTM cut to get more attention." If you can't articulate why it matters beyond what's on the calendar, the meeting is probably routine and the briefing can be very short.

**What you owe** — Scan commitments in the state file and recent meeting-notes/Slack/Gmail for anything {{YOUR_NAME}} said they'd bring, send, decide, or drive. If there's nothing specific, say so: "Nothing owed; this is an align-and-listen." Don't pad.

**Recent context** — Pull from meeting notes (prior meetings with overlapping attendees, especially in the last 2 weeks), Drive (docs touching the same topic, recently edited), Slack threads (especially DMs with attendees), Gmail (any thread on the topic in the last week). 2-4 bullets, with dates. Bias toward the freshest items. If the briefing could be improved by a link, include one.

**Watch for** — This is the highest-value section. Things like:
- "Riley pushed back on the timeline on Monday — they may raise it again."
- "Casey mentioned in their team's standup they're worried about the pricing model impact."
- "The last time this topic came up (3/12 meeting), you committed to a response by end of week and haven't followed up."
- "Jordan's OOO next week — anything you need from them should get pulled forward."

If nothing stands out, skip this section entirely. Don't invent watch-fors.

**Suggested ask/push** — Optional. Only include if there's a clear strategic move {{YOUR_NAME}} could make in the meeting that they might not think of without prompting. E.g., "Good time to lock in their commitment on the headcount number — they've been hedging." Don't include filler.

## Briefing length calibration

- **1:1 with a frequent collaborator (daily contact, low stakes)**: 4-6 lines total. Often just "Why it matters" + "What you owe" if anything is owed.
- **1:1 with a key person (weekly/biweekly)**: Full template if there's meaningful activity since last meeting; trimmed otherwise.
- **Team meeting / standup**: Short — highlight only things {{YOUR_NAME}} owns or needs to push.
- **External meeting (customer, partner, investor)**: Full template; recent context matters most.
- **High-stakes review (board, offsite, major decision)**: Full template, more detail, likely also a deadline nudge to have reviewed materials beforehand.

If the briefing exceeds ~200 words for a routine meeting, cut. The bar is "{{YOUR_NAME}} reads this and feels ready," not "{{YOUR_NAME}} knows everything."

## When to skip a briefing entirely

Don't send a briefing for:

- Meetings {{YOUR_NAME}} runs routinely where prep isn't needed (regular team syncs, recurring office hours)
- Meetings that are purely informational (all-hands where they just listen)
- Meetings where the last briefing was sent less than an hour ago and nothing new has happened
- Back-to-back meetings where a briefing would arrive too late to read

When in doubt, send something short rather than nothing — but don't force it.

## Worked examples

### Example 1: 1:1 with Jordan (VP Product), 3pm

```
📋 *1:1 with Jordan* — 3:00pm

*Why it matters*
They want to align on Q3 strategy before the offsite; also expecting your pricing feedback.

*What you owe*
• Pricing model feedback (promised Mon, they pinged today)
• Answer: are we still committing to the GTM cut going to the offsite?

*Recent context*
• You shared Q3 doc draft 4/20. Jordan left 3 comments, unresolved.
• Slack thread with them 4/19: they're worried engineering timeline slips the launch.

*Watch for*
Jordan tends to push timeline discussions at the end of the meeting — leave 10 min.
```

### Example 2: External — Partnership call with Beta Corp, 4pm

```
📋 *Beta Corp partnership call* — 4:00pm with Jenna Ortiz (CEO), Mike Park (BD)

*Why it matters*
First call since the partnership memo you drafted (4/14). They're evaluating 2 vendors; we're one. Goal: lock in their preference this call.

*What you owe*
• The memo itself — confirm they have it (check Gmail thread)
• Your opinion on the revenue share they proposed (65/35)

*Recent context*
• Jenna emailed Friday asking for a customer reference. You haven't replied.
• Memo hasn't been edited since 4/14 — confirm you want to go in with that version.

*Watch for*
Mike raised implementation concerns on the last call. Probably again.

*Suggested push*
Propose a 2-week pilot as a middle path if they hedge on commitment.
```

### Example 3: Quick 1:1 with direct report

```
📋 *1:1 with Alex* — 10:30am

Nothing owed. No new commitments since last week. Alex's doc (onboarding flow v3) hasn't been updated since Friday — ask how it's going.
```

## Sending the briefing

Send via Slack to the configured destination ({{COS_SLACK_CHANNEL}} or DM to {{SLACK_USER_ID}}). Prepend with a short preview line (used as the notification preview) that names the meeting. See `references/slack.md` for the exact send mechanics.

After sending, note in the state file that a briefing was sent for this meeting, so the skill doesn't duplicate if it runs again.
