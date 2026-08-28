#!/bin/bash
# DELIBERATELY NOT REGISTERED in hooks/settings.example.json.
#
# This is the Stop-hook version of the no-dashes rule: it scans the assistant's final
# response in every turn and forces a rewrite on a hit. It was the first implementation
# and it was retired for a reason worth keeping on file: enforcement for a voice rule
# belongs on content that LEAVES for someone else (PreToolUse on send/publish tools), not
# on conversational replies to you. Policing chat produced constant friction and caught
# nothing a reader would ever see. See hooks/no-dashes-outbound.sh for the live version.
#
# Kept as a worked example of a Stop hook that reads the transcript, in case you want the
# pattern for a different rule. Fails OPEN: any parse problem means no block.
input=$(cat)
[ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ] && exit 0
tp=$(printf '%s' "$input" | jq -r '.transcript_path // ""')
{ [ -z "$tp" ] || [ ! -f "$tp" ]; } && exit 0

last=$(tail -n 80 "$tp" | jq -rs '
  map(select(.type=="assistant")) | last // {} | .message.content //  [] |
  if type=="array" then (map(select(.type=="text") | .text) | join("\n")) else (.|tostring) end
' 2>/dev/null)
[ -z "$last" ] && exit 0

if printf '%s' "$last" | LC_ALL=en_US.UTF-8 grep -qE '—|–| -- '; then
  printf '{"decision":"block","reason":"Your last response used a dash connector (em dash, en dash, or \\" -- \\"). Rewrite it without dashes: use a period, comma, colon, parentheses, or split into two sentences. Compound hyphens are fine."}\n'
fi
exit 0
