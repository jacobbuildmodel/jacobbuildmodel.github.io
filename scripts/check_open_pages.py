#!/usr/bin/env python3
"""
check_open_pages.py -- an open question page cannot change silently after its
seal day.

Usage:
    python scripts/check_open_pages.py                 # run from the repo root
    python scripts/check_open_pages.py --base <ref>    # also require reason: lines

No dependencies. Python 3.8+.

Three checks:

1. Every content/open/*.md page (not _index.md) has an entry in
   data/open_seals.yaml, every entry has a page, and the md5 of the page body
   matches the entry. The body is everything after the closing --- of the
   front matter. Front matter is left out, which is where the answered marker
   lives (answered: "/economics/<slug>/", read by
   layouts/partials/answered_verdict.html, page_banner.html and
   open_questions_strip.html), so marking a page answered never trips this.
2. With --base: an entry whose body_md5 differs from the same entry at <ref>
   must carry a reason: line that is new or changed against <ref>, so an
   intentional edit to a sealed page shows in the diff with its why.
3. The scorecard page (whichever content page's front matter has sealed, held,
   failed and neither) satisfies sealed == held + failed + neither.

Exits 1 on any failure, printing one FAIL line per problem.
"""
import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

OPEN_DIR = Path("content/open")
SEALS = Path("data/open_seals.yaml")
CONTENT = Path("content")
KEYS = ("path", "body_md5", "seal", "reason")
BAND = ("sealed", "held", "failed", "neither")


def split_front_matter(raw):
    """Return (front matter lines, body bytes). Front matter is YAML between
    a first line '---' and the next line '---'."""
    lines = raw.split(b"\n")
    if not lines or lines[0].rstrip(b"\r") != b"---":
        return None, raw
    for i in range(1, len(lines)):
        if lines[i].rstrip(b"\r") == b"---":
            front = [l.rstrip(b"\r").decode("utf-8") for l in lines[1:i]]
            return front, b"\n".join(lines[i + 1:])
    return None, raw


def body_md5(path):
    front, body = split_front_matter(Path(path).read_bytes())
    if front is None:
        return None
    return hashlib.md5(body).hexdigest()


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_seals(text, where):
    """A strict reader for the one shape data/open_seals.yaml uses:
    a list of flat mappings, keys from KEYS, scalar values on one line."""
    entries, errors = [], []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^(- |  )([a-z0-9_]+):\s*(.*)$", line)
        if not m or m.group(2) not in KEYS:
            errors.append(f"{where}:{n}: cannot read line: {line!r}")
            continue
        lead, key, value = m.groups()
        if lead == "- ":
            entries.append({})
        elif not entries:
            errors.append(f"{where}:{n}: key before the first '- ' entry")
            continue
        if key in entries[-1]:
            errors.append(f"{where}:{n}: {key} given twice in one entry")
        entries[-1][key] = unquote(value)
    by_path = {}
    for e in entries:
        p = e.get("path", "")
        for k in ("path", "body_md5", "seal"):
            if not e.get(k):
                errors.append(f"{where}: entry {p or '?'} has no {k}")
        if p in by_path:
            errors.append(f"{where}: two entries for {p}")
        by_path[p] = e
    return by_path, errors


def check_pages(seals):
    fails = []
    pages = sorted(p for p in OPEN_DIR.glob("*.md") if p.name != "_index.md")
    seen = set()
    for page in pages:
        key = page.as_posix()
        seen.add(key)
        got = body_md5(page)
        if got is None:
            fails.append(f"FAIL {key}: no front matter, cannot find the body")
            continue
        entry = seals.get(key)
        if entry is None:
            fails.append(f"FAIL {key}: no entry in {SEALS} (body md5 {got})")
        elif entry.get("body_md5") != got:
            fails.append(
                f"FAIL {key}: body md5 {got} != sealed {entry.get('body_md5')} "
                f"in {SEALS}; an intentional edit changes body_md5 there and "
                f"adds a reason: line")
        else:
            print(f"ok   {key}: body md5 {got} matches")
    for key in sorted(set(seals) - seen):
        fails.append(f"FAIL {key}: entry in {SEALS} but no such page")
    return fails


def check_reasons(seals, base):
    try:
        old_text = subprocess.run(
            ["git", "show", f"{base}:{SEALS.as_posix()}"],
            check=True, capture_output=True, text=True).stdout
    except subprocess.CalledProcessError:
        print(f"ok   {SEALS} not at {base}: every entry is new, no reason: needed")
        return []
    old, errors = parse_seals(old_text, f"{base}:{SEALS}")
    if errors:
        return [f"FAIL {e}" for e in errors]
    fails = []
    for key, entry in sorted(seals.items()):
        before = old.get(key)
        if before is None or before.get("body_md5") == entry.get("body_md5"):
            continue
        reason = entry.get("reason", "")
        if not reason or reason == before.get("reason", ""):
            fails.append(
                f"FAIL {key}: body_md5 changed against {base} with no new "
                f"reason: line in {SEALS}")
        else:
            print(f"ok   {key}: body_md5 changed, reason: {reason}")
    return fails


def check_scorecard():
    found = []
    for page in sorted(CONTENT.rglob("*.md")):
        front, _ = split_front_matter(page.read_bytes())
        if front is None:
            continue
        values = {}
        for line in front:
            m = re.match(r"^([a-z]+):\s*(.*?)\s*(#.*)?$", line)
            if m and m.group(1) in BAND:
                values[m.group(1)] = unquote(m.group(2))
        if set(values) == set(BAND):
            found.append((page.as_posix(), values))
    if not found:
        return [f"FAIL no page under {CONTENT}/ has {', '.join(BAND)} "
                f"in its front matter"]
    fails = []
    for key, values in found:
        try:
            n = {k: int(v) for k, v in values.items()}
        except ValueError:
            fails.append(f"FAIL {key}: {values} are not all whole numbers")
            continue
        total = n["held"] + n["failed"] + n["neither"]
        line = (f"{key}: sealed {n['sealed']}, held {n['held']} + failed "
                f"{n['failed']} + neither {n['neither']} = {total}")
        if n["sealed"] != total:
            fails.append(f"FAIL {line}")
        else:
            print(f"ok   {line}")
    return fails


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--base", help="git ref to compare data/open_seals.yaml with")
    args = ap.parse_args()

    if not SEALS.is_file():
        print(f"FAIL {SEALS} is missing")
        return 1
    seals, errors = parse_seals(SEALS.read_text(encoding="utf-8"), str(SEALS))
    fails = [f"FAIL {e}" for e in errors]
    fails += check_pages(seals)
    if args.base:
        fails += check_reasons(seals, args.base)
    fails += check_scorecard()

    for f in fails:
        print(f)
    print("open pages check: " + (f"{len(fails)} failure(s)" if fails else "passed"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
