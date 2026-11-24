#!/usr/bin/env python3
"""tools/make_covers.py -- a cover and a share-card base for each project, drawn by
code from the project's own published series. No illustration, no AI image.

    python tools/make_covers.py --coe <coe-analysis clone> --hdb <hdb-affordability clone>
                                --gst <gst-passthrough clone>

Each cover is a ridgeline: a stack of thin lines, the newest in red.
  kind "dist"  one ridge per year: the spread of that year's values (a Gaussian
               kernel density, bandwidth 0.45 of the year's standard deviation,
               each ridge scaled to its own peak)
  kind "path"  one ridge per year or per group: the values in order, each ridge
               scaled to its own lowest and highest value
A cover is a picture of the data's shape, not a chart: it has no axes and a
ridge's height cannot be read off it. The charts in each article carry the
numbers.

Every series is read with "git show <commit>:<file>" from a clone of the
analysis repository, at the commit named in COVERS below, so a cover can be
redrawn from the same bytes. Nothing is read from an open question's folder.

Writes, for each project:
  assets/covers/<page>.svg   the cover, 1200 x 300, inline-able: lines take the
                             page's text colour (layouts/partials/cover.html)
  assets/covers/<page>.png   1200 x 630 share-card base: paper, the ridges in
                             the lower half, the top left clear for the title
                             (layouts/partials/share_card.html)
and data/covers.yaml: the series, source, dates, file and commit behind each,
which the page prints as the cover's credit line.
Needs numpy and Pillow. Pure ASCII output files.
"""
import argparse
import csv
import io
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "covers"
DATA = ROOT / "data" / "covers.yaml"
PAPER, INK, RED = "#f6f3ec", "#1b1f24", "#9b2d20"   # --paper and --ink of 00-tokens.css; the ground-line red
W, H_SVG, H_PNG, BAND_TOP = 1200, 300, 630, 310
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]

COE = ("coe", "7acce31a266433f276928042f6119e72f3a9cf0c")
HDB = ("hdb", "bc3545b93e861bd4ab998333630b2b2bee097381")
GST = ("gst", "998568b947a96312183e03cb56d7caf54d097b16")
REPO = {"coe": "coe-analysis", "hdb": "hdb-affordability", "gst": "gst-passthrough"}


def read(repos, where, path):
    key, commit = where
    raw = subprocess.run(["git", "-C", str(repos[key]), "show", f"{commit}:{path}"],
                         check=True, capture_output=True).stdout.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(raw)))


def month_name(ym):
    y, m = ym.split("-")[:2]
    return f"{MONTHS[int(m) - 1]} {y}"


def by_year(pairs):
    out = {}
    for year, v in pairs:
        out.setdefault(year, []).append(v)
    return [(str(y), out[y]) for y in sorted(out)]


# ---- the series: each returns (ridges, dates) with ridges = [(label, [values])] ----

def coe_rows(repos, cat):
    return [r for r in read(repos, COE, "analysis.csv") if r["cat"] == cat]


def coe_dates(rows):
    return f"{month_name(rows[0]['month'])} to {month_name(rows[-1]['month'])}"


def coe_premium(repos, cat):
    rows = coe_rows(repos, cat)
    return by_year((int(r["year"]), float(r["premium"])) for r in rows), coe_dates(rows)


def coe_winrate(repos):
    rows = coe_rows(repos, "A")
    return by_year((int(r["year"]), float(r["bids_success"]) / float(r["bids_received"])) for r in rows), coe_dates(rows)


def coe_round_gap(repos):
    rows = coe_rows(repos, "A")
    first = {r["month"]: float(r["premium"]) for r in rows if r["bidding_no"] == "1"}
    pairs = [(int(r["year"]), float(r["premium"]) / first[r["month"]] - 1.0)
             for r in rows if r["bidding_no"] == "2" and r["month"] in first]
    return by_year(pairs), coe_dates(rows)


def gst_cpi(repos):
    row = next(r for r in read(repos, GST, "raw/cpi_2024base_monthly.csv") if r["DataSeries"].strip() == "All Items")
    abbr = {m[:3]: i + 1 for i, m in enumerate(MONTHS)}
    level = {}
    for k, v in row.items():
        if k != "DataSeries" and v not in ("", "na"):
            level[(int(k[:4]), abbr[k[4:7]])] = float(v)
    keys = sorted(level)
    change = {k: level[k] / level[p] - 1.0 for p, k in zip(keys, keys[1:])}
    years = sorted({y for y, _ in change if y >= 2010 and all((y, m) in change for m in range(1, 13))})
    ridges = [(str(y), [change[(y, m)] for m in range(1, 13)]) for y in years]
    return ridges, f"January {years[0]} to December {years[-1]}"


def hdb_years(repos):
    rows = read(repos, HDB, "out/affordability.csv")
    buyers = sorted({r["buyer"] for r in rows})
    ridges = [(b, [float(r["price_to_income_years"]) for r in sorted(rows, key=lambda r: int(r["year"])) if r["buyer"] == b])
              for b in buyers]
    years = sorted(int(r["year"]) for r in rows)
    return ridges, f"{years[0]} to {years[-1]}"


def hdb_sora(repos):
    rows = [r for r in read(repos, HDB, "financing/out/rates_monthly.csv") if r["sora3m"] not in ("", "nan")]
    count = {}
    for r in rows:
        count[r["month"][:4]] = count.get(r["month"][:4], 0) + 1
    rows = [r for r in rows if count[r["month"][:4]] == 12]
    return by_year((int(r["month"][:4]), float(r["sora3m"])) for r in rows), f"{month_name(rows[0]['month'])} to {month_name(rows[-1]['month'])}"


def erp_speeds(repos):
    rows = read(repos, COE, "erp/out/annual.csv")
    ridges = [(c, [float(r[c]) for r in rows if r[c] not in ("", "nan")]) for c in ("speed_expressway", "speed_arterial")]
    years = [int(r["year"]) for r in rows if r["speed_expressway"] not in ("", "nan")]
    return ridges, f"{min(years)} to {max(years)}"


def pwm_groups(repos):
    rows = read(repos, COE, "pwm/out/group_values.csv")
    groups = ["C", "cleaning", "security", "landscape"]
    ridges = [(g, [float(r["value"]) for r in sorted(rows, key=lambda r: int(r["june"])) if r["group"] == g]) for g in groups]
    years = sorted(int(r["june"]) for r in rows)
    return ridges, f"June {years[0]} to June {years[-1]}"


def sgd_neer(repos):
    rows = [r for r in read(repos, COE, "sgd/out/neer.csv") if r["period"] >= "2005-01"]
    areas = sorted({r["area"] for r in rows}, key=lambda a: (a == "SG", a))   # Singapore last, in red
    ridges = [(a, [float(r["value"]) for r in sorted(rows, key=lambda r: r["period"]) if r["area"] == a]) for a in areas]
    periods = sorted(r["period"] for r in rows)
    return ridges, f"{month_name(periods[0])} to {month_name(periods[-1])}"


LTA = "Land Transport Authority via data.gov.sg"
COVERS = [
    # page, kind, where, file, loader, series (as the credit line names it), source
    ("2026-08-22", "dist", COE, "analysis.csv", lambda r: coe_premium(r, "A"),
     "the Category A COE premium at every bidding exercise, one ridge a year", LTA),
    ("2026-08-29", "dist", COE, "analysis.csv", coe_round_gap,
     "the change in the Category A COE premium from each month's first exercise to its second, one ridge a year", LTA),
    ("2026-09-05", "dist", COE, "analysis.csv", coe_winrate,
     "the share of Category A COE bids that won at every bidding exercise, one ridge a year", LTA),
    ("2026-09-12", "dist", COE, "analysis.csv", lambda r: coe_premium(r, "D"),
     "the motorcycle (Category D) COE premium at every bidding exercise, one ridge a year", LTA),
    ("2026-09-08", "path", GST, "raw/cpi_2024base_monthly.csv", gst_cpi,
     "the month-on-month change in the Consumer Price Index (All Items), one ridge a year", "Department of Statistics Singapore via data.gov.sg"),
    ("2026-09-19", "path", HDB, "out/affordability.csv", hdb_years,
     "the years of household income a four-room resale flat cost, one ridge each for buyers at the 20th, 50th and 80th percentiles of household income", "HDB and the Department of Statistics Singapore via data.gov.sg"),
    ("2026-10-03", "dist", HDB, "financing/out/rates_monthly.csv", hdb_sora,
     "the monthly benchmark interest rate used in the analysis (3-month compounded SORA), one ridge a year", "Monetary Authority of Singapore via data.gov.sg"),
    ("2026-10-17", "path", COE, "erp/out/annual.csv", erp_speeds,
     "average peak-hour speeds on expressways and on arterial roads, one ridge each", LTA),
    ("2026-10-31", "path", COE, "pwm/out/group_values.csv", pwm_groups,
     "bottom pay each June in the comparison jobs and in cleaning, security and landscape work, one ridge each", "Ministry of Manpower, Occupational Wage Survey"),
    ("2026-11-14", "path", COE, "sgd/out/neer.csv", sgd_neer,
     "the trade-weighted exchange rate index of each currency in the analysis, the Singapore dollar last, one ridge each", "Bank for International Settlements"),
]


# ---- drawing ----

def curve(kind, values, lo, hi, n=150):
    """Heights in 0..1 at n evenly spaced x positions."""
    v = np.asarray(values, dtype=float)
    if kind == "dist":
        xs = np.linspace(lo, hi, n)
        bw = 0.45 * (v.std(ddof=1) if len(v) > 1 and v.std(ddof=1) > 0 else (hi - lo) / 50.0)
        y = np.exp(-0.5 * ((xs[:, None] - v[None, :]) / bw) ** 2).sum(axis=1)
        return y / y.max()
    span = v.max() - v.min()
    y = (v - v.min()) / span if span > 0 else np.full(len(v), 0.5)
    return np.interp(np.linspace(0, len(v) - 1, n), np.arange(len(v)), y)


def layout(ridges, kind, height):
    """Polylines [(x, y)] per ridge and each baseline, in a W x height box."""
    ridges = [r for r in ridges if len(r[1]) >= 3]
    allv = np.concatenate([np.asarray(v, dtype=float) for _, v in ridges])
    pad = (allv.max() - allv.min()) * 0.06
    lo, hi = allv.min() - pad, allv.max() + pad
    k = len(ridges)
    amp = min(120.0, 2.6 * (height - 34) / (k - 1 + 2.6)) if k > 1 else 120.0
    step = (height - 34 - amp) / (k - 1) if k > 1 else 0.0
    xs = np.linspace(0, W, 150)
    out = []
    for i, (_, v) in enumerate(ridges):
        base = 22 + amp + i * step
        ys = base - curve(kind, v, lo, hi) * amp
        out.append(([(float(x), float(y)) for x, y in zip(xs, ys)], base))
    return out


def svg(lines):
    parts = ['<svg class="cover-art" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" aria-hidden="true" focusable="false">' % (W, H_SVG)]
    for i, (pts, base) in enumerate(lines):
        # The path starts and ends outside the picture, so its closing edges are never drawn.
        d = ("M-20 %.1fL-20 %.1f" % (base, pts[0][1]) + "".join("L%.1f %.1f" % p for p in pts)
             + "L%d %.1fL%d %.1f" % (W + 20, pts[-1][1], W + 20, base))
        cls = "cover-ridge is-last" if i == len(lines) - 1 else "cover-ridge"
        parts.append('<path class="%s" d="%s"/>' % (cls, d))
    parts.append("</svg>\n")
    return "\n".join(parts)


def png(lines, path):
    s = 2
    img = Image.new("RGB", (W * s, H_PNG * s), PAPER)
    draw = ImageDraw.Draw(img)
    for i, (pts, base) in enumerate(lines):
        poly = [(pts[0][0], base)] + pts + [(pts[-1][0], base)]
        draw.polygon([(x * s, (y + BAND_TOP) * s) for x, y in poly], fill=PAPER)
        draw.line([(x * s, (y + BAND_TOP) * s) for x, y in pts], fill=RED if i == len(lines) - 1 else INK, width=3, joint="curve")
    img.resize((W, H_PNG), Image.LANCZOS).save(path, optimize=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    for k in REPO:
        ap.add_argument(f"--{k}", required=True, help=f"a clone of {REPO[k]}")
    a = ap.parse_args()
    repos = {k: Path(getattr(a, k)) for k in REPO}
    OUT.mkdir(parents=True, exist_ok=True)
    y = ["# The cover of each project: what it was drawn from. WRITTEN BY tools/make_covers.py; do not edit by hand.\n"
         "# The page prints: Cover: drawn by code from <series>, <source>, <dates>. Script in the repository.\n"]
    for page, kind, where, file, loader, series, source in COVERS:
        ridges, dates = loader(repos)
        lines = layout(ridges, kind, H_SVG)
        (OUT / f"{page}.svg").write_text(svg(lines), encoding="ascii", newline="\n")
        png(lines, OUT / f"{page}.png")
        y.append(f'"{page}":\n  series: "{series}"\n  source: "{source}"\n  dates: "{dates}"\n'
                 f'  kind: {kind}\n  ridges: {len(lines)}\n'
                 f'  file: "https://github.com/jacobbuildmodel/{REPO[where[0]]}/blob/{where[1]}/{file}"\n')
        print(f"{page}: {len(lines)} ridges, {dates}")
    text = "".join(y)
    text.encode("ascii")
    DATA.write_text(text, encoding="ascii", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
