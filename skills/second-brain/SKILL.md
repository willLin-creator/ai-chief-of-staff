---
name: second-brain
description: The persistent, file-based memory layer that lets your Chief of Staff remember across sessions - atomic facts indexed by MEMORY.md, plus lessons, learnings, a meeting-notes context library, and session handoff. Use to understand how knowledge persists, how to save and recall it, and the discipline that keeps it useful.
---

# Second Brain — Persistent Memory

A chief of staff is only as good as what it remembers. This is the layer that turns
single sessions into a compounding body of knowledge: who you are, what you've
decided, what you've learned, and where you left off.

It is **plain files**, not a database. That's the point — it's portable, diffable,
greppable, and yours. Five layers:

| Layer | Location | Holds |
|---|---|---|
| **Memory** | `memory/` (+ `MEMORY.md` index) | Atomic, durable facts: who you are, your preferences, project context, references |
| **Lessons** | `lessons.md` | Corrections turned into rules, so the same mistake isn't repeated |
| **Learnings** | `learnings/` | Dated deep-dive docs when a single insight needs more than one line |
| **Context library** | `meeting-notes/` | Meeting summaries that compound (written by `/meeting`) |
| **Session handoff** | `CURRENT_TASK.md` | What's in flight + the specific next step, so any session can resume |

> In Claude Code, the `MEMORY.md` index is loaded into context at the start of each
> session, and relevant memories surface automatically as you work. The other layers
> are read on demand (e.g. `/gm` reads `lessons.md`; `/meeting` writes the context library).

---

## Memory: the core

One **fact per file**. Each file carries frontmatter so it can be recalled by relevance:

```markdown
---
name: <short-kebab-case-slug>
description: <one-line summary — used to decide relevance during recall>
metadata:
  type: user | feedback | project | reference
---

<the fact. For feedback/project, follow with **Why:** and **How to apply:** lines.
Link related memories with [[their-name]].>
```

**The four types:**

- **`user`** — who you are: role, expertise, durable preferences.
- **`feedback`** — guidance on how the assistant should work (corrections and confirmed approaches). Always include the *why*.
- **`project`** — ongoing work, goals, or constraints not derivable from the code/docs. Convert relative dates to absolute ("next Friday" → a date).
- **`reference`** — pointers to external resources (URLs, dashboards, docs, tickets).

Link liberally with `[[other-memory-name]]`. A link to a memory that doesn't exist
yet is fine — it marks something worth writing later.

## The index: MEMORY.md

`MEMORY.md` is a flat index — **one line per memory**, grouped by theme. It's the
table of contents that gets loaded each session. Never put memory *content* here;
just a pointer and a hook:

```markdown
## Writing & Voice
- [Prefers tight writing](EXAMPLE-prefers-tight-writing.md) — cut hedging, lead with the recommendation
```

After writing or updating a memory file, add or update its one-line pointer here.

---

## The discipline (what keeps it useful)

**Save when** something is durable and not otherwise recoverable: a stated
preference, a decision and its rationale, a project constraint, a correction.

**Don't save** what the repo, git history, or docs already record (code structure,
past fixes), or what only matters to the current conversation. If asked to "remember"
something already captured elsewhere, ask what was *non-obvious* about it and save that.

**Before saving**, check for an existing file that covers it — update rather than
duplicate. **Delete** memories that turn out to be wrong.

**On recall**, treat a memory as *what was true when written*. If it names a file,
flag, or person, verify it still exists before acting on it.

**Corrections become lessons.** After any correction, log it to `lessons.md`:
`[YYYY-MM-DD] LESSON: [what went wrong] → RULE: [what to do instead]`, and keep an
Active Rules table at the top. Review `lessons.md` at the start of complex sessions.

**Big insights become learnings.** When a realization is too rich for one memory
line, write a dated doc in `learnings/` and point to it from a `project` memory.

**Close every session** by updating `CURRENT_TASK.md` with what got done and the
exact next step, so the next session (or a different tool) resumes instantly.

---

## Setup

1. Create the directories: `memory/`, `learnings/`, `meeting-notes/`, and the files
   `lessons.md`, `CURRENT_TASK.md`.
2. Copy `memory/MEMORY.example.md` → `memory/MEMORY.md` and clear the examples.
3. In Claude Code, point your memory at this location (or use the default
   `~/.claude/.../memory/`). The index loads each session automatically.
4. These directories are **gitignored** in this repo — they hold your real life.
   Only the `README`, `MEMORY.example.md`, and `EXAMPLE-*` files are committed.

That's it. The second brain grows itself from here: every session can add a fact,
log a lesson, or write a learning, and the next session is a little sharper for it.
