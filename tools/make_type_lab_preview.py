"""tools/make_type_lab_preview.py -- one self-contained HTML file of the type
lab, for reading on a phone straight from a file (draft pull request 64).

    python tools/make_type_lab_preview.py <built site dir> <output.html>

<built site dir> is a local build with drafts (hugo --buildDrafts -d <dir>).
The words and markup are cut from its lab/typefaces/index.html, so they are
the site's own. The styles below repeat, by hand, only the rules that page
needs from assets/css/extended/ and the theme, with the same values; the
fonts are the files in static/fonts/ and static/fonts/lab/, embedded as
base64. The file makes no request to any site and runs no script: the
switches are radio buttons, and the stylesheet reads which one is checked,
so it also works where a file preview does not run JavaScript.
"""
import base64, os, re, sys

FONTS = "static/fonts"
CSS = r"""
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{margin:0}
.sw{position:fixed;top:0;left:0;width:1px;height:1px;opacity:0;pointer-events:none}
.lab{
  --paper:#ffffff;--surface:#ffffff;--code-bg:#f4f7f9;--ink:#15191e;--ink-2:#3f4852;--ink-3:#5f6873;
  --line:#c5ccd4;--navy:#1f3a5f;--navy-text:#1f3a5f;--accent:#3d6c8c;--accent-quiet:#6f93ad;
  --pos:#2E7D5B;--neg:#8A6116;--content:#1f1f1f;
  --font-serif:"NVD Serif","NVD Serif Fallback",Georgia,"Iowan Old Style",serif;
  --font-sans:"NVD Sans","NVD Sans Fallback",-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  min-height:100vh;padding-bottom:150px;background:var(--paper);color:var(--ink);
  font-family:var(--font-sans);font-size:18px;line-height:1.6;
}
#p-b:checked ~ .lab{--paper:#f6f3ec;--code-bg:#fdfcf9;--ink:#1b1f24;--ink-3:#59616b;--line:#b3ab9b;--accent:#35627f;--pos:#2a7354}
#p-d:checked ~ .lab{--paper:#1d1e20;--surface:#26282c;--code-bg:#2b2d32;--ink:#e6e6e7;--ink-2:#b4b8be;--ink-3:#9a9fa6;
  --line:#454951;--navy-text:#9dbbe0;--accent:#85acc9;--accent-quiet:#a3c0d6;--pos:#6FBF9A;--neg:#D6A544;--content:#c4c4c4}
#t-b:checked ~ .lab{
  --font-serif:"Lab Newsreader","Lab Newsreader Fallback",Georgia,"Iowan Old Style",serif;
  --font-sans:"Lab Inter","Lab Inter Fallback",-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
#t-b:checked ~ .lab :is(table,.method-strip-item){font-family:"Lab Mono Figures",var(--font-sans)}
#t-c:checked ~ .lab{
  --font-serif:"Lab Lato","Lab Lato Fallback",-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --font-sans:"Lab Lato","Lab Lato Fallback",-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
#t-c:checked ~ .lab :is(.post-title,.post-content h2){font-family:"Lab Playfair","Lab Playfair Fallback",Georgia,serif;font-weight:700}
#t-c:checked ~ .lab .entry-lead{font-style:normal}

.band{background:var(--navy);border-bottom:1px solid var(--line);padding:0 16px}
.brand{margin:0;padding-top:15px;font-size:20px;line-height:24px;font-weight:600;color:#ffffff}
.tagline{margin:2px 0 0;font-size:13px;line-height:16px;color:#dbe4ee}
.menu{display:flex;flex-wrap:wrap;gap:4px 16px;margin-top:15px}
.menu span{display:flex;align-items:center;min-height:44px;font-size:16px;color:#dbe4ee}
main{max-width:688px;margin:0 auto;padding:14px}
.about{margin:10px 0 0;padding:10px 12px;border:1px dashed var(--line);border-radius:4px;font-size:14px;line-height:1.45;color:var(--ink-3)}
.post-header{margin:24px 0 20px}
.breadcrumbs{display:flex;flex-wrap:wrap;align-items:center;gap:3px;font-size:16px;color:var(--ink-3)}
.breadcrumbs svg{width:14px;height:14px}
.entry-question{margin:4px 0 6px;font-size:15.2px;line-height:1.4;color:var(--ink-3)}
.post-title{margin:0;font-family:var(--font-serif);font-weight:600;
  font-size:clamp(30px,calc(30px + 10 * (100vw - 390px) / 890),40px);
  line-height:clamp(36px,calc(36px + 10 * (100vw - 390px) / 890),46px)}
.post-meta{margin-top:5px;font-size:14px;color:var(--ink-3)}
.method-strip{margin-top:14px;padding:10px 14px;border:1px solid var(--line);border-radius:8px;background:var(--code-bg);
  font-variant-numeric:tabular-nums lining-nums}
.method-strip-row{display:flex;flex-wrap:wrap;gap:4px 22px;align-items:baseline}
.method-strip-item{font-family:var(--font-sans);font-size:.78em;line-height:1.6;color:var(--ink-3)}
.method-strip-label{letter-spacing:.06em;margin-right:6px}
.method-strip-value{color:var(--ink)}
.ms-pass{color:var(--pos);white-space:nowrap}.ms-fail{color:var(--neg);white-space:nowrap}.ms-total{white-space:nowrap}
.method-strip-link,.post-content a{color:var(--accent);text-decoration:underline;text-decoration-color:var(--accent-quiet);text-underline-offset:.3rem}
.method-strip-note{margin:6px 0 0;font-size:.75em;line-height:1.4;color:var(--ink-3)}
.entry-lead{margin:14px 0 0;max-width:660px;font-family:var(--font-serif);font-style:italic;color:var(--ink);
  font-size:clamp(19.5px,calc(19.5px + 2.5 * (100vw - 390px) / 890),22px);line-height:1.45}
.post-content{margin:30px 0;font-family:var(--font-serif);font-size:1.05em;color:var(--content)}
.post-content p{margin:0 0 1.15em}
.post-content h2,.post-content h3{font-weight:600;color:var(--ink)}
.post-content h2{position:relative;margin:2.4em 0 .75em;line-height:1.2;
  font-size:clamp(25px,calc(25px + 5 * (100vw - 390px) / 890),30px)}
.post-content h3{margin:1.9em 0 .5em;line-height:1.3;font-size:clamp(21px,calc(21px + 3 * (100vw - 390px) / 890),24px)}
.post-content h2::after{content:"";display:block;width:48px;height:3px;margin-top:12px;background:var(--navy-text)}
.h2-label{display:block;margin-bottom:6px;font-family:var(--font-sans);font-size:13px;line-height:18px;font-weight:600;
  letter-spacing:.08em;text-transform:uppercase;color:var(--navy-text)}
.h2-colon{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.h2-text{display:block}
.h2-text::first-letter{text-transform:uppercase}
:is(#h-u,#h-o):checked ~ .lab :is(.h2-label,.h2-text){display:inline;margin:0;font:inherit;letter-spacing:inherit;text-transform:none;color:inherit}
:is(#h-u,#h-o):checked ~ .lab .h2-colon{position:static;width:auto;height:auto;overflow:visible;clip-path:none;white-space:inherit}
#h-o:checked ~ .lab .post-content h2{margin-top:2.2em;padding-top:16px;border-top:1px solid var(--line)}
#h-o:checked ~ .lab .post-content h2::after{position:absolute;top:-1px;left:0;margin:0}
.table-scroll{margin:22px 0;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.92em;font-variant-numeric:tabular-nums lining-nums}
th,td{padding:6px 10px;border:1px solid var(--line);text-align:left;line-height:1.5}
th{font-weight:600}

.bar{position:fixed;left:0;right:0;bottom:0;z-index:5;padding:6px 12px calc(6px + env(safe-area-inset-bottom));
  background:var(--surface);border-top:2px solid var(--ink);font-family:var(--font-sans);font-size:13px;line-height:16px;color:var(--ink)}
.bar-in{max-width:660px;margin:0 auto;display:grid;grid-template-columns:auto 1fr;gap:5px 10px;align-items:center}
.bar b{font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.set{display:flex;gap:6px}
.set label{flex:1 1 0;display:flex;align-items:center;justify-content:center;min-height:34px;padding:2px 4px;text-align:center;
  border:1px solid var(--line);border-radius:4px;background:var(--paper);cursor:pointer}
#t-a:checked ~ .lab label[for="t-a"],#t-b:checked ~ .lab label[for="t-b"],#t-c:checked ~ .lab label[for="t-c"],
#p-a:checked ~ .lab label[for="p-a"],#p-b:checked ~ .lab label[for="p-b"],#p-d:checked ~ .lab label[for="p-d"],
#h-k:checked ~ .lab label[for="h-k"],#h-u:checked ~ .lab label[for="h-u"],#h-o:checked ~ .lab label[for="h-o"]{
  background:#1f3a5f;border-color:#1f3a5f;color:#ffffff;font-weight:600}
.sw:focus-visible ~ .lab .bar{outline:2px solid var(--accent)}
"""

# family, file (under static/fonts), weight, style, extra descriptors
FACES = [
    ("NVD Serif", "NVDSerif-Regular.woff2", 400, "normal", ""),
    ("NVD Serif", "NVDSerif-It.woff2", 400, "italic", ""),
    ("NVD Serif", "NVDSerif-Semibold.woff2", 600, "normal", ""),
    ("NVD Sans", "NVDSans-Regular.woff2", 400, "normal", ""),
    ("NVD Sans", "NVDSans-Semibold.woff2", 600, "normal", ""),
]
LOCAL = """
@font-face{font-family:"NVD Serif Fallback";src:local("Georgia");size-adjust:107.45%;ascent-override:96.42%;descent-override:31.18%;line-gap-override:0%}
@font-face{font-family:"NVD Sans Fallback";src:local("Arial");size-adjust:93.76%;ascent-override:106.65%;descent-override:34.77%;line-gap-override:0%}
"""
PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Type lab preview: The New Void Deck</title>
<style>%(faces)s%(css)s</style>
</head>
<body>
<input class="sw" type="radio" name="t" id="t-a" checked aria-label="Typeface A"><input class="sw" type="radio" name="t" id="t-b" aria-label="Typeface B"><input class="sw" type="radio" name="t" id="t-c" aria-label="Typeface C">
<input class="sw" type="radio" name="p" id="p-a" checked aria-label="White page"><input class="sw" type="radio" name="p" id="p-b" aria-label="Warm page"><input class="sw" type="radio" name="p" id="p-d" aria-label="Dark">
<input class="sw" type="radio" name="h" id="h-k" checked aria-label="Heading with label line"><input class="sw" type="radio" name="h" id="h-u" aria-label="Heading with rule under"><input class="sw" type="radio" name="h" id="h-o" aria-label="Heading with rule over">
<div class="lab">
<div class="band"><p class="brand">The New Void Deck</p><p class="tagline">Jacob Ong: economics with a scorecard</p>
<div class="menu"><span>Economics</span><span>Scorecard</span><span>How it works</span><span>About</span></div></div>
<main>
<p class="about">Type lab preview, made %(date)s from draft pull request 64. Not the live site. The three rows at the bottom of the screen switch the typeface (A is the site as it is), the page colour and the section-heading mark. The words are from the 31 October piece and the scorecard.</p>
%(body)s
</main>
<div class="bar"><div class="bar-in">
<b>Type</b><div class="set"><label for="t-a">A Source</label><label for="t-b">B Newsreader</label><label for="t-c">C Playfair</label></div>
<b>Page</b><div class="set"><label for="p-a">White</label><label for="p-b">Warm</label><label for="p-d">Dark</label></div>
<b>Head</b><div class="set"><label for="h-k">Label line</label><label for="h-u">Rule under</label><label for="h-o">Rule over</label></div>
</div></div>
</div>
</body>
</html>
"""


def data_uri(path):
    return "data:font/woff2;base64," + base64.b64encode(open(path, "rb").read()).decode("ascii")


def faces():
    out = []
    for fam, f, w, st, extra in FACES:
        out.append('@font-face{font-family:"%s";src:url(%s) format("woff2");font-weight:%d;font-style:%s;font-display:swap;%s}'
                   % (fam, data_uri(os.path.join(FONTS, f)), w, st, extra))
    out.append(LOCAL)
    for sheet in ("type-b.css", "type-c.css"):
        css = open(os.path.join(FONTS, "lab", sheet), encoding="ascii").read()
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        css = re.sub(r"url\(/fonts/(lab/[^)]+)\)",
                     lambda m: "url(%s)" % data_uri(os.path.join(FONTS, m.group(1))), css)
        out.append(re.sub(r"\s+", " ", css))
    return "\n".join(out)


def body(built):
    html = open(os.path.join(built, "lab", "typefaces", "index.html"), encoding="utf-8").read()
    a = html.index('<header class="post-header">')
    b = html.index('<div class="lab-end">')
    part = html[a:b] + "</div>"
    part = re.sub(r"<style>.*?</style>", "", part, flags=re.S)
    part = re.sub(r'<p class="lab-note">.*?</p>', "", part, flags=re.S)
    part = re.sub(r'<span class="entry-hint".*?</span>', "", part, flags=re.S)
    part = re.sub(r'<a hidden class="anchor"[^>]*>#</a>', "", part)
    part = re.sub(r"<svg.*?</svg>", "&rsaquo;", part, flags=re.S)
    part = re.sub(r'\s(?:href|title|tabindex)="[^"]*"', "", part)
    part = re.sub(r"\n\s*\n+", "\n", part)
    return part.strip()


def main(built, out):
    import datetime
    d = datetime.date.today()
    page = PAGE % {"faces": faces(), "css": CSS, "body": body(built),
                   "date": "%d %s %d" % (d.day, d.strftime("%B"), d.year)}
    data = page.encode("ascii", "xmlcharrefreplace")
    for needle in (b"http://", b"https://", b"<script", b"@import"):
        if needle in data:
            sys.exit("the preview must not carry %r" % needle)
    open(out, "wb").write(data)
    print("wrote", out, len(data), "bytes")
    if len(data) > 900 * 1024:
        sys.exit("over 900 KB")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
