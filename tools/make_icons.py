#!/usr/bin/env python3
"""tools/make_icons.py -- the PNG and ICO icons, rendered from the mark's SVG files.

    python tools/make_icons.py

Reads static/brand/S16.svg and static/brand/S32.svg (the marks Jacob picked on
23 November 2026) and writes, into static/:
    favicon-16x16.png     S16 at 16 px, transparent
    favicon-32x32.png     S32 at 32 px, transparent
    favicon.ico           both of the above in one file
    apple-touch-icon.png  S32 at 132 px, centred on the page colour, 180 px
The SVG favicon (static/favicon.svg, a copy of S16) is what current browsers
use, and it switches its own colours in dark mode; these files are for
browsers and devices that do not read SVG icons. Rendered in the light
colours. Needs Playwright (Chromium) and Pillow. Run from the repository root.
"""
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"
PAPER = "#f6f3ec"


def render(page, svg, box, size, background=None):
    """The SVG drawn `size` px wide, centred in a `box` px square."""
    body = "background:%s" % background if background else "background:transparent"
    page.set_viewport_size({"width": box, "height": box})
    page.set_content(
        '<html><body style="margin:0;%s;display:flex;align-items:center;justify-content:center;'
        'width:%dpx;height:%dpx"><div style="width:%dpx;height:%dpx">%s</div></body></html>'
        % (body, box, box, size, size, svg.replace('width="32" height="32"', 'width="100%" height="100%"')
           .replace('width="16" height="16"', 'width="100%" height="100%"')))
    return Image.open(io.BytesIO(page.screenshot(omit_background=background is None)))


def main():
    s16 = (STATIC / "brand" / "S16.svg").read_text(encoding="utf-8")
    s32 = (STATIC / "brand" / "S32.svg").read_text(encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(color_scheme="light")
        i16 = render(page, s16, 16, 16)
        i32 = render(page, s32, 32, 32)
        touch = render(page, s32, 180, 132, PAPER)
        browser.close()
    i16.save(STATIC / "favicon-16x16.png", optimize=True)
    i32.save(STATIC / "favicon-32x32.png", optimize=True)
    i32.save(STATIC / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32)], append_images=[i16])
    touch.convert("RGB").save(STATIC / "apple-touch-icon.png", optimize=True)
    for name in ("favicon-16x16.png", "favicon-32x32.png", "favicon.ico", "apple-touch-icon.png"):
        print(name, (STATIC / name).stat().st_size, "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
