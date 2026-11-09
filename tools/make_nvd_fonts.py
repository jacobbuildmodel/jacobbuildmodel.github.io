"""tools/make_nvd_fonts.py -- the site's web fonts, NVD Serif and NVD Sans.

Subsets Adobe's Source Serif 4 (4.005) and Source Sans 3 (3.052) TTFs from
research/paper-template/fonts/ and renames the families. Under the SIL Open
Font License 1.1 a subset is a Modified Version, and a Modified Version may
not use the Reserved Font Name "Source" (front page PR A, fix round 1,
5 November 2026). The copyright, trademark and licence records are kept as
they are; the description record says what the file is. The script stops if
any other name record still says "Source".

Usage (needs fontTools and brotli: pip install fonttools brotli):
    python tools/make_nvd_fonts.py research/paper-template/fonts static/fonts

Writes NVDSerif-Regular, NVDSerif-It, NVDSerif-Semibold, NVDSans-Regular and
NVDSans-Semibold (.woff2). The licences stay in static/fonts/*-LICENSE.md.
"""
import sys, os
from fontTools import subset
from fontTools.ttLib import TTFont

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
FILES = {  # source TTF -> shipped WOFF2
    "SourceSerif4-Regular": "NVDSerif-Regular",
    "SourceSerif4-It": "NVDSerif-It",
    "SourceSerif4-Semibold": "NVDSerif-Semibold",
    "SourceSans3-Regular": "NVDSans-Regular",
    "SourceSans3-Semibold": "NVDSans-Semibold",
}
UNICODES = ("U+0000-00FF,U+0131,U+0152-0153,U+2000-206F,U+2074,U+20AC,"
            "U+2122,U+2190-2193,U+2212,U+2215,U+25CF,U+FEFF,U+FFFD")
FEATURES = ["kern", "liga", "lnum", "onum", "pnum", "tnum"]
RENAME = [("Source Serif 4", "NVD Serif"), ("SourceSerif4", "NVDSerif"),
          ("Source Sans 3", "NVD Sans"), ("SourceSans3", "NVDSans")]
KEEP_AS_IS = {0, 7, 8, 9, 11, 12, 13, 14}   # copyright, trademark, maker, designer, URLs, licence
NOTE = ("NVD Serif and NVD Sans are modified (subsetted) versions of Source Serif 4 "
        "and Source Sans 3 by Adobe, renamed under the SIL Open Font License 1.1 "
        "because a Modified Version may not use the Reserved Font Name \"Source\".")

opts = subset.Options()
opts.flavor = "woff2"
opts.layout_features = FEATURES
opts.name_IDs = ["*"]
opts.name_languages = ["*"]
unicodes = subset.parse_unicodes(UNICODES)

for s, d in FILES.items():
    # recalcTimestamp=False keeps head.modified as Adobe set it, so a rerun
    # writes byte-identical files.
    font = TTFont(os.path.join(src, s + ".ttf"), recalcTimestamp=False)
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=unicodes)
    sub.subset(font)
    name = font["name"]
    for rec in name.names:
        if rec.nameID in KEEP_AS_IS:
            continue
        txt = rec.toUnicode()
        new = txt
        for a, b in RENAME:
            new = new.replace(a, b)
        if new != txt:
            rec.string = new
    # description (ID 10): say what this file is
    for pid, eid, lid in ((3, 1, 0x409), (1, 0, 0)):
        name.setName(NOTE, 10, pid, eid, lid)
    # nothing but the kept notices may still say "Source"
    for rec in name.names:
        if rec.nameID not in KEEP_AS_IS | {10} and "Source" in rec.toUnicode():
            raise SystemExit(f"{d}: name ID {rec.nameID} still says Source: {rec.toUnicode()!r}")
    path = os.path.join(out, d + ".woff2")
    font.flavor = "woff2"
    font.save(path)
    print(f"{d}.woff2 {os.path.getsize(path)} B  family={name.getDebugName(1)!r} "
          f"full={name.getDebugName(4)!r} ps={name.getDebugName(6)!r} "
          f"typo={name.getDebugName(16)!r}/{name.getDebugName(17)!r}")
