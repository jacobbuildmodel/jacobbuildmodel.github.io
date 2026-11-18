"""Make one self-contained HTML file of the chart lab page, for reading on a phone straight from a file.

The file holds the page's text and charts, the site's style sheet, the chart style sheet, the chart script,
the chart data and the static fallback figures, all inline. It asks for nothing over the network: no fonts
(the system fonts stand in), no images, no analytics. Light and dark follow the device. It is a private
preview of a draft page, not a publication.

Usage:
  hugo --buildDrafts --buildFuture -d BUILD
  python -I tools/make_chart_preview.py --build BUILD --out PREVIEW.html

Pure standard library.
"""
import argparse
import base64
import glob
import os
import re

PAGE = "lab/interactive-charts/index.html"
HERE = os.path.dirname(os.path.abspath(__file__))


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def one(pattern):
    found = glob.glob(pattern)
    assert len(found) == 1, (pattern, found)
    return read(found[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True, help="folder of a hugo build made with --buildDrafts")
    ap.add_argument("--out", required=True)
    ap.add_argument("--static", default=os.path.join(HERE, "..", "static"))
    a = ap.parse_args()

    page = read(os.path.join(a.build, PAGE))
    title = re.search(r"<h1[^>]*>\s*(.*?)\s*(?:<|$)", page, re.S).group(1)
    start = page.index('<div class="post-content')
    start = page.index(">", start) + 1
    end = page.rindex("</div>", 0, page.index('<footer class="post-footer"'))
    body = page[start:end]

    # The chart system is inlined below, so its two tags go; the fallback figures become data URIs.
    body, n_css = re.subn(r'<link rel="stylesheet" href="/css/ichart[^>]*>', "", body)
    body, n_js = re.subn(r'<script type="module" src="/js/ichart[^>]*></script>', "", body)
    assert n_css == 1 and n_js == 1, (n_css, n_js)

    def figure(m):
        with open(os.path.join(a.static, "figs", m.group(1)), "rb") as f:
            return 'src="data:image/svg+xml;base64,' + base64.b64encode(f.read()).decode("ascii") + '"'

    body = re.sub(r'src="/figs/([A-Za-z0-9_.-]+\.svg)"', figure, body)

    site_css = one(os.path.join(a.build, "assets", "css", "stylesheet.*.css"))
    site_css = re.sub(r"@font-face\s*\{[^}]*\}", "", site_css)  # no font files: the fallback stack is used
    chart_css = one(os.path.join(a.build, "css", "ichart.min.*.css"))
    chart_js = one(os.path.join(a.build, "js", "ichart.min.*.js"))
    assert "</script" not in chart_js and "</style" not in site_css + chart_css

    html = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Chart lab preview (private)</title>
<script>(function(){{var m=matchMedia("(prefers-color-scheme: dark)");function s(){{document.documentElement.setAttribute("data-theme",m.matches?"dark":"light")}}s();m.addEventListener("change",s)}})();</script>
<style>{site_css}</style>
<style>{chart_css}</style>
<style>.preview-note{{margin:0 0 16px;padding:10px 12px;border:1px dashed var(--line);border-radius:8px;font:14px/1.4 var(--font-sans);color:var(--ink-2)}}</style>
</head>
<body id="top">
<main class="main" id="main">
<article class="post-single">
<header class="post-header">
<p class="preview-note">Private preview of a draft page, made for reading on a phone. Not published. Everything is inside this one file; it asks for nothing over the network.</p>
<h1 class="post-title">{title}</h1>
</header>
<div class="post-content md-content">{body}</div>
</article>
</main>
<script type="module">{chart_js}</script>
</body>
</html>
"""
    # Nothing may be fetched: no absolute-path or remote sources, no url() in the styles.
    leaks = re.findall(r'(?:src|srcset|poster)="(?!data:)[^"]*"|<link[^>]*>|url\((?!["\']?(?:data:|#))[^)]*\)|@import[^;]*;', html)
    assert not leaks, leaks[:5]
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("wrote", a.out, len(html.encode("utf-8")), "bytes")


if __name__ == "__main__":
    main()
