# CP0 note 4: The RTS Link and heartland retail sales

Input for the purpose review of 6 Nov 2026 (idea scout candidate 4). Not a verdict; no sealed
wording, no confidences.

**Stem.** Passenger service on the RTS Link, five minutes from Woodlands North to Bukit Chagar in
Johor Bahru, is expected in February 2027, subject to approvals (LTA and Malaysia's Ministry of
Transport, 2 Oct 2026). A study for three business bodies projects a net rise in outbound spending
equal to 0.4 per cent of Singapore's 2025 retail and F&B sales, groceries first (CNA, 16 Jul 2026).
A CNA check found several everyday groceries 30 to 40 per cent cheaper in Johor Bahru at S$1 to
RM3.15 (CNA, 23 Jul 2026).

**(a)** Using cross-price elasticity of demand and transaction costs, explain why a cheaper ringgit
and a faster crossing may shift grocery spending to Johor Bahru.

**(b)** Discuss whether rental relief for heartland shops or letting the market adjust is the more
appropriate response.

**Decision.** MOF, MTI and Enterprise Singapore on heartland support in Budget 2027; HDB on rents
for its shops (its stated approach is case-by-case help, such as shorter tenancies; the date of
that answer is unverified). If volumes follow the ringgit: a case for temporary help in grocery
and pharmacy lines. If not: costs, not Johor, are the main pressure, and market adjustment stays
the default. Stakes Medium.

**Rivals.**
- Woodlands retailers: "When the train opens, we're doomed" (CNA TODAY, 7 Aug 2026); merchants ask
  for rental support (CNA, 18 Jun 2026).
- SBF, RAS and SRA: the projection above, and wider CDC vouchers (CNA, 16 Jul 2026).
- Bank economists: the RTS Link is "not expected to topple" retail (Business Times, 10 Apr 2026);
  an academic: the exchange rate may matter more than the line (Singapore Business Review, 24 Sep
  2026); both as cited by the scout.
- Already stated? The industry figure is a projection, not an outcome. Abroad, yes: a stronger
  Canadian dollar cut Canadian retail sales, more so near the border (Baggs, Fung and Lapham,
  Journal of International Economics, 2018).

**Data (labels and coverage only).** SingStat M602201, Retail Sales Index, chained volume,
monthly, 1985 Jan-2026 Aug: Supermarkets & Hypermarkets; Mini-Marts & Convenience Stores; Food &
Alcohol; Petrol Service Stations (control); Cosmetics, Toiletries & Medical Goods; Total excluding
motor vehicles. M602211, F&B Services Index, same span. M700051, exchange rates, monthly, 1988
Jan-2026 Sep (ringgit row). For (b): M085841 and M085831, business cessations and formations by
detailed industry, monthly, 1990 Jan-2026 Sep (ACRA; supermarkets and minimarts, food and
alcohol). Gaps: no land-crossing series (M650661 is air and sea) and no regional retail series, so
the Woodlands-only fear cannot be tested.

**Method.** (a) Regression of monthly supermarket volume on the S$ price of the ringgit, with lags,
total retail and season as controls, over 2011-2019 and from April 2022 (the land border was closed
from March 2020 to 1 April 2022); the cross-price elasticity is the volume change per 1 per cent
cheaper ringgit. Second bet: a Bayesian structural time series for six months after opening, with
F&B and non-food rows as controls. (b) Grocery and pharmacy closures against other retail around
the 2022 reopening; an LLM sorts ACRA's rows by the study's categories, hand-checked. The rest of
(b) is reasoned: relief against adjustment, on equity and on whether relief only delays exit.

**Smallest effect that matters.** An elasticity of 0.1 (1 per cent of supermarket volume per 10 per
cent change in the ringgit) within three months; for the RTS bet, a 1 per cent dip.

**Positive control.** Petrol station volume must fall after the border reopened on 1 April 2022,
net of total retail. If the method cannot see cross-border fuel buying, it cannot see groceries.

**G3 grid.** Yes = supermarket volumes fall when the ringgit gets cheaper. Prior in per cent, not
a confidence.

| | Data says yes | Data says no |
|---|---|---|
| People believe it | "A cheaper ringgit pulls groceries to Johor Bahru" (30) | "Even a cheap ringgit barely moves Singapore groceries" (50) |
| Nobody suspects it | hidden link (5) | no news (15) |

**Seal-by and kill.** Seal by 31 Dec 2026, before the line opens. Kill: no passenger service by
30 Jun 2027 voids the RTS bet, and the ringgit test is judged alone.

**Cost.** 6-8 working days.
