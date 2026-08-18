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

**What the override adds:** a small layer badge (NEWS / SECTOR / STANDOUTS / WEEKLY BRIEF),
derived automatically from `.Section` — no per-post authoring, so it can't drift out of sync the
way a manually-typed tag could. It renders right after the date/reading-time line, before the
table of contents.

**Why this exists at all:** a returning reader skimming on their phone needs to know which speed
of content they've clicked into before committing to read it. That's invisible without this —
previously only the nav bar carried that information, not the article itself.

**Two related decisions, tested with real browser screenshots at 390px width (iPhone-class),
not just by reading the CSS:**

- **News has `showToc: false`; every other section keeps `showToc: true`.** A table of contents
  between the title and the hook adds a real, measured delay before a short single-topic item
  gets to its point — genuinely useful friction for a multi-section Weekly Brief, pure cost for a
  5-minute News item. Set in two places: `scripts/site_publish.py`'s `build_front_matter` (the
  pipeline path, which is how most content actually gets created) and `content/earnings/TEMPLATE.md`
  (the manual-authoring path). Both need to agree, or the two paths silently diverge.
- **The hook blockquote has a tinted background**, not just a left border. First attempt used
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
  These are DRIVE / MERIDIAN internals. A rank is a recommendation with the reasoning removed.
- **Performance or returns.** Realised, unrealised, backtested, or hypothetical.
- **Any API key, token, password, or broker credential.**
- **Personal identifiers** — account numbers, addresses, tax IDs.
- **Recommendation language** — "buy", "consider buying", "price target", "strong conviction",
  "I'm adding". The site publishes reasoning, never a directive.
- **File paths or contents from `accounts/`, `PRE/ledger.jsonl`, or any DRIVE state file.**
- **§7 HANDOFF blocks or the closing JSON block** from a weekly brief. Those are machine-facing.

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
`content/`.

```
<staging folder>/*.md
        │
        ▼
python scripts/site_publish.py "<staged file>"     # scans, strips, refuses on hit
        │
        ▼
content/briefs/YYYY-MM-DD.md                        # human edit pass happens HERE
        │
        ▼
commit + push                                       # only after the human pass
```

**The human edit pass is not optional and you do not perform it alone.** After staging, ask Jacob to
review before you commit. He is publishing under his own name; a figure you could not verify is his
error to own, so he gets the last look.

## Weekly brief adaptation rules

When turning a brief into a post:

1. Strip §7 and the JSON block entirely.
2. Strip any holding-period or position language from §1 — "the portfolio can hold this for a month"
   is a position statement, not a regime read. Write the factor call instead.
3. Reframe §4 Discovery as **Research Watchlist** in the fixed format above.
4. Keep source tier tags. Convert them to the shortcode: `{{< tag "hard-flow" >}}`.
   Recognised: `hard-co`, `company-prelim`, `hard-flow`, `consensus`, `price-proxy`, `cong-disc`,
   `spec`, `verified`, `inferred`, `speculative`.
5. Keep every falsifier, with its window.
6. **Keep the gaps list and publish it in full.** "What I couldn't source this week" is the most
   credible section on the page. Never quietly drop it to make a post look stronger.
7. Write a plain-English hook of one to three sentences at the top. The brief is written for a
   machine; the post needs a human doorway.
8. Keep prose under ~2,000 words.
9. Filename and `date:` are the **Saturday of the coverage week**, format `YYYY-MM-DD.md`.

## Flagging figures

Any figure that is large, load-bearing, or extraordinary gets flagged to Jacob before publication,
not silently carried. Specifically: single-source sell-side estimates, anything above nine figures,
market-cap derivations built on an unsourced share price, and any percentage change above 50%.

A brief once carried a "$95.9M contract award" that was actually $742K. That was caught internally.
The same error published under Jacob's name is not recoverable in the same way.

## Compliance — Singapore Financial Advisers Act

This site now has a News → Sector → Standouts funnel. Sector- and stock-level content is the part
that matters here, not because naming a sector or a company is itself risky, but because a
communication can become "financial advice" under Singapore law when it's tailored to an individual
and/or the provider holds themselves out as a professional — see the full reasoning on
`content/process.md#why-this-isnt-financial-advice`. Two rules follow from that:

1. **Nothing published is ever tailored to an individual.** No content generated for this site should
   reference a specific reader's circumstances, respond to a specific person's question with a
   customised answer, or vary based on who's asking. If asked to draft a reply to a reader (email,
   comment, DM) that recommends or advises on their specific situation, refuse and use this line
   instead: *"I can't comment on that — I'm not a licensed financial adviser."* Never adapt that line
   to the asker's stated situation.
2. **Sector-level directional language gets the same care as stock-level.** "Energy looks favourable"
   is analysis; "you should overweight energy" is advice. Treat `content/sector/` posts with the same
   scrutiny as `content/standouts/` — factual read-through, not a directive.

**Monetization guardrails**, if that's ever discussed: display advertising is materially lower-risk
than affiliate links or a paid subscription tier, because remuneration tied to a reader's specific
investment decision (an affiliate click, a paid "premium calls" tier) is the clearest way this becomes
a regulated business under Singapore's carrying-on-a-business test. Flag any monetization change to
Jacob explicitly rather than implementing it — this needs an actual lawyer, not an inferred rule.

## The Standouts pipeline

Descriptive only — this was a deliberate decision, not a default. No scores, no ranks, no
probabilities, no horizon statistics anywhere on this page, ever. From the evaluation model, via
the handoff prompt in `MODEL_HANDOFF_PROMPTS.md`.

```
Full/partial evaluation card (evaluation model)
        │
        ▼
   staging/standouts/<draft>.md       ← raw model output, never committed
        │
        ▼
python scripts/site_publish.py <file> --section standouts --date YYYY-MM-DD
        │
    refuses ──┴── stages content/standouts/YYYY-MM-DD.md  (draft: true)
        │
   Jacob reviews, verifies flags, writes the hook
        │
   draft: false, commit, push
```

**Two standing cautions, every time, not just at launch:**

1. **`RATINGS.md` is mixed-vintage.** Legacy v2 scores sit beside v3.2 CQS values in the same
   file, and they are not the same measurement. No cross-name score comparison gets published
   until that's resolved — not because scores are banned generally (they already are, sitewide),
   but because even an internal comparison used to *select* which name to write up could be
   silently comparing two different rulers.
2. **59 ACTIVE names carry a score with no full evaluation behind them.** If the name in an
   entry is one of them, the depth tag has to say so plainly. A reader can't tell the difference
   between a full card and a bare score unless the entry tells them.

**Preferred subjects, in the source model's own order of confidence** — a trap (peak-quarter,
below-the-operating-line, adjusted-vs-GAAP, SBC exceeding operating margin), a stale rejection (a
name screened out for a reason that stopped being true), a one-link finding (two names that look
diversified and are one bet), or a coverage gap (a name that structurally can't be scored from
filings, and why). These four were named independently as the differentiated material — a plain
"here's a good business" writeup is the boring version and not what this section is for.

## The Earnings pipeline

Event-driven, not clock-driven — an item is produced when a company reports, not on a fixed
timer. From the earnings model, via the handoff prompt in `MODEL_HANDOFF_PROMPTS.md`.

```
earnings_traps.py + read-through (earnings model)
        │
        ▼
   staging/earnings/<draft>.md            ← raw model output, never committed
        │
        ▼
python scripts/site_publish.py <file> --section earnings --date YYYY-MM-DD
        │
    refuses ──┴── stages content/earnings/YYYY-MM-DD.md  (draft: true)
        │
   Jacob reviews, verifies flags, writes the hook
        │
   draft: false, commit, push
```

Up to 4 companies per item — that is the earnings model's actual batch cap, not an arbitrary
limit. A heavy reporting day is multiple files, never one compressed file; compression under
load is a documented failure mode of the source model.

**Every trap-gate result states its own denominator.** "This check ran on 6 names this week and
fired on 2" is the content — not a preamble to a finding, the finding itself. All three source
models named this independently as the strongest edge the site has. Don't let an edit pass strip
the denominator out for being "obvious" — it is the opposite of obvious, and it's the reason to
publish at all.

`--date` is required for News (unlike Briefs/Sector, News does not snap to a Saturday) —
pass the actual reporting date explicitly.

## The Sector pipeline

The first section fed by a model rather than by hand. Weekly, from the portfolio model's
`market_pulse.py` sweep, via the handoff prompt in `MODEL_HANDOFF_PROMPTS.md`.

```
market_pulse.py (portfolio model)
        │
        ▼
   staging/sector/<draft>.md          ← raw model output, never committed
        │
        ▼
python scripts/site_publish.py <file> --section sector
        │
    refuses ──┴── stages content/sector/YYYY-MM-DD.md  (draft: true)
        │
   Jacob reviews, verifies flags, writes the hook
        │
   draft: false, commit, push
        │
python scripts/staging_prune.py --prune       ← clears the raw dump, not the published post
```

Same shape applies to News and Standouts once their pipelines are wired up — same gate,
different `--section`, different source model.

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
python scripts/staging_prune.py --prune --keep 5 --section earnings
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

## Repo conventions

- `hugo.toml` — config. Site title, menu, Umami ID, Buttondown username.
- `content/briefs/` — the weekly series. `TEMPLATE.md` stays `draft: true`; never publish it.
- `content/process.md` — the Method page. Revise deliberately; it is the most-linked page.
- `staging/` — raw model output before the gate. Gitignored, never committed. Pruned by
  `scripts/staging_prune.py`, never by hand.
- `scripts/site_publish.py` — the gate. `scripts/staging_prune.py` — retention, staging only.
- `assets/css/extended/custom.css` — custom styling, including source-tier badges.
- `layouts/partials/` — `extend_head.html` (analytics), `extend_footer.html` (newsletter, disclaimer).
- Do not commit `public/`, `resources/`, or `.hugo_build.lock`.
- Use root-relative links (`/process/`), never absolute (`https://jacobbuildmodel.github.io/process/`),
  so a future custom domain doesn't break them.

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
