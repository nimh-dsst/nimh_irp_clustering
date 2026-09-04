"""NIMH IRP data-sharing trend, 2019–2025, with the 2025 point and a manual-validation marker.

Reproduces the deck's open-science slide. All years are scored with the same tool
chain (minerU markdown -> OddPub v7.2.3); PDF *sources* differ by year (2025 =
publisher PDFs via PaperPile; earlier years partly author manuscripts / PMC copies).

Inputs (all under data/):
  irp_data_2024_7p1/All_ICs19_23_DM.csv, pmids_articles_2024.csv, ipids_2024.csv
        2019–2024 report-year -> PMID -> PI tables (from the Colab tarball)
  All_ICs_2025_NIMH.csv
        2025 report-year -> PMID -> PI, built from irp_scraper publications_2025.csv
        plus this repo's scrape cache
  nimh_oddpub_2019_2025_collected.csv
        per-PMID OddPub v7.2.3 result, collected from the HPC result stores
  ../Manually labelled pubs from NIMH IRP 2023.xlsx  (project dir; optional)
        gold-standard manual labels for the 2023 validation marker

Conventions, stated on the slide: a paper counts in every report-year that lists
it; the denominator is listed papers with an OddPub result (94–100% per year).
PI metric: PIs with >=1 open-data paper, among PIs with >=1 scored paper that year.

    uv run python data_sharing_figures.py
"""

from pathlib import Path

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter

D = Path("data")
T = D / "irp_data_2024_7p1"
FIG = Path("figures/FY2025")
MANUAL = Path("../Manually labelled pubs from NIMH IRP 2023.xlsx")

old = pd.read_csv(T / "All_ICs19_23_DM.csv").query('IC == "NIMH"')[["YEAR", "PI", "PMID"]]
n24 = (
    pd.read_csv(T / "pmids_articles_2024.csv")
    .merge(pd.read_csv(T / "ipids_2024.csv"), on="IPID")
    .query('IC == "NIMH"')[["YEAR", "PI", "PMID"]]
)
n25 = pd.read_csv(D / "All_ICs_2025_NIMH.csv")[["YEAR", "PI", "PMID"]]
pubs = pd.concat([old, n24, n25]).dropna(subset=["PMID"])
pubs["PMID"] = pubs.PMID.astype(int)

odd = pd.read_csv(D / "nimh_oddpub_2019_2025_collected.csv")[["PMID", "is_open_data"]]
df = (
    pubs.merge(odd, on="PMID", how="left")
    .dropna(subset=["is_open_data"])
    .drop_duplicates(["YEAR", "PMID"])
)

by = df.groupby("YEAR").agg(n=("PMID", "nunique"), open=("is_open_data", "sum"))
by["prop"] = 100 * by.open / by.n
pi = (
    df.groupby(["YEAR", "PI"]).is_open_data.any().reset_index()
    .groupby("YEAR").agg(pis=("PI", "nunique"), open_pis=("is_open_data", "sum"))
)
pi["prop"] = 100 * pi.open_pis / pi.pis
print(by.round(1).to_string())
print(pi.round(1).to_string())

# Manual validation on the SAME set the plotted 2023 point uses: every paper
# listed in a 2023 report (not just papers first listed that year).
star = None
if MANUAL.exists():
    def load(sheet):
        d = pd.read_excel(MANUAL, sheet_name=sheet, header=1)
        d.columns = [str(c).strip() for c in d.columns]
        return d

    man = pd.concat([load("NIMH_IRP_2023"), load("Copy of NIMH_IRP_2023")])
    man["PMID"] = pd.to_numeric(man.PMID, errors="coerce")
    man = man.dropna(subset=["PMID", "manual_is_open_data"])
    man["PMID"] = man.PMID.astype(int)
    man = man.drop_duplicates("PMID")
    man["manual"] = man.manual_is_open_data.astype(bool)
    listed23 = set(old.query("YEAR == 2023").PMID.astype(int))
    m = man[man.PMID.isin(listed23)]
    star = (len(listed23), len(m), 100 * m.manual.mean())
    print(
        f"2023: {star[0]} listed, {star[1]} manually labelled, manual rate {star[2]:.1f}% "
        f"(automated on the same set: {by.loc[2023, 'prop']:.1f}%)"
    )


def fig(data, ylab, title, out, star=None):
    f, ax = plt.subplots(figsize=(6.2, 5), dpi=170)
    d = data.reset_index()
    sns.regplot(data=d, x="YEAR", y="prop", ax=ax, ci=None,
                line_kws={"color": "red", "alpha": 0.3}, scatter_kws={"s": 60, "color": "blue"})
    if star:
        n_listed, n_man, rate = star
        ax.scatter([2023], [rate], marker="*", s=340, color="#DAA520", edgecolor="#8B6914",
                   zorder=5, label=f"Manually verified, 2023\n({n_man} of {n_listed} papers listed that year: {rate:.0f}%)")
        ax.annotate("", xy=(2023, rate - 1.8), xytext=(2023, by.loc[2023, "prop"] + 1.7),
                    arrowprops=dict(arrowstyle="-|>", color="#8B6914", alpha=0.6))
        ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.set_xlim([2018.5, 2025.5])
    ax.set_ylim([0, 80])
    ax.xaxis.set_ticks(range(2019, 2026))
    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=12)
    ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.set_ylabel(ylab, fontsize=11)
    ax.set_xlabel("")
    ax.set_title(title, fontsize=14, weight="bold")
    ax.yaxis.grid(True, color="#EEEEEE")
    ax.set_axisbelow(True)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    f.tight_layout()
    f.savefig(out, facecolor="white")
    print("wrote", out)


FIG.mkdir(parents=True, exist_ok=True)
fig(by, "Papers listed in that year's annual reports\nwith a data-sharing statement",
    "NIMH IRP Papers w/data sharing", FIG / "NIMH_IRP_2019-2025_oddpubV723_validated.png", star)
fig(pi, "PIs with ≥1 open-data paper\n(of PIs with ≥1 scored paper that year)",
    "NIMH PIs w/at least one pub w/data sharing", FIG / "NIMH_PIs_2019-2025_v723.png")
