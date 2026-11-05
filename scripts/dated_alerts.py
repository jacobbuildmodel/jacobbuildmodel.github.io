#!/usr/bin/env python3
"""
dated_alerts.py -- turn dated events into GitHub issues, so a date that matters
reaches Jacob's inbox even when no chat is running.

Usage:
    python scripts/dated_alerts.py --dry-run                     # print, change nothing
    python scripts/dated_alerts.py --dry-run --today 2026-11-11  # as if it were that day
    python scripts/dated_alerts.py                               # act (in CI)

No dependencies beyond the Python 3.8+ standard library. Run from the repo
root. Reads data/dated_events.yaml (format described in that file's header).
Talks to the GitHub REST API with GITHUB_TOKEN; the repository comes from
GITHUB_REPOSITORY or --repo.

What one run does, with "today" as the calendar date in Singapore (UTC+8):

1. Due events. For each event with date - lead_days <= today <= date, open
   one issue titled "[Due YYYY-MM-DD] <title>", labelled dated-event and
   assigned to the repository owner (GitHub emails the assignee). If an issue
   with that exact title already exists, open or closed, it is left alone:
   one issue per event, and closing it early means "done", not "remind me
   again tomorrow".
2. Past events. Every open dated-event issue whose title date is more than
   2 days before today is closed with a comment, unless it already carries
   this script's auto-close comment: that means it was closed once and Jacob
   reopened it on purpose, so it is left open from then on.
3. Deploy alert. If the most recent completed run of the "Deploy site to
   GitHub Pages" workflow on main (pull request runs left out) concluded
   "failure", open "[Alert] Latest deploy on main failed" (label deploy-alert)
   unless one is open, or one, open or closed, already names that run. If the
   most recent completed run succeeded, close any open alert with a comment
   (again, not one that was auto-closed before and reopened). Any other
   conclusion (cancelled, skipped) changes nothing.

--dry-run makes no write calls. It still reads issues and runs from the API
(unauthenticated works for a public repo); if a read fails it says so and
carries on as if nothing existed. A real run stops with exit 1 on any API
error, so GitHub's own failed-workflow email is the alert of last resort.

Exit codes: 0 ok, 1 API error (real run), 2 bad events file or arguments.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SGT = dt.timezone(dt.timedelta(hours=8), "SGT")
EVENTS = Path("data/dated_events.yaml")
LABEL = "dated-event"
LABEL_COLOR = "d93f0b"
ALERT_LABEL = "deploy-alert"
ALERT_COLOR = "b60205"
ALERT_TITLE = "[Alert] Latest deploy on main failed"
DEPLOY_WORKFLOW = "Deploy site to GitHub Pages"
DEPLOY_BRANCH = "main"
DEFAULT_LEAD_DAYS = 2
MAX_LEAD_DAYS = 60
CLOSE_AFTER_DAYS = 2
API = "https://api.github.com"

KEYS = ("date", "title", "what", "lead_days", "link")
REQUIRED = ("date", "title", "what")
TITLE_RE = re.compile(r"^\[Due (\d{4}-\d{2}-\d{2})\] ")
RUN_MARK = "<!-- dated-alerts deploy run_id: {} -->"
CLOSE_MARK = "<!-- dated-alerts auto-close -->"
REOPEN_LINE = "If it still needs doing, reopen it; the daily check will leave it open."


class EventsError(ValueError):
    """The events file is not in the one shape this script reads."""


# --------------------------------------------------------------------------
# Pure logic (unit-tested in scripts/tests/test_dated_alerts.py)
# --------------------------------------------------------------------------

def today_sgt(now=None):
    """The calendar date in Singapore. `now` is an aware datetime (for tests);
    default is the current time."""
    now = now or dt.datetime.now(dt.timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    return now.astimezone(SGT).date()


def _value(raw, key, lineno):
    raw = raw.strip()
    if raw.startswith('"'):
        try:
            val = json.loads(raw)
        except ValueError:
            raise EventsError(f"line {lineno}: {key}: bad double-quoted string")
        if not isinstance(val, str):
            raise EventsError(f"line {lineno}: {key}: expected a string")
        return val
    if key in ("date", "lead_days"):
        return raw
    raise EventsError(f"line {lineno}: {key}: value must be double-quoted")


def parse_events(text):
    """Read the events file. A strict reader for one shape: a top-level list
    of flat mappings, '- key: value' then '  key: value', full-line comments
    only. Anything else raises EventsError, so a typo stops the run instead of
    silently dropping an event."""
    items = []
    current = None
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.rstrip("\r")
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith("- "):
            current = {"_line": lineno}
            items.append(current)
            body = line[2:]
        elif line.startswith("  ") and not line.startswith("   "):
            if current is None:
                raise EventsError(f"line {lineno}: key outside an event")
            body = line[2:]
        else:
            raise EventsError(f"line {lineno}: unexpected indentation or text")
        key, sep, raw = body.partition(":")
        key = key.strip()
        if not sep or key not in KEYS:
            raise EventsError(f"line {lineno}: unknown key {key!r}")
        if key in current:
            raise EventsError(f"line {lineno}: {key} given twice")
        current[key] = _value(raw, key, lineno)

    events = []
    seen = set()
    for item in items:
        where = f"event at line {item['_line']}"
        for key in REQUIRED:
            if not item.get(key):
                raise EventsError(f"{where}: missing {key}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", item["date"]):
            raise EventsError(f"{where}: date must be YYYY-MM-DD")
        try:
            date = dt.date.fromisoformat(item["date"])
        except ValueError:
            raise EventsError(f"{where}: {item['date']} is not a real date")
        lead = item.get("lead_days", str(DEFAULT_LEAD_DAYS))
        if not re.fullmatch(r"\d+", lead) or int(lead) > MAX_LEAD_DAYS:
            raise EventsError(f"{where}: lead_days must be 0..{MAX_LEAD_DAYS}")
        for key in ("title", "what"):
            if "\n" in item[key] or item[key] != item[key].strip():
                raise EventsError(f"{where}: {key} must be one trimmed line")
        link = item.get("link")
        if link is not None and not link.startswith("https://"):
            raise EventsError(f"{where}: link must start with https://")
        event = {"date": date, "title": item["title"], "what": item["what"],
                 "lead_days": int(lead), "link": link}
        title = issue_title(event)
        if title in seen:
            raise EventsError(f"{where}: duplicate of an earlier event: {title}")
        seen.add(title)
        events.append(event)
    return events


def issue_title(event):
    return f"[Due {event['date'].isoformat()}] {event['title']}"


def due_from_title(title):
    """The date in a "[Due YYYY-MM-DD] ..." title, or None."""
    m = TITLE_RE.match(title)
    if not m:
        return None
    try:
        return dt.date.fromisoformat(m.group(1))
    except ValueError:
        return None


def alert_starts(event):
    return event["date"] - dt.timedelta(days=event["lead_days"])


def is_due(event, today):
    """True from lead_days before the date through the date itself."""
    return alert_starts(event) <= today <= event["date"]


def plan_opens(events, today, existing_titles):
    """Events to open an issue for: due today and no issue (any state) with
    the same title. Returns (to_open, already) lists of events."""
    existing = set(existing_titles)
    to_open, already = [], []
    for e in events:
        if not is_due(e, today):
            continue
        (already if issue_title(e) in existing else to_open).append(e)
    return to_open, already


def is_past(title, today):
    due = due_from_title(title)
    return due is not None and (today - due).days > CLOSE_AFTER_DAYS


def plan_closes(open_issues, today):
    """Open dated-event issues whose date is more than CLOSE_AFTER_DAYS past."""
    return [i for i in open_issues if is_past(i["title"], today)]


def was_auto_closed(comments):
    """True if any comment is this script's auto-close comment. An open issue
    carrying one was reopened by hand after an auto-close; never close it
    again."""
    return any(CLOSE_MARK in (c.get("body") or "") for c in comments)


def close_comment(text):
    """An auto-close comment: the reason, the reopen line, the hidden mark."""
    return f"{text} {REOPEN_LINE}\n\n{CLOSE_MARK}"


def latest_deploy_run(runs, branch=DEPLOY_BRANCH):
    """The most recent completed, non-pull-request run on `branch`."""
    done = [r for r in runs
            if r.get("status") == "completed"
            and r.get("head_branch") == branch
            and r.get("event") != "pull_request"]
    done.sort(key=lambda r: (r.get("created_at") or "", r.get("id") or 0),
              reverse=True)
    return done[0] if done else None


def deploy_action(run, alert_issues):
    """Decide what to do about the deploy alert.

    run          the latest completed deploy run on main, or None
    alert_issues deploy-alert issues (any state) with ALERT_TITLE
    Returns ("open", None), ("close", [issues]) or (None, reason)."""
    open_alerts = [i for i in alert_issues if i.get("state") == "open"]
    if run is None:
        return None, "no completed deploy run on main found"
    conclusion = run.get("conclusion")
    if conclusion == "failure":
        if open_alerts:
            return None, f"alert already open (#{open_alerts[0]['number']})"
        mark = RUN_MARK.format(run.get("id"))
        for i in alert_issues:
            if mark in (i.get("body") or ""):
                return None, f"run already alerted in #{i['number']} (closed)"
        return "open", None
    if conclusion == "success":
        if open_alerts:
            return "close", open_alerts
        return None, "latest deploy succeeded, no alert open"
    return None, f"latest deploy concluded {conclusion!r}, no change"


def event_body(event, today):
    lines = [
        f"**Due:** {event['date'].isoformat()} (Singapore time)",
        "",
        f"**What must happen:** {event['what']}",
    ]
    if event.get("link"):
        lines += ["", f"**Link:** {event['link']}"]
    lines += [
        "",
        "---",
        f"Opened {today.isoformat()} by `.github/workflows/dated-alerts.yml` from "
        "`data/dated_events.yaml` "
        f"(alerts start {event['lead_days']} day(s) before the date). Close it "
        "when done; it will not "
        f"be reopened. Still open {CLOSE_AFTER_DAYS} days after the date, it is "
        "closed automatically.",
    ]
    return "\n".join(lines)


def deploy_body(run):
    return "\n".join([
        f"The most recent completed run of \"{DEPLOY_WORKFLOW}\" on "
        f"`{DEPLOY_BRANCH}` concluded **failure**, so the live site may be "
        "behind main.",
        "",
        f"- Run: {run.get('html_url')}",
        f"- Trigger: {run.get('event')}",
        f"- Started: {run.get('created_at')}",
        "",
        "Fix and re-run the workflow (Actions tab, Run workflow). This issue "
        "closes itself on the next daily check after a later run succeeds.",
        "",
        RUN_MARK.format(run.get("id")),
    ])


# --------------------------------------------------------------------------
# GitHub REST API (standard library only)
# --------------------------------------------------------------------------

class GitHub:
    def __init__(self, repo, token, dry_run):
        self.repo = repo
        self.token = token
        self.dry_run = dry_run

    def request(self, method, path, data=None, query=None):
        url = f"{API}/repos/{self.repo}{path}"
        if query:
            url += "?" + urllib.parse.urlencode(query)
        body = json.dumps(data).encode() if data is not None else None
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", "dated-alerts")
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        if body is not None:
            req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
        return json.loads(raw) if raw else None

    def write(self, method, path, data, describe):
        print(("  would " if self.dry_run else "  ") + describe)
        if self.dry_run:
            return None
        return self.request(method, path, data)

    def issues(self, label, state):
        out = []
        for page in range(1, 11):
            batch = self.request("GET", "/issues", query={
                "labels": label, "state": state, "per_page": 100, "page": page})
            out += [i for i in batch if "pull_request" not in i]
            if len(batch) < 100:
                break
        return out

    def ensure_label(self, name, color, description):
        try:
            self.request("GET", "/labels/" + urllib.parse.quote(name))
            return
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
        self.write("POST", "/labels", {"name": name, "color": color,
                                        "description": description},
                   f"create label {name}")

    def open_issue(self, title, body, label, assignee):
        data = {"title": title, "body": body, "labels": [label]}
        if assignee:
            data["assignees"] = [assignee]
        try:
            return self.write("POST", "/issues", data,
                              f"OPEN  {title}  (label {label}, assignee {assignee})")
        except urllib.error.HTTPError as e:
            if e.code != 422 or not assignee:
                raise
            print(f"  assignee {assignee} refused (422); opening unassigned")
            data.pop("assignees")
            return self.request("POST", "/issues", data)

    def comments(self, number):
        out = []
        for page in range(1, 11):
            batch = self.request("GET", f"/issues/{number}/comments",
                                 query={"per_page": 100, "page": page})
            out += batch
            if len(batch) < 100:
                break
        return out

    def close_issue(self, issue, comment):
        n = issue["number"]
        self.write("POST", f"/issues/{n}/comments", {"body": comment},
                   f"comment on #{n}")
        self.write("PATCH", f"/issues/{n}", {"state": "closed"},
                   f"CLOSE #{n}  {issue['title']}")

    def deploy_runs(self):
        wfs = self.request("GET", "/actions/workflows",
                           query={"per_page": 100}).get("workflows", [])
        match = [w for w in wfs if w.get("name") == DEPLOY_WORKFLOW]
        if not match:
            raise RuntimeError(f"workflow {DEPLOY_WORKFLOW!r} not found")
        return self.request(
            "GET", f"/actions/workflows/{match[0]['id']}/runs",
            query={"branch": DEPLOY_BRANCH, "status": "completed",
                   "per_page": 20}).get("workflow_runs", [])


# --------------------------------------------------------------------------
# One run
# --------------------------------------------------------------------------

def read_or_empty(gh, what, fn):
    """In a dry run a failed read is reported and treated as empty; in a real
    run it propagates."""
    try:
        return fn()
    except (urllib.error.URLError, RuntimeError, ValueError) as e:
        if not gh.dry_run:
            raise
        print(f"  note: could not read {what} ({e}); assuming none")
        return None


def reopened(gh, issue):
    """Print and return True if `issue` was auto-closed before and reopened."""
    comments = read_or_empty(gh, f"comments on #{issue['number']}",
                             lambda: gh.comments(issue["number"])) or []
    if was_auto_closed(comments):
        print(f"  keep  #{issue['number']}  {issue['title']}  "
              "(reopened after an auto-close; left open)")
        return True
    return False


def run(events, today, gh, owner):
    mode = "DRY RUN, no changes" if gh.dry_run else "live"
    print(f"dated-alerts: {gh.repo}, today {today.isoformat()} (Singapore), {mode}")

    print("Events:")
    if not gh.dry_run:
        gh.ensure_label(LABEL, LABEL_COLOR, "Opened by dated-alerts before a dated event")
    all_issues = read_or_empty(gh, "dated-event issues",
                               lambda: gh.issues(LABEL, "all")) or []
    by_title = {i["title"]: i for i in all_issues}
    to_open, _ = plan_opens(events, today, by_title)
    for e in events:
        t = issue_title(e)
        if e in to_open:
            gh.open_issue(t, event_body(e, today), LABEL, owner)
        elif is_due(e, today):
            i = by_title[t]
            print(f"  keep  {t}  (already #{i['number']}, {i['state']})")
        elif today < alert_starts(e):
            print(f"  wait  {t}  (alerts from {alert_starts(e).isoformat()})")
        else:
            print(f"  past  {t}")

    print("Closing past events:")
    open_issues = [i for i in all_issues if i.get("state") == "open"]
    closes = plan_closes(open_issues, today)
    for i in closes:
        if reopened(gh, i):
            continue
        due = due_from_title(i["title"])
        gh.close_issue(i, close_comment(
            f"Closed automatically by dated-alerts: the due date {due.isoformat()} "
            f"passed more than {CLOSE_AFTER_DAYS} days ago (today is "
            f"{today.isoformat()}, Singapore time)."))
    if not closes:
        print("  nothing to close")

    print("Deploy on main:")
    runs = read_or_empty(gh, "deploy runs", gh.deploy_runs)
    latest = latest_deploy_run(runs or [])
    if latest:
        print(f"  latest completed run {latest.get('id')} ({latest.get('event')}, "
              f"{latest.get('created_at')}): {latest.get('conclusion')}")
    alerts = read_or_empty(gh, "deploy-alert issues",
                           lambda: gh.issues(ALERT_LABEL, "all")) or []
    alerts = [i for i in alerts if i["title"] == ALERT_TITLE]
    action, info = deploy_action(latest, alerts)
    if action == "open":
        if not gh.dry_run:
            gh.ensure_label(ALERT_LABEL, ALERT_COLOR,
                            "Opened by dated-alerts when the deploy on main fails")
        gh.open_issue(ALERT_TITLE, deploy_body(latest), ALERT_LABEL, owner)
    elif action == "close":
        for i in info:
            if reopened(gh, i):
                continue
            gh.close_issue(i, close_comment(
                f"Closed automatically by dated-alerts: a later deploy run on "
                f"{DEPLOY_BRANCH} succeeded ({latest.get('html_url')})."))
    else:
        print(f"  no action: {info}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--events", default=str(EVENTS), help="events file")
    ap.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"),
                    help="owner/name (default: $GITHUB_REPOSITORY)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would happen, write nothing")
    ap.add_argument("--today", help="YYYY-MM-DD, pretend it is this day in "
                                    "Singapore (only with --dry-run)")
    args = ap.parse_args(argv)

    if not args.repo or "/" not in args.repo:
        ap.error("--repo owner/name is required when GITHUB_REPOSITORY is unset")
    if args.today:
        if not args.dry_run:
            ap.error("--today only works with --dry-run")
        try:
            today = dt.date.fromisoformat(args.today)
        except ValueError:
            ap.error("--today must be YYYY-MM-DD")
    else:
        today = today_sgt()

    try:
        events = parse_events(Path(args.events).read_text(encoding="utf-8"))
    except (OSError, EventsError) as e:
        print(f"FAIL {args.events}: {e}", file=sys.stderr)
        return 2

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token and not args.dry_run:
        print("FAIL GITHUB_TOKEN is not set (use --dry-run to preview)",
              file=sys.stderr)
        return 2
    gh = GitHub(args.repo, token, args.dry_run)
    try:
        run(events, today, gh, args.repo.split("/")[0])
    except (urllib.error.URLError, RuntimeError, ValueError) as e:
        detail = ""
        if isinstance(e, urllib.error.HTTPError):
            detail = " " + e.read().decode("utf-8", "replace")[:300]
        print(f"FAIL GitHub API: {e}{detail}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
