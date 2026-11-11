"""tools/type_lab_shots.py -- phone screenshots and comparison sheets for the
type lab (draft pull request 64).

Needs a local build with drafts served on port 1323:
    hugo --buildDrafts --buildFuture --baseURL http://localhost:1323/ -d <dir>
    python -m http.server 1323 --bind 127.0.0.1      (run inside <dir>)
and Chrome or Edge, and Pillow.

    python tools/type_lab_shots.py shots <dir>   full-page captures, 390px wide
    python tools/type_lab_shots.py sheets    crops and side-by-side sheets

Captures are made by the browser itself in headless mode (--screenshot) at
twice the pixel density. A headless window on Windows cannot be narrower
than about 500px, so each page is loaded in a frame exactly 390 CSS px wide
and 5200 tall (a frame page written into <dir> for the run and removed after
it), and the picture is cut to the frame. The same frame page reports where
the title, first section heading and count sit, and which faces loaded; the
views are cut from the picture at those positions. The option is given in the address
(?type=b&paper=b&head=u&theme=dark), which the lab script in extend_head.html
reads. Output: office/type-lab/shots/.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

BASE = "http://localhost:1323"
OUT = "office/type-lab/shots"
RAW = os.path.join(tempfile.gettempdir(), "nvd_type_lab_raw")
W, SCALE, TALL = 390, 2, 5200
VIEW_H = 844   # one phone screen, CSS px
BROWSERS = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "/usr/bin/google-chrome", "/usr/bin/chromium"]
ARTICLE = "/economics/2026-10-31/"
SCORE = "/scorecard/"
TYPES = [("a", "A  Source Serif 4 + Source Sans 3 (now)"),
         ("b", "B  Newsreader + Inter + JetBrains Mono digits"),
         ("c", "C  Playfair Display + Lato")]
HEADS = [("k", "1  Label line + rule (default)"), ("u", "2  Rule under"),
         ("o", "3  Rule over")]


def browser():
    for b in BROWSERS:
        if os.path.exists(b):
            return b
    sys.exit("no Chrome or Edge found")


def url(path, type_="a", paper="a", head="k", theme="light"):
    return "%s%s?type=%s&paper=%s&head=%s&theme=%s" % (BASE, path, type_, paper, head, theme)


def name(page, type_="a", paper="a", head="k", theme="light"):
    return "%s_type-%s_paper-%s_head-%s_%s" % (page, type_, paper, head, theme)


def jobs():
    out = []
    for t, _ in TYPES:
        out.append(("article", ARTICLE, dict(type_=t)))
        out.append(("scorecard", SCORE, dict(type_=t)))
        out.append(("article", ARTICLE, dict(type_=t, theme="dark")))
        out.append(("article", ARTICLE, dict(type_=t, paper="b")))
        out.append(("scorecard", SCORE, dict(type_=t, paper="b")))
    for h, _ in HEADS:
        for theme in ("light", "dark"):
            out.append(("article", ARTICLE, dict(head=h, theme=theme)))
    for page, path in (("process", "/process/"), ("about", "/about/"), ("home", "/"), ("economics", "/economics/"),
                       ("lab", "/lab/typefaces/")):
        out.append((page, path, {}))
    out.append(("scorecard", SCORE, dict(theme="dark")))
    seen, uniq = set(), []
    for page, path, kw in out:
        n = name(page, **kw)
        if n not in seen:
            seen.add(n)
            uniq.append((n, url(path, **kw)))
    return uniq


PROBE = """<!doctype html><meta charset="utf-8"><title>probe</title>
<body style="margin:0"><iframe id="f" style="display:block;width:%dpx;height:%dpx;border:0"></iframe><pre id="out" style="display:none"></pre>
<script>
var f = document.getElementById("f");
f.onload = async function () {
  var d = f.contentDocument, w = f.contentWindow;
  await d.fonts.ready;
  await new Promise(function (r) { setTimeout(r, 400); });
  await d.fonts.ready;
  function box(sel) { var e = d.querySelector(sel); return e ? e.getBoundingClientRect() : null; }
  function top(sel) { var b = box(sel); return b ? Math.round(b.top + w.scrollY) : null; }
  function bottom(sel) { var b = box(sel); return b ? Math.round(b.bottom + w.scrollY) : null; }
  function face(sel) { var e = d.querySelector(sel); if (!e) return null; var c = w.getComputedStyle(e);
    return c.fontFamily.split(",")[0] + " " + c.fontSize + "/" + c.lineHeight + " " + c.fontWeight; }
  var loaded = [];
  d.fonts.forEach(function (x) { if (x.status === "loaded") loaded.push(x.family + " " + x.weight + " " + x.style); });
  document.getElementById("out").textContent = "PROBE" + JSON.stringify({
    "title": top(".post-title"), "lead_bottom": bottom(".entry-lead"),
    "h2": top(".post-content h2"), "count": top("#the-count"),
    "band": Math.round(box(".header").height), "overflow": d.documentElement.scrollWidth - w.innerWidth,
    "faces": {"title": face(".post-title"), "lead": face(".entry-lead"), "h2": face(".post-content h2"),
              "h3": face(".post-content h3"), "p": face(".post-content > p"), "td": face(".post-content td"),
              "strip": face(".method-strip-item"), "nav": face(".header .menu a"), "meta": face(".post-meta")},
    "loaded": loaded.sort()}) + "PROBE";
};
f.src = decodeURIComponent(location.search.slice(1));
</script>"""


def shots(served):
    os.makedirs(RAW, exist_ok=True)
    with open(os.path.join(served, "lab-probe.html"), "w", encoding="ascii") as fh:
        fh.write(PROBE % (W, TALL))
    exe = browser()
    pos = {}
    for n, u in jobs():
        png = os.path.join(RAW, n + ".png")
        common = [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                  "--user-data-dir=" + tempfile.mkdtemp(prefix="nvd_lab_prof_"),
                  "--virtual-time-budget=8000"]
        from urllib.parse import quote
        frame = BASE + "/lab-probe.html?" + quote(u, safe="")
        dom = subprocess.run(common + ["--window-size=800,%d" % TALL, "--dump-dom", frame],
                             check=True, capture_output=True, timeout=120).stdout.decode("utf-8", "replace")
        pos[n] = json.loads(dom.split("PROBE")[1].replace("&amp;", "&").replace("&quot;", '"'))
        subprocess.run(common + ["--force-device-scale-factor=%d" % SCALE,
                                 "--window-size=800,%d" % TALL, "--screenshot=" + png, frame],
                       check=True, capture_output=True, timeout=120)
        Image.open(png).convert("RGB").crop((0, 0, W * SCALE, TALL * SCALE)).save(png)
        print("shot", n, Image.open(png).size, {k: v for k, v in pos[n].items() if k not in ("faces", "loaded")})
    json.dump(pos, open(os.path.join(RAW, "positions.json"), "w"), indent=1)
    os.remove(os.path.join(served, "lab-probe.html"))


def font(size, bold=False):
    for f in (("segoeuib.ttf" if bold else "segoeui.ttf"), "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


def crop(n, top_css, height_css=VIEW_H):
    img = Image.open(os.path.join(RAW, n + ".png")).convert("RGB")
    top = max(0, int(top_css * SCALE))
    return img.crop((0, top, W * SCALE, min(img.size[1], top + height_css * SCALE)))


def save(im, path):
    """PNG with a 256-colour palette: a third of the bytes, and text on flat
    grounds loses nothing the eye can see."""
    im.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(path, optimize=True)


def sheet(cols, title, out, bg=(255, 255, 255), fg=(21, 25, 30)):
    """cols: list of (label, image). One row, labelled, full resolution."""
    pad, head, lab = 24, 64, 56
    h = max(im.size[1] for _, im in cols)
    w = sum(im.size[0] for _, im in cols) + pad * (len(cols) + 1)
    page = Image.new("RGB", (w, head + lab + h + pad), bg)
    d = ImageDraw.Draw(page)
    d.text((pad, 16), title, font=font(30, True), fill=fg)
    x = pad
    for label, im in cols:
        d.text((x, head + 10), label, font=font(24, True), fill=fg)
        page.paste(im, (x, head + lab))
        d.rectangle((x - 1, head + lab - 1, x + im.size[0], head + lab + im.size[1]), outline=(150, 150, 150))
        x += im.size[0] + pad
    save(page, os.path.join(OUT, out))
    print("wrote", out, page.size)


def stack(rows, out):
    w = max(r.size[0] for r in rows)
    page = Image.new("RGB", (w, sum(r.size[1] for r in rows)), (255, 255, 255))
    y = 0
    for r in rows:
        page.paste(r, (0, y))
        y += r.size[1]
    save(page, os.path.join(OUT, out))
    print("wrote", out, page.size)


def sheets():
    os.makedirs(OUT, exist_ok=True)
    pos = json.load(open(os.path.join(RAW, "positions.json")))

    def top(n, key):
        p = pos[n]
        return {"a-top": 0, "b-section": p["h2"] - 170, "c-count": (p["count"] or 0) - 70}[key]

    def view(n, key, h=VIEW_H):
        im = crop(n, top(n, key), h)
        save(im, os.path.join(OUT, "%s_%s.png" % (key, n)))
        return im

    # the three typefaces, three views, light
    for key, title in (("a-top", "View (a): top of the article, phone width 390"),
                       ("b-section", "View (b): first section heading and text, phone width 390"),
                       ("c-count", "View (c): the scorecard count, phone width 390")):
        page = "scorecard" if key == "c-count" else "article"
        cols = [(label, view(name(page, type_=t), key)) for t, label in TYPES]
        sheet(cols, title, "compare_%s_A-B-C.png" % key)
    # the heading candidates, light over dark
    rows = []
    for theme in ("light", "dark"):
        cols = [(label, view(name("article", head=h, theme=theme), "b-section", 620))
                for h, label in HEADS]
        tmp = "tmp_heads_%s.png" % theme
        sheet(cols, "Section heading candidates, %s theme, phone width 390" % theme, tmp)
        rows.append(Image.open(os.path.join(OUT, tmp)))
    stack(rows, "compare_heading-marks_light-dark.png")
    for theme in ("light", "dark"):
        os.remove(os.path.join(OUT, "tmp_heads_%s.png" % theme))
    # theme and paper for each typeface: current white, proposed warm, dark
    for t, label in TYPES:
        cols = [("White page (now)", view(name("article", type_=t), "a-top")),
                ("Warm page (proposed)", view(name("article", type_=t, paper="b"), "a-top")),
                ("Dark (unchanged)", view(name("article", type_=t, theme="dark"), "a-top"))]
        sheet(cols, "Option %s: page colours, phone width 390" % label, "compare_paper_type-%s.png" % t)
    cols = [("White page (now)", view(name("scorecard"), "c-count")),
            ("Warm page (proposed)", view(name("scorecard", paper="b"), "c-count"))]
    sheet(cols, "Scorecard count: page colours, option A", "compare_paper_scorecard.png")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "shots":
        shots(sys.argv[2])
    elif cmd == "sheets":
        sheets()
    else:
        sys.exit(__doc__)
