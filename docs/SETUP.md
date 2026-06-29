# Setup

This guide takes you from a fresh clone to a working AI Chief of Staff.

## 1. Prerequisites

- [Claude Code](https://claude.com/claude-code) installed and working
- Python 3.9+ (for the helper scripts)
- Accounts/MCP servers for the integrations you want (Gmail, Google Calendar, Slack, Granola or Fireflies)

## 2. Clone and copy templates

```bash
git clone <your-fork-url> ai-chief-of-staff
cd ai-chief-of-staff

cp goals.example.yaml goals.yaml
cp my-tasks.example.yaml my-tasks.yaml
cp .env.example .env
```

`goals.yaml`, `my-tasks.yaml`, and `.env` are gitignored. They hold your real data and never get committed.

## 3. Fill in your context

Work through these files and replace every `{{PLACEHOLDER}}`:

1. **`CLAUDE.md`** — your name, role, company, hard constraints, writing voice, and integrations. This is the operating system; spend the most time here.
2. **`persona/SOUL.md`** → fill in, then save your filled copy as `SOUL.md` at the repo/config root (the root copy is gitignored).
3. **`persona/IDENTITY.md`** and **`persona/STRATEGY.md`** → same pattern.
4. **`goals.yaml`** — your real current goals.
5. **`voice-profile.md`** — run the `voice` skill (`skills/voice/SKILL.md`) to build this
   from your real messages, so drafts sound like you. Copy from `voice-profile.example.md`.

The persona templates contain instructions; delete those once you've filled them in.

## 4. Install into Claude Code

Claude Code reads global config from `~/.claude/`. Make the framework available there:

```bash
# Operating system + persona (root-level, gitignored copies)
cp CLAUDE.md ~/.claude/CLAUDE.md          # or merge into your existing one
cp SOUL.md IDENTITY.md STRATEGY.md ~/.claude/ 2>/dev/null

# Data files
cp goals.yaml my-tasks.yaml ~/.claude/

# Slash commands and skills (symlink so repo edits stay live)
ln -s "$PWD/commands/"* ~/.claude/commands/
ln -s "$PWD/skills/"*   ~/.claude/skills/
mkdir -p ~/.claude/contacts && cp contacts/EXAMPLE-*.md ~/.claude/contacts/

# Second brain (persistent memory) — see skills/second-brain/SKILL.md
mkdir -p ~/.claude/memory ~/.claude/learnings ~/.claude/meeting-notes
cp memory/MEMORY.example.md ~/.claude/memory/MEMORY.md   # then clear the examples
touch ~/.claude/lessons.md ~/.claude/CURRENT_TASK.md
```

The second brain (`memory/`, `lessons.md`, `learnings/`, `meeting-notes/`,
`CURRENT_TASK.md`) is what lets the assistant remember and compound across sessions.
See **`skills/second-brain/SKILL.md`** for the memory format and discipline.

(Adjust to taste — some people keep everything in the repo and point Claude Code at it as a project. Symlinking `commands/` and `skills/` keeps your edits versioned.)

## 5. Connect MCP servers

**Not sure which tools you need? See [INTEGRATIONS.md](INTEGRATIONS.md) for a role-based
guide** (Founder, PM, Engineer, Sales, Personal). You do not need them all — start
minimal and add as you feel the gap.

Connect the integrations you want Claude to reach. At minimum, the commands assume some subset of:

- **Gmail** — `/triage`, `/gm` inbox scan
- **Google Calendar** — `/gm`, scheduling
- **Slack** — `/triage`, and delivery for `work-tracker` + scheduled agents
- **Granola and/or Fireflies** — `/meeting`

Each command degrades gracefully: if an MCP server isn't connected, that step is skipped.

## 6. Helper scripts (optional)

```bash
pip3 install google-auth google-auth-oauthlib google-api-python-client
```

Put your Google OAuth client JSON where `.env` points (`GOOGLE_OAUTH_CLIENT_FILE`), then run a script once to complete the one-time browser authorization. See `scripts/README.md`.

## 7. Scheduled agents + Slack delivery (optional)

The proactive layer posts to a Slack channel of your own.

1. Create a dedicated Slack channel for your chief of staff (e.g. `#yourname-cos`).
2. Set the placeholders: `{{COS_SLACK_CHANNEL}}`, `{{SLACK_USER_ID}}`, `{{TIMEZONE}}` (in the work-tracker and scheduled-agents skills).
3. Follow `skills/scheduled-agents/SKILL.md` to create the recurring agents (morning brief, midday triage, evening wrap).

## 8. First run

```
/gm            # morning briefing
/triage quick  # fastest inbox scan
/my-tasks list # see your tasks
```

If those work, you're live. Tune `CLAUDE.md` as you notice rough edges — the system is designed to improve through small, frequent edits.
