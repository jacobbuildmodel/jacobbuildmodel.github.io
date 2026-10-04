# REPLY_FORMAT -- every hand-back to Jacob

Adopted 4 October 2026. Every hand-back to Jacob, from any chat working in this
repo, uses the block below and nothing else: 12 lines at most, no pasted diffs.
Details (what changed and why, full command output, screenshots, findings) go
in the PR body, where they stay with the change.

```
STATUS: done | blocked | needs Jacob
PR: #<n>   HEAD: <7-char sha>
CHANGED: <paths, comma separated>
CHECKS: <command> -> <result>
NEEDS JACOB: <one line, or "nothing">
```

Rules:
1. STATUS is exactly one of the three words given. "done" means every check
   below passed on HEAD; anything red is "blocked" (something stops the work)
   or "needs Jacob" (a decision only Jacob can make).
2. PR and HEAD name the pull request and the commit the checks ran on. HEAD
   is the pushed head of the PR branch, 7 characters.
3. CHANGED lists the paths in git diff --name-only origin/main...HEAD.
4. One CHECKS line per check, each with the command and its result: the Hugo
   build, Vale as lint.yml runs it, and each CI check the PR touches
   (aitell.py as deploy.yml and lint.yml run it, scripts/check_open_pages.py).
5. NEEDS JACOB is one line. If more than one thing is needed, the line points
   to the PR body section that lists them.
6. Pure ASCII. No em dash.
