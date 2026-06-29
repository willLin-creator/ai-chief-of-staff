# Signals: what to scan

Signals are the raw activity from your connected tools. This skill converts them into three things: upcoming meetings (for briefings), progress on tracked deliverables (for nudges), and current state of work overall (for focus recs).

The scanning window is **since the last scan timestamp** in the state file's Config. For the first run, use the last 3 days.

## Upcoming meetings (for briefings)

This is the most time-sensitive scan. Run it every invocation.

**Meeting notes tool** (e.g., `list_meetings`, `query_meetings`). If it's calendar-synced, it will show upcoming meetings directly. For each upcoming meeting in the next ~4 hours:
- Capture: title, start time, attendees
- Pull the prior meeting transcript with the same attendees (if any) for recent context

**Email** (`search_threads` with calendar-related queries). Fallback when the meeting notes tool doesn't show upcoming. Look for:
- Recent calendar invites (`filename:invite.ics` or similar)
- Meeting-related threads ("agenda for tomorrow", "notes from our 3pm")

**If both sources show nothing and it's a scheduled invocation, exit quietly.** Don't ask where your meetings are — that defeats the point of proactive. If you invoked the skill manually, it's fine to ask.

## Deliverable progress (for nudges)

For each deliverable in the state file, determine: has anything changed since the last scan? Is progress being made?

**Cloud drive / docs** (`list_recent_files`, `read_file_content`). For docs linked to tracked deliverables:
- Has the doc been edited since the last scan? How substantively?
- Has it been shared with new people (potential completion signal)?
- Are there new comments (potential completion or new input signal)?

**Slack** (`slack_search_public_and_private`, `slack_read_thread`). Search for mentions of the deliverable or its associated people:
- Did you share a draft in Slack?
- Did someone say "looks good" or "got it" on something that might be this deliverable?
- Did someone ping you about it?

**Email** (`search_threads`). Similar: was anything sent or received related to the deliverable?

Update the deliverable's `Last activity` and rough progress estimate based on what you find.

## Commitments and asks (ongoing)

These feed into focus recs and surface new work to track.

**Meeting transcripts** for meetings you attended since last scan. Extract:
- Commitments you made: "I'll…", "let me…", "I can put together…" → add to Commitments
- Asks directed at you: "can you…", "what's your take on…" → add to Pending asks
- Decisions where you own the follow-through → Commitments

**Slack** DMs and @mentions since last scan:
- Unanswered questions to you → Pending asks
- Threads where you said "I'll" → Commitments
- Follow-up pings ("any update?") → upgrade urgency of existing ask

**Email** since last scan:
- Inbound threads ending with a question → Pending asks
- Your outbound "I'll send you X" messages → Commitments
- Unsent drafts → surface in next focus rec ("you have an unsent draft to [recipient]")

**Task file** — read it fresh every scan:
- New items you added → mirror into Deliverables if they look substantive
- Items checked off → move to Retired, confirm once if unsure

## Ignore lists (noise filtering)

Don't treat these as signals:

- Newsletter emails, automated notifications, mass announcements
- Slack channel chatter not directed at you
- Calendar invites for meetings you declined or won't attend
- Drive activity on docs you've only briefly viewed (not editing, not commenting)
- Thanks/acknowledgment messages ("got it", "thx")
- Emoji-only reactions

When in doubt, exclude. Missing a signal is cheaper than false signal.

## Reconciliation

After scanning, before composing any output:

1. **Deduplicate.** Same commitment in meeting notes + Slack + email → one item.
2. **Match signals to existing items.** A new signal about a tracked deliverable is a status update, not a new item.
3. **Detect completions carefully.** "Here's the draft" is probably done → confirm in the next focus rec or briefing, but don't silently mark complete.
4. **Flag contradictions.** If state says "not started" but signals say you already sent it, surface: "looks like you already sent the pricing feedback Tuesday — closing it out."

## Scan budget

Scans happen on every invocation, including scheduled ones. They need to complete fast enough that a scheduled run feels responsive.

- Upcoming meetings scan: always, bounded to next ~4 hours.
- Full signal scan (deliverables, commitments, asks): incremental since last scan. For a mid-day invocation with 2 hours of new activity, this should complete in seconds.
- First-ever run: one-time bigger scan over the last 3 days, note "doing a bigger scan to seed state, one moment."

Budget: if scanning is taking too long, prefer completeness on the most-recent signals and skip the older ones. Better to act on 80% of the signal quickly than 100% slowly.
