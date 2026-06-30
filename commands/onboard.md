# /onboard — Guided First-Run Setup

## Description
Walk a new user through setting up their AI Chief of Staff, one step at a time, like onboarding a new hire. Use on first install, or whenever the user says "set me up" / "onboard me."

## Instructions

You are onboarding the user to their own AI Chief of Staff. Use `ONBOARDING.md` as the source of truth, but **drive it conversationally**. Do not dump all the steps at once, and do not make the user hand-edit raw template files. Ask what you need, then write the files for them.

1. **Read `ONBOARDING.md` and `docs/SETUP.md`** so you know the full flow.
2. **Go one step at a time.** For each, ask only what you need, then fill in the file:
   - **Identity** → from their answers, fill `CLAUDE.md` and the `persona/` files (`SOUL.md`, `IDENTITY.md`, `STRATEGY.md`). Replace every `{{placeholder}}`.
   - **Goals** → turn their current priorities into `goals.yaml`.
   - **Voice** → run the `voice` skill: ask for a Slack thread, recent sent emails, or 2-3 pasted messages, and write `voice-profile.md` so drafts sound like them.
   - **Integrations** → ask their role, point them at `docs/INTEGRATIONS.md`, and confirm which MCP servers they connected. Update `CLAUDE.md` Part 11 to match.
   - **Second brain** → create the `memory/`, `learnings/`, `meeting-notes/` dirs and the `lessons.md` / `CURRENT_TASK.md` files; copy `memory/MEMORY.example.md` to `memory/MEMORY.md`.
3. **Confirm and move on.** After each step, show what you wrote in one line, then continue. Keep momentum.
4. **Finish with a live test:** run `/gm` so they see a real morning briefing, then point them at `skills/scheduled-agents/SKILL.md` to make it run autonomously.

## Guardrails
- **Never send a message to anyone during onboarding.** Drafting only.
- Fill files *for* the user from their answers. Don't hand them a raw template and walk away.
- If something is unclear, ask one question and proceed with a flagged assumption.
- Match their writing voice as soon as `voice-profile.md` exists.
