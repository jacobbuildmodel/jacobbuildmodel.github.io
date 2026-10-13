#!/usr/bin/env python3
"""
Tests for scripts/hooks/guard_open_pages.py. Standard library only.

    python -m unittest tests/test_guard_open_pages.py -v     # from the repo root

Each test feeds the hook the JSON Claude Code would send and reads its exit
code: 2 refuses the edit, 0 lets it through. The hook only reads files, so the
real open pages are used and nothing on disk changes.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "scripts" / "hooks" / "guard_open_pages.py"
PAGE = ROOT / "content" / "open" / "2026-10-03-singapore-dollar.md"
BODY_LINE = "Open question. Predictions sealed on 3 October 2026."
FRONT_LINE = "showToc: false"


def run(tool, tool_input, raw=None):
    payload = raw if raw is not None else json.dumps(
        {"hook_event_name": "PreToolUse", "tool_name": tool,
         "tool_input": tool_input, "cwd": str(ROOT)})
    p = subprocess.run([sys.executable, str(HOOK)], input=payload,
                       capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, p.stderr.strip()


def page_text():
    return PAGE.read_bytes().decode("utf-8").replace("\r\n", "\n")


class GuardOpenPages(unittest.TestCase):

    def test_body_edit_on_sealed_page_is_blocked(self):
        code, err = run("Edit", {"file_path": str(PAGE),
                                 "old_string": BODY_LINE,
                                 "new_string": BODY_LINE + " Edited."})
        self.assertEqual(code, 2)
        self.assertIn("content/open/2026-10-03-singapore-dollar.md", err)
        self.assertIn("coe-analysis/commit/9e46034", err)
        self.assertIn("edit the front matter only", err)
        self.assertEqual(len(err.splitlines()), 1)

    def test_front_matter_edit_passes(self):
        code, err = run("Edit", {"file_path": str(PAGE),
                                 "old_string": FRONT_LINE,
                                 "new_string": FRONT_LINE +
                                 '\nanswered: "/economics/2026-11-14/"'})
        self.assertEqual((code, err), (0, ""))

    def test_multiedit_with_one_body_step_is_blocked(self):
        code, _ = run("MultiEdit", {"file_path": str(PAGE), "edits": [
            {"old_string": FRONT_LINE, "new_string": FRONT_LINE + "\nanswered: x"},
            {"old_string": BODY_LINE, "new_string": "Changed."}]})
        self.assertEqual(code, 2)

    def test_multiedit_front_matter_only_passes(self):
        code, _ = run("MultiEdit", {"file_path": str(PAGE), "edits": [
            {"old_string": FRONT_LINE, "new_string": FRONT_LINE + "\nanswered: x"}]})
        self.assertEqual(code, 0)

    def test_write_same_body_passes_even_as_crlf(self):
        text = page_text().replace(FRONT_LINE, FRONT_LINE + "\nanswered: x")
        self.assertEqual(run("Write", {"file_path": str(PAGE), "content": text})[0], 0)
        crlf = text.replace("\n", "\r\n")
        self.assertEqual(run("Write", {"file_path": str(PAGE), "content": crlf})[0], 0)

    def test_write_changed_body_is_blocked(self):
        text = page_text() + "\nOne more line.\n"
        self.assertEqual(run("Write", {"file_path": str(PAGE), "content": text})[0], 2)

    def test_new_page_with_no_entry_passes(self):
        new = ROOT / "content" / "open" / "2099-01-01-new-question.md"
        code, _ = run("Write", {"file_path": str(new),
                                "content": "---\ntitle: x\n---\nBody.\n"})
        self.assertEqual(code, 0)

    def test_unrelated_file_passes(self):
        code, _ = run("Edit", {"file_path": str(ROOT / "content" / "scorecard.md"),
                               "old_string": "a", "new_string": "b"})
        self.assertEqual(code, 0)

    def test_other_tool_passes(self):
        self.assertEqual(run("Read", {"file_path": str(PAGE)})[0], 0)

    def test_old_string_not_found_passes(self):
        code, _ = run("Edit", {"file_path": str(PAGE),
                               "old_string": "text that is not on the page",
                               "new_string": "x"})
        self.assertEqual(code, 0)

    def test_bad_json_fails_open_with_warning(self):
        code, err = run(None, None, raw="{not json")
        self.assertEqual(code, 0)
        self.assertIn("warning", err)


if __name__ == "__main__":
    unittest.main()
