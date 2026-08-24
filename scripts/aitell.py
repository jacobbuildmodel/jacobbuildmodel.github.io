#!/usr/bin/env python3
"""
aitell.py — measure the things that make prose read as machine-written,
plus the things that break the site publish gate.

Usage:
    python aitell.py draft.md
    python aitell.py draft.md --numbers      # also print the number manifest
    python aitell.py a.md b.md               # compare drafts

No dependencies. Python 3.8+.

Every threshold here comes from a measurement, not a preference. Sources are
named beside each check. The tool reports; it never rewrites. A flag is a
question to answer, not an order to obey — some of these constructions are
correct in the right place, and the point is to notice you used it.
"""
import re
import sys
import unicodedata
from collections import Counter

# ---------------------------------------------------------------- thresholds
# Em dashes per 1,000 words. Published human literature averages 4.76
# (702,939 words sampled); GPT-4.1 measures 10.62 and Claude Opus 9.09 on
# matched prompts. Warn where prose enters the model band.
EM_WARN, EM_FAIL = 6.0, 8.0

# Share of sentences opening with The / This / It / In / There / These.
# Above roughly half is a documented LLM signature.
OPENER_WARN = 0.42

# Burstiness. Human prose varies sentence length; models cluster at 18-24
# words. A standard deviation below 7 means every sentence is the same size.
BURST_WARN = 7.0
CLUSTER_WARN = 0.45          # share of sentences in the 15-25 word band

# Reading speed for the layered-read budget.
WPM = 235

# --------------------------------------------------------------- vocabularies
AI_LEXICON = [
    "delve", "delves", "delving", "leverage", "leveraging", "landscape",
    "realm", "tapestry", "testament to", "underscore", "underscores",
    "navigate the", "navigating the", "crucial", "pivotal", "myriad",
    "plethora", "robust" , "seamless", "seamlessly", "holistic",
    "multifaceted", "nuanced", "intricate", "vibrant", "pave the way",
    "at the end of the day", "the reality is", "in today's", "ever-evolving",
    "game-changer", "unlock", "unlocking", "harness", "harnessing",
    "foster", "fostering", "spearhead", "cornerstone", "paradigm",
    "resonate", "resonates", "elevate", "elevating", "meticulous",
    "moreover", "furthermore", "notably", "importantly", "ultimately",
]

HEDGE_PREAMBLE = [
    "it is worth noting", "it's worth noting", "it is important to note",
    "it's important to note", "it is important to understand",
    "it should be noted", "generally speaking", "in many cases",
    "from a broader perspective", "that said", "having said that",
    "it is worth mentioning", "one could argue", "arguably",
    "in essence", "essentially", "fundamentally", "broadly speaking",
]

STACKED_HEDGES = [
    "may potentially", "might possibly", "could potentially",
    "seems to suggest", "appears to indicate", "tends to suggest",
    "may well", "somewhat likely", "relatively unclear",
]

CLOSERS = [
    "one thing is clear", "only time will tell", "the bottom line is",
    "in conclusion", "to sum up", "all in all", "at its core",
    "the takeaway is", "what is clear is", "remains to be seen",
]

# Intensifiers that stand in for a number.
EMPTY_INTENSIFIERS = [
    "dramatically", "massively", "considerably", "substantially",
    "significantly", "vastly", "hugely", "enormously", "markedly",
    "remarkably", "extremely", "incredibly", "particularly strong",
]

# Latinate verbs with a plainer Anglo-Saxon twin.
LATINATE = {
    "utilise": "use", "utilize": "use", "utilised": "used",
    "demonstrate": "show", "demonstrates": "shows", "demonstrated": "showed",
    "purchase": "buy", "purchased": "bought", "purchasing": "buying",
    "commence": "start", "terminate": "end", "endeavour": "try",
    "facilitate": "help", "necessitate": "need", "ascertain": "find out",
    "subsequently": "then", "additionally": "and", "prior to": "before",
    "in order to": "to", "a number of": "some", "the majority of": "most",
    "at this point in time": "now", "due to the fact that": "because",
    "with regard to": "about", "in the event that": "if",
}

# Finance register the site's compliance rules keep out of economics pieces.
FINANCE_REGISTER = [
    "alpha", "conviction", "tailwind", "headwind", "outperform",
    "undervalued", "overvalued", "price target", "attractive entry",
    "risk/reward", "asymmetric", "compelling opportunity",
]

# Characters that break the publish gate or a Windows console.
GATE_BREAKERS = {
    "−": "U+2212 MINUS SIGN (breaks the publish gate) -> use a hyphen",
    "×": "U+00D7 MULTIPLICATION SIGN -> use x",
    "≤": "U+2264 <= -> spell it",
    "≥": "U+2265 >= -> spell it",
    "≈": "U+2248 APPROX -> use about",
    "≠": "U+2260 NOT EQUAL -> spell it",
}
SAFE_NON_ASCII = set("—–''\"\"…°£€$¥•→‘’“”")


# ------------------------------------------------------------------ utilities
def strip_markdown(text):
    """Prose only: drop front matter, code fences, tables, links-to-text."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = "\n".join(l for l in text.split("\n") if not l.lstrip().startswith("|"))
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s+", "", text, flags=re.M)
    text = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", text)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    return text


def sentences(prose):
    parts = re.split(r"(?<=[.!?])[\s\n]+(?=[A-Z\"'(])", prose)
    return [p.strip() for p in parts if len(p.split()) >= 3]


def find_all(prose_lower, needles):
    hits = Counter()
    for n in needles:
        pat = r"\b" + re.escape(n) + r"\b" if n.isalpha() else re.escape(n)
        c = len(re.findall(pat, prose_lower))
        if c:
            hits[n] = c
    return hits


def bar(value, ceiling, width=28):
    filled = min(width, max(0, round(width * value / ceiling)))
    return "#" * filled + "." * (width - filled)


def verdict(ok, warn):
    return "  ok  " if ok else (" WARN " if warn else " FLAG ")


# -------------------------------------------------------------------- report
def is_draft(raw):
    m = re.match(r"\A---\n(.*?)\n---\n", raw, flags=re.S)
    return bool(m and re.search(r"^draft:\s*true\s*$", m.group(1), flags=re.M))


def analyse(path, show_numbers=False):
    raw = open(path, encoding="utf-8").read()
    prose = strip_markdown(raw)
    low = prose.lower()
    words = prose.split()
    n_words = max(1, len(words))
    sents = sentences(prose)
    n_sents = max(1, len(sents))

    print("=" * 74)
    print(f"  {path}")
    print("=" * 74)
    mins = n_words / WPM
    print(f"  {n_words:,} words   {n_sents:,} sentences   "
          f"~{mins:.0f} min read at {WPM} wpm")

    # ---- 1. rhythm ------------------------------------------------------
    lens = [len(s.split()) for s in sents]
    mean = sum(lens) / n_sents
    sd = (sum((x - mean) ** 2 for x in lens) / n_sents) ** 0.5
    clustered = sum(1 for x in lens if 15 <= x <= 25) / n_sents
    longest = max(lens)
    shortest = min(lens)

    print("\n--- rhythm " + "-" * 62)
    print(f"  mean sentence      {mean:5.1f} words   (shortest {shortest}, longest {longest})")
    print(f"  variation (sd)     {sd:5.1f}          {verdict(sd >= BURST_WARN, sd >= BURST_WARN - 1.5)}"
          f"  models cluster; sd below {BURST_WARN} reads flat")
    print(f"  in the 15-25 band  {clustered:5.0%}          "
          f"{verdict(clustered < CLUSTER_WARN, clustered < CLUSTER_WARN + 0.1)}")
    if lens.count(max(lens)) and sd < BURST_WARN:
        print("    fix: the load-bearing claims should be short sentences.")
        print("         Find your three most important claims and cut each to under 12 words.")

    # ---- 2. openers -----------------------------------------------------
    first = Counter(s.split()[0].strip("*_\"'").lower() for s in sents)
    monotone = sum(first[w] for w in ("the", "this", "it", "in", "there", "these", "that"))
    share = monotone / n_sents
    print("\n--- sentence openings " + "-" * 52)
    print(f"  The/This/It/In/There/These/That   {share:5.0%}   "
          f"{verdict(share < OPENER_WARN, share < OPENER_WARN + 0.08)}")
    print("    most common: " + ", ".join(f"{w} ({c})" for w, c in first.most_common(6)))

    # ---- 3. punctuation -------------------------------------------------
    em = prose.count("—")
    en = prose.count("–")
    semi = prose.count(";")
    density = 1000 * em / n_words
    print("\n--- punctuation " + "-" * 58)
    print(f"  em dashes          {em:4d}   {density:5.2f} per 1,000 words  "
          f"{verdict(density < EM_WARN, density < EM_FAIL)}")
    print(f"    {bar(density, 12)}")
    print(f"    human published prose 4.76  |  Claude Opus 9.09  |  GPT-4.1 10.62")
    if density >= EM_WARN:
        print("    fix: an em dash appends a qualification without committing to a sentence.")
        print("         For each one ask: does the clause after it deserve its own sentence?")
        print("         If yes, give it one. If no, cut it. Do not swap in a comma.")
    print(f"  en dashes          {en:4d}")
    print(f"  semicolons         {semi:4d}")

    # ---- 4. constructions ----------------------------------------------
    print("\n--- constructions " + "-" * 56)
    notjust = len(re.findall(r"not (just|only|merely|simply) [^.,;]{2,40}[,;] but", low))
    notxbutx = len(re.findall(r"(it'?s|this is|that'?s) not (about )?[^.,;]{2,40}[,.;] (it'?s|this is)", low))
    tricolon = len(re.findall(r"\b\w+, \w+,? and \w+\b", low))
    print(f"  'not just X, but Y'          {notjust:4d}   {verdict(notjust == 0, notjust <= 1)}")
    print(f"  'it's not X, it's Y'         {notxbutx:4d}   {verdict(notxbutx == 0, notxbutx <= 1)}")
    print(f"  tidy three-item lists        {tricolon:4d}   "
          f"{verdict(tricolon <= 2, tricolon <= 4)}   a third item invented to round the rhythm")
    if tricolon > 2:
        print("    fix: keep the two examples you actually have. Three is a cadence, not a count.")

    # ---- 5. vocabulary --------------------------------------------------
    groups = [
        ("AI lexicon", AI_LEXICON),
        ("hedge preambles", HEDGE_PREAMBLE),
        ("stacked hedges", STACKED_HEDGES),
        ("boilerplate closers", CLOSERS),
        ("intensifiers with no number", EMPTY_INTENSIFIERS),
        ("finance register (keep out of economics)", FINANCE_REGISTER),
    ]
    print("\n--- vocabulary " + "-" * 59)
    clean = True
    for label, vocab in groups:
        hits = find_all(low, vocab)
        if hits:
            clean = False
            total = sum(hits.values())
            print(f"  {label:<42} {total:3d}   "
                  + ", ".join(f"{k} x{v}" if v > 1 else k for k, v in hits.most_common(8)))
    lat = find_all(low, list(LATINATE))
    if lat:
        clean = False
        print(f"  {'latinate where plain exists':<42} {sum(lat.values()):3d}   "
              + ", ".join(f"{k} -> {LATINATE[k]}" for k in list(lat)[:6]))
    if clean:
        print("  nothing flagged")

    # ---- 6. 'significant' discipline ------------------------------------
    print("\n--- 'significant' " + "-" * 56)
    sig = [s for s in sents if re.search(r"\bsignifican", s, re.I)]
    if not sig:
        print("  not used")
    for s in sig:
        stat = bool(re.search(r"p\s*[=<>]|p-value|confidence|standard error|\bse\b", s, re.I))
        mark = "ok, statistical" if stat else "FLAG: means 'large'?"
        print(f"  [{mark}] {s[:96]}{'...' if len(s) > 96 else ''}")
    if any(not re.search(r"p\s*[=<>]|p-value|confidence|standard error", s, re.I) for s in sig):
        print("    In a piece with regressions in it, 'significant' means p < 0.05 and")
        print("    nothing else. For size, write large / sharp / a quarter higher.")

    # ---- 7. publish-gate safety ----------------------------------------
    print("\n--- publish gate " + "-" * 57)
    bad = Counter(ch for ch in raw if ch in GATE_BREAKERS)
    exotic = Counter(ch for ch in raw
                     if ord(ch) > 127 and ch not in SAFE_NON_ASCII and ch not in GATE_BREAKERS)
    if not bad and not exotic:
        print("  ASCII-safe")
    for ch, c in bad.items():
        print(f"  FLAG  {c:4d} x  {GATE_BREAKERS[ch]}")
    if exotic:
        print("  review  " + ", ".join(
            f"{ch!r} x{c} ({unicodedata.name(ch, 'unnamed')})" for ch, c in exotic.most_common(10)))
        print("    Greek letters and subscripts are fine in a memo and risky in a post.")
        print("    Write 'beta' in prose; keep the symbol for the appendix.")

    # ---- 8. headings, read as a skeleton --------------------------------
    heads = re.findall(r"^(#{2,3})\s+(.+)$", raw, flags=re.M)
    print("\n--- the heading test " + "-" * 53)
    if not heads:
        print("  no headings found")
    else:
        print("  Read these alone, in order. If they do not tell the story, the")
        print("  structure is wrong, not the prose.\n")
        for lvl, h in heads:
            h = re.sub(r"[*_`]", "", h).strip()
            long_ = len(h) > 50
            label = re.match(r"^(what|how|why|the)\b.*\b(data|analysis|method|results?|overview|introduction|background)\s*$",
                             h, re.I)
            note = "  <- over 50 chars, wraps on a phone" if long_ else ""
            note += "  <- label, not a finding" if label else ""
            print(f"    {'  ' if lvl == '###' else ''}{h}{note}")

    # ---- 9. number manifest ---------------------------------------------
    if show_numbers:
        print("\n--- every number in the prose " + "-" * 44)
        print("  Tick each against its primary source before the draft flag comes off.\n")
        seen = set()
        for s in sents:
            for m in re.finditer(r"(?<![\w.])(\$?\d[\d,]*\.?\d*\s?(?:%|bn|m|k)?)", s):
                tok = m.group(1).strip().rstrip(".,")
                if re.fullmatch(r"(19|20)\d\d", tok):      # bare years are not claims
                    continue
                if tok in seen or len(tok) < 2:
                    continue
                seen.add(tok)
                ctx = s[max(0, m.start() - 34):m.end() + 34].replace("\n", " ")
                print(f"    [ ] {tok:<12} ...{ctx.strip()}...")

    # ---- hard failures, for CI ------------------------------------------
    fails = []
    if density >= EM_FAIL:
        fails.append(f"em dash density {density:.2f} per 1,000 words (limit {EM_FAIL})")
    for ch, c in bad.items():
        fails.append(f"{c} x {GATE_BREAKERS[ch].split(' (')[0].split(' ->')[0]}")

    print()
    return dict(words=n_words, em=density, sd=sd, openers=share, fails=fails)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_numbers = "--numbers" in sys.argv
    strict = "--strict" in sys.argv
    published_only = "--published-only" in sys.argv
    if not args:
        print(__doc__)
        sys.exit(2)

    rows = []
    for p in args:
        raw = open(p, encoding="utf-8").read()
        if published_only and is_draft(raw):
            print(f"  skipped (draft: true)  {p}")
            continue
        rows.append((p, analyse(p, show_numbers)))

    if len(rows) > 1:
        print("=" * 74)
        print("  comparison")
        print("=" * 74)
        print(f"  {'file':<34}{'words':>8}{'em/1k':>9}{'sd':>7}{'openers':>10}")
        for p, r in rows:
            print(f"  {p[-33:]:<34}{r['words']:>8,}{r['em']:>9.2f}{r['sd']:>7.1f}{r['openers']:>9.0%}")
        print()

    if strict:
        failing = [(p, r["fails"]) for p, r in rows if r["fails"]]
        if failing:
            print("=" * 74)
            print("  STRICT MODE: publication blocked")
            print("=" * 74)
            for p, fs in failing:
                for f in fs:
                    print(f"  {p}: {f}")
            print("\n  Warnings above do not block. These do.\n")
            sys.exit(1)
        print("  strict checks passed\n")


if __name__ == "__main__":
    main()
