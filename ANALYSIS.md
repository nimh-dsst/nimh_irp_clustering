# NIMH IRP collaboration analysis — how to run a round

Requested by the Office of the Scientific Director (Jenny Mehren). Counts the
collaborations NIMH IRP investigators report in their annual reports on
intramural.nih.gov, at three scopes, and renders each as a network figure for a
short Town Hall deck.

| Round | Reporting year | Delivered | Within NIMH | Beyond NIMH | External |
|---|---|---|---|---|---|
| 1 | FY2018 | Jan 2019 | 54 PIs / 326 | 46 PIs / 303 | 470 / 300+ institutions |
| 2 | FY2021 | Sept 2022 | 53 PIs / 332 | 44 PIs / 290 | 464 / 300+ institutions |
| 3 | FY2025 | in progress | | | |

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
- **ipid discovery has no drop-in replacement.** Both earlier rounds saved a
  "list all NIMH reports for year X" search page by hand and regexed the ipids
  out of it. That browse path no longer exists — search now requires search
  terms. Instead, ipids are near-monotonic by fiscal year with ICs in contiguous
  blocks (FY2021 ≈ 121k, FY2023 ≈ 130k, FY2025 ≈ 138.5k–142k, nothing above
  ~143k), so a coarse scan locates the MH block and a fine sweep reads it.
  Rate-limit it.

Reproduce the previous round's published numbers before trusting a new scrape.
The saved search pages for FY2018 and FY2021 are still in `data/`, and those
ipids still resolve, so the prior year can be re-scraped on current code and
checked against the table above.

**2. The hand-maintained mappings go stale.** `collab_corrections` (~40
name-to-organization entries), `manual_edits`, and `drop_list` were curated by
hand against a specific year's roster. Reconciling them against a new roster is
the single largest time sink. Two asserts enforce it, and both will fail until
the work is done: every named intramural collaborator must resolve to a real
research organization, and every PI in the graph must have a photo.

**3. PI photos.** `data/pi_pics` had 62 headshots as of FY2021, matched to PIs by
surname prefix in the filename. Roster turnover means chasing new ones.

## Not in the code

The external-partners map slide was built by hand from Google Sheets, linked in
`data/README.md` — geocoding and layout were done there, not here. Confirm
access before promising that slide.

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
