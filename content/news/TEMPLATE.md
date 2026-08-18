---
# ── COPY THIS FILE for each news item. Rename to YYYY-MM-DD.md ──
# (Ordinarily produced by site_publish.py --section news from staged earnings-
#  model output — see MODEL_HANDOFF_PROMPTS.md. This template is for a manual
#  item, or for fixing a staged draft by hand.)
#
# One item can cover up to 4 companies in one file — that's the earnings
# model's actual batch cap. If a day is heavy (10+ names reporting), that's
# multiple files, not one compressed file. Compression under load is a
# documented failure mode of the source model — don't reintroduce it here.
title: "News — 00 Month 2026"
date: 2026-01-01
draft: true
showToc: true
TocOpen: false
summary: "One line: the sharpest thing a headline number hid today."
tags: ["news"]
---

**as_of:** YYYY-MM-DD

> **TODO — the hook.** One sentence, plain English, no jargon. What's the single most
> interesting gap between what a headline said and what a filing said today?

## [Company] (TICKER) — [what the headline number hides, six words or fewer]

**What the headline says.** The figure everyone will quote this print, and where it's from.

**What the filing says.** The trap-gate result in plain English — which check fired, what it
found. If the check ran and found nothing, say so plainly: "this check ran on N names this
week and fired on M" is itself the content, not a null result to skip past.

**Why it matters.** One paragraph. The mechanism, not a verdict.

**Provenance.** FILED / COMPANY / MARKET / ANALYST. If this is a foreign private issuer
filing 20-F or 6-K, say so explicitly — no US-GAAP filed data exists, and every figure here
is COMPANY tier at best, never FILED.

**Falsifier.** The named KPI, the threshold, and the date it resolves.

**Gaps.** What couldn't be verified. Filing lag if the quarter isn't in XBRL yet. Analyst
count if coverage is thin — a number's context changes completely between 2 analysts and 40,
and the reader needs the count stated, not just the figure.

<!-- Repeat the ## heading block above for each additional company, up to 4 total. -->

## Coverage note

What was on the earnings calendar this window, what got covered here, what didn't, and what
bias that selection creates. This is a mandatory closing paragraph, not optional colour —
undisclosed sampling bias is the default failure mode of daily market writing, and stating it
plainly is the correction.

---

<!--
PRE-PUBLISH CHECKLIST — delete this block before publishing.

  [ ] No Score:, VERDICT:, or ROUTE: line anywhere — all three cause an automatic refusal
  [ ] No CQS, band, tier, or grid-cell language
  [ ] No position_status, action_hint, signal_grade, or claim_key field names
  [ ] No horizon statistics of any kind (held back sitewide, not just here)
  [ ] Every trap-gate result states its denominator (ran N times, fired M times)
  [ ] Foreign filers are explicitly marked COMPANY-tier, not FILED
  [ ] Thin analyst coverage states the actual count
  [ ] Coverage note is present and honest about what was skipped
  [ ] Max 4 companies in this file — if the day was heavier, this is one of several files
  [ ] Hook written for a human, not a machine
  [ ] Filename is YYYY-MM-DD.md, date in front matter is correct, draft: false
-->
