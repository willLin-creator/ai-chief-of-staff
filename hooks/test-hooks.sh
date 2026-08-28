#!/bin/bash
# Smoke tests for every hook in this directory. Feeds each script the JSON Claude Code would
# send and asserts on the decision. Run from anywhere:
#
#     bash hooks/test-hooks.sh
#
# Exit 0 when every case passes. Requires jq and python3 (the same as the hooks).
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
pass=0; fail=0
ERR="$TMP/err"   # stderr of the last hook run (a fixed path, since run() executes inside $(...))

# run <hook> <stdin-json>  -> stdout of the hook (stderr captured separately in $ERR)
run() { printf '%s' "$2" | bash "$HERE/$1" 2>"$ERR"; }
ok()   { pass=$((pass+1)); }
bad()  { fail=$((fail+1)); echo "FAIL: $1"; }
expect_deny()  { if printf '%s' "$2" | grep -q '"deny"'; then ok; else bad "$1 (expected deny, got: ${2:-<empty>})"; fi; }
expect_allow() { if [ -z "$2" ]; then ok; else bad "$1 (expected allow, got: $2)"; fi; }
expect_block() { if printf '%s' "$2" | grep -q '"block"'; then ok; else bad "$1 (expected block, got: ${2:-<empty>})"; fi; }

mcp() { jq -cn --arg t "$1" --arg body "$2" '{tool_name:$t, tool_input:{text:$body}}'; }
bash_cmd() { jq -cn --arg c "$1" '{tool_name:"Bash", tool_input:{command:$c}}'; }

# --- no-dashes-outbound -----------------------------------------------------------------
H=no-dashes-outbound.sh
expect_deny  "$H em dash"        "$(run $H "$(mcp mcp__slack_send_message 'Ships Monday — read it first.')")"
expect_deny  "$H en dash"        "$(run $H "$(mcp mcp__slack_send_message 'Ships Monday – read it first.')")"
expect_deny  "$H double hyphen"  "$(run $H "$(mcp mcp__slack_send_message 'Ships Monday -- read it first.')")"
expect_allow "$H compound"       "$(run $H "$(mcp mcp__slack_send_message 'An AI-native, warm-but-direct reply.')")"
expect_allow "$H bash non-gdocs" "$(run $H "$(bash_cmd 'echo "a — b"')")"
expect_deny  "$H bash gdocs"     "$(run $H "$(bash_cmd 'python3 scripts/gdocs.py write --doc-id X --file "a — b.md"')")"
expect_allow "$H bash gdocs read mention" "$(run $H "$(bash_cmd 'cat > doc.md <<EOF
use gdocs.py read --doc-id X — then edit
EOF')")"
expect_allow "$H malformed"      "$(run $H 'not json')"

# --- no-praise-outbound -----------------------------------------------------------------
H=no-praise-outbound.sh
expect_deny  "$H great question" "$(run $H "$(mcp mcp__gmail_send 'Great question. The answer is no.')")"
expect_deny  "$H absolutely"     "$(run $H "$(mcp mcp__gmail_send "You're absolutely right about the date.")")"
expect_deny  "$H worth noting"   "$(run $H "$(mcp mcp__gmail_send "It is worth noting the limit.")")"
expect_allow "$H warmth"         "$(run $H "$(mcp mcp__gmail_send 'Thanks for sending! The answer is no.')")"
expect_allow "$H bare concession" "$(run $H "$(mcp mcp__gmail_send "You're right, I had that backwards.")")"
expect_allow "$H bash non-gdocs" "$(run $H "$(bash_cmd 'echo "great question"')")"

# --- block-git-attribution-and-main -----------------------------------------------------
H=block-git-attribution-and-main.sh
expect_deny  "$H trailer"        "$(run $H "$(bash_cmd 'git commit -m "fix" -m "Co-Authored-By: Claude <x>"')")"
expect_deny  "$H push main"      "$(run $H "$(bash_cmd 'git push origin main')")"
expect_deny  "$H push master -C" "$(run $H "$(bash_cmd 'git -C /tmp/repo push -u origin master')")"
expect_allow "$H push branch"    "$(run $H "$(bash_cmd 'git push -u origin feature/x')")"
expect_allow "$H override"       "$(run $H "$(bash_cmd 'GIT_GUARD_OVERRIDE=1 git push origin main')")"
expect_allow "$H non-git"        "$(run $H "$(bash_cmd 'echo main')")"
expect_allow "$H branch named main-ish" "$(run $H "$(bash_cmd 'git push origin maintenance')")"

# --- block-hosted-artifacts -------------------------------------------------------------
H=block-hosted-artifacts.sh
expect_deny  "$H publish"        "$(run $H '{"tool_name":"Artifact","tool_input":{"action":"publish"}}')"
expect_deny  "$H default action" "$(run $H '{"tool_name":"Artifact","tool_input":{"file_path":"x.html"}}')"
expect_deny  "$H upload_asset"   "$(run $H '{"tool_name":"Artifact","tool_input":{"action":"upload_asset"}}')"
expect_allow "$H list"           "$(run $H '{"tool_name":"Artifact","tool_input":{"action":"list"}}')"
expect_allow "$H override"       "$(ALLOW_HOSTED_ARTIFACT=1 run $H '{"tool_name":"Artifact","tool_input":{"action":"publish"}}')"

# --- gap-claim-requires-grep (warn on stderr, never block) --------------------------------
H=gap-claim-requires-grep.sh
out=$(run $H '{"tool_name":"Write","tool_input":{"content":"The tracker does not exist for this."}}')
if [ -z "$out" ] && grep -q 'GAP CLAIM' "$ERR"; then ok; else bad "$H should warn on stderr and not block"; fi
out=$(run $H '{"tool_name":"Write","tool_input":{"content":"All good here."}}')
if [ -z "$out" ] && [ ! -s "$ERR" ]; then ok; else bad "$H should stay silent on neutral content"; fi

# --- demo mode (context + stop) -----------------------------------------------------------
export COS_HOME="$TMP/cos"; mkdir -p "$COS_HOME"
expect_allow "demo-mode-context no flag" "$(run demo-mode-context.sh '{"prompt":"hi"}')"
echo '{"active": true, "audience": "Acme"}' > "$COS_HOME/demo-mode.json"
out=$(run demo-mode-context.sh '{"prompt":"hi"}')
if printf '%s' "$out" | grep -q 'DEMO MODE ACTIVE (audience: Acme)'; then ok; else bad "demo-mode-context should inject the register"; fi
printf '# comment\nsecret-project\n' > "$COS_HOME/demo-mode-patterns.txt"
TR="$TMP/transcript.jsonl"
printf '%s\n' '{"type":"assistant","message":{"content":[{"type":"text","text":"Here is the Secret-Project status."}]}}' > "$TR"
expect_block "demo-register-stop hit" "$(run demo-register-stop.sh "$(jq -cn --arg p "$TR" '{transcript_path:$p}')")"
printf '%s\n' '{"type":"assistant","message":{"content":[{"type":"text","text":"Nothing sensitive here."}]}}' > "$TR"
expect_allow "demo-register-stop clean" "$(run demo-register-stop.sh "$(jq -cn --arg p "$TR" '{transcript_path:$p}')")"
expect_allow "demo-register-stop re-entry guard" "$(run demo-register-stop.sh "$(jq -cn --arg p "$TR" '{transcript_path:$p, stop_hook_active:true}')")"
rm -f "$COS_HOME/demo-mode.json"
expect_allow "demo-register-stop flag removed" "$(run demo-register-stop.sh "$(jq -cn --arg p "$TR" '{transcript_path:$p}')")"

# --- sync-claude-to-agents-md ---------------------------------------------------------------
out=$(run sync-claude-to-agents-md.sh "$(jq -cn --arg f "$COS_HOME/CLAUDE.md" '{tool_input:{file_path:$f}}')")
if printf '%s' "$out" | grep -q 'systemMessage'; then ok; else bad "sync-claude-to-agents-md should nudge on CLAUDE.md"; fi
expect_allow "sync-claude-to-agents-md other file" "$(run sync-claude-to-agents-md.sh "$(jq -cn --arg f "$COS_HOME/goals.yaml" '{tool_input:{file_path:$f}}')")"

# --- settings.example.json parses ---------------------------------------------------------
if jq -e '.hooks.PreToolUse | length > 0' "$HERE/settings.example.json" >/dev/null; then ok; else bad "settings.example.json is not valid JSON with hooks"; fi

echo "hooks: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
