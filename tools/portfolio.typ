// tools/portfolio.typ -- layout of the one-page portfolio PDF.
//
// Used by tools/portfolio_pdf.py, which converts content/about.md to Typst
// with pandoc and wraps it in portfolio() below. Fonts and colours are the
// paper template's (research/paper-template): Source Serif 4 for prose,
// Source Sans 3 for the name, headings and labels; ink #1e1e1e, muted
// #6c6c6c, accent #3d6c8c, rule #e0e6ea.

#let ink = rgb("#1e1e1e")
#let muted = rgb("#6c6c6c")
#let accent = rgb("#3d6c8c")
#let rule = rgb("#e0e6ea")
#let sans = "Source Sans 3"
#let serif = "Source Serif 4"

// Pandoc 3.1's Typst writer emits these two for a block quote and a rule.
#let blockquote(body) = block(
  inset: (left: 0.9em, y: 0.1em),
  stroke: (left: 1.2pt + accent),
  text(size: 0.95em, style: "italic", body),
)
#let horizontalrule = line(length: 100%, stroke: 0.5pt + rule)

#let portfolio(name: "", site: "", url: "", date: "", day: none, body) = {
  set document(title: name + ": portfolio, " + date, author: name, date: day)
  set page(paper: "a4", margin: (x: 13mm, top: 11mm, bottom: 10mm))
  set text(font: serif, size: 9.6pt, fill: ink, lang: "en", region: "gb")
  // Paragraph gap 0.66em (was 0.72em) since 14 November 2026: with ten pieces
  // listed, 0.72em put the last line on a second page.
  set par(leading: 0.52em, spacing: 0.66em, justify: false)
  show heading: it => block(above: 1.05em, below: 0.45em, sticky: true,
    text(font: sans, weight: "semibold", size: 8.2pt, fill: accent,
      tracking: 0.07em, upper(it.body)))
  show link: set text(fill: accent)
  set list(indent: 0pt, body-indent: 0.45em, spacing: 0.62em,
    marker: text(fill: accent)[\u{2022}])

  grid(
    columns: (1fr, auto),
    align: (left + bottom, right + bottom),
    [
      #text(font: sans, weight: "bold", size: 19pt)[#name] \
      #text(font: sans, size: 9pt, fill: muted)[#site \u{00B7} #link(url)[#url.replace("https://", "").trim("/")]]
    ],
    text(font: sans, size: 9pt, fill: muted)[Portfolio \u{00B7} #date],
  )
  v(-0.2em)
  line(length: 100%, stroke: 0.6pt + rule)
  v(0.1em)
  columns(2, gutter: 7mm, body)
}
