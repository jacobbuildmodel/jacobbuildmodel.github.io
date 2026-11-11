---
title: "For low-paid gardeners, the floor became the pay"
question: "Minimum wage or the Progressive Wage Model: which actually lifts Singapore's lowest pay?"
date: 2026-10-31
draft: true
showToc: false
searchHidden: true
robotsNoIndex: true
summary: "Singapore has no minimum wage; it gave cleaners, security guards and landscape workers wage ladders instead. For landscape workers, pay at the bottom pulled about a quarter ahead of comparable jobs once the ladder bound, and at the one-in-four mark it sat exactly on the ladder's first rung. For cleaners and guards, pay was already moving before their ladders, so the record cannot say."
repo: "https://github.com/jacobbuildmodel/coe-analysis/tree/main/pwm"
# Type lab (draft pull request 64). A test page, never published: draft stays
# true. The title, question, summary and method strip above and the text
# below are copied from /economics/2026-10-31/ and /scorecard/ so the three
# typeface options are judged on the site's real words.
thesisSealed: "28 September 2026"
testsPassed: 3
testsFailed: 1
testsOther: 0
testsTotal: 4
---

<style>
.lab-bar { position: fixed; left: 0; right: 0; bottom: 0; z-index: 50; padding: 6px 12px calc(6px + env(safe-area-inset-bottom)); background: var(--surface); border-top: 2px solid var(--ink); font-family: var(--font-sans); font-size: 13px; line-height: 16px; color: var(--ink); }
.lab-bar-in { max-width: 660px; margin: 0 auto; display: grid; grid-template-columns: auto 1fr; gap: 5px 10px; align-items: center; }
.lab-bar b { font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; font-size: 11px; color: var(--ink-3); }
.lab-set { display: flex; gap: 6px; }
.lab-set button { flex: 1 1 0; min-height: 32px; padding: 2px 4px; border: 1px solid var(--line); border-radius: 4px; background: var(--paper); color: var(--ink); font: inherit; cursor: pointer; }
.lab-set button[aria-pressed="true"] { background: var(--navy); border-color: var(--navy); color: #ffffff; font-weight: 600; }
.lab-note { font-family: var(--font-sans); font-size: 14px; line-height: 1.45; color: var(--ink-3); border: 1px dashed var(--line); border-radius: 4px; padding: 10px 12px; }
.lab-end { height: 200px; }
</style>

<p class="lab-note">Type lab, a test page that is never published. The words are from the 31 October piece and the scorecard. The bar at the bottom of the screen switches the typeface, the page colour and the heading mark; the pick is remembered, so every other page of this local build shows it too. Option A is the site as it is.</p>

In June 2017, one in four of Singapore's landscape workers earned a basic wage
of S$1,300 a month or less, and at that mark pay sat exactly on the first rung
of the wage ladder written into the rules for registered landscape firms a year
earlier. In June 2018 the mark was S$1,300 again. By June 2022 the rung had
risen to S$1,550, and so had pay at the mark: S$1,550, to the dollar.

In September I wrote down four bets on what the public wage survey would show,
with how sure I was of each, and put them on an
[open question page](/open/2026-09-28-minimum-wage-or-pwm/) before opening the
data. Three held. This is what they found, where I was wrong, and the part of
the question public data cannot reach.

## The argument: one floor for everyone, or a ladder for each job

Singapore has no minimum wage. From 2014 it put wage ladders, a floor for each
step up in skill, into the licences of cleaning firms and security agencies,
and into the registration of landscape firms. The measure here is pay at the
bottom of each job: the 25th percentile of monthly wages in the Ministry of
Manpower's June Occupational Wage Survey, the pay at the one-in-four mark,
which a quarter of workers earn or less.

### How the count stands

| Piece | Held | Failed | Neither |
|---|---|---|---|
| Minimum wage or PWM | 3 | 1 | 0 |
| COE or ERP | 1 | 2 | 1 |
| HDB loan vs bank loan | 5 | 3 | 0 |
| HDB affordability | 3 | 2 | 4 |
| GST rises | 1 | 4 | 1 |
| **Total** | **13** | **12** | **6** |

## Sources

Landscape workers' bottom pay rose 24.6 per cent more than in low-paid jobs
without a ladder (90 per cent interval 17.1 to 32.6). Of 31 sealed
predictions, 13 held, 12 failed, and 6 landed in between.

<div class="lab-end"></div>

<div class="lab-bar" id="lab-bar" hidden>
<div class="lab-bar-in">
<b>Type</b><div class="lab-set" data-key="type"><button type="button" data-v="a">A Source</button><button type="button" data-v="b">B Newsreader</button><button type="button" data-v="c">C Playfair</button></div>
<b>Page</b><div class="lab-set" data-key="paper"><button type="button" data-v="a">White</button><button type="button" data-v="b">Warm</button><button type="button" data-v="dark">Dark</button></div>
<b>Head</b><div class="lab-set" data-key="head"><button type="button" data-v="k">Label line</button><button type="button" data-v="u">Rule under</button><button type="button" data-v="o">Rule over</button></div>
</div>
</div>

<script>
(function () {
  var root = document.documentElement, bar = document.getElementById("lab-bar");
  if (!bar) return;
  bar.hidden = false;
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function state() {
    return {
      type: root.getAttribute("data-type") || "a",
      paper: root.getAttribute("data-theme") === "dark" ? "dark" : (root.getAttribute("data-paper") || "a"),
      head: root.getAttribute("data-head") || "k"
    };
  }
  function paint() {
    var s = state();
    bar.querySelectorAll(".lab-set").forEach(function (set) {
      set.querySelectorAll("button").forEach(function (b) {
        b.setAttribute("aria-pressed", String(b.getAttribute("data-v") === s[set.getAttribute("data-key")]));
      });
    });
  }
  function attr(name, v, plain) {
    if (v === plain) root.removeAttribute(name); else root.setAttribute(name, v);
  }
  function apply(key, v) {
    if (key === "type") {
      attr("data-type", v, "a");
      store("nvd-type", v);
      if (v !== "a" && !document.getElementById("lab-css-" + v)) {
        var l = document.createElement("link");
        l.rel = "stylesheet"; l.id = "lab-css-" + v; l.href = "/fonts/lab/type-" + v + ".css";
        document.head.appendChild(l);
      }
    } else if (key === "head") {
      attr("data-head", v, "k");
      store("nvd-head", v);
    } else if (v === "dark") {
      root.setAttribute("data-theme", "dark");
      store("pref-theme", "dark");
    } else {
      root.setAttribute("data-theme", "light");
      store("pref-theme", "light");
      attr("data-paper", v, "a");
      store("nvd-paper", v);
    }
    paint();
  }
  bar.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (b) apply(b.parentNode.getAttribute("data-key"), b.getAttribute("data-v"));
  });
  paint();
})();
</script>
