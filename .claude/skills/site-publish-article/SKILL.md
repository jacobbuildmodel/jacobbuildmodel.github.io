---
name: site-publish-article
description: Add an answer article to content/economics/ as a future-dated post that stays hidden until its date. Use when a piece's answer article is approved and the prompt names its source commit, title and publication date. Opens the PR, never merges, and does not touch the scorecard or the open page (that is site-pubday).
---

# site-publish-article

Inputs, all from the prompt; stop and ask if any is missing:
- the source of the article text (repo, commit, path) and its md5 if given
- title, exactly as Jacob approved it
- publication date (`YYYY-MM-DD`)
- the open question page this article answers

Follows office/CHECKPOINTS.md (Checkpoints 2 and 3), office/QUESTION_RULES.md
and office/STORY_CRAFT.md. Never reword a number or a claim; a box that fails
is reported, not edited around.

1. Read office/CHECKPOINTS.md, office/QUESTION_RULES.md, office/STORY_CRAFT.md
   and office/REPLY_FORMAT.md from origin/main.
2. Fresh clone of this repo; branch from origin/main.
3. The date is not already used: `ls content/economics/<date>*.md` prints
   nothing on origin/main (Checkpoint 2).
4. Write `content/economics/<date>.md` from the source, text verbatim; record
   the source md5 and confirm it matches the prompt's. Title verbatim.
5. Front matter: `draft: false`, `date: <date>`, the `repo` and dataset
   fields. With `buildFuture = false` in hugo.toml the page stays hidden
   until its date; that is the mechanism, so draft stays false.
6. Prove it stays hidden: `hugo --minify` (today's clock) does not build
   public/economics/<date>/; `hugo --minify --clock <date>T00:30:00Z` does.
   Report both.
7. Banned-word grep is clean:
   `grep -niE 'should|recommend|choose|better option|you should' <article>`
   prints nothing (CHECKPOINTS 2; STORY_CRAFT R1).
8. No em dash, U+2212 or U+00D7: `LC_ALL=C.UTF-8 grep -nP '\x{2014}|\x{2212}|\x{00D7}' <article>`
   prints nothing; pure ASCII preferred (`LC_ALL=C.UTF-8 grep -nP '[^\x00-\x7F]'`).
9. Read-only checks, reported: headline is the finding, under 60 characters
   (QUESTION_RULES 5, 7); verdict in the first screen (H5, STORY_CRAFT L7);
   specimen and puzzle in the first 60 words after the verdict card (S1, S2);
   links back to its open question page and points to the next one (S9); no
   "we"; none of R1-R7.
10. Vale on the changed files as lint.yml runs it (Vale 3.24.0, 0 errors).
    If a Vale exemption is needed, it is Jacob's call, and it covers one
    file only: a `[content/economics/<date>.md]` section in .vale.ini, never
    a glob or a directory. Check with `git diff origin/main -- .vale.ini`.
11. aitell as deploy.yml and lint.yml run it (`--strict --published-only`).
12. Screenshots with Playwright at 390px and 1280px wide, light and dark,
    built with `--clock <date>T00:30:00Z`: the article, its charts, and the
    home page. No clipped text, no overlapping labels. Attach to the PR body.
13. Strip Hugo build artifacts: `git checkout -- go.mod`, remove go.sum,
    public/, resources/, .hugo_build.lock.
14. `git diff --name-only origin/main...HEAD` lists only the article, its
    static assets, and a one-file .vale.ini section if Jacob approved one.
    The scorecard and the open page are not touched here.
15. Commit, push, open the PR against main. Never merge.
16. Hand back in office/REPLY_FORMAT.md format, 12 lines max, no diffs.
    CHECKS lines: hugo (today and --clock), vale, aitell, banned-word grep.
