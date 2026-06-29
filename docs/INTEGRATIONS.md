# Integrations & Tooling — what to set up for your role

This system works with **whatever you connect** and skips the rest. Every skill
degrades gracefully: if an integration isn't connected, that step is silently
skipped. So start minimal and add tools as you feel the need.

This guide answers: *which tools do **I** actually need?*

---

## How integrations connect

Integrations are [MCP servers](https://modelcontextprotocol.io) you connect to
Claude Code. The only hard requirement for the whole system is **Claude Code itself**.
Everything below is optional and additive.

---

## What each integration powers

| Integration | Powers | Without it |
|---|---|---|
| **Google Calendar** | `/gm` calendar review, scheduling proposals, meeting timing | No calendar awareness; scheduling becomes manual |
| **Gmail** (or email MCP) | `/triage` inbox, `/gm` urgent scan, `/enrich` interaction history, meeting follow-ups | Email steps skipped |
| **Slack** | `/triage` DMs/mentions; **delivery** for `work-tracker` + `scheduled-agents` | Proactive layer can't post; console fallback only |
| **Granola** and/or **Fireflies** | `/meeting` transcript pull + synthesis | `/meeting` falls back to manual paste |
| **Task tracker** (Jira, Linear, etc.) | `/meeting` auto-creating tickets for product-change items | Action items still captured; just no auto-tickets |
| **Project board** (Trello, Linear, etc.) | Tracking build/work items in `work-tracker` detection | That source is skipped in detection |
| **CRM** (HubSpot, Salesforce, etc.) | Richer `/enrich` relationship data | `/enrich` uses email/calendar/Slack signals only |
| **Google Docs / Sheets** (via `scripts/`) | Reading/writing planning docs, roadmaps, reports | Those read/write helpers unavailable |
| **WhatsApp / iMessage** | `/triage` personal channels | Those channels skipped |
| Session-history / compounding tool *(optional)* | `/gm` "yesterday" recap, `/meeting` learning capture | Those optional steps skipped |

**Local-only (no integration needed):** `/my-tasks` (reads `my-tasks.yaml`), the
contacts system (`/enrich` file maintenance), goals, and all persona context.

---

## Setup by role

Pick the row closest to you. **Core** = set up first. **Recommended** = the payoff
tools for your role. **Optional** = add if/when you feel the gap. **Skip** = you
likely don't need it.

### Everyone — the minimal core
- **Core:** Claude Code + the context files (`CLAUDE.md`, `goals.yaml`, persona)
- **Recommended:** Google Calendar (powers `/gm`)
- Start here. `/gm` and `/my-tasks` work immediately. Add the rest later.

### Executive / Founder / Chief of Staff
- **Core:** Calendar + Gmail + Slack
- **Recommended:** Granola/Fireflies (meetings), `scheduled-agents` → your CoS Slack channel
- **Optional:** CRM, Google Docs/Sheets
- **Skip:** task tracker, GitHub (unless you're also building)
- This is the full reactive + proactive CoS loop.

### Product Manager
- **Core:** Calendar + Gmail + Slack + a task tracker (Jira/Linear)
- **Recommended:** Granola/Fireflies + Google Docs/Sheets (roadmaps, PRDs, reports)
- **Optional:** project board, analytics digest for the `/gm` Monday metrics pulse
- **Skills:** the **product track** in `commands/product/` — `/prd`, `/roadmap`, `/roadmap-edit`, `/idea`, `/insights`, `/bet`
- `/meeting` shines here: it classifies action items and drafts tickets in your tracker.

### Engineer / Builder / IC
- **Core:** Calendar + a project board or task tracker (Linear/Trello/Jira)
- **Recommended:** GitHub MCP, Granola/Fireflies
- **Optional:** Slack delivery for `work-tracker`
- **Skip:** CRM, heavy email triage (unless inbox is a burden)

### Sales / GTM / Partnerships
- **Core:** Calendar + Gmail + a CRM (HubSpot/Salesforce)
- **Recommended:** Slack, `/enrich` for relationship cadence, Granola/Fireflies
- **Optional:** Google Docs/Sheets
- **Skip:** task tracker, GitHub
- `/enrich` + the contacts system is your engine: never let a key relationship go stale.

### Personal productivity (no work stack)
- **Core:** Calendar + `/my-tasks` (local)
- **Optional:** personal email, WhatsApp/iMessage for `/triage`
- **Skip:** everything work-specific (Jira, CRM, Slack, GitHub)

---

## Wiring it up

1. Connect the MCP servers for your row above (see each tool's MCP setup docs).
2. Tell `CLAUDE.md` Part 11 which servers you connected, so Claude knows where
   information lives (the "Source Routing" table).
3. For the Google Docs/Sheets scripts, follow `scripts/README.md` and set the env
   vars in `.env`.
4. For Slack delivery + scheduled runs, follow `skills/scheduled-agents/SKILL.md`.

You can always add more later. The system is built to grow with you, not to demand
a full stack on day one.
