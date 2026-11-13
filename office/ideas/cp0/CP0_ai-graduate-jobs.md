# CP0 note 3: Generative AI and entry-level graduate jobs

Input for the purpose review of 6 Nov 2026 (idea scout candidate 3). Not a verdict; no sealed
wording, no confidences.

**Stem.** On 12 October 2026 Prime Minister Lawrence Wong said "there may be that bottom rung of
the career ladder that is broken", and that the Government is "looking at whether there is a need
for new programmes, new schemes" (The Straits Times, 12 Oct 2026). Graduate Industry Traineeships
(GRIT), launched in October 2025, fund 70 per cent of a fresh graduate's allowance for three to six
months and now cover the 2026 cohort (CNA, 21 Aug 2026). From the second half of 2026, people on
selected SkillsFuture AI courses get six months' free use of premium AI tools (MOM, 3 Mar 2026).

**(a)** Explain how generative AI can act as a substitute for, or a complement to, entry-level
graduate labour, and how each case would show up in employment rates and starting pay.

**(b)** Discuss whether wage subsidies for first jobs or subsidised AI-skills training is more
effective for graduates of the most AI-exposed courses.

**Decision.** MOF, MOM and MOE in Budget 2027 and the Committee of Supply (Feb-Mar 2027), on the
"new schemes"; SWDA on GRIT for the 2027 cohort; students choosing courses. Substitute pattern:
first-job subsidies fill the missing rung. Complement pattern: training is the better spend.
Neither: the hiring cycle, as MOE holds. Stakes High.

**Rivals.**
- PM Wong (12 Oct 2026): the bottom rung may be broken.
- MOE (Parliament, 6 Apr 2026, as cited by the scout): the impact on entry-level demand "remains
  uncertain". MOM (written answer, 4 Aug 2026): graduate outcomes "have generally remained
  resilient".
- On (b): an academic warns that funded traineeships can be a "free ride" for firms (CNA, 21 Aug
  2026). Card, Kluve and Weber (Journal of the European Economic Association, 2018), a
  meta-analysis of over 200 studies: effects are near zero at first and turn positive two to three
  years on, most for programmes that build skills.
- Already stated? Partly. United States: Brynjolfsson, Chandar and Chen (Stanford Digital Economy
  Lab, Aug 2025, updated Aug 2026, as cited by the scout) find the youngest workers in the most
  exposed jobs lost ground. Singapore: cohort outcomes are public, and a 2025 fall in one course
  cluster was named in Parliament (6 Apr 2026). Only the exposure split on the 2026 survey is unseen.

**Data (labels and coverage only).** data.gov.sg d_3c55210de27fcccda2ed0c63fdd2b352, Graduate
Employment Survey, six autonomous universities (MOE), annual; metadata coverage Nov 2013 to Mar
2025, updated 5 Mar 2026; columns year, university, school, degree, overall and full-time
permanent employment rates, basic and gross mean and median pay, gross quartiles (2025 rows
unchecked). The 2026 survey is due about March 2027. Exposure: Eloundou et al., "GPTs are GPTs"
(Science, 2024), by O*NET-SOC occupation; the SSOC crosswalk is unchecked. SingStat M213751 All
Items deflates pay.

**Method.** (a) Difference-in-differences: full-time permanent employment and real median gross
pay by degree, most against least exposed third, 2023-2026 against each third's 2013-2022 path
(break: ChatGPT, November 2022), with an event study by year. Substitute: both fall. Complement:
employment holds and pay rises. An LLM maps each degree to up to three first-job occupations from
course descriptions; two people hand-check 50 degrees; the rule is sealed before any GES value is
joined. (b) The pattern in (a) points to one side, weighed against the meta-analysis; GRIT's
public counts have no comparison group and cannot settle (b) alone.

**Smallest effect that matters.** 3 percentage points of full-time permanent employment, or 3 per
cent of real median pay, between the most and least exposed thirds, against their own paths.

**Positive control.** Before any GES value is joined, exposure scores alone must rank computing,
accountancy and business analytics above medicine, nursing and physiotherapy.

**G3 grid.** Yes = graduates of the most exposed degrees lost more ground than the least exposed.
Prior in per cent, not a confidence.

| | Data says yes | Data says no |
|---|---|---|
| People believe it | "AI took first jobs from the most exposed degrees" (40) | "AI-exposed degrees did no worse in first jobs" (45) |
| Nobody suspects it | hidden link (5) | no news (10) |

**Seal-by and kill.** Seal by 31 Jan 2027, before the 2026 survey. Kill: the LLM map agrees with
the hand-coded map on fewer than 40 of the 50 degrees.

**Cost.** 9-11 working days, mostly the exposure map. Can merge with the menu's graduate
starting-pay candidate: same dataset, one seal.
