---
name: scheduled-agents
description: Run your AI Chief of Staff on a cron schedule and deliver briefings and triages to a dedicated Slack channel (or a self-DM). Use to set up, edit, or manage recurring agents - a Morning Brief, a Midday Triage, an Evening wrap, and an optional Market Pulse scan - and to understand the message-sending guardrail that governs them.
---

# Scheduled Agents + Slack Delivery

This skill describes a reusable pattern: your Chief of Staff runs **unattended on a schedule**, then posts a short briefing or triage to a place only you watch. It turns the assistant from something you have to open into something that walks up to you at the right moments.

The pattern has three parts:

1. A **scheduling mechanism** that fires a prompt on a cron-style timetable.
2. A **self-contained prompt** for each trigger (it gets no chat history, so it must carry its own instructions).
3. A **Slack destination** you own - a dedicated channel or a DM to yourself - where every run posts its result.

Nothing here sends messages to other people. See "Message-sending guardrail" below.

---

## Configuration

Fill these placeholders before setting up any trigger. Keep them in one place (e.g., the top of your state file or a `config` block) so every trigger reads the same values.

```yaml
COS_SLACK_CHANNEL: "{{COS_SLACK_CHANNEL}}"   # dedicated channel you own, e.g. #cos
SLACK_USER_ID:     "{{SLACK_USER_ID}}"       # your own Slack user ID, for a self-DM
TIMEZONE:          "{{TIMEZONE}}"            # IANA tz, e.g. America/New_York

# Cron schedules (expressed in UTC; see "Timezone & DST" below)
CRON_MORNING:  "{{CRON_MORNING}}"   # e.g. fires ~7:00am local
CRON_MIDDAY:   "{{CRON_MIDDAY}}"    # e.g. fires ~12:00pm local
CRON_EVENING:  "{{CRON_EVENING}}"   # e.g. fires ~4:30pm local
CRON_MARKET_SCAN: "{{CRON_MARKET_SCAN}}"  # optional; e.g. Mon/Wed/Fri pre-dawn
```

Pick **one** delivery destination:

- **Dedicated channel (`{{COS_SLACK_CHANNEL}}`)** - recommended. A private channel you create just for this. Gives you a searchable archive of every brief and triage, separate from your real conversations.
- **Self-DM (`{{SLACK_USER_ID}}`)** - simplest. The agent messages your own user ID. Good if you don't want another channel.

Set the destination once and reuse it across all three triggers.

---

## The three daily triggers (default cadence)

Three recurring runs cover most of a working day. Each is independent and self-contained.

### 1. Morning Brief (~7am)

**Purpose:** start the day with a single, scannable picture of what changed overnight and what matters today.

**What it does:**
- Reviews what happened since the previous evening (new email from real people, overnight messages, calendar for today).
- Surfaces anything time-sensitive: meetings today, things due, anything at risk.
- Posts one digest to `{{COS_SLACK_CHANNEL}}`.

If you have a morning-briefing command (e.g. `/gm`), the trigger simply runs it and posts the output.

### 2. Midday Triage (~12pm)

**Purpose:** a quick mid-day sweep so urgent items from the morning don't sit unseen.

**What it does:**
- Triages only what arrived since the morning brief.
- Flags urgent or high-priority items that need a same-day response.
- Posts a short triage list to `{{COS_SLACK_CHANNEL}}`. Keep it tight - this is a check-in, not a full inbox review.

If you have a triage command (e.g. `/triage`), run it scoped to the window since the morning run.

### 3. Evening Triage / Wrap (~4-5pm)

**Purpose:** close the day cleanly and set up tomorrow.

**What it does:**
- Surfaces tasks that are slipping or still open.
- Catches anything that came in during the afternoon and needs a reply before end of day.
- Sets up tomorrow: tomorrow's first meeting, anything due, one or two suggested priorities.
- Posts the wrap to `{{COS_SLACK_CHANNEL}}`.

### 4. Market Pulse (optional, a few times a week, off-hours)

**Purpose:** keep a current read on competitors and market shifts so your prioritization carries a live Strategic Fit signal, without you running scans by hand.

**What it does:**
- Runs a competitive + market scan. If you use the product track, this is `/roadmap market-scan`; otherwise an inline web-research sweep over your 1-2 named competitors and your category.
- Appends findings to your market-pulse doc and feeds the `Strategic Fit` lens in the `work-tracker` prioritization (see `skills/work-tracker/references/market-pulse.md`).
- Posts a short "what moved" summary to `{{COS_SLACK_CHANNEL}}`.

Run it off-hours (e.g. pre-dawn) on Mon/Wed/Fri, not daily. Markets don't move fast enough to warrant a daily scan, and the off-hours timing keeps it out of your way. Skip this trigger entirely if you don't track competitors.

---

## How to set it up

### Step 1 - Create the Slack destination

Create a private channel (`{{COS_SLACK_CHANNEL}}`) or decide to use your self-DM (`{{SLACK_USER_ID}}`). Make sure the agent's Slack connection can post there.

### Step 2 - Write each trigger's prompt

A scheduled run starts cold: **no chat history, no memory of prior runs.** The prompt must therefore be fully self-contained. A good trigger prompt includes:

- **The task.** "Run the morning brief," or the inline steps if you don't have a command.
- **The time window.** "Cover everything since 6pm yesterday," "since the midday run," etc.
- **The destination.** "Post the result to `{{COS_SLACK_CHANNEL}}`."
- **Filtering rules.** What to ignore so the digest stays signal-rich (see below).
- **The guardrail.** "Post to my CoS channel only. Do not send messages to anyone else."

Example self-contained prompt for the Morning Brief:

```
You are my Chief of Staff running the morning brief.

Window: 6:00pm yesterday -> now, in {{TIMEZONE}}.

1. Review new email from real people (apply the filter rules below).
2. Review today's calendar and anything due today.
3. Flag what's time-sensitive or at risk.

Post one concise digest to {{COS_SLACK_CHANNEL}}.

Do NOT send any message to anyone other than this CoS channel.
```

Midday and evening prompts follow the same shape with a different window and task.

### Step 3 - Schedule the prompts

Use whatever cron-style scheduler your setup provides (a scheduled-agents feature, a hosted cron runner, or a local `cron`/`launchd` job that invokes the agent). Each entry maps one cron expression to one trigger prompt.

**Cron expressions** are easiest to reason about if you write them in UTC and translate from your local time. Examples for `America/New_York` during EDT (UTC-4):

| Trigger        | Local time        | Cron (UTC)     |
|----------------|-------------------|----------------|
| Morning Brief  | ~7:00am ET daily  | `0 11 * * *`   |
| Midday Triage  | ~12:00pm ET daily | `0 16 * * *`   |
| Evening Wrap   | ~4:30pm ET daily  | `30 20 * * *`  |
| Market Pulse   | ~3:15am ET M/W/F  | `15 7 * * 1,3,5` |

Adjust the hour offset for your own timezone. If your scheduler accepts a timezone directly, set it to `{{TIMEZONE}}` and skip the UTC math.

### Step 4 - Confirm and iterate

Run each trigger once manually to confirm it posts to the right place and reads the right window. Then let the schedule take over. Tune the windows and filters over the first week.

---

## Filtering rules (keep digests signal-rich)

A morning brief that lists every newsletter is useless. Encode exclusions in each prompt. Typical excludes:

- Automated senders: `no-reply@*`, `noreply@*`, `notifications@*`.
- Tool notifications: project-tracker, calendar, code-host, and meeting-notes notification addresses.
- Social and marketing mail, and anything carrying a `List-Unsubscribe` header.

Keep email from real colleagues, customers, and stakeholders. The goal is a digest you can act on in under a minute.

---

## Message-sending guardrail

This is the most important rule in the pattern.

- **Posting to your own CoS channel or self-DM is allowed.** These posts are *status and briefings* - notes from your assistant to you. They are not outbound communication.
- **Sending a message to any other person always requires explicit approval.** A scheduled agent must never email, DM, or message a colleague, customer, or anyone else on its own. If a trigger surfaces something that warrants an outbound reply, it should *draft* it and flag it for you - never send it.

This mirrors the global rule: *never send any message to others without explicit approval* (show draft -> wait for "Send" / "Y" -> only then send). Scheduled runs are unattended, so they cannot satisfy that approval step and therefore must not send to others under any circumstance.

When in doubt, a scheduled agent posts to `{{COS_SLACK_CHANNEL}}` and stops.

---

## Slack formatting (so posts stay scannable)

Slack uses mrkdwn, not full Markdown:

- **Bold:** `*bold*` (single asterisks)
- **Italic:** `_italic_`
- **Inline code:** `` `code` ``
- **Block quote:** start the line with `>`
- **Bullets:** lead with the bullet character, not `- `
- **Links:** `<https://url|display text>`
- Do **not** use `#`/`##` headers - Slack renders the hash literally.

A single lead emoji per message makes the feed easy to scan. One convention:

- 🌅 Morning brief
- ☀️ Midday triage
- 🌙 Evening wrap
- ⏰ Deadline nudge
- 🚨 At-risk / escalated
- 📈 Market pulse

One lead emoji per message. No emoji confetti.

**Front-load the preview.** Slack shows the first ~100 characters as the notification. Put the most important fact first:

- Good: `🌅 *3 things today* - 1:1 at 3pm, board doc due, 2 replies waiting`
- Bad: `Here's your morning briefing for today...`

---

## Failure modes to avoid

- **Don't double-post.** If a run already posted for a given window, don't repeat it unless meaningful new info appeared.
- **Don't invent a destination.** If `{{COS_SLACK_CHANNEL}}` / `{{SLACK_USER_ID}}` can't be resolved, log the failure and skip the send rather than posting somewhere random.
- **Don't send unprovable claims as fact.** "Looks like X shipped" is fine; "X shipped" when unsure is not.
- **Don't exceed one message per moment.** If a brief, a nudge, and a focus rec all apply, send the single most useful one.
- **Never send to others.** Re-read the guardrail above.

---

## Timezone & DST

Cron expressions written in UTC do not shift when your local clock changes for daylight saving. If you schedule in UTC, re-adjust the hour offsets when your region flips between standard and daylight time. If your scheduler supports a named timezone, set it to `{{TIMEZONE}}` and let it handle DST for you.
