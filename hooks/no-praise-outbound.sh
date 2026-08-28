#!/bin/bash
# PreToolUse: block PRAISE aimed at the reader's input in prose that leaves for someone
# else: outbound messages (email, Slack) and docs (issue tracker, wiki, Google Docs).
# Companion to no-dashes-outbound.sh: same surfaces, same fail-open posture.
#
# The distinction this enforces (CLAUDE.md Part 4, "Warmth stays, agreement goes"):
#   WARMTH is aimed at the PERSON  ("Thanks for sending!", a warm opener) -> KEEP, not matched.
#   PRAISE is aimed at their INPUT ("great question", "spot on")          -> DELETE, matched.
#
# Deliberately a CLOSED, high-precision list. It does NOT try to catch the judgment half of
# the rule (restating the ask back before answering it, generic affirmative openers); that
# stays as a pinned rule in CLAUDE.md because it is not reliably matchable.
# Bare "you're right" is ALLOWED on purpose: genuine concession in a real disagreement is
# not flattery. Only the intensified forms are blocked.
# Known false positive: quoting someone else's praise verbatim into a ticket. The deny
# message says what to do.
input=$(cat)
tool=$(printf '%s' "$input" | jq -r '.tool_name // ""' 2>/dev/null)

if [ "$tool" = "Bash" ]; then
  # Best-effort: only guard Google Docs WRITES via the gdocs.py helper (the command line can
  # carry a title or inline text). A command that merely mentions gdocs.py is not outbound and
  # must not trip this.
  cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')
  case "$cmd" in
    *gdocs.py*write*|*gdocs.py*create*) content="$cmd" ;;
    *) exit 0 ;;
  esac
else
  # Gather every prose string in the tool input and scan the lot.
  content=$(printf '%s' "$input" | jq -r '[.tool_input | .. | strings] | join("\n")' 2>/dev/null)
fi
[ -z "$content" ] && exit 0

# Each alternative is a phrase that only ever praises the reader's contribution.
PRAISE='(great|good|excellent|fantastic|terrific|wonderful) (question|point|call|catch|observation|insight)'
PRAISE="$PRAISE"'|(that.?s|this is) (a )?(really |very |such a )?(great|good|important|excellent|valid|fair) (point|question|observation|insight|call)'
PRAISE="$PRAISE"'|you.?re (absolutely|totally|completely|so|100%) right'
PRAISE="$PRAISE"'|you.?re on ?to something'
PRAISE="$PRAISE"'|(spot on|well said|nailed it|exactly right|couldn.?t agree more)'
PRAISE="$PRAISE"'|(makes total sense|totally makes sense)'
PRAISE="$PRAISE"'|as you (rightly|correctly) (point|pointed|note|noted|say|said)'
PRAISE="$PRAISE"'|i love (this|that|how you|the way you)'
PRAISE="$PRAISE"'|(it.?s|it is) worth noting'
PRAISE="$PRAISE"'|worth separating'

match=$(printf '%s' "$content" | LC_ALL=en_US.UTF-8 grep -ioE "$PRAISE" | head -1)

if [ -n "$match" ]; then
  esc=$(printf '%s' "$match" | sed 's/\\/\\\\/g; s/"/\\"/g')
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"This outbound content praises the reader'"'"'s input (\\"%s\\"). Warmth aimed at the person stays; praise aimed at what they said gets deleted. Cut the phrase and lead with the answer, or close with the next step, instead. Genuine concession in a real disagreement is fine, so plain \\"you'"'"'re right\\" is allowed. If this is quoted source text you need verbatim, tell the user and get an explicit go. (CLAUDE.md Part 4)"}}\n' "$esc"
fi
exit 0
