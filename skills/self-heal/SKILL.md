---
name: self-heal
description: >
  The self-healing loop. Turns the weekly review into prepared, evaluated improvements to the
  system itself (skills, trigger prompts, cadences, workflow rules), never to the user's behavior
  and never to safety rules. Observe -> Propose (prepare real diffs) -> Evaluate (a skeptical
  second agent judges usefulness) -> Gate (the user approves) -> Apply -> Record. Nothing is
  applied without explicit approval. Run weekly after the Weekly Coach, or when the coach appends
  "system tune-ups worth reviewing", or when the user says "self-heal", "run self-heal", "tune up
  the system", "what should the CoS improve".
---

# /self-heal: the self-healing loop

This operationalizes CLAUDE.md Part 9 (Claude proposes, you execute) and Part 7.I (Generate ->
Evaluate -> Reconcile), run proactively off the weekly review. It improves the SYSTEM, not you.
The coach coaches you; self-heal improves the machine that coaches you.

## Hard safety rails (read first, non-negotiable)

1. **Never auto-apply.** Every change waits for your explicit "Y" / "apply". An agent editing its
   own governance unsupervised is the thing this loop exists to prevent.
2. **Off-limits set (may STRENGTHEN, never weaken or remove):** CLAUDE.md 1.4 (message-send
   approval), 1.5 (confidentiality), Part 9 itself, every always-on hard rule in `MEMORY.md`, and
   every hook in `hooks/`. If a proposal touches any of these to loosen them, kill it before it
   reaches the evaluator.
3. **Small and reversible only.** Each change is at most 10 lines (Part 9). Back up every target
   before applying. No change that cannot be trivially undone.
4. **In scope:** skill bodies, trigger prompts, cadences and cron times, source lists, new small
   tools, memory hygiene, CLAUDE.md *workflow* rules (not safety rules).

## Step 1: observe (gather this week's friction)

Pull the signals; skip any that error. The primary input is the latest weekly review.

- **The latest Weekly Coach post** in `{{COS_SLACK_CHANNEL}}`: its "how to work better" and
  overload audit are the richest system-friction signal. If a manual `/week-in-review` was just
  run, use that instead.
- **`lessons.md`**: new correction entries since the last self-heal run. A repeated correction is
  a candidate rule or skill fix. If you run
  [agent-eval-loop](https://github.com/willLin-creator/agent-eval-loop), `eval_loop.py graduate`
  gives you the same signal as a per-rule number with a recommendation attached.
- **The work-tracker state file**: top-3 recommendations you ignored (the override signal), stale
  or retired deliverables.
- **Session history or your daily work log**: a manual step repeated many times is a candidate to
  automate.
- **Trigger and cron logs**: a source or job erroring repeatedly is a candidate fix.
- **Market Pulse posts** (if you run the scan): read each post's attention footer plus your
  reactions. Substrate for the two attention lanes below.
- **The ledger** (`self-heal/ledger.md`): do NOT re-propose anything already rejected there; note
  anything applied that did not stick.

## Step 2: propose (prepare real diffs)

For each distinct friction, draft a concrete, prepared change. Not a suggestion: the actual edit,
ready to apply. Each proposal:

```
- id: sh-<date>-<n>
  title: <one line>
  target: <file path | trigger id | cron | new file>
  type: skill-edit | trigger-edit | cadence | claude-md-workflow | new-tool | memory | priority
  lane: A-scanner | B-priority | -   # A/B for Market Pulse proposals, '-' otherwise
  evidence: <the specific thing THIS week that showed the friction>
  change: <exact old -> new edit, or trigger update body, or file content>  (<=10 lines)
  benefit: <what improves; ideally load reduction>
  reversibility: <how to undo>
  risk: <blast radius, one line>
```

Run the off-limits check (rail 2) on every draft and drop violators here, before the evaluator.
Cap a run at the ~5 highest-signal proposals. This loop reduces load; it does not generate a
backlog.

## Step 3: evaluate (the skeptical second agent)

Spawn an evaluator sub-agent on a model at least as capable as the one that drafted (evaluator >=
generator). Tell it to assume every proposal is useless and challenge each on:

- **Evidence:** grounded in real, recurring friction from the week, or a one-off, speculative
  "nice to have"? Kill speculation.
- **Goal alignment:** does it serve `goals.yaml`, or is it clever but off-mission?
- **Net load:** does it genuinely reduce your load or the system's surface, or add complexity to
  maintain? Scope creep dies here.
- **Reversible and small:** at most 10 lines, trivially undoable?
- **Adoption:** would you actually use this, or is it tidy but not useful?

The evaluator returns keep / revise / kill plus a one-line reason per proposal; it does not
rewrite. Then reconcile with full context: adopt genuine kills and revisions, keep survivors.

## Step 4: gate (present to the user)

Show survivors, ranked, decision-grade. Per proposal: title, one-line evidence, the prepared diff
(so you can read the exact change), benefit, risk and reversibility. Then: "Approve which? (e.g.
'apply 1,3', 'Y all', 'skip 2')." Apply NOTHING yet.

If nothing survived: say so in one line. A quiet week with no useful system change is a good
outcome, not a failure. Do not manufacture proposals.

## Step 5: apply (only what was approved)

For each approved proposal:

1. Back up the target to `self-heal/backups/<date>/`.
2. Apply the change (Edit/Write for files; your scheduler's update path for triggers).
3. If the target is `CLAUDE.md` operating substance and you keep a mirror for a second runtime
   (an `AGENTS.md`), re-adapt the same change there. It is a hand-adapted mirror, not a copy.
4. If it is a new rule from a repeated correction, also log it in `lessons.md`.
5. For Market Pulse proposals, use the lane-specific apply path below: Lane A applies to the scan
   trigger; Lane B is routed to `/roadmap` or `/idea` -> `/bet`, never a direct roadmap edit.

## Step 6: record (so the loop learns your taste)

Append every proposal to `self-heal/ledger.md`: date, id, title, lane, evaluator verdict, your
decision (applied / skipped / rejected), and the reason. Start from `self-heal/ledger.example.md`.
The ledger is what stops the loop from re-pitching rejected ideas and shows which kinds of change
you accept over time.

## Market Pulse attention lanes (two lanes, folded into this loop)

If you run a Market Pulse scan (`skills/work-tracker/references/market-pulse.md`), have it emit an
attention footer every run (Noise / Off-list surfaced / High-signal). Aggregate those across the
last ~2 weeks and split proposals into two independent lanes, each with its own gate group and its
own ledger row. Never blend them.

**Lane A, scanner focus (what the scan watches).** Retunes the trigger prompt.

- Promote: an off-list player or topic surfaced 2+ times -> add it to the watchlist.
- Demote: a scanned item in "Noise" ~4+ consecutive runs -> drop it or move it to a wildcard slot.
- Deepen: a recurring "High-signal" item -> add a targeted query or sub-topic.
- type: `trigger-edit`, lane A. Preserve the post channel, the evaluator pass, and the footer;
  Lane A retunes what is watched, never removes these.

**Lane B, company priority (what you work on).** Turns recurring market shifts into gated
attention changes for the roadmap, not edits self-heal makes itself.

- Signal: the same direct threat or directional move recurs across runs, or an actionable hook
  repeats unactioned.
- Propose a bump / demote / add with the recurring evidence. type: `priority`, lane B.
- Apply = route the approved item to `/roadmap` (epic reprioritization) or `/idea` -> `/bet` (a
  new bet). Self-heal never rewrites the roadmap, epics, or bets directly.

Both lanes still pass Step 3 and Step 4; present them as two separate groups. A quiet fortnight
with no attention change is a fine outcome.

## Relationship to the rest of the system

- Input is the Weekly Coach (`skills/week-in-review/`); the coach appends a one-line "system
  tune-ups worth reviewing: run /self-heal" when it detects friction.
- It is the proactive engine of Part 9 and the `lessons.md` mechanism. Build the watcher before
  building a smarter agent.
