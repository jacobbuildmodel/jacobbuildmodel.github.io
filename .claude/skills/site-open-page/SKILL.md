---
name: site-open-page
description: Publish an open question page in content/open/ on the seal day. Use when a piece's predictions have just been sealed and the prompt gives the piece slug, the seal commit URL, the title and the date. Copies the sealed draft verbatim, adds its hash entry to data/open_seals.yaml, opens the PR, never merges.
---

# site-open-page

Inputs, all from the prompt; stop and ask if any is missing:
- piece slug (for example `sgd`)
- seal commit URL (`https://github.com/jacobbuildmodel/<repo>/commit/<40-char sha>`)
- title, exactly as Jacob approved it
- date (`YYYY-MM-DD`), the seal day

Follows office/CHECKPOINTS.md (Checkpoint S), office/QUESTION_RULES.md and
office/STORY_CRAFT.md. A box that cannot be ticked is a FAIL, reported in the
hand-back, never fixed by rewording the sealed text.

1. Read office/CHECKPOINTS.md, office/QUESTION_RULES.md, office/STORY_CRAFT.md
   and office/REPLY_FORMAT.md from origin/main.
2. Fresh clone of this repo; branch from origin/main
   (`git checkout -b open-<slug> origin/main`).
3. Confirm the date is the seal day: in the source repo,
   `TZ=Asia/Singapore git log -1 --date=format-local:%Y-%m-%d --format=%cd <sha>`
   prints the input date, and today (Singapore) is that date. If not, stop:
   STATUS blocked.
4. Find the sealed draft of the page at the seal commit (the path the prompt
   names, or the piece folder's open-page draft). Record its md5. If the
   prompt gives an md5, it must match.
5. Write `content/open/<date>-<slug>.md`. Body: the draft text copied
   verbatim, byte for byte. Front matter only: `title` (the input title,
   verbatim), `date`, `draft: false`, `answerDue`, `showToc: false`,
   `summary`, `repo`. No `answered:` line.
6. Add no data values. Diff the body against the draft: no difference. The
   front matter `summary` carries no outcome number (Checkpoint S: the page
   is drafted with no data values).
7. Link the seal commit: the body links the sealed THESIS.md (or the commit)
   at the full 40-character sha from the input URL, and states the short hash
   and the date. If the draft lacks the link, stop and report it; do not add
   prose to a sealed page.
8. Read-only checks, reported, never fixed here: the page opens with a real,
   dated specimen or a labelled thought experiment, then the puzzle, and
   states the bet by the end of the first paragraph (STORY_CRAFT S1, S2;
   QUESTION_RULES H3, H5); it links back to the last answer (STORY_CRAFT S9);
   the title passes QUESTION_RULES H1-H7 as Jacob approved it.
9. Pure ASCII: `LC_ALL=C.UTF-8 grep -nP '[^\x00-\x7F]' <page>` prints
   nothing (this also catches em dash, U+2212 and U+00D7).
10. Vale on the changed files, as lint.yml runs it:
    `git diff --name-only --diff-filter=AM origin/main...HEAD -- 'content/*.md'`
    then `vale --no-wrap <files>` (Vale 3.24.0). 0 errors. If Vale flags
    sealed text, stop: STATUS needs Jacob (a one-file exemption in .vale.ini
    is Jacob's call, never a rewording).
11. aitell as deploy.yml runs it:
    `python3 scripts/aitell.py content/economics/*.md content/process/*.md content/open/*.md content/scorecard.md content/corrections.md content/ideas.md --strict --published-only`.
12. `hugo --minify` builds clean, and the page is in public/open/. Before
    08:00 SGT the UTC clock is still on the day before; build with
    `--clock <date>T00:30:00Z` to see what the 08:30 SGT deploy publishes.
13. Screenshots with Playwright at 390px and 1280px wide, light and dark
    (emulated colorScheme): the new page, /open/, and the home page's open
    questions strip. No clipped or overlapping text. Attach to the PR body.
14. Strip Hugo build artifacts before committing: `git checkout -- go.mod`,
    remove go.sum, public/, resources/, .hugo_build.lock.
15. Commit the page, push, and open the PR against main. Never merge.
16. On the same branch, add the page's entry to data/open_seals.yaml: `path`,
    `body_md5` (md5 of everything after the closing `---`; the "no entry"
    line of `python3 scripts/check_open_pages.py` prints it), and `seal` (the
    input URL). Run `python3 scripts/check_open_pages.py --base origin/main`:
    passed. Commit and push.
17. `git diff --name-only origin/main...HEAD` lists only the new page and
    data/open_seals.yaml.
18. Hand back in office/REPLY_FORMAT.md format, 12 lines max, no diffs.
    CHECKS lines: hugo, vale, aitell, check_open_pages.py.
