#!/usr/bin/env python3
"""
vale_changed_lines.py -- fail a pull request only for Vale errors on lines it
adds or changes.

    vale --no-exit --output=JSON <files> > vale.json
    git diff -U0 "$BASE"...HEAD -- <files> > changed.diff
    python scripts/vale_changed_lines.py --vale-json vale.json --diff changed.diff

Why: .github/workflows/lint.yml runs Vale over every content file a pull
request touches, whole. Older pages still carry findings, so editing one line
of such a page used to turn the pull request red for words it never wrote.
This filter keeps every finding visible and fails only for the new ones.

Each finding is printed and marked:
    changed line   the line is added or changed by the diff
    old line       the line was already there
Exit 1 when an error sits on a changed line. Warnings (the causal verbs) and
suggestions never fail, on any line, as before. Exit 2 when an input cannot be
read as what it should be, so a broken Vale run is not taken for a clean one.

A changed line is a "+" line of the unified diff: the new side of each hunk
("@@ -a,b +c,d @@" gives lines c to c+d-1; d is 1 when left out, and 0 for a
hunk that only deletes). A file the diff adds is all changed lines.

Standard library only. Tests: scripts/tests/test_vale_changed_lines.py.
"""
import argparse
import json
import re
import sys

HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


class InputError(Exception):
    """An input file is not what it should be."""


def norm(path):
    """One spelling for a path: forward slashes, no leading ./"""
    path = path.replace("\\", "/")
    return path[2:] if path.startswith("./") else path


def changed_lines(diff_text):
    """{path: set of line numbers on the new side} from `git diff -U0` output."""
    changed = {}
    current = None
    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            target = line[4:].strip().strip('"')
            if target == "/dev/null":
                current = None
            else:
                current = norm(target[2:] if target.startswith("b/") else target)
                changed.setdefault(current, set())
            continue
        m = HUNK.match(line)
        if m and current is not None:
            start = int(m.group(1))
            count = 1 if m.group(2) is None else int(m.group(2))
            changed[current].update(range(start, start + count))
    return changed


def findings(vale):
    """Vale's JSON ({path: [alert, ...]}) as a flat, sorted list of dicts."""
    if not isinstance(vale, dict):
        raise InputError("Vale JSON is not an object of files")
    out = []
    for path, alerts in vale.items():
        if not isinstance(alerts, list):
            # Vale reports its own failures as {"Code": "E100", "Text": "..."}.
            raise InputError("Vale JSON is not a list of alerts per file: %s: %r" % (path, alerts))
        for a in alerts:
            try:
                out.append({
                    "path": norm(path),
                    "line": int(a["Line"]),
                    "col": int((a.get("Span") or [0])[0]),
                    "severity": str(a["Severity"]),
                    "check": str(a.get("Check", "")),
                    "message": str(a.get("Message", "")),
                })
            except (KeyError, TypeError, ValueError) as e:
                raise InputError("Vale alert without Line or Severity in %s: %r" % (path, a)) from e
    return sorted(out, key=lambda f: (f["path"], f["line"], f["col"]))


def judge(vale, diff_text):
    """(rows, blocking): every finding marked, and the errors on changed lines."""
    changed = changed_lines(diff_text)
    rows = findings(vale)
    for f in rows:
        f["changed"] = f["line"] in changed.get(f["path"], ())
    blocking = [f for f in rows if f["changed"] and f["severity"] == "error"]
    return rows, blocking


def report(rows, blocking, out=sys.stdout):
    for f in rows:
        out.write("%-12s  %-7s  %s:%d:%d  %s  %s\n" % (
            "changed line" if f["changed"] else "old line",
            f["severity"], f["path"], f["line"], f["col"], f["check"], f["message"]))
    errors = [f for f in rows if f["severity"] == "error"]
    out.write("%d finding(s): %d error(s) on changed lines, %d error(s) on old lines, "
              "%d warning(s) or suggestion(s)\n" % (
                  len(rows), len(blocking), len(errors) - len(blocking), len(rows) - len(errors)))
    if blocking:
        out.write("FAIL: %d error(s) on lines this pull request adds or changes\n" % len(blocking))
    else:
        out.write("PASS: no error on a line this pull request adds or changes\n")


def main(argv=None, out=sys.stdout):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--vale-json", required=True, help="output of vale --output=JSON")
    ap.add_argument("--diff", required=True, help="output of git diff -U0 BASE...HEAD -- files")
    args = ap.parse_args(argv)
    try:
        with open(args.vale_json, encoding="utf-8") as fh:
            text = fh.read()
        vale = json.loads(text)
        with open(args.diff, encoding="utf-8") as fh:
            diff_text = fh.read()
        rows, blocking = judge(vale, diff_text)
    except (OSError, ValueError, InputError) as e:
        out.write("vale_changed_lines.py: %s\n" % e)
        return 2
    report(rows, blocking, out)
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
