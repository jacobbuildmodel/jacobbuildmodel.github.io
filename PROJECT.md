# PROJECT.md

Living document for jacobbuildmodel.github.io. Read this first in any new
consolidation chat. Update it when a piece ships.

Last updated: 15 September 2026

---

## 1. What this is

A public research site by Jacob Ong, Singapore. One theme:

> **Singapore policy, measured with public data.**

The purpose is an application to read Economics at SMU. Applications open
mid-November and close in March. The site exists to demonstrate what an economics
department selects for: a clear question, a defensible method, honesty about what
the data cannot settle, and prose a non-specialist can follow.

Hugo + PaperMod, GitHub Pages, deployed by GitHub Actions on push to `main`.

- Site: jacobbuildmodel.github.io
- Repo: github.com/jacobbuildmodel/jacobbuildmodel.github.io
- Local: `C:\Users\jacob\dev\jacobbuildmodel.github.io`

Jacob is 22, a Temasek Polytechnic graduate in banking and finance, currently on a
twelve-month UBS traineeship in a KYC and AML seat, studying toward FMVA. He is not
licensed by MAS. He does not write code; he directs AI systems and does the
editorial and judgement work. That is stated openly on the About page.

---

## 2. Current state

**Six published economics pieces**, all reproducible:

| Date | Title |
|---|---|
| 2026-08-22 | The COE quota went up 62%. Prices tripled anyway. |
| 2026-08-29 | Perfect COE timing is worth $1,840. Nobody has it. |
| 2026-09-05 | Two in three COE bidders win. It is not a lottery. |
| 2026-09-08 | You can only see the GST rise in your water bill |
| 2026-09-12 | Motorcycle COEs fell 17%. Car COEs rose 43%. |
| 2026-09-19 | A four-room flat costs less income than in 2013 |

**Three public analysis repositories**, each independently verified to rebuild every
published figure from raw data:

- github.com/jacobbuildmodel/coe-analysis
- github.com/jacobbuildmodel/gst-passthrough
- github.com/jacobbuildmodel/hdb-affordability

**Sections:** `economics` (the live work), `stocks` (three pages, frozen, kept
current but not added to), `process` (Method hub plus annexes), plus About and
Disclaimer. Earnings, briefs, sector and standouts were deleted in September.

**Nav:** Economics, Stocks, Method, About. Five items fit on a phone; six do not.

---

## 3. The sequence

Committed, in order:

1. **HDB financing.** Was the HDB concessionary loan actually cheaper than a bank
   loan? It is fixed at 2.6 per cent while bank rates ran below that for a decade
   then rose above it. Uses FMVA modelling on data already verified. Brief sent to
   a researcher chat; first task is establishing whether a defensible public bank
   mortgage rate series exists for 2010 to 2025. If it does not, the piece changes
   shape or does not happen.
2. **Renew or replace at year ten.** When a car's ten-year COE ran out, was
   renewing it cheaper than scrapping and buying new, and did the February 2026
   PARF cut change the answer? Brief is in the WEBSITE project as
   briefs/BRIEF_coe_renew_or_replace.md.
3. **Cooling measures replication.** A published study found Singapore's cooling
   measures cut prices 10 to 15 per cent. Four more rounds have happened since
   (Dec 2021, Sep 2022, Apr 2023, Aug 2024). Does the finding still hold? Uses
   transaction data already held. Ruled out: Maisy Wong's ethnic quota papers
   (RES 2013, JPubE 2014) are not replicable, because the treatment variable was
   hand-built from 500,000 phonebook names with HDB permission.

---

## 4. Who does what

```
Researcher chat (one per piece)    produces analysis + article + repo
        |
        v
Consolidation chat (this one)      verifies, catches errors, writes instructions
        |
        v
Claude Code (in the repo folder)   copies files, commits, pushes
        |
        v
GitHub Actions                     lints, builds, deploys
```

**Claude Code is launched with `claude-web` from the repo folder.** It is the only
thing that writes to the repository. The consolidation chat produces instructions
for it, never zips to download. That change removed the main source of friction.

---

## 5. The verification standard

This is the job. Do not read and nod. Run things.

- Download the repository fresh from GitHub, delete every output, run the pipeline
  from clean, compare MD5s against published checksums.
- Recompute headline figures independently in pandas rather than trusting the
  researcher's arithmetic.
- Audit `requirements.txt` against every import using the AST.
- Build the site with Hugo, screenshot at 390px and desktop, light and dark.
- Run the publish gate and the prose linter exactly as CI runs them.
- Open cited sources and check the figures are there and current.
- Diff the live repository to confirm what shipped versus what was claimed.

**Things this has caught before publication**, each of which would have shipped
otherwise: a headline resting on a partial year that flattered the comparison on
both sides; five scripts failing on a clean machine from an undeclared dependency;
an income ceiling back-dated three years inside a row marked VERIFIED-PRIMARY; a
repository pushed one directory too deep so its README never rendered; a filename
collision that would have silently overwritten a published article; a prediction
reported only in the year it confirmed; a Unicode minus sign that crashed the gate
on Windows; a line-ending setting that would have broken every published checksum.

Verify against a freshly fetched archive. Reusing an earlier download has produced
a false negative before.

---

## 6. House style

Every rule came from a real correction.

- **Delivery comes first.** Research that is not shown clearly is wasted. Plan
  the key charts and headline numbers before the prose, and check every piece
  at 390px and desktop, light and dark, before publishing.
- **Never argue with an objection nobody raised.** Flagged three times. Standing
  failure mode.
- **Pure ASCII.** No em dashes. No U+2212 minus sign, it crashes the gate on
  Windows consoles. No U+00D7 multiplication sign, it blocks the linter.
- **No royal "we".** One person writes this site.
- **Plain English.** Jargon explained in the same sentence or cut.
- **Ratios and percentages over raw figures**, with the basis stated inline rather
  than only in a caption.
- **Headline is the finding**, under about 60 characters. Not the topic.
- **Headings read as a storyline** when scanned alone. Statements about the
  specific finding, not generic labels.
- **Every claim carries what would prove it wrong**, and a date by which you would
  know.
- **Results that did not work still get published.** This is on the Method page as
  a commitment.

Articles: hook blockquote, unheaded introduction, storyline headings, what would
prove this wrong, what this does not explain, what to take from this, sources.
1,200 to 1,800 words of linear read.

---

## 7. Compliance

Under Singapore's Financial Advisers Act, a communication becomes financial advice
when it opines on the merits of a specific investment AND a reader could expect to
rely on it. Jacob is not licensed by MAS.

Never: a buy or sell call, a price target, a rating, a position size, an overall
score, a ranking, or anything tailored to an individual reader.

Always: mechanism, evidence, and what would prove it wrong.

The publish gate scans everything and refuses on recommendation language, holdings,
position sizing and model internals. It has produced eight false positives on
legitimate prose, two of them on pages describing the site's own rules. If it
refuses something that reads legitimate, it may be a ninth. Report it rather than
rewording around it.

**Outstanding:** Jacob works in a bank compliance seat and the About page publicly
links a site publishing financial analysis. The conversation with UBS Compliance
about outside activities and personal dealing has not happened yet.

---

## 8. Gotchas that have cost real time

- **`buildFuture = false`.** Future-dated content is silently excluded with no
  build error. If a page is missing from a clean build, check this first.
- **Filename collisions.** `content/economics/YYYY-MM-DD.md` overwrites silently.
  Taken: 2026-08-22, 08-29, 09-05, 09-08, 09-12, 09-19.
- **Repository nesting.** Unzipping into a folder of the same name creates
  `repo/repo/`. GitHub then never renders the README. Happened twice.
- **`hugo.test.toml` staleness.** If generated before editing `hugo.toml`, the
  build uses the old config. Regenerate after every config change.
- **Verify via codeload, not raw.githubusercontent**, which serves stale content:
  `curl -sL "https://codeload.github.com/OWNER/REPO/tar.gz/refs/heads/main"`
- **Long pastes into Claude Code truncate.** Give one instruction at a time.
- **PowerShell multi-line pastes merge lines.** Give one command per line.
- **data.gov.sg, SingStat and MAS return 403 to sandboxes.** Files must come from
  Jacob by hand. Ask for everything in one consolidated message with URLs and a
  size warning.

---

## 9. Repository conventions

Every analysis repo must have, from the start rather than retrofitted:

```
raw/              source files as downloaded, plus RETRIEVED.txt recording
                  title, publisher, dataset ID, URL, retrieval date, bytes, MD5
NN_*.py           numbered scripts, run in order
figs/ out/        committed outputs
THESIS.md         pre-registered and sealed before data
README.md         question, method, finding, run order, checksums
CHECKSUMS.md5     BOTH inputs and outputs, in labelled sections
run_all.sh        one command, set -euo pipefail, ends on md5sum -c
requirements.txt  every third-party import, pinned
number_manifest.csv   every figure in the prose, its source and script
LICENSE           MIT
.gitattributes    containing exactly:  * -text
```

Pre-registration is non-negotiable. `THESIS.md` states the tests with numbered
survive-if and fail-if conditions, written before the data is touched. A test that
failed in the opposite direction to its prediction is the most valuable thing in
the HDB piece.

---

## 10. When to end a chat

Each consolidation chat covers one piece. When it ships:

1. Update section 2 and 3 of this file.
2. Commit it.
3. Start a fresh chat for the next piece.

Do not carry a chat across multiple pieces. The previous one ran from August to
mid-September, accumulated weeks of verification output, and messages eventually
started arriving empty.
