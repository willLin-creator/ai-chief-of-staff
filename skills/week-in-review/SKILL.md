---
name: week-in-review
description: >
  The Weekly Coach. Reads across all of your sources for the past 7 days, reconstructs what
  actually got done (reconciling completions against evidence), assesses where the week went
  versus goals.yaml, and gives 1-3 concrete changes for working more effectively next week.
  The "AI exec coach: review my week and give me feedback" pattern, built. Runs autonomously
  on Friday afternoon as a scheduled agent; you can also run it manually any time. Trigger when
  the user says "review my week", "run the weekly coach", "how did my week go", "week in
  review", or on the Friday fire.
---

# /week-in-review: the Weekly Coach

## What this is

The retrospective, coaching twin of `work-tracker`. Where work-tracker looks *forward* ("what
should I do today?"), this looks *back* ("what got done, and how do I work better?").

Design constraint: **overload is the enemy.** This does not add a daily knock. It fires once a
week (Friday, the close of the week) and its job includes pruning the system's own noise. It must
end in a small number of concrete changes, never a summary you have to re-read. If nothing needs
changing, it says so in one line.

## When it runs

- **Autonomously:** Friday afternoon (~4:30pm local is a good default), as one more entry in
  `skills/scheduled-agents/`. A scheduled run is self-contained and can only reach the sources
  its runtime can reach, so it degrades to what is available. This skill file is the
  full-fidelity version. If you run a daily evening wrap, skip it on Friday so the two never
  double-fire.
- **Manually:** run `/week-in-review` any time. A local run also reads the local task and goal
  files, so it is the higher-fidelity path.

## Window

Past 7 days: last Saturday 00:00 local to now. (Manual runs: the last 7 days from now.)

## Step 1: read the sources (past 7 days)

Reuse `work-tracker`'s source list (`skills/work-tracker/references/deliverable-detection.md`),
but read it **retrospectively**: what happened, not what to do. Skip any source that errors and
note what you could not read; never block on one source.

1. **Your CoS channel (`{{COS_SLACK_CHANNEL}}`), last 7 days.** This is the system's own log:
   every morning briefing, midday and evening triage, and work-tracker knock. It is the single
   richest reconstruction of what was flagged, what recurred, and what got attention this week.
   Read it first.
2. **Slack DMs and @-mentions** of you (`{{SLACK_USER_ID}}`) in the window: what people asked of
   you and what you committed to.
3. **Email:** human-sent threads in the window (apply the CoS filter rules: exclude no-reply,
   notifications, newsletters). Which threads did you close, which are still open.
4. **Meeting notes** (Granola / Fireflies / `meeting-notes/`): meetings in the window and the
   action items assigned to you.
5. **Terminal work, the local blind spot.** A scheduled run cannot see work done in the terminal;
   this is where it lives. If you have a session-history tool that can summarize what your agent
   sessions worked on, run it for the past 7 days. If you keep a daily work log (a nightly capture
   of sessions plus git commits), read that too. Without either, `git log --since='7 days ago'`
   across your active repos is the fallback.
6. **Local task and goal surface** (manual runs, or remote if readable):
   - `my-tasks.yaml` and the task archive for the current month: tasks completed vs slipped.
   - `CURRENT_TASK.md`: what you were mid-flight on.
   - the work-tracker state file: planned knocks, Sent log, commitments, pending asks (what the
     system said it would do vs what happened).
   - `goals.yaml`: the yardstick for Step 2. Read this every run.

## Step 2: compose the coach (three parts, in order)

```
Weekly Coach: [Mon DD] to [Mon DD]

What got done:
- [completions reconstructed from evidence: shipped work, closed threads,
  meeting action items delivered]
- [work that looks done but is not marked complete -> "Close these? [list]"]
- [what slipped: named, with the reason if the evidence shows one]

Where the week went:
- [time and attention vs your top goals (goals.yaml). Did the week advance goal X,
  or drift? Name the drift plainly. 2-4 lines. This is the honest mirror.]

How to work better next week (max 3):
1. [concrete change grounded in this week's evidence]
2. [...]
3. [overload audit: what knocked you most this week, what to turn down or
   off. The coach prunes the system.]
```

Rules for the output:

- **Evidence, not memory.** "What got done" is reconstructed from the sources, not guessed. Close
  loops actively: propose marking done-but-unmarked tasks complete (CLAUDE.md Part 7E).
- **The mirror is honest.** Part 2 names drift plainly. If the week's calendar and attention did
  not advance the top goal, say so.
- **Ends in at most 3 concrete actions,** never a summary. If a section has nothing worth saying,
  one line: "Nothing to change here." Do not manufacture advice.

## Step 3: evaluator pass (before presenting or posting)

Per CLAUDE.md Part 7.I. Draft, then spawn a skeptical evaluator sub-agent: assume the draft is
wrong, challenge it on (a) goal alignment vs `goals.yaml`, (b) decision-grade: is "how to work
better" three concrete actions or vague platitudes, and is "what got done" evidence-based or
guessed, (c) send-ready. The evaluator lists critiques; it does not rewrite. Then reconcile with
full context: adopt genuine misses, discard context-blind flags, finalize. Present or post only
the final.

## Step 4: deliver

- **Autonomous (Friday trigger):** post one message to `{{COS_SLACK_CHANNEL}}`. No emojis beyond
  the lead one, concise, mobile-readable. If the coach detected system friction (a source that
  kept erroring, a knock you ignored every day, a manual step you repeated), append one line:
  "system tune-ups worth reviewing: run /self-heal".
- **Manual:** present in-session. Offer to action the loop closures it proposes (mark tasks
  complete, draft the slipped follow-ups) and any noise changes it recommends. Changes to
  triggers or config are proposals you approve (Part 9), never applied silently.

## Relationship to the rest of the system

- Distinct from any Monday market or metrics synthesis, which is *external*. This coach is
  *internal*: your own week.
- Distinct from an engineering retrospective (commits, code quality). This is the chief-of-staff
  retrospective.
- Reuses `work-tracker`'s detection sources; adds the retrospective and coaching lens
  work-tracker does not have.
- Feeds `/self-heal`, which turns the friction this coach surfaces into prepared, evaluated
  changes to the system itself.
