#!/usr/bin/env python3
"""
Tests for scripts/vale_changed_lines.py. No Vale and no git: the diff and
Vale's JSON are fixture files in scripts/tests/fixtures/vale_changed_lines/.
Standard library only.

    python -m unittest discover -s scripts/tests -v     # from the repo root

The fixture diff (changed.diff, `git diff -U0` form) changes line 9 of
content/a.md, adds lines 20 to 22, deletes two lines (a hunk with no new
lines) and adds content/new.md whole. Covers: an error on a changed line fails;
errors on old lines only pass; a warning never fails; a new file is all
changed lines; a hunk that only deletes changes no line; Windows paths; and a
Vale run that failed, or a Vale path that is not in the diff, is exit 2, never
a pass.
"""
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import vale_changed_lines as vcl  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "vale_changed_lines"
DIFF = str(FIX / "changed.diff")


def run(vale_json, diff=DIFF):
    out = io.StringIO()
    code = vcl.main(["--vale-json", str(FIX / vale_json), "--diff", diff], out=out)
    return code, out.getvalue()


class ChangedLines(unittest.TestCase):
    def setUp(self):
        self.changed = vcl.changed_lines((FIX / "changed.diff").read_text(encoding="utf-8"))

    def test_changed_and_added_lines(self):
        self.assertEqual(self.changed["content/a.md"], {9, 20, 21, 22})

    def test_a_hunk_that_only_deletes_changes_no_line(self):
        self.assertNotIn(32, self.changed["content/a.md"])

    def test_a_new_file_is_all_changed_lines(self):
        self.assertEqual(self.changed["content/new.md"], {1, 2, 3})

    def test_count_left_out_means_one_line(self):
        self.assertEqual(vcl.changed_lines("+++ b/x.md\n@@ -4 +7 @@\n+new\n"), {"x.md": {7}})

    def test_a_deleted_file_has_no_changed_lines(self):
        self.assertEqual(vcl.changed_lines("--- a/x.md\n+++ /dev/null\n@@ -1,2 +0,0 @@\n-a\n-b\n"), {})


class ExitCodes(unittest.TestCase):
    def test_error_on_a_changed_line_fails(self):
        code, text = run("error_on_changed_line.json")
        self.assertEqual(code, 1)
        self.assertRegex(text, r"changed line\s+error\s+content/a\.md:21:3\s+Site\.Directives")
        self.assertRegex(text, r"old line\s+error\s+content/a\.md:5:3\s+Site\.Acronyms")
        self.assertIn("FAIL: 1 error(s) on lines this pull request adds or changes", text)

    def test_old_line_errors_only_pass(self):
        code, text = run("old_line_errors_only.json")
        self.assertEqual(code, 0)
        self.assertRegex(text, r"old line\s+error\s+content/a\.md:5:3")
        self.assertRegex(text, r"old line\s+error\s+content/a\.md:32:3")
        self.assertIn("0 error(s) on changed lines, 2 error(s) on old lines", text)
        self.assertIn("PASS", text)

    def test_a_warning_never_fails_even_on_a_changed_line(self):
        code, text = run("warning_on_changed_line.json")
        self.assertEqual(code, 0)
        self.assertRegex(text, r"changed line\s+warning\s+content/a\.md:9:3\s+Site\.Causal")

    def test_error_in_a_new_file_fails(self):
        code, text = run("error_in_new_file.json")
        self.assertEqual(code, 1)
        self.assertRegex(text, r"changed line\s+error\s+content/new\.md:2:3")

    def test_windows_paths_match_the_diff(self):
        code, text = run("windows_paths.json")
        self.assertEqual(code, 1)
        self.assertIn("content/a.md:21:3", text)

    def test_every_finding_is_printed(self):
        _, text = run("error_on_changed_line.json")
        self.assertEqual(len([l for l in text.splitlines() if l.startswith(("changed line", "old line"))]), 3)
        self.assertIn("3 finding(s)", text)


class BrokenInputs(unittest.TestCase):
    def test_a_failed_vale_run_is_not_a_pass(self):
        code, text = run("vale_failed.json")
        self.assertEqual(code, 2)
        self.assertIn("not a list of alerts", text)

    def test_a_vale_path_that_is_not_in_the_diff_fails_closed(self):
        # Vale naming a file differently from git (here an absolute path) would
        # make every finding an "old line"; that must stop the job, not pass it.
        code, text = run("path_not_in_diff.json")
        self.assertEqual(code, 2)
        self.assertIn("vale_changed_lines.py: Vale reported /home/runner/work/site/content/a.md, "
                      "which is not in the diff; the two name files differently", text)
        self.assertNotIn("PASS", text)

    def test_missing_file(self):
        code, _ = run("no_such_file.json")
        self.assertEqual(code, 2)

    def test_empty_or_broken_json(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            for name, body in (("empty.json", ""), ("broken.json", "{not json")):
                p = Path(tmp) / name
                p.write_text(body, encoding="utf-8")
                out = io.StringIO()
                self.assertEqual(vcl.main(["--vale-json", str(p), "--diff", DIFF], out=out), 2)

    def test_no_findings_passes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "clean.json"
            p.write_text("{}\n", encoding="utf-8")
            out = io.StringIO()
            self.assertEqual(vcl.main(["--vale-json", str(p), "--diff", DIFF], out=out), 0)
            self.assertIn("0 finding(s)", out.getvalue())


if __name__ == "__main__":
    unittest.main()
