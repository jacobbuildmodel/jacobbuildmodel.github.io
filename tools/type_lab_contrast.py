"""tools/type_lab_contrast.py -- WCAG 2 contrast ratios for the light-theme
proposal in assets/css/extended/zz-type-lab.css (type lab, draft PR 64).

    python tools/type_lab_contrast.py

Prints every text colour against every background it sits on, for the
current light theme and the proposal, and exits 1 if any text pair in the
proposal is under 4.5:1. Formula: WCAG 2.2, relative luminance and
(L1 + 0.05) / (L2 + 0.05).
"""
import sys


def lum(h):
    h = h.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


CURRENT = {"paper": "#ffffff", "surface": "#ffffff", "code-bg": "#f4f7f9",
           "ink": "#15191e", "ink-2": "#3f4852", "ink-3": "#5f6873",
           "line": "#c5ccd4", "accent": "#3d6c8c", "navy-text": "#1f3a5f",
           "pos": "#2E7D5B", "neg": "#8A6116", "fig-subject": "#a32a1e",
           "lr-accent": "#c2410c", "content": "#1f1f1f"}
# The proposal changes seven tokens; every other colour is as it is today.
PROPOSED = dict(CURRENT, **{"paper": "#f6f3ec", "code-bg": "#fdfcf9",
                            "ink": "#1b1f24", "ink-3": "#59616b",
                            "line": "#b3ab9b", "accent": "#35627f",
                            "pos": "#2a7354"})
# "content" is the theme's own colour for article prose (PaperMod --content).
TEXT = ["ink", "content", "ink-2", "ink-3", "accent", "navy-text", "pos", "neg",
        "fig-subject", "lr-accent"]
GROUNDS = ["paper", "surface", "code-bg"]

bad = 0
for label, t in (("current", CURRENT), ("proposed", PROPOSED)):
    print(label)
    print("  %-12s %-8s" % ("token", "hex") + "".join("%-18s" % ("on " + g + " " + t[g]) for g in GROUNDS))
    for k in TEXT:
        cells = []
        for g in GROUNDS:
            r = ratio(t[k], t[g])
            if label == "proposed" and r < 4.5:
                bad += 1
            cells.append("%-18s" % ("%.2f" % r))
        print("  %-12s %-8s" % (k, t[k]) + "".join(cells))
    print("  line %s on paper %.2f, on surface %.2f (borders, not text)"
          % (t["line"], ratio(t["line"], t["paper"]), ratio(t["line"], t["surface"])))
    print("  paper against surface %.2f" % ratio(t["paper"], t["surface"]))
sys.exit(1 if bad else 0)
