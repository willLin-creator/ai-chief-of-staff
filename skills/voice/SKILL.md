---
name: voice
description: Capture and apply the user's writing voice so every drafted email, Slack message, or document sounds like them, not like an AI. Run setup once to build a voice profile from real samples (a Slack thread, recent sent emails, or pasted examples); thereafter every deliverable matches it. Refresh occasionally.
---

# Voice — Sound Like You, Not Like an AI

The fastest way to break trust in an assistant is a draft that doesn't sound like the
person. This skill captures the user's real writing voice and applies it to every
deliverable. It has two modes: **setup** (build the profile) and **apply** (use it).

---

## Setup — build the voice profile

Run this once during onboarding, and refresh every month or two. Gather real samples
using any or all of these sources. **Real samples beat any description** — get them first.

1. **From Slack** — read a recent thread or the user's own messages in a channel/DM.
   Look at how they actually write to peers vs. leadership.
2. **From email** — pull the user's recent **sent** replies (not received mail). Sent
   mail is the ground truth of their voice. 5-10 is plenty.
3. **From pasted samples** — if you can't reach their channels, ask the user to paste
   2-3 short, representative messages: one casual, one professional, one handling a
   hard or sensitive thing. Short is fine; even a few lines reveal a lot.

If samples are thin, ask a few quick calibration questions:
- Sign-off style by channel? Contractions (I'm, we'd)? Em dashes, or avoid them?
- Emoji — yes/no/sometimes? How does formality change by audience (exec vs peer vs customer)?

### Extract these dimensions

- **Tone** (warm / direct / formal / playful) and how it shifts by audience
- **Sentence and paragraph length** (short and punchy? long and considered?)
- **Contractions and punctuation quirks** (dashes, exclamation points, ellipses, lowercase)
- **Openers and sign-offs**, separately for email vs. Slack
- **Structure habits** (bullets vs. prose; do they lead with the ask?)
- **Signature words/phrases** they reach for, and ones they never use

### Write the profile

Save to `voice-profile.md` (gitignored — it's personal). Use `voice-profile.example.md`
as the template. It must include:

- A **characteristics** list (the dimensions above)
- **Channel-specific rules** (email vs. Slack)
- **2-3 verbatim gold-standard samples** — the examples to imitate
- A **"never do"** list (e.g. "never put scheduling burden on the recipient", "no em dashes")

Then make sure the main context file (`CLAUDE.md` Part 4) points to `voice-profile.md`
so it loads before any drafting.

---

## Apply — every deliverable

Before producing any email, Slack message, or document:

1. Load `voice-profile.md`.
2. Draft in that voice — match cadence, structure, and the right sign-off for the channel.
3. Self-check against the "never do" list before presenting.
4. **Never send without explicit approval** (per `CLAUDE.md`). Show the draft, wait for "Send."

If the user says "that doesn't sound like me," treat it as a signal to refresh the
profile, and log the correction to `lessons.md`.

---

## Refresh

Voice drifts and context changes. Re-run setup on recent sent messages every month or
two, or whenever a draft misses. Update `voice-profile.md` in place.

## Guardrail

The profile governs **style, not substance**. Matching someone's voice never means
inventing claims, commitments, or facts they didn't make. Style yes; content always true.
