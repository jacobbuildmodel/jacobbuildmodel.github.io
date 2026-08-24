---
title: "How the economics research works"
description: "What licenses a causal claim, how the data is handled, and what gets published when a result doesn't work."
showToc: true
TocOpen: false
draft: true
---

This covers the [Economics](/economics/) pieces specifically. The two rules on the
[Method page](/process/) apply here as everywhere: every number traces to a source, and every claim
carries what would prove it wrong. Causal claims need more than that, and this is the more.

Opinions about markets are easy to form and hard to test. Everything on this site starts
from a question people already have a strong view about, puts primary data next to the
view, and tries to work out what is actually going on.

This page is the part that makes the rest checkable. It covers how a causal claim gets
licensed, where the numbers come from, what happens when one turns out to be wrong, and
what I will not write about.

## How a claim gets licensed

Two things moving together is not evidence that one causes the other. Most of the work in
a research piece is not the arithmetic. It is explaining why a causal reading is allowed
at all.

Every piece says which of three situations it is in.

**A causal claim with a stated strategy.** Something in the world holds one side of the
market still, so the movement can only be coming from the other side. The COE auction is
the clean case: the Land Transport Authority fixes the quota before bidding opens, and no
matter how high the price climbs, not one extra certificate appears. Supply is a vertical
line, and the price that clears the auction is therefore a point on the demand curve. When
a piece claims cause, a paragraph like that one exists and is specific.

**A conditional claim.** The relationship holds once something is held constant, and the
piece says what and why. Year fixed effects, for example, mean the comparison runs between
bidding exercises inside the same year, so anything that moved slowly across the whole
period cannot be producing the result.

**A correlation, called a correlation.** Two series move together and nothing in the data
separates cause from effect. The piece says so, and says what evidence would settle it.

A claim that fits none of the three does not get published.

## The residual has a size, not a name

When an analysis shows that supply explains none of a price rise, it has measured how
large the unexplained part is. It has not measured what is inside it. Incomes, population,
credit conditions, foreign buyers, changing preferences and my own omissions all sit in
there together, and no amount of staring at the same data separates them.

So pieces here report the size of a residual and refuse to name its contents. "Demand rose"
is a description of the gap. "Demand rose because incomes rose" is a different claim,
needing different data, and it does not appear unless that data is in the piece.

## The shape of an argument

Seven functions, always in this order. The visible headings change to fit each argument,
because a heading should name the finding rather than the job it is doing. The sequence
underneath does not change.

| Function | What it does | Words |
|---|---|---|
| Hook | Two numbers that do not fit together, with no caveats yet | 100-150 |
| Why it is answerable | The identification logic, in plain words | 200-300 |
| The data | Source, period, and anything wrong with the file | 100-200 |
| The finding | Charts before coefficients | 250-350 |
| The payoff | What the finding implies. This is why the piece exists. | 300 |
| What would break it | The specific observation that would prove it wrong | 250 |
| What it does not explain | The residual, named honestly | 200 |

Then sources, with retrieval dates and links to the primary file.

## Two depths in one page

The linear read runs about 1,800 words and takes eight minutes. It proves one thing, and
someone reading on a phone gets the whole argument from it.

Underneath sit the collapsible sections: how an estimate was built, the specifications I
rejected and why, robustness tables, the full list of figures with sources. A reader who
opens everything is there for half an hour.

Nothing in the collapsed layer is load-bearing. If the argument does not stand without it,
it is not an aside, it is a paragraph I hid.

## Where the numbers come from

Primary sources only. For Singapore economics that means data.gov.sg, the Department of
Statistics, LTA, HDB, MAS and MOM. For company work it means the filing itself, named by
form type and filing date. News reporting is used to find out that something happened,
never as the source of a figure.

Every figure in a piece is listed in a manifest alongside the draft, with the source and
the retrieval date, and each line is ticked against the original before the draft flag
comes off. A number that cannot be sourced is reported as unavailable rather than
estimated. Saying a figure could not be obtained is a real finding and it gets written
that way.

Where a number is computed rather than read off, the piece says what was divided by what,
so the arithmetic can be repeated.

## When something is wrong

**In the source.** Government files contain errors. Checking the COE bidding results
against internal consistency turned up two: a motorcycle premium recorded as $20,090 when
the correct figure was $852, and a quota recorded as 1,154 when it was 693. Both were
values copied from the row above. Neither was corrected until it had been matched against
an independently published figure for the same day, both corrections are stated in the
piece that uses them, and the cleaning script asserts the original wrong value so it will
fail loudly if the source is ever fixed.

**In something I published.** A correction note goes at the top of the piece, dated, saying
what the figure was, what it should have been, and how the error happened. The original
wording stays visible. Nothing gets quietly edited, because a site whose whole claim is
that the numbers were checked cannot also be a site where numbers change without notice.

## Results that did not work still get published

Most write-ups appear only when the data agreed with the author. That selection is
invisible to a reader and it makes every published result less trustworthy than it looks.

So the rule here is that a test I set up in advance gets reported whichever way it comes
out. A hypothesis that fails is written up as a hypothesis that failed. Where a test turns
out to have no power to detect anything, that gets said too, and the piece shows the
placebo check that established it rather than quietly dropping the section.

Pieces also mark which findings were predicted before the analysis ran and which turned up
along the way. Both are worth having. They are not worth the same amount, and pretending
otherwise is the most common way research writing misleads.

## What the linter blocks

Drafts run through a script before publication. It measures the things that make prose read
as machine-written, and it checks for characters that break the build.

| Check | Threshold |
|---|---|
| Em dashes per 1,000 words | flags above 8; published human prose averages 4.76 |
| Sentence length variation | flags below a standard deviation of 7 |
| Sentences opening with The, This, It or In | flags above 42% |
| Hedge preambles, boilerplate closers, borrowed vocabulary | flags any |
| "Significant" used without a p-value nearby | flags any |
| Non-ASCII characters | blocks the build |

The word "significant" carries only its statistical meaning in a piece containing
regressions. Where the point is size rather than a p-value, the piece says large, or sharp,
or gives the number.

## Replication

Every piece links to a directory containing the raw file as downloaded, the cleaning script
with its corrections, the analysis scripts in the order they run, and the exact
specifications reported. Running them in order reproduces every figure in the piece.

If a result cannot survive someone else running the same code on the same file, it is not a
result.

## Scope and limits

I am not licensed by the Monetary Authority of Singapore and nothing here is financial
advice.

**No securities work in the economics pieces.** COE premiums, housing affordability and
labour statistics are not investment products. Where an economic finding might lead
somewhere investable, the piece stops at the economics.

**Nothing tailored to one person.** No content responds to an individual's situation.

**No policy recommendations.** These pieces explain what the data shows. What a government
ought to do about it is a different question, involving trade-offs the data does not
contain, and I do not answer it.

**Reasoning, not recommendations.** The point of the site is the argument and the evidence
behind it. A reader who disagrees with a conclusion should be able to find the exact place
where we part company, and check it themselves.
