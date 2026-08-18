# MODEL HANDOFF PROMPTS

Paste the relevant block into each model when you want site content. Each one specifies
exactly what to output, what to strip, and where it goes.

**Universal rule, in all three:** the site gate (`scripts/site_publish.py`) refuses on
verdict vocabulary, scores, ranks, `position_status`, `action_hint`, `signal_grade`,
`claim_key`, `DEPLOY-OK`, and all horizon statistics. If output contains any of those,
nothing gets written and you'll have to regenerate. Strip at the source.

**Horizon statistics are held back entirely** — no `P(+10%/4w)`, no median/worst/skew, no
probability-of-move framing anywhere. Standouts is descriptive only for now.

---

## 1. EARNINGS MODEL → News

```
Produce a NEWS ITEM for my public site from today's prints.

FORMAT — plain markdown, no code fences:

**as_of:** YYYY-MM-DD

## <Company> (<TICKER>) — <what the headline number hides, in six words>

**What the headline says.** The figure everyone will quote, and where it came from.

**What the filing says.** The trap-gate result in plain English. Which check fired,
what it found. If the check ran and found nothing, SAY SO — the denominator is the
product. "This check ran on 14 names this week and fired on 2" is the content.

**Why it matters.** One paragraph. The mechanism, not the verdict.

**Provenance.** FILED / COMPANY / MARKET / ANALYST — and if the company is a foreign
private issuer filing 20-F or 6-K, say plainly that no US-GAAP filed data exists and
every figure is COMPANY tier at best.

**Falsifier.** The named KPI, the threshold, and the date it resolves.

**Gaps.** What could not be verified. Filing lag if the quarter isn't in XBRL yet.
Analyst count if coverage is thin — "+70.5% upside on 2 analysts" is not the same
object as "+54.6% on 43", and the reader needs the count.

Then a COVERAGE NOTE at the end: what was on the calendar this window, what you
covered, what you didn't, and what bias that creates.

STRIP BEFORE OUTPUT — these will cause an automatic refusal:
- The Score: line, the VERDICT: line, the ROUTE: line. All three, every time.
- CQS values, first-pass CQS, band and tier labels, grid cells.
- position_status, action_hint, signal_grade, claim_key — every internal field name.
- Any BUY / ADD / HOLD / TRIM / EXIT / NO POSITION verdict.
- Horizon statistics of any kind.

KEEP: the driver, the falsifier, the gate result, the quality change described in
words, the gaps, the provenance tier, the depth tag.

Max 4 names. If it was a heavy day, tell me and split across responses rather than
compressing — compression under load is a known failure mode.

Where no edge exists, say so. "30+ analysts covered this within minutes, this is
context not a finding" is an honest and publishable line.
```

---

## 2. PORTFOLIO MODEL → Sector

```
Produce a SECTOR READ for my public site from this week's market_pulse.py sweep.

FORMAT — plain markdown, no code fences:

**as_of:** YYYY-MM-DD   (the Saturday of the coverage week)

## The rotation

One paragraph: which factor the market paid for this week and what changed. Name it.

## What moved

The pulse groups, in prose not raw tables: what's HOT, what's ACCELERATING (outperforming
AND by more than last month — that distinction is the signal), what's COLD, what's
BREAKING DOWN, and where volume surged above 1.5x its 3-month average.

Pair every move with participation. A theme up on 0.6x volume is a weak signal and
saying so is the value.

## Where the sector contradicts itself

THIS IS THE MOST IMPORTANT SECTION. Same-sector names telling opposite stories is the
finding, not sector agreement. If two equipment names are at cycle-high margins while
a third is coming off a trough, then "semis" is not one trade — write that. A sector
label that dissolves under inspection is a better article than a sector that holds.

## What would change this read

The specific observation, with a date, that would break the rotation call.

STRIP BEFORE OUTPUT — automatic refusal triggers:
- The ranking table in any form. No BuyS, no CQS, no rank numbers, no DEPLOY-OK.
- "RANKED n of m" headers.
- Horizon statistics — P+10/4w, skew, med, worst. All held back.
- Anything from /review or any account-derived output.

NOTE ON KNOWN BREAKAGE — do not publish figures from these until fixed:
- 6-month relative strength is dead universe-wide (all 12 benchmark ETFs returned N/A).
- The MA-structure label contradicts its own columns on ~35 of 153 rows.
- Two of three trend inputs are N/A universe-wide.
If a read depends on any of those, say "not obtained" rather than using the broken value.
```

---

## 3. EVALUATION MODEL → Standouts

```
Produce a STANDOUT ENTRY for my public site. Descriptive only — no scores, no ranks,
no probabilities.

FORMAT — plain markdown, no code fences:

**as_of:** YYYY-MM-DD

## <Company> (<TICKER>) — <the finding in six words>

**Mechanism.** Why capital would move. Not that it moved — the cause.

**What the filings say.** The period-pinned GAAP table, in prose or a small markdown
table, with the period_end stated. This is the piece I most want published: the margin
series is what turns a headline multiple into a peak-quarter artefact, and no free
screener shows it.

**What the market is assuming.** The reverse-DCF framed as a testable claim — "this
price requires roughly X% growth for ten years, which sits beyond the top row of the
historical achievement table." NEVER as a price target, NEVER as a valuation verdict.

**Depth.** Which stages ran and which didn't. "Stages 0-3 and 5 computed, Stage 4 not
run — no scenario tree" is exactly right. A reader calibrating confidence needs this.

**Falsifier.** Named KPI, threshold, date.

**Gaps.** What couldn't be verified and why. Foreign filer with no us-gaap concepts.
Sparse XBRL tags. Beta unavailable on a short listing. Say which.

STRIP BEFORE OUTPUT — automatic refusal triggers:
- CQS values and the whole "45 -> 54" score-delta shape.
- Band labels, tier labels, grid cells, QUALITY-BUY, Track letters.
- The BUY / ADD / HOLD / TRIM / EXIT / NO POSITION verdict vocabulary.
- position_status, claim_key, action_hint, signal_grade.
- Horizon statistics — held back entirely.

TWO STANDING CAUTIONS:
1. Do not publish anything drawn from a naive RATINGS.md leaderboard. The ledger is
   mixed-vintage — legacy v2 scores sit beside v3.2 values and they are not the same
   measurement. Until that's resolved, no cross-name comparison of scores.
2. 59 ACTIVE names carry a score with no full evaluation behind them. If a name you're
   writing up is one of them, the depth tag must say so.

PREFER these subjects, in order — they're the differentiated ones:
- A trap: peak-quarter, below-the-operating-line, adjusted-vs-GAAP, SBC exceeding
  operating margin.
- A stale rejection: a name screened out for a reason that stopped being true.
- A one-link finding: two names that look like diversification and are one bet.
- A coverage gap: a name that structurally cannot be scored from filings, and why.
```

---

## Running the gate

```powershell
cd C:\Users\jacob\dev\jacobbuildmodel.github.io
python scripts\site_publish.py "<staged file>" --section news
python scripts\site_publish.py "<staged file>" --section sector
python scripts\site_publish.py "<staged file>" --section standouts
python scripts\site_publish.py "<staged file>" --section briefs
```

Refusal means nothing was written. Fix the source, not the output.
Everything stages as `draft: true` — a human clears that, never the script.
