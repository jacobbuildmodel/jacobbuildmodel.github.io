#!/usr/bin/env python3
"""tools/build_calibration.py -- the data file behind the calibration dot strip.

    python tools/build_calibration.py            rewrite data/calibration.yaml
    python tools/build_calibration.py --check    exit 1 if the file is out of date

Reads the record (content/scorecard.md) and writes one row per sealed
prediction that carries a confidence: the piece, the result, the confidence
and where each was read. Nothing is typed by hand and nothing is set here: a
confidence is Jacob's, written into the sealed THESIS before the data was
opened, and this script only copies the number the record already prints
("Confidence 35%."). The strip itself is drawn at build time by
layouts/shortcodes/calibration.html, which stops the build if the rows do not
reproduce the count and the Brier score in the record's front matter.

Each row names the sealed file to check it against: the THESIS.md of the
piece's folder at the seal commit (the piece's sealedLink). Standard library
only; pure ASCII output.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORD = ROOT / "content" / "scorecard.md"
OUT = ROOT / "data" / "calibration.yaml"
BULLET = re.compile(r"^- \*\*(Held|Failed|Neither|Void)[^*]*\*\*\s*(.*)$")
LINK = re.compile(r"\]\((/economics/[0-9-]+)/\)")
CONF = re.compile(r"\bConfidence (\d{1,3})%")

HEAD = """# The scored confidences, one row per sealed prediction that carries one.
# WRITTEN BY tools/build_calibration.py FROM content/scorecard.md. Do not edit by
# hand: change the record, then rerun the script (lint.yml runs it with --check).
# A confidence is Jacob's alone, set before the data was opened; this file copies
# the numbers the record prints and sets none.
#   piece       the project page
#   result      held, failed or neither, as the record's bullet says
#   confidence  per cent, as the record's bullet says
#   words       the bullet's first words, to find it by eye
#   source      where the result and the confidence were read
#   sealed      the sealed file to check the confidence against, at the seal commit
"""


def front(path, key):
    for line in path.read_text(encoding="utf-8").split("\n"):
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def rows():
    out, piece, cur = [], None, None
    lines = RECORD.read_text(encoding="utf-8").split("\n")

    def close():
        if cur and cur["result"] != "void":
            m = CONF.search(cur["text"])
            if m:
                cur["confidence"] = int(m.group(1))
                out.append(cur)

    for n, line in enumerate(lines, 1):
        if line.startswith("## "):
            close()
            cur, piece = None, None
            continue
        m = LINK.search(line)
        if m and piece is None and cur is None:
            piece = m.group(1)
        b = BULLET.match(line)
        if b:
            close()
            cur = {"piece": piece, "result": b.group(1).lower(), "line": n, "text": b.group(2)}
        elif cur is not None and line.startswith("  "):
            cur["text"] += " " + line.strip()
        elif cur is not None and line.strip() == "":
            close()
            cur = None
    close()
    return out


def render():
    parts = [HEAD, "rows:\n"]
    for r in rows():
        if not r["piece"]:
            sys.exit(f"build_calibration.py: no project link above line {r['line']} of content/scorecard.md")
        page = ROOT / "content" / (r["piece"].strip("/") + ".md")
        seal = front(page, "sealedLink")
        m = re.search(r"github\.com/[^/]+/([^/]+)/commit/([0-9a-f]{40})", seal)
        repo = front(page, "repo")
        folder = repo.split("/tree/main/")[1] + "/" if "/tree/main/" in repo else ""
        if not m:
            sys.exit(f"build_calibration.py: {page.name} has no sealedLink to a seal commit")
        words = " ".join(r["text"].split()[:9]).replace('"', "'")
        parts.append(
            f'  - piece: "{r["piece"]}"\n'
            f'    result: {r["result"]}\n'
            f'    confidence: {r["confidence"]}\n'
            f'    words: "{words}"\n'
            f'    source: "content/scorecard.md, line {r["line"]}"\n'
            f'    sealed: "https://github.com/jacobbuildmodel/{m.group(1)}/blob/{m.group(2)}/{folder}THESIS.md"\n'
        )
    text = "".join(parts)
    text.encode("ascii")
    return text


def main():
    text = render()
    if "--check" in sys.argv:
        have = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if have != text:
            print("data/calibration.yaml is out of date: run python tools/build_calibration.py")
            return 1
        print("data/calibration.yaml matches content/scorecard.md")
        return 0
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {text.count('  - piece:')} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
