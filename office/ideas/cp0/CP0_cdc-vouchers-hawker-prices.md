# CP0 note 2: CDC vouchers and hawker food prices

Input for the purpose review of 6 Nov 2026 (idea scout candidate 2). Not a verdict; no sealed
wording, no confidences.

**Stem.** From 11 June 2026 each Singaporean household could claim S$500 in CDC vouchers, half for
more than 24,000 hawkers and heartland merchants and half for supermarkets, valid to 31 December
2027 (CNA, 11 Jun 2026). Asked on 3 March 2026 whether vouchers for every household feed
demand-pull inflation, MOF replied there is "no evidence", citing annual all-items inflation
(Hansard, 3 Mar 2026). The tranche planned for January 2027 was the one brought forward, so the
next is an open Budget 2027 decision.

**(a)** Explain why a voucher that can be spent only at certain sellers may raise their prices,
using the price elasticity of supply and the incidence of a demand-side subsidy.

**(b)** Discuss whether CDC vouchers or untied cash transfers are more effective in raising
low-income households' real purchasing power.

**Decision.** MOF in Budget 2027 (about Feb 2027): another tranche or not, its size, and vouchers
or untied cash (the Cost-of-Living Special Payment, GSTV-Cash). If prices rose: part of the
voucher reaches sellers, which favours cash or tighter targeting. If not: the demand-pull
objection falls, and the case rests on support for hawkers and heartland shops. Stakes Medium.

**Rivals.**
- Mr Lee Hong Chuang, MP (3 Mar 2026): the demand-pull worry. HardwareZone forum (1 Apr 2026, as
  cited by the scout): "If anything, CDC only makes the inflation worse."
- MOF, Mr Shawn Huang (3 Mar 2026): "no evidence"; package support "fully offset" the extra
  spending from high inflation for lower-income households, 2022-2025.
- SBF, RAS and SRA: widen CDC vouchers to more sectors (CNA, 16 Jul 2026).
- Already stated? On annual all-items data only. No monthly hawker test, and no comparison of
  vouchers against cash, was found.

**Data (labels and coverage only).** SingStat M213751, CPI (2024 base), monthly, 1961 Jan-2026
Sep: rows 1.11.3.1 Hawker Centres; 1.11.3.2 Food Courts, Coffee Shops & Kiosks; 1.11.1.1
Restaurants and 1.11.2 Fast Food Restaurants (comparisons, mostly outside the scheme); 1.03.2.3
Electricity (control). Row start dates unchecked. SingStat M213941, CPI for the lowest 20 per
cent, half-yearly, 1993 1H-2026 1H, with a Hawker Centres row. Events: tranches June 2020 to June
2026 (early dates to compile); GSTV-Cash each August; COL Special Payment from 9 Sep 2026. About 52
per cent of voucher spending to 3 Jun 2026 went to hawkers and heartland merchants (CDC, 11 Jun
2026).

**Method.** (a) Placebo-month permutation test: rank the hawker index's change in each tranche
month and the next against the same months in years without a tranche, differenced against
restaurants and fast food. Spending runs over up to 18 months, so the test looks for a step at
launch; mid-year tranches carry the weight, as Januaries are confounded. (b) The same test around
cash payouts: a hawker move with vouchers but not with cash means the tie leaks to sellers. Where
a household's hawker spending already exceeds its voucher, the voucher is inframarginal and works
like cash except through prices. An LLM extracts tranche and payout dates from CDC and MOF
releases, each hand-checked.

**Smallest effect that matters.** 0.5 per cent on the hawker index over the tranche month and the
next, above the same months in other years.

**Positive control.** The same method must find the months when SP Group's announced tariff
changes reached the Electricity row. If it cannot find a known, dated step, a null means nothing.

**G3 grid.** Yes = hawker prices rose in voucher months beyond the same months in other years.
Prior in per cent, not a confidence.

| | Data says yes | Data says no |
|---|---|---|
| People believe it | "CDC vouchers lifted hawker prices: sellers kept a share" (15) | "CDC vouchers did not lift hawker prices" (60) |
| Nobody suspects it | hidden link (5) | no news (20) |

**Seal-by and kill.** Seal by 27 Nov 2026, for the pre-Budget consultation (about early December
by precedent). Kill: the Hawker Centres row does not run monthly from January 2019 (coverage
count only).

**Cost.** 4-5 working days.
