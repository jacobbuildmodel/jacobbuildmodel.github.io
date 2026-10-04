---
name: site-pubday
description: The publication-day PR for an answer article. Use on the day an answer article goes live, when the checker's prompt supplies the scorecard numbers. Updates content/scorecard.md with those numbers as given, marks the open question page answered, adds a named Ideas entry, and nothing else. Opens the PR, never merges.
---

# site-pubday

Inputs, all from the checker's prompt; stop and ask if any is missing:
- sealed, held, failed, neither, brier, brierN, and the running record
  wording for the scorecard
- the article's URL (`/economics/<date>/`) and the open page it answers
- the Ideas entry, if one is named (name, one-sentence definition, source)

Follows office/CHECKPOINTS.md (Checkpoint 3, scorecard box),
office/QUESTION_RULES.md and office/STORY_CRAFT.md.

1. Read office/CHECKPOINTS.md, office/QUESTION_RULES.md, office/STORY_CRAFT.md
   and office/REPLY_FORMAT.md from origin/main.
2. Fresh clone of this repo; branch from origin/main. The article is on
   main and its date is today.
3. Every scorecard number (sealed, held, failed, neither, brier, brierN,
   running record) is copied from the prompt. This chat never computes,
   rounds, sums or corrects one. If a number looks wrong, stop: STATUS needs
   Jacob, with the line it disagrees with.
4. content/scorecard.md: set the front matter `sealed`, `held`, `failed`,
   `neither`, `brier`, `brierN` to the supplied values, and the title and
   body wording that state them, verbatim from the prompt.
5. `python3 scripts/check_open_pages.py --base origin/main` passes. It checks
   sealed == held + failed + neither; if that fails, the supplied numbers
   disagree with each other: stop and report, do not adjust.
6. Mark the open page answered with one front matter line,
   `answered: "/economics/<date>/"`, and nothing else on that page. The
   body stays byte for byte, so its body_md5 in data/open_seals.yaml still
   matches (step 5 shows it).
7. If an Ideas entry is named, add it to content/ideas.md in the existing
   shape (heading, one-sentence definition, "From:" link), text verbatim
   from the prompt (STORY_CRAFT S3). If none is named, do not touch the file.
8. Keep the PR on its own: `git diff --name-only origin/main...HEAD` lists
   only content/scorecard.md, the open page, and content/ideas.md if step 7
   applied. No other change rides along. If Vale flags sealed open-page text,
   stop: a one-file exemption is Jacob's call.
9. Vale on the changed files as lint.yml runs it (0 errors); aitell as
   deploy.yml runs it (`--strict --published-only`).
10. `hugo --minify --clock <date>T00:30:00Z` builds clean. Check in public/:
    the open page shows "Answered: read the verdict" linking the article;
    the home page band shows the supplied numbers; the open page is gone
    from the home page's open questions strip.
11. Screenshots with Playwright at 390px and 1280px wide, light and dark: the
    scorecard, the answered open page, and the home page band.
12. Strip Hugo build artifacts: `git checkout -- go.mod`, remove go.sum,
    public/, resources/, .hugo_build.lock.
13. Commit, push, open the PR against main. Never merge.
14. Hand back in office/REPLY_FORMAT.md format, 12 lines max, no diffs.
    CHECKS lines: hugo, vale, aitell, check_open_pages.py.
