---
title: "Merging COE Categories A and B: LTA's Proposal on One Page"
date: 2026-10-27
draft: false
showToc: false
hideMeta: true
repo: "https://github.com/jacobbuildmodel/coe-analysis"
# Decision strip (layouts/partials/decision_strip.html)
decider: "LTA"
decision: "COE categories for cars"
opened: "8 Oct 2026"
closes: "2 Nov 2026, 23:59"
status: "Open"
reply_sent: "15 Oct 2026, 00:44"
# Figure 1 (layouts/partials/lta_road.html), placed just before this heading
# by layouts/decisions/_markup/render-heading.html; the body below is
# coe-analysis lta-ab/ONEPAGER.md at a3ca1ed without its H1, byte for byte.
figure: "lta-road"
figure_before_heading: "What the bidding record shows"
# The bands data under the figure. Pinned to coe-analysis PR #16's head until
# that PR merges; then this becomes .../blob/main/lta-ab/out/bands.csv.
data_url: "https://github.com/jacobbuildmodel/coe-analysis/blob/a3ca1ed8a5bd4817d3bebcce10c5caec3cf0edc7/lta-ab/out/bands.csv"
changelog:
  - "27 Oct 2026: first version, six days before the consultation closes."
---
**Jacob Ong**, 22 October 2026. The question and choices here are mine; the text was drafted by AI under my direction; a separate AI checker recomputed every number.

## Summary

LTA proposes one car COE category, with a rebate or surcharge set by model value.

- **Named cars:** the two BYD Sealion 7 versions would be $15,000 apart in surcharge under three bands and $7,500 under five (as proposed, not final).
- **Record:** Category A's COE price was higher than Category B's in 21 of 397 bidding exercises, from January 2010 to the first exercise of October 2026.
- **Balance:** at the 2025 mix behind LTA's tables, surcharges exceed rebates by $2,250 a car on average; a starting point, not a forecast.

## What is LTA deciding?

LTA proposes a feebate, a rebate or surcharge on the COE price (paragraph 2.9), banded by each model's median Open Market Value (OMV) as a percentile of 2025 registrations (paras 2.15-2.18):

- **Option A:** 0-35th percentile, $15,000 rebate; 35th-50th, $0; above 50th, $15,000 surcharge.
- **Option B:** 0-10th, $15,000 rebate; 10th-35th, $7,500 rebate; 35th-50th, $0; 50th-75th, $7,500 surcharge; above 75th, $15,000 surcharge.

Views close 2 November 2026, 23:59; findings are expected in the first half of 2027.

## What would it mean for named cars?

The two BYD Sealion 7 versions sit one band apart under both options.

Table 1. Examples from LTA's Tables 1-2 (as proposed, not final)

| Model | Option A (three bands) | Option B (five bands) |
|---|---|---|
| Toyota Sienta | Band 1, -$15,000 | Band 2, -$7,500 |
| BYD Sealion 7 Dynamic | Band 2, $0 | Band 3, $0 |
| BYD Sealion 7 Performance | Band 3, +$15,000 | Band 4, +$7,500 |
| Toyota Alphard | Band 3, +$15,000 | Band 5, +$15,000 |

Notes: minus, rebate; plus, surcharge. All 30 named models: lta-ab/out/bands.csv.
Sources: LTA, Tables 1-2; lta-ab/16_bands.py.

## What the bidding record shows

Category A cleared above B in 21 of 397 exercises from January 2010 to October 2026, exercise 1; later exercises are not counted; 3 were in 2026 (lta-ab/out/a_above_b.csv; lta-ab/NOTE.pdf).

## Where the design could go wrong

**(a) Balance.** Of the 2025 registrations behind LTA's tables, about 50 per cent sit in surcharge bands and 35 per cent in rebate bands, so at that mix surcharges exceed rebates by $2,250 a car on average under both options. A starting point, not a forecast: once set, a model's band follows its value, and a rebate makes cars in rebate bands cheaper, so buyers can shift towards them, shrinking the net, possibly reversing it. Bands are set by OMV percentile and reviewed annually (para 2.15), method not stated; if cut-offs are re-set by percentile at each review, surcharges again exceed rebates. A centred design starts neutral; a yearly published balance shows where it stands.

A merged premium clears where one quota meets all bids, so it need not equal the A and B average. A Straits Times illustration (Instagram, 18 October 2026) takes the merged price as the average of the A and B premiums. This page gives no direction for it; a sealed prediction follows in December.

**(b) Category E.** Category E certificates register any car (para 2.21). Since May 2022 Category E cleared at or above both A and B in 74 of 107 exercises, and across all 107 a median $888 above B: far below a $15,000 surcharge. The paper does not say whether the feebate applies to such cars. Unless the feebate follows the car, Category E could become the cheaper route for the most expensive cars.

**(c) Cliffs.** At each cut-off, a model just above pays a full step more: $15,000 under three bands, $7,500 under five. Elsewhere, car tax thresholds drew models to their cheaper side (Sallee and Slemrod 2012; Ito and Sallee 2018).

## What I sent

I sent my own views through LTA's form on 15 October 2026 at 00:44 SGT, in a personal capacity: [SUBMITTED_REPLY.md](https://github.com/jacobbuildmodel/coe-analysis/blob/main/lta-ab/SUBMITTED_REPLY.md). It supports the merger with a feebate ("my first choice is a sliding scale; if LTA keeps bands, five rather than three"), asks LTA to centre the design and publish the balance yearly, asks that the feebate apply to cars on Category E certificates, and says "I would not apply the feebate at renewal."

## What this site will check

As LTA publishes them, the measures the reply asked for: the yearly balance of rebates and surcharges; registrations either side of each cut-off; cars in each band on Category E certificates; private-hire and leasing shares by band; an evaluation after two years. In December the site seals its prediction for the merged premium.

## LTA's feedback form

LTA's form, https://go.gov.sg/coe-pcd-feedback, closes on 2 November 2026 at 23:59.

## Scope

LTA's proposal, its example bands (as proposed, not final) and the bidding record to October 2026, exercise 1. No forecast of the merged premium.
