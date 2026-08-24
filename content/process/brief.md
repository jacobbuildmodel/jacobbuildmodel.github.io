---
title: "How the weekly brief works"
description: "The method behind the weekly market brief: source tiers, the blank-page rule, and the failure modes it was built to avoid."
showToc: true
TocOpen: false
---

This covers the weekly market brief, which is the oldest thing on the site and currently the least
active. It is kept here because the source-tier system it introduced is used everywhere else, and
because the failure modes it documents were expensive to learn.

Most market commentary is unfalsifiable. It describes what happened, attributes a cause after the
fact, and never states what would have counted as being wrong. This page describes the rules this
site is written under, so that a reader can check the work rather than take it on trust.

## What the brief is trying to add

A stock's filed financials, its price history, and its analyst coverage are all freely available and
already priced. Restating them is not analysis. The brief is written against a fixed question:
**what is true that is not in a filing, not in a price series, and not yet consensus?**

That narrows the useful output to five categories.

| | What it means | Why it is hard to get |
|---|---|---|
| **Flows** | Money movement measured in dollars — ETF creations and redemptions, fund flows, 13F changes, insider-buying clusters | Not derivable from price; requires locating the actual measurement |
| **Cause** | The policy, regulation, supply agreement, or disclosure behind a move | Requires reading past the headline to the mechanism |
| **Forward catalysts** | Dated, scheduled events not yet reflected in expectations | Requires building a calendar, not reacting to one |
| **Discovery** | Themes and companies outside the well-covered mega-cap complex | Coverage is thin precisely where it is uncomfortable to look |
| **Regime** | Which factor the market is currently paying for — growth, duration, quality, cash flow, defensives | Only visible across assets, not within one |

If a paragraph in a brief serves none of these, it should not be there.

## Source tiering

Every figure a conclusion could rest on carries a tag. The point is that a reader can see
immediately how much weight a number can bear.

{{< tag "hard-co" >}} Company-filed. Straight from a 10-Q, 10-K, or 8-K.

{{< tag "company-prelim" >}} Guided or preliminary. Management's number, not yet filed.

{{< tag "hard-flow" >}} A measured fund flow, in currency, from a flow provider or fund disclosure.

{{< tag "consensus" >}} Sell-side aggregate. Useful as a description of expectations, not of reality.

{{< tag "price-proxy" >}} Price movement used as a stand-in for flow. Weak. Labelled so it is never mistaken for the real thing.

{{< tag "cong-disc" >}} Congressional or insider disclosure filing.

{{< tag "spec" >}} Speculative or undated. Carries no decision weight and says so.

**A figure that cannot be tiered gets zero weight and is marked as such inline.** Where a number
could not be sourced, the brief says "figure not obtained" rather than reaching for an approximation.
That is a deliberate choice: an admitted gap is information, a fabricated number is damage.

## Rules the brief is written under

**Blank page.** No prior brief is read before writing a new one. Not for continuity, not for tone,
not for grading old calls. The reason is that a brief which grades its own prior claims becomes a
closed loop — last week's error gets laundered into this week's evidence, and last week's framing
quietly constrains this week's search. Continuity is a reader's job, and the archive is public
precisely so it can be done.

**Portfolio-blind.** The brief is written without reference to any holding. There are no recurring
monitoring blocks around particular companies, because that is how coverage silently narrows to
whatever is already owned.

**Deltas, not levels.** A backlog above fifteen billion dollars means nothing on its own. Whether it
rose or fell, and against what, is the entire signal.

**Moves are paired with participation.** A theme up twelve per cent on 0.6x average volume is a weak
signal, and saying so is more useful than reporting the twelve per cent.

**Price is not flow.** Money "flowing into" something means dollars were measured moving. A rising
price is a {{< tag "price-proxy" >}} and is labelled that way every time.

**Where flow and price disagree, flow leads.** Institutions creating ETF shares into a falling price
is among the more informative things a week can produce, and it is stated explicitly when it happens.

**Non-technology coverage is mandatory, not incidental.** Each brief carries at least two items
outside technology and at least one company under roughly twenty billion dollars of market
capitalisation. Availability bias is the default failure mode of market writing; this is the
correction.

**No technical analysis.** No support levels, no RSI, no chart patterns. Trend and volume appear only
as flow evidence at theme level.

**No hedging.** "May", "could potentially", "it remains to be seen" are removed. State what is known,
tag the confidence, stop.

**A quiet week is written short.** Padding a slow week with restated facts is the most common way
this kind of writing goes wrong. If little happened, the brief says so and ends.

## Falsifiers

Every thesis on this site carries two things: the observation that would disprove it, and a date or
window by which that observation should have arrived. A claim without a falsifier is not a claim, it
is a mood.

The **Disconfirmation Watch** section of each brief grades live theses — both consensus positions the
market is currently holding and claims made inside that same brief — as `confirmed`,
`leaning disconfirmed`, `disconfirmed`, or `new variable`.

## Known failure modes

These are the specific ways this brief has gone wrong, kept public because a method that only lists
its principles and not its failures is marketing.

| Failure | What it looked like |
|---|---|
| **Price dressed as flow** | "Money is moving into X", citing only a price rise |
| **Return without participation** | A theme's weekly gain reported with no volume context |
| **Restating levels** | A backlog figure quoted flat, as though the level were news |
| **Missing same-day news** | Publishing hours after a major story broke on a covered name. A brief once went out the day merger talk moved a covered stock nine per cent and omitted it entirely |
| **Fabricated figures** | A contract award once carried at $95.9M was actually $742K. This is why unsourced numbers are now written as "not obtained" |
| **Availability bias** | Every item traceable to the same two or three outlets |
| **Padding a quiet week** | Long paragraphs restating known facts |

## What this site does not do

It does not recommend trades. It does not size, rank, or tell anyone what to buy. It does not
disclose positions, performance, or returns — partly because that information invites the wrong kind
of reading, and partly because a public track record incentivises writing that defends prior calls
rather than testing them.
