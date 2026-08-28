# /capture — Second-Brain Capture

## Description

Turn any external source (a post or article, a web page, a PDF, or a raw idea) into a durable,
connected note in your second brain. One command runs the full loop: **fetch full text →
(optionally) research the topic → synthesize against your themes → cross-link into the memory
graph → confirm → save.**

This is the ingest path that sits in front of `learnings/` and the memory graph. It exists so
"read this and add it to my brain" happens the same way every time instead of ad hoc.

Plain-language orchestration: paste a URL, or a URL plus what you want. The skill picks the fetch
method and the output type automatically, and always shows the draft before writing.

## The second-brain model (what this feeds)

Three layers already exist (see `skills/second-brain/SKILL.md`); `/capture` writes to the first two:

- **`learnings/<YYYY-MM-DD>-<slug>.md`** — digested synthesis notes (the slow brain). Default output.
- **Memory graph** — `MEMORY.md` index + `memory/*.md` nodes with `[[wiki-links]]` (fast recall). A
  capture always either links into it (synthesis) or adds a one-liner to it (bookmark).
- **Insights / ideas / tasks** — if a source is really a *product* signal, route it, don't just file
  it (see Routing).

## Usage

```
/capture <url-or-source> [what you want]
```

Examples that all work:
- `/capture https://example.com/post` — fetch, synthesize, file
- `/capture <url> look into this topic first` — research the topic (web + memory) before synthesizing
- `/capture <url> as reference` — pure bookmark: one-line `reference_*` memory, no synthesis note
- `/capture <local.pdf> — the agents paper`
- `/capture this thread + my notes: ...` — mix a source with your own take

## Step 1 — Fetch full text (never synthesize a preview)

Route by source. Always get the COMPLETE text before writing anything.

| Source | Method |
|---|---|
| Web article, blog post | `WebFetch` first. If it 401/402s or returns a login or paywall shell, fall back to a headless browser (navigate, then read `document.querySelector('article')?.innerText || document.body.innerText`). |
| Social post or thread (X, LinkedIn) | Same as above; these often need the browser path. If you keep a reader script for the platform, use it. Threads: fetch every post, not the first. |
| PDF | `Read` the file. |
| Google Doc | the Docs helper in `scripts/` (`read --doc-id <id>`). |
| Raw idea, no source | Skip fetch; your text IS the source (`source.type: own_thought`). |

If a fetch is blocked and no fallback works, say so plainly and ask for the text to be pasted. Do not
synthesize from a title plus a preview.

## Step 2 — (Optional) Look into the topic

Trigger when the user says "look into", "research", "go deeper", or the source is a pointer rather
than the substance. Otherwise skip.

1. `WebSearch` for prior art, the primary source behind the post, and 1-2 credible counterpoints.
2. Grep `learnings/` and the memory graph for what you already know on this topic, so the note
   *extends* rather than repeats.
3. Keep it tight: enough grounding to synthesize well, not a full research report. If it clearly
   warrants that depth, offer a deeper research pass as a separate step.

## Step 3 — Synthesize (the default output)

Write a dated learnings note: `learnings/<YYYY-MM-DD>-<slug>.md`.

Structure:
1. **Header** — title, date (today, absolute), source URL(s), one line on *why filed*.
2. **Faithful capture** — the source's actual argument or content, enough that the note stands alone
   without re-fetching. Use tables for taxonomies and frameworks.
3. **Why this matters to your work** — the synthesis. Map claims onto active projects and themes and
   **cross-link every connection with `[[memory-node-name]]`**. This is the leverage; a note that
   does not connect to existing work is a bookmark, not a synthesis.
4. **One-line takeaway** — the compressed insight.

Voice: your own (CLAUDE.md Part 4). This is an internal artifact, but keep the voice.

## Step 4 — Wire into the memory graph

- If the note earns durable recall, add a one-line pointer to `MEMORY.md` under the right section
  and, when warranted, a small `memory/*.md` node.
- **When you extended an existing note instead of creating one (Guardrail 5), reconcile its index
  entry.** This is the one drift a structural auditor cannot catch: a healthy note whose content
  outgrew its description is never flagged, so it is never re-judged. Capture time is the only
  reliable place to catch it, because capture is the moment the drift is created. Check the note's
  `MEMORY.md` line (or the hub node that points to it): does that description still cover what the
  note now says? If your addendum added a *distinct new thread* the index does not advertise, propose
  one of (a) broaden the existing description, (b) add a dedicated pointer for the new thread, or (c)
  if the index is at budget, broaden the hub node's description instead of adding a line. Fold the
  proposal into the Step 5 confirm; never silently leave a note mis-described by its index.
- `[[links]]` to nodes that do not exist yet are fine; they mark future captures.
- For `as reference` mode: skip the learnings note entirely; write a one-line `reference_*` (or
  `project_*`) memory plus a `MEMORY.md` pointer. That is the whole output.

## Step 5 — Confirm before saving

Always show the drafted note (or reference line) and wait for approval before writing to disk. This
is a save, not a send, so no "Send" gate, but never write silently.

## Routing — when a capture is really something else

A capture that is actually a product signal should ALSO be routed, and the note should say so:

| If the source is... | Route to |
|---|---|
| A feature or product idea for your product | `/idea add ...` (then this note becomes its `source.reference`) |
| Customer feedback or a pain signal | `/insights add ...` |
| An actionable to-do | `/my-tasks` |
| A deep multi-source question | offer a deeper research pass |

Filing to learnings and routing are not exclusive. Capture the thinking; route the action.

## Guardrails

1. **Full text or nothing.** Never synthesize from a preview or snippet. Fetch or ask.
2. **Synthesis must connect.** At least one `[[link]]` to existing work, or it is a bookmark (use
   `as reference`).
3. **Confirm before disk write.** Always show the draft.
4. **Cite the source.** Every note carries its URL(s) and author.
5. **Don't duplicate.** Grep `learnings/` first; if a note already covers the topic, extend it instead
   of creating a near-duplicate.
6. **Absolute dates.** Convert "today" and "this week" to ISO dates.
7. **Extending a note means reconciling its index.** A capture that adds a new thread to an existing
   note must verify the note's index entry still describes it, and propose a fix if not. This is the
   capture-time half of consolidation (the `consolidate` skill in
   [agent-memory-vault](https://github.com/willLin-creator/agent-memory-vault) is the periodic half):
   the deterministic auditor is blind to description drift on an otherwise healthy note, so if
   capture does not catch it, nothing will.

## What this skill does NOT do

- It does NOT auto-post anywhere (no send gate needed; it only writes local files).
- It does NOT replace `/idea` or `/insights`; it feeds them when a capture is a product signal.
- It does NOT hoard. A pure link with no connection to your work is a one-line reference, not a
  learnings note.
