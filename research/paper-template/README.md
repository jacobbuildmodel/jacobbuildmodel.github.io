# Paper template (trial): "Jacob's Projects" working papers

One Quarto source renders to a PDF (Typst) and an HTML page, in the website's
colours and typefaces. The sample is the published HDB financing piece
(content/economics/2026-10-03.md, live since 3 October 2026).

## Render

    quarto render            # in this folder: paper.pdf and paper.html

Quarto 1.10.19 (bundles Typst 0.15.1). The portable Windows zip works without
installing anything: download quarto-1.10.19-win.zip from the quarto-cli
release, check its sha256 against quarto-1.10.19-checksums.txt, unzip, run
bin/quarto.exe. Only paper.pdf is committed; paper.html and paper_files/ are
build output (.gitignore).

## Why Typst, not LaTeX

Typst did every required element cleanly on the first render: footnotes,
a captioned and cross-referenced table, captioned SVG figures drawn as vectors,
a citeproc reference list, and a custom title block (series label, ORCID,
abstract, keywords, JEL). It needs no TeX installation and compiles in about a
second. LaTeX was not needed.

## What is where

| File | Role |
|---|---|
| paper.qmd | the paper: front matter (series, author + ORCID, abstract, keywords, jel) and body |
| _quarto.yml | both formats, fonts, citeproc, section numbers, date format |
| partials/typst-template.typ | PDF layout: page, type, title block, tables, captions, footnotes |
| partials/typst-show.typ | maps front matter to the PDF layout |
| partials/title-block.html, html/paper.css | the same title block and styling for the HTML page |
| references.bib | the piece's Sources list as BibTeX |
| figures/source/*.svg | the site's charts, byte for byte as in static/figs/ |
| figures/*.svg | print-safe copies made by flatten_svg.py (used by both outputs) |
| flatten_svg.py | resolves the charts' CSS custom properties to their light values |
| fonts/ | Source Serif 4 and Source Sans 3 (SIL OFL 1.1, licences alongside) |

## Design, taken from the site
- Colours from assets/css/extended/custom.css and the PaperMod light theme:
  ink #1e1e1e, muted #6c6c6c, accent #3d6c8c, tint #f4f7f9, rule #e0e6ea.
- Prose in Source Serif 4, the site's reading serif. Headings, labels,
  captions and tables in Source Sans 3: the site uses the system sans there,
  which a PDF cannot embed portably, so Source Sans 3 (OFL) stands in.
- Series label "Jacob's Projects - <project name>" above the title and in the
  running header; no number, no surname.

## Gotchas
- The site's chart SVGs colour themselves with CSS custom properties and a
  dark-mode block. Typst's SVG renderer does not support custom properties,
  so the charts printed as solid black boxes. Run
  `python flatten_svg.py figures/source/*.svg --out figures/` after copying a
  new chart in. It also sets chart text in Source Sans 3, so no system font
  (Segoe UI on Windows) is embedded.
- Quarto turns a date like "3 October 2026" into ISO unless `date-format` is
  set (it is, in _quarto.yml).
- Pipe tables are centred and justified by default in Typst; the table in
  paper.qmd uses `:---` alignment and `tbl-colwidths`, and the template turns
  justification off inside tables.

## Before a real paper
- The ORCID in paper.qmd is a placeholder (0000-0000-0000-0000).
- The JEL codes (G21, R31, E43) and keywords are illustrative for the trial.
- Table 1 restates the eight results as published on the scorecard page; the
  body text is the article's, verbatim, with the two asides as footnotes.
