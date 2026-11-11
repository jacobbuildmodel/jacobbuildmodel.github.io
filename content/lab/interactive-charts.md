---
title: "Chart lab: interactive charts"
question: "Can a chart be scrubbed, played and questioned, and still be clear on a phone?"
date: 2026-11-11
draft: true
showToc: false
hidemeta: true
summary: "Prototypes, not published. Existing figures rebuilt so a reader can move through time, switch the measure, ask about any point, and pick the year a comparison starts from."
---

These are prototypes for review. The page is a draft: it is not built on the live site.
Each chart below is an existing figure, drawn again from the same pipeline output, with
the same numbers. Two come from published pieces. The third, on the Singapore dollar,
belongs to a piece that is not published until 14 November 2026, and is built from that
piece's review files. With JavaScript switched off, each chart shows the static figure,
the "how to read this" text and the table.

Round one, the first three charts, is the restrained baseline. Round two, under it, pushes
the look and the interaction further in three different directions, so they can be compared
side by side.

## Round one: the baseline

### HDB affordability: move through the years

{{< ichart "hdb_years_of_income" >}}

### COE or ERP: speeds against the target bands

{{< ichart "erp_peak_speeds" >}}

### The Singapore dollar and the yen: switch the measure

{{< ichart "sgd_measure" >}}

## Round two, direction A: explain this point

Tap any point and a card reads it in plain words: the value, the change from the year
before, where it ranks, and how far it sits from the target band or from the first year.
The sentences are worked out from the data when the page is built. None is typed by hand,
and none comes from a live model.

{{< ichart "erp_peak_speeds" "explain" >}}

{{< ichart "hdb_years_of_income" "explain" >}}

## Round two, direction B: build the comparison

The reader picks the year the comparison starts from, and the chart answers against that
year. The bars under it give the answer for every starting year at once.

{{< ichart "hdb_years_of_income" "compare" >}}

## Round two, direction C: instrument panel

A dark panel that stays on screen while the story scrolls under it. Each step of the story
moves the panel to its year. The numbers run to their values and the line glides between
years. With reduced motion switched on in the device settings, nothing moves by itself.

{{< ichart "erp_peak_speeds" "panel" >}}

*Prototype page. A historical reading of public data, about what happened, not a forecast.
It is not financial advice.*
