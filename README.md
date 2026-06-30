# AI Chief of Staff

An open-source operating system that turns [Claude Code](https://claude.com/claude-code) into a proactive personal chief of staff: it triages your inboxes, manages your tasks against your goals, processes your meetings, deepens your key relationships, and proactively surfaces what matters most, on a schedule, in your own Slack channel.

This is a **template**. It ships with the full framework and example data, but none of the author's personal information. You fill in the placeholders and make it yours.

## Background

This is a genericized, open-source adaptation of a personal AI chief-of-staff system I've built, refined, and relied on daily for **3,000+ hours** of real use. It runs my actual workflow: triaging my inboxes, processing my meetings, tracking my work against my goals, capturing knowledge into a second brain, and operating proactively in the background.

The public repository is a fresh extraction with every personal and company detail replaced by templates, so its commit history is recent. **The system it's distilled from is not.** What's here is the framework, hardened by real use, with the private data stripped out.

---

## What makes this different

Most "AI assistant" repos are a prompt or a chatbot wrapper. Two things set this apart:

1. **It's a second brain, not a session.** A file-based memory layer (atomic facts indexed by `MEMORY.md`, plus lessons, learnings, and a meeting-notes context library) means it remembers across sessions and compounds. It gets sharper over time instead of starting cold every chat.
2. **It runs autonomously to 10x your day.** This isn't a tool you open. Scheduled agents and the "knock on the door" work-tracker run your brief, triage, and focus recommendations in the background, then surface the highest-leverage thing at the right moment in a Slack channel you own. You trigger almost nothing.

## What it does

| Capability | How |
|---|---|
| **Morning briefing** | `/gm` — calendar, due/overdue tasks, goal check, urgent inbox items, focus rec |
| **Inbox triage** | `/triage` — scans email/Slack/messages, tiers by urgency, drafts replies in your voice |
| **Task management** | `/my-tasks` — tracks tasks against goals, executes work, never lets a deadline slip |
| **Meeting processing** | `/meeting` — pulls transcripts (Granola/Fireflies), extracts action items, drafts follow-ups, saves to your context library |
| **Relationship CRM** | `/enrich` — maintains contact files, flags relationships going stale by tier cadence |
| **Proactive delivery** | `work-tracker` skill — a "knock on the door" CoS that plans your day, scores deliverables, and posts briefings/nudges/focus recs to Slack at the right moments |
| **Scheduled agents** | runs the above automatically (morning brief, midday triage, evening wrap, market-pulse scan) and posts to your CoS Slack channel |
| **Product track** *(optional)* | `commands/product/` — `/prd`, `/roadmap`, `/roadmap-edit`, `/idea`, `/insights`, `/bet` for product-management work |
| **Second brain** | `skills/second-brain/` — persistent memory: atomic facts indexed by `MEMORY.md`, plus lessons, learnings, and a meeting-notes context library that compound across sessions |
| **Voice matching** | `skills/voice/` — builds a `voice-profile.md` from your real messages so every drafted email/Slack/doc sounds like you, not like an AI |

## The philosophy

The default posture is **clarity → focus → decision → action → improve**. This isn't a passive assistant. It's configured to push hard, challenge your priorities, surface opportunity cost, and optimize for long-term leverage, while never sending a message on your behalf without explicit approval.

## How it's meant to run

This operates **around you, not on command**. Once configured, the scheduled layer runs your brief, triage, wrap, and market-pulse, and the `work-tracker` knocks only when something genuinely needs you. **In steady state you trigger almost nothing.** The one command most people run by hand is **`/meeting`** — when you need a meeting processed for your next task. Treat the other commands as manual entry points to capabilities that otherwise just run.

## Architecture

A layered context system. Claude reads it in this order:

```
SOUL.md        →  who you are, what you optimize for (the "why")
goals.yaml     →  current priorities (source of truth for "what to work on")
CLAUDE.md      →  how Claude operates: principles, guardrails, modes, voice
IDENTITY.md    →  your organization's identity: mission, beliefs, what it won't do
STRATEGY.md    →  your organization's current strategy + operating context
```

On top of that context sit the **skills** (slash commands + the proactive work-tracker) and the **integrations** (MCP servers for Gmail, Calendar, Slack, meeting notes).

```
ai-chief-of-staff/
├── ONBOARDING.md              # ← start here: guided, tool-agnostic setup
├── CLAUDE.md                  # the operating system (fill in the placeholders)
├── persona/                   # SOUL / IDENTITY / STRATEGY templates
├── goals.example.yaml         # → copy to goals.yaml
├── my-tasks.example.yaml      # → copy to my-tasks.yaml
├── voice-profile.example.md   # → built by the voice skill from your real messages
├── contacts/                  # EXAMPLE contact (real ones are gitignored)
├── commands/                  # mostly run on a schedule; /meeting is the main on-demand one
│   └── product/               # product track: /prd /roadmap /roadmap-edit /idea /insights /bet
├── memory/                    # second brain: MEMORY.md index + atomic facts (real ones gitignored)
├── skills/
│   ├── work-tracker/          # proactive "knock on the door" CoS
│   ├── scheduled-agents/      # cron + Slack delivery layer
│   ├── second-brain/          # persistent memory architecture
│   └── voice/                 # capture + apply your writing voice
├── scripts/                   # Google Docs/Sheets helpers (secrets via env)
└── docs/                      # SETUP.md, INTEGRATIONS.md (role-based), ARCHITECTURE.md
```

## Built for Claude Code

This is built for and runs best on **Claude Code** (CLI agentic workflows). That's where you get the full operating system: auto-loaded `CLAUDE.md` + `MEMORY.md`, slash commands, auto-triggering skills, scheduled agents, and the file-based second brain.

**Can you run it in any agent? Honestly, no, not as-is.** The *content* is plain Markdown, so the ideas are portable, but to actually run the system an agent needs three things: **local file access** (to read and write `CLAUDE.md`, `goals.yaml`, `memory/`, etc.), **tool/MCP use** (Gmail, Slack, Calendar), and a **scheduler** for the autonomous parts. What that means in practice:

| Runtime | What you get |
|---|---|
| **Claude Code** | Everything. The system as designed. |
| **Another agentic CLI with file + tool access** (Cursor agent, etc.) | Most of it, by adapting the glue points below. |
| **Chat-only apps** (Claude Desktop, ChatGPT, Gemini app) | A manual subset: load `CLAUDE.md` + a skill into a Project, connect the same MCP connectors, brief/triage in chat. No scheduling, no slash commands, no persistent file-based memory. |

Adapting to another agentic runtime means swapping these glue points (the content stays the same):

| Glue point | Claude Code | Elsewhere |
|---|---|---|
| Load context | auto-loads `CLAUDE.md` + `MEMORY.md` | point the tool at the file, or paste it |
| Invoke a command | `/gm`, `/meeting`, … | paste the command's prompt |
| Trigger a skill | auto-invoked by description | reference or paste the `SKILL.md` |
| Schedule it | scheduled agents | OS `cron`/`launchd` calling a CLI |

See `ONBOARDING.md` for the mapping.

## Get started

Point your agent at the repo. In Claude Code, that's the whole user step:

> Hey Claude, I want to start using https://github.com/willLin-creator/ai-chief-of-staff. Run whatever is necessary to set it up.

Claude reads the setup below, clones the repo, installs it into your Claude config, and runs the onboarding interview, filling everything in for you.

**What the agent does (it follows this; you don't paste any of it):**
1. Clone the repo locally.
2. Install into the Claude config dir `~/.claude/`: copy `CLAUDE.md` and the example data, symlink `commands/` and `skills/`, and create `memory/`, `learnings/`, `meeting-notes/`, `lessons.md`, and `CURRENT_TASK.md`. (Details: [docs/SETUP.md](docs/SETUP.md).)
3. Run onboarding via the `/onboard` skill / [ONBOARDING.md](ONBOARDING.md): source `IDENTITY.md` + `STRATEGY.md` from the user's company and strategy docs, capture their voice from real messages, fill `CLAUDE.md` + persona + `goals.yaml`, and interview only for what isn't written down.
4. Verify with a live `/gm`, then point them at `skills/scheduled-agents/SKILL.md` for autonomy.

Requires write access to `~/.claude/` and the MCP connectors for whatever integrations you want. Prefer to set it up by hand? [ONBOARDING.md](ONBOARDING.md) and [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) walk through it.

## Privacy & safety

- **No personal data ships in this repo.** Your real `goals.yaml`, `my-tasks.yaml`, `contacts/*`, `memory/`, `meeting-notes/`, and filled-in persona files are all gitignored. The repo carries only `*.example.*` templates and `EXAMPLE-` files.
- **Secrets never commit.** `.gitignore` blocks every `*token*`, `*cred*`, `*secret*`, `*.key`, `*oauth*`, and `.env`. Scripts read credential paths from environment variables only.
- **Nothing sends without approval.** Posting status to your own CoS Slack channel is fine; any message to another person always requires your explicit "send."

## Requirements

- An AI agent that can read a context file and run prompts. Built and proven on
  [Claude Code](https://claude.com/claude-code); adaptable to Cursor, Gemini CLI, or a
  custom agent (see [Portability](#portability--works-with-any-capable-agent))
- Optional MCP servers for the integrations you want. **You don't need them all** —
  see **[docs/INTEGRATIONS.md](docs/INTEGRATIONS.md)** for a role-based setup guide
  (Founder, PM, Engineer, Sales, Personal). Common ones: Gmail, Google Calendar,
  Slack, Granola/Fireflies, a task tracker.
- Python 3 for the helper scripts (`google-auth google-auth-oauthlib google-api-python-client`)

## License

MIT — see [LICENSE](LICENSE).
