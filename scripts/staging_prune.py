#!/usr/bin/env python3
"""
staging_prune.py — keeps staging/ from growing forever.

staging/ holds RAW model output before it passes through site_publish.py.
Once a piece is gated and staged into content/<section>/, the raw dump in
staging/ has done its job.

This script is deliberately separate from site_publish.py, not called
automatically inside it. Pruning is a decision, not a side effect — you
should be able to see what's about to go before it goes.

IMPORTANT: this only ever touches staging/. It never touches content/ —
the published archive stays forever. A published post is a few KB; fifty-two
weeks of them is nothing. What actually accumulates is raw staging dumps,
and that's the only thing this script prunes.

    python scripts/staging_prune.py --status
    python scripts/staging_prune.py --prune
    python scripts/staging_prune.py --prune --keep 5 --section news
"""

import argparse
from pathlib import Path

SECTIONS = ("news", "sector", "standouts", "briefs")
DEFAULT_KEEP = 3


def files_for(staging_root, section):
    d = Path(staging_root) / section
    if not d.is_dir():
        return []
    return sorted(d.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--staging", default="staging", help="path to the staging root")
    ap.add_argument("--section", choices=SECTIONS, help="limit to one section; default all four")
    ap.add_argument("--keep", type=int, default=DEFAULT_KEEP, help="how many newest files to keep")
    ap.add_argument("--status", action="store_true", help="show what would happen (this is also the default)")
    ap.add_argument("--prune", action="store_true", help="actually delete. Default is a dry run.")
    args = ap.parse_args()

    sections = [args.section] if args.section else SECTIONS
    total_dropped = 0

    for section in sections:
        files = files_for(args.staging, section)
        keep, drop = files[: args.keep], files[args.keep :]
        verb = "dropping" if args.prune else "would drop"
        print(f"{section:10s} {len(files)} file(s) in staging — keeping {len(keep)}, {verb} {len(drop)}")
        for f in keep:
            print(f"    keep     {f.name}")
        for f in drop:
            if args.prune:
                f.unlink()
                print(f"    deleted  {f.name}")
            else:
                print(f"    would delete  {f.name}")
        total_dropped += len(drop)

    if not args.prune and total_dropped:
        print(f"\n--status only, nothing deleted. Pass --prune to actually remove {total_dropped} file(s).")
    elif not total_dropped:
        print("\nNothing to prune.")


if __name__ == "__main__":
    main()
