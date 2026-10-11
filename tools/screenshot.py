#!/usr/bin/env python3
"""
screenshot.py -- screenshots of one page at 390 and 1280 px, light and dark,
plus a full-page 390 px PNG, with an overflow check.

Usage:
    # a page of a built site (serves the folder on localhost for you)
    hugo --minify --buildFuture -d /tmp/site
    python tools/screenshot.py /economics/2026-10-17/ --root /tmp/site --out shots

    # a live or local URL
    python tools/screenshot.py https://jacobbuildmodel.github.io/economics/2026-10-03/ --out shots

Options:
    --root DIR   built site folder to serve when TARGET is a site path
                 (default: public). Build it with --baseURL http://localhost:PORT/
                 if the pages use absolute asset URLs, or leave the default
                 baseURL: the script rewrites nothing, so CSS must resolve.
    --port N     port for the local server (default 1316, so a build made with
                 --baseURL http://localhost:1316/ works unchanged)
    --out DIR    where the PNGs go (default: shots)
    --name NAME  file name prefix (default: derived from the page path)

Writes, for NAME:
    NAME_390_light.png  NAME_390_dark.png  NAME_1280_light.png  NAME_1280_dark.png
    NAME_390_full_light.png   (the whole page at 390 px, light)

Prints, per width and theme: the page's scrollWidth against the viewport
(anything wider is horizontal scroll), and how many images failed to load.
Exits 1 if any page scrolls sideways or any image failed, 0 otherwise.

Needs: pip install playwright && python -m playwright install chromium
Standard library otherwise.
"""
import argparse
import functools
import http.server
import os
import re
import sys
import threading

from playwright.sync_api import sync_playwright

WIDTHS = ((390, 844, 2), (1280, 900, 1))   # width, viewport height, device scale
SCHEMES = ("light", "dark")


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(root, port):
    handler = functools.partial(QuietHandler, directory=root)
    srv = http.server.ThreadingHTTPServer(("localhost", port), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    ap = argparse.ArgumentParser(description="Screenshots at 390/1280 px, light/dark, plus full page at 390 px")
    ap.add_argument("target", help="a URL, or a site path such as /economics/2026-10-17/")
    ap.add_argument("--root", default="public")
    ap.add_argument("--port", type=int, default=1316)
    ap.add_argument("--out", default="shots")
    ap.add_argument("--name")
    a = ap.parse_args()

    srv = None
    if re.match(r"https?://", a.target):
        url = a.target
    else:
        if not os.path.isdir(a.root):
            sys.exit(f"--root {a.root!r} is not a folder; build the site first")
        srv = serve(a.root, a.port)
        url = f"http://localhost:{a.port}/" + a.target.lstrip("/")
    name = a.name or (re.sub(r"[^A-Za-z0-9]+", "_", re.sub(r"^https?://[^/]+", "", url)).strip("_") or "home")
    os.makedirs(a.out, exist_ok=True)

    problems = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width, height, scale in WIDTHS:
            for scheme in SCHEMES:
                ctx = browser.new_context(viewport={"width": width, "height": height},
                                          color_scheme=scheme, device_scale_factor=scale)
                page = ctx.new_page()
                resp = page.goto(url, wait_until="networkidle")
                if resp is None or resp.status >= 400:
                    sys.exit(f"{url}: HTTP {resp.status if resp else 'no response'}")
                page.wait_for_timeout(400)
                tag = f"{width}_{scheme}"
                page.screenshot(path=os.path.join(a.out, f"{name}_{tag}.png"))
                if width == 390 and scheme == "light":
                    page.screenshot(path=os.path.join(a.out, f"{name}_390_full_light.png"), full_page=True)
                sw = page.evaluate("document.documentElement.scrollWidth")
                # The site's images are loading=lazy, so ones below the fold have
                # not loaded yet. Switch them to eager and wait for every image to
                # settle (load or error, 10 s cap) before the check; the
                # screenshots above are already taken.
                broken = page.evaluate("""async () => {
                    const imgs = Array.from(document.images);
                    imgs.forEach(i => { i.loading = 'eager'; });
                    await Promise.race([
                        Promise.all(imgs.map(i => i.complete ? null :
                            new Promise(r => { i.addEventListener('load', r); i.addEventListener('error', r); }))),
                        new Promise(r => setTimeout(r, 10000))]);
                    return imgs.filter(i => i.naturalWidth === 0).map(i => i.src);
                }""")
                ok = sw <= width and not broken
                problems += not ok
                print(f"{'ok  ' if ok else 'FAIL'} {tag:<12} scrollWidth {sw} (viewport {width}); "
                      f"images not loaded {len(broken)}" + (f": {broken[:3]}" if broken else ""))
                ctx.close()
        browser.close()
    if srv:
        srv.shutdown()
    print(f"saved to {a.out}/ as {name}_*.png")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
