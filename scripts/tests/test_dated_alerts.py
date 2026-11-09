#!/usr/bin/env python3
"""
Tests for scripts/dated_alerts.py. No network: the API is faked.
Standard library only (one test also uses PyYAML if installed).

    python -m unittest discover -s scripts/tests -v     # from the repo root

Covers Singapore time, lead days, duplicates, closing, the deploy alert
decision, the strict events reader, the real data/dated_events.yaml, and one
whole run against a fake API (what it would write, and that a dry run writes
nothing). CI runs these in .github/workflows/dated-alerts.yml before the
script itself.
"""
import datetime as dt
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import dated_alerts as da  # noqa: E402

D = dt.date
UTC = dt.timezone.utc


def ev(date, title="Thing", lead=2):
    return {"date": date, "title": title, "what": "Do it.",
            "lead_days": lead, "link": None}


class SingaporeTime(unittest.TestCase):

    def test_utc_evening_is_next_day_in_singapore(self):
        # 16:00 UTC on 11 Nov is 00:00 on 12 Nov in Singapore
        self.assertEqual(da.today_sgt(dt.datetime(2026, 11, 11, 16, 0, tzinfo=UTC)),
                         D(2026, 11, 12))

    def test_just_before_singapore_midnight(self):
        self.assertEqual(da.today_sgt(dt.datetime(2026, 11, 11, 15, 59, tzinfo=UTC)),
                         D(2026, 11, 11))

    def test_scheduled_run_time(self):
        # the cron, 00:05 UTC, is 08:05 the same day in Singapore
        self.assertEqual(da.today_sgt(dt.datetime(2026, 11, 12, 0, 5, tzinfo=UTC)),
                         D(2026, 11, 12))

    def test_late_scheduled_run_same_day(self):
        # GitHub can start the 00:05 run hours late; still the same day
        self.assertEqual(da.today_sgt(dt.datetime(2026, 11, 12, 6, 30, tzinfo=UTC)),
                         D(2026, 11, 12))

    def test_naive_datetime_refused(self):
        with self.assertRaises(ValueError):
            da.today_sgt(dt.datetime(2026, 11, 12, 0, 5))


class LeadDays(unittest.TestCase):

    def test_window_is_lead_days_through_the_date(self):
        e = ev(D(2026, 11, 12), lead=2)
        self.assertFalse(da.is_due(e, D(2026, 11, 9)))
        self.assertTrue(da.is_due(e, D(2026, 11, 10)))
        self.assertTrue(da.is_due(e, D(2026, 11, 11)))
        self.assertTrue(da.is_due(e, D(2026, 11, 12)))
        self.assertFalse(da.is_due(e, D(2026, 11, 13)))

    def test_zero_lead_days_is_the_day_only(self):
        e = ev(D(2026, 12, 1), lead=0)
        self.assertFalse(da.is_due(e, D(2026, 11, 30)))
        self.assertTrue(da.is_due(e, D(2026, 12, 1)))

    def test_window_crosses_month_end(self):
        e = ev(D(2026, 12, 1), lead=2)
        self.assertTrue(da.is_due(e, D(2026, 11, 29)))
        self.assertFalse(da.is_due(e, D(2026, 11, 28)))

    def test_default_lead_days_is_two(self):
        events = da.parse_events('- date: 2026-12-02\n  title: "T"\n  what: "W"\n')
        self.assertEqual(events[0]["lead_days"], 2)


class Duplicates(unittest.TestCase):

    def test_due_and_no_issue_opens(self):
        e = ev(D(2026, 11, 12))
        to_open, already = da.plan_opens([e], D(2026, 11, 11), [])
        self.assertEqual(to_open, [e])
        self.assertEqual(already, [])

    def test_existing_issue_is_left_alone(self):
        e = ev(D(2026, 11, 12))
        to_open, already = da.plan_opens([e], D(2026, 11, 11), [da.issue_title(e)])
        self.assertEqual(to_open, [])
        self.assertEqual(already, [e])

    def test_same_title_other_date_is_a_different_issue(self):
        e = ev(D(2026, 12, 1), title="Monthly source check")
        old = da.issue_title(ev(D(2026, 11, 1), title="Monthly source check"))
        to_open, _ = da.plan_opens([e], D(2026, 11, 30), [old])
        self.assertEqual(to_open, [e])

    def test_not_due_opens_nothing(self):
        to_open, already = da.plan_opens([ev(D(2026, 11, 12))], D(2026, 11, 4), [])
        self.assertEqual((to_open, already), ([], []))

    def test_duplicate_event_in_file_refused(self):
        text = ('- date: 2026-11-12\n  title: "T"\n  what: "W"\n'
                '- date: 2026-11-12\n  title: "T"\n  what: "W2"\n')
        with self.assertRaises(da.EventsError):
            da.parse_events(text)

    def test_body_states_the_lead(self):
        body = da.event_body(ev(D(2026, 11, 12), lead=2), D(2026, 11, 12))
        self.assertIn("(alerts start 2 day(s) before the date)", body)
        self.assertNotIn("ahead", body)

    def test_title_format(self):
        self.assertEqual(da.issue_title(ev(D(2026, 11, 12), "Merge day")),
                         "[Due 2026-11-12] Merge day")


class Closing(unittest.TestCase):

    def issue(self, title, n=1):
        return {"number": n, "title": title, "state": "open"}

    def test_closes_only_after_more_than_two_days(self):
        i = self.issue("[Due 2026-11-12] Merge day")
        self.assertEqual(da.plan_closes([i], D(2026, 11, 13)), [])
        self.assertEqual(da.plan_closes([i], D(2026, 11, 14)), [])
        self.assertEqual(da.plan_closes([i], D(2026, 11, 15)), [i])

    def test_ignores_titles_without_a_due_date(self):
        i = self.issue("Something Jacob labelled by hand")
        self.assertEqual(da.plan_closes([i], D(2027, 1, 1)), [])

    def test_ignores_impossible_dates(self):
        self.assertIsNone(da.due_from_title("[Due 2026-02-30] Nope"))

    def test_future_issue_stays_open(self):
        i = self.issue("[Due 2026-12-02] Pre-Budget")
        self.assertEqual(da.plan_closes([i], D(2026, 11, 30)), [])


class DeployAlert(unittest.TestCase):

    def run_(self, rid, conclusion, created, event="push", branch="main"):
        return {"id": rid, "status": "completed", "conclusion": conclusion,
                "created_at": created, "event": event, "head_branch": branch,
                "html_url": f"https://example.invalid/{rid}"}

    def alert(self, n, state, rid=None):
        body = da.RUN_MARK.format(rid) if rid else ""
        return {"number": n, "state": state, "title": da.ALERT_TITLE, "body": body}

    def test_latest_ignores_pull_requests_and_other_branches(self):
        runs = [self.run_(1, "success", "2026-11-03T00:30:00Z"),
                self.run_(2, "failure", "2026-11-04T01:00:00Z", event="pull_request"),
                self.run_(3, "failure", "2026-11-04T02:00:00Z", branch="feature"),
                {"id": 4, "status": "in_progress", "head_branch": "main",
                 "event": "push", "created_at": "2026-11-04T03:00:00Z"}]
        self.assertEqual(da.latest_deploy_run(runs)["id"], 1)

    def test_failure_opens(self):
        r = self.run_(9, "failure", "2026-11-04T00:30:00Z")
        self.assertEqual(da.deploy_action(r, []), ("open", None))

    def test_failure_with_open_alert_does_not_duplicate(self):
        r = self.run_(9, "failure", "2026-11-04T00:30:00Z")
        self.assertIsNone(da.deploy_action(r, [self.alert(5, "open")])[0])

    def test_failure_already_alerted_and_closed_by_hand_stays_closed(self):
        r = self.run_(9, "failure", "2026-11-04T00:30:00Z")
        self.assertIsNone(da.deploy_action(r, [self.alert(5, "closed", rid=9)])[0])

    def test_new_failure_after_closed_alert_opens_again(self):
        r = self.run_(10, "failure", "2026-11-05T00:30:00Z")
        self.assertEqual(da.deploy_action(r, [self.alert(5, "closed", rid=9)])[0], "open")

    def test_success_closes_open_alert(self):
        r = self.run_(11, "success", "2026-11-05T01:30:00Z")
        a = self.alert(5, "open", rid=9)
        self.assertEqual(da.deploy_action(r, [a]), ("close", [a]))

    def test_cancelled_changes_nothing(self):
        r = self.run_(12, "cancelled", "2026-11-05T01:30:00Z")
        self.assertIsNone(da.deploy_action(r, [self.alert(5, "open")])[0])


class EventsReader(unittest.TestCase):

    def test_real_file_parses(self):
        # Only what holds for any valid file, so adding or removing an event
        # never fails the tests (the daily job runs them before acting).
        events = da.parse_events((ROOT / "data" / "dated_events.yaml").read_text("utf-8"))
        self.assertGreaterEqual(len(events), 1)
        for e in events:
            self.assertIsInstance(e["date"], dt.date)
            self.assertTrue(0 <= e["lead_days"] <= da.MAX_LEAD_DAYS)
            self.assertTrue(e["title"].strip())
            self.assertTrue(e["what"].strip())

    def test_real_file_matches_a_full_yaml_parser(self):
        # Hugo also parses data/*.yaml, so the file must be standard YAML and
        # read the same both ways. Skipped where PyYAML is not installed.
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        text = (ROOT / "data" / "dated_events.yaml").read_text("utf-8")
        ours = da.parse_events(text)
        theirs = yaml.safe_load(text)
        self.assertEqual(len(ours), len(theirs))
        for a, b in zip(ours, theirs):
            self.assertEqual(a["date"], b["date"])
            self.assertEqual(a["title"], b["title"])
            self.assertEqual(a["what"], b["what"])
            self.assertEqual(a["lead_days"], b.get("lead_days", 2))
            self.assertEqual(a["link"], b.get("link"))

    def test_unquoted_title_refused(self):
        with self.assertRaises(da.EventsError):
            da.parse_events("- date: 2026-11-12\n  title: Merge day: x\n  what: \"W\"\n")

    def test_unknown_key_refused(self):
        with self.assertRaises(da.EventsError):
            da.parse_events('- date: 2026-11-12\n  title: "T"\n  what: "W"\n  when: "x"\n')

    def test_bad_date_refused(self):
        for bad in ("2026-11-31", "12/11/2026", "2026-1-2"):
            with self.assertRaises(da.EventsError, msg=bad):
                da.parse_events(f'- date: {bad}\n  title: "T"\n  what: "W"\n')

    def test_missing_what_refused(self):
        with self.assertRaises(da.EventsError):
            da.parse_events('- date: 2026-11-12\n  title: "T"\n')

    def test_bad_lead_days_refused(self):
        for bad in ("-1", "two", "61"):
            with self.assertRaises(da.EventsError, msg=bad):
                da.parse_events(f'- date: 2026-11-12\n  title: "T"\n  what: "W"\n  lead_days: {bad}\n')

    def test_non_https_link_refused(self):
        with self.assertRaises(da.EventsError):
            da.parse_events('- date: 2026-11-12\n  title: "T"\n  what: "W"\n  link: "http://x"\n')

    def test_comments_and_crlf_ok(self):
        text = '# c\r\n- date: 2026-11-12\r\n  # c\r\n  title: "T"\r\n  what: "W"\r\n'
        self.assertEqual(len(da.parse_events(text)), 1)


class FakeGitHub(da.GitHub):
    """Records write calls instead of sending them; serves canned reads."""

    def __init__(self, issues, runs, dry_run=False, comments=None):
        super().__init__("o/r", "t", dry_run)
        self._issues, self._runs, self.calls = issues, runs, []
        self._comments = comments or {}

    def request(self, method, path, data=None, query=None):
        if method == "GET" and path.endswith("/comments"):
            n = int(path.split("/")[2])
            return self._comments.get(n, []) if query["page"] == 1 else []
        if method == "GET" and path == "/issues":
            st, lab = query["state"], query["labels"]
            return [i for i in self._issues if lab in i["labels"]
                    and (st == "all" or i["state"] == st)] if query["page"] == 1 else []
        if method == "GET" and path.startswith("/labels/"):
            return {}
        if method == "GET" and path == "/actions/workflows":
            return {"workflows": [{"id": 1, "name": da.DEPLOY_WORKFLOW}]}
        if method == "GET":
            return {"workflow_runs": self._runs}
        self.calls.append((method, path, data))
        return {}


class WholeRun(unittest.TestCase):
    """run() end to end against a fake API, quietly."""

    EVENTS = [ev(D(2026, 11, 12), "Merge day"), ev(D(2026, 11, 14), "Pub day")]
    OK = [{"id": 7, "status": "completed", "conclusion": "success", "event": "push",
           "head_branch": "main", "created_at": "2026-11-11T00:30:00Z", "html_url": "u"}]

    def go(self, today, issues, runs=None, dry_run=False, comments=None):
        import contextlib, io
        gh = FakeGitHub(issues, runs if runs is not None else self.OK, dry_run,
                        comments)
        with contextlib.redirect_stdout(io.StringIO()):
            da.run(self.EVENTS, today, gh, "jacobbuildmodel")
        return gh.calls

    def test_opens_assigned_and_labelled(self):
        calls = self.go(D(2026, 11, 11), [])
        self.assertEqual(len(calls), 1)
        method, path, data = calls[0]
        self.assertEqual((method, path), ("POST", "/issues"))
        self.assertEqual(data["title"], "[Due 2026-11-12] Merge day")
        self.assertEqual(data["labels"], ["dated-event"])
        self.assertEqual(data["assignees"], ["jacobbuildmodel"])

    def test_second_run_same_day_opens_nothing(self):
        existing = [{"number": 3, "title": "[Due 2026-11-12] Merge day",
                     "state": "open", "labels": "dated-event"}]
        self.assertEqual(self.go(D(2026, 11, 11), existing), [])

    def test_closes_past_with_comment(self):
        existing = [{"number": 3, "title": "[Due 2026-11-12] Merge day",
                     "state": "open", "labels": "dated-event"},
                    {"number": 4, "title": "[Due 2026-11-14] Pub day",
                     "state": "closed", "labels": "dated-event"}]
        calls = self.go(D(2026, 11, 15), existing)
        self.assertEqual([(m, p) for m, p, _ in calls],
                         [("POST", "/issues/3/comments"), ("PATCH", "/issues/3")])
        self.assertEqual(calls[1][2], {"state": "closed"})
        body = calls[0][2]["body"]
        self.assertIn(da.CLOSE_MARK, body)
        self.assertIn("If it still needs doing, reopen it; the daily check will "
                      "leave it open.", body)

    def test_reopened_after_auto_close_is_left_open(self):
        # Run 1 closes #3 with the auto-close comment; Jacob reopens it; run 2
        # (and every later run) must leave it open.
        issue = {"number": 3, "title": "[Due 2026-11-12] Merge day",
                 "state": "open", "labels": "dated-event"}
        first = self.go(D(2026, 11, 15), [issue])
        comment = first[0][2]["body"]
        later = self.go(D(2026, 11, 16), [issue],
                        comments={3: [{"body": "done?"}, {"body": comment}]})
        self.assertEqual(later, [])

    def test_other_comments_do_not_block_closing(self):
        issue = {"number": 3, "title": "[Due 2026-11-12] Merge day",
                 "state": "open", "labels": "dated-event"}
        calls = self.go(D(2026, 11, 15), [issue],
                        comments={3: [{"body": "Closed automatically? not yet"}]})
        self.assertEqual(calls[-1], ("PATCH", "/issues/3", {"state": "closed"}))

    def test_reopened_deploy_alert_is_left_open(self):
        alert = {"number": 5, "title": da.ALERT_TITLE, "state": "open",
                 "labels": "deploy-alert", "body": da.RUN_MARK.format(8)}
        mark = da.close_comment("Closed automatically by dated-alerts: x.")
        self.assertEqual(self.go(D(2026, 11, 4), [alert],
                                 comments={5: [{"body": mark}]}), [])
        # without the earlier auto-close comment it is closed as usual
        self.assertEqual(self.go(D(2026, 11, 4), [alert])[-1],
                         ("PATCH", "/issues/5", {"state": "closed"}))

    def test_failed_deploy_opens_alert(self):
        runs = [dict(self.OK[0], id=8, conclusion="failure")]
        calls = self.go(D(2026, 11, 4), [], runs)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][2]["title"], da.ALERT_TITLE)
        self.assertIn(da.RUN_MARK.format(8), calls[0][2]["body"])

    def test_dry_run_writes_nothing(self):
        runs = [dict(self.OK[0], id=8, conclusion="failure")]
        self.assertEqual(self.go(D(2026, 11, 11), [], runs, dry_run=True), [])


if __name__ == "__main__":
    unittest.main()
