# /gm — Morning Briefing

## Description
Start your day with a structured briefing: today's calendar, priority tasks,
urgent messages, and upcoming deadlines. Know exactly what matters before
you open your inbox.

## Instructions

You are running the morning briefing for {{YOUR_NAME}}. Follow these steps
in order, collecting information before presenting the final briefing.

### Step 0: Get Current Time

Get the authoritative date and time (e.g., via the calendar MCP's current-time
tool). Extract the day of week, date, and timezone. Never guess the day of week.

### Step 1: Calendar Review

Fetch today's calendar events for today's date range.

For each event, note time/duration, title/attendees, whether it needs prep,
and any conflicts or back-to-back meetings.

Flag:
- Meetings that conflict with hard constraints (e.g., dinner time)
- Back-to-back meetings with no buffer
- Meetings with no clear agenda or purpose

### Step 2: Task Review

Read `~/.claude/my-tasks.yaml` and identify:
- Tasks due TODAY (urgent)
- Tasks OVERDUE (critical)
- Tasks due in the next 3 days (approaching)
- Tasks that can be completed today given the calendar

### Step 3: Goals Check

Read `~/.claude/goals.yaml` and briefly assess:
- Which goals have stalled (no progress update in 7+ days)?
- Does today's calendar align with the highest-priority goals?
- Any goal-aligned work that should be scheduled today?

### Step 4: Inbox Quick Scan (if an email MCP is connected)

Do a quick scan of email for anything urgent from the last 12 hours.
Flag Tier 1 items (from key contacts, marked urgent, or time-sensitive).
Don't do a full triage — just surface what's critical.

### Step 4.5: Yesterday's Working Memory (optional)

If you use a session-history tool that can summarize what your past agent
sessions worked on yesterday, pull a 1-line summary per session (max 3).
This closes the "where did I leave off?" loop. If unavailable, skip silently.

### Step 4.6: Weekly Metrics Pulse (Mondays only, optional)

If today is Monday and you have a metrics/analytics digest source (e.g., a
weekly product-analytics email), surface 2-3 top signals: usage anomalies,
error/regression spikes, or behavioral patterns worth investigating.
- How to fetch: search email for your weekly digest (e.g., `subject:weekly digest newer_than:7d`)
- If no digest found: skip silently. Mornings are not the moment for manual data fetches.

Cap at 3 bullets. If not Monday or no digest, skip silently.

### Step 5: Present the Briefing

```
Good morning. It's [Day], [Date]. Here's your day:

CALENDAR ([count] meetings)
- [time]  [title] ([duration]) [any flags]

[If applicable: "Heads up: [conflict or concern]"]

TASKS
- DUE TODAY: [list or "Nothing due today"]
- OVERDUE: [list or "All clear"]
- APPROACHING: [list of next 3 days]

GOALS
- [Brief status on top 1-2 goals, especially if stalled]

YESTERDAY (from your sessions)
- [1-line summary per session — max 3, or omit if none]

[MONDAYS ONLY:]
WEEKLY METRICS PULSE
- [signal 1] / [signal 2] / [signal 3]

URGENT
- [Any Tier 1 items from inbox, or "No urgent items"]

FOCUS RECOMMENDATION
1. [Top priority]
2. [Second priority]
3. [Third priority, if time allows]
```

### Guidelines

- Be concise. The whole briefing should fit on one screen.
- Lead with the most important information.
- If there are no urgent items, say so — that's good news.
- The focus recommendation should reflect goal alignment.
- If today's calendar is misaligned with goals, say so explicitly.
- End with an offer: "Want me to run a full triage or prep for any of these meetings?"
