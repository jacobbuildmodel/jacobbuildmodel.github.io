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
read as what it should be, or when Vale reports a file that is not in the diff
(the two name files differently, so no finding could ever match a changed
line): a broken run is not taken for a clean one.

A changed line is a "+" line of the unified diff: the new side of each hunk
("@@ -a,b +c,d @@" gives lines c to c+d-1; d is 1 when left out, and 0 for a
hunk that only deletes). A file the diff adds is all changed lines.

A moved paragraph is old lines. When a page is rearranged, its paragraphs
appear in the diff as "-" lines in one place and the same "+" lines in another.
A run of "+" lines (the "+" lines of one hunk between blank lines) is counted
as moved, not changed, only when both of these hold:
  - every non-blank line of the run is also a "-" line of the same file (one
    "-" line excuses one "+" line), so the whole paragraph moved. One reworded
    or new line makes the whole run changed lines: a published line set beside
    a new one can say something new.
  - none of those "-" lines sat inside an HTML comment or a code fence of the
    base file, where no reader saw it and Vale never checked it. This needs
    the base file: pass --base-ref (the pull request's base commit) and the
    script reads it with git. Without --base-ref this second test is not run
    and the report says so.
November 2026: moving the published paragraphs of three articles into a new
layout turned the check red for words written months earlier; the checker then
showed three ways a new sentence could pass as a moved one (18 November).

Standard library only. Tests: scripts/tests/test_vale_changed_lines.py.
"""
import argparse
import json
import re
import subprocess
import sys

HUNK = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


class InputError(Exception):
    """An input file is not what it should be."""


def norm(path):
    """One spelling for a path: forward slashes, no leading ./"""
    path = path.replace("\\", "/")
    return path[2:] if path.startswith("./") else path


def hidden_lines(text):
    """Line numbers of a file that sit inside an HTML comment or a fenced code block."""
    hidden, in_comment, fence = set(), False, None
    for no, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if fence:
            hidden.add(no)
            if stripped.startswith(fence):
                fence = None
            continue
        if in_comment:
            hidden.add(no)
            if "-->" in line:
                in_comment = False
            continue
        m = re.match(r"(`{3,}|~{3,})", stripped)
        if m:
            fence = m.group(1)[0] * 3
            hidden.add(no)
            continue
        if "<!--" in line:
            hidden.add(no)
            if "-->" not in line.split("<!--", 1)[1]:
                in_comment = True
    return hidden


def changed_lines(diff_text, base_text=None):
    """{path: set of line numbers on the new side} from `git diff -U0` output.

    A run of "+" lines that is a moved paragraph is left out; see the module
    docstring. base_text, when given, is a function from a path to the base
    file's text (or None): a "-" line inside a comment or a code fence of that
    file is no twin.
    """
    changed = {}
    added = {}        # path -> [(hunk index, line number, text)]
    removed = {}      # path -> [(old line number, text)]
    current = None
    next_no = old_no = None
    hunk = 0
    for line in diff_text.splitlines():
        if line.startswith("--- "):
            continue
        if line.startswith("+++ "):
            target = line[4:].strip().strip('"')
            if target == "/dev/null":
                current = None
            else:
                current = norm(target[2:] if target.startswith("b/") else target)
                changed.setdefault(current, set())
                added.setdefault(current, [])
                removed.setdefault(current, [])
            next_no = old_no = None
            continue
        m = HUNK.match(line)
        if m and current is not None:
            start = int(m.group(2))
            count = 1 if m.group(3) is None else int(m.group(3))
            changed[current].update(range(start, start + count))
            next_no, old_no = start, int(m.group(1))
            hunk += 1
            continue
        if current is None:
            continue
        if line.startswith("-") and old_no is not None:
            removed[current].append((hunk, old_no, line[1:].strip()))
            old_no += 1
        elif line.startswith("+") and next_no is not None:
            added[current].append((hunk, next_no, line[1:].strip()))
            next_no += 1
    for path, lines in added.items():
        hidden = set()
        if base_text is not None:
            text = base_text(path)
            hidden = hidden_lines(text) if text else set()
        # The diff alone already shows a comment or a fence that was removed whole: its markers are
        # "-" lines of the same hunk. (The base file, when given, also covers one that stays.)
        by_hunk = {}
        for h, no, text in removed[path]:
            by_hunk.setdefault(h, []).append((no, text))
        for items in by_hunk.values():
            inside = hidden_lines("\n".join(text for _, text in items))
            hidden.update(items[i - 1][0] for i in inside)
        left = {}
        for _, no, text in removed[path]:
            if text and no not in hidden:
                left[text] = left.get(text, 0) + 1
        # runs: the "+" lines of one hunk, cut at blank lines
        runs, run, last = [], [], None
        for h, no, text in lines:
            if not text or (last is not None and (h, no) != (last[0], last[1] + 1)):
                if run:
                    runs.append(run)
                run = []
            if text:
                run.append((no, text))
            last = (h, no)
        if run:
            runs.append(run)
        for run in runs:
            need = {}
            for _, text in run:
                need[text] = need.get(text, 0) + 1
            if all(left.get(text, 0) >= n for text, n in need.items()):
                for text, n in need.items():
                    left[text] -= n
                changed[path].difference_update(no for no, _ in run)
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


def git_base_text(base_ref):
    """A function from a path to that file's text on the old side of `git diff BASE...HEAD`."""
    def run(*args):
        r = subprocess.run(["git"] + list(args), capture_output=True)
        return r.stdout.decode("utf-8", errors="replace") if r.returncode == 0 else None
    merge_base = (run("merge-base", base_ref, "HEAD") or "").strip()
    if not merge_base:
        raise InputError("cannot find the merge base of %s and HEAD" % base_ref)
    return lambda path: run("show", "%s:%s" % (merge_base, path))


def judge(vale, diff_text, base_text=None):
    """(rows, blocking): every finding marked, and the errors on changed lines."""
    changed = changed_lines(diff_text, base_text)
    rows = findings(vale)
    for f in rows:
        # Fail closed: if Vale and git spell a path differently, every finding
        # would read "old line" and errors on new lines would pass unseen.
        if f["path"] not in changed:
            raise InputError("Vale reported %s, which is not in the diff; "
                             "the two name files differently" % f["path"])
        f["changed"] = f["line"] in changed[f["path"]]
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
    ap.add_argument("--base-ref", help="the BASE of that diff; lets a line moved out of a comment or a code "
                                       "fence count as a changed line")
    args = ap.parse_args(argv)
    try:
        with open(args.vale_json, encoding="utf-8") as fh:
            text = fh.read()
        vale = json.loads(text)
        with open(args.diff, encoding="utf-8") as fh:
            diff_text = fh.read()
        rows, blocking = judge(vale, diff_text, git_base_text(args.base_ref) if args.base_ref else None)
    except (OSError, ValueError, InputError) as e:
        out.write("vale_changed_lines.py: %s\n" % e)
        return 2
    report(rows, blocking, out)
    if not args.base_ref:
        out.write("note: no --base-ref, so lines moved out of comments or code fences were not looked for\n")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
