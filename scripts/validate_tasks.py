#!/usr/bin/env python3
"""Uniqueness, shape, and intake guard for my-tasks.yaml.

Exits 0 when the file is clean, 1 when it is not. Wire it as a PostToolUse hook on Write/Edit of
my-tasks.yaml (see hooks/settings.example.json), or run it by hand:

    python3 scripts/validate_tasks.py
    python3 scripts/validate_tasks.py --file /path/to/my-tasks.yaml
    python3 scripts/validate_tasks.py --next-id     # print the next safe id
    python3 scripts/validate_tasks.py --intake      # report today's intake against the cap

Why the id check exists: task files are NOT id-ordered. Completions get archived out and edits
reinsert mid-file, so "last entry + 1" is wrong, and allocating that way produced duplicate ids in
the deployment this was extracted from. Allocate from --next-id, which is max(id) over the whole
file plus one.

Why the intake cap exists: a backlog that accepts everything is triaged down and is back over the
line within a week. Measured intake on active days was 12 to 14 new rows; triage cannot win against
that, only a cap can. The cap forces the choice at write time: fold the item into an open row, send
it to the ideas file, or name the row it displaces.

Config (env):
  COS_HOME             directory holding my-tasks.yaml (default ~/.claude)
  TASKS_INTAKE_CAP     net-new rows allowed per day (default 3; 0 disables the cap)
  TASKS_INTAKE_START   YYYY-MM-DD; rows created before this date are grandfathered (default: none)
"""

import argparse
import collections
import datetime
import os
import re
import sys

COS_HOME = os.path.expanduser(os.environ.get("COS_HOME", "~/.claude"))
DEFAULT_PATH = os.path.join(COS_HOME, "my-tasks.yaml")
ID_RE = re.compile(r'^\s*-\s*id:\s*"?(task-(\d+))"?\s*$')
REQUIRED_KEYS = {"id", "title", "status", "priority", "due_date", "created"}

INTAKE_CAP = int(os.environ.get("TASKS_INTAKE_CAP", "3"))
INTAKE_RULE_START = os.environ.get("TASKS_INTAKE_START", "")
CLOSED_STATES = {"complete", "completed", "archived", "packaged"}
# A row is exempt from the cap if it is not net-new work:
#   displaces:    -> one out, one in. The trade is the point.
#   package_key:  -> a consolidation, which REDUCES the count.
INTAKE_EXEMPT_KEYS = ("displaces", "package_key")


def intake_report(tasks, today=None):
    """Return (countable_ids, exempt_ids) for rows created today under the cap."""
    today = today or datetime.date.today().isoformat()
    if INTAKE_RULE_START and today < INTAKE_RULE_START:
        return [], []
    countable, exempt = [], []
    for t in tasks:
        if not isinstance(t, dict) or str(t.get("created")) != today:
            continue
        if t.get("status") in CLOSED_STATES:
            continue
        if any(t.get(k) for k in INTAKE_EXEMPT_KEYS):
            exempt.append(t.get("id"))
        else:
            countable.append(t.get("id"))
    return countable, exempt


def parse_ids(path):
    """Return [(line_no, id_str, id_num)] using a line scan.

    A line scan, not a YAML load: a YAML mapping load would silently collapse duplicate keys, which
    is exactly the failure being checked for. It also keeps the guard dependency-free so a hook can
    call it anywhere.
    """
    found = []
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            m = ID_RE.match(line)
            if m:
                found.append((i, m.group(1), int(m.group(2))))
    return found


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=DEFAULT_PATH)
    ap.add_argument("--next-id", action="store_true",
                    help="print the next safe task id (max across the whole file + 1) and exit")
    ap.add_argument("--quiet", action="store_true", help="print only on failure")
    ap.add_argument("--intake", action="store_true",
                    help="report today's intake against the cap and exit 0 (for a SessionStart hook)")
    ap.add_argument("--no-intake-cap", action="store_true",
                    help="skip the intake cap check (for deliberate bulk operations)")
    args = ap.parse_args(argv)

    path = os.path.expanduser(args.file)
    if not os.path.exists(path):
        if args.intake:
            return 0          # fresh install: nothing to report every session
        print("FAIL: %s does not exist" % path, file=sys.stderr)
        return 1

    ids = parse_ids(path)
    if not ids:
        if args.intake or args.next_id:
            if args.next_id:
                print("task-001")
            return 0
        print("FAIL: no task ids found in %s" % path, file=sys.stderr)
        return 1

    if args.next_id:
        print("task-%03d" % (max(n for _, _, n in ids) + 1))
        return 0

    # --intake: report-only surface, so overage is visible no matter who wrote it. An autonomous
    # layer that writes this file directly never passes through the tool hooks, so a hook alone
    # would police only one writer.
    if args.intake:
        if INTAKE_CAP <= 0:
            return 0
        try:
            import yaml
        except ImportError:
            print("intake: pyyaml unavailable, cannot check")
            return 0
        doc = yaml.safe_load(open(path, encoding="utf-8")) or {}
        countable, exempt = intake_report(doc.get("tasks") or [])
        if len(countable) > INTAKE_CAP:
            print(
                "INTAKE CAP EXCEEDED: %d net-new rows created today, cap is %d.\n"
                "  over the line: %s\n"
                "  Something added rows without passing the gate. Resolve by folding the extras into\n"
                "  existing rows, moving them to the ideas file via /idea, or adding displaces: task-NNN."
                % (len(countable), INTAKE_CAP, ", ".join(countable))
            )
        elif countable or exempt:
            print("intake today: %d/%d net-new%s"
                  % (len(countable), INTAKE_CAP,
                     (", %d exempt (%s)" % (len(exempt), ", ".join(exempt))) if exempt else ""))
        return 0

    problems = []

    # 1. Duplicate ids: the failure this guard exists for.
    counts = collections.Counter(tid for _, tid, _ in ids)
    for tid, n in sorted(counts.items()):
        if n > 1:
            where = ", ".join(str(ln) for ln, t, _ in ids if t == tid)
            problems.append("duplicate id %s appears %dx at lines %s" % (tid, n, where))

    # 2. Parseable YAML, and no task silently missing core fields.
    try:
        import yaml  # optional dependency: the id check works without it
    except ImportError:
        if not args.quiet:
            print("note: pyyaml not available, skipped parse + field checks")
        yaml = None
    if yaml is not None:
        try:
            doc = yaml.safe_load(open(path, encoding="utf-8"))
        except yaml.YAMLError as exc:
            problems.append("YAML does not parse: %s" % exc)
            doc = None
        if isinstance(doc, dict):
            tasks = doc.get("tasks") or []
            if len(tasks) != len(ids):
                problems.append("parsed %d tasks but scanned %d id lines (nesting or indentation is off)"
                                % (len(tasks), len(ids)))
            for t in tasks:
                if not isinstance(t, dict):
                    problems.append("task entry is not a mapping: %r" % (t,))
                    continue
                missing = REQUIRED_KEYS - set(t)
                if missing:
                    problems.append("%s missing required key(s): %s"
                                    % (t.get("id", "<no id>"), ", ".join(sorted(missing))))
        elif doc is not None:
            problems.append("top level of the file is not a mapping with 'tasks'")

        # 3. Intake cap. Blocks the write so the choice gets made now, not at the next triage.
        if isinstance(doc, dict) and not args.no_intake_cap and INTAKE_CAP > 0:
            countable, _ = intake_report(doc.get("tasks") or [])
            if len(countable) > INTAKE_CAP:
                problems.append("INTAKE CAP: %d net-new rows created today, cap is %d. Over the line: %s"
                                % (len(countable), INTAKE_CAP, ", ".join(countable[INTAKE_CAP:])))

    if problems:
        print("FAIL: %s" % path, file=sys.stderr)
        for p in problems:
            print("  - %s" % p, file=sys.stderr)
        if any(p.startswith("duplicate id") for p in problems):
            print("\nFix duplicates by moving the LATER-created task to a fresh id (get one with "
                  "--next-id), keeping the earlier task on the original, then update any prose that "
                  "references the moved task.", file=sys.stderr)
        if any(p.startswith("INTAKE CAP") for p in problems):
            print(
                "\nINTAKE CAP, three ways out. Pick one per extra row, do not raise the cap:\n"
                "  1. Fold it into an open row as a checklist line in that row's notes. Cheapest, and\n"
                "     usually correct, because most 'new tasks' are steps in existing work.\n"
                "  2. Send it to the ideas file via /idea. Correct for anything with no external party\n"
                "     waiting and no hard date. It stays in the funnel for /bet.\n"
                "  3. Trade: add displaces: task-NNN naming an open row you are archiving for it.\n"
                "Two tie-breakers, in order: if the owner is not you it is not a row at all; if nobody\n"
                "external is waiting and there is no hard date, it goes to /idea. Consolidations carrying\n"
                "package_key are exempt, since they reduce the count. For a deliberate bulk operation,\n"
                "re-run with --no-intake-cap.", file=sys.stderr)
        return 1

    if not args.quiet:
        mx = max(n for _, _, n in ids)
        print("OK: %d tasks, all ids unique, max task-%03d, next safe id task-%03d" % (len(ids), mx, mx + 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
