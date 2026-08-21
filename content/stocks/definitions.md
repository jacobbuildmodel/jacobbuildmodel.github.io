---
title: "How the scores are calculated"
date: 2026-08-19
showToc: true
TocOpen: true
summary: "Every figure on a stock page, what it measures, and how it's worked out."
_build:
  list: never
---

Everything on a stock page describes the **business**. Nothing says whether the shares are worth
buying. There is no overall score, no ranking of one company against another, and no buy or sell
call anywhere on this site.

Most of what follows is arithmetic on filed accounts. Where something is a judgement, it says so.

## Balance sheet resilience

**Scale 1 to 5.** How well the company could survive a bad stretch without needing to raise money.

Computed from net cash or net debt, debt relative to shareholder funds, and the current ratio. For
companies not yet profitable, months of cash left at the current burn rate.

| Score | What it means |
|---|---|
| 1 | Fragile. A bad year creates real financing pressure. |
| 2 | Stretched. |
| 3 | Ordinary. Manageable debt, no particular cushion. |
| 4 | Comfortable. |
| 5 | Fortress. Could absorb a severe downturn without flinching. |

## Margin trend

**Expanding, stable, or compressing.** Which direction profitability is moving, measured against
both the previous quarter and the same quarter a year earlier.

Not a score, because a direction isn't a quantity.

## Dilution trend

**Two figures, always.** The three-year annual growth rate in share count, *and* the most recent
quarter.

Both are needed because they routinely disagree. A company can show heavy three-year issuance while
having largely stopped, or the reverse. One figure alone would mislead. Where the basic and diluted
share counts diverge meaningfully, both are shown.

If a company issues more shares, existing owners hold a smaller slice of the same business. Some
issuance is normal where staff are paid partly in shares. Persistent heavy issuance is worth
noticing and rarely appears in a headline.

## Statement integrity

**Clean, flagged, or red-flag**, always accompanied by which checks *passed*.

A set of standard accounting-quality checks runs against the filings: whether net profit exceeds
operating profit, share-based pay as a share of revenue, cash flow against reported earnings, how
long customers take to pay, and inventory movement.

Showing only the flags would be misleading. A company can trip one check while passing the one that
matters most, and that combination is a very different picture from tripping several. So the passed
checks are always listed alongside.

**A flag is not an accusation.** These checks produce false positives and plenty of honest companies
trip one for innocent reasons. It means look closer, nothing more.

## What the revenue rides on

**A statement, not a score.** What this company's sales actually depend on: the economic cycle,
government budgets, a commodity price, consumer credit, or something else.

This replaced a cyclicality score during testing, because the score was measuring the wrong thing. A
company with eight unbroken years of growth scores as perfectly stable, even when half its revenue
depends on government spending decisions that could change in a single budget. The number looked
precise and hid the actual risk. The sentence naming what the revenue rides on is more useful and
harder to misread.

## Customer concentration

**A percentage, not a score.** How much of revenue comes from the largest customers.

Shown as the disclosed figure. Where no customer exceeds the disclosure threshold, that shows as
**not concentrated**. Where a company doesn't disclose it, **not disclosed**.

Expect "not disclosed" often. Many large companies report concentration without naming who the
customers are, listing them only as Customer A, B and C.

## Recurring revenue

**A percentage where the company publishes one.** How much of revenue arrives again next year
without winning a new sale.

Three possible answers, and the distinction matters:

- **A percentage** where the company discloses it.
- **Not applicable** where the concept genuinely doesn't apply. A bank or an oil producer has no
  subscription base.
- **Not disclosed** where the business clearly is subscription-based but the company doesn't publish
  the figure. Some large subscription businesses don't. Calling that "not applicable" would be
  false, and inventing a number would break the rule that every figure here traces to a filing.

## What isn't here, and why

**Moat strength and pricing power** were designed as scores and cut after testing.

Moat was scored 1 to 3, but in practice nothing publishable ever scored 1, making it a two-point
scale pretending to be three. Both were pure judgement, which conflicts directly with the rule that
every score shows its arithmetic. And both were only available for certain kinds of business, so
pages carried or omitted them with no explanation a reader could see.

The underlying evidence was always the useful part, and it now appears as plain prose instead: that
gross margins held flat through a large volume increase says more about pricing power than a number
out of five ever did.

**AI-resistance** was cut before launch for the same reason in a stronger form: nothing behind the
scenes measured it at all. It would have been a guess with a number attached to look rigorous.

## Coverage

Companies appear here only when there's real evidence behind them, drawn from filings rather than
from any internal summary. A large number of companies sit in the underlying system with a score and
no supporting work. None of those are published. If a company isn't listed, the work hasn't been
done.

---

*These figures describe businesses. They are not investment advice, not a recommendation, and not
tailored to anyone's circumstances. See the [disclaimer](/disclaimer/).*
