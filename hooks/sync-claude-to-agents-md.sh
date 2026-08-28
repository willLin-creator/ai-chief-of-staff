#!/bin/bash
# PostToolUse(Edit|Write): when CLAUDE.md changes, remind the agent to re-adapt the mirror
# that a second agent runtime reads (for example ~/.codex/AGENTS.md for Codex, or any
# AGENTS.md-style file). The mirror is a HAND-ADAPTED version (different tool surface,
# read-order pointing back at the primary config), NOT a verbatim copy, so this NUDGES
# rather than clobbering.
#
# Skip this hook entirely if you run one agent runtime.
# Config: COS_HOME (default ~/.claude), AGENTS_MD_PATH (default ~/.codex/AGENTS.md).
COS_HOME="${COS_HOME:-$HOME/.claude}"
AGENTS_MD_PATH="${AGENTS_MD_PATH:-$HOME/.codex/AGENTS.md}"
input=$(cat)
f=$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_response.filePath // ""')
case "$f" in
  "$COS_HOME/CLAUDE.md")
    jq -cn --arg p "$AGENTS_MD_PATH" '{systemMessage:("CLAUDE.md changed -> review " + $p + " and re-adapt it if the operating substance changed. It is an adapted mirror, not a copy, so do NOT blind-copy CLAUDE.md over it.")}' ;;
esac
exit 0
