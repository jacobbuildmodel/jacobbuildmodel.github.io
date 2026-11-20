#!/usr/bin/env python3
"""
Tests for scripts/check_scope_line.py. Each case writes a tiny built site
into a temporary folder. Standard library only.

    python -m unittest discover -s scripts/tests -v     # from the repo root
"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_scope_line as csl  # noqa: E402

OLD_P = ("<p><strong>No policy recommendations.</strong> These pieces explain what the data shows. "
         "What a government ought to do about it is a different question, involving trade-offs the "
         "data does not contain, and I do not answer it.</p>")
NEW_P = ("<p>The site tests popular arguments against public data. In each ‘My view’ section "
         "I say where I land and why.</p>")
VIEW = '<section class="my-view" aria-labelledby="my-view"><h2 id="my-view">My view</h2><p>I would keep the quota.</p></section>'
EMPTY_VIEW = '<section class=my-view><h2 id=my-view>My view <a hidden class=anchor aria-hidden=true href=#my-view>#</a></h2></section>'


def site(tmp, process, pages):
    root = Path(tmp)
    (root / "process").mkdir(parents=True)
    (root / "process" / "index.html").write_text(f"<main>{process}</main>", encoding="utf-8")
    for slug, html in pages.items():
        d = root / "economics" / slug
        d.mkdir(parents=True)
        d.joinpath("index.html").write_text(f"<main><p>Body.</p>{html}</main>", encoding="utf-8")
    return str(root)


class ScopeLine(unittest.TestCase):
    def run_case(self, process, pages):
        with tempfile.TemporaryDirectory() as tmp:
            return csl.check(site(tmp, process, pages))[0]

    def test_no_view_published_paragraph_passes(self):
        self.assertTrue(self.run_case(OLD_P, {"2026-08-22": ""}))

    def test_no_view_new_sentence_fails(self):
        self.assertFalse(self.run_case(NEW_P, {"2026-08-22": ""}))

    def test_view_live_new_sentence_passes(self):
        self.assertTrue(self.run_case(NEW_P, {"2026-08-22": VIEW}))

    def test_view_live_old_paragraph_fails(self):
        self.assertFalse(self.run_case(OLD_P, {"2026-08-22": VIEW}))

    def test_both_texts_fail_either_way(self):
        self.assertFalse(self.run_case(OLD_P + NEW_P, {"2026-08-22": ""}))
        self.assertFalse(self.run_case(OLD_P + NEW_P, {"2026-08-22": VIEW}))

    def test_heading_only_section_is_not_a_live_view(self):
        # a minified, unquoted section with only its heading and the heading's "#" anchor
        self.assertTrue(self.run_case(OLD_P, {"2026-08-22": EMPTY_VIEW}))
        self.assertFalse(self.run_case(NEW_P, {"2026-08-22": EMPTY_VIEW}))

    def test_missing_page_is_an_error_not_a_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(csl.check(tmp)[0])


if __name__ == "__main__":
    unittest.main()
