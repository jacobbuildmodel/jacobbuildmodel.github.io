---
title: "DRIVE: how I research listed companies with AI"
description: "A private system I built with AI to study listed companies: my role, the loop it runs, the checks on it, and what I want to study next."
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
---

My approach to markets rests on three ideas: trend, growth and fundamentals. DRIVE is the
system I built with AI to study listed companies in that light, with data instead of gut
feel. I set its goals and rules, and every decision is mine.

DRIVE is private. Its code and records are not published, so a reader cannot check what
this page says. It is personal research, not advice to anyone.

## My role

I set the goals, write the rules in plain English, rule on disputes and make every
decision; the system has no brokerage access. AI writes all the code, drafts formulas and
tests, and runs them.

Three times I overruled the AI:

- **23 September 2026.** A valuation table the AI wrote was more generous than the study
  it cited, up to 20-fold in one cell, and 95 score cards had used it. Offered a blend of
  the two, I chose the source.
- **14 October 2026.** Hand-off notes told the scorer what I owned and that its earlier
  verdict had been overruled. I ruled that it receives only evidence and a question.
- **15 October 2026.** Of the 9 tests registered in the lab, 7 had no date for a verdict.
  I required a goal, an expected result, a decision and a deadline before any data; the
  code now refuses a test without them.

## How it works

DRIVE runs as a loop. AI assistants, each with one job, collect public data, score each
company from its filed accounts, and argue against every candidate. I make the decision,
and it is logged before the outcome is known. Four weeks later it is graded, and what the
grading shows feeds back into the rules, but only through a test written down before any
data is seen.

{{< flow steps="Public data|Blind scoring|Reconcile|Rank and critic|My decision|Graded ledger" feedback="Lab tests and the weekly auditor|Changes to the method" >}}
Figure 1. The six boxes run for every decision. The dashed pair is not a seventh step: it changes the rules the six follow.
{{< /flow >}}

## Integrity

Five ways a system like this can fool its owner, and the check on each:

- **Look-ahead.** Calls and hypotheses are timestamped before outcomes, and AI scores are
  validated forward only.
- **Leakage.** Roles run in separate sessions, and code stops the scorer seeing what I own.
- **Overfitting.** Tests use companies the system never chose, split samples, a random
  control and a correction for testing many ideas at once (the Holm correction).
- **Cherry-picking.** Ledgers are append-only, every call is graded, and counts are given
  before rates.
- **AI errors.** Every figure is checked against a primary filing. AI-written briefs have
  contained fabricated numbers, one overstated about 130-fold.

## How it improves

An integrity gate runs at the start of every session, and a failure stops work. A weekly
auditor reads the files, never the conversation. Methods change only through the lab: the
hypothesis, the decision rule and the deadline are hashed before any data, and blind
replication and adversarial review follow. One test passed as registered and was thrown
out when replication disagreed.

## What it gives me

It has taught me to read company data with discipline: to check every figure against the
filing it came from, to write a call down before I know how it turns out, and to ask
whether a pattern survives once risk is taken into account. It gives me a clearer,
data-based way to evaluate companies than I had before.

## What I hope for, and what I want to study next

Over the long run, I hope the loop helps me find the trends that matter, with AI sifting
more information than I could alone and every decision still mine. It has also given me
my next question for economics: how to tell skill from luck in a short record. That means
studying inference with overlapping observations, testing many ideas at once, and
statistical power.

The facts on this page come from a summary of the system's own logs (private), as of 18
November 2026. AI drafted the page from that summary under my direction.
