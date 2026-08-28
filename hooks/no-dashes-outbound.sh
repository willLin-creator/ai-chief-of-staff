#!/bin/bash
# PreToolUse: block dash connectors in prose that leaves for someone else: outbound
# messages (email, Slack) and docs (issue tracker, wiki, Google Docs via scripts/gdocs.py).
#
# Scope is OUTBOUND ONLY. This never fires on conversational replies to you; it fires on
# content being SENT or WRITTEN outward. (A Stop-hook variant that policed every chat reply
# was tried and retired: it nagged constantly and caught nothing that mattered. It is kept
# as hooks/no-dashes-stop.sh for reference, deliberately unregistered.)
#
# Flags ONLY the three unambiguous banned forms: em dash, en dash, and " -- " joining
# clauses. Never plain hyphens (compound hyphens like "AI-native" are allowed). Excludes
# code and mockups by design, since dashes are legitimate in CSS/HTML/SQL.
#
# Fails OPEN: if it cannot read or parse the input it does nothing, so it never blocks
# work erroneously.
#
# Wire it: see hooks/settings.example.json (Bash matcher + the outbound MCP matcher).
input=$(cat)
tool=$(printf '%s' "$input" | jq -r '.tool_name // ""' 2>/dev/null)

if [ "$tool" = "Bash" ]; then
  # Best-effort: only guard Google Docs WRITES via the gdocs.py helper (the command line can
  # carry a title or inline text). A command that merely mentions gdocs.py, such as a heredoc
  # writing a doc that documents the helper, is not outbound and must not trip this.
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

if printf '%s' "$content" | LC_ALL=en_US.UTF-8 grep -qE '—|–| -- '; then
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"This outbound content uses a dash connector (em dash, en dash, or \\" -- \\"). Rewrite it without dashes before sending: use a period, comma, colon, parentheses, or split into two sentences. Compound hyphens are fine. (CLAUDE.md Part 4)"}}\n'
fi
exit 0
