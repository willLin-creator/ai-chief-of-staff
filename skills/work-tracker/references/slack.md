# Slack delivery

All outputs from this skill — briefings, nudges, focus recs — go to Slack. This file covers where to send them, how to format them, and how to handle edge cases.

## Destination

Read the `Slack destination` from the Config section of the state file. Defaults and options:

- **DM to self** (your own Slack user ID) — default for most users who want a personal feed.
- **Dedicated channel** — e.g., `{{COS_SLACK_CHANNEL}}`, a private channel you created for this purpose. Good if you want a searchable archive.
- **Specific person's DM** — unusual, but possible if an EA or someone else routes you.

On first use, ask which you prefer. Save the answer to Config. Confirm any changes back.

## Resolving the destination

Use the Slack tools available:

- To send a DM to self: `slack_send_message` with the channel set to your own user ID. If you don't have the user ID, use `slack_search_users` with your work email to get it, then cache it in Config.
- To send to a channel: `slack_send_message` with the channel name or ID.

If you can't resolve the destination, don't invent one. Surface it (if you're in-session) or log to state and skip this send (if scheduled).

## Message formatting

Slack supports mrkdwn formatting. Use it to keep messages scannable.

- **Bold:** `*bold*` (single asterisks, not double)
- **Italic:** `_italic_`
- **Inline code:** `` `code` ``
- **Block quotes:** start the line with `>`
- **Bullets:** `• ` at the start of a line (use the bullet char, not `- `)
- **Links:** `<https://url|display text>`
- **User mentions:** `<@USER_ID>` — don't use for @mentioning your own name in your self-DM; just use your first name plainly.

Don't use Markdown headers (`#`, `##`) — Slack renders them as plain text with the hash.

## Emoji conventions

One emoji at the start of each message signals the type. Makes it easy to scan a feed:

- 📋 Pre-meeting briefing
- ⏰ Deadline nudge
- 🚨 Escalated nudge (deliverable at risk)
- 🎯 Focus recommendation
- ✅ Confirmation back to you (after you responded)
- 👀 Reconciliation/ambiguity surface ("looks like you sent X — closing?")

Don't overdo it. One lead emoji; no emoji confetti.

## Preview / notification behavior

Slack DM notifications show the first line (or ~100 chars) as the preview. Front-load the most important info:

- Good: `📋 *1:1 with your manager* — 3:00pm`
- Bad: `Here's your briefing for later this afternoon…`

Since you may see only the preview on a phone lock screen, the preview line alone should be useful.

## Threading

Don't use threads by default. Each briefing/nudge/focus rec is a standalone message in the destination channel. If you reply, that thread can be read and processed — but the skill sends top-level messages.

Exception: if a nudge escalates (e.g., a second nudge on the same deliverable later in the day because it's now urgent), optionally reply in thread to the original nudge rather than sending a new top-level message. Keeps the feed clean.

## Timing — don't send when the moment is wrong

Timing judgment lives primarily in `references/knock-moments.md`, not here. Before composing any message, the skill already decided this is a good moment. But a few Slack-specific rules:

- **Off-hours (evenings, weekends):** Respect them by default. Exception: a briefing for a meeting that starts within the next hour — send it, because the meeting itself doesn't care. Use a slightly softer tone ("heads up for your 7pm call…").
- **Just-woke-up window:** Your first reactive moment of the day is a reasonable knock moment, but don't pile a nudge onto a briefing onto a focus rec — pick the most useful one.
- **Late replies:** If you reply to a knock hours later, update state but don't chain follow-up knocks unless genuinely needed.

## Response handling

When you reply to a message this skill sent, the reply is signal for the next run. The skill can:

- Parse simple acknowledgments: "done", "dropped", "moved to Friday", "on it" → update state accordingly.
- Handle requests in-thread: "yes draft it" (from a nudge's "want me to…?" offer) → kick off that work.
- Ignore vague replies: a thumbs up or "k" is acknowledgment, no state change needed.

Reply back briefly to confirm state changes: `✅ Closed pricing feedback. Logged.`

## Failure modes to avoid

- **Don't double-post.** Check the Sent log before every send. If a briefing for the 3pm was already sent, don't send another unless meaningful new info appeared.
- **Don't spam on detection bugs.** If the skill detects what it thinks are 5 new commitments from a single meeting and they look wrong (e.g., parsing errors), don't send 5 nudges. Surface it as one message: "found these in your 2pm meeting — add to tracker? [list]".
- **Don't send unprovable signal as fact.** "Looks like you shipped X" is fine. "You shipped X" when you're not sure is not.
- **Don't exceed one message per moment.** Even if briefings + nudges + focus would all theoretically apply, send the one that's most valuable.

## Confirming destination on first use

On the very first run, before sending anything, confirm the destination in the current session:

```
I'll send briefings, nudges, and focus recs to [default: your self-DM].
Works? Or want them in a channel (e.g., {{COS_SLACK_CHANNEL}})?
```

Save the answer immediately and use it from then on. Don't ask again unless you change it.
