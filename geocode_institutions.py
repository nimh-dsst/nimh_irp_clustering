"""Geocode external-collaborator institutions via Nominatim, with a committed cache.

The FY2021 round placed institutions on a map by pasting them into a Google
Sheet and importing it into Google My Maps, which geocoded them server-side —
the exported KMZ stores only addresses, so none of that work was reusable.
This replaces the manual workflow: institutions resolve through
data/institution_geocodes.csv first, and only names not yet in the cache go to
Nominatim (OpenStreetMap's geocoder, https://nominatim.org). The cache is
committed, so a future round pays only for its new institutions.

    uv run python geocode_institutions.py data/pi_collabs_FY2025.csv

Nominatim usage policy: max 1 request/second and an identifying User-Agent.
Do not parallelize this.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from pathlib import Path

import requests

CACHE = Path("data/institution_geocodes.csv")
NOMINATIM = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "nimh-irp-collab-analysis/2025 (adamt@nih.gov)"


def load_cache() -> dict[str, tuple[float, float, str]]:
    if not CACHE.exists():
        return {}
    with CACHE.open() as f:
        return {
            r["institution"]: (float(r["lat"]), float(r["lon"]), r["source"])
            for r in csv.DictReader(f)
            if r["lat"]
        }


def save_cache(cache: dict, misses: set[str]) -> None:
    with CACHE.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["institution", "lat", "lon", "source"])
        for name in sorted(set(cache) | misses):
            if name in cache:
                lat, lon, source = cache[name]
                w.writerow([name, f"{lat:.5f}", f"{lon:.5f}", source])
            else:
                # Kept in the file so a person can fill the row in by hand;
                # blank lat/lon rows are re-tried on the next run.
                w.writerow([name, "", "", "nominatim_miss"])


def query_variants(name: str) -> list[str]:
    """Progressively simplified queries for one institution string.

    NIDB strings carry departments and parenthetical countries the geocoder
    chokes on: "University of Sydney, Brain and Mind Centre" or
    "Tetra Therapeutics (United States)". Try the full string, then without
    the parenthetical, then the head segment (plus country when one was named).
    """
    name = name.strip()
    variants = [name]
    country = None
    m = re.search(r"\(([^)]+)\)\s*$", name)
    if m:
        country = m.group(1)
        bare = name[: m.start()].strip()
        variants.append(f"{bare}, {country}")
        variants.append(bare)
        name = bare
    head = name.split(",")[0].strip()
    if head != name:
        variants.append(f"{head}, {country}" if country else head)
        if country:
            variants.append(head)

    # Nominatim matches places, not org charts: "Stanford University School of
    # Medicine" misses while "Stanford University" hits. Strip unit suffixes
    # from the head segment to reach the parent institution — city-level
    # placement is all the map needs.
    suffixes = (
        " school of medicine", " medical school", " medical center",
        " medical centre", " medical research institute", " health system",
        " hospital system", " health sciences", " school of public health",
        " college of medicine", " system",
    )
    parent = head.lower()
    for suffix in suffixes:
        if parent.endswith(suffix):
            variants.append(head[: -len(suffix)].strip())
            break

    seen: list[str] = []
    for v in variants:
        if v and v not in seen:
            seen.append(v)
    return seen


def geocode(name: str, session: requests.Session) -> tuple[float, float] | None:
    for q in query_variants(name):
        r = session.get(
            NOMINATIM,
            params={"q": q, "format": "json", "limit": 1},
            timeout=30,
        )
        time.sleep(1.1)  # usage policy: never more than 1 request/second
        if r.status_code != 200:
            continue
        hits = r.json()
        if hits:
            return float(hits[0]["lat"]), float(hits[0]["lon"])
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collab_csv", help="pi_collabs_FY<year>.csv from the notebook run")
    args = parser.parse_args()

    with open(args.collab_csv) as f:
        institutions = sorted(
            {r["institute"].strip() for r in csv.DictReader(f) if r["scope"] == "EM"}
        )
    cache = load_cache()
    todo = [n for n in institutions if n not in cache]
    print(f"{len(institutions)} institutions; {len(institutions) - len(todo)} cached, {len(todo)} to geocode")
    if todo:
        print(f"(~{len(todo) * 2 * 1.1 / 60:.0f} min worst case at 1 req/s)")

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    misses: set[str] = set()
    for i, name in enumerate(todo, 1):
        result = geocode(name, session)
        if result:
            cache[name] = (result[0], result[1], "nominatim")
        else:
            misses.add(name)
            print(f"  MISS: {name}")
        if i % 20 == 0:
            print(f"  {i}/{len(todo)}")
            save_cache(cache, misses)  # checkpoint: a crash loses nothing

    save_cache(cache, misses)
    resolved = sum(1 for n in institutions if n in cache)
    print(f"done: {resolved}/{len(institutions)} resolved, {len(misses)} misses (blank rows in {CACHE})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
