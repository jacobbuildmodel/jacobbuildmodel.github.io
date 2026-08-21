---
# ── COPY THIS FILE for each company. Rename to the lowercase ticker: nvda.md ──
# URL becomes /stocks/nvda/ — evergreen, not dated. Update in place.
title: "TODO: Company Name (TICKER)"
ticker: "TICKER"
company: "TODO: Company Name"
date: 2026-01-01
draft: true
showToc: true
TocOpen: false
summary: "TODO: one sentence a 15-year-old would understand."
tags: ["stocks"]
---

> TODO: two sentences. What is this company, in the plainest words possible?

## What it actually sells

Concrete. Not "a data analytics platform" — what is the thing, who uses it, what does it do for
them.

For companies where no honest short description exists, the pilot found only one thing that works:
**one specific worked example, then generalise from it.** Not a category, not an abstraction. A
single concrete situation the reader can picture, followed by "and the same applies to..."

Every genuinely hard-to-explain company needs its own example invented from scratch. This is the
most expensive part of the page and it does not get easier with practice.

## How a dollar arrives

Who pays, for what, how often, and whether it repeats.

**Ratios, not raw dollars.** A contracted revenue figure means nothing on its own; the same figure
expressed as a share of a quarter's sales is immediately readable. Where an absolute number is
genuinely the point, give the denominator beside it.

## What the business is made of

The segments and roughly what share each is.

**A company may publish more than one split that doesn't reconcile** — one by product line, another
by reporting segment, for the same revenue. Show both and say they're different cuts. Don't pick one
silently.

## Who buys it, who competes

**Customers.** Name them where disclosed. Expect **"not disclosed"** to be the normal answer:
plenty of large companies report that three customers are most of their revenue while identifying
them only as Customer A, B and C.

**Competitors.** Name them where the company does.

**If the company names no competitor, say that explicitly first**, then list the market-consensus
alternatives clearly labelled as not company-sourced. Some companies state they compete against
customers' own internal teams rather than against named firms, and that fact is itself worth
reporting. Without this rule the writer imports a list from memory and presents it as disclosure.

Competitors means who competes for the same customers, which is not the valuation comparison set.

## What would break it

What would have to change for this business to be in real trouble.

## How it's owned and controlled

Governance, where there's something worth knowing: dual-class shares, founder voting control, a
structure where a small economic stake carries a large share of the votes.

**Omit this section entirely for ordinary single-class companies.** It exists because the pilot
found a share structure carrying roughly 4% of the economics and up to 49.999999% of the votes,
which doesn't "break the business" and so had nowhere else to go.

## What most people get wrong

The commonly misunderstood thing.

**This section may reference the dollar mechanics above rather than restating them.** On both pilot
names the most misunderstood thing *was* how the money actually works. If that's the case here, say
so briefly and point back rather than writing it twice.

## The business at a glance

{{</* attr-open */>}}

{{</* exposure value="Government budgets" why="One line naming what sales actually depend on." */>}}
{{</* stars label="Balance sheet resilience" value="4" max="5" why="Net cash position, debt to equity, current ratio." */>}}
{{</* trend label="Margin trend" value="Expanding" why="Versus prior quarter and prior year." */>}}
{{</* trend label="Dilution trend" value="+7.5% over 3 years, +0.2% last quarter" why="Both figures required — they routinely disagree." */>}}
{{</* integrity value="Flagged" flagged="Which checks tripped." passed="Which checks passed — required, never omit." */>}}
{{</* fact label="Customer concentration" value="Top 3 = 54% of revenue, not named" */>}}
{{</* fact label="Recurring revenue" value="Not disclosed as a percentage" */>}}

{{</* attr-close */>}}

[How these are calculated →](/stocks/definitions/)

---

<!--
PRE-PUBLISH CHECKLIST. Delete before publishing.

  SUBSTANCE
  [ ] Someone with no finance background could follow every section
  [ ] Section 1 uses a concrete worked example if the company is hard to explain
  [ ] Ratios, not raw dollars — every absolute figure has its denominator
  [ ] Multiple revenue splits shown where the company publishes more than one
  [ ] Competitors: named, or "company names none" stated explicitly before
      any consensus list, which is labelled as not company-sourced
  [ ] Customers: "not disclosed" is a normal and acceptable answer
  [ ] Governance section present only if there's something worth knowing
  [ ] Statement integrity shows BOTH what flagged and what passed

  SOURCING
  [ ] Every figure traces to a filing, not to an internal card or summary
  [ ] Card material re-verified against the filing before use — cards go
      stale and can miss an entire quarter

  HARD RULES
  [ ] No overall score, no ranking, no buy/sell call
  [ ] No moat or pricing-power score (cut — judgement, no arithmetic)
  [ ] No cyclicality score (replaced by the exposure statement)
  [ ] No AI-resistance score (cut — nothing measures it)
  [ ] No CQS, band, tier, or Track labels (the gate refuses these)
  [ ] No price target, no valuation verdict

  MECHANICS
  [ ] Filename is the lowercase ticker; ticker + company set in front matter
  [ ] draft: false
-->
