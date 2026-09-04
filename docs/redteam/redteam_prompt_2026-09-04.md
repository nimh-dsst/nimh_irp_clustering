# Red-team prompt — NIMH IRP unified deck (DRAFT, not yet run)

*Intended for an independent agent with fresh context. Everything it needs is
listed below; it should not rely on any prior conversation.*

---

You are an independent, adversarial reviewer. Your job is to find every way the
quantitative claims in a slide deck could be wrong, overstated, or indefensible
to an expert bibliometrician, and to report what you find without softening it.
You are not here to fix things or to praise the work.

## Who will read the deck

It was prepared for Jenny Mehren (Senior Scientific Advisor, NIMH Intramural
Research Program) to share with NIMH leadership in September 2026, and may later
be used to brief the incoming NIMH Director. Jenny has asked to share it with
two people in NIMH's Office of Science Policy, Planning and Communications
(OSPPC):

- **Mindy Chai, PhD** — leads OSPPC (the NIMH website still lists Meredith Fox,
  who left in the 2025 reduction in force; treat the site as out of date).
  https://www.linkedin.com/in/mindy-chai-phd-2281333/
- **Didi Cross** — OSPPC; does bibliometric and research-portfolio analysis
  professionally. Assume she will check numbers against sources, know the
  standard tools (Web of Science, InCites, iCite, RCR) intimately, and notice
  denominator and window problems immediately.
  https://www.linkedin.com/in/dhcross/

Office page: https://www.nimh.nih.gov/about/organization/od/office-of-science-policy-planning-and-communications-osppc

Review for that audience. The email thread that led to the deck is in
`/Users/adamt/proj/irp_collab/*.eml` (read them with Python's `email` module);
it shows what Jenny asked for, what she has already questioned, and how the
deck was described to her. The NIH Library bibliometric report the deck draws
on was produced by Joelle Mornini at Jenny's request and is attached to
`FW_ NIMH IRP bibliometrics.eml`.

## The deliverable under review

`/Users/adamt/proj/irp_collab/2026 NIMH IRP - Collaboration Impact OpenScience - <latest date>.pptx`
(use the newest file matching that pattern). Eleven slides: 1–4 reported
collaborations, 5 synthesis, 6–8 bibliometrics, 9 translation triangle,
10 data sharing, 11 methods. Render it to images (`soffice --headless
--convert-to pdf` then `pdftoppm`) and read every slide, including footers.

## Where each number is supposed to come from

**Slides 1–5 and 11 (collaborations)** — repo
`/Users/adamt/proj/irp_collab/nimh_irp_clustering`, branch `fy2025-refresh`
(also on GitHub, `nimh-dsst/nimh_irp_clustering`). Read `ANALYSIS.md` first.
Pipeline: `nidb.py` (scraper) → `notebooks/cluster_IRP_labs_clean_for_figs.ipynb`
(curation + figures) → `data/pi_collabs_FY2025.csv`. Prior rounds' published
numbers are in `ANALYSIS.md`; `validate_scrape.py` is the regression test.
Hand-curated tables live in the notebook: `manual_edits`, `collab_corrections`,
`drop_list`.

**Slides 6–8 (bibliometrics)** — the NIH Library report, extracted from the
email `/Users/adamt/proj/irp_collab/FW_ NIMH IRP bibliometrics.eml`
(PDF attachment) plus a re-run of its Web of Science query:
`/Users/adamt/proj/irp_collab/wos_export_1_to_1000.ris` and
`wos_export_1000_to1194.ris` (and `.txt` twins). The deck quotes the report's
numbers directly; the synthesis memo is
`nimh_irp_clustering/docs/synthesis_collab_bibliometrics_FY2025.md`.

**Slide 9 (translation triangle)** — `nimh_irp_clustering/translation_triangle.py`
with `data/triangle_cohorts.csv` and `data/icite_triangle.csv` (cached iCite
API responses). Re-run it; it must reproduce the slide's numbers.

**Slide 10 (data sharing)** — inputs:
`/Users/adamt/proj/irp_collab/irp_data_2024_7p1.tar.gz` (the 2019–2024 tables
and the earlier "7p1" OddPub results used in the Colab notebook
`/Users/adamt/proj/irp_collab/IRP Open Data 7p1.ipynb`),
`/Users/adamt/proj/irp_collab/nimh_oddpub_2019_2025_collected.csv` (per-PMID
OddPub v7.2.3 results collected from HPC), and the gold-standard manual labels
`/Users/adamt/proj/irp_collab/Manually labelled pubs from NIMH IRP 2023.xlsx`.
The FY2025 publication list is `/Users/adamt/proj/irp_collab/nimh_irp_fy2025_publications.ris`.
The processing pipeline itself (minerU → OddPub) ran on NIH HPC and is described
in `ANALYSIS.md` ("Round 3 extensions"); you cannot re-run it, but you can
re-derive every number on the slide from the collected CSV and the tarball.

## What to do

1. **Build a claims inventory.** Every number, comparison, and qualitative
   assertion on every slide (including footers), one row each: slide, claim,
   where it should come from, whether you could reproduce it, and the value you
   got.

2. **Reproduce, don't trust.** Recompute every number you can from the files
   above. Report exact matches, near-misses, and failures separately. Where a
   number comes from the Library report, check that the deck transcribes it
   faithfully and that the report's own footnotes don't undercut how the deck
   uses it.

3. **Attack the denominators and windows.** Fiscal vs calendar years;
   report-year vs publication-year; "PIs" vs "investigators" vs "reports";
   unique PMIDs vs rows; publications with vs without PMIDs/MeSH; cross-IC
   double counting. For each slide, state the denominator the slide implies and
   the one the data actually supports.

4. **Stress the strongest claims hardest.** In particular:
   - "Collaborations rose in every scope" (slide 4) — how much of the rise is
     roster change, reporting-behavior change, or curation change vs real
     growth? The FY2021 re-scrape drift and the hand-curated corrections are
     both attack surfaces.
   - The two-lens convergence claim (slide 5) — is "~15 of top 20" a fair
     summary, and are the institution matches real or substring artifacts?
   - "Roughly twice parity" and the RCR interpretation (slide 7).
   - "60% vs 33% human-only, p < 0.001" (slide 9) — cohort comparability,
     MeSH-based classification validity, whether NIMH's annual-report
     publication set is representative of NIMH output, the effect of the
     lattice-snapping in the figure.
   - "The automated trend is conservative" (slide 10) — this rests on 57%
     sensitivity / 94% specificity measured on 2022–23 publications. Is it valid
     to extend that to 2019–2021 and to 2025? Does the switch to publisher PDFs
     in 2025 (earlier years partly author manuscripts) make the 2025 point
     non-comparable? Is a linear fit through seven points defensible?
   - The 79% PI figure (slide 10) — PI denominators by year, and what "≥1
     open-data paper" means when PIs have very different paper counts.

5. **Check internal consistency** across slides (e.g., the number of PIs on
   slides 1, 3, 6, 10; publication counts on slides 6, 9, 10, 11).

6. **Check the methods slide** against what was actually done. Anything the
   footers assert that you cannot verify, say so.

## What to report

A single markdown file, `redteam_findings.md`, with:
- The claims inventory as a table.
- Findings ranked by severity: **fatal** (claim is wrong or unsupportable),
  **material** (an expert would dispute it or demand a caveat), **minor**
  (wording, precision, presentation). For each: the slide, the claim, what you
  found, the evidence, and the smallest change that would make it defensible.
- A short list of the claims you consider fully solid, so the authors know
  what *not* to touch.
- Anything you could not check and why.

Do not edit any project files. Do not soften findings because the work is
extensive. If a claim is fine, say so briefly and move on.
