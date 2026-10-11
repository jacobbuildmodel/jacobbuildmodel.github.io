#!/usr/bin/env python3
"""
flatten_svg.py -- make a site chart SVG print-safe for the paper.

The site's charts colour themselves with CSS custom properties
(`--surface-1`, `var(--series-1)`, ...) and switch them in a
prefers-color-scheme: dark block. Typst's SVG renderer does not support
custom properties, so every such fill came out black. This writes a copy
with each var() replaced by its light-theme value, the dark-mode blocks
removed, and chart text set in Source Sans 3 (the paper's sans), so no
system font is embedded.

Usage:
    python flatten_svg.py figures/source/chart.svg figures/chart.svg
    python flatten_svg.py figures/source/*.svg --out figures/

Standard library only. The source file is never modified.
"""
import os
import re
import sys

SANS = '"Source Sans 3", sans-serif'


def flatten(svg):
    style = re.search(r"<style[^>]*>(.*?)</style>", svg, re.S)
    css = style.group(1) if style else ""
    # Light values: the first declaration of each custom property, outside any
    # @media or :root[data-theme=...] block.
    light_css = re.sub(r"@media[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css)
    light_css = re.sub(r":root\[data-theme=[^\]]*\][^{]*\{[^}]*\}", "", light_css)
    values = {}
    for name, val in re.findall(r"(--[\w-]+)\s*:\s*([^;}]+)", light_css):
        values.setdefault(name, val.strip())

    def resolve(text):
        for _ in range(5):                       # var() may refer to var()
            new = re.sub(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]+))?\)",
                         lambda m: values.get(m.group(1), (m.group(2) or "").strip()) or m.group(0), text)
            if new == text:
                break
            text = new
        return text

    new_css = resolve(light_css)
    new_css = re.sub(r"font-family\s*:[^;}]+", "font-family: " + SANS, new_css)
    out = svg[:style.start(1)] + new_css + svg[style.end(1):] if style else svg
    out = resolve(out)
    out = re.sub(r'font-family="[^"]*"', 'font-family=\'' + SANS + '\'', out)
    if "var(--" in out:
        raise SystemExit("unresolved var() left in the output")
    return out


def main(argv):
    if "--out" in argv:
        i = argv.index("--out")
        outdir, srcs = argv[i + 1], argv[:i] + argv[i + 2:]
        pairs = [(s, os.path.join(outdir, os.path.basename(s))) for s in srcs]
    elif len(argv) == 2:
        pairs = [(argv[0], argv[1])]
    else:
        sys.exit(__doc__)
    for src, dst in pairs:
        data = flatten(open(src, encoding="utf-8").read())
        open(dst, "w", encoding="utf-8", newline="\n").write(data)
        print(f"{src} -> {dst}")


if __name__ == "__main__":
    main(sys.argv[1:])
