# PURPOSE: is this worth our effort? (v1, 15 October 2026)

Written by the moderator at Jacob's request (15 Oct): "an inner right and wrong principle ... a
logical model where you think should we push it, should we spend effort on this", checked by a
dedicated, experienced reviewer and enforced in code. v0.1 was tested against how funders, journals
and policy units decide (office/research/PURPOSE_GATE_EVIDENCE.md, 50 sources; source numbers [Sn]
below refer to that file). Rulings and examples live in reviews/purpose/, never here, so a reviewer
reading this file is not anchored by earlier verdicts.

## 1. The core rule: research is worth doing only if its answer could change a decision
Value = what is at stake x the chance the answer changes what someone does, compared with the cost
of finding out. A perfect answer that changes nothing is worth nothing [S1, S3, S5]. Every body that
judges research before results asks this first (NICE, NIH, ERC, UKRI) [S3, S6, S16, S19, S23].
Curiosity is where questions come from. It does not get the site's resources. Good method is
necessary, never sufficient.

## 2. Six gates, in this order (all before a brief; G3 again before the seal)
G0. **Answerable.** Can public data and a sound method answer it at all? Data feasibility (labels and
    coverage only, no values) is checked here, before any cost is weighed [S10, S29].
G1. **Decision.** Name the person or body, the decision, and what they would do under each result
    ("yes", "no", "unclear"). Rate the stakes High/Medium/Low [S6]. If even a perfect answer leaves
    every action unchanged, STOP here [S3].
G2. **Attention.** Pass if EITHER (a) a live argument exists, with a dated source from the last 12
    months (Hansard, letters, forums, surveys), OR (b) the likely result is a credible surprise that
    contradicts a named belief [S34]. Plus timing: a decision date or a news peg, because evidence is
    used when it arrives at the moment of decision [S23, S25].
G3. **Both results are news.** Before the seal, write the headline for each likely result and give
    each cell a probability (the reviewer's, then two cold readers'):
    | | Data says yes | Data says no |
    |---|---|---|
    | People believe it | confirms a contested belief | myth-busting (highest value) |
    | Nobody suspects it | a hidden link (high value) | no news (zero) |
    If more than half the probability sits in the zero cell, the piece cannot be a reader article.
    Also name the smallest effect that would matter, so "no" means "smaller than X", a precise
    finding [S46]; and an outcome-neutral check the data must pass (a positive control, a coverage
    test), so a weak test is never read as "no link" [S10, S47].
G4. **Who it serves.** The public (a reader's decision) and/or a ministry: a named unit, decision,
    date and channel, and the message that would be sent on release day [S26, S29-S32]. A "no" result
    serves a ministry when a current policy rests on the belief [S28]. Jacob's own benefit (SMU,
    markets) is a tie-breaker only: interest inflates estimates once effort is spent [S42].
G5. **Opportunity cost.** Must-meet: a named slot in the calendar and what it displaces. Should-meet:
    it beats the best alternative on the question menu and the weakest live piece [S43]. Kill
    criteria with dates are set here (for example a minimum tap rate in the reader round, a minimum
    coverage) and checked at each later gate [S41].

## 3. Words never rescue a question
The gates judge the QUESTION, not the title. A new hook that borrows attention from another debate is
not a new question. If a reader says "so what", the next step is a purpose review, never new words.
Results-stage changes cannot alter the registered question [S10].

## 4. Independence, stop rules, teeth
- The chat that builds a piece never grades its own purpose, just as it never checks its own
  numbers. The Purpose Reviewer (.claude/agents/purpose-reviewer.md) runs the gates, writes both
  headlines itself, runs a pre-mortem ("it is six months later and this piece failed: why?") [S38],
  and argues against its own verdict.
- Verdicts: GO (reader article), PAPER TRACK, REDESIGN (say exactly how), STOP.
- When it runs: (1) at Checkpoint 0, before any brief; (2) before the seal (G3 with real readers);
  (3) after ANY reader round that ends in "so what" or no taps; (4) monthly, over the portfolio.
- A STOP or PAPER TRACK can only be overruled by Jacob, in writing, naming the decision the result
  would change. Work already done is never a reason [S40, S42].
- Stopping is a good decision, logged as one. The monthly review reports how many pieces the gate
  stopped or redirected; zero over a quarter is a warning that the gate has no teeth [S41, S43].
- Enforced in code: checker_tools/purpose_gate.py (reviews, the portfolio, BLOCK on any breach), the
  checkpoint and checker routines, and the research-repo CI seal guard.
- Sealed results are always reported on the scorecard, in the same format, whatever the track.

## 5. Tracks
- **Reader article:** passes G0-G5.
- **Paper or note:** valuable to economists or evaluators (method, replication) but fails G2 or G3
  for the public. Written like a Registered Report: the seal is stage 1, the scorecard entry and a
  short note are stage 2 [S10, S14]. A full working paper only if it passes G5 on its own.
- **Stop:** fails G0 or G1 for everyone. Any sealed results are still reported.
