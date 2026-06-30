# Onboarding — set up your AI Chief of Staff

A guided, step-by-step setup. Plan for **30-45 minutes**. Works with any AI agent tool
that can read a context/instructions file and run prompts — Claude Code, Cursor, Gemini
CLI, and others.

---

## Fastest path: let your agent run it

If you're using Claude Code, you don't have to do this by hand. This installs into your Claude config dir (`~/.claude/`), not the folder you cloned into, so the agent places it there first, then onboards you. Clone the repo and paste:

> I just cloned the ai-chief-of-staff repo. Install it into my Claude config: copy CLAUDE.md and the example data into ~/.claude, symlink commands/ and skills/ so the slash commands and skills load, and create the memory/learnings/meeting-notes folders. Then onboard me per ONBOARDING.md: source from my existing docs and recent messages where you can, interview me only for what's missing, and fill in CLAUDE.md, the persona files, goals, and my voice profile. Don't make me hand-edit templates.

It places the system and drives setup interactively. Once installed, `/onboard` re-runs it anytime. The steps below are the same flow, for reference or for doing it manually.

## How this maps to your tool

This kit uses Claude Code conventions by default, but the design is tool-agnostic.
Wherever a step says `CLAUDE.md` or `/command`, substitute your tool's equivalent:

| Concept | Claude Code | Cursor | Gemini CLI | Generic |
|---|---|---|---|---|
| Context / instructions file | `CLAUDE.md` | `.cursor/rules` | `GEMINI.md` | your agent's system/context file |
| Reusable command | `/gm` etc. (`commands/`) | a saved prompt | a saved prompt | "paste the skill's prompt" |
| Config / home dir | `~/.claude/` | project root | `~/.gemini/` | wherever your agent reads config |
| Memory loaded each session | auto-loads `MEMORY.md` | `@`-reference the file | include in context | paste/reference your index |

If your tool can't auto-load context, just paste the relevant file at the start of a
session. Everything here is plain Markdown, so any tool can use it.

---

## Step 0 — Prerequisites (5 min)

- An AI agent tool installed and working.
- (Optional) accounts for the integrations you'll use — see `docs/INTEGRATIONS.md`.
- Python 3 if you want the Google Docs/Sheets helper scripts.

## Step 1 — Clone and copy templates (2 min)

```bash
git clone <your-fork-url> ai-chief-of-staff
cd ai-chief-of-staff
cp goals.example.yaml goals.yaml
cp my-tasks.example.yaml my-tasks.yaml
cp voice-profile.example.md voice-profile.md
cp .env.example .env
cp memory/MEMORY.example.md memory/MEMORY.md
```

These copies are gitignored — they hold your real data and never get committed.

## Step 2 — Tell it who you are (10 min)

Fill in every `{{PLACEHOLDER}}`:

- [ ] `CLAUDE.md` — name, role, company, hard constraints, integrations
- [ ] `persona/SOUL.md` → save your filled copy as `SOUL.md` (root, gitignored)
- [ ] `persona/IDENTITY.md` and `persona/STRATEGY.md` → same
- [ ] `goals.yaml` — your real current priorities

This is the foundation. `SOUL.md` is *you* (who you are, what you optimize for). `IDENTITY.md` and `STRATEGY.md` are your **organization** — its identity and its current strategy — the background that grounds the assistant's decisions in your company's reality. **If you ran `/onboard`, the agent drafts these for you instead of handing you blank files** — sourcing IDENTITY and STRATEGY from existing material (a strategy/OKR doc, the company site, a deck) and interviewing you for the parts of `SOUL.md` that aren't written down anywhere, then asking you to confirm or tweak. Spend your attention on `SOUL.md`.

## Step 3 — Capture your voice (10 min)

So every drafted email/Slack/doc sounds like *you*, not like an AI. Run the `voice`
skill (`skills/voice/SKILL.md`). Give it real samples — best to worst:

1. Point it at a **Slack thread** or your **recent sent emails**, or
2. **Paste 2-3 short messages** (one casual, one professional, one handling a hard thing).

It extracts your tone, cadence, sign-offs, and quirks into `voice-profile.md`. Review
that file and fix anything that's off. Confirm `CLAUDE.md` Part 4 points to it.

- [ ] `voice-profile.md` built and reviewed

## Step 4 — Connect your tools, by role (5-15 min)

Open `docs/INTEGRATIONS.md`, find the row closest to your role (Founder, PM, Engineer,
Sales, Personal), and connect the **Core** set first. You don't need everything — every
skill skips gracefully when an integration isn't connected.

- [ ] Core integrations for your role connected
- [ ] `CLAUDE.md` Part 11 "Source Routing" updated to list what you connected

## Step 5 — Turn on the second brain (3 min)

Persistent memory is what makes the assistant compound instead of starting cold.

```bash
mkdir -p memory learnings meeting-notes
touch lessons.md CURRENT_TASK.md
```

Read `skills/second-brain/SKILL.md` for the memory format. You already copied
`MEMORY.md` in Step 1.

- [ ] memory dirs + `lessons.md` + `CURRENT_TASK.md` created

## Step 6 — Make it run on its own (the point)

This is what turns the kit from "commands you run" into a chief of staff that operates
**around you**. Follow `skills/scheduled-agents/SKILL.md`: create a dedicated CoS Slack
channel, set the placeholders, and schedule the morning / midday / evening / market-pulse
runs. In steady state these run without you — the one command you'll still trigger by hand
is `/meeting`.

If your tool can't schedule yet, run the commands manually in the meantime, but set up
scheduling as soon as you can. The autonomy is the design, not an add-on.

- [ ] CoS Slack channel created, placeholders set, triggers scheduled

## Step 7 — First run and verify (5 min)

Day-to-day you won't run these by hand — they're scheduled (Step 6). This is a one-time
check that each piece works.

- [ ] Run the morning brief (`/gm` or paste its prompt) — does it read your calendar/tasks?
- [ ] Run a triage (`/triage`) — does it tier correctly?
- [ ] Ask it to **draft a test email**, then check it against `voice-profile.md`. Sound like you?

If the email doesn't sound like you, add a better sample to `voice-profile.md` and retry.

## You're live — the 1-week tuning loop

The system is designed to improve through small, frequent edits:

- When a draft or decision misses, correct it and log the correction to `lessons.md`.
- When you learn something durable, save a memory (`skills/second-brain`).
- Re-read `CLAUDE.md` after the first week and tighten anything that felt off.

---

## Setup checklist

```
[ ] Step 1  Templates copied
[ ] Step 2  CLAUDE.md + persona + goals filled
[ ] Step 3  Voice profile built and verified
[ ] Step 4  Integrations connected for your role
[ ] Step 5  Second brain initialized
[ ] Step 6  Scheduled agents + Slack (the autonomous layer)
[ ] Step 7  First brief run + voice verified on a test draft
```
