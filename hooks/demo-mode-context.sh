#!/bin/bash
# UserPromptSubmit: while $COS_HOME/demo-mode.json exists and is active, inject the
# sanitized-register instruction into every turn of every session, so demo mode is
# system-wide state rather than something one session remembers.
# Pairs with skills/demo-mode/SKILL.md (which writes the flag) and demo-register-stop.sh
# (the backstop scan). Fails OPEN: any parse problem means no injection, never a block.
COS_HOME="${COS_HOME:-$HOME/.claude}"
FLAG="$COS_HOME/demo-mode.json"
[ -f "$FLAG" ] || exit 0
active=$(jq -r '.active // false' "$FLAG" 2>/dev/null)
[ "$active" = "true" ] || exit 0
audience=$(jq -r '.audience // "unspecified"' "$FLAG" 2>/dev/null)

ctx="DEMO MODE ACTIVE (audience: ${audience}). The user is presenting or screen-sharing. Sanitized register, per skills/demo-mode/SKILL.md: professional and general information about people is fine (role, company, public context); WITHHOLD intimate or personal detail (relationships, family, health, private reads on people), confidential business matters (fundraising, M&A, personnel, compensation, legal, the user's own career moves), real memory titles, real customer specifics, internal ticket IDs, and anything under a '## Private' heading in contact files. Default-deny when unsure. If the register limits an answer, say briefly that the rest is held for a private session. Demo mode ends only when the user says so (then delete $FLAG)."

jq -cn --arg ctx "$ctx" '{hookSpecificOutput:{hookEventName:"UserPromptSubmit",additionalContext:$ctx}}'
exit 0
