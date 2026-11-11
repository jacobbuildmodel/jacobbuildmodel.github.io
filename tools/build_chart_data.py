"""Build the data files for the interactive charts (data/charts/*.json) from the research repositories.

Every value is read from a committed output file of the piece's own pipeline, at a named commit, so an
interactive chart can never show a number the article's pipeline did not produce. Each JSON file records
where every series came from (repository, commit, file, column).

Usage:
  python -I tools/build_chart_data.py --hdb PATH_TO_hdb-affordability --coe PATH_TO_coe-analysis [--ref origin/HEAD]

Reads with `git show <ref>:<path>`, so a clone without a working tree is enough. Pure standard library.
"""
import argparse
import csv
import io
import json
import math
import os
import subprocess

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "charts")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, check=True).stdout.decode("utf-8")


def table(repo, ref, path):
    return list(csv.DictReader(io.StringIO(git(repo, "show", f"{ref}:{path}"))))


def source(repo, ref, name, files):
    return {"repository": f"https://github.com/jacobbuildmodel/{name}",
            "commit": git(repo, "rev-parse", ref).strip(), "files": files}


def pct(log_change):
    return (math.exp(log_change) - 1) * 100


def money(v):
    return "S$" + format(int(round(v)), ",")


GENERATED = ("The sentences in the card are worked out when the page is built, from the same data file as the "
             "line. None is typed by hand and none comes from a live model, so the card and the chart cannot disagree.")


def g(v):
    """A number as the pipeline's files print it, without trailing zeros."""
    return f"{round(v, 2):g}"


def ordinal(k):
    return f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"


def rank_line(years, vals, i, fmt):
    """Where one year sits in its series, in words: 'the lowest since 2013', or its rank."""
    v, n = vals[i], len(vals)
    tie = vals.count(v) > 1
    above, below = sum(1 for o in vals if o > v), sum(1 for o in vals if o < v)
    if not tie and above == 0:
        return f"The highest of the {n} years shown."
    if not tie and below == 0:
        return f"The lowest of the {n} years shown."
    for word, beats in (("highest", lambda o: o < v), ("lowest", lambda o: o > v)):
        j = i - 1
        while j >= 0 and beats(vals[j]):
            j -= 1
        if i - 1 - j >= 2:  # it beats at least the two years before it
            if j >= 0:
                was = "the same" if vals[j] == v else fmt(vals[j])
                return f"The {word} since {years[j]} ({was})."
            return f"The {word} of the years up to {years[i]}."
    k, word = (above + 1, "highest") if above <= below else (below + 1, "lowest")
    if k == 1:
        return f"The joint {word} of the {n} years shown."
    return f"{'Joint ' if tie else ''}{ordinal(k)} {word} of the {n} years shown."


def band_line(v, lo, hi, unit):
    """How far one value sits from a target band, in words."""
    if v > hi:
        return f"{g(v - hi)} {unit} above the top of the band."
    if v < lo:
        return f"{g(lo - v)} {unit} below the bottom of the band."
    if v in (lo, hi):
        return f"At the {'top' if v == hi else 'bottom'} of the band ({v:g} {unit})."
    if hi - v <= v - lo:
        return f"Inside the band, {g(hi - v)} {unit} below its top."
    return f"Inside the band, {g(v - lo)} {unit} above its bottom."


def band_status(v, lo, hi):
    return "above the band" if v > hi else "below the band" if v < lo else "inside the band"


def points(years, vals, unit, fmt, band=None, extra=None, instead=None):
    """The 'explain this point' card for every year of one series: the value, the change from the year
    before, the rank, the distance from the band or from the first year. Built here, from the same
    numbers as the line, so a card can never disagree with the chart."""
    out = []
    for i, (y, v) in enumerate(zip(years, vals)):
        if i == 0:
            step = {"dir": 0, "text": "First year shown"}
        else:
            d = round(v - vals[i - 1], 2)
            step = {"dir": (d > 0) - (d < 0),
                    "text": f"{'Up' if d > 0 else 'Down'} {fmt(abs(d))} from {years[i - 1]}" if d
                    else f"Same as in {years[i - 1]}"}
        lines = [["rank", rank_line(years, vals, i, fmt)]]
        if band:
            lines.append(["band", band_line(v, band[0], band[1], unit)])
        d0 = round(v - vals[0], 2)
        if instead and y in instead:
            lines.append(instead[y])
        elif i == 0:
            lines.append(["start", "The first year shown."])
        elif d0 == 0:
            lines.append(["start", f"The same as in {years[0]}, the first year."])
        else:
            lines.append(["start", f"{fmt(abs(d0))} {unit} {'above' if d0 > 0 else 'below'} {years[0]}, "
                                   "the first year."])
        if extra and y in extra:
            lines.append(extra[y])
        assert all(len(t) <= 50 for _, t in lines), lines  # short enough for a phone: one row, two at most
        out.append({"big": f"{fmt(v)} {unit}", "dir": step["dir"], "step": step["text"], "lines": lines})
    return out


def compare(years, ratio_raw, ratio, price, income):
    """'Build the comparison': for every possible starting year, the series as a change from that year,
    and a verdict on the last year in words. A reading of history, built from the pipeline's numbers."""
    end, n = years[-1], len(years)

    def move(x):
        return f"{'rose' if x >= 0 else 'fell'} {abs(x):.0f}%"

    starts = []
    for s in range(n - 1):
        vals = [round(100 * (r / ratio_raw[s] - 1), 1) for r in ratio_raw]
        exact = 100 * (ratio_raw[-1] / ratio_raw[s] - 1)  # rounded once for the label, not twice
        pct = vals[-1]
        shown = 100 * (ratio[-1] / ratio[s] - 1)
        assert abs(pct - shown) < 0.6, (years[s], pct, shown)  # agrees with the two-decimal figures on show
        d = round(ratio[-1] - ratio[s], 2)
        more = d > 0
        dp, di = 100 * (price[-1] / price[s] - 1), 100 * (income[-1] / income[s] - 1)
        starts.append({
            "year": years[s], "values": vals, "pct": pct, "dir": 1 if more else -1,
            "pct_text": f"{exact:+.0f}%",
            "headline": f"{'more' if more else 'fewer'} years of income than in {years[s]}",
            "verdict": f"The flat took {ratio[-1]:.2f} years of median household income in {end}, against "
                       f"{ratio[s]:.2f} in {years[s]}: {abs(d):.2f} {'more' if more else 'fewer'}.",
            "why": f"Between those years the price {move(dp)} and income {move(di)}."})
    up = [s["year"] for s in starts if s["dir"] > 0]
    down = [s["year"] for s in starts if s["dir"] < 0]
    few, word = (down, "lower") if len(down) <= len(up) else (up, "higher")
    many_word = "higher" if word == "lower" else "lower"
    tally = f"From {n - 1 - len(few)} of the {n - 1} starting years, {end} comes out {many_word}."
    if few:
        tally += (f" From {' and '.join(str(y) for y in few)} it comes out {word}." if len(few) <= 2
                  else f" From the other {len(few)} it comes out {word}.")
    flat = [v for s in starts for v in s["values"]]
    lo, hi = 10 * math.floor(min(flat) / 10), 10 * math.ceil(max(flat) / 10)
    ends = [s["pct"] for s in starts]
    i_lo = min(range(n - 1), key=lambda j: ratio[j])
    i_hi = max(range(n - 1), key=lambda j: ratio[j])
    return {"end": end, "initial": i_lo, "domain": [lo, hi],
            "title": f"Whether {end} looks high or low depends on the year it is compared with",
            "subtitle": "Years of median household income to pay for a constant-quality four-room resale flat, "
                        "as a change from the starting year the reader picks",
            "ticks": [t for t in range(lo, hi + 1, 10) if t % 20 == 0],
            "strip_domain": [10 * math.floor(min(ends + [0]) / 10), 10 * math.ceil(max(ends) / 10)],
            "presets": [{"i": i_hi, "label": f"{years[i_hi]}, the peak"},
                        {"i": i_lo, "label": f"{years[i_lo]}, the low"}],
            "tally": tally, "starts": starts}


def hdb(repo, ref):
    rows = [r for r in table(repo, ref, "out/affordability.csv") if r["buyer"] == "p50"]
    years = [int(r["year"]) for r in rows]
    ratio_raw = [float(r["price_to_income_years"]) for r in rows]
    ratio = [round(v, 2) for v in ratio_raw]
    price = [float(r["price"]) for r in rows]
    income = [float(r["monthly_income"]) for r in rows]
    p0, i0 = price[0], income[0]
    notes = {}
    for y, p, i, k in zip(years, price, income, ratio):
        base = "" if y == years[0] else (f" Since {years[0]}: price {100 * (p / p0 - 1):+.0f}%, "
                                         f"income {100 * (i / i0 - 1):+.0f}%.")
        notes[str(y)] = f"{money(p)} flat, {money(i)} a month: {k:.2f} years of income." + base
    lo = min(range(len(ratio)), key=lambda j: ratio[j])
    cash = {y: ["coins", f"Flat {money(p)}. Median income {money(i)} a month."]
            for y, p, i in zip(years, price, income)}
    return {
        "id": "hdb-years-of-income", "type": "timeline", "icon": "house", "topic": "HDB resale flats",
        "explain": [0], "compare": compare(years, ratio_raw, ratio, price, income),
        "howto2": {
            "explain": [
                "Each point is one year: the price of the same kind of four-room resale flat, divided by what "
                "the median household earned in a year. Lower means the flat took less income.",
                "Tap a point, drag across the chart, or use the slider and the arrow buttons. The card under "
                "the chart reads that year: the value, the change from the year before, where it ranks, and how "
                "far it sits from the first year.",
                GENERATED],
            "compare": [
                "Pick a starting year with the slider or the two buttons. The line then shows every year as a "
                "change from that year, in per cent. The starting year sits on the zero line.",
                "Above the zero line the flat took more years of income than in the starting year; below it, "
                f"fewer. The card gives the answer for {years[-1]} in words.",
                "The bars under the chart give the same answer for every starting year at once, so the reader "
                "can see how much the answer depends on where the comparison starts.",
                "This is a reading of what happened. It says nothing about any one household, and nothing "
                "about what prices will do."]},
        "title": "A four-room flat took fewer years of income in 2025 than in 2013",
        "subtitle": "Price of a constant-quality four-room resale flat, in years of median household income, "
                    f"{years[0]} to {years[-1]}",
        "x": years,
        "panels": [
            {"title": "Years of median household income to pay the price", "unit": "years", "decimals": 2,
             "domain": [0, 7], "ticks": [0, 2, 4, 6], "short": "Years of income",
             "points": points(years, ratio, "years", lambda v: f"{v:.2f}", extra=cash),
             "series": [{"key": "ratio", "label": "years of income", "role": "subject", "values": ratio}]},
            {"title": f"Why: income rose faster than the price ({years[0]} = 100)", "unit": "index", "decimals": 0,
             "domain": [80, 160], "ticks": [80, 100, 120, 140, 160], "baseline": 100,
             "series": [
                 {"key": "income", "label": "income", "role": "subject",
                  "values": [round(100 * i / i0, 1) for i in income]},
                 {"key": "price", "label": "flat price", "role": "context",
                  "values": [round(100 * p / p0, 1) for p in price]}]},
        ],
        "notes": notes,
        "steps": [
            {"at": years[0], "text": f"{years[0]} was a price peak: the flat cost {ratio[0]:.2f} years of median income."},
            {"at": years[lo], "text": f"{years[lo]} was the low: {ratio[lo]:.2f} years. Starting a comparison "
                                      "here makes everything after it look worse."},
            {"at": years[-1], "text": f"{years[-1]}: {ratio[-1]:.2f} years. More than in {years[lo]}, "
                                      f"fewer than in {years[0]}."},
        ],
        "howto": ["Each point is one year: the price of the same kind of four-room resale flat, divided by what "
                  "the median household earned in a year.",
                  "Lower means the flat took less income. Drag the slider, or press Play, to move through the years.",
                  "The second panel sets both the price and the income to 100 in the first year, so the two "
                  "can be compared on one scale."],
        "source_line": "Source: HDB resale transactions and SingStat household income, via the piece's own pipeline.",
        "source": source(repo, ref, "hdb-affordability",
                         [{"path": "out/affordability.csv", "rows": "buyer = p50",
                           "columns": ["year", "price", "monthly_income", "price_to_income_years"]}]),
        "fallback": {"src": "/figs/fig1_price_to_income.svg"},
    }


def erp(repo, ref):
    rows = table(repo, ref, "erp/out/annual.csv")
    years = [int(r["year"]) for r in rows]
    ex = [float(r["speed_expressway"]) for r in rows]
    ar = [float(r["speed_arterial"]) for r in rows]
    out_ar = [y for y, v in zip(years, ar) if (v > 30 or v < 20) and y not in (2020, 2021)]
    out_ex = [y for y, v in zip(years, ex) if (v > 65 or v < 45) and y not in (2020, 2021)]
    notes = {}
    for y, e, a in zip(years, ex, ar):
        tag = " Not scored: pandemic year." if y in (2020, 2021) else (
            " Arterial roads ran above the target band." if y in out_ar else "")
        notes[str(y)] = f"Expressways {e:g} km/h (target 45 to 65). Arterial roads {a:g} km/h (target 20 to 30)." + tag
    lo = min(range(len(ex)), key=lambda j: ex[j])
    hi_ar = max(range(len(ar)), key=lambda j: ar[j])
    skip = {y: ["mute", "Not scored: a pandemic year."] for y in (2020, 2021)}

    def status(vals, lo_b, hi_b):
        return ["not scored" if y in skip else band_status(v, lo_b, hi_b) for y, v in zip(years, vals)]

    return {
        "id": "erp-peak-speeds", "type": "timeline", "icon": "car", "topic": "Roads at peak hours",
        "explain": [0, 1],
        "howto2": {
            "explain": [
                "The line is the average speed at peak hours in each year; the shaded band is the range LTA "
                "aims for. The two buttons switch between expressways and arterial roads.",
                "Tap a point, drag across the chart, or use the slider and the arrow buttons. The card under "
                "the chart reads that year: the speed, the change from the year before, where it ranks, and how "
                "far it sits from the band.",
                "A ringed dot marks a year outside the band. 2020 and 2021 are drawn faint: the piece did not "
                "score the pandemic years.",
                GENERATED],
            "panel": [
                "Each dial shows the speed in the selected year on one kind of road. The thick part of the arc "
                "is LTA's target band, and the words under the number say whether the speed is inside it.",
                "Tap a dial to draw that road's line under it. Drag the slider, or press Play, to move through "
                "the years.",
                "Scroll on: each step of the story under the panel moves it to that step's year.",
                "A ringed dot marks a year outside the band. 2020 and 2021 are drawn faint: the piece did not "
                "score the pandemic years."]},
        "title": "Peak-hour speeds stayed near LTA's target bands",
        "subtitle": f"Average weekday peak-hour speed, km/h, {years[0]} to {years[-1]}, against LTA's target bands",
        "x": years,
        "panels": [
            {"title": "Expressways (target band 45 to 65 km/h)", "unit": "km/h", "decimals": 1,
             "domain": [40, 70], "ticks": [45, 55, 65], "band": [45, 65], "mute": [2020, 2021],
             "flag": out_ex, "short": "Expressways", "status": status(ex, 45, 65),
             "points": points(years, ex, "km/h", g, band=(45, 65), instead=skip),
             "series": [{"key": "ex", "label": "expressways", "role": "subject", "values": ex}]},
            {"title": "Arterial roads (target band 20 to 30 km/h)", "unit": "km/h", "decimals": 1,
             "domain": [15, 35], "ticks": [20, 25, 30], "band": [20, 30], "mute": [2020, 2021],
             "flag": out_ar, "short": "Arterial roads", "status": status(ar, 20, 30),
             "points": points(years, ar, "km/h", g, band=(20, 30), instead=skip),
             "series": [{"key": "ar", "label": "arterial roads", "role": "subject", "values": ar}]},
        ],
        "notes": notes,
        "steps": [
            {"at": years[0], "panel": 0,
             "text": f"{years[0]}: expressways {ex[0]:g} km/h, arterial roads {ar[0]:g} km/h. "
                     "The shaded bands are LTA's targets."},
            {"at": out_ar[0], "panel": 1, "text": f"{out_ar[0]}: arterial roads at {ar[years.index(out_ar[0])]:g} km/h, above the "
                                      f"band. It happened again in {out_ar[-1]}. The sealed bet that every scored "
                                      "year would sit inside the bands failed on these years."},
            {"at": years[hi_ar], "panel": 1,
             "text": f"{years[hi_ar]}: arterial roads at {ar[hi_ar]:g} km/h, the highest in the record. The piece "
                     "did not score 2020 and 2021, the pandemic years."},
            {"at": years[lo], "panel": 0,
             "text": f"{years[lo]}: expressways at {ex[lo]:g} km/h, the lowest in the record and "
                     "still inside the band."},
        ],
        "howto": ["Each panel is one kind of road. The line is the average speed at peak hours in each year; "
                  "the shaded band is the range LTA aims for.",
                  "A ringed dot marks a year outside the band. 2020 and 2021 are drawn faint: the piece did not "
                  "score the pandemic years.",
                  "Drag the slider, or press Play, to move through the years."],
        "source_line": "Source: Land Transport Authority via data.gov.sg, through the piece's own pipeline.",
        "source": source(repo, ref, "coe-analysis",
                         [{"path": "erp/out/annual.csv", "columns": ["year", "speed_expressway", "speed_arterial"]}]),
        "fallback": {"src": "/figs/chart1_speed_vs_band.svg"},
    }


def sgd(repo, ref):
    t = {r["key"]: r["value"] for r in table(repo, ref, "sgd/out/tests.csv")}
    a1 = {r["key"]: float(r["value"]) for r in table(repo, ref, "sgd/out/review_a1_usd.csv")}
    a3 = {r["key"]: float(r["value"]) for r in table(repo, ref, "sgd/out/review_a3_real.csv")}
    b = float(t["T2_b"])
    states = [
        {"key": "broad", "label": "All trading partners",
         "explain": "Each currency against all its trading partners (BIS broad nominal index).",
         "bars": [["Singapore dollar against all partners", pct(float(t["T2_s"]))],
                  ["Yen against all partners", pct(float(t["T2_nx"]))],
                  ["Singapore dollar against the yen", pct(b)]],
         "shares": {"sgd": float(t["T2_S"]), "other": float(t["T2_P"]), "remainder": float(t["T2_R"])}},
        {"key": "usd", "label": "US dollar",
         "explain": "Each currency against the US dollar alone.",
         "bars": [["Singapore dollar against the US dollar", a1["A1_scored_JPY_sgd_vs_usd_pct"]],
                  ["Yen against the US dollar", -a1["A1_scored_JPY_x_vs_usd_pct"]],
                  ["Singapore dollar against the yen", pct(a1["A1_scored_JPY_b"])]],
         "shares": {"sgd": a1["A1_scored_JPY_share_sgd"], "other": a1["A1_scored_JPY_share_x"], "remainder": 0.0}},
        {"key": "real", "label": "After prices",
         "explain": "Each currency against all its trading partners, after consumer prices (BIS broad real index).",
         "bars": [["Singapore dollar against all partners, real", a3["A3_scored_JPY_s_real_pct"]],
                  ["Yen against all partners, real", -a3["A3_scored_JPY_n_real_pct"]],
                  ["Singapore dollar against the yen, real", a3["A3_scored_JPY_b_real_pct"]]],
         "shares": {"sgd": a3["A3_scored_JPY_S"], "other": a3["A3_scored_JPY_P"], "remainder": a3["A3_scored_JPY_R"]}},
    ]
    for s in states:
        s["bars"] = [[lab, round(v, 1)] for lab, v in s["bars"]]
        s["shares"] = {k: round(v, 3) for k, v in s["shares"].items()}
    lo = min(s["shares"]["other"] for s in states)
    hi = max(s["shares"]["other"] for s in states)
    return {
        "id": "sgd-measure", "icon": "currency", "topic": "Singapore dollar and yen", "type": "switch",
        "title": "Whichever measure is used, the yen's own fall was the larger part",
        "subtitle": "The Singapore dollar's rise against the yen, average of January to March 2021 to average of "
                    "October to December 2025, split three ways",
        "domain": [-40, 60], "ticks": [-40, -20, 0, 20, 40, 60],
        "subject": "Yen's own fall", "partner": "Singapore dollar's own rise",
        "states": states,
        "summary": f"The yen's own fall is between {100 * lo:.0f} and {100 * hi:.0f} per cent of the move, "
                   "depending on the measure.",
        "howto": ["Each bar is a move in per cent over the same period. Right of the line is a rise, left a fall.",
                  "The buttons change the measure: what each currency is measured against. The first two bars "
                  "are each currency's own move; the third is the Singapore dollar against the yen.",
                  "The strip below shows how much of the move each side accounts for, as shares of the change "
                  "in logs. Where the shares do not sum to 100 the remainder is printed."],
        "source_line": "Source: Bank for International Settlements and MAS, through the piece's own pipeline.",
        "source": source(repo, ref, "coe-analysis",
                         [{"path": "sgd/out/tests.csv", "keys": ["T2_s", "T2_nx", "T2_b", "T2_S", "T2_P", "T2_R"]},
                          {"path": "sgd/out/review_a1_usd.csv", "keys": "A1_scored_JPY_*"},
                          {"path": "sgd/out/review_a3_real.csv", "keys": "A3_scored_JPY_*"}]),
        "fallback": {"src": "/figs/sgd_chart1_split.svg"},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hdb", required=True)
    ap.add_argument("--coe", required=True)
    ap.add_argument("--ref", default="origin/HEAD")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    for chart in (hdb(a.hdb, a.ref), erp(a.coe, a.ref), sgd(a.coe, a.ref)):
        name = chart["id"].replace("-", "_") + ".json"
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump(chart, f, indent=1)
            f.write("\n")
        print("wrote", name)


if __name__ == "__main__":
    main()
