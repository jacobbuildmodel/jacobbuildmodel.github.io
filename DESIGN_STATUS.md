# Design session one  -  status

Branch: `design-phase2-first-screens`. PR: #3. **Merged** (merge commit
`61fc5c7`). First written at the end of the Phase 2 review round, 22 September
2026, for whoever picks this up next  -  a fresh session or a human  -  so the
last hour of debugging doesn't have to happen twice. Updated 24 September
2026 to record the merge and add the Phase 3 status section below.

## Where this came from

Phase 1 (mockups only, no code) proposed three directions  -  A "The Paper
Trail" (method-first), B "The Front Page" (finding-first, data-journalism),
C "The Notebook" (restraint, serif). Jacob picked a hybrid: B's finding-and-
chart-first layout, C's serif type and unmistakable asides, and a version of
A's method strip rebuilt from facts that already exist rather than new
authoring fields. Phase 2 is that hybrid, built for real on this branch.

## What Phase 2 has done

**Layout.** `layouts/single.html` and `layouts/list.html`: every article and
every economics/home card now leads with the piece's own `summary` (already
existed in front matter, just promoted) and its own first chart (extracted
from `.Content` server-side, never a new field, never duplicated). Table of
contents stays `ShowToc: true` everywhere per CLAUDE.md  -  only the
open-by-default behavior changed, and only because six published posts had
drifted from the pipeline's own `TocOpen: false` default.

**Method strip.** `layouts/partials/method_strip.html`. Renders only when a
post carries transcribed pre-registration facts (`thesisSealed`,
`testsPassed`, `testsFailed`, `testsOther`, `testsTotal`)  -  copied verbatim
from the linked repo's `THESIS.md` seal line and `RESULTS.md` verdict table,
not composed. Revisit date is *computed* (publish date + 12 months), not a
field, so it can't drift. Currently wired up for exactly one post,
`content/economics/2026-09-19.md` (the HDB piece)  -  the only post whose
linked repo (`hdb-affordability`) has this structure. `gst-passthrough` also
has `THESIS.md`/`RESULTS.md` but in a different, harder-to-parse format
(plain-text `T1 FAIL` blocks, not a markdown table) and has **not** been
wired up  -  nobody has transcribed its numbers into front matter yet.
`coe-analysis` has no `THESIS.md`/`RESULTS.md` at all (different structure:
`FINDINGS.md` notes, no formal pre-registration), so it will never get a
strip until that changes upstream, and the template correctly renders
nothing there rather than something half-true.

**Identity.** "Jacob Ong" appears once, in the masthead
(`layouts/partials/header.html`, reading `site.Params.author`).
`hideAuthor: true` in `hugo.toml` stops it repeating on every card/article
meta line.

**Reading type.** Source Serif 4 for `.post-content` prose only (loaded in
`layouts/partials/extend_head.html`). Nav, meta, labels, the method strip
stay in the theme's system sans/mono.

**Asides.** Extended the *existing* `details.aside` component in
`assets/css/extended/economics.css` (tint, border, desktop margin-float)
rather than writing a second one  -  see "found the hard way" below for why
that matters.

**Palette.** Morning, chosen from three options. Baked into
`assets/css/extended/custom.css`'s base `:root` tokens
(`--accent`, `--accent-quiet`, `--code-bg`, `--border`). The
`?palette=morning|mint|sky` comparison scaffolding was temporary and has
been fully removed  -  nothing to clean up later.

**Identity copy.** `hugo.toml` description/keywords and
`static/img/social-preview.png` no longer describe deleted sections (NEWS,
SECTOR, STANDOUTS, "weekly market analysis"). Site title stays
"Jacob | Market Research"  -  Jacob said not to rebrand yet. New description
is "Singapore policy, measured with public data.", reused verbatim from the
live homepage rather than composed fresh.

## The checker's five fixes  -  all finished

1. **About page regression**  -  `single.html` was reading `.Summary`
   (Hugo's auto-excerpt fallback for pages with no explicit summary), which
   printed About's own headings-stripped text as a dek. Fixed to
   `.Params.summary`, the raw front matter value only. Verified: zero
   `.entry-lead` elements render on `/about/`, `/process/`, `/stocks/`.
2. **Masthead sizing/clipping**  -  0.68em (12.24px, technically over the
   11px floor but a monospace face reads smaller than its font-size at a
   glance) raised to 0.8em (14.4px), plus 6px top clearance added.
3. **Home reorder**  -  the latest piece now renders before the home-info
   intro on every viewport. Required a real refactor: pulled the card
   markup into a new `layouts/partials/entry_card.html` so the featured
   entry and the loop below share one implementation via Hugo's
   `{{ continue }}`, instead of two copies that could drift apart.
4. **Method strip revisit date + phone wrap**  -  revisit date added
   (computed, see above). "of 9" / "of N" no longer orphans onto its own
   line on a phone (`nbsp` + `white-space: nowrap` on the value fragments).
5. **ASCII-only**  -  every non-ASCII character *this branch's own diff*
   introduced (em dashes, one box-drawing section banner I'd copied from
   the file's existing style, two inherited pagination guillemets) replaced
   with ASCII. Checked line-by-line against `origin/main`, not by eye  - 
   pre-existing non-ASCII in lines this branch never touched (e.g. the
   original "Layer badge  - " comment in `single.html`, predates this branch)
   was deliberately left alone as out of scope.

Commits, in order: `1b267f7` (Phase 2 build) -> `69f2d4c` (palette + wording
baked in, plus a dark-mode accent bug found along the way) -> `ebf3f40` (the
five fixes above) -> `b576486` (the wording decision below).

## Jacob's wording decision  -  resolved, not open

The method strip's "N other" vs "N inconclusive" call was explicitly left to
Jacob rather than decided. **He picked "inconclusive."** Shipped in
`b576486`, re-verified the longer word still wraps cleanly (moves as one
whole fragment to its own line at a comma boundary, never splits
mid-word). Nothing pending here  -  noting it as resolved specifically because
the instruction to write this file described it as still open; it was open
when that instruction was drafted and isn't anymore.

## Found the hard way  -  things a fresh session would otherwise rediscover

- **`assets/css/extended/economics.css` already existed** before this
  session touched it, with a working `.aside` component (`+`/`-` marker,
  hover/focus-visible states, reduced-motion handling). The Phase 1 audit
  only read `custom.css` and missed it. First attempt at the aside redesign
  wrote a second, higher-specificity-losing `.aside` ruleset into
  `custom.css` that silently never rendered because the real file's rules
  won the cascade. **Read both CSS files before touching aside/figure
  styling.**
- **Two separate `.dark`-class bugs**, same root cause, found and fixed in
  this session: this site stamps `data-theme="dark"` on `<html>`, never a
  literal `.dark` class. `economics.css` had `.dark { --fig-subject: ...; }`
  (dead since written). `custom.css` had the same pattern on `--accent`/
  `--pos`/`--neg`  -  meaning dark mode had been silently using the *light*
  accent color (`#446485`, 2.71:1 contrast on the dark background  -  a real
  WCAG AA failure) site-wide, on every link and badge, for however long
  that CSS existed. Both fixed to `[data-theme="dark"]`. **If you add a new
  dark-mode override anywhere on this site, it must target
  `[data-theme="dark"]`, never a `.dark` class  -  that selector has never
  once worked here.**
- **Hugo Modules vs. a direct theme clone render identically** for this
  theme (confirmed: both resolve PaperMod to the exact same commit,
  `d3768854d00a`). The Phase 1 "article is ~32 screens / desktop is
  left-aligned" discrepancy against the checker's numbers was **not** a
  build-method difference  -  it was two measurement bugs in the Phase 1
  screenshot script (an unaccounted `device_scale_factor=2` doubling the
  apparent pixel height, and an eyeballed-not-measured alignment claim).
  Real numbers: ~16 screens, centered. Still use real Hugo Modules going
  forward (Go is now installed) since it costs nothing and matches CI
  exactly  -  just don't assume a discrepancy means the modules path is
  broken.
- **`hugo mod get` / any `hugo` command that resolves modules rewrites
  `go.mod` and creates `go.sum`.** Neither should ever be committed  -  CI's
  own `hugo mod get` step regenerates them fresh every run. If `git status`
  shows them dirty, `git checkout -- go.mod && rm -f go.sum` before
  committing anything.
- **`partialCached` in the theme's `baseof.html` can serve a stale render**
  across a `hugo server` session when only the cached partial's *template*
  changes (header.html edits didn't show up until the server was
  restarted, twice, during this session). If a template edit isn't
  appearing in the live preview and there's no build error, restart the
  server before debugging further.
- **`handoff/` in the repo root is untracked, pre-existing, and not part of
  this branch's work**  -  a stray `.gitignore` addition for it exists
  uncommitted on `update-project-md-item2` (now merged to `main`), stashed
  rather than applied. Per CLAUDE.md, `SESSION_SUMMARY.md`-style files are
  exactly the kind of machine-facing content that must never reach
  `content/` or get published. It was left alone all session  -  never
  staged, never read beyond confirming what it was. Whoever owns that
  stash should either commit the `.gitignore` line or delete the directory;
  it doesn't belong to Phase 2's scope either way.
- **The three chart-source repos are not uniform.** `hdb-affordability` and
  `gst-passthrough` both have `THESIS.md`/`RESULTS.md`, but in genuinely
  different formats (a markdown summary table vs. a plain-text verdict
  block with different test-numbering conventions)  -  there is no single
  regex or parser that reads both. `coe-analysis` has neither. Any future
  attempt to fully automate the method strip across all posts needs to
  design for this, not assume one format.

## What Phase 3 is

Chart unification  -  one shared visual language across the three figure
scripts (`07_figures.py` in `hdb-affordability`, `09_figures.py` in
`coe-analysis`, `12_figures.py` in `gst-passthrough`). Confirmed in the
Phase 1 audit with real evidence: the three repos currently use three
different CSS-variable naming conventions, three different accent colors
(steel blue `#2a78d6`, rust red `#a32a1e`, a different blue `#0b6bcb`), two
font stacks, and three legend conventions. Explicitly **not started**  - 
Jacob said not to restyle charts in Phase 2, and nothing in this branch
touches any of the three repos' Python scripts or the SVGs in
`static/figs/`. `assets/css/extended/economics.css` already has
`--fig-subject`/`--fig-context`/etc. tokens tied to the page's own theme
variables, which reads like early infrastructure for this  -  but those
tokens can't currently reach the chart SVGs at all, since they're embedded
via `<img src>`, which is a fully isolated document with no access to the
parent page's CSS. Whatever Phase 3 does, it has to either inline the SVGs
(bigger change, touches every post) or bake the unified palette directly
into each Python script's own literal output (smaller change, keeps the
`<img>` embedding as-is). That choice hasn't been made and isn't implied by
anything currently in this repo.

## Phase 3 status  -  in progress, four PRs open, none merged

Started after Phase 2 merged, per Jacob's own sequencing instruction. The
open question from the section above  -  inline the SVGs, or bake the
palette into each script's own literal output  -  is resolved: **baked into
each script**, so the `<img src>` embedding stays exactly as-is and no post
template changes.

**Shared token set** (WCAG AA verified against both surfaces, light
4.6-4.8:1, dark 4.7-4.9:1): `--fig-ink`, `--fig-ink-2`, `--fig-ink-3`,
`--fig-rule`, `--fig-surface`, `--fig-subject`, `--fig-context`. Same
names, same hex values, in all three repos' figure scripts.

**Canvas and type**, all three repos: viewBox width 640-660px -> 480px,
base text 10.5-11px -> 14px. Effective on-screen size at 390px measured with
real Playwright rendering (not estimated): was ~5.7-6.4px depending on the
chart, now **11.38px on every chart, all twelve of them**.

**All twelve charts converted**, three repos, three open PRs (not merged):

- `hdb-affordability` PR #13  -  3 charts. Rename and recolor only; the
  480px canvas itself was already merged earlier as PR #10
  (`mobile-charts`)  -  a stale-branch correction caught this mid-session,
  see the commit history if picking this up cold.
- `coe-analysis` PR #1  -  7 charts across `09_figures.py` (mechanism,
  indexed, decomposition, gap_distribution), `motorcycles/14_figures.py`,
  and `win-rate/12_figures.py`. This repo's charts had **never once
  rendered in dark mode**  -  zero `prefers-color-scheme` occurrences
  anywhere before this PR  -  found by grep, not by eye, then fixed
  everywhere at once as part of the same token rename.
- `gst-passthrough` PR #1  -  3 charts (`fig1-signal-vs-noise`,
  `fig2-water-supply`, `fig3-still-prices`).
- `financing/23_figures.py` on `hdb-affordability`'s `financing-wip`
  branch was **not touched**, per explicit instruction  -  that branch is
  mid-Checkpoint 2, and the token rename there happens after it merges to
  `hdb-affordability` main.

**Real layout bugs, found only by rendering the new size, not by reading
the code:** `mechanism.svg` had a label overlapping the x-axis and a curve
line striking through its own label, both from margins tuned for the old
660px canvas. `gst-passthrough`'s fig1 had a bar-annotation label running
off the right edge at the new width, moved below the bar instead of beside
it. fig3 had two long captions doing the same thing, split across two lines
each at a natural clause break, wording unchanged (checked by literal
concatenation against the original single-line strings, not by eye).

**This website PR** copies all twelve regenerated SVGs into `static/figs/`
and re-screenshots every affected article at 390px, both color schemes:
`2026-08-22`, `2026-08-29`, `2026-09-05`, `2026-09-08`, `2026-09-12`,
`2026-09-19`. All clean in both modes.

**A pre-existing issue found along the way, not caused by this work and not
fixed here:** `gst-passthrough`'s `CHECKSUMS.md5` has four `out/*.csv`
files (`category_2023.csv`, `category_2023_cny.csv`,
`event_estimates.csv`, `lownoise_2023.csv`) that fail verification even
on a genuinely fresh clone with `requirements.txt`'s exact pinned
dependency versions. Not a scipy version mismatch (checked with the exact
pin) and not run-to-run randomness (stable across in-place reruns, no
random/seed/bootstrap code in the four scripts that produce them). All four
come from scripts doing regression/statistical estimation, so this looks
like platform-level floating-point rounding (BLAS/LAPACK backend)
differing at the last printed decimal between whatever machine originally
committed `CHECKSUMS.md5` and this one. Flagged for the GST audit; not
something this round of work touches.

## Exact next steps

1. **Jacob reviews and merges the three figure-repo PRs**  -  `hdb-affordability`
   #13, `coe-analysis` #1, `gst-passthrough` #1  -  in whatever order suits
   him; they don't depend on each other.
2. **Jacob reviews and merges this website PR.** It doesn't strictly depend
   on the three repo PRs merging first  -  the copied SVGs are self-contained
   files, already regenerated and already in `static/figs/`  -  but merging
   the source repos first keeps each repo's own git history the record of
   truth for its own chart, which is the cleaner order.
3. **Still open, not yet raised for a decision:** whether `gst-passthrough`
   should get its `RESULTS.md` transcribed into that post's front matter so
   its method strip can appear too  -  nobody has done this yet, and it's a
   one-post, ~15-minute job once someone reads that file's verdict block
   format.
4. **Still open, explicitly deferred in the original Phase 1 brief:**
   whether the Stocks section belongs on a site that's otherwise all
   Singapore policy. Not Claude's call; raise it with Jacob separately.
5. **Still open, found during the Phase 3 pass, not fixed:** the
   `gst-passthrough` `CHECKSUMS.md5` drift on four `out/*.csv` files,
   described above. Goes into the GST audit, not this round.
