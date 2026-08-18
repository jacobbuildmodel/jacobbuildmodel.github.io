# CLAUDE.md — jacobbuildmodel.github.io

Instructions for Claude Code working in this repository. Read this before any commit.

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

## Repo conventions

- `hugo.toml` — config. Site title, menu, Umami ID, Buttondown username.
- `content/briefs/` — the weekly series. `TEMPLATE.md` stays `draft: true`; never publish it.
- `content/process.md` — the Method page. Revise deliberately; it is the most-linked page.
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
