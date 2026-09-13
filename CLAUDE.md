# CLAUDE.md — jacobbuildmodel.github.io

Instructions for Claude Code working in this repository. Read this before any commit.

## Mobile reading pass — a `layouts/single.html` override exists, and why

The site has a project-level `layouts/single.html` that overrides PaperMod's default. This is
Hugo's standard, sanctioned override pattern — it does not modify the vendored theme in
`themes/PaperMod/`, which stays untouched and gets replaced fresh on every build. If PaperMod
ever updates its own `single.html` with new features, this override will silently not pick them
up; that tradeoff was accepted deliberately because no narrower hook point exists. PaperMod ships
`extend_post_content.html` for adding content, but it only fires *after* the article body — no
use for anything that needs to be seen in the first three seconds of a skim.

**What the override adds:** a small layer badge (ECONOMICS / STOCKS), derived automatically from
`.Section` — no per-post authoring, so it can't drift out of sync the way a manually-typed tag
could. It renders right after the date/reading-time line, before the table of contents.

**Why this exists at all:** a returning reader skimming on their phone needs to know which
section they've clicked into before committing to read it. That's invisible without this —
previously only the nav bar carried that information, not the article itself.

Every section keeps `showToc: true` — economics pieces and stock pages are both long-form enough
to benefit from a table of contents between the title and the hook. Set in two places:
`scripts/site_publish.py`'s `build_front_matter` (the pipeline path for economics) and
`content/stocks/TEMPLATE.md` (the hand-authoring path for stock pages). Both need to agree, or
the two paths silently diverge.

**Tested with real browser screenshots at 390px width (iPhone-class), not just by reading the
CSS:** the hook blockquote has a tinted background, not just a left border. First attempt used
`var(--entry)` — turned out to be a dead end worth knowing about: PaperMod's light theme sets
`--entry` identical to `--theme` (both pure white), so that tint was completely invisible in
light mode, the site's now-primary reading mode. Caught only by actually screenshotting it, not
by reading the CSS rule and assuming it worked. Switched to `var(--code-bg)`, which is
genuinely distinct from the page background in both light and dark mode — verified with
screenshots of both before trusting it.

**Numeric tables** get `font-variant-numeric: tabular-nums` so digits in a comparison table sit
at equal width and actually line up in a column, instead of ragged proportional-width digits that
are harder to scan. This doesn't retroactively rewrite any live article's prose into a table —
that's an editorial call about existing published content, not a styling one, and stays with
whoever's writing the next piece.

## What this repo is

The public site. Hugo + PaperMod, deployed to GitHub Pages by GitHub Actions on push to `main`.
**Everything committed here is world-readable, permanently, and indexed by search engines.**
There is no such thing as a private commit in this repo.

## The never-publish list — this is the hard boundary

Refuse to write, commit, or push anything containing:

- **Holdings, position sizes, weights, cost basis, account balances, cash, or P&L.** In any form,
  including "small position", "half size", "I'm long", or a ticker paired with a percentage.
- **Kelly fractions, position sizing output, conviction scores, composite scores, or rankings.**
  These are MERIDIAN / CATALYST internals. A rank is a recommendation with the reasoning removed.
- **Performance or returns.** Realised, unrealised, backtested, or hypothetical.
- **Any API key, token, password, or broker credential.**
- **Personal identifiers** — account numbers, addresses, tax IDs.
- **Recommendation language** — "buy", "consider buying", "price target", "strong conviction",
  "I'm adding". The site publishes reasoning, never a directive.
- **§7 HANDOFF blocks or a closing JSON block**, if a source file ever carries one. Those are
  machine-facing, from the same model tooling that never-publish exists to keep off this site.

If you encounter any of the above in a source file you have been asked to publish: **stop, name what
you found and where, and write nothing.** Do not clean it up and proceed — surface it and wait.

## What MERIDIAN and CATALYST output may become

Model output is **never published as-is.** It is a source for human-written research notes.

| Model field | Publishable? |
|---|---|
| The mechanism — why capital would move | **Yes** |
| The question being researched | **Yes** |
| The falsifier and its window | **Yes** |
| Confidence tier (verified / inferred / speculative) | **Yes** |
| Ticker as a subject of research | **Yes** |
| Quality score, value score, composite, rank | **No** |
| Reverse-DCF implied growth rate as a *stated conclusion* | **No** — the method may be described, the output may not |
| Position size, Kelly fraction, allocation | **No** |
| Directional call, T+1 price estimate, expected payoff | **No** |
| Anything with the word "buy" attached to a ticker | **No** |

The watchlist format is fixed: **ticker · mechanism · the question I'm researching · falsifier ·
confidence tier.** No score, no rank, no size, no target. If a note cannot be written in that shape,
it is not ready to publish.

## Publishing workflow

Content is staged, gated, then committed. Never write directly from a model output folder into
`content/`. The gate (`scripts/site_publish.py`) recognises exactly two sections:

```
<staging folder>/*.md
        │
        ▼
python scripts/site_publish.py "<staged file>" --section economics   # or --section stocks
        │
        ▼
content/<section>/YYYY-MM-DD.md                     # human edit pass happens HERE
        │
        ▼
commit + push                                       # only after the human pass
```

In practice `stocks` pages don't flow through this dated staging path — they're evergreen
(`content/stocks/<ticker>.md`), copied by hand from `content/stocks/TEMPLATE.md` and updated in
place, per the Repo conventions below. `--section stocks` exists in the gate but is rarely
exercised; `economics` is the active pipeline.

**The human edit pass is not optional and you do not perform it alone.** After staging, ask Jacob to
review before you commit. He is publishing under his own name; a figure you could not verify is his
error to own, so he gets the last look.

## Flagging figures

Any figure that is large, load-bearing, or extraordinary gets flagged to Jacob before publication,
not silently carried. Specifically: single-source sell-side estimates, anything above nine figures,
market-cap derivations built on an unsourced share price, and any percentage change above 50%.

A brief once carried a "$95.9M contract award" that was actually $742K. That was caught internally.
The same error published under Jacob's name is not recoverable in the same way.

## Compliance — Singapore Financial Advisers Act

This site publishes two kinds of content: Singapore economics research and stock explainer
pages. Stock-level content is the part that matters most here, not because naming a company is
itself risky, but because a communication can become "financial advice" under Singapore law when
it's tailored to an individual and/or the provider holds themselves out as a professional — see
the full reasoning on `content/process/_index.md#why-this-isnt-financial-advice`. Two rules follow
from that:

1. **Nothing published is ever tailored to an individual.** No content generated for this site should
   reference a specific reader's circumstances, respond to a specific person's question with a
   customised answer, or vary based on who's asking. If asked to draft a reply to a reader (email,
   comment, DM) that recommends or advises on their specific situation, refuse and use this line
   instead: *"I can't comment on that — I'm not a licensed financial adviser."* Never adapt that line
   to the asker's stated situation.
2. **Sector-level directional language gets the same care as stock-level.** "Energy looks favourable"
   is analysis; "you should overweight energy" is advice. The same scrutiny applies wherever a
   sector-level view appears, including inside a stock page or an economics piece.

**Monetization guardrails**, if that's ever discussed: display advertising is materially lower-risk
than affiliate links or a paid subscription tier, because remuneration tied to a reader's specific
investment decision (an affiliate click, a paid "premium calls" tier) is the clearest way this becomes
a regulated business under Singapore's carrying-on-a-business test. Flag any monetization change to
Jacob explicitly rather than implementing it — this needs an actual lawyer, not an inferred rule.

## The `aitell.py` lint gate — enforced in CI, before the build ever runs

`.github/workflows/deploy.yml` runs a `lint` job before `build`, wired with `needs:` so build
cannot start until lint passes — a separate `lint.yml` workflow couldn't gate this, since `needs:`
only works between jobs in the same file. It runs:

```
python scripts/aitell.py content/economics/*.md content/process/*.md --strict --published-only
```

`--strict` is required for it to actually fail the job — without it, `aitell.py` prints its
findings and still exits 0. `--published-only` skips anything still `draft: true`, so
work-in-progress drafts don't break CI. What it enforces at `--strict` level: em-dash density
under 8 per 1,000 words, and no gate-breaking Unicode (see the ASCII/Unicode note below) — the
rest of what `aitell.py` reports (opener monotony, sentence-rhythm clustering, AI-lexicon hits,
hedge language, tidy three-item lists) is advisory and does not block, but should be read and
acted on before a draft goes to Jacob for review.

`content/stocks/*.md` is **not** currently in the lint job's file list. If stock pages start
seeing heavier machine-assisted drafting, that's worth revisiting; until then, run
`scripts/aitell.py` on a stock draft by hand rather than assuming CI caught it.

## Repo conventions

- `hugo.toml` — config. Site title, menu, Umami ID, Buttondown username.
- `content/economics/` — Singapore economics research, the active pipeline. Has its own linter
  (`scripts/aitell.py`, gated in CI) and its own method page at `/process/economics/`. Each
  published piece's front matter carries a `repo:` field linking to the public code/data
  repository behind it — currently `coe-analysis`, `gst-passthrough`, and `hdb-affordability`,
  all under `github.com/jacobbuildmodel`. Link a new finding's repo the same way rather than
  inlining code in the post.
- `content/stocks/` — evergreen company explainer pages, one file per ticker (`nvda.md`,
  `pltr.md`, `shop.md`), copied from `content/stocks/TEMPLATE.md` and updated in place rather
  than dated and re-staged. `definitions.md` documents every score shown on a stock page.
- `content/process/` — the Method pages. `_index.md` is the hub at `/process/`, written for a retail
  reader and carrying the compliance section. Annexes: `economics.md`, `brief.md`. Revise the hub
  deliberately; it is the most-linked page and the compliance text lives there. `brief.md`
  documents the weekly-brief method for historical/reference purposes — the pipeline that used to
  produce that content is retired, but the source-tier system it introduced is still used
  everywhere else, so the page stays linked from the hub.
- `staging/` — raw model output before the gate. Gitignored, never committed. Meant to be pruned by
  `scripts/staging_prune.py`, never by hand — but see the gotcha below before relying on that script.
- `scripts/site_publish.py` — the gate. `SECTIONS = ("economics", "stocks")`; passing any other
  `--section` value is a hard argparse error, by design.
- `scripts/staging_prune.py` — retention for `staging/` only. **Its own `SECTIONS` tuple is
  `("news", "sector", "standouts", "briefs")` — none of which match `site_publish.py`'s current
  sections.** `--section economics` or `--section stocks` will fail with an invalid-choice error.
  Fix the tuple before relying on `--section` with this script; running it with no `--section` at
  all still works (it just iterates its own stale list, most of which are empty directories now).
- `scripts/aitell.py` — the prose/AI-tell linter, described above.
- `assets/css/extended/custom.css` — custom styling, including source-tier badges.
- `layouts/partials/` — `extend_head.html` (analytics), `extend_footer.html` (newsletter, disclaimer).
- Do not commit `public/`, `resources/`, or `.hugo_build.lock`.
- Use root-relative links (`/process/`), never absolute (`https://jacobbuildmodel.github.io/process/`),
  so a future custom domain doesn't break them.

## Staging and retention

`staging/` holds raw model output before it passes through the gate. It's gitignored — nothing
in it is ever committed. Once a piece is staged into `content/<section>/`, the raw dump has done
its job.

**This is the only thing that gets pruned.** The published archive in `content/` is never
touched by retention — a published post is a few KB, fifty-two weeks of them is nothing, and the
archive is the asset. Only `staging/` accumulates clutter worth clearing.

```
python scripts/staging_prune.py --status              # see what would happen, changes nothing
python scripts/staging_prune.py --prune                # actually delete, keeps newest 3 per section
```

Run it after a successful publish, not before — never prune a raw dump you haven't gated yet.

## A Hugo behaviour worth knowing

`hugo.toml` sets `buildFuture = false`. Any content dated later than the actual calendar day at
build time is silently excluded — no error, the page just doesn't exist. This will never bite in
normal use, because you only flip `draft: false` on or after the date you're publishing. But if a
page is ever staged and approved ahead of its own `date:`, it will vanish from the build with no
warning until that date arrives. If a published post is confirmed missing from the live site with
no build error, check this first.

## A gate-pattern gotcha

Several refusal patterns in `site_publish.py` are line-anchored (`^\s*VERDICT\s*:`, `^\s*ROUTE`,
`^\s*Score\s*:`) to avoid false-positiving on the word appearing mid-sentence. The first version
of these missed real leaks because a naturally-formatted markdown draft writes labels as
`**VERDICT:**`, and the literal `**` sits before the anchor, so `^\s*VERDICT` never matched.
Fixed by allowing optional `\*\*` or `__` around the keyword and the colon. If you add a new
line-anchored pattern to the gate, test it against a bold-wrapped variant before trusting it —
`**Label:**` is the default way anything gets written here, not an edge case.

A second gap found the same way: tier vocabulary like `Track D`, `WATCH-quality`, and
`STAYS COLD` was only being caught when a `CQS` number happened to sit nearby — strip the
number and the label alone passed clean through. These are now their own patterns, deliberately
narrow (`Track [A-Z]`, the exact compound phrases) so they don't false-positive on ordinary use
of the words "watch," "cold," or "track" in real prose — tested against a normal-English sample
before trusting the fix, not just against the leak.

## Before every push

- [ ] Nothing from the never-publish list, anywhere in the diff
- [ ] No §7, no JSON block, no DRIVE references
- [ ] Every decision-carrying figure has a source tier and a date
- [ ] Every thesis has a falsifier with a window
- [ ] Gaps section present and complete
- [ ] Flagged figures raised with Jacob and cleared
- [ ] `hugo --gc --minify` builds clean
- [ ] Jacob has reviewed the post

If any box is unchecked, do not push.

## House style — how pieces are written

The site is read by people with no finance background, often on a phone, often before work. Every
editorial rule below came from a real correction, not a preference.

**First person, never "we."** This is one person's research, published under Jacob's own name —
see the Compliance section above and `/disclaimer/`. Write "I" for the author's own reasoning and
"you" for the reader; never the royal or institutional "we," even in a piece with substantial
model-assisted drafting behind it. A "we" reads as a research house issuing a call, which is
exactly the impression the compliance section exists to avoid.

**Never argue with an objection nobody raised.** Early drafts of the Earnings section opened with
lines like "what a headline number hides, and how often the same check finds nothing," and articles
contained sentences like "it isn't a filing yet, and that's the first finding." Both are arguing
against an imaginary skeptic. Say what the thing is. If no one asked, don't answer it. This has been
flagged twice, once on the About page and once on the Earnings section, so treat it as a standing
failure mode rather than a one-off.

**Percentages over raw figures.** "Revenue came in about 3% below what analysts expected" is
readable. "Revenue of $4.62B against a $4.74B consensus estimate" is not, for this audience. Use
absolute figures only when the absolute size is the actual point.

**Explain jargon in the sentence, or cut it.** Don't write "non-GAAP" and move on. Either explain
what it means where it appears or find a plainer way to say it. Assume a smart reader with no
finance training, not a dumb one.

**The headline is the finding.** Not the date, not the section name. Under about 60 characters, so
it doesn't fill a phone screen and push the hook out of view.

**Forward-looking, always.** Every piece ends with what this makes worth watching and the specific,
dated observation that would confirm or kill it. Framed as questions to follow, never instructions
to act on. That framing is both the editorial voice and the compliance boundary, and they happen to
point the same direction.

**Read it aloud before publishing.** Anything that sounds like a machine wrote it gets rewritten.
