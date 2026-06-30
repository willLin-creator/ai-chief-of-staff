# /onboard — Guided First-Run Setup

## Description
Walk a new user through setting up their AI Chief of Staff, one step at a time, like onboarding a new hire. Use on first install, or whenever the user says "set me up" / "onboard me."

## Instructions

You are onboarding the user to their own AI Chief of Staff. Use `ONBOARDING.md` as the source of truth, but **drive it conversationally**. Do not dump all the steps at once, and do not make the user hand-edit raw template files. Ask what you need, then write the files for them.

**Source before you ask.** Most people already have most of this written down, and some just want it done. Before interviewing, ask whether they have existing material you can build from (a strategy or planning doc, OKRs, a company page, their resume or LinkedIn) or want you to look things up. Then draft from real sources and have them confirm or tweak, rather than handing them a blank page. Offer two modes, and mix freely per file:
- **Fast / sourced** — you pull from their docs and the web, draft everything, they review and adjust. Best when material exists or they're short on time.
- **Deep / interview** — you ask the reflective questions. Best for what isn't written down anywhere (most of SOUL).

**Install before you configure.** This framework runs from the user's Claude config dir (`~/.claude/` for Claude Code), not the folder they cloned into, so the slash commands, skills, and `~/.claude/...` data paths resolve. If it isn't installed yet, place it first per `docs/SETUP.md`: copy `CLAUDE.md` and the example data into `~/.claude/`, symlink `commands/` and `skills/`, and create the `memory/` `learnings/` `meeting-notes/` dirs. It needs normal write access to `~/.claude/`, nothing elevated.

1. **Read `ONBOARDING.md` and `docs/SETUP.md`** so you know the full flow.
2. **Go one step at a time.** For each, ask only what you need, then fill in the file:
   - **Identity (the foundation).** These files are the throughline that grounds every later decision, so build them with care, in order, drafting each and reading it back before moving on. For each, **source first where you can, then fill the gaps by interview**:
     - **`persona/SOUL.md`** (read first by the system; the "why"). Hardest to source, but you don't have to start from a blank page: with their OK, read a sample of their own recent Slacks and sent emails and synthesize a first draft of how they think, what they care about, and how they operate, then refine it with them. Otherwise interview: who they are beyond their title, what they optimize their life for, where they want hard pushback and where they don't, what a good day looks like, what they keep getting wrong. Draft in the first person, in their voice. A quick three-question version is fine if they're short on time; just flag that a richer SOUL makes everything downstream sharper. (Reading their messages needs Slack/Gmail connected.)
     - **`CLAUDE.md`** — operational config: name, role, company, hard constraints, writing voice, integrations. **Company context here is sourceable:** web-search the company, or read any site or one-pager they point you at, and draft it.
     - **`persona/IDENTITY.md`** — their **organization's** identity: mission, the beliefs it operates from, who it serves, what it won't build. This is background that grounds decisions in the company's reality, not a personal bio. **Sourceable:** draft from a mission/values doc, the company site, or a deck, then have them confirm.
     - **`persona/STRATEGY.md`** — the **organization's** current strategy and operating context: target problem, approach, segments, metrics, tracks of work, non-goals, and the team/stakeholder facts worth knowing. **Best sourced from documents:** ask for their strategy / OKR / planning docs or a board deck, read them, synthesize, and have them confirm or tweak.
     The quality of everything downstream depends on these, but sourced-and-confirmed beats blank-and-perfect. Get a good draft from real material, then refine.
   - **Goals** → turn their current priorities into `goals.yaml` (pull from their OKRs or planning doc if they have one).
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
