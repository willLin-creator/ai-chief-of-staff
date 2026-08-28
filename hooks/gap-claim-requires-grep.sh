#!/bin/bash
# PreToolUse(Write|Edit), NON-BLOCKING: warn whenever content being written asserts a GAP
# ("does not exist", "unowned", "nothing tracks this", "still open") so the agent confirms it
# actually searched the local stores before the claim lands in a durable file.
#
# Why this exists: "X is missing" is a claim about team state, and it is wrong surprisingly
# often. The idea is already in the ideas file, the task is already tracked, the decision is
# already in a learnings note. A transcript or an action item asserting a gap is not evidence
# of one. This hook does not know whether a grep ran; it fires on the vocabulary and puts the
# question in front of the agent at the moment it matters. It never blocks.
#
# Config: COS_HOME (default ~/.claude) is where goals, tasks, ideas, memory and learnings live;
#         COS_CODE_DIR (default ~/code) is where the repos live.
COS_HOME="${COS_HOME:-$HOME/.claude}"
COS_CODE_DIR="${COS_CODE_DIR:-$HOME/code}"
content=$(cat | python3 -c 'import json,sys; d=json.load(sys.stdin).get("tool_input",{}); print(d.get("content","")+d.get("new_string",""))' 2>/dev/null)
if printf '%s' "$content" | grep -qiE 'unowned|uncatalogued|uncataloged|does ?n.t exist|nothing exists|no one has|conflicting versions|unreconciled|still open|never been (owned|tracked)'; then
  echo "GAP CLAIM: this content asserts something is missing, unowned, or unresolved. Before it lands, confirm you grepped $COS_HOME (goals, my-tasks.yaml, product-ideas.yaml, memory/, learnings/) and $COS_CODE_DIR. A transcript or action item asserting a gap is not evidence of one." >&2
fi
exit 0
