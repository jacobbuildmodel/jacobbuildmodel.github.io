---
title: "How the scorecard works"
description: "How each prediction is sealed, tested and scored, and who does each step."
ShowRssButtonInSectionTermList: false
---

## The promise

Singapore's favourite arguments, tested with public data. Before I open the data, I write down my
prediction and seal it.

## The cycle

Since September 2026, every scored piece has followed these steps:

1. Pick a question.
2. Write the prediction and, from October, its confidence.
3. Seal it (a dated commit with md5 fingerprints of every sealed file) before the data is opened.
4. Open the data and run the test.
5. Score it on the [scorecard](/scorecard/): held, failed, or neither.
6. Publish, failures included.

## Who does what

| Step | Who |
|---|---|
| Picks the question | Jacob |
| Writes the prediction and sets its confidence | Jacob |
| Seals the prediction before the data is opened | Jacob |
| Research, code and first drafts | Claude (an AI model by Anthropic), under rules Jacob sets |
| Recomputes every number from a fresh copy | a separate AI checker |
| Reads some drafts before publication | outside readers, not named |
| Edits, approves and publishes every page | Jacob |

No one pays for this work, and no one but Jacob approves it before it is published.

## Where the AI fits

Most pages here are produced inside a research workflow I designed and run. Claude, an AI model made by
Anthropic, does the research, coding and drafting under rules I set; I write the specifications, decide
what counts as evidence, and do the editorial pass.

Saying so plainly matters more than it might seem. Nearly every rule on this site exists because an
early version produced something fluent and wrong, and I had to write a rule to stop it. That history
is the reason to trust the current version, not a reason to hide it.

Mistakes that reach publication are mine.

## What is sealed

Each seal fixes THESIS.md, the predictions with their pass and fail lines, in the piece's public
repository: [coe-analysis](https://github.com/jacobbuildmodel/coe-analysis),
[hdb-affordability](https://github.com/jacobbuildmodel/hdb-affordability) or
[gst-passthrough](https://github.com/jacobbuildmodel/gst-passthrough).
[research-checks](https://github.com/jacobbuildmodel/research-checks) re-checks every seal on every
change there.

## How the scorecard counts

In the scorecard's words: "**Held** means the sealed prediction survived. **Failed** means it did
not, and the article says so. **Neither** means the result landed between the pass and fail lines
written in advance, or no verdict was recorded, and it is not rounded to either side." A prediction
that could not be scored stays on the scorecard with its reason.

Predictions with a confidence count toward the calibration line. Its Brier score, where 0 is
perfect and a flat 50 per cent on everything scores 0.25, appears on the home page once 16 are
scored.

## Limits

Economics only, tested with Singapore public data. A prediction can be wrong for reasons the test
cannot see.

## Replies and corrections

Replies to public consultations are published too: the
[reply to LTA on COE categories](https://github.com/jacobbuildmodel/coe-analysis/blob/main/lta-ab/SUBMITTED_REPLY.md)
and its [one-page summary](/decisions/lta-coe-categories/). Every change to a published page is
listed on the [corrections page](/corrections/).

## Why this isn't financial advice

Under Singapore's Financial Advisers Act, a communication is generally treated as financial advice
when it expresses an opinion on whether to buy, sell or hold a specific investment, *and* a reasonable
reader could expect to rely on it. That turns on whether it's tailored to your circumstances, whether
it tells you to do something, and whether the writer holds themselves out as a professional adviser.
Naming a company isn't the deciding factor. Personalisation is.

So these aren't a workaround, they're what keeps this a research record rather than an advisory
service:

- **Nothing here is tailored.** Every reader sees the same page, whatever their goals, holdings,
  income or risk tolerance.
- **Nothing here tells you to act.** Mechanism, evidence, and what would prove it wrong. Never a buy,
  a sell, a price target or a position size.
- **I don't claim to be a professional.** No analyst title, no research house, no implied credential.
  One person's documented reasoning, published under his own name.
- **If you ask what to do with your own money, the answer is always the same:** I can't comment,
  because I'm not a licensed financial adviser. If you're weighing a real decision, a licensed adviser
  can account for your actual situation in a way a public page never can.

I'm not licensed by the Monetary Authority of Singapore. See the [disclaimer](/disclaimer/) for the
full statement.
