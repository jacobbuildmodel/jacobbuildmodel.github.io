#!/usr/bin/env python3
"""
portfolio_pdf.py -- the one-page portfolio PDF, made from content/about.md.

Usage (from the repo root):
    python tools/portfolio_pdf.py                      # dated today
    python tools/portfolio_pdf.py --date 2026-11-04    # a given date

Writes static/portfolio/Jacob-Ong-portfolio-YYYY-MM.pdf, served at
/portfolio/Jacob-Ong-portfolio-YYYY-MM.pdf. Rerun it whenever content/about.md
changes (for example once the email address replaces EMAIL_TO_CONFIRM), so the
PDF and the page keep the same text.

The PDF is the About page's own text, with four mechanical changes only:
  - front matter dropped;
  - {{< age >}} replaced by the age on --date, computed as
    layouts/shortcodes/age.html computes it;
  - the page's line linking to this PDF dropped (it would point at itself);
  - root-relative links (/scorecard/) made absolute, so they work in a PDF.
It fails, writing nothing, if the result is longer than one page, or if the
text holds an em dash, U+2212 or U+00D7.

Needs pandoc (3.1.3 used) and Typst (0.13.1 used) on PATH, or pass --pandoc
and --typst. Layout: tools/portfolio.typ. Fonts: research/paper-template/fonts.
Page count is read with pdfinfo (poppler) when it is installed, otherwise
from the PDF itself.
"""
import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ABOUT = ROOT / "content" / "about.md"
LAYOUT = ROOT / "tools" / "portfolio.typ"
FONTS = ROOT / "research" / "paper-template" / "fonts"
SITE_URL = "https://jacobbuildmodel.github.io"
SITE_NAME = "The New Void Deck"   # hugo.toml title
AUTHOR = "Jacob Ong"              # hugo.toml params.author
BIRTH = dt.date(2004, 6, 10)      # layouts/shortcodes/age.html
BANNED = {"\u2014": "em dash", "\u2212": "U+2212 minus", "\u00d7": "U+00D7 times"}


def age_on(day):
    """Same rule as the age shortcode: one less before the birthday's day of the year."""
    age = day.year - BIRTH.year
    if day.timetuple().tm_yday < BIRTH.timetuple().tm_yday:
        age -= 1
    return age


def page_text(day):
    raw = ABOUT.read_text(encoding="utf-8")
    m = re.match(r"^---\n.*?\n---\n", raw, re.S)
    if not m:
        sys.exit("content/about.md: no front matter found")
    body = raw[m.end():]
    body, n = re.subn(r"\{\{<\s*age\s*>\}\}", str(age_on(day)), body)
    if n != 1:
        sys.exit(f"expected one {{{{< age >}}}} shortcode, found {n}")
    # The page's link to this PDF: one line of its own.
    body, n = re.subn(r"^\[[^\]]*\]\(/portfolio/[^)]*\.pdf\)[^\n]*\n\n?", "", body, flags=re.M)
    if n != 1:
        sys.exit(f"expected one line linking to the PDF, found {n}")
    if "{{" in body:
        sys.exit("a Hugo shortcode is left in the text; teach this script to render it")
    body = re.sub(r"\]\((/[^)]*)\)", lambda m: f"]({SITE_URL}{m.group(1)})", body)
    for ch, name in BANNED.items():
        if ch in body:
            sys.exit(f"content/about.md holds an {name}; the site's rules forbid it")
    return body


def pages_in(pdf):
    if shutil.which("pdfinfo"):
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
        return int(re.search(r"^Pages:\s+(\d+)", out, re.M).group(1))
    return len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", pdf.read_bytes()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="date printed on the PDF, YYYY-MM-DD")
    ap.add_argument("--out", help="default: static/portfolio/Jacob-Ong-portfolio-YYYY-MM.pdf")
    ap.add_argument("--pandoc", default="pandoc")
    ap.add_argument("--typst", default="typst")
    a = ap.parse_args()
    day = dt.date.fromisoformat(a.date)
    out = Path(a.out) if a.out else ROOT / "static" / "portfolio" / f"Jacob-Ong-portfolio-{day:%Y-%m}.pdf"

    md = page_text(day)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        body = subprocess.run([a.pandoc, "-f", "markdown", "-t", "typst", "--wrap=none"],
                              input=md, capture_output=True, text=True, check=True).stdout
        for ch, name in BANNED.items():
            if ch in body:
                sys.exit(f"pandoc's output holds an {name}")
        # An included file has its own scope: it imports what pandoc's output calls.
        (tmp / "body.typ").write_text('#import "portfolio.typ": blockquote, horizontalrule\n' + body,
                                      encoding="utf-8")
        shutil.copy(LAYOUT, tmp / "portfolio.typ")
        when = f"{day.day} {day:%B %Y}"
        (tmp / "main.typ").write_text(
            '#import "portfolio.typ": *\n'
            f'#show: portfolio.with(name: "{AUTHOR}", site: "{SITE_NAME}", url: "{SITE_URL}/",\n'
            f'  date: "{when}", day: datetime(year: {day.year}, month: {day.month}, day: {day.day}))\n'
            '#include "body.typ"\n', encoding="utf-8")
        pdf = tmp / "portfolio.pdf"
        subprocess.run([a.typst, "compile", "--font-path", str(FONTS), "--ignore-system-fonts",
                        str(tmp / "main.typ"), str(pdf)], check=True)
        n = pages_in(pdf)
        if n != 1:
            sys.exit(f"the PDF runs to {n} pages, not one; nothing written")
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(pdf, out)
    print(f"wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} (1 page, dated {when})")


if __name__ == "__main__":
    main()
