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
