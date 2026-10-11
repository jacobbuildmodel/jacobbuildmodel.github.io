---
title: "The Singapore dollar, the yen and the ringgit: method and derivation"
date: 2026-11-14
draft: false
url: "/researchers/singapore-dollar/"
---

The companion to the article
[Tokyo got cheaper. The yen did most of the work](/economics/2026-11-14/).
It sets out how each result was derived, every test as sealed, and every
sealed sensitivity. Every number below is in `sgd/number_manifest.csv` with
the script that wrote it, and `14_manifest.py --check` verifies each one.

## 1. The question as sealed

The thesis was sealed on 3 October 2026 in commit
[9e46034](https://github.com/jacobbuildmodel/coe-analysis/blob/9e460349ebfc56bf313728e14243876e9dd6c9f4/sgd/THESIS.md),
before any exchange-rate, GDP or CPI value was read. THESIS section 1,
verbatim:

> **Sealed question 1 (window from section 5).** "From January
> 2021 to December 2025, how much of the Singapore dollar's rise against the
> yen and the ringgit came from the Singapore dollar rising against everyone,
> and how much from those currencies falling against everyone?"
>
> **Sealed question 2.** "Did the Singapore dollar's broad path
> follow MAS's announced policy decisions more closely than Singapore's
> growth?"

The verdict rule, THESIS section 8, verbatim in its two parts. Part A, for
each of the yen and the ringgit, X, exactly one of:

> - **"the Singapore dollar did not rise against the X"**: `b_X <= 0` over the
>   scored window.
> - **"the record cannot split the Singapore dollar's rise against the X"**:
>   T1 fails for X on the scored window.
> - **"most of the Singapore dollar's rise against the X was the X falling
>   against everyone"**: T2 (yen) or T3 (ringgit) survives.
> - **"most of the Singapore dollar's rise against the X was the Singapore
>   dollar rising against everyone"**: T2 or T3 fails.
> - **"neither side accounts for most of the Singapore dollar's rise against
>   the X"**: T2 or T3 is INCONCLUSIVE.

Part B, exactly one of:

> - **"the record cannot say whether the broad path followed MAS or
>   growth"**: gate C fails. The BIS index does not stand in for MAS's own.
> - **"the broad path followed MAS's decisions more closely than growth"**: T7
>   survives. The weak-evidence sentence of T7 is printed beside it.
> - **"the broad path followed growth at least as closely as MAS's
>   decisions"**: T7 fails.
> - **"the broad path followed MAS's decisions a little more closely than
>   growth, by less than the line"**: T7 is INCONCLUSIVE.

The verdict that the rule produced: most of the Singapore dollar's rise
against the yen was the yen falling against everyone; most of its rise
against the ringgit was the Singapore dollar rising against everyone; the
broad path followed MAS's decisions more closely than growth.

## 2. The derivation

**The identity.** Let `x_k` be the log of units of currency k per US dollar
(BIS WS_XRU, monthly averages), and let `w_Ak` be the weight of currency k
in the BIS broad basket of area A. Each basket's weights sum to 1 and leave
out the area's own currency. For a change `d` over a window:

```
b_X = d(x_X - x_SGD)                       SGD rises against X if b_X > 0
s   = sum over k of w_SG,k * dx_k - dx_SGD  the SGD broad index (BIS M.N.B.SG)
n_X = sum over k of w_X,k  * dx_k - dx_X    X's broad index (BIS M.N.B.<AREA>)

e_X = b_X - s + n_X
    = sum over k of (w_X,k - w_SG,k) * dx_k
```

So `b_X = s - n_X + e_X` holds by definition, and dividing by `b_X` (the
premise of each share test is `b_X > 0`):

```
S_X = s / b_X       the Singapore dollar rising against everyone
P_X = -n_X / b_X    X falling against everyone
R_X = e_X / b_X     neither broad index
S_X + P_X + R_X = 1
```

The shares add to 1 because they are the three terms of one identity over
one denominator. Either share can exceed 1 or fall below 0 when the other
moves the opposite way, as the ringgit's did.

**What `e_X` contains.** The second line of `e_X` shows that it is the
difference between the two baskets, applied to every currency's move. It
would be zero if both indices used one basket. They do not:

- the Singapore dollar's basket holds the yen and not the Singapore dollar,
  and Japan's holds the Singapore dollar and not the yen;
- the weights differ, and BIS updates them for each three-year period and
  chain-links the index, so the fixed-weight algebra above holds only
  approximately over a window;
- averaging: `b_X` is the ratio of two monthly-average US dollar rates,
  which need not equal the cross rate built into each index.

Since the weight differences sum to zero, `e_X` does not depend on the
choice of the US dollar as the numeraire. T1 bounds it: `|R_X| <= 0.20` on
both windows for both currencies.

**Endpoints.** Each change is the mean of the log over three months at the
end minus the mean over three months at the start: January to March 2021 and
October to December 2025 for the scored window, August to October 2005 and
the last three full months for the long window. THESIS section 5 fixed this
before the data was opened, to damp a single month's noise. The single-month
endpoints are a sealed sensitivity (section 5 below), and they matter for
the ringgit.

**Whose index moved, not why.** The split is an accounting identity, not a
model. `s` and `n_X` record that each index moved; they do not say what moved
it. A shock that moves the US dollar, oil, or risk appetite lands in both
indices at once, and the identity assigns it to whichever index it shows up
in. So "the yen falling against everyone" means the yen's broad index fell,
not that something Japanese caused the fall.

## 3. Policy or growth (T7)

**The policy score.** All 62 statements linked from MAS's Past Monetary
Policy Decisions page, 22 February 2001 to 27 July 2026, were coded by a
rule written before any statement was read (THESIS section 5), into
[office/MPS_CODING.csv](https://github.com/jacobbuildmodel/coe-analysis/blob/main/sgd/office/MPS_CODING.csv).
Only the decision paragraph was read, found mechanically by a decision
phrase ("MAS will", "MAS has decided" and the like) and a band word ("slope",
"policy band", "re-centre"); paragraphs that describe the S$NEER's or the
economy's movement were excluded mechanically. Each row records the quoted
words behind each code, and MAS's own Slope, Width and Level cells from the
decisions page as a cross-check.

- **Slope:** zero, negative, steeper, flatter or same.
- **Centre:** up, down or unchanged.
- **Width:** recorded, not scored.
- **The eight rows ruled by the Level cell.** Six statements re-centred "at
  the prevailing level" with no direction word, and two read "up to its
  prevailing level", which the rule coded AMBIGUOUS. Before the seal the
  checker ruled that their direction comes from the Level cell on MAS's
  decisions page, MAS's own record of the decision. Both codes are kept in
  the sheet (`centre_statement`, `centre_source`).

```
slope in force after decision i:  0 after zero, -1 after negative,
                                   1 after steeper or flatter,
                                   carried forward after same
re-centring:                       +1 up, -1 down, 0 unchanged
p_i = slope in force + re-centring, from -2 to 2
```

**Intervals.** Interval i runs from the month before decision i to the month
before decision i+1; the last runs to the last full month in the BIS data.

```
y_i = 12 * (ln NEER_SG[end] - ln NEER_SG[start]) / months
g_i = mean year-on-year real GDP growth over the quarters whose last month
      falls in (start, end]; if none, the quarter of decision i
```

Of the 62 intervals, the one after the July 2026 decision was dropped
because its quarter was not yet published, leaving 61.

**The statistic.** Spearman rank correlations with ties at average rank:

```
rho_p = spearman(y, p)
rho_g = spearman(y, g)
D     = rho_p - rho_g
Survive if D >= 0.20 and rho_p > 0;  Fail if D <= 0
```

The line of 0.20, as sealed: "With about 60 intervals, the standard error of
one Spearman coefficient is about 1/sqrt(59), roughly 0.13. A lead of 0.20 is
one and a half of those."

**The bootstrap range.** Intervals were resampled with replacement, 10,000
draws, with Python's `random.Random` seeded at 20260929; D was recomputed on
each draw, and the range is the pair of percentiles that bound the central
90 per cent of the draws, with linear interpolation. It is reported and is not part of the rule.

**Result.** rho_p 0.4653, rho_g 0.1127, D 0.3526, with a 90 per cent
bootstrap range of 0.1117 to 0.5867, on 61 intervals.

## 4. Every test

Gate C, a gate and not a scored test, compared monthly log changes of the BIS
index with MAS's weekly S$NEER, averaged by month: the correlation was 0.9240
on 331 changes, against a line of 0.90 on at least 120, so T4 and T7 were
read.

| Test | Survive if (sealed) | Fail if (sealed) | Numbers | Outcome | Confidence |
|---|---|---|---|---|---|
| T1 the split closes | \|R_X\| <= 0.20 and the mean absolute difference (b) <= 0.005, for both JPY and MYR, on both windows. | \|R_X\| > 0.20 or the mean absolute difference (b) > 0.005, for either currency on either window. | R: yen -0.0392, ringgit 0.1672 (scored); yen -0.0782, ringgit -0.0663 (long). BIS against MAS: 0.0003 to 0.0007 | SURVIVE | 55% |
| T2 the yen | P_JPY >= 0.50 and P_JPY > S_JPY. | S_JPY >= P_JPY. | b 0.4018, s 0.1234, n -0.2942, e -0.0157; S 0.3070, P 0.7321, R -0.0392 | SURVIVE | 90% |
| T3 the ringgit | P_MYR >= 0.50 and P_MYR > S_MYR. | S_MYR >= P_MYR. | b 0.0486, s 0.1234, n 0.0829, e 0.0081; S 2.5386, P -1.7058, R 0.1672 | FAIL | 8% |
| T4 the slow path | SGD's rank <= 2. | SGD's rank >= 6 (steadier than at most five of the ten partners). | SD of monthly log change: SG 0.0047, rank 1 of 11; HK 0.0100; JP 0.0216, the least steady | SURVIVE | 80% |
| T7 policy or growth | D >= 0.20 and rho_p > 0. | D <= 0 (growth lines up at least as well). | rho_p 0.4653, rho_g 0.1127, D 0.3526 (0.1117 to 0.5867), 61 intervals | SURVIVE | 35% |

The confidences are Jacob's, set alone before the data was opened. Held: 4
of 5, against an expected 2.680, the sum of the confidences. The Brier score
was 0.136:

```
Brier = (1/N) * sum over tests k of (c_k - o_k)^2
c_k = the confidence at seal, o_k = 1 if test k held and 0 if it failed,
N = the number of tests scored
```

A forecaster who always says 50 per cent scores 0.25.

## 5. Robustness: every sealed sensitivity

None of these is scored. "Holds" means the reading matches the scored one;
"flips" means the sealed rule, applied to the variant, would have given a
different outcome.

| Variant (sealed) | Numbers | Reading |
|---|---|---|
| T7, growth lagged one quarter | rho_g 0.1924, D 0.2729 | holds |
| T7, CPI inflation in place of growth | rho_g 0.5074, D -0.0421 | **flips**: inflation lined up at least as well as MAS's decisions |
| T7, finer slope coding | rho_p 0.4587, D 0.3460 | holds |
| T7, intervals from 2010 only | 41 intervals; rho_p 0.5490, rho_g 0.0335, D 0.5155 | holds |
| Yen, long window | S 0.5724, P 0.5058, R -0.0782 | **flips**: the Singapore dollar's own rise was the larger part |
| Yen, single-month endpoints, scored | S 0.2921, P 0.7537, R -0.0459 | holds |
| Yen, end-of-period rates, scored | S 0.3066, P 0.7311, R -0.0377 | holds |
| Yen, single-month and end-of-period, long | P 0.5122 and 0.5089, against S 0.5688 and 0.5758 | the long-window flip holds |
| Ringgit, long window | S 1.0394, P 0.0269, R -0.0663 | holds (the Singapore dollar's rise) |
| Ringgit, single-month endpoints, scored | S 3.1752, P -2.3901, R 0.2149 | split holds; **T1 flips**: R over 0.20 |
| Ringgit, end-of-period rates, scored | S 3.0098, P -2.0224, R 0.0126 | holds |
| Real indices, scored, yen and ringgit | yen P 0.7680, R -0.1098; ringgit R -1.0416 | context only: the residual absorbs inflation differentials |
| Sensitivity B, monthly covariance shares | partner's own move larger for 10 of 10 partners, both windows | holds |
| World view, long window | Hong Kong SD over US SD 0.7798, correlation 0.9248; yen rank 11 of 11 | as the extremes predicted |

The real-index rows set BIS real broad indices against the nominal cross,
since BIS publishes no real bilateral rate, so their residual carries the
inflation differentials (THESIS_ADDENDUM item 3). Two flips matter. With
inflation in place of growth, D is negative, so the T7 result cannot separate
MAS's decisions from inflation, which MAS's framework targets. And the yen
split is a statement about the scored window: over the long window, the
Singapore dollar's own rise was the larger part.

## 6. What the design cannot say

- **T7 leans toward the rival, sealed:** "The band is the path MAS keeps the
  index on, so a score that describes the band will match the index's path
  wherever MAS held the index inside it. A result that the path followed
  MAS's decisions is weak evidence that MAS rather than the economy moved
  the Singapore dollar."
- **T7 leans the other way too, sealed:** "`p_i` takes few values with many
  ties, which lowers `rho_p`. And MAS set its slope partly on the growth
  outlook, so the two predictors share a cause."
- **The bootstrap treats intervals as independent.** Consecutive intervals
  share MAS cycles and growth spells, so the range likely understates the
  uncertainty in D.
- **The ringgit basket overlap.** Malaysia and Singapore weigh heavily in
  each other's baskets, so part of each currency's move shows up in the
  other's index. THESIS sealed either T3 result as weaker evidence than the
  yen's, and the single-month residual above shows how close the ringgit's
  split ran to T1's line.
- **Growth vintage.** The current published GDP series was used, not the
  advance estimate MAS saw on the day. THESIS states as an assumption, not a
  finding, that revisions are small next to growth's swings between
  quarters.
- **The band position.** MAS does not publish the band's slope, width or
  centre, so no test asks where the rate sat inside the band, or whether MAS
  intervened at its edges.
- **Prices.** The split is nominal; it says nothing about Japanese or
  Malaysian prices.

## 7. Data provenance

All files were retrieved on 3 October 2026, byte for byte as served; the
URLs and the coverage report are in
[raw/RETRIEVED.txt](https://github.com/jacobbuildmodel/coe-analysis/blob/main/sgd/raw/RETRIEVED.txt).

| Source | Series | File | md5 | Terms |
|---|---|---|---|---|
| BIS effective exchange rates, broad, nominal | WS_EER, M.N.B.<AREA>, eleven areas | `s1_bis_eer_neer_broad_monthly.csv` | e3467448791abd778b12b06b482bca79 | [BIS terms](https://www.bis.org/terms_conditions.htm) |
| BIS effective exchange rates, broad, real | WS_EER, M.R.B.<AREA> | `s1b_bis_eer_reer_broad_monthly.csv` | d4c2f2770353fbda55f2493c43b58272 | [BIS terms](https://www.bis.org/terms_conditions.htm) |
| BIS US dollar rates, monthly average | WS_XRU, M.<AREA>.<CUR>.A | `s2_bis_xru_usd_monthly_avg.csv` | 1f740cf8c1d3832c5c9e13307cd0e4de | [BIS terms](https://www.bis.org/terms_conditions.htm) |
| BIS US dollar rates, end of period | WS_XRU, M.<AREA>.<CUR>.E | `s2e_bis_xru_usd_monthly_eop.csv` | 3c3d432a19aa8f842b92bd83c431b640 | [BIS terms](https://www.bis.org/terms_conditions.htm) |
| MAS exchange rates, monthly average (SingStat) | M700051: Japanese Yen, Malaysian Ringgit | `s3a_mas_fx_monthly_avg_M700051.json` | 014858ba90ce5df154681ceaaaa3969e | [SingStat terms](https://www.singstat.gov.sg/terms-of-use) |
| MAS S$NEER, weekly | MAS chart feed | `s4_mas_sneer_weekly.json` | 54966f6d59e0e40d5fb561fedcab21a5 | [MAS terms](https://www.mas.gov.sg/terms-of-use) |
| MAS Past Monetary Policy Decisions and the 62 statements | decisions page; `s5b_*.html` | `s5a_mas_past_mp_decisions.html` | 355bb0d7cbc7a61ea69532f66fe0ee63 | [MAS terms](https://www.mas.gov.sg/terms-of-use) |
| SingStat GDP, year-on-year, quarterly | M015631: GDP In Chained (2015) Dollars | `s6a_singstat_gdp_yoy_quarterly_M015631.json` | 4d4971b4cfa3e78912274b873bf98239 | [SingStat terms](https://www.singstat.gov.sg/terms-of-use) |
| SingStat CPI, monthly | M213751: All Items | `s7a_singstat_cpi_monthly_M213751.json` | a6ef0f94ae00a08f8f789add4cbe58c9 | [SingStat terms](https://www.singstat.gov.sg/terms-of-use) |

The md5 of each statement file is in RETRIEVED.txt. The coding sheet's md5
is fixed in the seal manifest, and every input and output's md5 is in
`sgd/CHECKSUMS.md5`.

## 8. Rerun it

```
git clone https://github.com/jacobbuildmodel/coe-analysis.git
cd coe-analysis
python3 -m pip install -r sgd/requirements.txt
python3 -m playwright install chromium   # only for the chart overflow check
bash sgd/run_all.sh
```

The run took about a minute on a four-core machine. It runs the synthetic
test suite (invented data, every outcome branch), then every analysis step on
the real files, the chart overflow check, and `14_manifest.py --check`, which
verifies every md5 and every number in the manifest, the article and this
page. It exits non-zero on any mismatch. The versions used are pinned in
`sgd/requirements.txt`.

`15_reproduce.py` re-derives every scored number and outcome by a second
route: it reads `raw/` and the coding sheet with pandas, does the arithmetic
in numpy and the rank correlations with `scipy.stats.spearmanr`, and imports
nothing from steps 10 and 11. It compares with `out/tests.csv` and fails on
any difference above one part in a million. The bootstrap range is not
reproduced, since it is not scored.

## 9. Process

Jacob chose the question and set every confidence alone, before the data was
opened. AI models wrote the code, the coding of the statements under the
sealed rule, and the drafts. An independent checker recomputed every scored
number with its own code from a fresh clone. Every change after the seal is
listed, dated and with md5s, in
[THESIS_ADDENDUM.md](https://github.com/jacobbuildmodel/coe-analysis/blob/main/sgd/THESIS_ADDENDUM.md);
none changed a rule, a threshold, a window, the coding or a score.

## 10. After outside review (not sealed)

Added on 10 October 2026, after reading by four outside readers: a lecturer,
an economics faculty member, a reader with no economics training, and a reader
who works in currency markets. The first two confirmed the arithmetic and
asked for the meaning to be tightened. The other two also confirmed it: 78,125
and 120,482 yen per S$1,000 at the two-decimal rates; 31 + 73 - 4 = 100; 2.68;
0.136. Everything in this section was **added after
outside review, not sealed**, and none of it is scored. No sealed number,
outcome, threshold or verdict wording changed. The script is
`sgd/16_review.py`: it reuses the sealed definitions in `11_tests.py`
(the same three-month endpoint means) and writes `out/review_*.csv`. Every
number below is in the number manifest. The change log is THESIS_ADDENDUM
item 10.

**The ringgit's shares, explained.** The article no longer prints them. Over
the scored window, `b_MYR` was small (0.0486) while both broad indices rose,
so `S_MYR` = 2.5386 and `P_MYR` = -1.7058. In per cent, the Singapore
dollar's own rise was 254 per cent of the move, and the ringgit's own rise
took back 171 per cent. A share above 1, or below 0, is what a small
denominator and two indices moving the same way produce. It is not an error.

### A1. The US dollar as the reference currency

```
b_X = d ln(X per USD) - d ln(SGD per USD)          exact, no remainder
1   = [-d ln(SGD per USD)] / b_X + [d ln(X per USD)] / b_X
       the Singapore dollar's own    X's own fall against
       move against the US dollar     the US dollar
```

| Window | Currency | SGD against USD | X against USD | SGD's share | X's share |
|---|---|---|---|---|---|
| 2021-25 | yen | up 2.7% | down 31.3% | 0.0670 | 0.9330 |
| 2021-25 | ringgit | up 2.7% | down 2.1% | 0.5543 | 0.4457 |
| Aug 2005 on | yen | up 30.6% | down 30.2% | 0.4263 | 0.5737 |
| Aug 2005 on | ringgit | up 30.6% | down 7.5% | 0.7741 | 0.2259 |

The checker's rough figures for 2021-25 were confirmed: the Singapore dollar
rose 2.7% and the yen fell 31.3% against the US dollar (shares 7 and 93 per
cent), and the ringgit fell 2.1% (55 and 45). The identity is exact, but its
reference is a single currency, whose own swings sit inside both shares. On
the long window the choice of reference decides the reading. Against
everyone, the Singapore dollar's own rise was the larger part (0.5724 against
0.5058, with a remainder of -0.0782).
Against the US dollar, the yen's fall was (0.5737 against 0.4263).

### A2. Each currency removed from the other's basket

```
s    = w_SG,X * b + (1 - w_SG,X) * s_ex    =>  s_ex = (s - w_SG,X * b) / (1 - w_SG,X)
n_X  = w_X,SG * (-b) + (1 - w_X,SG) * n_ex =>  n_ex = (n_X + w_X,SG * b) / (1 - w_X,SG)
S_ex = s_ex / b,  P_ex = -n_ex / b,  R_ex = 1 - S_ex - P_ex
```

Here `w_SG,X` is X's weight in Singapore's basket and `w_X,SG` is the
Singapore dollar's weight in X's basket. The weights come from `raw/s1c`.
Each month of the window takes the sheet whose three-year period holds its
year, years after 2022 take the 2020-22 sheet, and the result is averaged over
the window. X's index moves by -b against the Singapore dollar, hence the
plus sign in `n_ex`. The BIS indices are chain-linked geometric averages with
time-varying weights, so this is a first-order approximation.

| Window | Currency | X in SG's basket | SGD in X's basket | S_ex | P_ex | R_ex |
|---|---|---|---|---|---|---|
| 2021-25 | yen | 6.1% | 2.7% | 0.2620 | 0.7246 | 0.0133 |
| 2021-25 | ringgit | 13.1% | 12.6% | 2.7703 | -2.0960 | 0.3257 |
| Aug 2005 on | yen | 8.4% | 2.7% | 0.5332 | 0.4924 | -0.0256 |
| Aug 2005 on | ringgit | 9.3% | 10.5% | 1.0435 | -0.0868 | 0.0434 |

The yen's split barely moved. For the ringgit on the scored window, the
remainder rose to 0.3257, above T1's sealed line of 0.20. Without the
overlap, the ringgit's split is less well determined. That is the overlap
THESIS sealed as weak evidence.

### A3. The real split of the yen cross

```
b_real = b + d ln CPI_SG - d ln CPI_JP
e_real = b_real - s_real + n_real    (s_real, n_real: BIS real broad indices)
```

Singapore's CPI is S7 (SingStat, All Items). Japan's is the BIS long series
on consumer prices, M.JP.628. It was retrieved on 10 October 2026 and is
recorded in RETRIEVED.txt.

| 2021-25 | Value |
|---|---|
| Singapore's CPI | up 17.1% |
| Japan's CPI | up 13.1% |
| Real yen per SGD | 0.4367 (up 54.8%) |
| SGD real broad index | up 14.7% |
| Yen real broad index | down 26.6% |
| S, P, R (real cross) | 0.3146, 0.7067, -0.0212 |
| Tokyo goods per SGD, b - d ln CPI_JP (round 5) | up 32.1% |
| Sealed "real indices" row (nominal cross) | 0.3419, 0.7680, -0.1098 |

The traveller's figure and the real exchange rate sit on opposite sides of the
nominal 49.5%: deflating by Japan's prices alone gives 32.1% more Tokyo
goods per Singapore dollar, while the real exchange rate, deflated by both
countries' prices, rose 54.8%, because Singapore's prices rose faster (17.1%
against 13.1%). On a real cross the remainder shrank from -0.1098 to -0.0212, as expected
once both countries' prices are on both sides. The yen's real fall was still
most of the real rise. The long window was not computed: Japan's series ends
in July 2026, before the long window's last endpoint month.

### A4. Every five-year window

Each window covers 60 months. The first starts in August 2005 and the next
every three months after, through the last full month. Each end is a
three-month mean. Chart 4 plots S and P for the yen.

| Windows | SGD rose against the yen | Did not | Yen's fall larger | SGD's rise larger |
|---|---|---|---|---|
| 65 | 46 | 19 | 39 | 7 |

The checker's quick count, one window fewer, matches these counts without
the last window, which ends in August 2026. The windows overlap: consecutive
ones share 57 of 60 months, so the 46 are not independent results. They
describe one persistent pattern, and, as with the serial dependence in A5(c),
the effective number of independent observations is far smaller than the
count. The Singapore dollar did not rise against the yen in the
windows starting from 2005 to 2008 and from 2014 to 2016. Its own rise was
larger only in windows starting in 2008, 2009, 2013 and 2014. Over the full
long window the order reverses (S 0.5724, P 0.5058). The Singapore dollar's broad index
rose in every window, while the yen's rose in some and fell in others, so the
yen's falls and recoveries partly offset over two decades.

### A5. T7, reconsidered

**(a) A moving-block bootstrap for D.** Blocks of consecutive intervals are
drawn with replacement, 10,000 draws, seed 20260929, and the range bounds the
central 90 per cent of the draws.

| Resampling | 90% range for D |
|---|---|
| Sealed, ordinary (intervals independent) | 0.1117 to 0.5867 |
| Block of 2 | 0.10 to 0.63 |
| Block of 4 (main) | 0.09 to 0.69 |
| Block of 8 | 0.14 to 0.71 |

Allowing for serial dependence widened the range but kept it above zero. The
sealed rule reads the point estimate, D 0.3526, not the range.

**(b) Leads.** MAS decides on forecasts, so growth and CPI inflation are
taken from the stretch shifted 1 or 2 quarters later. Each interval keeps its
length.

| Predictor | rho | rho_p on the same intervals | D | Intervals |
|---|---|---|---|---|
| Growth, led 1 quarter | 0.04 | 0.48 | 0.44 | 60 |
| Growth, led 2 quarters | -0.18 | 0.48 | 0.66 | 59 |
| CPI inflation, led 1 quarter | 0.49 | 0.48 | -0.01 | 60 |
| CPI inflation, led 2 quarters | 0.40 | 0.48 | 0.08 | 59 |

Led growth lined up with the path less well than contemporaneous growth.
Led inflation at one quarter tied with MAS's decisions, as the sealed CPI
sensitivity did (D -0.0421).

**(c) Effective sample size.** The 61 intervals do not overlap, so the
dependence is serial. The lag-1 autocorrelations were 0.14 for the path,
0.52 for MAS's score and 0.57 for growth.

```
N_eff = N * (1 - r_y * r_x) / (1 + r_y * r_x)      Bartlett, lag 1
```

This gives 53 for MAS's score and 52 for growth. A Spearman coefficient then
has a standard error of about 0.14, against the 0.13 that THESIS assumed.

### A6. Context for the article (round 5)

| Item | Value |
|---|---|
| Yen per US dollar, Jan-Mar 2021 (mean of the log, S2) | 105.9 |
| Yen per US dollar, Oct-Dec 2025 | 154.1 |
| Japan's real broad index (S1b), 2025 average | 72.5, the 2nd lowest of 32 full years since 1994 |
| Lowest full year | 2024, at 71.5 |
| December 2025 among all 392 months | 9th lowest |
| Lowest month | 65.2, in July 2026 |

The 2025 average was near the bottom of the series but not the lowest: 2024's
was lower, and the lowest months came in 2026. One line of context in the
article links the yen's fall to the gap between Japanese and US interest
rates. Japan's side is cited to the Bank of Japan's statement of 19 March 2024
(`raw/s9_boj_mps_20240319.html`), which ended its negative interest rate
policy. The Federal Reserve's policy-rate page could not be retrieved: the
session's network policy refused the host. So the US side stays general and
cites nothing. Nothing here tests the interest-rate link.

The specimen at the two-decimal rates the article prints, S$1.28 and S$0.83
per 100 yen: 78,125 and 120,482 yen per S$1,000, said as "about 78,000" and
"about 120,000".

## 11. References

- Balassa, B. (1964). "The Purchasing-Power Parity Doctrine: A Reappraisal."
  *Journal of Political Economy* 72(6): 584-596.
- Fung, S. S., M. Klau, G. Ma and R. N. McCauley (2006). "Estimation of Asian
  effective exchange rates: a technical note." *BIS Working Papers* No 217,
  October. In raw/ as `s1f_bis_wp217_asian_eer.pdf`.
- Klau, M. and S. S. Fung (2006). "The new BIS effective exchange rate
  indices." *BIS Quarterly Review*, March, pp 51-65. In raw/ as
  `s1e_bis_qr0603_eer.pdf`.
- Monetary Authority of Singapore. "Frequently Asked Questions on Singapore's
  Monetary Policy Framework." Retrieved 3 October 2026. In raw/ as
  `s5c_mas_mp_faqs.pdf`.
- Samuelson, P. A. (1964). "Theoretical Notes on Trade Problems." *Review of
  Economics and Statistics* 46(2): 145-154.
