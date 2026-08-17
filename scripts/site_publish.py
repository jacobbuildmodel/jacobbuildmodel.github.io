#!/usr/bin/env python3
"""
site_publish.py — the gate between model output and the public site.

Same contract as brief_intake.py: it scans BEFORE anything lands, and a hit
refuses the whole operation and writes nothing.

    python scripts/site_publish.py "<staged .md file>"
    python scripts/site_publish.py "<staged .md>" --date 2026-08-15
    python scripts/site_publish.py "<staged .md>" --scan-only

What it does, in order:
    1. Scans the source for credentials, holdings, sizing, rankings and
       recommendation language. ANY hit -> exit 2, nothing written.
    2. Strips section 7 / HANDOFF onward, and any fenced JSON block.
    3. Re-scans the stripped text (belt and braces).
    4. Derives the as_of date (Saturday of the coverage week) and writes
       content/briefs/YYYY-MM-DD.md with front matter and draft: true.
    5. Prints a review checklist. The post stays draft until a human clears it.

It deliberately does NOT rewrite prose. Automatic transformation of analysis is
where errors hide. This stages a safe skeleton; the human edit pass is real work.
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# REFUSAL PATTERNS — a hit means nothing gets written.
# Ordered by how bad it would be to publish.
# ─────────────────────────────────────────────────────────────────────────────

CREDENTIALS = [
    (r"sk-ant-[A-Za-z0-9_\-]{10,}",           "Anthropic API key"),
    (r"ghp_[A-Za-z0-9]{20,}",                  "GitHub personal access token"),
    (r"github_pat_[A-Za-z0-9_]{20,}",          "GitHub fine-grained token"),
    (r"AKIA[0-9A-Z]{16}",                      "AWS access key id"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----",    "private key block"),
    (r"(?i)\b(api[_\-]?key|secret|passwd|password|bearer)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}",
                                               "credential assignment"),
]

STATE_PATHS = [
    (r"(?i)\baccounts[/\\][A-Za-z0-9_\-]+\.json", "DRIVE accounts state file path"),
    (r"(?i)\bPRE[/\\]ledger\.jsonl",              "capital ledger path"),
    (r"(?i)\b(10K|positions|holdings)\.json\b",   "holdings state file"),
    (r"(?i)\bSTATE\.md\b|\bRATINGS\.md\b",        "DRIVE state document"),
]

DISCLOSURE = [
    (r"(?i)\bmy (position|holding|portfolio|book|allocation|stake)\b", "position disclosure"),
    (r"(?i)\bI (?:currently )?(own|hold|bought|sold|added to|trimmed)\b", "position disclosure"),
    (r"(?i)\bI'?m (long|short)\b",                     "directional position disclosure"),
    (r"(?i)\b(cost basis|unrealised|unrealized|realised P&L|realized P&L)\b", "P&L disclosure"),
    (r"(?i)\b(position siz\w+|kelly (fraction|siz\w+|criterion)|half[- ]size|full size)\b",
                                                        "position sizing"),
    (r"(?i)\b\d+(\.\d+)?\s*%\s*(of (the |my )?(portfolio|book|nav|capital))", "portfolio weight"),
    (r"(?i)\b(portfolio|book) (weight|allocation) (of|is|at)\b", "portfolio weight"),
    (r"(?i)\b(account balance|cash balance|buying power)\b", "account balance"),
]

SCORES_AND_CALLS = [
    (r"(?i)\b(composite|quality|value|conviction)\s+score\b", "model score"),
    (r"(?i)\bscore\s*[:=]\s*\d",                              "model score"),
    (r"(?i)\brank(ed|ing)?\s*[:#=]\s*\d",                     "model ranking"),
    (r"(?i)\bexpected (payoff|value|return) of\b",            "payoff estimate"),
    (r"(?i)\bT\+1 (price|target|estimate) (of|is|:)\s*\$?\d", "CATALYST directional call"),
    (r"(?i)\bprice target\b",                                 "price target"),
]

RECOMMENDATION = [
    (r"(?i)\bconsider (buying|selling|adding)\b",  "recommendation language"),
    (r"(?i)\b(strong )?(buy|sell) (rating|signal|call)\b", "recommendation language"),
    (r"(?i)\b(you should|I recommend|I'd recommend) (buy|sell|add|trim)", "recommendation language"),
    (r"(?i)\bstocks? to buy\b",                    "recommendation language"),
]

BANDS = [
    ("CREDENTIAL",     CREDENTIALS),
    ("DRIVE STATE",    STATE_PATHS),
    ("DISCLOSURE",     DISCLOSURE),
    ("SCORE / CALL",   SCORES_AND_CALLS),
    ("RECOMMENDATION", RECOMMENDATION),
]

# ─────────────────────────────────────────────────────────────────────────────
# FLAGS — do not refuse, but must be reviewed before the draft goes live.
# ─────────────────────────────────────────────────────────────────────────────

FLAGS = [
    # A big number sitting next to projection language. This is the $370bn shape:
    # a single sell-side estimate about a future year, which is the highest-risk
    # thing a post can carry because nothing filed contradicts it yet.
    (r"(?i)\$\s?\d[\d,\.]*\s?(?:bn|billion|tn|trillion)\b[^.\n]{0,120}?"
     r"\b(?:estimat\w+|project\w+|forecast\w+|could|by 20\d\d|expect\w+)\b",
     "projected figure — single-source? verify before it goes out under your name"),
    (r"(?i)\b(?:estimat\w+|project\w+|forecast\w+|could reach|by 20\d\d)\b[^.\n]{0,120}?"
     r"\$\s?\d[\d,\.]*\s?(?:bn|billion|tn|trillion)\b",
     "projected figure — single-source? verify before it goes out under your name"),

    # $100bn+ (unit required, so $365.5m does not trip it), or anything in trillions.
    (r"\$\s?(?:[1-9]\d{2,}(?:[\d,\.]*)?\s?(?:bn|billion)|\d[\d,\.]*\s?(?:tn|trillion))\b",
     "figure at or above $100bn — confirm the magnitude and the unit"),

    # Signed moves of 50%+, or any unsigned figure of 70%+. Keeps probability
    # levels like "55% odds" out of the list while catching a −90.1% collapse.
    (r"[-+−–]\s?(?:[5-9]\d|\d{3,})(?:\.\d+)?\s?%",
     "signed change of 50% or more — confirm base, period and direction"),
    (r"\b(?:[7-9]\d|\d{3,})(?:\.\d+)?\s?%",
     "figure of 70% or more — confirm base and period"),

    # Market-cap derivations built on an unsourced share price.
    (r"(?i)market\s?cap\w*[^.\n]{0,80}\$\s?\d",
     "market-cap derivation — is the share price itself sourced?"),

    # Sell-side attribution: a named bank plus a number is a libel-adjacent shape
    # if the note does not say what you claim it says.
    (r"(?i)\b(?:BofA|Bank of America|Goldman|Morgan Stanley|JPMorgan|Jefferies|Barclays|UBS|Citi)\b"
     r"[^.\n]{0,120}\$\s?\d",
     "figure attributed to a named bank — confirm the note says this"),

    # Declared gaps must survive into the published post.
    (r"(?i)\b(?:figure not obtained|not obtained|could not reconcile)\b",
     "declared gap — must appear in the published gaps list"),
]

STRIP_FROM = re.compile(
    r"^\s{0,3}#{1,4}\s*(§\s*7|7\.|SECTION\s*7|HANDOFF)\b.*$",
    re.IGNORECASE | re.MULTILINE,
)
JSON_FENCE = re.compile(r"^```(?:json)?\s*\n\s*\{.*?^```\s*$", re.DOTALL | re.MULTILINE)


def scan(text, patterns_bands):
    hits = []
    for band, patterns in patterns_bands:
        for pattern, label in patterns:
            for m in re.finditer(pattern, text):
                line = text.count("\n", 0, m.start()) + 1
                snippet = text.splitlines()[line - 1].strip()[:110]
                hits.append((band, label, line, snippet))
    return hits


def strip_machine_sections(text):
    notes = []
    m = STRIP_FROM.search(text)
    if m:
        removed = text[m.start():].count("\n")
        text = text[: m.start()].rstrip() + "\n"
        notes.append(f"stripped section 7 / handoff onward ({removed} lines)")
    text, n = JSON_FENCE.subn("", text)
    if n:
        notes.append(f"stripped {n} fenced JSON block(s)")
    return text.rstrip() + "\n", notes


def coverage_saturday(text, override=None):
    if override:
        return dt.date.fromisoformat(override)
    m = re.search(r"as_of[:\*\s]*\**\s*(\d{4}-\d{2}-\d{2})", text, re.IGNORECASE)
    if m:
        d = dt.date.fromisoformat(m.group(1))
    else:
        d = dt.date.today()
    # Snap back to the Saturday of that coverage week. Saturday == weekday 5.
    return d - dt.timedelta(days=(d.weekday() - 5) % 7)


def build_front_matter(date):
    return (
        "---\n"
        f'title: "Weekly Brief — {date.strftime("%-d %B %Y") if sys.platform != "win32" else date.strftime("%#d %B %Y")}"\n'
        f"date: {date.isoformat()}\n"
        "draft: true          # cleared by a human, not by this script\n"
        "showToc: true\n"
        "TocOpen: false\n"
        'summary: "TODO — one plain-English line. The most interesting thing in this brief."\n'
        'tags: ["weekly brief"]\n'
        "---\n\n"
        "> **TODO — the hook.** One to three sentences, no jargon, before any structure.\n\n"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="staged markdown file from the model output folder")
    ap.add_argument("--repo", default=".", help="path to the site repo root (default: cwd)")
    ap.add_argument("--date", help="override the as_of date (YYYY-MM-DD)")
    ap.add_argument("--scan-only", action="store_true", help="scan and report, write nothing")
    args = ap.parse_args()

    src = Path(args.source)
    if not src.is_file():
        print(f"REFUSED — source not found: {src}")
        return 2

    raw = src.read_text(encoding="utf-8", errors="replace")

    hits = scan(raw, BANDS)
    if hits:
        print("=" * 72)
        print("REFUSED — nothing written. The source contains material that must not")
        print("be published. Fix the source, do not fix the output.")
        print("=" * 72)
        for band, label, line, snippet in hits:
            print(f"  [{band}] line {line}: {label}")
            print(f"      {snippet}")
        print(f"\n{len(hits)} finding(s). Exit 2.")
        return 2

    body, notes = strip_machine_sections(raw)

    post_hits = scan(body, BANDS)
    if post_hits:
        print("REFUSED — findings appeared after stripping. Exit 2.")
        for band, label, line, snippet in post_hits:
            print(f"  [{band}] line {line}: {label}\n      {snippet}")
        return 2

    date = coverage_saturday(raw, args.date)
    flags = scan(body, [("REVIEW", FLAGS)])

    print(f"scan clean — 0 refusal findings")
    for n in notes:
        print(f"  · {n}")
    print(f"  · as_of resolved to {date.isoformat()} ({date.strftime('%A')})")

    if args.scan_only:
        print("\n--scan-only: nothing written.")
    else:
        out = Path(args.repo) / "content" / "briefs" / f"{date.isoformat()}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            print(f"\nREFUSED — {out} already exists. Delete it or pass --date. Exit 2.")
            return 2
        out.write_text(build_front_matter(date) + body, encoding="utf-8")
        print(f"\nstaged: {out}  (draft: true)")

    if flags:
        by_line = {}
        for _, label, line, snippet in flags:
            entry = by_line.setdefault(line, {"snippet": snippet, "labels": []})
            if label not in entry["labels"]:
                entry["labels"].append(label)
        print(f"\n{len(by_line)} line(s) to verify before clearing the draft:")
        for line in sorted(by_line):
            entry = by_line[line]
            print(f"  line {line}: {'; '.join(entry['labels'])}")
            print(f"      {entry['snippet']}")

    print(
        "\nnext:\n"
        "  1. verify every flagged figure against a primary source\n"
        "  2. write the hook and the summary line\n"
        "  3. reframe discovery items as: ticker · mechanism · the question · falsifier · tier\n"
        "  4. confirm the gaps list survived\n"
        "  5. set draft: false, then commit\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
