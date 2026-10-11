// typst-show.typ -- maps the paper's front matter onto article() in
// typst-template.typ. Front-matter fields used: title, series, author (name,
// orcid, affiliations), date, abstract, keywords, jel, section-numbering.
#show: doc => article(
$if(title)$
  title: [$title$],
$endif$
$if(series)$
  series: [$series$],
$endif$
$if(by-author)$
  authors: (
$for(by-author)$
    ( name: [$it.name.literal$],
      orcid: $if(it.orcid)$"$it.orcid$"$else$none$endif$,
      affiliation: $if(it.affiliations)$[$for(it.affiliations)$$it.name$$sep$, $endfor$]$else$none$endif$ ),
$endfor$
  ),
$endif$
$if(date)$
  date: [$date$],
$endif$
$if(abstract)$
  abstract: [$abstract$],
$endif$
$if(keywords)$
  keywords: ($for(keywords)$"$keywords$",$endfor$),
$endif$
$if(jel)$
  jel: [$jel$],
$endif$
$if(section-numbering)$
  sectionnumbering: "$section-numbering$",
$endif$
  doc,
)
