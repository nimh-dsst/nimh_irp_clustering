# Synthesizing the FY2025 collaboration analysis with the NIH Library bibliometric report

*Prepared 2026-08-17 · Adam Thomas (NIMH DSST) with Claude Code · sources: FY2025 NIDB
collaboration analysis (`nimh_irp_clustering`, branch `fy2025-refresh`); "A bibliometric
analysis of NIMH IRP, 2021–2025" (Joelle Mornini, NIH Library, Aug 2026); BMJ Impact
Analytics exports (July 2026)*

## The two analyses measure different things — and that's the value

The 2022 email thread anticipated exactly this pairing. Jenny: "co-authors would probably
over-inflate the number, as not all co-authorships are necessarily 'significant'
collaborators. Would be interesting to see both." We now have both:

| | Collaboration analysis (ours) | Bibliometric report (NIH Library) |
|---|---|---|
| Source | FY2025 NIDB annual reports (86 reports, 54 PIs) | Web of Science author search, 2021–2025 |
| Unit | Collaborations *declared* by PIs | Publications and co-authorships *observed* |
| Bias | Under-reports (PIs forget); carries stale entries forward | Over-counts (middle authors); misses non-publishing collaborations (cores, consults, data sharing) |
| Window | One fiscal year | Five calendar years |

## Where they agree (this is what makes the story credible)

1. **The same institutions dominate both lists.** Of the library's top-20 co-publication
   institutions, ~15 also appear in PI-reported collaborations (Harvard, Hopkins, Penn,
   Maryland, Stanford, Mount Sinai, Yale, Columbia, Toronto, Oxford, McGill, Erasmus,
   Karolinska…). Two independent measurement methods converge on the same partner set.
2. **The same people anchor the network.** The library's individual co-authorship network
   (Pine, Zarate, Brotman, Merikangas, Thurm, Raznahan as hubs, clustered into mood /
   neurodevelopment / imaging / basic-neuroscience communities) mirrors the FY2025
   reported-collaboration network's structure.
3. **Cross-IC collaboration is real in both.** 19% of IRP publications have co-authors at
   other NIH ICs (library); 48 of 54 PIs report cross-IC collaborators spanning 21 ICs
   (ours). NINDS is the top partner IC in both.
4. **International reach.** 43.5% of publications have non-US co-authors (library); our
   reported-collaboration map shows 343 external institutions across ~30 countries on six
   continents.
5. **Scale is consistent.** WOS finds 212 publications in CY2025; the FY2025 annual
   reports yield 229 unique publications. Given the window offset (FY vs CY) and
   database coverage differences, these are the same number.

## Where they diverge (equally useful)

- **Reported-but-not-co-published:** Nationwide Children's Hospital is our #1 reported
  external partner (10 mentions) and Duke Health and the Child Mind Institute rank high —
  none are in the library's top 20. These are likely consortium/clinical/data
  partnerships that haven't (yet) produced proportional co-authorships. The reverse
  (Univ. of California system #1 in co-publications, modest in reports) reflects
  many-author papers where UC authors aren't the PI's named collaborators.
- **Window effects:** the library's five-year author network still features investigators
  who have since left (Lisanby, Leibenluft, Kircanski). Our FY2025 roster is current.
  Any unified slide should state its window explicitly.
- **What only the library adds:** citation impact (27,937 citations; H-index 68; median
  RCR 1.56 — the median IRP paper is cited ~56% more than the median NIH-funded paper in
  its field; 19.3% of papers in the top citation decile, ~2× parity), translation profile
  (predominantly human research), and real-world uptake (117 health-policy documents and
  32 clinical guidelines cite IRP work; 30 citing patents).
- **What only ours adds:** collaboration *within* NIMH (405 collaborations; invisible to
  institution-level bibliometrics), collaborations that don't produce papers, per-PI
  reporting behavior, and the three-round FY2018→FY2021→FY2025 trend.
- **What neither had until now:** the annual reports missed at least 3 FY2025
  publications the library found (all now in the RIS file), and the library's approach
  can't see the ~15 report-listed publications without PubMed records. Union > either.

## The third leg: open science (in progress)

The OddPub pipeline (2019–2024 figures already shared with Maryland Pao) adds the
openness dimension: the NIMH IRP's proportion of publications with open-data statements
has been rising. The FY2025 RIS file (`nimh_irp_fy2025_publications.ris`, 229 DOIs, 214
with PMIDs) feeds PaperPile → publisher PDFs → OddPub v7 → the 2025 datapoint.
Note for the OddPub merge: the Colab notebook keys on `<PMID>.pdf` filenames and joins on
PMID — the RIS carries each PMID in the `AN` and `N1` fields so PDFs can be renamed
programmatically after PaperPile export.

## Proposed unified deck (for Jenny → NIMH leadership, early Sept)

Framing for an incoming Director: *the NIMH IRP is productive, collaborative far beyond
its walls, influential in science and policy, and increasingly open.*

1. **Title** — "The NIMH Intramural Research Program: Collaboration, Impact, and Open
   Science" (FY2025 update).
2. **IRP at a glance** — 54 PIs · 86 research projects · ~220 publications/year, steady
   across five years (library fig. p.2) · 229 FY2025 publications.
3. **Collaboration within NIMH** — our circle network (52 PIs, 405 collaborations, ~8/PI).
4. **Collaboration across NIH** — our cross-IC shell figure (48 PIs, 315 collaborations,
   21 ICs) + corroboration: 19% of publications have other-IC co-authors.
5. **Collaboration with the world** — our 343-institution map + the library's top-20
   co-publication institutions side by side; 43.5% of papers have international co-authors.
6. **Two lenses, one picture** — small comparison table: declared collaborations vs
   observed co-authorships converge on the same partners and people; each sees things the
   other can't. (Directly answers the question Jenny raised in 2022.)
7. **Trend** — our FY2018/FY2021/FY2025 grouped bars: collaboration rising in every scope.
8. **Scientific impact** — citations, H-index 68, median RCR 1.56, 19.3% top-decile
   (library pp.9–10).
9. **Impact beyond the literature** — 117 policy documents, 32 clinical guidelines,
   30 patents citing IRP work (BMJ/PatCite, library p.11).
10. **Open science** — data-sharing-statement trend 2019→2024, with the 2025 point added
    once OddPub runs (Colab notebook figures).
11. **Methods & caveats** — one slide: sources, windows, known biases of each method,
    attribution.

Slides 2, 8, 9 lift directly from the library report (with credit to Joelle Mornini);
3–7 come from our repo; 10 from the Colab notebook. Everything regenerable except the
library figures.

## Loose ends

- Ask Joelle for the full 1,187-publication WOS export (only the 76-pub BMJ subset was
  attached). It would let us cross-check the RIS union and reuse her institution
  normalizations.
- The RIS deliberately includes one bioRxiv preprint DOI listed in an annual report
  (10.1101/2024.10.19.619187) — drop it before import if you want journal articles only.
- Publications listed in FY2025 reports include some with earlier publication dates
  (PIs list late-2023/2024 papers); this matches how prior OddPub years were binned
  (by report year), so the 2025 datapoint stays comparable.
