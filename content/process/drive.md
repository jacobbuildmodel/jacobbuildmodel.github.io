---
title: "DRIVE: how I research listed companies with AI"
description: "A private system I built with AI to study listed companies. I make every decision, and each is logged before its outcome is known and graded once the outcome is in."
date: 2026-11-18
showToc: false
hidemeta: true
# A case-study page under How I work (SMU week, systems update, November 2026).
# Its content comes only from the system's own public-safe summary of 18 Nov
# 2026 and Jacob's rulings on it (WEBSITE folder, office/smu_week_2026-11/
# systems/ and MODERATOR_TO_MISSION.md sections 14 and 14a). Hard limits for
# this page: no tickers, company names, holdings, sizes, account values,
# returns, trade dates or buy and sell words; no results of any kind; nothing
# that reads as advice; the system's repository is never linked.
# Reworded on 19 Nov 2026 after three independent reads (WEBSITE folder,
# office/smu_week_2026-11/reviews_D/); the opening paragraph is Jacob's
# approved framing and was not touched.
# 19 Nov 2026: the checker's fixes 2 to 6 (reviews/smu_week/prD_verify_2026-11-19.md), in its words.
# Opening: Jacob's choice C with his own change (19 Nov 2026, DRIVEOPEN, MODERATOR_TO_MISSION.md
# section 20), his words exactly, with a full stop at the end.
# Changed on 19 Nov 2026 on the moderator's rulings (MODERATOR_TO_MISSION.md
# section 18): the shorter title; the two comparisons out of the grading
# sentence; three terms the summary does not explain taken out.
---

My approach to markets rests on three ideas: trend, growth and fundamentals. My portfolio
model is the system I built with AI to bring data to that approach. It scores listed
companies on the quality and valuation shown in their filings, and every decision is mine.

DRIVE, as my portfolio model is called, is private. Its code and records are not published, so a reader cannot check what
this page says. It is personal research, not advice to anyone.

## My role

I set the goals, write the rules in plain English, rule on disputes and make every
decision; the system has no brokerage access. AI writes all the code, drafts formulas and
tests, and runs them.

Three cases where I overruled the AI:

- **23 September 2026.** A valuation table the AI wrote was more generous than the study
  it cited, up to 20-fold in one cell, and 95 score cards had used it. Offered a blend of
  the two, I chose the source.
- **14 October 2026.** Hand-off notes told the scorer what I owned and that its earlier
  verdict had been overruled. I ruled that it receives only evidence and a question.
- **15 October 2026.** Of the 9 tests registered in the system's lab, 7 had no date for a
  verdict. I required a goal, an expected result, a decision and a deadline before a
  test's data is opened; the code now refuses a test without them.

## How it works

DRIVE runs as a loop. AI assistants, each with one job, collect public data and score each
company's quality and valuation from its filed accounts, blind to what I own. Their findings are
reconciled by the rank of the evidence: filed, company-stated, market, analyst. Candidates are ranked mechanically, and a critic then argues against each one. I then decide, and
the decision is logged before its outcome is known. Once the outcome is in, it is graded.

{{< flow steps="Public data|Blind scoring|Reconcile|Rank and critic|My decision|Graded ledger" feedback="Lab tests and the weekly auditor|Changes to the method" >}}
Figure 1. The six steps run in order. The dashed pair sits outside them and changes the method the steps follow.
{{< /flow >}}

## Integrity

Here are five ways a system like this can fool its owner, each with checks that reduce it:

- **Look-ahead.** Decisions and hypotheses are timestamped before outcomes, and AI scores
  are judged only on outcomes that come after the score is made.
- **Leakage.** Roles run in separate sessions, and code stops the scorer seeing what I own.
- **Overfitting.** Tests use companies the system never chose and apply the Holm correction for multiple testing.
- **Cherry-picking.** Ledgers are append-only, every decision is graded once its
  outcome is in, and the system's own reports give counts before rates.
- **AI errors.** Every figure is checked against a primary filing. AI-written briefs have
  contained fabricated numbers, one overstated about 130-fold.

## How the method changes

An integrity gate runs at the start of every session, and a failure stops work. A weekly
auditor reads the files, never the conversation. Methods change only through the lab: the
hypothesis, the decision rule and the deadline are hashed before the test's data is
opened, and replication and adversarial review follow. A test that passes as
registered still has to survive replication.

## What it gives me

It has taught me to read company data with discipline: to check every figure against the
filing it came from, to write a decision down before I know how it turns out, and to ask
of any pattern whether it still holds once volatility is controlled for. It gives me a
clearer, data-based way to evaluate companies than I had before.

## What I hope for, and what I want to study next

Over the long run, I hope the loop helps me find the trends that matter, with AI sifting
more information than I could alone and every decision still mine. It has also given me
my next question for economics: how to tell skill from luck in a short record of
overlapping outcomes. That means studying inference with overlapping observations, multiple-testing control, statistical power and correction for selection.

The facts about the system come from a summary its own AI wrote from its private records,
as of 18 November 2026; the approach and the hopes are mine. AI drafted the page from
both under my direction.
