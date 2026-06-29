---
name: work-tracker
description: "A proactive chief-of-staff delivery layer. Runs a daily planning pass that auto-detects candidate deliverables across your connected systems (email, Slack, meeting notes, task list, planning docs), scores them with a 4-lens P-score framework (Stakeholder Pull, Strategic Fit, Time Pressure, Leverage Multiplier), and maps out when to 'knock' on you during the day. It self-schedules those knocks and re-plans them as the day evolves. Produces three things -- pre-meeting briefings, deadline nudges, and focus recommendations -- delivered to a Slack channel at moments that feel like a good assistant walking up. Trigger when the daily planning run fires, a scheduled knock fires, or you ask to be briefed / what to work on / your top priorities."
---

# Work Tracker -- The Knock on the Door

## The model

Imagine you hired a very good chief of staff. Every morning they look at your calendar, read your deliverables, and plan the day: "I'll brief them at 2:35 before the 3pm, nudge them at 10:30 about the hiring plan, and catch them after the 11am to ask about any commitments that came out of it." During the day they follow their plan but adjust as reality unfolds -- a meeting runs long, a new deliverable lands, you're clearly in flow. A good CoS doesn't stand at the door interrupting; they read the room.

This skill is that CoS. One daily planning run (e.g., 9:00am weekdays) detects deliverables, scores them, and maps out the day's knocks. Each knock is a separate scheduled fire. When a knock fires, it re-reads the current state before acting -- if the moment is wrong, it defers; if new context has landed, it adjusts, and may schedule additional knocks.

The skill has two modes of invocation:

1. **Plan mode** -- the morning daily run. Detects candidate deliverables (`references/deliverable-detection.md`). Scores them with the P-score framework (`references/prioritization.md`). Surveys the day. Decides when and what to knock about. Creates scheduled one-time tasks for each knock. See `references/daily-plan.md`.

2. **Knock mode** -- each scheduled knock fires into this mode. Re-evaluates the moment, sends the message if appropriate, scans for new context, and optionally schedules additional knocks. See below.

Both modes share the same underlying content logic: when it's time to actually say something, the skill uses `references/briefings.md`, `references/nudges.md`, or `references/focus.md` to compose it.

## Why this skill exists -- the mandate

This skill is designed for an operator with a broad delivery mandate (e.g., a head-of-product or chief-of-staff scope at a startup, where one person owns many threads). The mandate it serves is to:

1. **Deliver on your manager's and customers' asks fast** -- speed is a moat at an early stage
2. **Ship high-leverage artifacts** -- strategic narratives, frameworks, positioning, not just task output
3. **Move quickly without dropping balls** -- prevent renewals from slipping, keep the eng team unblocked, and surface decisions before they go stale

The skill's job is to be the unblocking and prioritization layer that makes that mandate doable. It does NOT need you to feed it deliverables -- it derives them from your connected systems. It does NOT pick low-leverage work just because it's loud -- the P-score framework biases toward what compounds.

## The three things the skill says

Just three. Each knock delivers exactly one, never a stack.

1. **Pre-meeting briefing** -- before a meeting. "Before your 3pm 1:1: they're expecting pricing feedback, and the draft hasn't moved since Monday. Two minutes to skim." See `references/briefings.md`.

2. **Deadline nudge** -- when a deliverable is quietly slipping toward a deadline. "The board report is due 5/14 and you haven't touched it in 3 days. Next 45 min is your best window today." See `references/nudges.md`.

3. **Focus recommendation** -- in a gap, or as the morning lead. "You've got 40 min before your 2pm. Highest-leverage thing: reply to the onboarding doc -- they've been waiting." See `references/focus.md`.

All three go to Slack. See `references/slack.md`.

## The daily loop

### Morning daily run (weekdays): Plan mode

The day starts with the morning planning run (triggered by a recurring scheduled agent, e.g., `13 9 * * 1-5`). This run:

1. **Read state.** Clean up leftover knocks from yesterday (disable anything not fired).
2. **Detect candidate deliverables** -- run the full sweep across your email, Slack, meeting notes, task list, your roadmap doc, your project board, and any planning docs you track, plus **yesterday's coding-agent sessions** (optional, if you use such a tool -- catches in-flight work that hasn't landed in any other system yet). See `references/deliverable-detection.md`.
3. **Score every active deliverable** -- apply the 4-lens P-score (Stakeholder / Fit / Pressure / Leverage). See `references/prioritization.md`. Apply auto-rules. Sort.
4. **Survey today** -- calendar / meeting notes for meetings, signals for any overnight activity.
5. **Send a morning focus rec to Slack immediately** -- "here's the shape of the day," leading with the top P-scored deliverable.
6. **Plan the day's knocks** -- for each, decide kind (briefing / nudge / focus), time to fire, and a short prompt describing what to say. Typical plan for a busy day: 3-6 knocks. Knocks target the top 2-3 deliverables; meetings get briefings if they warrant.
7. **Schedule each knock** as a one-time scheduled task. Task description includes enough context that the knock run is self-contained.
8. **Write today's plan into state** under "Today's planned knocks" so knock-mode runs can reference it.

See `references/daily-plan.md` for how to decide knock count, timing, and content.

### Throughout the day: Knock mode

Each scheduled knock fires into this skill in knock mode. Steps:

1. Read state. Find this knock in "Today's planned knocks" -- get its original intent.
2. **Re-evaluate.** Is this still a good moment to knock?
   - Are you actually free, or did a meeting run over?
   - Did the deliverable already complete?
   - Did the meeting this briefing is for get canceled?
   - Are you in deep work?
   See `references/knock-moments.md` for the state model.
3. **Decide:** proceed, defer (reschedule 15 min later), or cancel (original intent no longer valid).
4. If proceeding, compose and send the message to Slack.
5. **Scan for new context.** What's changed since the morning plan? New meetings added? New commitments from meetings you attended? New pings from teammates?
6. **Update the plan.** If the new context warrants additional knocks -- e.g., a new meeting got added for 4pm that needs a briefing, or a new urgent deliverable arrived -- create new one-time scheduled tasks for them. Also cancel/defer any upcoming knocks that are no longer relevant.
7. Log what was sent in state. Mark this knock as fired.

### When you ask directly

You may ping the skill directly ("what should I work on", "brief me for my 3pm", "top 3 today"). In that case, skip the knock-moment evaluation -- you're asking, so respond. Run a quick delta scan, re-score the active list if anything changed since the morning, compose the answer. Don't re-plan the whole day from an ad-hoc ask unless the ask implies something new to track.

## Why this architecture works

Morning planning gives the skill a day-sized view: it can pick high-leverage moments, space knocks out, and avoid bunching messages. Per-knock re-planning gives it resilience: the plan survives contact with reality.

Auto-detection means you don't have to maintain a parallel todo list -- the skill watches your actual systems. Scoring means the surfaced top-3 reflects current reality, not yesterday's hypothesis.

Fixed-interval scheduling (e.g., "every 3 hours") does none of this well -- it pings during meetings, misses brief-able moments, can't adapt to the day's actual shape, and surfaces stale priorities.

## Setup on first install

On the very first use, the skill does the following in order:

1. **Confirm config.** Ask only what isn't already known from your CLAUDE.md and memory:
   - Slack destination (default: DM to your own Slack user ID `{{SLACK_USER_ID}}`)
   - Quiet hours (defaults: before 8am, after 6:30pm, weekends -- per your CLAUDE.md hard constraints)
   - Top customer domains for the renewal-risk weighting (seed from memory + recent emails)
   - Daily planning schedule: `13 9 * * 1-5` (9:13am weekdays; off-minute by design)

2. **Write the initial state file** at `{{STATE_DIR}}/work-tracker_state.md` with the Config block and seeded sections (empty Deliverables, Upcoming meetings, Sent log).

3. **Create the daily planning schedule.** Use the `schedule` skill to create a recurring agent:
   - Name: `work-tracker-daily-plan`
   - Cron: `13 9 * * 1-5` (9:13am weekdays)
   - Prompt: self-contained directive, e.g., *"Run the work-tracker skill in plan mode. Detect candidate deliverables across all sources per references/deliverable-detection.md. Score them via references/prioritization.md. Send a morning focus rec to Slack. Schedule the day's knocks (briefings, nudges, focus recs) as one-time scheduled tasks per references/daily-plan.md."*

4. **Run an initial plan immediately** -- don't wait for tomorrow morning. Detect, score, surface the top 3, and present to you for confirmation before sending anything to Slack.

5. **Trigger the first market scan** to seed the market-pulse doc (see `references/market-pulse.md`) so the next morning plan has a baseline strategic-fit signal.

## Integration with your existing setup

- **CLAUDE.md CoS logic** -- Strategy/priorities live there. This skill handles the delivery layer and the daily cadence.
- **Existing scheduled triggers** -- If you already run other scheduled briefings (morning brief, midday triage, evening triage), work-tracker is additive and does not replace those.
- **Your task list** -- Read freely on every run; write carefully (only check off tasks you explicitly confirm done).
- **Your current-task / pivot file** -- Read for current pivot context.
- **Roadmap skill** -- Source of strategic anchor. Work-tracker reads your roadmap doc, project board, and any planning docs on every plan run.
- **Slack** -- Primary delivery. See `references/slack.md`.
- **Pattern compounding** (optional, if you use such a tool) -- When the morning planning detects a pattern recurring across 3+ days (same deliverable type slipping, same blocker showing up, same kind of nudge needed), surface a prompt: "This pattern keeps coming up. Worth documenting as a learning doc?" Don't auto-fire -- the call on what's worth compounding is yours. One prompt per pattern per week max to avoid noise.

## Core principle

What makes this skill feel like a real CoS is not that it's proactive, it's that it's proactive with **taste** and **judgment**. The morning plan gives it intent; the per-knock re-evaluation gives it sensitivity; the P-score framework gives it judgment about what matters. All three matter. A CoS who stuck rigidly to a morning plan and ignored the day's reality would be annoying; one with no plan would be reactive noise; one without judgment would be a feature factory PM. The discipline here is: **detect the work, score it well, plan the day, then respect the day as it actually unfolds.**

Three rules the skill lives by:

- **If you wouldn't say it in person at this moment, don't say it in Slack.**
- **Better silent than noisy.** A canceled knock is often the right move.
- **One thing per knock.** Even if three things are true, pick one.

Plus one more, baked in via the framework:

- **The top-3 must reflect what compounds, not what's loudest.** A strategically important ask beats a low-stakes loud one if the framework says so. The skill's job is to argue for leverage, not to please.

## Reference files

- `references/prioritization.md` -- the 4-lens P-score framework, auto-rules, tiebreakers, considerations for a broad-scope role
- `references/deliverable-detection.md` -- where candidate deliverables come from and dedup rules
- `references/market-pulse.md` -- the periodic competitive + market scan that feeds Strategic Fit
- `references/daily-plan.md` -- the morning run: detection, scoring, planning knocks, scheduling them
- `references/knock-moments.md` -- the state model for re-evaluating at each knock
- `references/briefings.md` -- pre-meeting briefing content
- `references/nudges.md` -- deadline nudge content
- `references/focus.md` -- focus recommendation content
- `references/slack.md` -- delivery mechanics
- `references/state.md` -- memory file schema (includes today's planned knocks, scored deliverables)
- `references/signals.md` -- per-source scanning guidance
