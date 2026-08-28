---
name: demo-mode
description: Presentation-safe register for the whole system. Trigger when the user says anything like "I'm demoing this", "I'm demoing this for <audience>", "I'm about to present / screen-share", "demo mode on", or when they say the demo is over ("demo mode off", "demo's done"). While active, every session sanitizes what it surfaces. General and professional information is fine; intimate or confidential detail is withheld.
---

# /demo-mode: presentation-safe register

## What this is

When you demo or screen-share the system, the system itself must know to speak in a sanitized
register. You should not have to remember what is safe. You say "I'm demoing this for Acme" once,
and everything after that is presentation-safe until you say the demo is over.

## Mechanics

State lives in a flag file, `$COS_HOME/demo-mode.json` (default `~/.claude/demo-mode.json`):

```json
{"active": true, "audience": "Acme", "since": "<ISO timestamp>"}
```

- **Turn ON** (any demo declaration): write the flag file with the audience if one was named.
  Confirm in one line: "Demo register on (audience: Acme). Intimate and confidential detail is
  suppressed until you tell me the demo is over."
- **Turn OFF** ("demo's over", "demo mode off"): delete the flag file. Confirm in one line.
- **Status** ("am I in demo mode?"): read the flag file and say.

Two hooks make this system-wide rather than session-local (wired in `hooks/settings.example.json`):

- `hooks/demo-mode-context.sh` (UserPromptSubmit): injects the active register into every turn of
  every session while the flag exists.
- `hooks/demo-register-stop.sh` (Stop): backstop scan of each final response against
  `$COS_HOME/demo-mode-patterns.txt`; blocks and forces a rewrite on a hit. Start the patterns
  file from `skills/demo-mode/demo-mode-patterns.example.txt`.

## The register (what changes while active)

Allowed, unchanged:

- General and professional information about people: role, company, public context, what they
  care about professionally. ("Jane Doe, VP Operations at Acme, oversees field teams" is fine.)
- Everything about how the system works: categories, flows, structure.
- Sanitized assets (placeholder names, fictional examples).

Withheld (do not surface, even if asked directly on screen):

- Intimate or personal detail about anyone: relationship notes, family, health, personal history,
  how you really read them. That intel exists for private prep sessions, not for an audience.
- Confidential business matters: fundraising, M&A, personnel changes, compensation, legal, org
  changes, your own career moves.
- Real memory titles, real customer names and specifics, internal ticket IDs, private script and
  tool names.
- Contact file contents beyond the professional summary. Anything under a `## Private` heading in
  `contacts/*.md` is never surfaced in demo register, and intimate detail is withheld even when
  unmarked. Default-deny.

When the register materially limits an answer, say so briefly ("holding the rest for a private
session") rather than pretending the information does not exist. You may be narrating; the system
should give you a clean line, not a refusal.

## Example

You, mid-demo: "What do we know about Jane?"

- Demo register: "Jane Doe, VP Operations at Acme. She runs the field teams and came in through
  the partnerships thread; she picked Monday for this call. Full brief is in your contact notes."
- NOT in demo register: negotiation reads, personal rapport notes, anything you would only say
  with the door closed.

## Notes

- Keep the flag file format stable. Other tools (a dashboard, a status bar) can read the same file
  to show a DEMO badge.
- Add terms to the patterns file before a sensitive demo rather than trusting recall. Keep
  patterns narrow: a false block mid-demo is worse than a near miss, because the register
  instruction is the primary control and the scan is only the backstop.
- Fail-open philosophy: the hooks never block when the flag is absent.
