# Architecture

## The idea

Most "AI assistant" setups are a single prompt. This is an **operating system**: a
layered context that defines who Claude is working for and how, plus a set of skills
that act on that context, plus integrations that connect it to your real life.

## The context layers (read order)

Claude reads these in order. Each grounds the next.

1. **`SOUL.md`** — the personal throughline. Who you are and what you optimize for.
   Read first because it grounds *interpretation* of everything else.
2. **`goals.yaml`** — current priorities. The source of truth for "what should I work on?"
3. **`CLAUDE.md`** — the operating manual. Principles, guardrails, operating modes,
   writing voice, always-on responsibilities, and integrations.
4. **`IDENTITY.md`** — your organization's identity (mission, beliefs, what it won't do). Background that grounds decisions in the company's reality.
5. **`STRATEGY.md`** — your organization's current strategy and operating context. Keeps tactical work aligned with the plan.

## The skill layers

### Default mode: autonomous

The system is built to operate **around you**. In steady state the scheduled layer and
the work-tracker run the day; you trigger almost nothing.

- `skills/scheduled-agents/` — runs the brief / triage / wrap / market-pulse on a
  schedule and posts to your channel.
- `skills/work-tracker/` — the "knock on the door" chief of staff that plans the day,
  scores deliverables, and interrupts only when something needs you.

### On demand (when you want to pull, not wait)

The same capabilities are also slash commands in `commands/`, for when you want
something now:

- `/meeting` — **the one most people actually run by hand**: process a meeting when
  you need its content for your next task.
- `/gm`, `/triage`, `/my-tasks`, `/enrich` — manual entry points to what the scheduled
  layer otherwise runs for you.
- Product track (`commands/product/`) — `/prd`, `/roadmap`, `/idea`, etc., invoked when
  you're doing product work.

### How the work-tracker runs (the proactive engine)

`skills/work-tracker/` — the "knock on the door" chief of staff. Two modes:

- **Plan mode** (once each morning): detect candidate deliverables across your
  connected systems, score them with a 4-lens P-score (Stakeholder Pull, Strategic
  Fit, Time Pressure, Leverage Multiplier), survey the day, and schedule the day's "knocks."
- **Knock mode** (each scheduled knock): re-evaluate the moment, and if it's still a
  good time, post one of three things to Slack — a pre-meeting briefing, a deadline
  nudge, or a focus recommendation.

`skills/scheduled-agents/` — the cron + Slack delivery layer that runs the morning
brief / midday triage / evening wrap automatically and posts to your CoS channel.

## The knowledge layer (second brain)

What turns single sessions into a compounding system. Plain files, not a database:

- **`memory/`** — atomic, durable facts (one per file, with frontmatter), indexed by
  `MEMORY.md` which loads each session. Four types: `user`, `feedback`, `project`, `reference`.
- **`lessons.md`** — corrections turned into rules, so mistakes don't repeat.
- **`learnings/`** — dated deep-dive docs for insights too rich for one memory line.
- **`meeting-notes/`** — the context library `/meeting` writes and compounds.
- **`CURRENT_TASK.md`** — session handoff: what's in flight + the exact next step.

See `skills/second-brain/SKILL.md`. This is why the assistant gets sharper over time
rather than starting cold each session.

## The enforcement layer (hooks)

Every rule the assistant follows sits in one of three tiers. **hook**: a script in `hooks/` wired
into the runtime's tool events enforces it mechanically. **pinned**: it sits in an always-loaded
block of `CLAUDE.md` or `MEMORY.md`. **recall**: a memory's description surfaces it when a task
makes it relevant. Instructions get skipped under load; mechanisms do not. A rule earns a hook by
recurring in `lessons.md`, and the hooks that ship (`hooks/README.md`) are the ones that did.

Hooks fail open, act on outbound content rather than conversational replies, prefer a closed
high-precision pattern to a broad one, and each carry a one-call override named in the deny
message. `hooks/test-hooks.sh` feeds each one the JSON the runtime would send and asserts on the
decision.

## The improvement loop

The system is built to get better without anyone editing it unsupervised:

```
correction ──► lessons.md ──► recurs? ──► hook (mechanizable) or pinned (judgment)
                   │                              ▲
                   ▼                              │
        Friday: /week-in-review ──► /self-heal ───┘  (Observe > Propose > Evaluate > Gate > Apply > Record)
                                        │
                                        └── every change waits for your "Y"; safety rules can only be strengthened
```

`scripts/rotate-lessons.py` keeps `lessons.md` small enough to actually be read, because the loop
depends on the review happening. The companion
[agent-eval-loop](https://github.com/willLin-creator/agent-eval-loop) turns the "recurs?" step
into a per-rule number and recommends promotions and relaxations in both directions; a hook that
keeps leaking corrections is a hook with a gap. Autonomous output (scheduled posts, knocks) runs
through Generate → Evaluate → Reconcile (`CLAUDE.md` Part 7.I): a skeptical evaluator challenges,
the primary agent with the most context decides.

## The integration layer

MCP servers connect the system to reality: Gmail, Google Calendar, Slack, Granola/
Fireflies. The helper scripts in `scripts/` add Google Docs/Sheets read/write. Every
skill degrades gracefully when a given integration isn't connected.

## The privacy model

The repo is a **template**. The boundary between "framework" (shared) and "your life"
(local) is enforced by `.gitignore`:

| Shared (committed) | Local only (gitignored) |
|---|---|
| `CLAUDE.md`, `persona/*` templates | your filled-in `SOUL/IDENTITY/STRATEGY.md` at root |
| `*.example.yaml` | `goals.yaml`, `my-tasks.yaml` |
| `EXAMPLE-*` contacts | real `contacts/*.md` |
| skills, scripts, hooks, docs | `memory/`, `learnings/`, `meeting-notes/`, `.env`, all tokens/creds |
| `self-heal/ledger.example.md`, `demo-mode-patterns.example.txt` | your `self-heal/ledger.md` and backups, `demo-mode.json`, `demo-mode-patterns.txt`, `lessons-archive/` |

This is why the system can be open-source and personal at the same time: the
intelligence lives in the framework; the private data never leaves your machine.

## Design principles

- **Push hard, but never act unilaterally.** Strong recommendations; zero messages
  sent without explicit approval.
- **Detect, don't depend on input.** The proactive layer watches your real systems
  rather than asking you to maintain a parallel todo list.
- **Leverage over loudness.** Prioritization biases toward what compounds, not what's
  noisiest.
- **Improve through small edits.** Corrections become rules (`lessons.md`); rules that
  recur become mechanisms (`hooks/`); the mistake rate drops over time.
- **The system never edits itself unsupervised.** `/self-heal` prepares and evaluates
  changes; you approve each one.
