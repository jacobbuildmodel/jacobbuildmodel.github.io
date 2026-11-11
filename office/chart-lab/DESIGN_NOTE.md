# Interactive charts: design note for the prototypes

Written 11 Nov 2026 with the three prototypes on this branch. Nothing here is published: the demo page
(`content/lab/interactive-charts.md`) is a draft, and no existing article is changed.

## What was built

One shortcode, one small script, one small style sheet, and three charts rebuilt from published figures with the
same numbers.

| Chart | From | What a reader can do |
|---|---|---|
| HDB affordability: years of income | Figure 1 of the 19 Sep piece | Drag or play through 2013 to 2025; see the price, the income and the ratio for any year; a second panel shows why (income against price, 2013 = 100); three story steps |
| COE or ERP: peak speeds against LTA's bands | Chart 1 of the 17 Oct piece | Drag or play through 2004 to 2025; the two years outside the band are ringed; the unscored pandemic years are drawn faint; three story steps |
| Singapore dollar and yen: switch the yardstick | Chart 1 of the 14 Nov piece | Three buttons change what each currency is measured against (all trading partners, the US dollar, after prices); the bars and the share strip move; the remainder is printed |

To use one in an article: `{{</* ichart "hdb_years_of_income" */>}}` in place of the figure.

## Library choice: none, and why

The charts are plain SVG and HTML, drawn by about 230 lines of JavaScript with no dependency and no build step.
- **Weight.** The script is 6.2 KB (2.6 KB compressed) and the style sheet 6.1 KB (1.8 KB compressed). Both load
  only on pages that use the shortcode. For comparison, D3 is about 280 KB, Chart.js about 200 KB, Plotly over 3 MB.
  The site's whole font budget is 97 KB.
- **Fit.** A general chart library draws general charts. These charts need three specific things: a line that can be
  scrubbed, a target band, and bars that change with a yardstick. Writing those directly is less code than
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
   article's own order. Yardstick buttons change the measure. There are no menus, zooms or settings.
3. **The readout says it in words.** Under each chart one sentence states the selected year in plain numbers
   ("S$640,157 flat, S$10,591 a month: 5.04 years of income. Since 2013: price +40%, income +51%."). On a phone
   there is no hover, so the sentence replaces the tooltip; with a mouse, moving over the plot moves the year.
4. **The title is the finding**, the subtitle is the unit and period, and the first panel is the published figure.
5. **One axis per panel.** Two measures on different scales get two panels, never two y-axes.
6. **Colour carries one distinction.** The site's existing figure tokens: the subject colour for the series the
   piece is about, grey for what it is compared with, blue for the Singapore dollar in the yardstick chart. Every
   series is also labelled in words, so colour is never the only signal.
7. **Honesty devices are part of the chart.** Years outside a target band are ringed; years the piece did not score
   are faint; the remainder of a split is printed; a decomposition comes with its yardstick switch, so a reader can
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
- The colour pair in the yardstick chart (red and blue) was checked for contrast against the page, not with a
  colour-blindness simulator: Node is not installed on this machine. Both bars are labelled in words.
- No reader test. Before any of these replaces a published figure: five readers, 30 seconds each, static against
  interactive, can they state the finding (the test already written into the 2026-27 plan).
- The yardstick chart uses the keys of the Singapore dollar piece's review files at research-repository HEAD. It
  must be rebuilt from the merged results note before use.

## Next, if these are kept

1. A fourth type: small multiples that share one slider (the PWM pay chart, the 11-currency steadiness chart).
2. Story steps that follow the article as it scrolls (the "scroll story" in the 2026-27 plan), built on the same
   steps data.
3. A "your case" input only where it is not advice: for example the year a reader first looked at flats, on the
   affordability chart.
4. Numbers in the prose printed from the same data files as the charts.
