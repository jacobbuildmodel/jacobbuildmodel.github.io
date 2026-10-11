# CHECKPOINTS -- objective pass criteria

Purpose: nothing reaches Jacob as "ready" unless every box below is ticked with
evidence (a command output, an md5, a file path, or a page and line). A box that
cannot be ticked is a FAIL, not a judgement call. Each checkpoint is passed twice:
first by the bot checker (office/CHECKER.md), then independently by the Cowork
checker, who also compares its findings with the bot's.
Revised 25 September 2026 to carry office/EXCELLENCE_PLAN.md (A-E).
Revised 26 September 2026: checker independence rules (section at the end).
Revised 28 September 2026: story-craft boxes from office/STORY_CRAFT.md (S1-S9, R1-R7).
Revised 29 September 2026: data feasibility first; HOOK rules and Editor review;
merge commits for sealed branches (lessons from the PWM piece).

## Checkpoint 0 -- the question (before any brief is handed to a researcher)
Goal: the piece is built on a fight or belief people already have. See office/QUESTION_RULES.md.
- [ ] Rule 0 answered in one line each: what people already believe or argue; the
      sides or the belief and its rival explanation; what the reader or country
      stands to gain or lose; the extreme of each side with an everyday analogy.
- [ ] Started from the argument or the lived moment, not from what a dataset can compute.
- [ ] DATA FEASIBILITY: every planned test lists the exact series it needs, and a
      label-and-coverage listing (no values) confirms each exists at the needed
      detail and years. A test whose series does not exist is dropped now, not
      after the design is built.
- [ ] At least one other country that chose differently is named (world view).
- [ ] The title and first paragraph pass HOOK rules H1-H7 and the Editor's blind
      review (office/EDITOR.md); the sealed question passes rules 1-9.
- [ ] At most one named idea proposed for the piece (EXCELLENCE_PLAN D).
- [ ] Jacob has approved the question and the title.

## Checkpoint S -- the seal (before any outcome value is opened)
Goal: the bet is fixed, dated and public.
- [ ] Coverage known (00_coverage.py output in RETRIEVED.txt); year ranges written
      as numbers in every test.
- [ ] Every scored prediction has a confidence set by Jacob alone. The researcher
      may propose a number with a reason (kept beside it); the checker raises
      considerations only and never proposes or adjusts a number. Any number
      changed after someone else's input is disclosed with both values.
      Expected number holding stated (sum of confidences). (EXCELLENCE_PLAN A)
- [ ] Weak-evidence sentence written where the design leans one way.
- [ ] Analysis scripts written and tested on synthetic data before the seal, and
      their md5s recorded in the seal manifest (PWM onward).
- [ ] Seal committed on its own; commit hash recorded.
- [ ] Open question page drafted with no data values, reviewed, and published on
      the seal day with the commit hash linked. (EXCELLENCE_PLAN B)
- [ ] Open question page opens with a real, dated specimen or a labelled thought
      experiment, then the puzzle, and states the bet by the end of the first
      paragraph (STORY_CRAFT S1, S2; QUESTION_RULES H3).
- [ ] The data key (pwm/SEALED or equivalent) is created only after the page is live.

## Checkpoint 1 -- analysis, charts and headline numbers
Goal: the numbers are right, reproducible, and scored honestly against the seal.
- [ ] THESIS.md was sealed in a commit that comes BEFORE the first commit reading the data.
- [ ] Fresh clone of the named commit: ./run_all.sh exit 0; git status clean after.
- [ ] Every md5 quoted in the hand-back matches.
- [ ] Each scored number recomputed by the checker from raw/ with the checker's
      own code (not the researcher's outputs), to the published precision.
- [ ] The checker reads each result's sign convention from the code before
      describing its direction in words.
- [ ] Every prediction scored against the sealed wording, verbatim, with its
      confidence at seal beside it.
- [ ] Failed predictions reported first in the hand-back.
- [ ] The weak-evidence sentence is next to the headline number.
- [ ] requirements.txt covers every import.
- [ ] Charts exist as SVG, each with a prefers-color-scheme block, written with LF line endings.
- [ ] Charts rendered at 390px and 1280px, light and dark, with no clipped text, no
      overlapping labels; no <text> outside the viewBox in DejaVu Sans incl. bold.
- [ ] Lead chart title states the finding; subtitle unit and period; one
      annotation marks the answer; no title implies a cause the design cannot
      license. (EXCELLENCE_PLAN E)
- [ ] Every chart caption says how to read it (STORY_CRAFT S8); groups that failed a
      design test are drawn muted, with no averages that invite a reading.
- [ ] The finding is under 60 characters and is supported by a number in RESULTS.md.
- [ ] Pure ASCII across the piece's folder.

## Checkpoint 2 -- draft article
Goal: a non-specialist can follow it, sees how the author thinks, and it says
nothing the data does not support.
- [ ] All Checkpoint 1 boxes still pass on the new commit.
- [ ] Reasoning spine, in order (EXCELLENCE_PLAN C): the argument (both sides at
      their strongest); pushed to the extreme; my bet with confidence and seal
      date; what the data said (one chart); where I was wrong; what would change
      my mind; the verdict in one line with the number; sources.
- [ ] Verdict card at the top: question, verdict, key number, confidence at seal,
      scored n of N, what would change it.
- [ ] Opens with a specimen (one real, dated case) and the puzzle within the
      first 60 words after the verdict card (STORY_CRAFT S1, S2).
- [ ] Editor's blind review done (office/EDITOR.md); its wording changes re-checked
      against the evidence by the checker.
- [ ] Section headings carry the finding after the spine label (S4).
- [ ] The named idea is shown through the example first, then named once in
      plain words, and added to the ideas page (S3).
- [ ] The reader's obvious objection is asked and answered (S5).
- [ ] Where the finding flips (a group, a period, a type), said with its numbers (S6).
- [ ] At most one compression line; every word in it is supported by RESULTS.md (S7).
- [ ] Ends by pointing to the next open question; links back to its own open
      question page (S9).
- [ ] None of R1-R7: no advice, no post-hoc flip presented as a finding, no
      one-sided evidence, no overclaim word (incl. causal verbs the design cannot
      license), no untranslated jargon, no engagement bait, no headline number
      without its cost (n, interval, drawdown).
- [ ] At least one other country that chose differently is in the piece (world view).
- [ ] 1,200 to 1,800 words of linear prose (count reported).
- [ ] Headline is the finding, under 60 characters, no jargon (QUESTION_RULES 4, 7).
- [ ] Every number in the prose is in the number manifest with its script, and the
      manifest audit passes.
- [ ] Every source cited opens to a file in raw/ listed in RETRIEVED.txt.
- [ ] No "we"; no em dash, U+2212 or U+00D7.
- [ ] Banned-word grep clean: choose, should, recommend, better option, you should.
- [ ] Not-advice line present; findings in past tense and by cohort.
- [ ] Front matter: draft: true, the agreed date, repo and dataset fields.
- [ ] Date not already used in content/economics/.
- [ ] Rendered through the real site at 390px and 1280px, light and dark.

## Checkpoint 3 -- ready to merge and publish
Goal: what ships is exactly what was checked.
- [ ] All Checkpoint 1 and 2 boxes pass on the PR head commit.
- [ ] PR diff contains only the intended paths (git diff --name-only origin/main...HEAD).
- [ ] A sealed branch is brought into main with a MERGE COMMIT (never squash or
      rebase); the seal and data-key commits are ancestors of main afterwards.
- [ ] run_all.sh at repo root rebuilds everything.
- [ ] Site build (Hugo) with the article passes; screenshots at 390px and desktop,
      light and dark, reviewed; future-dated post hidden until its date.
- [ ] Publish gate and prose linter pass as CI runs them.
- [ ] Scorecard updated on publication day in its own PR: outcomes, confidences,
      running calibration, and the open question page marked answered.
- [ ] Jacob has seen the question, the headline, the charts and the three numbers.

## Checker independence (how the Cowork checker stays unbiased)

What the checker does:
- Verifies from a fresh clone; never trusts a reported pass, md5 or number.
- Recomputes scored numbers from raw data with its own code.
- Tries to break things: corruption tests, sabotaged scripts, worst-case fonts.
- Discloses anything it has seen that bears on a sealed test, so the test can
  exclude it.
- Writes its rulings, with reasons, in reviews/, including when it reverses
  itself or accepts a researcher's correction of it.

Known limits, stated plainly:
- The checker and the researchers are the same family of model, so they can
  share blind spots. Mitigation: the Editor runs on a different model where
  possible; an outside reader reviews at least one piece per quarter; real
  readers test titles (reviews/READER_TESTS.md).
- The checker writes briefs and prompts, then checks work done to them: it is
  not independent of its own design choices. Mitigation: objective boxes above,
  and outside review of the design, not only the numbers.
- Judgements of prose and presentation are less objective than numbers.

Recorded lapse, 25 September 2026: on the ERP piece the checker moved two of
Jacob's confidences after a debate (T1 20 -> 35, T2 80 -> 65). His original
numbers would have scored a Brier of 0.153; the committed ones scored 0.194.
Rule since: the checker never proposes or adjusts a confidence number.
