"""Translation triangle: NIMH IRP vs the rest of the NIH IRP, report-years 2021–2025.

Reproduces the deck's "human-focused research program" slide. The NIH Library
report plotted NIMH alone on iCite's Triangle of Biomedicine, which shows shape
but tells no story without a comparator. This adds one — every other IC's
annual-report publications over the same window — and tests for drift.

Inputs
  data/triangle_cohorts.csv   (YEAR, IC, PMID, grp)  built from the Colab tarball
                              (All_ICs19_23_DM.csv + 2024 files) and irp_scraper's
                              publications_2025.csv
  data/icite_triangle.csv     iCite API fields per PMID: human, animal,
                              molecular_cellular (MeSH-derived weights), year

Outputs
  figures/FY2025/translation_triangle_nimh_vs_irp.png
  printed statistics (two-proportion z tests)

    uv run python translation_triangle.py [--refetch]

iCite: https://icite.od.nih.gov/api  (public, no key; batches of 300 with a
0.4 s pause). Method reference: Weber GM (2013) "Identifying translational
science within the triangle of biomedicine", J Transl Med 11:126.
"""

from __future__ import annotations

import argparse
import os
import time
from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from matplotlib import pyplot as plt

DATA = Path("data")
FIG = Path("figures/FY2025")
COHORTS = DATA / "triangle_cohorts.csv"
ICITE = DATA / "icite_triangle.csv"
USER_AGENT = "nimh-irp-analysis (adam.thomas@nih.gov)"

# Barycentric vertices: Human top, Molecular/Cellular bottom-left, Animal bottom-right
V_H = np.array([0.5, np.sqrt(3) / 2])
V_M = np.array([0.0, 0.0])
V_A = np.array([1.0, 0.0])


def fetch_icite(pmids: list[int]) -> pd.DataFrame:
    done = set(pd.read_csv(ICITE).pmid) if ICITE.exists() else set()
    todo = [p for p in pmids if p not in done]
    print(f"iCite: {len(pmids)} PMIDs, {len(todo)} to fetch")
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    rows = []
    for i in range(0, len(todo), 300):
        chunk = todo[i : i + 300]
        r = session.get(
            "https://icite.od.nih.gov/api/pubs",
            params={
                "pmids": ",".join(map(str, chunk)),
                "fl": "pmid,year,human,animal,molecular_cellular,is_research_article",
            },
            timeout=60,
        )
        r.raise_for_status()
        for d in r.json()["data"]:
            rows.append(
                {
                    "pmid": d["pmid"],
                    "year": d.get("year"),
                    "human": d.get("human"),
                    "animal": d.get("animal"),
                    "mol_cell": d.get("molecular_cellular"),
                    "research": d.get("is_research_article"),
                }
            )
        time.sleep(0.4)
    if rows:
        pd.DataFrame(rows).to_csv(ICITE, mode="a", header=not ICITE.exists(), index=False)
    return pd.read_csv(ICITE).drop_duplicates("pmid")


def two_proportion_z(k1: int, n1: int, k2: int, n2: int) -> float:
    p = (k1 + k2) / (n1 + n2)
    return (k1 / n1 - k2 / n2) / sqrt(p * (1 - p) * (1 / n1 + 1 / n2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refetch", action="store_true", help="ignore the iCite cache")
    args = parser.parse_args()
    if args.refetch and ICITE.exists():
        ICITE.unlink()

    cohorts = pd.read_csv(COHORTS)
    icite = fetch_icite(sorted(cohorts.PMID.unique()))
    df = cohorts.merge(icite, left_on="PMID", right_on="pmid", how="left")

    # Cross-IC papers appear once per IC in the cohort table; count once per group.
    df = df.drop_duplicates(["grp", "PMID"])
    weights = df[["human", "animal", "mol_cell"]]
    df["has_mesh"] = weights.notna().all(axis=1) & (weights.sum(axis=1) > 0)
    coverage = df.groupby("grp").has_mesh.mean()
    print("MeSH coverage by group:", coverage.round(3).to_dict())
    print("MeSH coverage by NIMH report year:",
          df[df.grp == "NIMH"].groupby("YEAR").has_mesh.mean().round(2).to_dict())

    t = df[df.has_mesh].copy()
    s = t[["human", "animal", "mol_cell"]].sum(axis=1)
    for c in ["human", "animal", "mol_cell"]:
        t[c] = t[c] / s

    groups = {g: d for g, d in t.groupby("grp")}
    for g, d in groups.items():
        print(
            f"{g:8s} n={len(d):5d} mean H/A/M {d.human.mean():.3f}/{d.animal.mean():.3f}/"
            f"{d.mol_cell.mean():.3f} | human-only {(d.human == 1).mean():.1%}"
        )
    a, b = groups["NIMH"], groups["restIRP"]
    z = two_proportion_z(int((a.human == 1).sum()), len(a), int((b.human == 1).sum()), len(b))
    print(f"human-only NIMH vs rest: z = {z:.1f}")

    early = a[a.YEAR.isin([2021, 2022])]
    late = a[a.YEAR.isin([2024, 2025])]
    z_drift = two_proportion_z(
        int((early.human == 1).sum()), len(early), int((late.human == 1).sum()), len(late)
    )
    print(
        f"NIMH drift human-only: {(early.human == 1).mean():.1%} (2021-22, n={len(early)}) vs "
        f"{(late.human == 1).mean():.1%} (2024-25, n={len(late)}), z = {z_drift:.1f}"
    )
    print("cross-listed NIMH∩rest PMIDs:", len(set(a.PMID) & set(b.PMID)))

    # ---- figure: paired triangles, bubble area = share of each group's papers ----
    FIG.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.6), dpi=200)
    panels = [("NIMH IRP", "NIMH", "#124E7E"), ("Rest of NIH IRP", "restIRP", "#4E8FC4")]
    for ax, (label, g, color) in zip(axes, panels):
        d = groups[g].copy()
        # snap to a 1/24 lattice so identical MeSH mixes aggregate into one bubble
        for col, src in [("hx", "human"), ("ax_", "animal"), ("mx", "mol_cell")]:
            d[col] = (d[src] * 24).round() / 24
        agg = d.groupby(["hx", "ax_", "mx"]).size().rename("n").reset_index()
        agg["share"] = agg.n / agg.n.sum()
        xy = np.outer(agg.hx, V_H) + np.outer(agg.mx, V_M) + np.outer(agg.ax_, V_A)
        ax.add_patch(plt.Polygon([V_M, V_A, V_H], closed=True, fill=False,
                                 edgecolor="#888888", linewidth=1.2))
        ax.scatter(xy[:, 0], xy[:, 1], s=agg.share * 2600 + 4, color=color, alpha=0.55,
                   edgecolors="white", linewidths=0.4, zorder=3)
        ax.text(0.5, 1.03, f"{(d.human == 1).mean():.0%} of papers are human-only",
                ha="center", fontsize=11, fontweight="bold", color=color)
        ax.text(0.5, 0.955, "Human", ha="center", fontsize=10, color="#444444",
                bbox=dict(facecolor="white", edgecolor="none", pad=1.5), zorder=4)
        ax.text(-0.02, -0.06, "Molecular / Cellular", ha="left", fontsize=10, color="#444444")
        ax.text(1.02, -0.06, "Animal", ha="right", fontsize=10, color="#444444")
        ax.set_title(f"{label}  (n={len(d):,} papers)", fontsize=13, weight="bold", pad=22)
        ax.set_xlim(-0.08, 1.08)
        ax.set_ylim(-0.11, 1.09)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.tight_layout()
    out = FIG / "translation_triangle_nimh_vs_irp.png"
    fig.savefig(out, facecolor="white", bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main()
