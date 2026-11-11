"""tools/make_type_lab_fonts.py -- numbers and one subset for the type lab.

The type lab (draft pull request 64) compares three typeface options. The
candidate files in static/fonts/lab/ are the Latin subsets published by
Fontsource (version 5.3.0 of each package, served by jsDelivr), unchanged,
except one: the digits 0 to 9 of JetBrains Mono, cut out here so that option
B does not ship 21 KB of a monospace face per weight to draw ten glyphs.

Usage (needs fontTools and brotli: pip install fonttools brotli):
    python tools/make_type_lab_fonts.py digits <JetBrains Mono latin woff2> 400
    python tools/make_type_lab_fonts.py digits <JetBrains Mono latin woff2> 700
        writes static/fonts/lab/jetbrains-mono-digits-400.woff2 and -700
    python tools/make_type_lab_fonts.py metrics
        prints, for every face, the x-height, the average letter width and
        the size-adjust and override values used in static/fonts/lab/*.css
    python tools/make_type_lab_fonts.py csv
        rewrites the bytes and sha256 columns of office/type-lab/FONTS.csv

Method for the numbers (the same idea as 00-tokens.css, Capsize):
  size-adjust of a lab face  = chosen, so its x-height is close to the
                               current face's (NVD Serif 0.475, NVD Sans 0.486)
  ascent- and descent-override of a lab face
                             = the current face's hhea ascent and descent
                               divided by that size-adjust, so every line box
                               is built exactly as it is today
  size-adjust of a fallback  = lab face's average letter width x its
                               size-adjust / the fallback's average width
The average width is weighted by English letter frequency, space included.
"""
import csv, hashlib, os, sys
from fontTools import subset
from fontTools.ttLib import TTFont

LAB = "static/fonts/lab"
CSV = "office/type-lab/FONTS.csv"
FREQ = {" ": 18.3, "e": 10.2, "t": 7.5, "a": 6.5, "o": 6.2, "n": 5.7, "i": 5.7,
        "s": 5.3, "r": 5.0, "h": 5.0, "l": 3.3, "d": 3.3, "u": 2.3, "c": 2.2,
        "m": 2.0, "f": 2.0, "w": 1.7, "g": 1.6, "p": 1.5, "y": 1.4, "b": 1.3,
        "v": 0.8, "k": 0.6, "x": 0.14, "j": 0.12, "q": 0.08, "z": 0.06}
SERIF = (1.036, 0.335)   # NVD Serif hhea ascent, descent per em
SANS = (1.000, 0.326)    # NVD Sans
# face file, size-adjust, line metrics to copy, fallback file
FACES = [
    ("newsreader-latin-400-normal.woff2", 1.08, SERIF, "georgia.ttf"),
    ("newsreader-latin-600-normal.woff2", 1.08, SERIF, "georgia.ttf"),
    ("inter-latin-400-normal.woff2", 0.90, SANS, "arial.ttf"),
    ("jetbrains-mono-digits-400.woff2", 0.90, SANS, None),
    ("lato-latin-400-normal.woff2", 0.96, SANS, "arial.ttf"),
    ("playfair-display-latin-700-normal.woff2", 0.95, SERIF, "georgia.ttf"),
]


def measure(path):
    f = TTFont(path, lazy=True)
    upm = f["head"].unitsPerEm
    cmap, hmtx = f.getBestCmap(), f["hmtx"]
    have = {c: w for c, w in FREQ.items() if ord(c) in cmap}
    avg = (sum(hmtx[cmap[ord(c)]][0] * w for c, w in have.items())
           / sum(have.values()) / upm) if have else 0.0
    return f["OS/2"].sxHeight / upm, avg


def digits(src, weight):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = []
    font = TTFont(src, recalcTimestamp=False)
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=subset.parse_unicodes("U+0030-0039"))
    sub.subset(font)
    out = os.path.join(LAB, "jetbrains-mono-digits-%s.woff2" % weight)
    font.save(out)
    print("wrote", out, os.path.getsize(out), "bytes")


def metrics():
    win = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts")
    for name, adj, (asc, desc), fb in FACES:
        xh, avg = measure(os.path.join(LAB, name))
        print("%s\n  x-height %.3f, shown %.3f; average width %.4f, shown %.4f"
              % (name, xh, xh * adj, avg, avg * adj))
        print("  size-adjust %.2f%%; ascent-override %.2f%%; descent-override %.2f%%"
              % (adj * 100, asc / adj * 100, desc / adj * 100))
        if fb and os.path.exists(os.path.join(win, fb)):
            _, favg = measure(os.path.join(win, fb))
            f = avg * adj / favg
            print("  fallback %s: size-adjust %.2f%%; ascent-override %.2f%%; "
                  "descent-override %.2f%%" % (fb, f * 100, asc / f * 100, desc / f * 100))


def rewrite_csv():
    with open(CSV, newline="", encoding="ascii") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        p = os.path.join("static/fonts" if r["option"] == "A" else LAB, r["file"])
        data = open(p, "rb").read()
        r["bytes"] = str(len(data))
        r["sha256"] = hashlib.sha256(data).hexdigest()
    with open(CSV, "w", newline="", encoding="ascii") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("rewrote", CSV, len(rows), "rows")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "digits":
        digits(sys.argv[2], sys.argv[3])
    elif cmd == "metrics":
        metrics()
    elif cmd == "csv":
        rewrite_csv()
    else:
        sys.exit(__doc__)
