# memory/

Your second brain's core: **atomic, durable facts, one per file.**

- `MEMORY.md` — the index loaded each session (one line per memory). Copy
  `MEMORY.example.md` → `MEMORY.md` to start.
- `EXAMPLE-*.md` — example memory files showing the frontmatter format.
- Your real memory files live here too, but are **gitignored** — they never get committed.

See `../skills/second-brain/SKILL.md` for the full format, the four memory types
(`user` / `feedback` / `project` / `reference`), the recall/dedupe discipline, and
how this connects to `lessons.md`, `learnings/`, and the meeting-notes context library.

## The engine (health auditing)

This folder ships the *convention*. The *engine* is a standalone, deterministic auditor
that checks the index budget, dangling `[[wikilinks]]`, graph orphans, hubs, and stale
entries. It lives in its own repo so it can be shared across tools without drifting:

**https://github.com/willLin-creator/agent-memory-vault**

Clone it alongside this one and point it at this folder:

    python3 memory-reindex.py --dir /path/to/this/memory

See that repo's `docs/ARCHITECTURE.md` for the full design: the bounded hot-set index,
recall by description, enforcement tiers, and the knowledge graph.

## Corrections and enforcement tiers: agent-eval-loop

`lessons.md` is where corrections land. The engine that turns those corrections into a number, and
the number into a recommendation about how much enforcement each rule still needs, lives in its own
repo for the same reason the memory engine does:

**https://github.com/willLin-creator/agent-eval-loop**

Each correction becomes a dated case tagged to a rule slug. `eval_loop.py score` counts recurrence
per rule over rolling windows; `graduate` recommends moving a rule between `hook` (a mechanism
enforces it), `pinned` (always in context), and `recall` (trusted to memory), in both directions,
and never applies the move itself. Its `hats/` are the skeptical evaluators for work with no oracle,
the same Generate, Evaluate, Reconcile discipline this operating system runs in Part 7.I. A memory in
this folder can link to a rule slug, and a promoted rule is a fine thing to write a memory about;
neither repo requires the other.
