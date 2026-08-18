---
title: "Method"
date: 2026-08-17
lastmod: 2026-08-17
showToc: true
TocOpen: true
hidemeta: false
summary: "How the weekly brief is produced: what counts as evidence, how claims are tiered, and what would prove them wrong."
---

Most market commentary is unfalsifiable. It describes what happened, attributes a cause after the
fact, and never states what would have counted as being wrong. This page describes the rules this
site is written under, so that a reader can check the work rather than take it on trust.

## The one-sentence version

Every brief is written from a blank page, sources evidence published that week, tags each
decision-carrying figure with how it was obtained, and attaches to every claim the observation that
would kill it.

## The structure: news, sector, standouts

The site is organised as a funnel, each layer narrower and more specific than the one before it.

**[News](/news/)** is factual: what moved, what the data says, verifiable and checkable by anyone.
**[Sector](/sector/)** is a general read on which sectors the data favours, through a fixed panel read
the same way every week. **[Standouts](/standouts/)** is the narrowest layer — specific companies
screening strongest within those sectors, with the mechanism and the falsifier that would prove it
wrong.

Each layer earns the next. The point of writing it this way isn't just clarity — it's that each layer
gets progressively more careful about staying general rather than personal, for reasons the
[compliance](#why-this-isnt-financial-advice) section below explains.

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

**Moves are paired with participation.** A theme up twelve per cent on 0.6× average volume is a weak
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

## Where the machine ends and I begin

The brief is produced with substantial AI assistance and it is worth being precise about the
division, because vagueness here is the thing that should worry a reader.

The language model runs the search, sweeps the tape, and drafts to a system specification I wrote and
have revised through eight versions. That specification is the actual work: it encodes the
monopolies above, the source tiers, the failure modes below, and the hard requirements on
non-technology coverage and market-cap floor. Left unconstrained, a model writes fluent,
well-hedged, availability-biased market commentary. Nearly every rule on this page exists because an
earlier version produced exactly that and I had to build the rule to stop it.

I do the editorial pass: verifying figures that carry weight, cutting anything that restates a filing
or a price move, and killing claims I cannot defend. Errors that survive to publication are mine.

A separate scoring system I maintain consumes the brief privately. Its outputs — position sizing,
ranking, anything resembling a recommendation — are not published here and never will be.

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

## Why this isn't financial advice

This matters enough to be explicit about, not just for readers but because it shapes how every layer
above is written.

Under Singapore's Financial Advisers Act, a communication is generally treated as financial advice
when it expresses an opinion on the merits of buying, selling or holding a specific investment product
or a class of them, *and* a reasonable recipient could expect it to be relied on — which turns on
whether it's tailored to that person's particular circumstances, whether it recommends a course of
action, and whether the person providing it holds themselves out as a professional adviser. Naming a
company or a sector isn't the deciding factor. Personalisation is.

So the rules that follow aren't a workaround — they're the actual thing that keeps this a research
record instead of an advisory service:

- **Nothing here is tailored.** Every reader sees the same page, regardless of their goals, holdings,
  income, or risk tolerance. Content that responds to an individual's specific situation is
  categorically different from what's published here, and this site doesn't do that.
- **Nothing here tells you to act.** Mechanism, evidence, and falsifier — never "buy," "sell," a price
  target, or a position size.
- **I don't claim to be a professional.** No "analyst," no "research house," no implied credential.
  This is one person's documented reasoning, published under his own name.
- **If you ask what to do with your own money, the answer is the same every time:** *"I can't comment
  on that — I'm not a licensed financial adviser. If you're weighing a real decision, a licensed
  adviser can account for your actual situation in a way a public post never can."* That line doesn't
  change based on who's asking or how the question is framed.

See the [disclaimer](/disclaimer/) for the full statement.
