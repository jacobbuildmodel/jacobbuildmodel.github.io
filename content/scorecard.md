---
title: "27 sealed predictions: 10 held, 11 failed"
question: "How often has this site been wrong?"
date: 2026-10-03
draft: false
showToc: false
hidemeta: true
summary: "Every prediction this site wrote down and sealed before opening the data, and what happened to it. Failures included, and never removed."
# Read by the home page band (layouts/partials/track_record.html). Keep these
# equal to the counts this page states. brier and brierN stay empty until the
# page states a Brier score; the band then adds its calibration line.
sealed: 27
held: 10
failed: 11
neither: 6
brier: 0.194
brierN: 4
menu:
  main:
    name: "Scorecard"
    weight: 30
---

> Before any data is opened, each piece writes its predictions into a file called
> `THESIS.md` and seals it in a dated commit. This page is what happened next.
> Of 27 sealed predictions, 10 held, 11 failed, and 6 landed in between.

A method that never fails is not being tested. This page exists so that anyone can
check how often this one does, without reading a single article first.

## The count

| Piece | Held | Failed | Neither |
|---|---|---|---|
| [COE or ERP](/economics/2026-10-17/) | 1 | 2 | 1 |
| [HDB loan vs bank loan](/economics/2026-10-03/) | 5 | 3 | 0 |
| [HDB affordability](/economics/2026-09-19/) | 3 | 2 | 4 |
| [GST rises](/economics/2026-09-08/) | 1 | 4 | 1 |
| **Total** | **10** | **11** | **6** |

**Held** means the sealed prediction survived. **Failed** means it did not, and the
article says so. **Neither** means the result landed between the pass and fail lines
written in advance, or no verdict was recorded, and it is not rounded to either side.
Each piece is scored again against newer data twelve months after it is published.

**Calibration.** From the COE or ERP piece on, each sealed prediction also carries
a confidence, written before the data was opened. The first four: 1 of 4 held,
against 1.9 expected from those confidences. Brier score 0.194, where 0 is perfect
and a flat 50 per cent on everything scores 0.25.

## COE or ERP: which one actually keeps Singapore's roads moving?

[Roads got about a quarter more crowded. Speeds held.](/economics/2026-10-17/)
Sealed 26 September 2026. Revisit 17 October 2027.

- **Failed.** Every scored year's average peak speed would sit inside the Land
  Transport Authority's target band: 45 to 65 km/h on expressways, 20 to 30 km/h
  on arterial roads. Confidence 35%. Result: arterial roads ran above the band in
  2016 (30.4 km/h) and 2023 (31 km/h). No year fell below either band.
- **Held.** Once road space is allowed for, peak speed would barely move as cars
  per lane-kilometre changed. Confidence 65%. Result: from 2005 to 2017 crowding
  rose 22 per cent on expressways and 25 per cent on arterial roads; expressway
  speed did not move with it, and arterial speed rose.
- **Failed.** Cars would be driven no more than 3 per cent less in the seven
  dearest COE years than in the seven cheapest. Confidence 20%. Result: 11.0 per
  cent less, 17,600 km per car against 19,772.
- **Neither.** Once the number of cars is known, the COE premium would add nothing
  to explaining peak speed. Confidence 70%. Result: true on expressways; on
  arterial roads the premium still carried information, which is neither the pass
  nor the fail line.

## Was the HDB loan really cheaper than a bank's?

[Early HDB loans lost to any bank charging under 1.4 points](/economics/2026-10-03/).
Sealed 17 September 2026. Revisit 3 October 2027.

- **Held.** Borrowers who started in 2010-2015 needed a bigger bank margin to break
  even than those who started in 2020-2023. Result: lowest 2010-2015 figure 1.64,
  highest 2020-2023 figure 1.52.
- **Held (the headline).** Every 2010-2015 start needed more than 1.0 point over the
  benchmark for a bank to lose. Result: 1.64 to 2.05. A pass here is weak evidence,
  because the one bias in the design favours it.
- **Held.** No 2010-2015 borrower's bank advantage flipped before 2022 at margins up
  to 0.75. Result: none did.
- **Failed.** Every 2020-2023 start would flip to an HDB advantage within three
  years. Result: 15 of 24 cases did not, 10 of them never flipped at all.
- **Failed.** Refinancing whenever it paid would matter most for 2010-2015 starts
  and hardly at all for 2022-2025. Result: the reverse, 0.30 against 1.26 points.
- **Failed.** Switching from HDB to a bank in 2021 would leave every borrower worse
  off. Result: 31 of 66 cases worse, 35 not.
- **Held.** Switching early, in 2012 or 2015, would pay for 2010-2011 starts at
  margins up to 0.75. Result: 12 of 12 did.
- **Held.** The finance-company housing rate stayed above 2.6 per cent in every
  published month. Result: 150 of 150 months.

## Is an HDB flat really harder to afford than a decade ago?

[A four-room flat takes fewer years of income than in 2013](/economics/2026-09-19/).
Sealed 11 September 2026. Revisit 19 September 2027.

- **Neither.** From 2013, years of income for a four-room flat would rise by more
  than 0.5. Result: it fell 0.39, outside both the pass and the fail line.
- **Held.** From 2017, the same rise of more than 0.5. Result: up 0.76.
- **Held.** The HDB concessionary rate would move 0.1 points or less. Result: no
  move, a decade apart.
- **Neither.** Grants would cover more than 40 per cent of the price rise for a
  lower-income buyer. Result: 17 per cent, short of the pass line, above the fail
  line.
- **Failed.** Lower-income buyers' repayment burden would rise at least 5 points
  less than higher-income buyers'. Result: it rose 8.8 points more.
- **Failed.** Grants would fully offset the price rise for lower-income buyers.
  Result: their repayment share rose 9.3 points.
- **Neither.** Correcting for which flats sold would change the answer by more than
  3 points. Result: 2.2 points.
- **Neither.** Two correction methods would agree within 2 points. Result: 2.5
  points apart.
- **Held.** Median income would cross the frozen grant ceiling within the window.
  Result: it crossed in 2022.

## Where did the GST rises actually show up in prices?

[You can only see the GST rise in your water bill](/economics/2026-09-08/).
Sealed 4 September 2026. Revisit 8 September 2027.

- **Failed.** Taxed and untaxed prices moved in parallel before the rises, so they
  could be compared. Result: they did not, and the main design was declared invalid
  before it produced a number.
- **Failed.** The national index would show a January step close to the tax rise.
  Result: neither year did.
- **Failed.** The 2023 and 2024 estimates would agree within 0.3 points. Result:
  0.45 apart.
- **Held, with a caveat.** The 2007 mid-year rise would show a step of at least 1.4
  per cent. Result: it did, but most of it was the 2007 property boom.
- **Neither.** Some, but fewer than half, of price categories would over-shoot the
  tax. Result: 6 of 162 did; no verdict was recorded against the sealed wording.
- **Failed.** Januaries with no tax change would show no step. Result: they showed
  steps as large as the tax, so no national figure for how much of the GST reached
  prices could be published.

## Before the rule existed

The four COE pieces were written before this site sealed predictions in advance.
They are not scored here, and they are not retrofitted with predictions after the
fact.

## What this page will not do

It will not be edited to remove a failure. It will not gain a prediction written
after the data was seen. When a piece is re-scored against newer data, the result
is added here whichever way it comes out.
