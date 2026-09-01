# NIMH IRP collaboration analysis — how to run a round

Requested by the Office of the Scientific Director (Jenny Mehren). Counts the
collaborations NIMH IRP investigators report in their annual reports on
intramural.nih.gov, at three scopes, and renders each as a network figure for a
short Town Hall deck.

| Round | Reporting year | Delivered | Within NIMH | Beyond NIMH | External |
|---|---|---|---|---|---|
| 1 | FY2018 | Jan 2019 | 54 PIs / 326 | 46 PIs / 303 | 470 / 300+ institutions |
| 2 | FY2021 | Sept 2022 | 53 PIs / 332 | 44 PIs / 290 | 464 / 300+ institutions |
| 3 | FY2025 | Aug 2026 | 52 PIs / 405 | 48 PIs / 315 | 562 / 343 institutions |

Round 3 also added a trend slide (the three rounds side by side) and, on the
external slide, the count of PIs reporting external collaborations (47 of 54 in
FY2025) — a number Jenny asked for in the FY2021 round.

Round 3 then grew into a unified deck for NIMH leadership (Sept 2026) combining
this analysis with an NIH Library bibliometric report and a data-sharing trend
— see "Round 3 extensions" at the end of this file.

The three scopes come from three headings on each annual report, and map onto
the `scope` column of the collaboration table as `NIMH`, `NIH`, and `EM`.

## Environment

Pinned in `uv.lock`. The FY2018 and FY2021 rounds ran on unpinned Python 3.7 and
3.9 environments that no longer exist, which is why neither could be re-run to
check a published number.

```bash
uv sync
```

Then `uv run jupyter lab`, and run `notebooks/cluster_IRP_labs_clean_for_figs.ipynb`
top to bottom. The other two notebooks are from the FY2018 round:
`cluster_IRP_labs.ipynb` (superseded) and `irp_citation_count.ipynb` (the start of
a co-authorship-based version, never finished).

Note for anyone porting old code: this round moved to pandas 3, where
`pd.unique()` no longer accepts a plain list.

## Running a new round

Bump `FY` in the configuration cell and re-run. All paths and output filenames
derive from it. That part is now cheap — but three things are not, and they are
what actually consume the schedule:

**1. The scraper will probably be broken.** intramural.nih.gov has restructured
its markup before every single round so far. Verified state as of Aug 2026:

- Every URL needs `&nidbreload=true` appended, or you get a ~381-byte
  JavaScript redirect stub instead of content.
- `searchview.taf?ipid=<N>&nidbreload=true` returns fully server-rendered HTML.
  It is the only dependable entry point. `onereport.taf`, `allreports.taf`, and
  the search flow are session + AJAX driven and return shells.
- Report fields live in a CSS grid: `headinggrid` holds the label, and the
  following `easygrid` / `pigrid` / `collabgrid` / `morelist` holds the value.
  The `headings` / `data` classes the FY2018 and FY2021 code parsed are gone.
  Heading *label text* is unchanged, so `col_rn` and everything downstream of
  the parser survived.
- **ipid discovery needs a person once per round.** The year+IC browse both
  earlier rounds saved by hand still exists but now sits behind an arithmetic
  bot-check on the search form. Don't automate the check: run the search in a
  browser, save the results page into `data/` (naming convention:
  `nidb_nimh_search_<date>.html`), and commit the ipid list extracted from it
  (see `data/nimh_fy2025_ipids.csv` and its `.md` sidecar for the FY2025
  provenance, which came from Josh Lawrimore's `nimh-dsst/irp_scraper`).
  Fallback if the browse disappears entirely: ipids are near-monotonic by
  fiscal year with ICs in contiguous blocks (FY2021 ≈ 121k, FY2023 ≈ 130k,
  FY2025 ≈ 138.5k–142k), so a rate-limited coarse scan of `searchview.taf`
  locates the MH block and a fine sweep reads it.

Reproduce the previous round's published numbers before trusting a new scrape:

```bash
uv run python validate_scrape.py
```

re-scrapes the 93 FY2021 reports (cached in `data/fy2021_rescrape_cache.json`)
and checks them against the published FY2021 numbers. Expect small drift on the
row level — NIDB records keep being edited after a year closes (typo fixes,
institution renames, duplicates collapsed); in Aug 2026 the NIH count still
matched 290/290 exactly while ~13% of external rows differed textually. One
formatting quirk matters: names carry a double space where a middle name is
absent (`Joyce  Chung, MD`), and the correction tables are keyed on those exact
strings — never collapse whitespace in name fields (`nidb._clean_name` exists
for this).

**2. The hand-maintained mappings go stale.** `collab_corrections` (~40
name-to-organization entries), `manual_edits`, and `drop_list` were curated by
hand against a specific year's roster. Reconciling them against a new roster is
the single largest time sink. Two asserts enforce it, and both will fail until
the work is done: every named intramural collaborator must resolve to a real
research organization, and every PI in the graph must have a photo.

**3. PI photos.** `data/pi_pics` had 62 headshots as of FY2021, matched to PIs by
surname prefix in the filename. Roster turnover means chasing new ones.

## The external-partners map

Automated as of round 3. The FY2018/FY2021 rounds built this slide by hand:
institutions pasted into a Google Sheet, imported into Google My Maps for
geocoding, screenshot onto the slide. The exported KMZ stores addresses, not
coordinates, so none of that work was reusable and the whole path depended on
one person's Drive access.

Now:

```bash
uv run python geocode_institutions.py data/pi_collabs_FY2025.csv
```

resolves institutions through the committed cache
(`data/institution_geocodes.csv`) and sends only new names to Nominatim
(OpenStreetMap's geocoder — respect its 1 request/second policy; the script
does). Misses stay in the cache as blank rows for hand-filling; re-runs retry
them. The notebook's map cell then renders the slide figure from the cache and
the committed Natural Earth basemap (`data/ne_110m_land.geojson`, public
domain) — no Google account, no manual step. The old Google Sheets links remain
in `data/README.md` for provenance.

## Known data-quality caveat

NIDB makes it easy for investigators to carry a collaborator list forward
unchanged, and it does not prompt them to remove people who have left. Both
earlier rounds found NIMH collaborators who had left NIMH years before. Reported
collaborations therefore understate churn and, in places, overstate current
activity. Co-authorship would be the independent check; it would also overstate
in the other direction, since not every co-author is a meaningful collaborator.
Worth reporting both, which is why round 3 keeps FY2021 and FY2025 on identical
code — collaborator lists that are byte-identical across four years are
detectable, and named NIMH collaborators can be checked against the live roster.

## Round 3 extensions (Aug 2026): the unified leadership deck

The FY2025 round expanded into an 11-slide deck ("2026 NIMH IRP — Collaboration
Impact OpenScience") combining three streams. Slides 1–4 come from this repo;
the rest draw on the sources below. The synthesis memo
(`docs/synthesis_collab_bibliometrics_FY2025.md`) holds the full comparison.

**Bibliometrics** — "A bibliometric analysis of NIMH IRP, 2021–2025" by Joelle
Mornini (NIH Library, Aug 2026): Web of Science author search; 1,187
publications, H-index 68, median RCR 1.56, 117 policy documents and 32 clinical
guidelines citing IRP work. Key cross-check: ~15 of its top-20 co-publication
institutions also appear in PI-reported collaborations, while its author search
found 90 FY2025-window publications the annual reports never listed (PIs
under-report). Deck slides 6–8 use charts cropped from the report PDF.

**FY2025 publication corpus** — `nimh_irp_fy2025_publications.ris` (229 DOIs,
214 with PMIDs): union of annual-report publications (Josh Lawrimore's
`nimh-dsst/irp_scraper` browser scrape + this repo's scrape cache, which caught
7 IDs added to NIDB after his January run) and the library's BMJ policy subset
(3 publications the reports missed). Built for the PaperPile → publisher-PDF →
OddPub pipeline.

**Data sharing (OddPub)** — the production pipeline is PDF → minerU (GPU,
markdown) → OddPub v7.2.3 on markdown, per-PMID results in
`datalad-osm/oddpubV7minerU_v2/` on Biowulf; runner scripts in
`nimh-dsst/dsst-etl`, `osm-pipeline`, and `minerU_osm`. Do NOT run oddpub's
pdftools path on the older intramural PDFs — pathological files hang it past
its internal timeout. NIMH trend 2019→2025 on uniform methodology: papers with
data-sharing statements 6.9% → 31.3%; PIs with ≥1 open-data paper 27.5% →
79.1%. Version check: v7.1 vs v7.2.3 agree on 95.3% of 1,048 shared
publications.

**Manual validation** — "Manually labelled pubs from NIMH IRP 2023.xlsx"
(224 pubs hand-checked for the BSC, mostly report-years 2022–23): true
open-data rate 40.0% for 2023 (150/209 of that trend year checked). Against
this gold standard OddPub v7.2.3 shows 94% specificity but only 57% sensitivity
— the automated trend understates true sharing, so the deck's papers figure
carries a manually-verified marker at 2023 and the caveat runs in the
leadership deck's methods slide. Note the 2025 point used publisher PDFs;
earlier years were partly author manuscripts, which under-carry
data-availability statements.

**Deferred** — the all-IC 2025 data-sharing update: only 22% of the 5,261
all-IC FY2025 PMIDs had results as of Aug 2026 (~4,100 publisher PDFs to
source, NCI the largest gap).
