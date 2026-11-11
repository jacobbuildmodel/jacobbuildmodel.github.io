# Type: design note

12 November 2026. Pull request 64 (draft), branch `fix-heading-scale`. This note began as the
type lab's comparison for Jacob. He chose option B on 12 November ("B: Newsreader + Inter",
then "Do it now"), so it is now the record of that choice and of what was built from it.

## 0. What the pull request does

| | Change | Status |
|---|---|---|
| a | Newsreader for headlines, standfirst and prose; Inter for the interface | Jacob's choice of 12 November, now the default on every page |
| b | The digits of JetBrains Mono for numbers in tables, the method strip, the decision strip and the scorecard table | Part of option B as shown |
| c | The section-heading mark "label line plus rule", and the size ladder | The default he was shown (part 1) |
| d | The warm light page | Its own commit, 9ccab6f; reverting that commit brings the white page back and touches nothing else |

The lab itself is gone from the code: options A and C, the switcher page, its script, the
attribute-driven style blocks and the old font files. The comparison pictures stay in
`office/type-lab/shots/` as the record. Nothing on the site now depends on an attribute.

Four things were changed after the lab pictures, all found in the page check (part 6):
the label line is applied only on article pages; a wide hyphen in the method strip is fixed;
two more preloads; fallback faces for the italic and the semibold.

## 1. Section headings and sizes

### The mark

Three candidates were drawn and looked at on the 31 October article at phone width, light and
dark: `shots/compare_heading-marks_light-dark.png`.

| | Candidate | What it does |
|---|---|---|
| 1 | Label line and rule (shipped) | A heading written "Label: finding" is set as a small capitals label in navy, the finding under it in the serif, then a short thick navy rule (48 x 3 px). A heading with no colon gets the rule alone. |
| 2 | Rule under | The heading as written, then the same short rule. |
| 3 | Rule over | A hairline across the column with the short rule on its left end, then the heading. |

Shipped: candidate 1. The heading can be told from body text by three things at once (a label
in another face and colour, a larger bold line, the rule), and "The argument: one floor for
everyone, or a ladder for each job" drops from three lines to two on a phone, because the
label leaves the line. Candidates 2 and 3 were removed from the stylesheet with the lab; the
picture shows them.

How it is built:

- `layouts/_default/_markup/render-heading.html`, one small render hook. For a level-2 heading
  whose label is 2 to 30 plain characters before the first colon it writes two spans inside
  the same H2. Everything else is written as Hugo writes it.
- Changed on 12 November: the split now applies only in the sections `economics` and `open`
  (articles and open questions), where "Label: finding" is the house style. Before, it also
  caught one entry on the scorecard, "COE or ERP: which one actually keeps Singapore's roads
  moving?", and set "COE or ERP" as a label while the other four question titles on that page
  stayed whole. That heading is whole again.
- The words do not change. The colon stays in the text, in its own span, hidden from the eye
  only; the capital first letter of the finding is drawn by the stylesheet, not typed.
- Checked on 12 November on a normal build (no drafts) of this branch against a normal build
  of `main`: 47 HTML files on both sides; in every one the heading words, ids, "#" anchors,
  the table of contents and the whole visible text are identical (225 headings, 18 of them
  split: 11 in the 31 October article, 7 on two open-question pages); the 8 XML files (RSS
  feeds and sitemap) are byte-identical. The comparison is
  `python tools/type_page_check.py compare <main build> <branch build>`.
- The rule is drawn by the heading (`::after`) on every H2 inside `.post-content`. Looked at,
  at phone width, on all ten page types of part 6. The home page has no such heading. H3 has
  no mark.

### The ladder

Before, on a phone (390 px): title 28, standfirst 22, H2 23.5, H3 20.5, body 18.9. Now each
step is about a fifth larger than the one below, and each step also differs in face, weight
or colour:

| Step | Phone (390 px) | Desktop (1280 px) | Was (phone) |
|---|---|---|---|
| Title | 30/36 serif 600 | 40/46 | 28/34 |
| Standfirst | 19.5/28 serif italic | 22/32 | 22/33 |
| H2 | 25/30 serif 600, label 13 caps, rule | 30/36, label 14 | 23.5/29 |
| H3 | 21/27 serif 600 | 24/31 | 20.5/27 |
| Body | 18.9/30 | 18.9/30 | unchanged |
| Table | 17.4 | 17.4 | unchanged |
| Method strip | 14, note 13.5 | same | unchanged |

Measured in the browser on 12 November on nine page types (the home page has no article
body): title 30, H2 25, body 18.9 at 390 px; 39.8, 29.9, 18.9 at 1280 px. None of the ten
pages checked has an H3. The title of a section page ("How the scorecard works", "Economics")
uses the article title rule.

## 2. The typeface

### What was compared

| | Faces | Outcome |
|---|---|---|
| A | Source Serif 4 and Source Sans 3 (own subsets, named "NVD Serif" and "NVD Sans") | The site until this pull request. Removed. |
| B | Newsreader for headline, standfirst and prose; Inter for the interface; the digits of JetBrains Mono for numbers in tables and strips | Chosen by Jacob, 12 November 2026. |
| C | Playfair Display for title and section headings; Lato for standfirst, prose and interface | Not chosen. Removed. |

Pictures of the three side by side: `shots/compare_a-top_A-B-C.png`,
`compare_b-section_A-B-C.png`, `compare_c-count_A-B-C.png`.

### Sizes

Each face is scaled with `size-adjust` in its `@font-face` so that its x-height (the height
of a lowercase x, which is what makes text look large or small) is close to the face it
replaced, and it is given the line metrics of that face (`ascent-override`,
`descent-override`), so every size and line box set elsewhere in the stylesheets holds.

| Face | x-height as drawn | Scale | x-height shown | Face it replaced |
|---|---|---|---|---|
| Newsreader | 0.426 | 108% | 0.460 | 0.475 |
| Inter | 0.546 | 90% | 0.491 | 0.486 |
| JetBrains Mono digits | 0.550 | 90% | 0.495 | |

Newsreader was first set at 110%. Its capitals and ascenders are taller, so the page read a
size larger; 108% looked level. Body text stays 18.9 px with line height 1.6.

`size-adjust` works in Chrome and Firefox from version 92 and in Safari from 17. An older
iPhone draws the faces at their natural size: Newsreader about 7 per cent smaller, Inter
about 11 per cent larger. Accepted for now and not tested (part 8).

### Figures

Newsreader's figures are tabular as drawn (every digit 1133 of 2000 units wide). In tables,
the method strip, the decision strip and the scorecard the digits 0 to 9 come from JetBrains
Mono through a `unicode-range` face (token `--font-figures`); letters and punctuation stay in
Inter, and table text is Inter, not the serif. Prose figures are not touched. Measured in the
browser: ten 1s and ten 0s are the same width in table cells, table headers, the method strip
and the decision strip.

Changed on 12 November, after the lab pictures: Inter's tabular-figures feature (`tnum`,
which the site switches on for these blocks) also sets the hyphen on a digit's width (942 to
1328 of 2048 units). In the lab pictures of option B that pulled hyphenated words apart in
the method strip: "PRE - REGISTERED", "RE - CHECK DUE". The digits are fixed-width by their
own face, so the feature is now switched off for these blocks (`font-feature-settings` in
`00-tokens.css`). A hyphenated word in the strip is measured the same width with and without
the site's rules. `shots/final_before-after_article.png` shows the strip as it is now.

## 3. Fonts shipped, and their licences

Seven files in `static/fonts/` (sources and sha256 in `FONTS.csv`):

| File | Bytes | What |
|---|---|---|
| newsreader-latin-400-normal.woff2 | 22,480 | Fontsource Latin subset of Newsreader 1.003 (16pt optical size), unchanged |
| newsreader-latin-400-italic.woff2 | 24,340 | the same, italic |
| newsreader-latin-600-normal.woff2 | 23,876 | the same, semibold |
| inter-latin-400-normal.woff2 | 23,664 | Fontsource Latin subset of Inter 4.001, unchanged |
| inter-latin-600-normal.woff2 | 24,452 | the same, semibold |
| jetbrains-mono-digits-400.woff2 | 1,204 | the digits 0 to 9 cut from Fontsource's JetBrains Mono 2.211 Latin file |
| jetbrains-mono-digits-700.woff2 | 1,188 | the same, bold |

Licences. Each family's licence text is beside the files (`Newsreader-LICENSE.md`,
`Inter-LICENSE.md`, `JetBrainsMono-LICENSE.md`), each with a first paragraph saying which
files it covers and what was done to them.

| Family | Licence | Copyright line | Reserved Font Name | So |
|---|---|---|---|---|
| Newsreader | SIL Open Font License 1.1 | Copyright 2020 The Newsreader Project Authors | none declared | a subset may keep the name |
| Inter | SIL Open Font License 1.1 | Copyright 2016 The Inter Project Authors (the licence copy shipped says 2020; both notices are in `Inter-LICENSE.md`) | none declared | a subset may keep the name |
| JetBrains Mono | SIL Open Font License 1.1 | Copyright 2020 The JetBrains Mono Project Authors | none declared | a subset may keep the name |

How this was checked on 12 November: the first line of each shipped licence text; the
copyright record inside each of the seven font files (it names no reserved name); and the
licence file at the head of each upstream repository, read through the GitHub API
(`rsms/inter` LICENSE.txt, `productiontype/Newsreader` OFL.txt, `JetBrains/JetBrainsMono`
OFL.txt): in all three the words "Reserved Font Name" appear only in the licence's own
definitions and conditions, never after the copyright line. No file had to be renamed.
The OFL asks that the copyright notice and the licence travel with the fonts: they do.

Removed: the five NVD files, their two licence notes and `tools/make_nvd_fonts.py`, which
only made those files. Still in the repository and still needed, untouched: the Source Serif
4 and Source Sans 3 files in `research/paper-template/fonts/` (paper template, portfolio
PDF) and `assets/share/SourceSans3-Bold.ttf` (share cards). Those are the original files
under their own names, with their licences beside them.

## 4. Fallback faces, preloads, layout shift, page weight

### Fallback faces

While a web font is on its way the text is drawn in Georgia or Arial, resized so that the
swap moves as little as possible (`00-tokens.css`). Recomputed on 12 November by
`python tools/type_tools.py metrics <built site>` from the shipped files and the Georgia and
Arial of Windows 11. size-adjust is the web face's average letter width, times its own
size-adjust, over the fallback's average width, with the widths weighted by the visible text
of the built site (227,266 characters); ascent and descent are the line metrics divided by
that size-adjust; line gap 0.

| Web face | Fallback | size-adjust | ascent | descent |
|---|---|---|---|---|
| Newsreader 400 | Georgia | 104.00% | 99.61% | 32.21% |
| Newsreader 400 italic | Georgia Italic | 95.87% | 108.07% | 34.94% |
| Newsreader 600 | Georgia Bold | 94.01% | 110.20% | 35.64% |
| Inter 400 | Arial | 96.14% | 104.02% | 33.91% |
| Inter 600 | Arial Bold | 91.47% | 109.32% | 35.64% |

Weighted by plain English letter frequency instead, the two regular values would be 103.69%
and 96.60%, the numbers the lab used. The italic and the semibold got faces of their own
because one regular fallback for all three made the title and the standfirst wrap
differently before and after the swap (the article row "390 px, fonts held back" below).

A direct test: with every font replaced by its fallback, the 31 October article is 32 px
taller at 390 px (13,699 to 13,731; 2 of 55 text blocks change height) and 30 px taller at
1280 px (1 of 55). Where Georgia or Arial is not installed (Android, most Linux) the next
family in the stack is used, unsized; not tested.

### Preloads (`layouts/partials/extend_head.html`)

The rule is the one the file already followed: a face is preloaded where the page uses it
above the fold.

| Face | Preloaded on |
|---|---|
| Newsreader 400, Inter 400, Inter 600 | every page |
| Newsreader 600 | single pages, and now also section and tag list pages (their title is in the serif since 11 November) |
| Newsreader 400 italic | single pages that show a standfirst |
| JetBrains Mono digits 400 | new: pages with a method strip or a decision strip |

Checked on the build: all 30 pages; a page has the Newsreader 600 preload exactly when it
has a serif title, and the digit preload exactly when it has a strip. In the browser, on the
ten page types at both widths, every face used in the first screen is preloaded, with one
exception: on About at 1280 px a line of italic in the body is in the first screen and the
italic is not preloaded there (the same was true before this change).

### Layout shift

Chrome, in the app's built-in browser, on local servers that forbid caching, one load per
cell unless stated. "Held back" means every font file was delayed by 400 ms, so the page is
drawn in the fallback faces first and then swaps: the hard case, and the one a phone on a
slow connection sees. Each load also made one deliberate shift to prove the counter was
running (it read 0.14 at 390 px and 0.06 at 1280 px).

| Page, width | Before (main) | After (this branch) |
|---|---|---|
| Article, 390 px | 0 | 0 |
| Home, 390 px | 0 | 0 |
| Article, 1280 px | 0.0036 | 0.0003 (three loads: 0.00026, 0.00025, 0.00025) |
| Home, 1280 px | 0 | 0.0001, then 0 on a second load |
| Article, 390 px, fonts held back | 0.0021 | 0.0007 (0.0176 with one regular fallback, before the italic and semibold fallbacks) |
| Home, 390 px, fonts held back | 0 | 0 |
| Article, 1280 px, fonts held back | 0.0036 | 0.0003 |
| Home, 1280 px, fonts held back | 0.096 | 0.0001 |

The site's earlier figure of 0 was measured on 5 November in another set-up; in this one the
article at 1280 px reads 0.0036 before the change, so compare the two columns, not this table
with that figure. What still moves on the article at 1280 px: one item of the method strip
slides 13 px sideways when Inter replaces Arial under the letter-spaced capitals of the
labels. Also measured: the 17 October article at 1280 px, 0.0002; the LTA decision page at
1280 px, 0.

### Font bytes transferred

| Page | Before | After |
|---|---|---|
| Article (/economics/2026-10-31/) | 97,404 (5 files) | 120,016 (6 files) |
| Home | 59,436 (3 files) | 70,596 (3 files) |
| LTA decision page | not measured | 95,676 (5 files) |

The bold digit file (1,188 bytes) is fetched only where a table header has digits.

## 5. The light theme (commit 9ccab6f)

The reader said the dark theme is good and the white one is not. The dark theme has three
levels (page #1d1e20, card #26282c, panel #2b2d32) and soft text. The light theme had one
level, pure white for page and card, with the hardest text contrast on the site (17.7:1).
Light now has the structure dark has: a warm off-white page, white cards that stand off it,
slightly softer ink, and borders that can be seen. The dark theme is not touched. Pictures:
`shots/compare_paper_type-b.png`, `shots/final_*_light.png`.

Seven values change, six in the light block of `00-tokens.css` and `--pos` in `custom.css`.

| Token | Was | Now |
|---|---|---|
| `--paper` (page) | #ffffff | #f6f3ec |
| `--code-bg` (panels) | #f4f7f9 | #fdfcf9 |
| `--ink` | #15191e | #1b1f24 |
| `--ink-3` (meta) | #5f6873 | #59616b |
| `--accent` (links) | #3d6c8c | #35627f |
| `--pos` (passed) | #2E7D5B | #2a7354 |
| `--line` (borders) | #c5ccd4 | #b3ab9b |

Contrast of every light-theme text colour, WCAG 2, from
`python tools/type_tools.py contrast`, which reads the values out of the stylesheets:

| Text colour | Hex | On the page #f6f3ec | On a card #ffffff | On a panel #fdfcf9 |
|---|---|---|---|---|
| `--ink` | #1b1f24 | 14.94 | 16.56 | 16.14 |
| article prose (the theme's own) | #1f1f1f | 14.87 | 16.48 | 16.07 |
| `--ink-2` | #3f4852 | 8.38 | 9.29 | 9.06 |
| `--ink-3` | #59616b | 5.66 | 6.27 | 6.12 |
| `--accent` | #35627f | 5.91 | 6.55 | 6.39 |
| `--navy-text` | #1f3a5f | 10.36 | 11.48 | 11.19 |
| `--pos` | #2a7354 | 5.15 | 5.71 | 5.56 |
| `--neg` | #8A6116 | 4.98 | 5.52 | 5.38 |
| figure red | #a32a1e | 6.52 | 7.22 | 7.04 |
| LTA accent | #c2410c | 4.67 | 5.18 | 5.05 |

On the navy band (unchanged): wordmark 11.48, menu 8.94. Borders, not text: 2.06 on the
page, 2.28 on a card. Lowest text ratio 4.67; nothing under 4.5.

The same was measured on the rendered pages: a script walked every piece of visible text on
the ten page types, at both widths, and compared its colour with the colour behind it.
Lowest ratio per page in light: 4.67 on the LTA decision page, 5.38 on the article, 5.66 on
the other eight. In dark: 5.17 at the lowest. No text under 4.5 in any of the 40 states.

Not done: the chart pictures keep their own white backgrounds; the browser bar colour
(`theme-color`) is one value for both themes in the theme and was left alone.

## 6. The page check (12 November)

Build: `hugo --baseURL http://localhost:1324/ -d <folder>`, no drafts, served with
`python -I -m http.server 1324 --bind 127.0.0.1`. Pages: the home page, /economics/,
/economics/2026-10-31/, /open/2026-09-26-coe-or-erp/, /scorecard/, /process/,
/process/economics/, /about/, /decisions/lta-coe-categories/, /corrections/. Each at 390 and
1280 px, light and dark: 40 states, each loaded in a frame of that width in the app's
built-in browser (Chrome); the frame page is written by
`python tools/type_page_check.py harness <build>`. The run was made twice, once with a 15 px scrollbar inside the
frame (so 375 and 1265 px of page) and once without.

| Check | Result |
|---|---|
| Horizontal scroll | none in 40 states |
| Console errors | none on the ten pages, opened one by one at 390 px |
| Font files that failed to load | none |
| First font family of title, standfirst, H2, label, body, table cell, table header, strips, menu, meta, footer | Newsreader, Inter or the digit face as designed, on every page; the only other family anywhere is the monospace of `code` |
| Title larger than H2 larger than body | yes on the nine pages that have them |
| Digits the same width in tables and strips | yes wherever a table or strip exists |
| Heading mark | every H2 in a page body has the rule; the label line appears on the article only (11 of 14 headings); nothing split on the other nine pages |
| Characters without a glyph | one, see below |

The web fonts hold every character the built site uses except one: the right arrow in
"Repository" + arrow, the link at the end of the method strip on the four articles that have
a strip (U+2192, four uses in the whole build). The Fontsource Latin subset of Inter has the
up and down arrows but not the left and right ones; the old NVD files had all four. The arrow
is therefore drawn by the next family in the stack, the Arial-based fallback on Windows, Mac
and iPhone (it is in both pictures of `final_before-after_article.png`). To close it: cut
own subsets from the upstream Inter files with the arrow in them. Not done here.

Pictures of all ten page types at 390 px, light and dark, were looked at as sheets; the six
kept are `shots/final_*.png`.

## 7. References

Two statements were confirmed by fetch on 11 and 12 November and are used above:

- Body size. GOV.UK sets body text at 19 px with 25 px lines on small and large screens, on
  a scale it says was tested for reading on different devices
  (design-system.service.gov.uk/styles/type-scale/). The site's 18.9 px is in line with that.
  The same scale, where every heading step is smaller than the one above it on every screen,
  is the model for the ladder.
- Line length. Butterick, Practical Typography, advises an average line of 45 to 90
  characters, spaces included (practicaltypography.com/line-length.html). At 390 px the body
  runs about 42 characters a line, just under; a smaller body size would fix that and cost
  legibility, so nothing was changed.

The rows this note once carried for the Financial Times, The Economist, The Guardian and Our
World in Data were written from memory. On 12 November four look-ups were allowed to confirm
them; all four failed on an error in the search command, before any result was read. The
rows, and the sentences that leaned on them, have been deleted. Nothing in this note or in
the pull request now rests on them.

## 8. Not checked, and known gaps

- No real phone. Every picture is desktop Chrome in headless mode drawing a frame 390 px
  wide at twice the pixel density; the measurements are Chrome on Windows 11.
- No Safari and no Firefox. `size-adjust`, `:is()`, `clamp()` and `font-feature-settings` are
  supported in current versions by their documentation, not by test here. Safari before 17
  ignores `size-adjust` (part 2).
- No Android: there Georgia and Arial are missing, so the fallback faces are not the sized
  ones and the swap may move more than measured.
- No readers. Nobody from the target group has seen the result.
- The right arrow (part 6).
- Layout shift is one load per cell, on a local server (part 4).
- The Fontsource files were taken as published (sha256 in `FONTS.csv`); their glyphs were
  not compared with the upstream releases.
- Tablet widths were not looked at.
- The corrections page has no entry for this change yet: it must carry the merge date, so it
  is a step for merge day.

## Files

| File | What |
|---|---|
| `assets/css/extended/00-tokens.css` | the faces, the fallback faces, the font tokens, the figures rule, the light and dark colours |
| `assets/css/extended/custom.css`, `masthead.css` | the heading mark and the ladder; `--pos` |
| `layouts/_default/_markup/render-heading.html` | the heading hook |
| `layouts/partials/extend_head.html` | the preloads |
| `static/fonts/` | the seven font files and three licences |
| `office/type-lab/FONTS.csv` | every font file the lab used: source, bytes, sha256, licence, and whether it ships |
| `office/type-lab/shots/` | the lab's comparison pictures (`compare_*`, and the single views) and the six `final_*` pictures |
| `tools/type_tools.py` | how the numbers and the final pictures were made: `metrics`, `chars`, `contrast`, `csv`, `digits`, `serve`, `shots` |
| `tools/type_page_check.py` | the page check: `compare` (headings, anchors, contents, text and feeds against another build) and `harness` (the 40-state check page) |

The lab's own scripts (`tools/make_type_lab_fonts.py`, `type_lab_shots.py`,
`type_lab_contrast.py`, `make_type_lab_preview.py`) and `tools/make_nvd_fonts.py` were
removed with the lab; they are in the history at commit 3d0c789.
