# Self-heal proposal ledger

Every `/self-heal` proposal is recorded here with its evaluator verdict and your decision, so the
loop never re-pitches a rejected idea and you can see which kinds of change you accept over time.
Newest first. Copy this file to `self-heal/ledger.md` (gitignored) to start.

Market Pulse proposals carry a Lane: A-scanner (retune what the scan watches) or B-priority
(route a recurring market shift to /roadmap or /bet). Everything else uses Lane `-`.

| Date | ID | Lane | Title | Evaluator | Decision | Note |
|------|----|------|-------|-----------|----------|------|
| 2026-08-17 | sh-2026-08-17-1 | - | Make "every acceptance criterion states both branches" an always-on rule | keep | applied | New memory + index line. Evidence: two tickets shipped defects through unstated AC branches in two weeks. Ranked first because both were hand-written and never ran /prd, so only an always-on rule binds. |
| 2026-08-17 | sh-2026-08-17-2 | - | Put the same rule in the /prd AC template | keep | applied | Catches it at authoring for anything that does run /prd. Secondary to -1. |
| 2026-08-17 | sh-2026-08-17-4 | - | Lint tickets for conditional words without a paired branch | kill | rejected | Over-engineered for a two-instance pattern; would fire noise on every well-written AC. |
| 2026-07-15 | sh-seed | - | Ledger initialized | - | - | Loop built; first real run is the next weekly review. |
