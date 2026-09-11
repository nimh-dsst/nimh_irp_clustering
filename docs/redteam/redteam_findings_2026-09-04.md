# Red-team findings — "2026 NIMH IRP – Collaboration Impact OpenScience" (2026-09-04_edit3)

*Independent adversarial review, 2026-09-04. Deck reviewed: `2026 NIMH IRP - Collaboration Impact OpenScience - 2026-09-04_edit3.pptx` (newest file matching the pattern; text also diffed against the `2026-09-04`, `_edit2` and `09-01` versions). Everything below was recomputed from the files named in the review brief; nothing was taken on trust from ANALYSIS.md, the synthesis memo, or the notebook's saved outputs (which, note, are from the FY2021 run — 332/290/464 — not FY2025).*

*Repository side effect to be aware of: re-running `translation_triangle.py` as the brief required regenerated the untracked `figures/FY2025/translation_triangle_nimh_vs_irp.png`; `git status` is otherwise clean and `data/icite_triangle.csv` is byte-identical to HEAD (the 22 uncached PMIDs returned nothing from iCite). No project file was edited.*

---

## 1. Claims inventory

Legend for "Reproduced": **exact** = recomputed to the stated precision; **near** = within rounding or a defensible variant; **transcribed** = matches the source document (not independently computable); **no** = could not reproduce or not supported; **n/a** = qualitative.

| # | Slide | Claim | Should come from | Reproduced | Value obtained / note |
|---|---|---|---|---|---|
| 1 | 1 | 52 PIs report NIMH collaborations | `pi_collabs_FY2025.csv`, notebook graph nodes | near | 51 investigators *report* ≥1 NIMH collaborator; 52 = graph nodes (51 reporters + Plenz, who is only named by others). Same definition as 2019/2022 decks. |
| 2 | 1 | 405 intramural collaborations | same | exact | 405 rows (= 448 raw − 38 drop-list − 5 self-edges). Rows are person-mentions: 381 unique (PI, person) pairs; 133 unique people; 297 directed / 225 undirected PI–PI pairs. |
| 3 | 1 | ~8 per investigator | 405/52 | exact | 7.8 (405/52); 7.5 if /54. |
| 4 | 1 | Network figure (headshots) | notebook | not re-rendered | 52 nodes consistent with claim 1. |
| 5 | 2 | 48 PIs report IRP collaborations outside NIMH | csv | exact | 48. |
| 6 | 2 | 315 IRP collaborations beyond NIMH | csv | exact | 315 (raw = curated; 298 unique PI–person pairs). |
| 7 | 2 | ~6 per investigator | 315/54 | exact | 5.8 (/54); 6.6 per reporting PI (/48). |
| 8 | 2 | (figure) 21 ICs | csv | exact | 21 partner ICs incl. CC and OD. |
| 9 | 2 | **Rendered text "NIMH315 IRP collaborations…"** | slide XML | — | Text corruption present in the file (paragraph split after "outside", "NIMH" glued to "315"). Not present in the `2026-09-04.pptx` version. |
| 10 | 3 | 562 external collaborations | csv | exact | 562 (531 unique PI–person pairs). |
| 11 | 3 | More than 340 institutions | csv `institute` strings | **no** | 343 raw strings; 268 after dropping department suffixes; ~257 after school/medical-center variants (Harvard = 4 strings, UC = 15, Stanford = 7, Yale = 7, Penn = 7, Maryland = 6). |
| 12 | 3 | ~10 per IRP investigator | 562/54 | exact | 10.4 (/54); 12.0 per reporting PI (/47). |
| 13 | 3 | Reported by 47 of 54 PIs | csv + scrape cache | exact | 47; roster 54 = 42 Principal Investigators + 12 Lead Investigators. |
| 14 | 3 | Map | `institution_geocodes.csv` | exact | 342 of 343 strings geocoded (252 distinct coordinates). |
| 15 | 4 | Bars 326/332/405, 303/290/315, 470/464/562 | ANALYSIS.md, prior decks | exact (FY2025); transcribed (FY2018/21) | FY2018 and FY2021 match the 2019 and 2022 Town Hall decks exactly. |
| 16 | 4 | Collaborations rose in every scope in FY2025 | raw scrapes FY2021 vs FY2025 | near (aggregate) | +22% / +9% / +21% curated; +19% / +9% / +21% raw. Median continuing investigator: +1 / 0 / 0. Top-3 gainers = 54/70, 22/25, 78/96 of raw growth. |
| 17 | 4 | …after holding flat from FY2018 to FY2021 | published totals | exact | 326→332, 303→290, 470→464. |
| 18 | 4 | Reported by 54 investigators, consistent across rounds | notebook outputs (FY2018/21), cache (FY2025) | **no** | 57 (FY2018), 55 (FY2021), 54 (FY2025). |
| 19 | 5 | Same partner institutions in both lenses: Harvard, Hopkins, Penn, Maryland, Stanford | Library p.3 top-20 vs EM strings | exact | All five present in FY2025 external partners (17, 10, 14, 14, 12 rows). 17 of the Library's top-20 found (NINDS is NIH-scope; Ohio, USC absent). |
| 20 | 5 | The same network hubs appear in both | Library p.5 vs FY2025 within-NIMH degree | **no** | FY2025 hubs: Pereira 23, Allen-Worthington 23, Dold 19, Bandettini 17, Pao 16, Thomas 15, Zarate 15. Library hubs: Pine (deg 12), Zarate (15), Brotman (5), Merikangas (8), Thurm (10), Raznahan (8). Only Zarate is a hub in both. |
| 21 | 6 | 1,187 publications in five years | Library p.9 | transcribed | Re-run WoS export: 1,194 unique UTs (30 with PY 2026); 1,165 with PY ≤ 2025. Drift expected. |
| 22 | 6 | a steady ~220 per year | Library p.2 chart | **no** | 299, 216, 228, 232, 212. Mean 237; 2021 is 35% above the 2022–25 mean (222). |
| 23 | 6 | from 54 investigators | — | **no** | Library searched a requestor-supplied name list over 2021–25 that includes departed investigators (Lisanby 33 docs, Leibenluft, Kircanski). Not the FY2025 roster of 54. |
| 24 | 6 | 76% co-authored with universities | Library p.3 (76.1%, "estimated", InCites org-type filter) | transcribed | Should read "estimated". |
| 25 | 6 | 43.5% with international co-authors | Library p.3 | transcribed | ✓ |
| 26 | 6 | top partners UC system, Harvard, Johns Hopkins | Library p.3 (130/124/87) | transcribed | ✓ |
| 27 | 6 | Chart 299/216/228/232/212 | Library p.2 | transcribed; near from RIS | Re-export reproduces 300/218/232/234/211 only when a paper is assigned to min(publication year, early-access year). |
| 28 | 7 | 27,937 citations | Library p.9 (1,187 pubs) | transcribed | ✓ |
| 29 | 7 | institutional H-index 68 | Library p.9 | transcribed | ✓ |
| 30 | 7 | median IRP paper cited ~56% more than median NIH-funded paper in its field (RCR 1.56) | Library p.9 (1,142 pubs with PMIDs) | transcribed / wording | RCR = field-normalized citations *per year* vs NIH **R01**-funded benchmark. |
| 31 | 7 | 19.3% in top citation decile | Library p.9 (19.33% of 1,169) | transcribed | ✓; donut Top 1% 4% + Top 10% 16% = 20% consistent. |
| 32 | 7 | roughly twice parity | Library note 11 (10% expected) | exact | 1.93×. |
| 33 | 8 | 117 health-policy documents, 32 clinical guidelines | Library p.9/11; BMJ xlsx | exact | BMJ export: 153 rows, 149 unique documents (4 duplicates as Library stated) = 117 + 32. |
| 34 | 8 | (WHO, NICE, AAP, and others) | BMJ "Results" sheet | **no** | Source counts: UNESCO 25, French Government Ministries 13, National Academies 9, City of San Francisco 6, UK Govt 4, INESSS 4+1, Australian DVA 4, UK Parliament 4 … WHO **2**, American Academy of Pediatrics **1**, NICE **0**. |
| 35 | 8 | 30 patent documents cite IRP work | Library p.9 (PatCite, 1,178 pubs) | transcribed | Not independently checkable. |
| 36 | 8 | Chart 8/37/11/23/25/13 by year | Library p.11 | transcribed | ✓ (BMJ export by year: 12/40/17/31/29/18 — Library's chart appears to use a different date field; not the deck's doing). |
| 37 | 9 | 60% of NIMH IRP papers purely human vs 33% rest of IRP | `translation_triangle.py` | exact | 59.9% (565/944) vs 33.4% (6,714/20,081). |
| 38 | 9 | p < 0.001 | same | exact | z = 16.7. |
| 39 | 9 | the portfolio's most distinctive feature | per-IC recomputation | qualified | NIMH ranks 3rd of 24 ICs on human-only share (NIMHD 89%, NINR 85%, NIMH 60%, NINDS 50%, CC 49%). Pooled comparator is 27% NCI, 14% NIAID. |
| 40 | 9 | Stable across 2021–2025 (no significant drift) | same | near | 63.9 → 57.5 → 67.4 → 51.5 → 58.4%. 2021–22 vs 2024–25: 61.1% vs 54.8%, z = 1.8, p ≈ 0.07; Cochran–Armitage trend p ≈ 0.10. |
| 41 | 9 | full bench-to-bedside range retained | figure | n/a | Points along the animal–molecular edge exist; qualitative. |
| 42 | 9 | n = 944 / n = 20,081 | same | exact | ✓ |
| 43 | 9 | 94–97% had MeSH terms | same | exact | NIMH by year 0.94–0.97; groups 0.955 / 0.965. |
| 44 | 9 | 130 papers cross-listed appear in both panels | same | exact | 130. Removing them from the comparator leaves 33.4%. |
| 45 | 9 | Bubble area scales with share | code | exact | `s = share·2600 + 4` (area units). Coordinates snapped independently to a 1/24 lattice (see minor findings). |
| 46 | 9 | Cohorts = papers listed in NIH intramural annual reports, report-years 2021–2025 | `triangle_cohorts.csv` vs tarball | exact | Cohort = each PMID counted once in its **first** report-year (825/825 match). 2023 NIMH cohort is therefore small (150; 141 with MeSH). |
| 47 | 10 | Papers with data-sharing statements 7% (2019) → 31% (2025) | collected CSV + tarball + RIS | exact | 6.9% (15/217) → 31.3% (67/214), all seven points reproduce with "unique PMIDs within each report-year" (no cross-year dedup): 6.9, 9.1, 14.7, 15.1, 24.9, 24.9, 31.3. |
| 48 | 10 | PIs with ≥1 open-data paper 28% → 79% | same + PMID→PI | near | 27.5% (11/40) exact; 2019–2024 points reproduce (28.3, 42.2, 50.0, 60.0, 54.5); 2025: I get 72.7% (32/44) vs 79.1% (34/43) — 2025 PMID→PI table not in the repo. |
| 49 | 10 | Manual verification of 2023 pubs: true rate 40% (150 of 209 checked) | manual xlsx | exact but mixed denominators | 40.0% (60/150) is the manual rate on pubs **first** listed in 2023; automated rate on that same set is 28.8%. The plotted 2023 point (24.9%) is on all 216 pubs listed in 2023 reports, whose manual rate is 37.0%. "150 of 209" mixes the two sets. |
| 50 | 10 | the automated trend is conservative | sens/spec arithmetic | partly | With sens 0.57 / spec 0.94 the detector overstates when true prevalence < 12.5%; Rogan–Gladen: 2019 ≈ 2%, 2023 ≈ 44%, 2025 ≈ 47%. Slope understated; early levels overstated. |
| 51 | 10 | Linear fits | figure | n/a | 7 bounded points; 2023→2024 flat (24.9 → 24.9). |
| 52 | 11 | 86 reports, 54 PIs | `nimh_fy2025_ipids.csv`, cache | exact | 86 ipids (confirmed by hand search 2026-08-11); 54 investigators = 42 PIs + 12 Lead Investigators. |
| 53 | 11 | trend uses identical code on FY2018/FY2021 archives | notebook cell 71; ANALYSIS.md | **no** | Notebook hard-codes the *published* FY2018/FY2021 totals. FY2021 re-scrape with current code: NIMH raw 378 (published 332 post-curation), NIH 290 (exact), EM 466 vs 464. FY2018 never re-derived. |
| 54 | 11 | WoS author search 2021–2025 (NIH Library); windows differ FY vs CY | Library p.1 | transcribed | ✓ good caveat. |
| 55 | 11 | publisher PDFs → minerU → OddPub v7.2.3, uniform across 2019–2025 | — | not checkable | Contradicted in the same bullet ("earlier years partly author manuscripts"). Tool chain uniformity cannot be verified from the CSV (no version column); 2025 rows carry a distinct `source = staging` label (151 of 167). |
| 56 | 11 | against 213 manually verified pubs: 94% specificity, 57% sensitivity | manual xlsx × collected CSV | exact (n=209) | Primary sheet: n = 209, sens 57.1%, spec 93.9%. "Copy" sheet: n = 213, sens 56.4%, spec 93.3%. The quoted 94/57 belong to n = 209. |
| 57 | 11 | reported rates understate true sharing | see #50 | partly | True for 2021 onward; false for 2019–2020 under the measured operating characteristics. |
| 58 | 11 | 2025 used publisher PDFs (earlier years partly author manuscripts) | — | not checkable | Consistent with `source` labels; input change coincides with the largest single-year PI jump (54.5% → 79%). |
| 59 | 1–4 footer | "building on Dylan Nielson's 2019 and 2022 analyses" | emails/decks | exact | ✓ |
| 60 | 5–8 footer | "Bibliometrics: Joelle Mornini, NIH Library (Aug 2026)" | report | exact | ✓ |
| 61 | 9 footer | attribution | — | n/a | Fine after edit3 rewording. |
| 62 | 11 footer | GitHub URL | repo | exact | `nimh-dsst/nimh_irp_clustering`, branch `fy2025-refresh` (branch not named on slide). |

---

## 2. Findings, ranked

### FATAL — claim is wrong or unsupportable as written

**F1. Slide 8 — "(WHO, NICE, AAP, and others)".**
The BMJ Impact Analytics export attached to the Library's email (`2026-07-20_BMJ citing policy documents and matched references.xlsx`, Results sheet, 149 unique documents) contains **no NICE document at all**, 2 WHO documents and 1 American Academy of Pediatrics document. The citing corpus is dominated by UNESCO (25), French Government Ministries (13), the National Academies (9), the City of San Francisco (6), UK Government / UK Parliament briefings (4+4+2), INESSS Québec (5), Australian DVA (4). Didi Cross will open the same export. *Smallest fix:* "(UNESCO, national health ministries and agencies in France, the UK, Canada and Australia, the US National Academies, WHO, and others)" — or drop the parenthetical.

**F2. Slide 5 — "the same network hubs appear in both".**
The Library's individual co-authorship hubs are Pine, Zarate, Brotman, Merikangas, Thurm, Raznahan. In the FY2025 reported-collaboration network their degrees are 12, 15, 5, 8, 10, 8. The FY2025 hubs are Pereira (23, Machine Learning Team), Allen-Worthington (23, veterinary), Dold (19, instrumentation), Bandettini (17, fMRI core), Pao (16), Thomas (15, DSST), Zarate (15). Only Zarate is a hub in both. The two lenses disagree on hubs — which is actually the more interesting finding (declared collaboration is anchored by cores and services; co-authorship by clinical PIs). *Smallest fix:* delete "and the same network hubs appear in both", or replace with "the network hubs differ: core facilities anchor declared collaboration, clinical investigators anchor co-authorship".

**F3. Slide 11 — "trend uses identical code on FY2018/FY2021 archives".**
Notebook cell 71 hard-codes `published = {2018: {...326, 303, 470}, 2021: {...332, 290, 464}}` with the comment "FY2018 and FY2021 are the numbers as delivered". ANALYSIS.md states neither earlier round can be re-run. The FY2021 regression re-scrape with the current code gives raw within-NIMH 378 (published 332 is post-curation with a different drop list), NIH 290 (exact), EM 466 (published 464). FY2018 was never re-derived. *Smallest fix:* "trend compares each round's published totals; the FY2021 reports were re-scraped with the current code and matched within 1% on the two uncurated scopes."

**F4. Slide 2 — rendered bullet reads "NIMH315 IRP collaborations beyond NIMH".**
Introduced in `_edit3` (the paragraph break landed after "outside" and "NIMH" was glued to "315"); confirmed in `ppt/slides/slide2.xml`. The `2026-09-04.pptx` version is correct. A garbled headline number on slide 2 of a leadership deck is disqualifying on its own. *Fix:* restore "48 PIs report IRP collaborations outside NIMH" / "315 IRP collaborations beyond NIMH".

### MATERIAL — an expert would dispute it or demand a caveat

**M1. Slide 4 — "Collaborations rose in every scope in FY2025."**
True in aggregate (curated +22% / +9% / +21%; raw +19% / +9% / +21%), but not a broad-based change:
- Roster turnover: 43 investigators appear in both rounds; 12 departed (72 / 59 / 94 rows in FY2021) and 11 arrived (75 / 66 / 112 rows in FY2025). Net roster effect is small and positive.
- Among the 43 continuing investigators the **median change is +1 (NIMH), 0 (NIH), 0 (EM)**; 25/21/18 increased, 12/12/14 decreased.
- Concentration: the three largest gainers account for 54 of the 70-row raw NIMH increase (Pereira +34, Zarate +10, Thomas +10), 22 of 25 for NIH (Buckley +8, Zarate +8, Wong +6) and 78 of 96 for EM (Zarate +41, Bandettini +20, Pao +17). Excluding the top-3 gainers, continuing investigators changed by +13 / −4 / 0.
- Carry-forward: 44% of FY2025 NIMH rows, 48% of NIH rows and 36% of EM rows are (investigator, name) pairs already present in FY2021; 10 of 118 investigator×scope lists are byte-identical.
*Smallest fix:* add "growth is concentrated in a few investigators; the median investigator's counts are unchanged" (or show a per-investigator median alongside the totals).

**M2. Slide 4 — "Reported by 54 investigators, consistent across rounds."**
The rosters were 57 (FY2018), 55 (FY2021), 54 (FY2025) (from the notebook's own saved outputs: 326/5.719 = 57, 332/6.036 = 55). Per-investigator means therefore rose slightly more than the totals (NIMH 5.7 → 6.0 → 7.5). *Fix:* "54–57 investigators per round".

**M3. Slide 3 — "More than 340 institutions."**
343 is the count of distinct *strings* in the External Collaborators field, which carry department and school suffixes. Collapsing text after the first comma gives 268; also collapsing "School of Medicine / Medical Center / Health System" variants gives ~257. Harvard alone is 4 strings, the UC campuses 15, Stanford 7, Yale 7, Penn 7, Maryland 6. The FY2018/FY2021 "more than 300" had the same inflation. *Fix:* "more than 250 institutions (343 as named in reports)".

**M4. Slide 6 — "a steady ~220 per year from 54 investigators."**
(a) The Library's own chart is 299, 216, 228, 232, 212: five-year mean 237, and 2021 is 35% above the 2022–25 mean; "steady ~220" describes 2022–25 only. (b) "from 54 investigators" is unsupported: the Library searched a requestor-supplied author list over CY2021–2025 that includes investigators who have left (Lisanby appears with 33 documents and 1,542 citations in the report's top-20 authors; Leibenluft and Kircanski are in its network), while the 54 FY2025 investigators include 12 Lead Investigators who are unlikely to be on that list. *Fix:* "~240 publications a year (216–232 in 2022–25) by current and former NIMH IRP investigators"; drop "54".

**M5. Slide 9 — "Stable across 2021–2025 (no significant drift)."**
Human-only share by report-year: 63.9%, 57.5%, 67.4%, 51.5%, 58.4%. Early (2021–22) vs late (2024–25): 61.1% vs 54.8%, z = 1.8, p ≈ 0.07; Cochran–Armitage trend p ≈ 0.10. Not significant, but a 6-point decline at p ≈ 0.07 is not "stable", and the 2023 cohort is only 141 papers because cohorts count each paper in its first report-year. *Fix:* "no statistically significant change (61% in 2021–22 vs 55% in 2024–25, p ≈ 0.07)".

**M6. Slide 9 — "the portfolio's most distinctive feature" / choice of comparator.**
Against the pooled rest of the IRP (27% NCI, 14% NIAID) the contrast is real and reproduces (59.9% vs 33.4%, z = 16.7). But per IC, NIMH ranks third: NIMHD 88.8%, NINR 85.4%, NIMH 59.9%, NINDS 49.7%, CC 49.3%. A bibliometrician will ask for the per-IC distribution. *Fix:* "vs 33% for the rest of the IRP pooled; among ICs with sizeable output only NIMHD and NINR are more human-focused".

**M7. Slide 10 — "Manual verification of 2023 pubs found the true rate is higher still (40%)" and the star label "150 of 209 pubs checked".**
The 40.0% (60/150) is the manual rate on the 150 publications *first listed* in FY2023 reports; on that same set the automated rate is 28.8%. The plotted 2023 point (24.9%) uses all 216 publications listed in 2023 reports (209 with results), whose manual rate is 37.0%. The slide pairs the manual rate of one set with the automated rate of another, stretching the gap from 11–12 points to 15. "150 of 209" conflates the two sets (all 216 listed pubs were manually checked, not 150 of 209). *Fix:* star at 37% with "216 pubs listed in 2023, all manually checked" — or compare 40% vs 29% on the 150-pub set.

**M8. Slides 10–11 — "the automated trend is conservative" / "reported rates understate true sharing".**
With sensitivity 0.57 and specificity 0.94 the detector's expected output is 0.06 + 0.52·p; it *overstates* whenever true prevalence is below 12.5%. A Rogan–Gladen correction of the plotted points gives 2019 ≈ 2%, 2020 ≈ 9%, 2021 ≈ 18%, 2023 ≈ 44%, 2025 ≈ 47%: the slope is understated (roughly doubled after correction), the recent levels are understated, but the 2019–2020 levels are *over*stated. Additionally the operating characteristics were measured on 2022–23 publications processed from the 2019–2024 PDF stock; applying them to 2025, where 151 of 167 results come from a new publisher-PDF batch (`source = staging`), assumes sensitivity did not change — it almost certainly rose, which is the same direction as the 2025 jump. *Fix:* "the detector compresses the trend: after correcting for 57% sensitivity / 94% specificity, the 2025 rate is closer to ~47%", and move "2025 inputs differ" next to the 2025 point rather than to the methods slide.

**M9. Slide 10 — PI metric "28% → 79%".**
(a) Denominator is investigators with ≥1 publication *with an OddPub result* in that year (40–46 per year), not the roster; a PI with 1 covered paper and one with 26 (2025 max) count equally, so the metric is mechanically sensitive to paper counts. (b) The 2025 point is the only one I could not reproduce: 2019–2024 match exactly (27.5, 28.3, 42.2, 50.0, 60.0, 54.5) but I get 32/44 = 72.7% for 2025 vs the deck's 34/43 = 79.1%, because the FY2025 PMID→investigator mapping (irp_scraper `publications_2025.csv`, private) is not in the repo or tarball; I attributed 188 of 214 RIS PMIDs via DOI matching against report text. (c) The 2024→2025 PI jump (+24.6 pts) is four times the paper-level change (+6.4 pts) and coincides with the PDF-source change. *Fix:* state the denominator in the axis label, commit the 2025 PMID–PI table so the point is reproducible, and consider a robustness line (PIs with ≥3 covered papers).

**M10. Slide 10 — what "papers" means.**
The plotted paper points use every PMID listed in a given year's reports; 263 of 1,396 NIMH PMIDs (19%) are listed in two or three report-years and count in each. The earlier Colab/Pao figure (`IRP Open Data 7p1.ipynb`, `drop_duplicates(["PMID"])`) counted each paper once in its first year, which yields 6.9, 10.5, 15.4, 16.1, 28.8, 25.6, 30.5 — a different 2023 (28.8 vs 24.9). Either convention is defensible; the deck should say which. The denominator is publications with a retrievable PDF (94–100% of listed PMIDs per year in the v7.2.3 run — good), but the earlier v7.1 run had 68–99% coverage, so the two figures are not directly comparable. *Fix:* axis label "publications listed in that year's annual reports"; footnote the convention.

**M11. Slide 11 — internal contradiction and the 213.**
"publisher PDFs → minerU → OddPub v7.2.3, uniform across 2019–2025" is contradicted three clauses later by "2025 used publisher PDFs (earlier years partly author manuscripts)". What is uniform is the tool chain; the inputs are not. "213 manually verified pubs" is the overlap using the "Copy of NIMH_IRP_2023" sheet, where sens/spec are 56.4% / 93.3%; the quoted 57% / 94% correspond to the primary sheet's 209-publication overlap (TP 44, FN 33, FP 8, TN 124). *Fix:* "same tool chain (minerU + OddPub v7.2.3) on all years; PDF sources differ by year" and "209".

**M12. Slides 1–3 — what a "collaboration" is.**
Headline counts are collaborator *listings*: a person named on two or three reports of the same investigator counts once per report. Unique (investigator, person) pairs are 381 / 298 / 531 against 405 / 315 / 562 (5–6% double counting). Within NIMH, the 405 listings name 133 people (many are staff, e.g. "Kurt Braunlich"), mapped to 297 directed / 225 undirected PI–PI links. Prior rounds used the same convention, so the trend is internally consistent, but the word "collaborations" invites the reading "distinct partnerships". *Fix:* footnote "collaborator listings in annual reports; a collaborator named on several of an investigator's reports counts once per report".

**M13. Slide 8 — concentration and the report's own footnote conflict.**
76 of 1,178 searched publications (6.5%) have any policy mention; two consortium papers ("Brain charts for the human lifespan", 34 mentions; "Neurodevelopment of the association cortices", 25) account for 59 of 216 mention-instances (27%). The Library report is internally inconsistent — p.9 footnote says "Of 122 publications searched in BMJ Impact Analytics", note 14 says 1,178 publications / 1,170 DOIs / 1,143 PMIDs. The deck inherits whichever is right. *Fix:* add "(76 publications cited)" and ask the Library to resolve 122 vs 1,178 before OSPPC sees the report.

> **Resolution (2026-09-11):** Jenny asked; Joelle confirmed the 122 was a typo carried over from a template spreadsheet and issued a corrected report (`…_2021_2025_corrected.pdf`). The corrected PDF differs from the original in exactly that one line — all 1,178 publications were searched in BMJ Impact Analytics — so the 117 / 32 / 76 figures are complete counts, not lower bounds, and slide 8 needs no change.

**M14. Slide 1 — "52 PIs report NIMH collaborations".**
51 investigators report ≥1 NIMH collaborator; the 52nd node (Plenz) is only named by others. Same convention as the 2019/2022 decks ("54"/"53" were also node counts), so the trend is consistent, but the verb is wrong. *Fix:* "52 PIs connected by reported collaborations" or "51 PIs report…".

### MINOR — wording, precision, presentation

- **Slides 1–3, per-investigator denominators.** Slide 1 divides by reporting PIs (405/52 = 7.8), slides 2–3 divide by the whole roster (315/54 = 5.8; 562/54 = 10.4). Per reporting PI the latter are 6.6 and 12.0. Pick one convention and state it.
- **"PIs" vs "investigators".** The 54 are 42 Principal Investigators + 12 Lead Investigators (cores, staff scientists, the veterinarian). Use "investigators" throughout, as slide 4 already does.
- **Slide 6, "76% co-authored with universities".** The Library labels this an *estimate* from an InCites organization-type filter (note 4). Say "an estimated 76%".
- **Slide 6, per-year chart.** The Library's bars assign papers to the earlier of publication year and early-access year (my re-export reproduces 300/218/232/234/211 only under that rule). If the deck quotes "per year", "by first online year" is the accurate label.
- **Slide 7, RCR gloss.** RCR is field-normalized citations *per year* benchmarked to NIH **R01**-funded papers; 1.56 is the median of the 1,142 publications with PMIDs found in iCite (of 1,187). "Cited ~56% more per year than the median NIH R01-funded paper in its field" is accurate; the current wording drops "per year" and the R01 benchmark. Also note three denominators on the slide (1,187 WoS; 1,169 InCites; 1,142 iCite) and that 2024–25 RCRs and percentiles are provisional (the report says so on p.1).
- **Slide 9, lattice snapping.** Human, animal and molecular coordinates are each rounded to 1/24 independently, so a snapped point need not sum to 1 (small off-simplex displacements); the vertex bubble absorbs everything with human ≥ 0.979. Neither changes the printed shares (59.9% / 33.4% either way). Cosmetic.
- **Slide 9, n for 2023.** Because cohorts take each paper's first report-year, the 2023 NIMH cohort is 150 (141 with MeSH). State "unique papers, first report-year" in the footer.
- **Slide 10, "keeps rising".** 2023 → 2024 is flat (24.9% → 24.9%); "has risen" or "has quadrupled since 2019" is safer. A straight line through seven bounded proportions is a visual aid, not a model; fine as long as no slope is quoted.
- **Slide 11, footer.** The repo link should name the branch (`fy2025-refresh`); master does not contain the FY2025 work.
- **WoS re-run drift.** A fresh export returns 1,194 unique records (30 dated 2026); the report's 1,187 is a July 2026 snapshot. Expected; worth one clause if numbers are ever re-quoted.

---

## 3. Claims that are solid (leave alone)

- FY2025 totals **405 / 315 / 562**, **48** PIs (NIH scope), **47 of 54** (external), **86 reports**, **21 partner ICs** — all reproduce exactly from `pi_collabs_FY2025.csv` and independently from `fy2025_scrape_cache.json` (448 raw − 38 drop-list − 5 self-edges = 405; NIH and EM untouched by curation).
- FY2018 and FY2021 bars on slide 4 match the 2019 and 2022 Town Hall decks exactly; "flat from FY2018 to FY2021" is correct.
- Slide 5's five named institutions all appear among FY2025 external partners with double-digit listings; 17 of the Library's top-20 institutions are present (substring matching, generous). The institution convergence claim stands.
- Every number transcribed from the Library report (1,187; 76.1%; 43.5%; 27,937; 68; 1.56; 19.33%; 117; 32; 30; per-year and per-year-policy charts) is transcribed faithfully.
- Slide 9's **59.9% vs 33.4%**, **n = 944 / 20,081**, **p < 0.001** (z = 16.7), **94–97% MeSH coverage**, **130 cross-listed** all reproduce from the committed script and cache; the cache matches the live iCite API on 10 spot-checked PMIDs; the cohort table is exactly the first-report-year dedup of the Colab tarball.
- Slide 10's paper-level series reproduces to the decimal at all seven points (variant: unique PMIDs per report-year); PI-level 2019–2024 reproduce exactly; OddPub validation **sens 57.1% / spec 93.9%, n = 209** reproduces; the ANALYSIS.md check "v7.1 vs v7.2.3 agree on 95.3% of 1,048" reproduces exactly.
- Coverage in the v7.2.3 run is 94–100% of listed PMIDs every year, so "papers without a PDF" is not a hidden denominator problem for slide 10.

---

## 4. What I could not check, and why

- **The Library's WoS author list and search strategy** (report notes 15–16 link to WoS saved searches, not accessible). Consequently "from 54 investigators" (slide 6) and the coverage of the 1,187 cannot be verified, and the FY-vs-CY offset cannot be quantified.
- **InCites percentile/RCR/PatCite computations** — proprietary; transcription checked only.
- **BMJ Report PDF** — text is font-encoded and unreadable via `pdftotext`; the two xlsx exports were used instead (they are the underlying data).
- **The HPC pipeline** (minerU → OddPub v7.2.3 on Biowulf): tool version, PDF provenance per year, and whether 2019–2024 results used the same PDFs as the v7.1 run. The collected CSV has no version or input-type column; the only trace is `source ∈ {v2store, staging}`.
- **The FY2025 PMID→investigator mapping** used for the 2025 PI point (irp_scraper `publications_2025.csv`, private repo). My DOI-based reconstruction attributes 188 of 214 PMIDs and gives 72.7%, not 79.1%.
- **FY2018 re-scrape.** The FY2018 HTML archives are in `data/`, but the trend cell does not use them and I did not re-parse them; the FY2018 bars rest on the January 2019 deck.
- **The "~15 of top 20" statement in ANALYSIS.md** — checked only by substring matching, which has known artifacts ("ucl" ↔ UCLA, "Columbia" ↔ British Columbia). Not on the slide itself.
- **Whether NIDB records for FY2025 have been edited since the 11 Aug 2026 scrape** — ANALYSIS.md documents ~13% row drift on FY2021 over four years; not re-scraped here.

---

## Appendix A — recomputed tables

**A1. Slide-10 paper series, three denominators (NIMH, OddPub v7.2.3 results)**

| Year | unique PMIDs listed that year | covered | open | **share (deck)** | first-year dedup share (Colab convention) | v7.1 pdftools share (tarball) |
|---|---|---|---|---|---|---|
| 2019 | 219 | 217 | 15 | **6.9%** | 6.9% | 5.5% |
| 2020 | 253 | 242 | 22 | **9.1%** | 10.5% | 9.2% |
| 2021 | 277 | 265 | 39 | **14.7%** | 15.4% | 13.1% |
| 2022 | 272 | 259 | 39 | **15.1%** | 16.1% | 12.7% |
| 2023 | 216 | 209 | 52 | **24.9%** | 28.8% | 26.9% |
| 2024 | 218 | 217 | 54 | **24.9%** | 25.6% | 20.7% |
| 2025 | 214 | 214 | 67 | **31.3%** | 30.5% | — |

Rogan–Gladen corrected (sens 0.579, spec 0.940) from the deck series: 1.7%, 6.0%, 16.7%, 17.5%, 36.4%, 36.4%, 48.7%.

**A2. Slide-10 PI series (PIs with ≥1 covered paper → share with ≥1 open-data paper)**

| Year | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| PIs with covered paper | 40 | 46 | 45 | 42 | 40 | 44 | 44 |
| with ≥1 open | 11 | 13 | 19 | 21 | 24 | 24 | 32 |
| share (mine) | 27.5% | 28.3% | 42.2% | 50.0% | 60.0% | 54.5% | 72.7% |
| deck | 28% | ~28% | ~42% | ~50% | ~60% | ~55% | **79%** |

**A3. Manual validation (`Manually labelled pubs from NIMH IRP 2023.xlsx`)**

| Sheet | pubs | overlap with v7.2.3 | TP / FN / FP / TN | sens | spec | manual rate | auto rate |
|---|---|---|---|---|---|---|---|
| NIMH_IRP_2023 | 216 | 209 | 44 / 33 / 8 / 124 | 57.1% | 93.9% | 36.8% | 24.9% |
| Copy of NIMH_IRP_2023 | 224 | 213 | 44 / 34 / 9 / 126 | 56.4% | 93.3% | 36.6% | 24.9% |

By first report-year of the labelled pubs: 2021 n=9; 2022 n=57 (manual 28.1%); **2023 n=150 (manual 40.0%, automated 28.8%)**; all 216 pubs listed in 2023 reports: manual 37.0%, automated 24.9%.

**A4. FY2021 → FY2025 raw change decomposition (scrape caches)**

| Scope | raw FY2021 | raw FY2025 | continuing 43 PIs | departed 12 PIs (FY2021 rows) | new 11 PIs (FY2025 rows) | top-3 gainers | median Δ (continuing) |
|---|---|---|---|---|---|---|---|
| NIMH | 378 | 448 | 306 → 373 (+67) | 72 | 75 | Pereira +34, Zarate +10, Thomas +10 | +1 |
| NIH | 290 | 315 | 231 → 249 (+18) | 59 | 66 | Buckley +8, Zarate +8, Wong +6 | 0 |
| EM | 466 | 562 | 372 → 450 (+78) | 94 | 112 | Zarate +41, Bandettini +20, Pao +17 | 0 |

**A5. Human-only share by IC (rest-of-IRP cohort, report-years 2021–25, papers with MeSH)**
NIMHD 88.8% (224) · NINR 85.4% (41) · **NIMH 59.9% (944)** · NINDS 49.7% (862) · CC 49.3% (720) · NCCIH 47.2% · NIAMS 46.7% · NIAAA 43.4% · NHGRI 43.3% · NIA 42.5% · NIEHS 40.1% · NICHD 39.9% · NLM 35.2% · NCI 33.6% (5,430) · NEI 32.5% · NHLBI 31.8% · NIDDK 27.2% · NIDA 26.8% · NIDCD 20.1% · NIDCR 19.7% · NCATS 18.0% · NIBIB 13.6% · NIAID 12.9% (2,895).

**A6. Citing policy documents by source (BMJ export, 149 unique documents)**
UNESCO 25 · French Government Ministries 13 · National Academies 9 · City of San Francisco 6 · INESSS 5 · UK Government 4 · Australian DVA 4 · UK Parliament Research Briefings 4 · OECD 3 · Guidelines in PMC 3 · Federatie Medisch Specialisten 3 · RANZCP 3 · State of Maryland 3 · NHS Trusts 3 · … · **World Health Organization 2** · **American Academy of Pediatrics 1** · **NICE 0**. Document types after dedup: 112 policy documents, 30 clinical guidelines, 7 other (working papers, decision support, legal, periodical, scholarly) — the Library's 117 + 32 folds the 7 into the two classes.
