"""Independent check of the generated sentences in data/charts/*.json against the research repositories'
CSV files, read again here with separate code. Usage: python -I verify_sentences.py SITE HDB_REPO COE_REPO"""
import csv, io, json, re, subprocess, sys

site, hdb_repo, coe_repo = sys.argv[1:4]


def rows(repo, path):
    out = subprocess.run(["git", "-C", repo, "show", "origin/HEAD:" + path], capture_output=True, check=True).stdout
    return list(csv.DictReader(io.StringIO(out.decode("utf-8"))))


def check_points(name, years, vals, pts, band=None):
    n, bad = len(vals), 0
    for i, (y, v, p) in enumerate(zip(years, vals, pts)):
        texts = [t for _, t in p["lines"]]
        num = float(re.match(r"[-0-9.]+", p["big"]).group())
        ok = abs(num - v) < 1e-9
        # change from the year before
        if i:
            d = round(v - vals[i - 1], 2)
            m = re.match(r"(Up|Down) ([0-9.]+) from (\d+)|Same as in (\d+)", p["step"])
            if d == 0:
                ok &= m.group(4) == str(years[i - 1])
            else:
                ok &= m.group(1) == ("Up" if d > 0 else "Down") and abs(float(m.group(2)) - abs(d)) < 1e-9 \
                      and m.group(3) == str(years[i - 1]) and p["dir"] == (1 if d > 0 else -1)
        else:
            ok &= p["step"] == "First year shown" and p["dir"] == 0
        # rank
        r = texts[0]
        hi, lo = sum(o > v for o in vals), sum(o < v for o in vals)
        m = re.match(r"The (highest|lowest) since (\d+) \((.+)\)\.", r)
        if m:
            j = years.index(int(m.group(2)))
            between = vals[j + 1:i]
            if m.group(1) == "highest":
                ok &= all(o < v for o in between) and vals[j] >= v and len(between) >= 2
            else:
                ok &= all(o > v for o in between) and vals[j] <= v and len(between) >= 2
            ok &= (m.group(3) == "the same") == (vals[j] == v)
            if m.group(3) != "the same":
                ok &= abs(float(m.group(3)) - vals[j]) < 1e-9
        elif re.match(r"The (highest|lowest) of the years up to", r):
            w = re.match(r"The (highest|lowest)", r).group(1)
            ok &= str(y) in r and all((o < v) if w == "highest" else (o > v) for o in vals[:i]) and i >= 2
        elif re.match(r"The (joint )?(highest|lowest) of the (\d+) years shown", r):
            m = re.match(r"The (joint )?(highest|lowest) of the (\d+)", r)
            ok &= int(m.group(3)) == n and ((hi if m.group(2) == "highest" else lo) == 0)
            ok &= bool(m.group(1)) == (vals.count(v) > 1)
        else:
            m = re.match(r"(Joint )?(\d+)(?:st|nd|rd|th) (highest|lowest) of the (\d+) years shown\.", r)
            ok &= bool(m) and int(m.group(4)) == n and int(m.group(2)) == (hi if m.group(3) == "highest" else lo) + 1 \
                  and bool(m.group(1)) == (vals.count(v) > 1)
        # band
        if band:
            b = texts[1]
            a, z = band
            if v > z:
                ok &= b == f"{round(v - z, 2):g} km/h above the top of the band."
            elif v < a:
                ok &= "below the bottom" in b
            elif v == z:
                ok &= b.startswith("At the top of the band")
            else:
                m = re.match(r"Inside the band, ([0-9.]+) km/h (below its top|above its bottom)\.", b)
                want = round(z - v, 2) if m.group(2) == "below its top" else round(v - a, 2)
                ok &= abs(float(m.group(1)) - want) < 1e-9 and ((z - v <= v - a) == (m.group(2) == "below its top"))
        # first year
        s = [t for t in texts if "first year" in t]
        if s and i:
            m = re.match(r"([0-9.]+) \S+ (above|below) (\d+), the first year\.", s[0])
            d0 = round(v - vals[0], 2)
            ok &= bool(m) and abs(float(m.group(1)) - abs(d0)) < 1e-9 and (m.group(2) == "above") == (d0 > 0) \
                  and int(m.group(3)) == years[0]
        if not ok:
            bad += 1
            print("MISMATCH", name, y, p)
    print(name, "points checked:", n, "mismatches:", bad)
    return bad


bad = 0
h = json.load(open(site + "/data/charts/hdb_years_of_income.json"))
src = [r for r in rows(hdb_repo, "out/affordability.csv") if r["buyer"] == "p50"]
years = [int(r["year"]) for r in src]
ratio = [round(float(r["price_to_income_years"]), 2) for r in src]
assert years == h["x"] and ratio == h["panels"][0]["series"][0]["values"]
bad += check_points("hdb ratio", years, ratio, h["panels"][0]["points"])
for r, p in zip(src, h["panels"][0]["points"]):
    money = [t for _, t in p["lines"] if t.startswith("Flat")][0]
    want = "Flat S$%s. Median income S$%s a month." % (format(int(round(float(r["price"]))), ","),
                                                         format(int(round(float(r["monthly_income"]))), ","))
    if money != want:
        bad += 1
        print("MISMATCH money", r["year"], money, want)
q = h["compare"]
end = src[-1]
for s, st in zip(src[:-1], q["starts"]):
    raw = 100 * (float(end["price_to_income_years"]) / float(s["price_to_income_years"]) - 1)
    dp = 100 * (float(end["price"]) / float(s["price"]) - 1)
    di = 100 * (float(end["monthly_income"]) / float(s["monthly_income"]) - 1)
    a, b = round(float(end["price_to_income_years"]), 2), round(float(s["price_to_income_years"]), 2)
    word = "more" if a > b else "fewer"
    want_v = (f"The flat took {a:.2f} years of median household income in {end['year']}, against {b:.2f} in "
              f"{s['year']}: {abs(a - b):.2f} {word}.")
    want_w = (f"Between those years the price {'rose' if dp >= 0 else 'fell'} {abs(dp):.0f}% and income "
              f"{'rose' if di >= 0 else 'fell'} {abs(di):.0f}%.")
    ok = (abs(st["pct"] - round(raw, 1)) < 1e-9 and st["pct_text"] == f"{raw:+.0f}%" and st["verdict"] == want_v
          and st["why"] == want_w and st["headline"] == f"{word} years of income than in {s['year']}"
          and st["dir"] == (1 if a > b else -1) and st["year"] == int(s["year"]))
    for i, r in enumerate(src):
        ok &= abs(st["values"][i] - round(100 * (float(r["price_to_income_years"]) / float(s["price_to_income_years"]) - 1), 1)) < 1e-9
    if not ok:
        bad += 1
        print("MISMATCH compare", s["year"], st["pct_text"], st["verdict"], st["why"])
ups = sum(1 for st in q["starts"] if st["dir"] > 0)
print("compare starts checked:", len(q["starts"]), "| higher from", ups, "| tally:", q["tally"])

e = json.load(open(site + "/data/charts/erp_peak_speeds.json"))
src = rows(coe_repo, "erp/out/annual.csv")
years = [int(r["year"]) for r in src]
for k, col, band in ((0, "speed_expressway", (45, 65)), (1, "speed_arterial", (20, 30))):
    vals = [float(r[col]) for r in src]
    assert years == e["x"] and vals == e["panels"][k]["series"][0]["values"]
    bad += check_points(col, years, vals, e["panels"][k]["points"], band)
    for y, v, st in zip(years, vals, e["panels"][k]["status"]):
        want = "not scored" if y in (2020, 2021) else "above the band" if v > band[1] else "below the band" if v < band[0] else "inside the band"
        if st != want:
            bad += 1
            print("MISMATCH status", y, st, want)
print("TOTAL MISMATCHES:", bad)
sys.exit(1 if bad else 0)
