// typst-template.typ -- "Jacob's Projects" working-paper layout.
// Colours and typefaces are the website's own (assets/css/extended/custom.css
// and the PaperMod light theme): ink #1e1e1e (--primary), muted #6c6c6c
// (--secondary), accent #3d6c8c (--accent), tint #f4f7f9 (--code-bg), rule
// #e0e6ea (--border). Prose in Source Serif 4 (the site's reading serif);
// headings, labels, captions and tables in Source Sans 3, the open sans
// stand-in for the site's system sans (a PDF needs an embedded font).

#let ink = rgb("#1e1e1e")
#let muted = rgb("#6c6c6c")
#let accent = rgb("#3d6c8c")
#let tint = rgb("#f4f7f9")
#let rule = rgb("#e0e6ea")
#let serif = ("Source Serif 4",)
#let sans = ("Source Sans 3",)

#let label-text(body) = text(font: sans, size: 8pt, weight: "semibold", fill: accent, tracking: 0.05em, body)

#let article(
  title: none,
  series: none,
  authors: (),
  date: none,
  abstract: none,
  keywords: (),
  jel: none,
  sectionnumbering: none,
  doc,
) = {
  set page(
    paper: "a4",
    margin: (x: 24mm, top: 26mm, bottom: 24mm),
    header: context {
      if counter(page).get().first() > 1 {
        set text(font: sans, size: 8pt, fill: muted)
        grid(columns: (1fr, auto), series, title)
        v(-4pt)
        line(length: 100%, stroke: 0.4pt + rule)
      }
    },
    footer: context {
      set text(font: sans, size: 8pt, fill: muted)
      align(center, counter(page).display())
    },
  )
  set text(font: serif, size: 10.5pt, fill: ink, lang: "en", region: "gb", number-type: "lining")
  set par(justify: true, leading: 0.62em, spacing: 0.95em)
  set heading(numbering: sectionnumbering)
  show heading: set text(font: sans, fill: ink, weight: "bold")
  show heading.where(level: 1): it => block(above: 1.5em, below: 0.7em, text(size: 12.5pt, it))
  show heading.where(level: 2): it => block(above: 1.2em, below: 0.6em, text(size: 11pt, it))
  show link: set text(fill: accent)
  show quote: it => block(width: 100%, fill: tint, inset: (x: 10pt, y: 8pt), stroke: (left: 2.5pt + accent), it.body)
  show figure.caption: set text(font: sans, size: 8.5pt, fill: muted)
  show figure.caption: set align(left)
  show figure.where(kind: table): set figure.caption(position: top)
  set table(
    stroke: (x, y) => if y == 0 { (top: 0.8pt + ink, bottom: 0.6pt + ink) } else { (bottom: 0.4pt + rule) },
    inset: (x: 5pt, y: 4.5pt),
  )
  show table: set text(font: sans, size: 8.5pt, number-width: "tabular")
  show table: set par(justify: false)
  show table.cell.where(y: 0): set text(weight: "semibold")
  set footnote.entry(separator: line(length: 30%, stroke: 0.4pt + rule))
  show footnote.entry: set text(size: 8.5pt)

  // ---- title block ----
  block(width: 100%, fill: tint, inset: (x: 14pt, y: 14pt), stroke: (left: 3pt + accent), radius: 2pt)[
    #if series != none [#label-text(series) #v(6pt)]
    #text(font: sans, size: 19pt, weight: "bold", fill: ink, hyphenate: false, title)
    #v(8pt)
    #set text(font: sans, size: 9.5pt)
    #for a in authors [
      #text(weight: "semibold", a.name)
      #if a.orcid != none [ #h(4pt) #text(fill: muted)[ORCID #link("https://orcid.org/" + a.orcid)[#a.orcid]]]
      #if a.affiliation != none [#linebreak() #text(fill: muted, a.affiliation)]
      #linebreak()
    ]
    #if date != none [#text(fill: muted, date)]
  ]
  v(10pt)
  if abstract != none {
    block(width: 100%, inset: (x: 14pt))[
      #label-text[Abstract]
      #v(2pt)
      #set par(justify: true)
      #text(size: 10pt, abstract)
      #v(4pt)
      #set text(font: sans, size: 8.5pt, fill: muted)
      #if keywords.len() > 0 [*Keywords:* #keywords.join("; ") #linebreak()]
      #if jel != none [*JEL:* #jel]
    ]
    v(6pt)
    line(length: 100%, stroke: 0.4pt + rule)
  }
  doc
}
