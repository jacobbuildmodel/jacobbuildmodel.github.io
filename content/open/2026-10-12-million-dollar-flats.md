---
title: "Million-dollar flats came with $100,000 COEs. Coincidence?"
date: 2026-10-12
draft: false
answerDue: "December 2026"
showToc: false
summary: "Three predictions, each with a confidence, sealed before the HDB resale price data was opened. The answer is due in December 2026."
repo: "https://github.com/jacobbuildmodel/hdb-affordability/tree/7ee9b9169c36399a80400b0e2e9ef9bd6b5000af/cargradient"
---

Open question. Predictions sealed on 12 October 2026.

Everyone knows a COE is a car-owner's problem. Million-dollar HDB resale
transactions went from 46 in 2017 to 259 in 2021, and made up about 6% of
resale transactions in 2025. Huang, Li and Ross (2018) found that in private
condos from 2002 to 2015, dearer COEs went with bigger gains near the city
centre than further out. Their explanation: dearer cars mean more households
go carless and pay to live close in. My bet, sealed before I open the HDB
data: the same tilt shows up in HDB flats, 2002 to 2015 and 2016 to 2026,
and has weakened, not strengthened, since growth in the car quota was cut to
zero in February 2018. At most, this would explain part of what a flat near
town costs, not million-dollar flats as a whole.

Picture two families who will never own a car. One buys an HDB flat a short
train ride from Raffles Place, the other a flat at the end of the line. If
car prices and flat prices are separate stories, a dearer COE changes
nothing for either of them.

## The argument: two headlines, or one story

**Separate stories.** A COE is the price of a car. Million-dollar flats are
about location, size and lease. A family without a car has no stake in the
COE.

**One story.** When owning a car costs more, living near town is worth more,
because getting around without a car is easier there. So part of what a
flat near town costs moves with the COE, for every buyer, car or no car.
That is what Huang, Li and Ross found for private condos.

## Push it to the extreme

Thought experiment: if cars cost nothing, every family drives, and a flat far
out costs little more in time than one near town. If cars were out of
reach, every family would live by the train timetable, and nearness to town
would be everything. Singapore sits between the two. A dearer COE tips some
households from one side to the other.

## The obvious objection: isn't this just good times?

COE prices rise in good years, and good years may lift flats near town more
than flats far out for reasons that have nothing to do with cars. So the
test does not rely on the COE price alone. It uses the car quota, which the
government sets mostly from the number of cars taken off the road, as the
lever that moves the COE price. Even so, a tilt toward town is weaker
evidence for the car story than no tilt is against it.

## My bets

This is a test on different homes from the paper's: HDB resale flats, not
private condos.

**First bet. Their years.** From 2002 to 2015, when COEs cost more, HDB
flats near Raffles Place gained relative to flats further out.
Confidence: 70%.

Why: "Same city, same years and same COE swings as a paper that found the
effect strongly in condos, and the central HDB premium widened over most of
those years."

**Second bet. Since then.** The same was true from 2016 to 2026.
Confidence: 40%.

Why: "COEs tripled in 2021-23, but outer towns kept pace with central ones,
and the only clear tilt toward far-out flats came just as COEs started
rising."

**Third bet. After the 2018 cut.** Since growth in the car quota was cut to
zero in February 2018, that tilt has been weaker than in the years of
step-by-step cuts before it.
Confidence: 15%.

<!-- vale Site.Directives = NO -->
Why: "I'd lean weaker, but not by much. The "stronger" story needs a big
change, and 2018 was a small one. Moving from 0.25% growth to 0% hardly
changes how many households can get a car. It's hard to see that pushing
many more families to stay car-free and pay up for flats near town. Most of
what changed after 2018 cuts the other way. New rail lines and working from
home both make living further out cheaper in time and effort. Either would
make a COE rise matter less for where people choose to live. Two catches. A
weaker result wouldn't tell you whether rail or COVID caused it, so the bet
is about direction, not the reason. And my honest best guess is close to
"no clear change," given how small the 2018 change was."
<!-- vale Site.Directives = YES -->

## How it will be tested

Every HDB resale from April 2002 whose block could be placed on the map is
matched to its block's distance from Raffles Place. Each quarter's price per square metre is set against the COE premium
for cars that quarter. The question is whether flats near town gained more
than flats far out when the premium was higher. Because COE prices and the
quota change only from quarter to quarter, the uncertainty is counted by
quarter (54 quarters in the first bet's years and 42 since), not by
the hundreds of thousands of individual sales. Before the seal, the method
was run on invented prices with no link built in, using the real blocks,
distances and COE prices, to check that it finds a link no more often than
chance allows.

## What would change my mind

- No tilt toward town in HDB flats when COEs rose, in either period.
- A tilt the other way: flats far out gaining when COEs rose.
- A tilt that grew, not shrank, after February 2018.

## Sources

- Million-dollar resale counts: Parliament of Singapore, written answer by
  the Minister for National Development, 4 July 2022; oral answer, 7 April
  2026.
- COE premium, quota and successful bids: SingStat Table Builder M651121,
  data source Land Transport Authority.
- Car-quota growth rates: Parliament of Singapore, Ministry of Transport
  answers of 5 February 2013, 11 March 2015, 9 May 2016 and 6 November
  2017; LTA news release, 13 August 2020.
- HDB resale flat prices: data.gov.sg, Housing and Development Board,
  under the Singapore Open Data Licence version 1.0.
- MRT station exits: data.gov.sg, Land Transport Authority.
- Block locations: contains information from OneMap (Singapore Land
  Authority), accessed 5 and 6 October 2026, under the Singapore Open Data
  Licence version 1.0.
- The paper: Huang, Li and Ross, "The impact of the cost of car ownership on
  the house price gradient in Singapore", Regional Science and Urban
  Economics 68 (2018), 160-171.

## Proof

The [sealed predictions](https://github.com/jacobbuildmodel/hdb-affordability/blob/7ee9b9169c36399a80400b0e2e9ef9bd6b5000af/cargradient/THESIS.md) are THESIS.md in commit
7ee9b91, 12 October 2026.

Answer due December 2026, published here whichever way it lands.

Last answered: [Was the HDB loan really cheaper than a bank's?](/economics/2026-10-03/)

Previous open question: [Tokyo got cheaper. Did Singapore get richer?](/open/2026-10-03-singapore-dollar/)
