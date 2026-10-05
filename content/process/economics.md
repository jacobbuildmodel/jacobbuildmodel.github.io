---
title: "How the economics research works"
description: "What licenses a causal claim, how the data is handled, and what gets published when a result doesn't work."
showToc: true
TocOpen: false
draft: false
---

This covers the [Economics](/economics/) pieces specifically. The two rules on the
[Method page](/process/) apply here as everywhere: every number traces to a source, and every claim
carries what would prove it wrong. Causal claims need more than that, and this page covers that more.

Opinions about markets are easy to form and hard to test. Everything on this site starts
from a question people already have a strong view about, puts primary data next to the
view, and tries to work out what is actually going on.

This page is the part that makes the rest checkable. It covers how a causal claim gets
licensed, where the numbers come from, what happens when one turns out to be wrong, and
what I will not write about.

## Bets before the data

It is easy to explain a result after seeing it. Every piece here commits to its
predictions before the data is opened, in a form I cannot quietly change later.

1. **Start from an argument.** A question people in Singapore already disagree
   about, both sides at full strength, and a list of every data series each test
   will need. If a series does not exist, the test is dropped there, before
   anything is built on it.
2. **Write the tests down.** A file called `THESIS.md` states each prediction,
   the line it has to clear and what counts as failing, in plain words.
3. **Write the code blind.** The analysis scripts are written and tested on
   invented data, so no real number can shape them.
4. **Seal it.** One commit records a fingerprint (an md5 hash) of the thesis and
   of every script. Change a comma afterwards and the fingerprint no longer
   matches.
5. **Publish the bet.** The same day, an open question page goes up with the
   predictions and a link to the sealed commit.
6. **Then open the data.** Only once that page is live does a separate commit
   add the small file the scripts look for before they will read the raw data.
7. **List every later change.** `THESIS_ADDENDUM.md` records anything touched
   after the seal, dated, with fingerprints before and after. Wording and
   layout can change there. A test, a threshold or a score cannot.

Steps 2 to 7 have applied since the Progressive Wage Model piece, sealed on 28
September 2026. The data check in step 1 was added after that piece (see Lapses
on record). Earlier pieces sealed a thesis before opening the data, without all
of these steps.

A commit date on its own can be faked. The open question page is one outside
record of when a bet was made. From the next piece on, each sealed thesis is
also registered on OSF, an independent research archive whose time stamp I
cannot edit.

## Confidence, and keeping score

A prediction without a confidence cannot be graded. "The yen fell" and "I am 90
per cent sure the yen fell" are different claims, and only the second can be
shown to be overconfident.

So every prediction carries a number, set before the seal. I set those numbers
alone. The researcher may propose a number with a reason, and it is printed
beside mine, so anyone can see where the two numbers differed. The checker may raise
considerations but never suggests a number. If a debate moves one of my numbers
before the seal, both values are published.

The [scorecard](/scorecard/) counts every sealed prediction, held or failed, and
sets the number that held against the number my confidences expected. It also
reports a Brier score: the average squared gap between each confidence and what
happened. Always saying 50 per cent scores 0.25, and lower is better. A
confident miss costs far more than a cautious one, so the score rewards knowing
what I don't know.

A failure can be the right call. On the Singapore dollar piece I gave one
prediction 8 per cent, because I expected it to fail. It failed. That is the
system working.

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
because a heading names the finding rather than the job it is doing. The sequence
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

## Two depths for two readers

Each article is written for anyone: about 1,800 words, one argument, readable on
a phone. Next to it sits a page for researchers with everything the article
leaves out: the derivation step by step, each test in its sealed wording, every
robustness check and where the result turns over, where each series came from,
and the commands that rerun the whole thing from a fresh copy.

Nothing on the researcher page changes the article's conclusion. If the argument
does not stand without it, it is not detail, it is a paragraph I hid.

## Where the numbers come from

Primary sources only. For Singapore economics that means data.gov.sg, the Department of
Statistics, LTA, HDB, MAS and MOM, and for exchange rates the Bank for International
Settlements. News reporting is used to find out that something happened, never as the
source of a figure.

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
what the figure was, what the correct figure is, and how the error happened. The original
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

## House style checks

Drafts run through a script before publication. It enforces a house style that machine drafts
tend to break: plain sentences, varied length, no filler, and no characters that break the build.

| Check | Threshold |
|---|---|
| Em dashes per 1,000 words | warns from 6, blocks the build at 8 |
| Sentence length variation | flags below a standard deviation of 7 |
| Sentences opening with The, This, It, In, There, These or That | flags above 42% |
| Hedge preambles, boilerplate closers, borrowed vocabulary | flags any |
| "Significant" used without a p-value nearby | flags any |
| Six characters that break the build | blocks the build; other non-ASCII characters are flagged for review |

The word "significant" carries only its statistical meaning in a piece containing
regressions. Where the point is size rather than a p-value, the piece says large, or sharp,
or gives the number.

A second checker, Vale, holds the house wording: no first-person plural and no instructions to the reader.

## Who checks the work

A number is not right because the person who produced it says so, and that
includes me. Three checks sit between a draft and publication, and none of them
is done by the draft's author.

**The numbers.** A separate checker starts from a fresh copy of the code,
confirms the seal and every fingerprint, and recomputes every scored number from
the raw files with its own code. If its answer differs at the published
precision, the piece stops. The checker gets checked too: on the Singapore
dollar piece, the checker's own instructions listed one robustness result the
wrong way round, and the researcher wrote it correctly instead of copying it.

**The reading.** An editor reviews how a piece reads: the title alone, then the
opening alone, then the whole, against written rules. It cannot change a number
or how strongly a claim is made, and anything it rewrites goes back to the
checker.

**Real readers.** Titles go to friends who are not economists before they ship,
and when they disagree with the editor, they win. For the Singapore dollar
question, the editor's favourite was "Japan felt cheap. Was it our dollar, or
their yen?" My friends said it felt weird. They chose "Tokyo got cheaper. Did
Singapore get richer?" Every test is logged.

The checker, the editor and the researcher are AI models from the same family,
so they can share blind spots. That is why real readers get the last word on
titles, and why outside readers with economics training are invited to review
pieces.

## Who does what

Most of the work on this site is done by AI models (Anthropic's Claude), each in
its own session with its own job: one researches, writes the code and drafts;
one checks; one edits. They work inside written rules, and most of those rules
exist because an earlier version produced something fluent and wrong.

Some parts are mine alone:

- choosing each question, and deciding it is worth asking;
- setting every confidence before the data is opened;
- approving each sealed thesis, each title and each page before it goes live;
- running the reader tests;
- merging every change. Nothing reaches the site or the code without my
  approval.

That split is deliberate. A model can write a regression faster than I can. It
cannot decide which argument matters to people here, or put its name to a bet.

Mistakes that reach publication are mine.

## Lapses on record

Most rules on this site were written after something went wrong. Two that shaped
how it works now:

**A confidence that moved.** On the COE and ERP piece, after a debate with the
checker, two of my numbers changed before the seal: 20 to 35 per cent, and 80
to 65. My first numbers would have scored a Brier of 0.153; the ones I sealed
scored 0.194. Two outcomes do not prove the first numbers were better. The
problem is why they moved: no new evidence had come in. I changed them because I
lost an argument. Since then the checker can raise considerations but never puts
a number on the table, and any change after outside input is published with both
values.

**A test with no data behind it.** On the Progressive Wage Model piece, a
prediction about jobs was designed before anyone confirmed that a public count
of cleaners and security guards existed. It did not, so the prediction could not
be scored. Every test now names its exact data series, and that series is
confirmed to exist before anything is designed around it.

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
behind it. A reader who disagrees with a conclusion can find the exact point where the
disagreement starts, and check it there.
