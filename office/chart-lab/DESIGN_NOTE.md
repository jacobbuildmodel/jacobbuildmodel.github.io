# Interactive charts: design note for the prototypes

Written 11 Nov 2026 with the three prototypes on this branch; round two added 12 Nov 2026 (the section
"Round two" below). Nothing here is published: the demo page (`content/lab/interactive-charts.md`) is a
draft, and no existing article is changed.

## What was built

One shortcode, one small script, one small style sheet, and three charts rebuilt from existing figures with the
same numbers. Two of the figures are published (HDB, 19 Sep; COE or ERP, 17 Oct). The third is not: the
Singapore dollar piece is not published until 14 Nov 2026, and its chart here is built from that piece's review
files at the research repository's HEAD, not from a published figure. (An earlier version of this note said all
three came "from published figures"; that was wrong for the third.)

| Chart | From | What a reader can do |
|---|---|---|
| HDB affordability: years of income | Figure 1 of the 19 Sep piece | Drag or play through 2013 to 2025; see the price, the income and the ratio for any year; a second panel shows why (income against price, 2013 = 100); three story steps |
| COE or ERP: peak speeds against LTA's bands | Chart 1 of the 17 Oct piece | Drag or play through 2004 to 2025; the two years outside the band are ringed; the unscored pandemic years are drawn faint; three story steps |
| Singapore dollar and yen: switch the measure | Chart 1 of the piece due 14 Nov 2026 (not yet published; from its review files) | Three buttons change what each currency is measured against (all trading partners, the US dollar, after prices); the bars and the share strip move; the remainder is printed |

To use one in an article: `{{</* ichart "hdb_years_of_income" */>}}` in place of the figure.

## Library choice: none, and why

The charts are plain SVG and HTML, drawn by JavaScript with no dependency and no build step (about 230 lines in round
one, 549 with round two).
- **Weight.** In round one the script was 6.2 KB (2.6 KB compressed) and the style sheet 6.1 KB (1.8 KB
  compressed); with round two they are 17.0 KB (6.4 KB) and 13.7 KB (3.8 KB), see "Measured" below. Both load
  only on pages that use the shortcode. For comparison, D3 is about 280 KB, Chart.js about 200 KB, Plotly over 3 MB.
  The site's whole font budget is 97 KB.
- **Fit.** A general chart library draws general charts. These charts need three specific things: a line that can be
  scrubbed, a target band, and bars that change with the measure. Writing those directly is less code than
  configuring a library to do them, and every label can be placed by hand.
- **Ageing.** There is nothing to upgrade and nothing that can be withdrawn. The script uses only features every
  current browser has had for years (SVG, ES modules, ResizeObserver, pointer events, `<input type="range">`).
  If the script ever fails, the reader sees the published static figure.

When a fourth or fifth chart type is needed (a map, a distribution), the same pattern takes another function of
40 to 80 lines. If a chart ever needs real statistics in the browser, that is the moment to reconsider a library,
loaded for that page only.

## How it stays clear

1. **The static chart is the floor.** Hugo prints the published SVG, the title, the "how to read this" text, the
   full table of numbers and the source line. All of it works with JavaScript off. The script only adds.
2. **One idea per control.** A slider and a Play button move through time. Numbered steps tell the story in the
   article's own order. Measure buttons change what a move is set against. There are no menus, zooms or settings.
3. **The readout says it in words.** Under each chart one sentence states the selected year in plain numbers
   ("S$640,157 flat, S$10,591 a month: 5.04 years of income. Since 2013: price +40%, income +51%."). On a phone
   there is no hover, so the sentence replaces the tooltip; with a mouse, moving over the plot moves the year.
4. **The title is the finding**, the subtitle is the unit and period, and the first panel is the published figure.
5. **One axis per panel.** Two measures on different scales get two panels, never two y-axes.
6. **Colour carries one distinction.** The site's existing figure tokens: the subject colour for the series the
   piece is about, grey for what it is compared with, blue for the Singapore dollar in the measure chart. Every
   series is also labelled in words, so colour is never the only signal.
7. **Honesty devices are part of the chart.** Years outside a target band are ringed; years the piece did not score
   are faint; the remainder of a split is printed; a decomposition comes with its switch of measure, so a reader can
   see for themselves whether the answer depends on the measure. The last one is the lesson of the Singapore
   dollar reviews turned into a design rule.

## Design tokens

No new colours or fonts. The charts read the site's tokens (`00-tokens.css`, `economics.css`), so light and dark
follow the page.

| Token | Use | Contrast on the page, light / dark |
|---|---|---|
| `--fig-subject` (#a32a1e / #e0705f) | the subject series, slider, readout rule | 7.2 / 5.3 |
| `--fig-context` (#8d9096 / #90939a) | comparison series, band | 3.2 / 5.4 (lines and fills only, never text) |
| `--accent` (#3d6c8c / #85acc9) | the Singapore dollar's bars, focus ring | 5.6 / 6.9 |
| `--ink`, `--ink-2`, `--ink-3`, `--line`, `--surface`, `--code-bg` | text, grid, readout panel | as the site |
| `--font-sans`, `--font-serif` | labels and controls; the title | no new font files |

Sizes: controls are at least 44 px tall; labels in the plot are 12 to 13 px at real size (the plot is drawn at the
width of the screen, not scaled down); one panel is 176 px tall.

## Accessibility

- Every control is a native element: a range input, buttons, `<details>`. All work from the keyboard and show a
  focus ring.
- The plot is marked as an image with a text alternative that names the finding; the numbers are in a real table
  below it; the readout is announced when it changes (`aria-live="polite"`).
- `prefers-reduced-motion` turns off the opening animation and the bar transitions. Play still works, one year at
  a time.
- Forced-colours mode and print fall back to system colours and to the static figure.

## Speed and layout

- The stage (the box the plot is drawn in) has its final height from the first paint, set in CSS, and the controls
  are printed by Hugo, so nothing moves when the script runs. Layout shift measured in the built-in browser at
  375 px: 0.
- No new font, no image, no request to another site. The data for a chart travels inside the page (3 to 6 KB).
- The demo page with three charts is 43 KB of HTML (10 KB compressed).

## Where the numbers come from

`tools/build_chart_data.py` reads each series from the piece's own committed pipeline output in the research
repositories and writes `data/charts/*.json`, with the repository, commit, file and column of every series. The
story steps and readout sentences are built from the same numbers by the same script, so a chart, its annotations
and its table cannot disagree. Each chart's source line links to that commit.

## Not done yet (stated so nobody assumes it)

- Not tested on a real phone or in Safari; tested in the desktop app's browser at 375 px and desktop width, light
  and dark.
- No Lighthouse run. The layout-shift figure is from the browser's own layout-shift entries.
- The colour pair in the measure chart (red and blue) was checked for contrast against the page, not with a
  colour-blindness simulator: Node is not installed on this machine. Both bars are labelled in words.
- No reader test. Before any of these replaces a published figure: five readers, 30 seconds each, static against
  interactive, can they state the finding (the test already written into the 2026-27 plan).
- The measure chart uses the keys of the Singapore dollar piece's review files at research-repository HEAD. It
  must be rebuilt from the merged results note before use.

## Next, if these are kept

1. A fourth type: small multiples that share one slider (the PWM pay chart, the 11-currency steadiness chart).
2. Story steps that follow the article as it scrolls (the "scroll story" in the 2026-27 plan), built on the same
   steps data.
3. A "your case" input only where it is not advice: for example the year a reader first looked at flats, on the
   affordability chart.
4. Numbers in the prose printed from the same data files as the charts.

## Round two: three bolder directions (12 Nov 2026)

Jacob saw phone screenshots of round one and said "Push further". Round one stays on the demo page as the
baseline. Round two adds three directions under it. Each is a different answer to "what can a chart do
that a picture cannot", and each is switched on by a second word in the shortcode:

| Direction | Shortcode | Shown on | What the reader does | What it is for |
|---|---|---|---|---|
| A. Explain this point | `{{</* ichart "erp_peak_speeds" "explain" */>}}` | ERP speeds (two lines, one at a time), HDB years of income | Taps or drags to a point, or uses the slider and the arrow buttons. A card under the plot reads that year in words | Any line chart in any article. The reader gets the reading a careful analyst would give for each point |
| B. Build the comparison | `{{</* ichart "hdb_years_of_income" "compare" */>}}` | HDB years of income | Picks the starting year. The line, the verdict and the bars all answer "compared with that year" | Pieces whose argument is about the base year |
| C. Instrument panel | `{{</* ichart "erp_peak_speeds" "panel" */>}}` | ERP speeds | Scrolls. A dark panel stays on screen and each step of the story moves it to its year. Dials, slider and Play also work by hand | One flagship piece at a time. The boldest look |

Screenshots, phone width, light and dark: `office/chart-lab/shots/r2-*.jpg`.

### What is shared

- **Icons.** Fourteen small line icons, drawn for this site as inline SVG symbols and printed once per page by
  the shortcode: house, coins, car, gauge, currency, spark, play, pause, and six small marks (up, previous,
  rank, band, start, not scored). Every icon sits beside its words or inside a button that has an accessible
  name; none carries meaning alone. No icon font, no image file.
- **One new colour.** `--ic-sig` (#0f6f9c light, #5cc8ee dark) marks the reading layer: the explanation card,
  the selected-year label, the controls. The data keep the site's subject colour. Inside round two the dark
  subject colour is a little brighter (#f39483) so that large numbers on a tinted card pass 4.5:1.
- **A topic chip** over each title (icon and two or three words), and a filled label on the axis under the
  selected year, so the eye finds "where am I" without reading the card.
- **Fixed sizes.** Every card, stage, dial and bar strip has its height set in CSS and is printed by Hugo with
  its first content, so the script fills boxes that are already there.

### A. Explain this point

The card has four parts, all read from the chart's data file: the value, the change from the year before, where
the year ranks, and how far it sits from the target band or from the first year. The HDB card adds the flat
price and the median income for that year. Examples, exactly as built:

- "55 km/h. Down 3 from 2024. The lowest of the 22 years shown. Inside the band, 10 km/h below its top.
  7.7 km/h below 2004, the first year."
- "30.4 km/h. Up 1 from 2015. The highest of the years up to 2016. 0.4 km/h above the top of the band."
- "5.04 years. Up 0.05 from 2024. The highest since 2013 (5.43). 0.39 years below 2013, the first year."

How the rank sentence is chosen (`rank_line` in `tools/build_chart_data.py`): the highest or lowest of all
years if it is; otherwise "the highest since 2013 (5.43)" when it beats at least the two years before it;
otherwise its place ("5th highest of the 13 years shown", "Joint 5th" for a tie). Each sentence is at most 50
characters so that it fits one row on most phones; the builder stops if one is longer.

Nothing in the card is typed by hand and nothing comes from a live model. The spark icon marks the card as an
explanation layer; the "how to read this" text says in plain words where the sentences come from.

### B. Build the comparison

This is the HDB article's own argument made into a control. The reader picks a starting year (a slider, and
two buttons for the years the article names: 2013, the peak, and 2019, the low). Then:

- the card gives the verdict for 2025 in words and one number ("+25%, more years of income than in 2019.
  The flat took 5.04 years of median household income in 2025, against 4.04 in 2019: 1.00 more. Between those
  years the price rose 58% and income rose 27%.");
- the plot shows every year as a change from the starting year, in per cent, with the starting year on the
  zero line; years before it are dotted;
- the bars under it give the answer for all twelve starting years at once.

It stays a reading of history. There is no input about the reader's own income, flat or loan, and no sentence
says what anyone ought to do.

**One thing the bars make plain, for Jacob to see before this is used:** from 11 of the 12 starting years,
2025 comes out higher; only from 2013 does it come out lower. The article's headline uses 2013. The chart
does not argue with the article (the article makes the base-year point itself), but a reader will see at a
glance that the headline year is the one exception.

### C. Instrument panel

- **Look.** The panel is the masthead navy in both themes (deeper in dark), with its own bright colours: a warm
  line with a glow, a pale blue band, white numbers. It is dark-first, and in light mode it reads as an
  instrument set into the page, in the same navy as the site's band.
- **Dials.** One arc for each kind of road. The whole arc is the axis, the thick part is LTA's target band, the
  bright dot is the selected year. Under the number the words say "inside the band", "above the band" or "not
  scored". A dial is also a button: it picks which road's line is drawn, so the plot has one axis at a time.
- **Motion.** Moving between years glides: the line is revealed up to the year, the dot slides along it and the
  dial numbers run to their values. The first time the panel is seen, it runs once from the first year to the
  last. Numbers between two years appear only while something is moving; every movement ends on a number from
  the data file.
- **Scroll story.** The panel is sticky. The four story steps are ordinary text under it; the last step whose
  top has come up past the lower part of the screen is the active one, and it sets the year and the road.
  Without JavaScript the steps are four paragraphs under the static figure.
- **Reduced motion.** With the device setting on, nothing moves by itself: no opening run, no glide, no pulse,
  no card rise. Play still steps one year at a time.

### Rules added in round two

1. **An area is filled only where it is honest**: where the axis starts at zero (HDB years of income), or where
   the area is itself the change (direction B, between the line and the zero line). The speed lines have axes
   that start at 40 and 15 km/h, so they get a glow and no fill. The brief for direction C asked for gradient
   area fills; this is the one place where it was not followed, for that reason.
2. **One axis per panel still holds.** Where two lines have different scales (expressways and arterial roads),
   a button swaps the line and its axis together.
3. **A percentage is rounded once.** The label is made from the exact ratio, not from a number that was
   already rounded.
4. **Every derived number is made by the builder**: ranks, changes, distances from the band, the change from
   each starting year, the count of starting years, the verdict sentences. The script only places them.

### Measured (the build of 12 Nov 2026)

| | Minified | Compressed (gzip) | Budget |
|---|---|---|---|
| Script, the whole chart system (`ichart.js`, 549 lines) | 16,990 bytes | 6,444 bytes | 20 KB |
| Style sheet, the whole chart system (`ichart.css`) | 13,673 bytes | 3,776 bytes | 14 KB |

No new font file, no image, no request to another site. The icon sprite is about 1.8 KB inside the page. The
demo page with seven charts is 95 KB of HTML (18 KB compressed); the data of one chart is printed once per
page however often it is drawn. The data files are larger than in round one because they now carry the
sentences (ERP 15.8 KB, HDB 12.2 KB as printed in the page, before compression).

### Contrast of the new colours (computed from the hex values, WCAG formula)

| Text | On | Ratio |
|---|---|---|
| `--ic-sig` #0f6f9c | page / tinted card, light | 5.6 / 4.7 |
| `--ic-sig` #5cc8ee | page / tinted card, dark | 8.7 / 6.0 |
| subject #a32a1e, partner #3d6c8c | tinted card, light | 6.1, 4.8 |
| subject #f39483, partner #85acc9 | tinted card, dark | 5.2, 4.8 |
| white label on a selected button | #0f6f9c, light | 5.6 |
| dark label on a selected button | #5cc8ee, dark | 7.7 |
| panel: white, #dbe4ee, #c3d0df | navy, at its lightest corner | 10.1, 7.9, 6.5 |
| panel: #c3d0df, "above the band" #ffb3a5 | a selected dial at the lightest corner | 5.1, 4.7 |
| panel line #ff9c8a (a line, not text) | navy, at its lightest corner | 5.0 |

### What was checked

- In the desktop app's browser at 375 px and 320 px wide, light and dark, and once at desktop width: no
  horizontal scroll, no console error, no clipped or overlapping label.
- Layout shift: the browser's own layout-shift entries sum to 0 on load and while scrolling through all seven
  charts and the scroll story.
- Every explanation card (57 points) and every comparison verdict (12 starting years) fits its fixed box at
  375 px and at 320 px; measured by stepping the sliders through every value.
- The no-JavaScript page: a copy of the built page with the script removed shows the static figure, the title,
  the how-to text, the table and the story steps as plain paragraphs.
- The sentences: `tools/check_chart_data.py` reads the research repositories again with separate code and
  checks every card (value, change, rank, band, first year, price and income), every comparison (all 156
  re-based values, the verdict, the why-sentence) and every dial status. 0 mismatches. On its first run it
  caught a percentage that had been rounded twice (2014: "+4%" where the exact figure rounds to "+5%"); the
  builder was fixed.
- Sizes, from the files Hugo wrote.
- A normal build (no drafts) contains no `/lab/` page and no chart script. Round two added a draft
  `content/lab/_index.md` for this: without it, merging would have published an empty section page.

### What was not checked

- Not tested on a real phone, in Safari or in Firefox. The sticky panel and the scroll story are the parts
  most worth trying on a real phone.
- Reduced motion was not tried with the device setting switched on; the code path is simple (one flag) but it
  was only read, not run.
- No screen-reader run. The controls are native and the cards are live regions, but how the card sounds when a
  reader drags quickly was not heard.
- No Lighthouse run and no colour-blindness simulator (Node is not installed on this machine). Direction B
  uses red for "more" and blue for "fewer", always with an arrow, a sign and the words.
- No reader test. The five-reader, 30-second test in the 2026-27 plan applies to each direction before it
  replaces a published figure.
- `color-mix()` (the card tint and soft shadows) needs a browser from 2023 or later. An older browser shows the
  cards without the tint; not tested.
- The demo page loads the ERP data once and draws it three times. A real article would use one chart per
  figure.

### A private preview for a phone

`tools/make_chart_preview.py` turns a draft build of the demo page into one self-contained HTML file (styles,
script, data and fallback figures inline, system fonts, no request of any kind). It is a private preview, not a
publication.
