#!/bin/bash
# PreToolUse(Bash): backstop for two git rules across ALL repos.
#  - No AI attribution in commit messages or PR bodies. Primary enforcement is the native
#    Claude Code setting  "attribution": {"commit": "", "pr": ""}  in settings.json; this
#    catches a manually typed trailer.
#  - Never push to main/master. Push a feature branch and open a PR. (Commit-on-main stays
#    a pinned habit: a global hook cannot reliably know the branch of an arbitrary compound
#    command.)
#
# Override for one command: prefix it with  GIT_GUARD_OVERRIDE=1
# (a legitimate case is a fast-forward merge you are doing on purpose after a PR review).
input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')
printf '%s' "$cmd" | grep -q 'GIT_GUARD_OVERRIDE=1' && exit 0
printf '%s' "$cmd" | grep -Eq 'git([[:space:]]+-C[[:space:]]+[^[:space:]]+)?[[:space:]]+(commit|push)' || exit 0

deny() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$1"
  exit 0
}

if printf '%s' "$cmd" | grep -Eqi 'Co-Authored-By:[[:space:]]*Claude|Generated with[[:space:]]+Claude|Claude Code'; then
  deny "Remove AI attribution from the commit/PR (no Co-Authored-By: Claude, no Generated-with-Claude). Override for one command: GIT_GUARD_OVERRIDE=1."
fi
if printf '%s' "$cmd" | grep -Eq 'push([[:space:]]+[^[:space:]]+)*[[:space:]]+(main|master)([[:space:]]|$)'; then
  deny "Never push to main/master. Push a feature branch and open a PR. Override for one command: GIT_GUARD_OVERRIDE=1."
fi
exit 0
