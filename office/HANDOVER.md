# HANDOVER -- site build and downloads chat (written 11 October 2026)

For a new chat taking over with no history. Read this, then CLAUDE.md, then the
office/ files named below. Every hand-back uses office/REPLY_FORMAT.md.

## What this role does
Builds and ships the website (this repo), and fetches raw files for pieces in
github.com/jacobbuildmodel/coe-analysis without opening data values. Never the
researcher, never the checker, never the one who merges.

## Repos
- jacobbuildmodel.github.io (this one): Hugo 0.147.9 extended + PaperMod (Hugo
  module, go.mod). Deployed by .github/workflows/deploy.yml to GitHub Pages
  (Pages source = GitHub Actions). buildFuture = false: a page dated in the
  future is not built until that day.
- coe-analysis: COE pieces at the root; erp/, pwm/, sgd/ each a sealed piece
  (THESIS.md, SEALED, run_all.sh, raw/RETRIEVED.txt, 00_coverage.py).
- gst-passthrough, hdb-affordability: one piece each.

## Pieces (state on 11 October 2026)
| Date | Article | Repo | State |
|---|---|---|---|
| 22 Aug - 12 Sep | four COE pieces | coe-analysis | live; written before sealing existed, not scored |
| 8 Sep | GST in the water bill | gst-passthrough | live; scored |
| 19 Sep | HDB four-room affordability | hdb-affordability | live; scored |
| 3 Oct | HDB loan vs bank | hdb-affordability | live; scored |
| 17 Oct | ERP: roads more crowded, speeds held | coe-analysis/erp | sealed 26 Sep; data opened; article on main, hidden until 17 Oct |
| 31 Oct | PWM: the floor became the pay | coe-analysis/pwm | sealed 28 Sep; data opened; article on main, hidden until 31 Oct |
| 14 Nov | SGD: the yen did most of the work | coe-analysis/sgd | sealed 3 Oct (9e46034); data opened; article + /researchers/singapore-dollar/ on main, hidden until 14 Nov; reviewed version pending (below) |

Open question pages (content/open/): coe-or-erp, minimum-wage-or-pwm,
singapore-dollar. Each is sealed: its body md5 is in data/open_seals.yaml. The
`answered:` front-matter marker is added on publication day. Scorecard on
main: 23 sealed, 9 held, 9 failed, 5 neither (front-matter params feed the
home band). Ideas page goes live 17 Oct.

## Open work, with the exact next step
- Site PR #17 (erp-pubday): Jacob merges on 17 Oct, not before (scorecard
  27/10/11/6, Brier 0.194 over 4; marks coe-or-erp answered). It CONFLICTS in
  .vale.ini: resolve by keeping both one-file sections,
  [content/open/2026-09-26-coe-or-erp.md] Site.Jargon = NO and
  [content/researchers/singapore-dollar.md] Site.Acronyms = NO. Then rerun
  Vale and scripts/check_open_pages.py.
- coe-analysis PR #5 (sgd-review, d57f873): the article and researcher page
  after four outside reviews, plus the new sgd/figs/sgd_chart4_rolling.svg.
  NOT merged on 11 Oct. After Jacob merges it: branch sgd-final from site
  main, copy sgd/2026-11-14.md -> content/economics/2026-11-14.md and
  sgd/FOR_RESEARCHERS.md -> content/researchers/singapore-dollar.md, changing
  only `draft: true` -> `draft: false`. Copy changed charts and chart 4 to
  static/figs/ (md5 identical). Screenshots, Vale, open-pages check, PR.
- PWM publication day (31 Oct) and SGD publication day (14 Nov): one PR each,
  by .claude/skills/site-pubday (scorecard + open page answered). Not yet opened.
- Branches ending -previews hold PR screenshots only; delete after review.
  Many merged feature branches remain; delete only if Jacob says so.

## Rules and where they live
- CLAUDE.md: never-publish list, Singapore FAA compliance, house style.
- office/CHECKPOINTS.md: pass criteria per checkpoint (0, S, 1, 2, 3).
- office/QUESTION_RULES.md: HOOK H1-H7, Rule 0 items 1-5 (5 = decision test), "What it changes".
- office/STORY_CRAFT.md (S1-S10, R1-R7), office/EDITOR.md, office/REPLY_FORMAT.md.
- .claude/skills/: site-publish-article, site-pubday, site-open-page. Follow
  them when the task matches.
- .vale.ini + styles/Site/: Directives, We, Jargon, Acronyms (errors), Causal (warning).

## Commands
- Build: `hugo --gc --minify`; future pages: `hugo --minify --buildFuture`;
  a given day: `hugo --minify --clock 2026-11-14T00:30:00Z`.
- aitell as CI: `python scripts/aitell.py content/economics/*.md content/process/*.md content/open/*.md content/scorecard.md content/corrections.md content/ideas.md --strict --published-only`.
- Vale as lint.yml: Vale 3.24.0 on `git diff --name-only --diff-filter=AM <base>...HEAD -- 'content/*.md'`.
- Open pages: `python scripts/check_open_pages.py --base origin/main`.
- Overflow and screenshots: Playwright (Python) at 390 and 1280 px, light and
  dark; check `document.documentElement.scrollWidth` equals the viewport, and
  each chart img has naturalWidth > 0.
- Piece checks live in coe-analysis: `./run_all.sh` in the piece folder, its
  tests/ fixtures, and for sgd `python 14_manifest.py --check`.
- Downloads: only `<piece>/00_coverage.py` (labels, coverage, md5) may read a
  data file before the seal. PDFs: title page only.

## Gotchas and fixes
- Windows core.autocrlf: working copies are CRLF, so md5s, the open-pages seal
  check and Vale's front-matter parsing all fail falsely. Run checks in
  `git -c core.autocrlf=false clone`; compare committed blobs (`git cat-file -p HEAD:path | md5sum`).
- Hugo edits go.mod and creates go.sum: `git checkout -- go.mod; rm go.sum`
  before commit. Never commit public/, resources/, .hugo_build.lock.
- Scheduled deploys (00:30 and 01:30 UTC) start about 5-6 hours late. If a
  page must be up at 08:30 Singapore, Jacob runs the workflow by hand.
- SingStat TableBuilder serves at most 5,000 points per request: page with `&offset=5000, 10000, ...`.
- data.gov.sg: v1 poll-download API, not the page. bis.org old /publ/ URLs now
  redirect to landing pages; use /publications/... paths.
- Vale reads front matter (titles, summaries) but TokenIgnores do not apply
  there. A one-file exemption is a `[content/<path>.md]` section, and only
  with Jacob's approval.
- `build: render: never` on a section _index hides the list page; PaperMod's
  breadcrumb then shows that section as a link to the page itself.
- Git Bash rewrites leading-slash arguments: prefix MSYS_NO_PATHCONV=1.
- PaperMod's own opengraph/twitter partials are overridden in layouts/partials/templates/.

## Credentials (names only; no value is ever in the repo)
- GitHub CLI login for the jacobbuildmodel account (gh auth).
- OneMap API token: EXPIRED 8 October 2026; Jacob renews it.
- Umami website ID and Buttondown username sit in hugo.toml (public, not secret).

## Do not
- Merge any PR, or push to main. Jacob merges.
- Edit a sealed file: THESIS.md, SEALED, SEAL_MANIFEST.md, a published open
  page body (data/open_seals.yaml), or any confidence number.
- Propose or adjust a confidence. Only Jacob sets them.
- Open, print or preview a data value before a seal, or accept a site's terms
  on Jacob's behalf.
- Change the scorecard or an open page outside its publication-day PR.
- Publish anything on the CLAUDE.md never-publish list, advice, or "we".
