# hooks/

The enforcement layer. Everything else in this repo is instruction; a hook is a mechanism.
The difference matters because instructions get skipped under load and a mechanism does not.

## Why a hook, and when

Every rule the assistant follows sits in one of three tiers:

| Tier | Where it lives | When it fires | Use it for |
|---|---|---|---|
| **hook** | a script here, wired in `settings.json` | mechanically, every time, before or after a tool call | rules that can be matched by a pattern and that you never want to argue about again |
| **pinned** | an always-loaded block of `CLAUDE.md` or `MEMORY.md` | every session, by being in context | judgment rules that cannot be mechanized but must never be forgotten |
| **recall** | a memory file's `description:` | when a task makes it relevant | everything else |

A rule earns a hook by recurring. The write path is `lessons.md` (CLAUDE.md Part 9): log the
correction, count it, and when the same correction lands for the third time, ask whether a pattern
can catch it. If yes, write a hook. If no, pin it and sharpen the phrasing. The companion repo
[agent-eval-loop](https://github.com/willLin-creator/agent-eval-loop) turns that count into a number
per rule and recommends promotions and relaxations in both directions; a hook that keeps leaking
corrections is a hook with a gap, and it will tell you so.

## Design rules every hook here follows

1. **Fail open.** A hook that cannot parse its input exits 0 and does nothing. A broken hook must
   never block work.
2. **Outbound, not conversational.** Voice rules fire on content that leaves for someone else
   (send, publish, ticket, doc), never on the assistant's replies to you. The Stop-hook version of
   the dash rule was tried, nagged constantly, and was retired; it is kept as
   `no-dashes-stop.sh` for reference and is not wired.
3. **High precision over recall.** A closed list of phrases that are only ever wrong beats a broad
   regex that sometimes is. The judgment half of a rule stays pinned in `CLAUDE.md`.
4. **One override each, named in the deny message.** Every blocking hook can be bypassed for one
   call with an environment variable, so a legitimate exception never requires editing the hook.
5. **Say why, and what to do instead.** The deny reason is the fix, not just the verdict.

## What ships

| Hook | Event | What it does | Override |
|---|---|---|---|
| `no-dashes-outbound.sh` | PreToolUse: Bash (gdocs.py only) + outbound MCP tools | blocks em dash, en dash, and ` -- ` as connectors in content leaving for someone else | rewrite |
| `no-praise-outbound.sh` | same surfaces | blocks praise aimed at the reader's input ("great question", "you're absolutely right"); warmth aimed at the person passes | rewrite |
| `block-git-attribution-and-main.sh` | PreToolUse: Bash | blocks AI attribution trailers in commits and any push to `main`/`master` | `GIT_GUARD_OVERRIDE=1` |
| `block-hosted-artifacts.sh` | PreToolUse: Artifact | blocks publishing deliverables to a hosted page; local files only | `ALLOW_HOSTED_ARTIFACT=1` |
| `gap-claim-requires-grep.sh` | PreToolUse: Write, Edit | warns (never blocks) when written content asserts a gap ("does not exist", "unowned") so the local stores get searched first | n/a |
| `demo-mode-context.sh` | UserPromptSubmit | while `demo-mode.json` is active, injects the sanitized register into every turn of every session | delete the flag |
| `demo-register-stop.sh` | Stop | while demo mode is active, scans the final response against `demo-mode-patterns.txt` and forces a rewrite on a hit | delete the flag |
| `sync-claude-to-agents-md.sh` | PostToolUse: Edit, Write | when `CLAUDE.md` changes, nudges to re-adapt the mirror a second runtime reads (e.g. `~/.codex/AGENTS.md`) | skip if you run one runtime |
| `no-dashes-stop.sh` | (not wired) | the retired Stop-hook variant, kept as a worked example | |

Two more hooks are one-liners in `settings.example.json` rather than scripts: a PostToolUse guard
that runs `scripts/validate_tasks.py` whenever `my-tasks.yaml` is written (duplicate IDs, required
fields, the daily intake cap), and SessionStart checks that report today's task intake and whether
`lessons.md` has grown past the size anyone will actually read.

## Wire it

Merge `settings.example.json` into `~/.claude/settings.json`. The paths assume `hooks/` and
`scripts/` are symlinked into `~/.claude/` (see `docs/SETUP.md`):

```bash
ln -s "$PWD/hooks"   ~/.claude/hooks
ln -s "$PWD/scripts" ~/.claude/scripts    # or symlink the individual scripts you want
chmod +x hooks/*.sh
```

Hooks need `jq` and `python3`. The `attribution` key in the example is the native setting that
strips AI attribution from commits and PRs; the git hook is the backstop for a hand-typed trailer.

Set `COS_HOME` if your config directory is not `~/.claude`. The demo-mode and gap-claim hooks read
it; the rest do not need it.

## Test it

```bash
bash hooks/test-hooks.sh
```

Feeds each hook the JSON Claude Code would send and asserts on the decision: every banned form
denies, every allowed form passes, every override works, malformed input is ignored. Run it after
editing any hook. If you add a hook, add its cases here in the same commit.

## What was deliberately not shipped

The private version of this layer also carries hooks that are specific to one company's tooling:
a write-lock on the production monorepo, a draft-prefix rule for its issue tracker, a guard against
machine-local paths in tickets. They are the same shape as the ones here (PreToolUse, fail open,
one override, a deny message that says what to do). Write yours the same way, and add them to
`test-hooks.sh`.
