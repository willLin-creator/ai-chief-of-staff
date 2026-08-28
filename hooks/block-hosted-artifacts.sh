#!/bin/bash
# PreToolUse(Artifact): deliverables are LOCAL files you own, never pages hosted on a
# third-party service. Blocks the actions that CREATE or FEED a hosted page (publish, which
# is the default when no action is given, and upload_asset). Leaves the read/manage actions
# alone (list, comments, reply, resolve, read_asset, list_assets, delete_asset) so anything
# published earlier can still be found, answered, and cleaned up.
#
# Why: a hosted artifact is a send. It leaves your machine, it may be cached or indexed, and
# it is not in your repo or your notes. Write the deliverable to a local file (Markdown, or
# .html for a browsable page) and hand over the path instead.
#
# Override for one call: ALLOW_HOSTED_ARTIFACT=1
[ "$ALLOW_HOSTED_ARTIFACT" = "1" ] && exit 0
input=$(cat)
action=$(printf '%s' "$input" | jq -r '.tool_input.action // "publish"')
case "$action" in
  publish|upload_asset)
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Blocked: deliverables are local files, never hosted artifacts. Write the deliverable to a local file and give the user the path. For a browsable page, write .html locally and open it. Override for one call: ALLOW_HOSTED_ARTIFACT=1."}}\n'
    ;;
esac
exit 0
