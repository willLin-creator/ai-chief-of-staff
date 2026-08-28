#!/bin/bash
# Stop: while demo mode is active, backstop-scan the final response against the
# sensitive-pattern list and force a sanitized rewrite on a hit. The register instruction
# (demo-mode-context.sh) does the thinking; this catches slips.
# Fails OPEN: missing flag, missing patterns file, or missing transcript means no-op.
#
# Patterns file: $COS_HOME/demo-mode-patterns.txt, one extended regex per line,
# case-insensitive, '#' comments allowed. Start from demo-mode-patterns.example.txt.
COS_HOME="${COS_HOME:-$HOME/.claude}"
FLAG="$COS_HOME/demo-mode.json"
PATTERNS="$COS_HOME/demo-mode-patterns.txt"
[ -f "$FLAG" ] || exit 0
[ "$(jq -r '.active // false' "$FLAG" 2>/dev/null)" = "true" ] || exit 0
[ -f "$PATTERNS" ] || exit 0

input=$(cat)
[ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ] && exit 0
tp=$(printf '%s' "$input" | jq -r '.transcript_path // ""')
{ [ -z "$tp" ] || [ ! -f "$tp" ]; } && exit 0

last=$(tail -n 80 "$tp" | jq -rs '
  map(select(.type=="assistant")) | last // {} | .message.content // [] |
  if type=="array" then (map(select(.type=="text") | .text) | join("\n")) else (.|tostring) end
' 2>/dev/null)
[ -z "$last" ] && exit 0

hit=$(printf '%s' "$last" | grep -iEof <(grep -vE '^\s*(#|$)' "$PATTERNS") 2>/dev/null | head -3 | tr '\n' ', ')
if [ -n "$hit" ]; then
  jq -cn --arg hit "$hit" '{decision:"block", reason:("DEMO MODE is active and your response contains sensitive-register terms (" + $hit + "). Rewrite it sanitized: professional and general info only; drop intimate personal detail, confidential business matters, real titles, customers, and IDs. See skills/demo-mode/SKILL.md.")}'
fi
exit 0
