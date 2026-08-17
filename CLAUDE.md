# CLAUDE.md — DRIVE v2 Automation Project

You are operating the DRIVE v2 equity-screening system for Jacob, a Singapore-based
active investor with NO coding background. He talks to you in plain English. You do ALL
the technical work (installing tools, running Python, editing files). Never ask him to
run a command himself — you run it.

## WHAT'S IN THIS FOLDER
- `DRIVE_v2_Cell2_v19_3.py` — the screening engine (the "Colab code"). It fetches market
  data (yfinance), computes RSI/OBV/scores, and prints 10 ranked output tables.
- `custom_instructions_v20.md` — the DRIVE framework (scoring rules, gates, exit rubric,
  decisiveness mandate, evaluate-protocol, auto-add). This governs all judgment.
- This file (CLAUDE.md) — how you operate.

## FIRST-TIME SETUP (do this automatically when asked to "set up")
1. Check whether Python 3 is installed (`python3 --version`). If not, install it (Homebrew
   on macOS, the official installer on Windows). Tell Jacob in one plain sentence what
   you're doing; don't make him decide technical details.
2. Install the screen's libraries:
   `pip install yfinance pandas pandas_ta requests numpy lxml --break-system-packages`
   (drop `--break-system-packages` if it errors on his platform).
3. Do a test run of the screen on a 3-ticker subset to confirm data fetches work.
4. Report "Setup done — ready for the weekly run" in one line.

## THE WEEKLY RUN (when Jacob says "run the weekly screen")
1. Run `python3 DRIVE_v2_Cell2_v19_3.py` and capture the full output.
2. Show him Output 1 (Entry Priority), Output 8 (Actions Required), Output 9 (Deployment
   Queue), and Output 10 (Catalyst Calendar) — these are the decision tables.
3. THEN, only if he asks for analysis, apply `custom_instructions_v20.md` and produce the
   ACTIONS REQUIRED for the $500K book per the Output Spec (action-first, ranked, sized,
   sequenced, conviction-labelled, with the gate-completion stamp and one disclaimer footer).
4. If a yfinance ticker fails to download, note it and continue — do not halt the whole run.

## MAINTAINING PORTFOLIO / WATCHLIST STATE (the auto-add mechanism)
- The `.py` file is the SOURCE OF TRUTH for holdings. The editable block is at the top:
  the `PORTFOLIO`, `WATCHLIST`, and `CATALYST_CALENDAR` dictionaries (clearly marked
  "EDIT ONLY THIS SECTION").
- When Jacob approves a name for the portfolio or watchlist (or an `evaluate [ticker]`
  verdict approves one), you edit the relevant dict DIRECTLY — no permission needed. Add
  the line with score, role/tier, weight, sector-ETF benchmark, and a one-line entry note.
- When a name is exited/trimmed per the Exit Rubric, remove or re-weight its line.
- EVERY time you edit the file: (a) bump the version number in the header, (b) add a
  one-line CHANGELOG entry at the top, (c) re-run `python3 -m py_compile` to confirm it
  still compiles before telling him it's done. Never hand back a file that doesn't compile.
- Keep a running "PENDING CHANGES" note in your reply so nothing is silently dropped.

## EVALUATE A STOCK (when Jacob says "evaluate [TICKER]")
Run the full Evaluation Protocol from `custom_instructions_v20.md` Section 6: the reordered
gates, T1/T2 quality, the five lenses, T3/T4, the MANDATORY bear thesis, the disruptor
check, the verdict block, and the gate-completion stamp. If approved, auto-add per above.
Use web search for current financials — do NOT score from memory.

## HARD RULES
- VERIFY every dollar figure / contract / statistic against a primary source before it
  touches a score. Weekly briefs have repeatedly contained FABRICATED numbers (e.g. a
  "$95.9M RCAT award" that was really $742K). Flag fabrications explicitly.
- You run the deterministic SCREEN and maintain FILES. Final trading decisions are Jacob's.
  Always end portfolio output with one "not financial advice" line.
- Never fabricate market data. If a fetch fails, say so.
- Keep replies tight and copy-paste-ready. Tables for rankings. Surface the uncomfortable
  finding. No threaded hedging.
- Token discipline: the screen run itself is cheap. Heavy analysis is what consumes tokens.
  Keep separate tasks in separate sessions; don't let one conversation balloon.
