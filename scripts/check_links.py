#!/usr/bin/env python3
"""
check_links.py -- every internal link, and every link to
github.com/jacobbuildmodel/*, on the built site resolves.

Usage:
    hugo --gc --minify -d public
    hugo --gc --minify --buildFuture -d public-future
    python scripts/check_links.py --site public --future public-future

Checks every page of --site (the build that is live today):
  - internal links (href/src that are root-relative, relative, or on the
    site's own baseURL): the target file exists in --site. A target that
    exists only in --future is a future-dated page: reported as "future" and
    NOT a failure, so pages hidden until their date never fail the check.
  - fragments (#id) on internal links: the id exists on the target page.
  - links to github.com/jacobbuildmodel/...: checked through the GitHub API
    (a missing path is a real 404 there, where github.com pages can soft-404).
    Uses GITHUB_TOKEN from the environment when set.
Every other external host is not requested (see EXCLUDED in
.github/workflows/linkcheck.yml for why); they are counted and listed.

Pages that are only redirect stubs (Hugo aliases, page/1/) are checked for
their target only. Exits 1 on any failure. Standard library only.
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from urllib.parse import urljoin, urlparse, unquote

OWNER = "jacobbuildmodel"
ATTR = re.compile(r'<(a|link|img|script|source)\b[^>]*?\s(href|src)=("([^"]*)"|\'([^\']*)\'|([^\s>]+))', re.I)
IDS = re.compile(r'\sid=("([^"]*)"|\'([^\']*)\'|([^\s>]+))', re.I)


def pages(root):
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".html"):
                yield os.path.join(d, f)


def target_file(root, path):
    """The file a site path is served from, or None."""
    p = unquote(path).lstrip("/")
    f = os.path.join(root, p)
    if os.path.isfile(f):
        return f
    if os.path.isfile(os.path.join(f, "index.html")):
        return os.path.join(f, "index.html")
    return None


_ids = {}
def ids_of(f):
    if f not in _ids:
        t = open(f, encoding="utf-8", errors="replace").read()
        _ids[f] = {html.unescape(next(g for g in m.groups()[1:] if g is not None)) for m in IDS.finditer(t)}
    return _ids[f]


_gh = {}
def github_ok(url, token):
    """(ok, detail) for a github.com/jacobbuildmodel URL, via the API."""
    u = urlparse(url)
    parts = [p for p in unquote(u.path).split("/") if p]
    if len(parts) == 1:
        api = f"users/{parts[0]}"
    elif len(parts) == 2:
        api = f"repos/{parts[0]}/{parts[1]}"
    elif len(parts) >= 4 and parts[2] in ("blob", "tree"):
        ref, path = parts[3], "/".join(parts[4:])
        api = f"repos/{parts[0]}/{parts[1]}/contents/{path}?ref={ref}"
    elif len(parts) >= 4 and parts[2] == "commit":
        api = f"repos/{parts[0]}/{parts[1]}/commits/{parts[3]}"
    elif len(parts) >= 4 and parts[2] == "pull":
        api = f"repos/{parts[0]}/{parts[1]}/pulls/{parts[3]}"
    else:
        api = f"repos/{parts[0]}/{parts[1]}"     # issues, releases, ...: the repo exists
    if api in _gh:
        return _gh[api]
    req = urllib.request.Request("https://api.github.com/" + api,
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "check_links.py"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30):
                res = (True, "200")
            break
        except urllib.error.HTTPError as e:
            res = (False, f"HTTP {e.code}")
            if e.code not in (403, 429, 502, 503):
                break
        except Exception as e:                       # network blip: retry, then report
            res = (False, f"{type(e).__name__}")
        time.sleep(5 * (attempt + 1))
    _gh[api] = res
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="public")
    ap.add_argument("--future", help="a --buildFuture build; targets found only there are future-dated pages")
    ap.add_argument("--base-url", default="https://jacobbuildmodel.github.io/")
    a = ap.parse_args()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    base = urlparse(a.base_url)

    fails, future, skipped = [], set(), Counter()
    n_internal = n_gh = n_pages = 0
    gh_links = {}
    for f in sorted(pages(a.site)):
        rel = os.path.relpath(f, a.site).replace(os.sep, "/")
        page_url = urljoin(a.base_url, rel[:-len("index.html")] if rel.endswith("index.html") else rel)
        t = open(f, encoding="utf-8", errors="replace").read()
        n_pages += 1
        stub = bool(re.search(r'http-equiv=("?)refresh\1', t, re.I))
        for m in ATTR.finditer(t):
            tag, raw = m.group(1).lower(), html.unescape(next(g for g in m.groups()[3:] if g is not None))
            if stub and tag != "a" and tag != "link":
                continue
            if not raw or raw.startswith(("mailto:", "tel:", "javascript:", "data:")):
                continue
            absu = urljoin(page_url, raw)
            u = urlparse(absu)
            if u.netloc == base.netloc:
                n_internal += 1
                tf = target_file(a.site, u.path)
                if tf is None:
                    if a.future and target_file(a.future, u.path):
                        future.add(u.path)
                        continue
                    fails.append(f"{rel}: internal {raw} -> no such page")
                    continue
                if u.fragment and tf.endswith(".html") and u.fragment not in ids_of(tf):
                    fails.append(f"{rel}: internal {raw} -> no id '{u.fragment}' on {u.path}")
            elif u.netloc == "github.com" and u.path.strip("/").split("/")[0].lower() == OWNER:
                n_gh += 1
                gh_links.setdefault(absu.split("#")[0], set()).add(rel)
            elif u.scheme in ("http", "https"):
                skipped[u.netloc] += 1

    for url, where in sorted(gh_links.items()):
        ok, detail = github_ok(url, token)
        if not ok:
            fails.append(f"{sorted(where)[0]}{' (+%d more)' % (len(where) - 1) if len(where) > 1 else ''}: {url} -> {detail}")

    print(f"pages checked: {n_pages}")
    print(f"internal links: {n_internal}; to future-dated pages (not failures): {len(future)}"
          + (f" {sorted(future)}" if future else ""))
    print(f"github.com/{OWNER} links: {n_gh} ({len(gh_links)} distinct), checked through the GitHub API"
          + ("" if token else " without a token"))
    print(f"external links not requested: {sum(skipped.values())} across {len(skipped)} hosts: "
          + ", ".join(f"{h} ({c})" for h, c in skipped.most_common()))
    for x in fails:
        print("FAIL", x)
    print(f"link check: {'passed' if not fails else str(len(fails)) + ' failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
