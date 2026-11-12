"""tools/type_tools.py -- numbers and pictures for the site's typefaces.

The site's faces since 12 November 2026 (pull request 64): Newsreader,
Inter and the digits of JetBrains Mono, in static/fonts/, declared in
assets/css/extended/00-tokens.css. This script is how the numbers in that
file and in office/type-lab/DESIGN_NOTE.md were made, and how the final
pictures in office/type-lab/shots/ were taken. Run it from the repository
root. Needs fontTools and brotli (metrics, chars, csv, digits) and Pillow
and Chrome or Edge (shots).

    python tools/type_tools.py metrics [<built site>]
        x-height and average letter width of each face, and the size-adjust,
        ascent-, descent- and line-gap-override of its fallback face
        (Georgia for Newsreader, Arial for Inter; read from C:/Windows/Fonts)
    python tools/type_tools.py chars <built site>
        every character above U+007E in the built pages, and whether each
        face has a glyph for it
    python tools/type_tools.py contrast
        WCAG 2 contrast of every light-theme text colour, read from the
        stylesheets, on the page, on a card and on a panel; exit 1 under 4.5
    python tools/type_tools.py csv
        rewrite bytes and sha256 in office/type-lab/FONTS.csv for the files
        that are in static/fonts/
    python tools/type_tools.py digits <JetBrains Mono latin woff2> <400|700>
        cut the digits 0 to 9 into static/fonts/jetbrains-mono-digits-*.woff2
    python tools/type_tools.py serve <built site> <port> [<font delay ms>]
        a local server that forbids caching and can hold every font file
        back, to measure layout shift when the fallback face is drawn first
    python tools/type_tools.py shots <built site> <port> [<scratch folder>]
        phone captures (390 px wide, twice the pixel density) of the page
        types from a build served on <port>; writes the six final_*.png files
        and, into the scratch folder, sheets of every page type for checking

Method for the fallback faces (the Capsize idea, as before):
  size-adjust of the fallback = the web face's average letter width, times
      the web face's own size-adjust, divided by the fallback's average width
  ascent-, descent-override   = the line metrics the web face is given in
      00-tokens.css (1.036 / 0.335 serif, 1.000 / 0.326 sans, per em of
      font-size) divided by the fallback's size-adjust; line gap 0
The average width is taken twice: weighted by English letter frequency
(space included), and, when a built site is given, weighted by every
character of the built pages' visible text. 00-tokens.css uses the second.
"""
import csv, glob, hashlib, html, json, os, re, subprocess, sys, tempfile

FONTS = "static/fonts"
CSV = "office/type-lab/FONTS.csv"
OUT = "office/type-lab/shots"
TOKENS = "assets/css/extended/00-tokens.css"
FREQ = {" ": 18.3, "e": 10.2, "t": 7.5, "a": 6.5, "o": 6.2, "n": 5.7, "i": 5.7,
        "s": 5.3, "r": 5.0, "h": 5.0, "l": 3.3, "d": 3.3, "u": 2.3, "c": 2.2,
        "m": 2.0, "f": 2.0, "w": 1.7, "g": 1.6, "p": 1.5, "y": 1.4, "b": 1.3,
        "v": 0.8, "k": 0.6, "x": 0.14, "j": 0.12, "q": 0.08, "z": 0.06}
SERIF = (1.036, 0.335)   # line metrics given to the serif: ascent, descent per em
SANS = (1.000, 0.326)    # and to the sans
# web face file, its size-adjust, its line metrics, the fallback's file
# (each weight and style has a fallback face of its own: Georgia, Georgia
# Italic, Georgia Bold, Arial, Arial Bold)
FACES = [
    ("newsreader-latin-400-normal.woff2", 1.08, SERIF, "georgia.ttf"),
    ("newsreader-latin-400-italic.woff2", 1.08, SERIF, "georgiai.ttf"),
    ("newsreader-latin-600-normal.woff2", 1.08, SERIF, "georgiab.ttf"),
    ("inter-latin-400-normal.woff2", 0.90, SANS, "arial.ttf"),
    ("inter-latin-600-normal.woff2", 0.90, SANS, "arialbd.ttf"),
    ("jetbrains-mono-digits-400.woff2", 0.90, SANS, None),
]
PAGES = [("home", "/"), ("economics", "/economics/"), ("article", "/economics/2026-10-31/"),
         ("open", None), ("scorecard", "/scorecard/"), ("process", "/process/"),
         ("process-economics", "/process/economics/"), ("about", "/about/"),
         ("decision", "/decisions/lta-coe-categories/"), ("corrections", "/corrections/")]
LIVE = "https://jacobbuildmodel.github.io/economics/2026-10-31/"
W, SCALE, TALL, VIEW_H = 390, 2, 5200, 844
BROWSERS = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "/usr/bin/google-chrome", "/usr/bin/chromium"]


# ---------------------------------------------------------------- text
def visible_text(served):
    """Visible text of every built page, tags, scripts and styles removed."""
    out = []
    for p in glob.glob(os.path.join(served, "**", "*.html"), recursive=True):
        t = open(p, encoding="utf-8", errors="replace").read()
        t = re.sub(r"(?is)<(script|style|svg|head)\b.*?</\1>", " ", t)
        t = html.unescape(re.sub(r"(?s)<[^>]+>", " ", t))
        out.append((p, re.sub(r"\s+", " ", t)))
    return out


def open_page(served):
    for d in sorted(glob.glob(os.path.join(served, "open", "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(d))
        if slug != "page":
            return "/open/%s/" % slug
    sys.exit("no open question page in the build")


# ---------------------------------------------------------------- fonts
def load(path):
    from fontTools.ttLib import TTFont
    f = TTFont(path)
    return f, f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm


def avg_width(font, weights):
    _, cmap, hmtx, upm = font
    have = {c: w for c, w in weights.items() if ord(c) in cmap}
    return sum(hmtx[cmap[ord(c)]][0] * w for c, w in have.items()) / sum(have.values()) / upm


def metrics(served=None):
    win = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts")
    site = {}
    if served:
        for _, t in visible_text(served):
            for ch in t:
                site[ch] = site.get(ch, 0) + 1
        print("built pages: %d characters of visible text" % sum(site.values()))
    for name, adj, (asc, desc), fb in FACES:
        web = load(os.path.join(FONTS, name))
        xh = web[0]["OS/2"].sxHeight / web[3]
        hh = web[0]["hhea"]
        print("%s\n  x-height %.3f, shown %.3f at size-adjust %.0f%%; own hhea %d/%d/%d per %d"
              % (name, xh, xh * adj, adj * 100, hh.ascent, hh.descent, hh.lineGap, web[3]))
        print("  web face: size-adjust %.2f%%; ascent-override %.2f%%; descent-override %.2f%%"
              % (adj * 100, asc / adj * 100, desc / adj * 100))
        if not fb or not os.path.exists(os.path.join(win, fb)):
            continue
        fall = load(os.path.join(win, fb))
        for label, weights in (("letter frequency", FREQ), ("built pages", site)):
            if not weights:
                continue
            both = {c: w for c, w in weights.items() if ord(c) in web[1] and ord(c) in fall[1]}
            a, b = avg_width(web, both), avg_width(fall, both)
            f = a * adj / b
            print("  fallback %s by %s: web %.4f, fallback %.4f -> size-adjust %.2f%%; "
                  "ascent-override %.2f%%; descent-override %.2f%%; line-gap-override 0%%"
                  % (fb, label, a, b, f * 100, asc / f * 100, desc / f * 100))


def chars(served):
    used = {}
    for p, t in visible_text(served):
        for ch in t:
            if ord(ch) > 0x7e:
                used.setdefault(ch, [0, p])[0] += 1
    for p in glob.glob(os.path.join(served, "assets", "css", "*.css")):
        for m in re.finditer(r'content:\s*"\\([0-9a-fA-F]{2,6})', open(p, encoding="utf-8").read()):
            used.setdefault(chr(int(m.group(1), 16)), [0, p + " (content:)"])[0] += 1
    faces = [(n, load(os.path.join(FONTS, n))[1]) for n in sorted(os.listdir(FONTS))
             if n.endswith(".woff2") and "digits" not in n]
    print("characters above U+007E in the build: %d" % len(used))
    for ch in sorted(used):
        miss = [n.split("-latin")[0] + n.split("latin")[1][:-6] for n, cmap in faces if ord(ch) not in cmap]
        print("  U+%04X x%-5d %s%s" % (ord(ch), used[ch][0],
              ("NO GLYPH in " + ", ".join(miss)) if miss else "in every face",
              ("   e.g. " + os.path.relpath(used[ch][1], served)) if miss else ""))


def digits(src, weight):
    from fontTools import subset
    from fontTools.ttLib import TTFont
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = []
    font = TTFont(src, recalcTimestamp=False)
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=subset.parse_unicodes("U+0030-0039"))
    sub.subset(font)
    out = os.path.join(FONTS, "jetbrains-mono-digits-%s.woff2" % weight)
    font.save(out)
    print("wrote", out, os.path.getsize(out), "bytes")


def rewrite_csv():
    with open(CSV, newline="", encoding="ascii") as fh:
        rows = list(csv.DictReader(fh))
    n = 0
    for r in rows:
        p = os.path.join(FONTS, r["file"])
        if os.path.exists(p):
            data = open(p, "rb").read()
            r["bytes"], r["sha256"] = str(len(data)), hashlib.sha256(data).hexdigest()
            n += 1
    with open(CSV, "w", newline="", encoding="ascii") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("rewrote", CSV, "-", n, "of", len(rows), "rows are files in", FONTS)


# ---------------------------------------------------------------- contrast
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


def token(path, name, default=None):
    """First value of a custom property in a stylesheet: the light one."""
    m = re.search(r"--%s:\s*(#[0-9a-fA-F]{6})\b" % re.escape(name), open(path, encoding="utf-8").read())
    if m:
        return m.group(1)
    if default:
        return default
    sys.exit("no --%s in %s" % (name, path))


def contrast():
    css = "assets/css/extended/"
    t = {k: token(TOKENS, k) for k in ("paper", "surface", "code-bg", "ink", "ink-2", "ink-3",
                                       "line", "accent", "navy-text", "navy", "on-navy", "on-navy-2")}
    t["pos"] = token(css + "custom.css", "pos")
    t["neg"] = token(css + "custom.css", "neg")
    t["fig-subject"] = token(css + "economics.css", "fig-subject", "#a32a1e")
    t["lr-accent"] = token(css + "decisions.css", "lr-accent", "#c2410c")
    t["content"] = "#1f1f1f"   # PaperMod's own colour for article prose (--content)
    text = ["ink", "content", "ink-2", "ink-3", "accent", "navy-text", "pos", "neg",
            "fig-subject", "lr-accent"]
    grounds = ["paper", "surface", "code-bg"]
    bad = 0
    print("light theme, text colours as the stylesheets have them")
    print("  %-12s %-8s" % ("token", "hex") + "".join("%-18s" % ("on " + g + " " + t[g]) for g in grounds))
    for k in text:
        cells = []
        for g in grounds:
            r = ratio(t[k], t[g])
            bad += r < 4.5
            cells.append("%-18s" % ("%.2f" % r))
        print("  %-12s %-8s" % (k, t[k]) + "".join(cells))
    for k in ("on-navy", "on-navy-2"):
        r = ratio(t[k], t["navy"])
        bad += r < 4.5
        print("  %-12s %-8s on the navy band %s: %.2f" % (k, t[k], t["navy"], r))
    print("  line %s on paper %.2f, on surface %.2f (borders, not text)"
          % (t["line"], ratio(t["line"], t["paper"]), ratio(t["line"], t["surface"])))
    print("  lowest text ratio: %.2f; pairs under 4.5: %d"
          % (min(ratio(t[k], t[g]) for k in text for g in grounds), bad))
    sys.exit(1 if bad else 0)


# ---------------------------------------------------------------- serve
def serve(served, port, delay_ms=0):
    import functools, http.server, time

    class Handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            super().end_headers()

        def do_GET(self):
            if delay_ms and self.path.split("?")[0].endswith(".woff2"):
                time.sleep(delay_ms / 1000.0)
            super().do_GET()

        def log_message(self, *a):
            pass

    h = functools.partial(Handler, directory=served)
    http.server.ThreadingHTTPServer(("127.0.0.1", port), h).serve_forever()


# ---------------------------------------------------------------- shots
PROBE = """<!doctype html><meta charset="utf-8"><title>probe</title>
<body style="margin:0;background:#888"><iframe id="f" style="display:block;width:%dpx;height:%dpx;border:0;background:#fff"></iframe><pre id="out" style="display:none"></pre>
<script>
var q = new URLSearchParams(location.search), f = document.getElementById("f");
try { localStorage.setItem("pref-theme", q.get("theme") || "light"); } catch (e) {}
function done(o) { document.getElementById("out").textContent = "PROBE" + JSON.stringify(o) + "PROBE"; }
f.onload = async function () {
  var d, w;
  try { d = f.contentDocument; w = f.contentWindow; d.body; } catch (e) { d = null; }
  if (!d) { await new Promise(function (r) { setTimeout(r, 2500); }); return done({}); }
  await d.fonts.ready;
  await new Promise(function (r) { setTimeout(r, 400); });
  await d.fonts.ready;
  function top(sel) { var e = d.querySelector(sel); return e ? Math.round(e.getBoundingClientRect().top + w.scrollY) : null; }
  var loaded = [];
  d.fonts.forEach(function (x) { if (x.status === "loaded") loaded.push(x.family + " " + x.weight + " " + x.style); });
  done({"h2": top(".post-content h2"), "count": top("#the-count"),
        "overflow": d.documentElement.scrollWidth - w.innerWidth, "loaded": loaded.sort()});
};
f.src = q.get("u");
</script>"""


def browser():
    for b in BROWSERS:
        if os.path.exists(b):
            return b
    sys.exit("no Chrome or Edge found")


def capture(exe, base, target, theme, png, want_pos=True):
    """A headless window on Windows cannot be narrower than about 500 px, so
    the page is loaded in a frame exactly 390 CSS px wide and cut out."""
    from urllib.parse import quote
    from PIL import Image
    frame = "%s/type-probe.html?theme=%s&u=%s" % (base, theme, quote(target, safe=""))
    common = [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
              "--user-data-dir=" + tempfile.mkdtemp(prefix="nvd_type_prof_"),
              "--virtual-time-budget=9000", "--window-size=800,%d" % TALL]
    pos = {}
    if want_pos:
        dom = subprocess.run(common + ["--dump-dom", frame], check=True, capture_output=True,
                             timeout=180).stdout.decode("utf-8", "replace")
        pos = json.loads(html.unescape(dom.split("PROBE")[1]))
    subprocess.run(common + ["--force-device-scale-factor=%d" % SCALE, "--screenshot=" + png, frame],
                   check=True, capture_output=True, timeout=180)
    Image.open(png).convert("RGB").crop((0, 0, W * SCALE, TALL * SCALE)).save(png)
    return pos


def shots(served, port, scratch=None):
    from PIL import Image, ImageDraw, ImageFont
    scratch = scratch or os.path.join(tempfile.gettempdir(), "nvd_type_final_raw")
    os.makedirs(scratch, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    base = "http://localhost:%s" % port
    exe = browser()
    pages = [(n, p or open_page(served)) for n, p in PAGES]
    probe = os.path.join(served, "type-probe.html")
    with open(probe, "w", encoding="ascii") as fh:
        fh.write(PROBE % (W, TALL))
    pos = {}
    try:
        for theme in ("light", "dark"):
            for n, p in pages:
                key = "%s_%s" % (n, theme)
                pos[key] = capture(exe, base, base + p, theme, os.path.join(scratch, key + ".png"))
                print("shot", key, {k: v for k, v in pos[key].items() if k != "loaded"}, flush=True)
        capture(exe, base, LIVE, "light", os.path.join(scratch, "live_article.png"), want_pos=False)
        print("shot live article", LIVE, flush=True)
    finally:
        os.remove(probe)
    json.dump(pos, open(os.path.join(scratch, "positions.json"), "w"), indent=1)

    def font(size):
        for f in ("segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
            try:
                return ImageFont.truetype(f, size)
            except OSError:
                pass
        return ImageFont.load_default()

    def crop(key, top_css=0, height_css=VIEW_H):
        img = Image.open(os.path.join(scratch, key + ".png")).convert("RGB")
        top = max(0, int(top_css * SCALE))
        return img.crop((0, top, W * SCALE, min(img.size[1], top + height_css * SCALE)))

    def save(im, path):
        im.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                                   dither=Image.Dither.NONE).save(path, optimize=True)
        print("wrote", path, im.size, os.path.getsize(path), "bytes", flush=True)

    def sheet(cols, title, path, shrink=1):
        pad, head, lab = 24, 64, 56
        cols = [(l, im.resize((im.size[0] // shrink, im.size[1] // shrink), Image.LANCZOS) if shrink > 1 else im)
                for l, im in cols]
        h = max(im.size[1] for _, im in cols)
        w = sum(im.size[0] for _, im in cols) + pad * (len(cols) + 1)
        page = Image.new("RGB", (w, head + lab + h + pad), (255, 255, 255))
        d = ImageDraw.Draw(page)
        d.text((pad, 16), title, font=font(30 if shrink == 1 else 22), fill=(21, 25, 30))
        x = pad
        for label, im in cols:
            d.text((x, head + 10), label, font=font(24 if shrink == 1 else 18), fill=(21, 25, 30))
            page.paste(im, (x, head + lab))
            d.rectangle((x - 1, head + lab - 1, x + im.size[0], head + lab + im.size[1]), outline=(150, 150, 150))
            x += im.size[0] + pad
        save(page, path)

    # the six final pictures
    save(crop("home_light"), os.path.join(OUT, "final_home_light.png"))
    save(crop("article_light"), os.path.join(OUT, "final_article-top_light.png"))
    save(crop("article_dark"), os.path.join(OUT, "final_article-top_dark.png"))
    save(crop("article_light", pos["article_light"]["h2"] - 170), os.path.join(OUT, "final_article-section_light.png"))
    count = pos["scorecard_light"].get("count") or 0
    save(crop("scorecard_light", count - 70 if count > 600 else 0), os.path.join(OUT, "final_scorecard_light.png"))
    sheet([("Live site today (12 November 2026)", crop("live_article")),
           ("This branch (pull request 64)", crop("article_light"))],
          "The 31 October article at phone width (390 px): before and after",
          os.path.join(OUT, "final_before-after_article.png"))
    # check sheets, for the person checking; not kept in the repository
    names = [n for n, _ in pages]
    for theme in ("light", "dark"):
        for i in (0, 5):
            sheet([(n, crop("%s_%s" % (n, theme))) for n in names[i:i + 5]],
                  "Top of page, %s, 390 px" % theme, os.path.join(scratch, "check_top_%s_%d.png" % (theme, i // 5 + 1)), 2)
    withh2 = [n for n in names if pos["%s_light" % n].get("h2")]
    for i in range(0, len(withh2), 5):
        sheet([(n, crop("%s_light" % n, pos["%s_light" % n]["h2"] - 170)) for n in withh2[i:i + 5]],
              "First section heading, light, 390 px", os.path.join(scratch, "check_h2_light_%d.png" % (i // 5 + 1)), 2)


if __name__ == "__main__":
    a = sys.argv[1:]
    cmd = a[0] if a else ""
    if cmd == "metrics":
        metrics(a[1] if len(a) > 1 else None)
    elif cmd == "chars" and len(a) > 1:
        chars(a[1])
    elif cmd == "contrast":
        contrast()
    elif cmd == "csv":
        rewrite_csv()
    elif cmd == "digits" and len(a) > 2:
        digits(a[1], a[2])
    elif cmd == "serve" and len(a) > 2:
        serve(a[1], int(a[2]), int(a[3]) if len(a) > 3 else 0)
    elif cmd == "shots" and len(a) > 2:
        shots(a[1], a[2], a[3] if len(a) > 3 else None)
    else:
        sys.exit(__doc__)
