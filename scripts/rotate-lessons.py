#!/usr/bin/env python3
"""rotate-lessons.py: keep lessons.md small enough to actually be read.

CLAUDE.md Part 9 says "review lessons.md at the start of any complex or multi-step session." That
instruction only works while the file is cheap to read. In the deployment this was extracted from,
the file reached 115KB and ~80 entries, roughly 29k tokens; an instruction that expensive gets
skipped, and a skipped review means the promotion loop (correction -> count -> hook or pinned rule)
quietly stops working. Same failure a memory index has: a file grew past the budget of the thing
that consumes it.

What is kept vs archived
------------------------
  KEPT, always and untouched: everything above `## Log`. That is the header, the enforcement tiers,
    and the Active Rules table, which is the DISTILLED layer and the part actually worth re-reading.
    Rotation never edits a rule.
  KEPT: the most recent log entries, newest first, until the log would exceed --keep-bytes.
  ARCHIVED: everything older, appended to lessons-archive/<YYYY-MM>.md, grouped by the entry's own
    date. Nothing is deleted, and a pointer to the archive is left in lessons.md.

Rotating is safe precisely because a lesson's durable form is its Active Rule, not its log entry. If
a lesson has no rule, archiving it is the signal that it never earned one.

Usage:
  rotate-lessons.py --dry              # show what would move
  rotate-lessons.py                    # rotate
  rotate-lessons.py --check            # exit 1 if over budget (for a SessionStart hook)
  rotate-lessons.py --keep-bytes 30000

Config (env): COS_HOME, the directory holding lessons.md (default ~/.claude).
"""

import argparse
import os
import re
import sys
from collections import OrderedDict

HOME = os.path.expanduser(os.environ.get("COS_HOME", "~/.claude"))
LESSONS = os.path.join(HOME, "lessons.md")
ARCHIVE_DIR = os.path.join(HOME, "lessons-archive")
DEFAULT_KEEP = 15_000          # bytes of LOG to retain (header/rules are always kept)
TOTAL_WARN = 45_000            # whole-file budget before --check complains

ENTRY_RE = re.compile(r"^\[(\d{4})-(\d{2})-(\d{2})\]", re.M)
POINTER = "<!-- older entries: lessons-archive/ (rotated by scripts/rotate-lessons.py) -->"


def split_entries(log_text):
    """-> ([(date, text)] in document order, preamble before the first entry)."""
    marks = [m.start() for m in ENTRY_RE.finditer(log_text)]
    if not marks:
        return [], log_text
    preamble = log_text[: marks[0]]
    out = []
    for i, start in enumerate(marks):
        end = marks[i + 1] if i + 1 < len(marks) else len(log_text)
        chunk = log_text[start:end]
        d = ENTRY_RE.match(chunk)
        out.append(("%s-%s-%s" % d.groups(), chunk))
    return out, preamble


def plan(entries, keep_bytes):
    """Split entries into (keep, archive).

    Sort by DATE, newest first; do not trust document order. The header may say "new entries go
    at the top" but real files are only mostly ordered, and trusting position once archived the
    newest lesson while keeping older ones.

    Keep a contiguous PREFIX of the newest entries and STOP at the first that does not fit. A greedy
    fill (skip the one that does not fit, keep trying smaller older ones) archived a newer entry
    because it was large and kept an older smaller one that happened to fit. "Keep the most recent"
    has to mean a prefix, or the newest lessons, which are the most relevant, get silently dropped.
    The very newest entry is always kept even if it alone exceeds the budget.
    """
    entries = sorted(entries, key=lambda e: e[0], reverse=True)
    keep, archive, run, full = [], [], 0, False
    for d, chunk in entries:
        size = len(chunk.encode())
        if not full and (run + size <= keep_bytes or not keep):
            keep.append((d, chunk))
            run += size
        else:
            full = True
            archive.append((d, chunk))
    return keep, archive


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=LESSONS)
    ap.add_argument("--archive-dir", default=ARCHIVE_DIR)
    ap.add_argument("--keep-bytes", type=int, default=DEFAULT_KEEP)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    path = os.path.expanduser(args.file)
    if not os.path.exists(path):
        # A missing lessons.md is a fresh install, not a failure to report every session.
        return 0
    text = open(path, encoding="utf-8").read()
    if "## Log" not in text:
        print("FAIL: no '## Log' section in %s" % path, file=sys.stderr)
        return 1
    head, log = text.split("## Log", 1)
    entries, preamble = split_entries(log)
    total = len(text.encode())

    if args.check:
        if total > TOTAL_WARN:
            print(
                "lessons.md is %d bytes / %d budget with %d entries. CLAUDE.md asks for a read at the "
                "start of complex sessions, which is not affordable at this size.\n"
                "  Rotate: python3 scripts/rotate-lessons.py" % (total, TOTAL_WARN, len(entries)),
                file=sys.stderr,
            )
            return 1
        if not args.quiet:
            print("lessons.md OK: %d bytes / %d, %d entries" % (total, TOTAL_WARN, len(entries)))
        return 0

    keep, archive = plan(entries, args.keep_bytes)
    run = sum(len(c.encode()) for _, c in keep)

    print("entries: %d total -> keep %d, archive %d" % (len(entries), len(keep), len(archive)))
    print("file   : %d bytes -> ~%d bytes" % (total, len(head.encode()) + run + 200))
    if keep:
        print("keeping: %s .. %s" % (keep[0][0], keep[-1][0]))
    if archive:
        print("archiving: %s .. %s" % (archive[0][0], archive[-1][0]))
    by_month = OrderedDict()
    for d, chunk in archive:
        by_month.setdefault(d[:7], []).append((d, chunk))
    for m, items in by_month.items():
        print("  %s -> %d entries" % (m, len(items)))

    if args.dry:
        print("\nDRY RUN, nothing written.")
        return 0
    if not archive:
        print("nothing to rotate.")
        return 0

    archive_dir = os.path.expanduser(args.archive_dir)
    os.makedirs(archive_dir, exist_ok=True)
    for m, items in by_month.items():
        apath = os.path.join(archive_dir, "%s.md" % m)
        existing = open(apath, encoding="utf-8").read() if os.path.exists(apath) else (
            "# Lessons archive %s\n\n"
            "Rotated out of lessons.md to keep it readable. The durable form of a lesson is its\n"
            "row in the Active Rules table there; this is the original log entry.\n" % m
        )
        with open(apath, "w", encoding="utf-8") as fh:
            fh.write(existing.rstrip("\n") + "\n\n" + "\n".join(c.rstrip() for _, c in items) + "\n")

    new_log = "## Log" + preamble.rstrip("\n") + "\n\n" + POINTER + "\n\n" + \
        "\n".join(c.rstrip() for _, c in keep) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(head.rstrip("\n") + "\n\n" + new_log)

    after = os.path.getsize(path)
    print("\nrotated. lessons.md now %d bytes (was %d). archive: %s" % (after, total, archive_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
