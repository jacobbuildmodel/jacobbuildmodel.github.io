# Type lab: design note

12 November 2026. Draft pull request 64, branch `fix-heading-scale`. For Jacob to decide.

This note covers two things on the same branch:

1. What changes on every page if the pull request is merged: the section-heading mark and the
   size ladder (part 1). These are the answer to "make the header obvious" and "the sizing
   looks weird".
2. What is only offered, and changes nothing until Jacob picks: three typeface options and a
   light-theme proposal (parts 2 to 6).

Pictures are in `office/type-lab/shots/`. The phone file is
`office/fable52/type_lab_preview.html` in the WEBSITE folder (435 KB, no script, no outside
request).

## 1. Section headings and sizes (the default, for every option)

### The mark

Three candidates were drawn and looked at on the 31 October article at phone width, light and
dark: `shots/compare_heading-marks_light-dark.png`.

| | Candidate | What it does |
|---|---|---|
| 1 | Label line and rule (shipped) | A heading written "Label: finding" is set as a small capitals label in navy, the finding under it in the serif, then a short thick navy rule (48 x 3 px). A heading with no colon gets the rule alone. |
| 2 | Rule under | The heading as written, then the same short rule. |
| 3 | Rule over | A hairline across the column with the short rule on its left end, then the heading: the way a newspaper opens a section. |

Shipped: candidate 1. Reasons: the heading can be told from body text by three things at once
(a label in another face and colour, a larger bold line, the rule), so it does not depend on
size alone; "The argument: one floor for everyone, or a ladder for each job" drops from three
lines to two on a phone, because the label leaves the line; and the label-over-headline
pattern is one newspapers already use, so it reads as editorial, not as decoration. Candidates
2 and 3 are one attribute away in the lab (`data-head="u"` and `data-head="o"`), if Jacob
prefers the plainer look.

How it is built:

- `layouts/_default/_markup/render-heading.html`, one small render hook. For a level-2 heading
  whose label is 2 to 30 plain characters before the first colon, it writes two spans inside
  the same H2. Everything else is written as Hugo writes it.
- The words do not change. The colon stays in the text, in its own span, hidden from the eye
  only; the capital first letter of the finding is drawn by the stylesheet, not typed.
- Checked on a build without drafts against the branch as it was: 47 pages before and after;
  the visible text of every page is identical; the only HTML differences are the stylesheet
  file name and the heading spans; every heading id and "#" anchor is the same (274 headings,
  32 of them split); the RSS feed is byte-identical.
- The rule is drawn by the heading (`::after`), so it takes its space with the heading. No
  image, no script.
- The mark applies to H2 inside `.post-content`. Looked at, at phone width: two economics
  articles, the scorecard, How it works, About, the Economics list, an open question, the LTA
  decision page and the researchers page. It does not reach the home page (no such heading
  there). H3 has no mark.

### The ladder

Before, on a phone (390 px): title 28, standfirst 22, H2 23.5, H3 20.5, body 18.9. Five steps
inside a ratio of 1.5, and the standfirst nearly the size of a section heading. That is the
"weird". Now each step is about a fifth larger than the one below (the "minor third" of type
scales), and each step also differs in face, weight or colour:

| Step | Phone (390 px) | Desktop (1280 px) | Was (phone) |
|---|---|---|---|
| Title | 30/36 serif 600 | 40/46 | 28/34 |
| Standfirst | 19.5/28 serif italic | 22/32 | 22/33 |
| H2 | 25/30 serif 600, label 13 caps, rule | 30/36, label 14 | 23.5/29 |
| H3 | 21/27 serif 600 | 24/31 | 20.5/27 |
| Body | 18.9/30 | 18.9/30 | unchanged |
| Table | 17.4 | 17.4 | unchanged |
| Method strip | 14, note 13.5 | same | unchanged |

Title > H2 > H3 > body holds at every width (each is a `clamp` between the two columns).

One more thing found while checking: the title of a section page ("How the scorecard works",
"Economics") was still the theme's system sans at 40 px on a phone, a third larger than an
article title and in another face. It now uses the article title rule.

## 2. The three typeface options

Switch: `data-type="b"` or `"c"` on `<html>` (`assets/css/extended/zz-type-lab.css`); no
attribute is option A. The candidate faces are in `static/fonts/lab/` and are fetched only
when an option is on.

| | Faces | What it is for |
|---|---|---|
| A | Source Serif 4 and Source Sans 3 (the "NVD" files), as now | The safe choice. Sturdy, plain, already licensed, subset and measured. |
| B | Newsreader for headline, standfirst and prose; Inter for the interface; the digits of JetBrains Mono for numbers in tables and the method strip | What Jacob asked for on 3 November. A newspaper text face with more character in the italic and the headline; a clearer interface sans; numbers that look like data. |
| C | Playfair Display for the title and section headings; Lato for the standfirst, prose and interface | The different one: reading text in a sans, the way phone apps are set, with a high-contrast display serif only where it is large. From memory this is also the pairing Our World in Data uses. |

On Playfair in option B: Jacob named Newsreader or Playfair Display. Newsreader is used for
both headline and prose in B. Playfair is a display face with hairline strokes; it does not
hold at standfirst or body size, and using it only for the headline would add a fourth family
to B. It is shown where it works, as the headline face of C.

### Sizes used, so the comparison is fair

Each candidate is scaled so its x-height (the height of a lowercase x, which is what makes
text look large or small) is close to the current face, with `size-adjust` in its
`@font-face`. The line metrics of the current faces are copied onto the candidates
(`ascent-override`, `descent-override`), so every line box is built as today and only the
letterforms differ. Numbers from `python tools/make_type_lab_fonts.py metrics`.

| Face | x-height as drawn | Scale | x-height shown | Against A |
|---|---|---|---|---|
| NVD Serif (A, prose) | 0.475 | 100% | 0.475 | |
| Newsreader (B, prose) | 0.426 | 108% | 0.460 | 97% |
| Lato (C, prose) | 0.506 | 96% | 0.486 | 102% |
| NVD Sans (A, interface) | 0.486 | 100% | 0.486 | |
| Inter (B, interface) | 0.546 | 90% | 0.491 | 101% |
| JetBrains Mono digits (B) | 0.550 | 90% | 0.495 | |
| Playfair Display 700 (C, headings) | 0.514 | 95% | 0.488 | 102% of NVD Serif Semibold |

Newsreader was first set at 110% (x-height within 1 per cent of A). Its capitals and
ascenders are taller, so the page read a size larger than A; 108% looked level.

Body text is 18.9 px with line height 1.6 in all three. Estimated characters per line on a
390 px phone (column 362 px, from each face's average letter width): A 43, B 42, C 47.

Figures: tables, the method strip and the scorecard keep tabular lining figures in all three
(Source and Lato figures are tabular as drawn; Inter and Newsreader through
`font-variant-numeric`, already set by the site). In B the digits 0 to 9 in tables, the
strips and the count band come from JetBrains Mono through a `unicode-range` face; letters
and punctuation stay in Inter, and table text is Inter, not the serif. Prose figures are
not touched.

Fallbacks: each candidate has a fallback face (Georgia or Arial) sized by average letter
width, the method `00-tokens.css` already uses, so the swap from fallback to web font keeps
line breaks close.

### Measured page weight

Font bytes on the article page /economics/2026-10-31/, counting the files the page actually
drew with (read from the browser's loaded-fonts list):

| Option | Files | Bytes |
|---|---|---|
| A | 5 | 97,404 |
| B | 6 (a seventh, 1,188 bytes, only where a table has bold figures) | 120,016 |
| C | 4 | 94,252 |

In the lab, options B and C load on top of A's preloaded files; the figures above are what a
page would carry after adoption. Option A's own cost on this branch: no font change; the
stylesheet grows from 42,530 to 45,040 bytes (9,585 to 10,097 gzipped) for the heading mark,
the ladder and 1,731 bytes of lab rules. The lab script is written only into a build with
drafts; a normal build has it on 0 of 47 pages.

## 3. References

Jacob asked for the choice to be checked against sites and articles. Six fetches were allowed.
Two confirmed a statement; four failed (two sites refuse requests from this tool, two source
files were not at the address tried). Statements marked "from memory" were not confirmed
today and need a look before anyone quotes them.

| Publication | Headlines | Body | Numbers and interface | Source |
|---|---|---|---|---|
| GOV.UK | GDS Transport (sans) | the same, 19 px with 25 px lines on small and large screens | the same | Confirmed today: design-system.service.gov.uk/styles/type-scale/ (the page gives the scale; the typeface name is from memory) |
| Financial Times | Financier Display (serif) | Georgia on article pages | Metric (sans) | From memory. origami.ft.com/latest/foundations/typography/ could not be fetched |
| The Economist | Milo Serif | Milo Serif | Econ Sans | From memory. design-system.economist.com could not be fetched |
| The Guardian | Guardian Headline (serif) | Guardian Text Egyptian (serif), 17 px on phones | Guardian Text Sans | From memory. The address tried in github.com/guardian/csnx returned 404 |
| Our World in Data | Playfair Display (serif) | Lato (sans) | Lato | From memory. The address tried in github.com/owid/owid-grapher returned 404 |

What they have in common, as far as memory goes: a serif with character for headlines; body
text in either a serif (FT, Economist, Guardian) or a sans (Our World in Data, GOV.UK); and
numbers in tables and charts in the sans with tabular figures. None of the five, to my
knowledge, sets table numbers in a monospace. That makes the mono digits the least usual part
of option B; they are one rule and 1.2 KB, and can be dropped without touching the rest.

Readability:

- Body size. GOV.UK sets body text at 19 px on phones and desktops, on a scale it says was
  tested for reading on different devices (confirmed today, address above). The site's 18.9 px
  is in line with that and is not changed.
- Line length. Butterick, Practical Typography, advises an average line of 45 to 90
  characters, spaces included, and calls line length the usual flaw of responsive pages
  (confirmed today: practicaltypography.com/line-length.html). At 390 px wide options A and B
  sit just under that (43 and 42) and C inside it (47). A smaller body size would fix it and
  cost legibility; no change is proposed.
- Heading scale. GOV.UK's scale, where every heading step is smaller than the one above it
  on every screen, is the model for the ladder (cited by the first heading fix on
  11 November; today's fetch of the same page was read for the body rows only).

## 4. Light-theme proposal

Switch: `data-paper="b"`, light theme only; the dark theme is not touched. It combines with
any typeface. Pictures: `shots/compare_paper_type-a.png` (and `-b`, `-c`),
`shots/compare_paper_scorecard.png`.

The reader said the dark theme is good and the white one is not. The dark theme has three
levels (page #1d1e20, card #26282c, panel #2b2d32) and soft text (#e6e6e7, 13.4:1). The light
theme has one level, pure white for page and card, with the hardest text contrast on the site
(17.7:1). The proposal gives light the same structure dark has: a warm off-white page, white
cards that stand off it, slightly softer ink, and borders that can be seen.

Seven tokens change. Contrast is WCAG 2, computed by `python tools/type_lab_contrast.py`,
on the page / on a white card / on a panel.

| Token | Now | Proposed | Contrast, proposed |
|---|---|---|---|
| `--paper` (page) | #ffffff | #f6f3ec | |
| `--code-bg` (panels) | #f4f7f9 | #fdfcf9 | |
| `--ink` | #15191e (17.7) | #1b1f24 | 14.9 / 16.6 / 16.1 |
| `--ink-3` (meta) | #5f6873 (5.7) | #59616b | 5.7 / 6.3 / 6.1 |
| `--accent` (links) | #3d6c8c (5.6) | #35627f | 5.9 / 6.6 / 6.4 |
| `--pos` (passed) | #2E7D5B (5.0) | #2a7354 | 5.2 / 5.7 / 5.6 |
| `--line` (borders) | #c5ccd4 (1.6) | #b3ab9b | 2.1 / 2.3 (borders, not text) |

Colours that do not change, checked on the new page colour: article prose #1f1f1f 14.9;
`--ink-2` 8.4; navy labels 10.4; `--neg` 5.0; figure red 6.5; the LTA accent 4.7. The lowest
text contrast anywhere in the proposal is 4.67:1; nothing is under 4.5:1.

Not done in this proposal: the chart SVGs keep their own backgrounds; the browser bar colour
(`theme-color`) was not looked at.

## 5. Recommendation

Take option B, with the warm page, because it is what Jacob asked for and the pictures give
no reason to refuse it: at matched size Newsreader reads as easily as Source Serif on the
phone captures and gives the headline and the italic standfirst more of a newspaper voice.
It costs about 23 KB more per article page than A (120 KB against 97 KB) and its three
licences have no reserved name, so it is the easier of the two swaps to adopt cleanly.
Treat the mono digits as a separate yes or no: they are the one part of B that no reference
publication does, and Inter's own tabular figures are the plain alternative. If Jacob would
rather not spend the adoption work now, A with the new headings and the warm page already
answers the two complaints on record (the sizes and the white), since those fixes do not
depend on the typeface. C is the one to show a 17-year-old reader before ruling it out: a
sans body is what phone apps look like, but it moves the site furthest from the look of a
research paper.

The decision is Jacob's. NEEDS JACOB: choose A, B or C; yes or no to the warm page; and,
only if he prefers one, heading mark 2 or 3 instead of 1.

## 6. What adoption would take

For B or C (one pull request, after the choice):

1. Fonts. Make own subsets from the upstream TTF files with the same character set and
   features as the NVD files (`tools/make_nvd_fonts.py` is the pattern), instead of shipping
   the Fontsource subsets used in the lab.
2. Licence step, the one the current fonts went through. All five candidate families are
   SIL Open Font License 1.1 (copies in `static/fonts/lab/OFL-*.txt`, from the Google Fonts
   repository). Newsreader, Inter and JetBrains Mono name no Reserved Font Name, so a subset
   may keep the name; the copyright line and licence text must ship with the files.
   Playfair Display and Lato each reserve their name, so a subset of either must be renamed,
   as Source was renamed NVD. The lab uses third-party subsets that still carry those names:
   acceptable on a draft, not for the live site.
3. `00-tokens.css`: replace the `@font-face` rules and the two font tokens; move the
   fallback-face numbers across from `static/fonts/lab/type-b.css` or `type-c.css`; for B add
   the figures rule from `zz-type-lab.css`.
4. `size-adjust` works in Chrome and Firefox from version 92 and Safari from 17. On an older
   iPhone the candidates would draw at their natural size (Newsreader about 7 per cent smaller,
   Inter 11 per cent larger). For adoption either accept that or set the sizes in the
   stylesheet instead.
5. Preloads in `layouts/partials/extend_head.html`: the same five roles (serif regular, sans
   regular, sans semibold; on articles serif semibold and serif italic), new file names.
   Re-measure layout shift at 390 and 1280 px, as fix round 1 did on 5 November.
6. Remove the lab: `zz-type-lab.css`, `static/fonts/lab/`, `content/lab/`, the script block
   in `extend_head.html`, and the old NVD files if they are no longer used. The paper
   template and the share cards use Source faces of their own and are a separate decision.

For the warm page alone: move the seven values into the light block of `00-tokens.css` (and
`--pos` in `custom.css`), and set `theme-color` to match.

For heading mark 2 or 3 instead of 1: move the few rules from `zz-type-lab.css` into
`custom.css`; with mark 2 or 3 the render hook can be deleted.

## 7. What was not checked

- No real phone. Every picture is desktop Chrome in headless mode drawing a frame 390 px
  wide at twice the pixel density. Text rendering on an iPhone or an Android phone differs.
- No Safari and no Firefox. `size-adjust`, `:is()` and `clamp()` are all supported in current
  versions, by their documentation, not by test here.
- No readers. Nobody from the target group has seen the options.
- The preview file was opened in desktop Chrome only. It has no script, so a phone's file
  preview should show it; that was not tried on a phone.
- Layout shift for B and C was not measured. The fallback faces are matched by calculation.
- The Fontsource files were taken as published (sha256 in `FONTS.csv`); their glyphs were not
  compared with the upstream releases.
- Four of the five publication rows in part 3 are from memory.
- Desktop width was looked at once (1280 px, the 31 October article); tablet widths were not.

## Files

| File | What |
|---|---|
| `assets/css/extended/custom.css`, `masthead.css` | the mark and the ladder (default) |
| `layouts/_default/_markup/render-heading.html` | the heading hook |
| `assets/css/extended/zz-type-lab.css` | options B and C, the warm page, marks 2 and 3 |
| `static/fonts/lab/` | candidate fonts, their `@font-face` sheets, licences |
| `layouts/partials/extend_head.html` | lab script, only in a build with drafts |
| `content/lab/typefaces.md`, `_index.md` | the draft lab page |
| `office/type-lab/FONTS.csv` | every font file: source, bytes, sha256, licence |
| `office/type-lab/shots/` | captures and comparison sheets |
| `tools/make_type_lab_fonts.py`, `type_lab_contrast.py`, `type_lab_shots.py`, `make_type_lab_preview.py` | how the numbers, pictures and preview were made |

To browse the whole site in an option: `hugo --buildDrafts --buildFuture --baseURL
http://localhost:1323/ -d <dir>`, serve `<dir>` on port 1323, open `/lab/typefaces/` and use
the bar; or add `?type=b&paper=b&head=u&theme=dark` to any address.
