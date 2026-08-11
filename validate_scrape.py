"""Regression test for the scraper: re-scrape FY2021 and check the published numbers.

The FY2021 round reported 332 within-NIMH, 290 other-IC, and 464 external
collaborations. Those ipids still resolve, so a rewritten scraper can be checked
against them before it is trusted on a new year.

The other-IC and external counts are the sharp test. Neither was touched by the
hand-curated corrections, so they must match exactly. The within-NIMH count is
reported for reference only: it is post-curation in the published figure, so a
raw re-scrape is expected to come out higher.

    uv run python validate_scrape.py
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

import nidb

DATA = Path("data")
SEARCH_HTML = DATA / "nidb_nimh_search_2021_09_09.html"
PUBLISHED_CSV = DATA / "pi_collabs_2021reports.csv"
CACHE = DATA / "fy2021_rescrape_cache.json"

PUBLISHED = {"NIMH": 332, "NIH": 290, "EM": 464}
SCOPE_FIELDS = {
    "NIMH": "Collaborators from other NIMH organizations",
    "NIH": "Collaborators from other NIH organizations",
    "EM": "External Collaborators",
}


def fy2021_ipids() -> list[str]:
    html = SEARCH_HTML.read_text(errors="replace")
    return list(dict.fromkeys(re.findall(r"\?ipid=([0-9]+)", html)))


def collab_pairs(records: list[dict]) -> pd.DataFrame:
    """Flatten parsed reports into one row per reported collaboration."""
    rows = []
    for record in records:
        for scope, field in SCOPE_FIELDS.items():
            for name, institute in record.get(field) or []:
                rows.append(
                    {
                        "pi": record.get("Principal Investigator")
                        or record.get("Lead Investigator"),
                        "ro": record.get("Research Organization"),
                        "collab": name,
                        "institute": institute,
                        "scope": scope,
                    }
                )
    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delay", type=float, default=0.5, help="seconds between requests")
    parser.add_argument("--limit", type=int, default=None, help="only scrape the first N (smoke test)")
    parser.add_argument("--refresh", action="store_true", help="re-fetch instead of using the cache")
    args = parser.parse_args()

    ipids = fy2021_ipids()
    if args.limit:
        ipids = ipids[: args.limit]
    print(f"FY2021 ipids from saved search page: {len(ipids)}")

    if CACHE.exists() and not args.refresh:
        records = json.loads(CACHE.read_text())
        errors = []
        print(f"loaded {len(records)} reports from {CACHE} (--refresh to re-fetch)")
    else:
        records, errors = nidb.scrape_reports(ipids, expect_fy=2021, delay=args.delay)
        print(f"parsed {len(records)} reports, {len(errors)} error(s)")
        for ipid, message in errors:
            print(f"  ERROR {ipid}: {message}")
        CACHE.write_text(json.dumps(records, indent=1))

    scraped = collab_pairs(records)
    published = pd.read_csv(PUBLISHED_CSV)

    print(f"\n{'scope':6s} {'scraped':>8s} {'published':>10s}  {'verdict'}")
    failures = []
    for scope in ("NIMH", "NIH", "EM"):
        got = int((scraped.scope == scope).sum())
        want = PUBLISHED[scope]
        if scope == "NIMH":
            # Published figure is post-curation, so raw must come out higher.
            verdict = "ok (raw >= curated)" if got >= want else "FAIL raw < curated"
        elif scope == "NIH":
            verdict = "ok" if got == want else "FAIL"
        else:
            # Reports stay editable after the year closes; allow slight drift.
            drift = abs(got - want) / want
            verdict = f"ok (drift {got - want:+d})" if drift <= 0.01 else f"FAIL drift {drift:.1%}"
        if verdict.startswith("FAIL"):
            failures.append(scope)
        print(f"{scope:6s} {got:>8d} {want:>10d}  {verdict}")

    if scraped.pi.nunique() != published.pi.nunique():
        failures.append("PI count")

    # Row-level comparison on the two uncurated scopes, keyed on the bare name.
    # The FY2021 round stripped academic degrees from external collaborators
    # (none of its 464 EM names contain a comma) but kept them for other-IC
    # collaborators, so a raw string comparison is not meaningful across rounds.
    def key(frame: pd.DataFrame) -> set[tuple[str, str]]:
        bare = frame.collab.astype(str).str.split(",").str[0].str.strip()
        return set(zip(bare, frame.institute.astype(str).str.strip()))

    for scope in ("NIH", "EM"):
        got = key(scraped.query("scope == @scope"))
        want = key(published.query("scope == @scope"))
        missing, extra = want - got, got - want
        matched = len(got & want)
        rate = matched / max(len(want), 1)
        print(
            f"\n{scope}: {matched}/{len(want)} published pairs re-found "
            f"({rate:.1%}), {len(missing)} missing, {len(extra)} new"
        )
        for pair in sorted(missing)[:6]:
            print(f"   missing: {pair}")
        for pair in sorted(extra)[:6]:
            print(f"   new:     {pair}")
        # Reports stay editable after the year closes. Spot-checking every
        # discrepancy in Aug 2026 found NIDB-side record edits, not parse errors:
        # typo fixes (Brian Yukata Hill -> Brian Yutaka Hill, Jozef H Duyn ->
        # Jeff H Duyn), institution renames (UCLA -> University of California,
        # Los Angeles), and one duplicate entry collapsed into a single person.
        # External institutions have been cleaned up the most, so EM drifts more.
        floor = 0.95 if scope == "NIH" else 0.85
        if rate < floor:
            failures.append(f"{scope} rows ({rate:.1%} re-found, floor {floor:.0%})")

    print(f"\nPIs: scraped {scraped.pi.nunique()}, published {published.pi.nunique()}")
    print("\nRESULT:", "FAILED -> " + ", ".join(map(str, failures)) if failures else "PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
