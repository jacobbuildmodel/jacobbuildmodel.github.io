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


def hdb(repo, ref):
    rows = [r for r in table(repo, ref, "out/affordability.csv") if r["buyer"] == "p50"]
    years = [int(r["year"]) for r in rows]
    ratio = [round(float(r["price_to_income_years"]), 2) for r in rows]
    price = [float(r["price"]) for r in rows]
    income = [float(r["monthly_income"]) for r in rows]
    p0, i0 = price[0], income[0]
    notes = {}
    for y, p, i, k in zip(years, price, income, ratio):
        base = "" if y == years[0] else (f" Since {years[0]}: price {100 * (p / p0 - 1):+.0f}%, "
                                         f"income {100 * (i / i0 - 1):+.0f}%.")
        notes[str(y)] = f"{money(p)} flat, {money(i)} a month: {k:.2f} years of income." + base
    lo = min(range(len(ratio)), key=lambda j: ratio[j])
    return {
        "id": "hdb-years-of-income", "type": "timeline",
        "title": "A four-room flat took fewer years of income in 2025 than in 2013",
        "subtitle": "Price of a constant-quality four-room resale flat, in years of median household income, "
                    f"{years[0]} to {years[-1]}",
        "x": years,
        "panels": [
            {"title": "Years of median household income to pay the price", "unit": "years", "decimals": 2,
             "domain": [0, 7], "ticks": [0, 2, 4, 6],
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
    return {
        "id": "erp-peak-speeds", "type": "timeline",
        "title": "Peak-hour speeds stayed near LTA's target bands",
        "subtitle": f"Average weekday peak-hour speed, km/h, {years[0]} to {years[-1]}, against LTA's target bands",
        "x": years,
        "panels": [
            {"title": "Expressways (target band 45 to 65 km/h)", "unit": "km/h", "decimals": 1,
             "domain": [40, 70], "ticks": [45, 55, 65], "band": [45, 65], "mute": [2020, 2021],
             "flag": out_ex,
             "series": [{"key": "ex", "label": "expressways", "role": "subject", "values": ex}]},
            {"title": "Arterial roads (target band 20 to 30 km/h)", "unit": "km/h", "decimals": 1,
             "domain": [15, 35], "ticks": [20, 25, 30], "band": [20, 30], "mute": [2020, 2021],
             "flag": out_ar,
             "series": [{"key": "ar", "label": "arterial roads", "role": "subject", "values": ar}]},
        ],
        "notes": notes,
        "steps": [
            {"at": years[0], "text": f"{years[0]}: expressways {ex[0]:g} km/h, arterial roads {ar[0]:g} km/h. "
                                     "The shaded bands are LTA's targets."},
            {"at": out_ar[0], "text": f"{out_ar[0]}: arterial roads at {ar[years.index(out_ar[0])]:g} km/h, above the "
                                      f"band. It happened again in {out_ar[-1]}. The sealed bet that every scored "
                                      "year would sit inside the bands failed on these years."},
            {"at": years[lo], "text": f"{years[lo]}: expressways at {ex[lo]:g} km/h, the lowest in the record and "
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
        "id": "sgd-yardstick", "type": "switch",
        "title": "Whichever yardstick is used, the yen's own fall was the larger part",
        "subtitle": "The Singapore dollar's rise against the yen, average of January to March 2021 to average of "
                    "October to December 2025, split three ways",
        "domain": [-40, 60], "ticks": [-40, -20, 0, 20, 40, 60],
        "subject": "Yen's own fall", "partner": "Singapore dollar's own rise",
        "states": states,
        "summary": f"The yen's own fall is between {100 * lo:.0f} and {100 * hi:.0f} per cent of the move, "
                   "depending on the yardstick.",
        "howto": ["Each bar is a move in per cent over the same period. Right of the line is a rise, left a fall.",
                  "The buttons change the yardstick: what each currency is measured against. The first two bars "
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
