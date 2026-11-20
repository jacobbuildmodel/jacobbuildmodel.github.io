#!/usr/bin/env python3
"""
Check the "Scope and limits" line on How I work against the built site.

    python scripts/check_scope_line.py public

A project page has a live "My view" when its built HTML holds the section
the myview shortcode prints (class my-view) with words in it beyond the
heading. If any page has one, How I work must carry Jacob's sentence ("In
each 'My view' section I say where I land and why.") and must not carry the
published "No policy recommendations" paragraph. If none has one, the
reverse. Exit 0 when the two agree, 1 when they do not, 2 when the page
cannot be read.

Why: Jacob, 19 Nov 2026 (SCOPE): keep the published paragraph until his
first view is in, then swap his sentence in. The swap is done by
layouts/shortcodes/scope.html; this script reads only the built HTML, so it
does not share the shortcode's logic. Standard library only.
"""
import html
import re
import sys
from pathlib import Path

OLD = "No policy recommendations."
NEW = "In each 'My view' section I say where I land and why."
SECTION = re.compile(r"<section\b[^>]*\bclass=\"?my-view\"?[^>]*>(.*?)</section>", re.S | re.I)


def text(fragment):
    s = re.sub(r"<[^>]+>", " ", fragment)
    s = html.unescape(s)
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


def live_views(site):
    """Project pages whose My view section has words beyond its heading."""
    found = []
    for page in sorted(Path(site).glob("economics/*/index.html")):
        for m in SECTION.finditer(page.read_text(encoding="utf-8")):
            # the heading (with its "#" anchor link) is not words of the view
            words = text(re.sub(r"<h[1-6]\b.*?</h[1-6]\s*>", " ", m.group(1), flags=re.S | re.I))
            if words:
                found.append(page.parent.name)
                break
    return found


def check(site):
    """Return (ok, message)."""
    page = Path(site) / "process" / "index.html"
    if not page.is_file():
        return None, f"cannot read {page}"
    body = text(page.read_text(encoding="utf-8"))
    views = live_views(site)
    has_old, has_new = OLD in body, NEW in body
    if views:
        ok = has_new and not has_old
        want = "Jacob's sentence and not the published paragraph"
    else:
        ok = has_old and not has_new
        want = "the published paragraph and not Jacob's sentence"
    state = (f"{len(views)} live view(s){': ' + ', '.join(views) if views else ''}; "
             f"How I work has the published paragraph: {has_old}, Jacob's sentence: {has_new}")
    return ok, ("PASS" if ok else "FAIL") + f": {state}. Expected {want}."


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    ok, msg = check(argv[1])
    print(msg)
    return 2 if ok is None else (0 if ok else 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
