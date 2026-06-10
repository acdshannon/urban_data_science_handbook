# The Urban Data Science Handbook — Table of Contents (Design Document)

*Second-edition design, June 2026. This document is the working blueprint: chapter themes, sub-chapters, anchor cities and datasets (each verified against the live web in June 2026), pedagogical furniture, and the mapping from the first-edition Jupyter Book.*

---

## Design commitments

- **Platform:** Quarto book (successor to the Jupyter Book edition), keeping the first edition's design identity — navy/gold/teal Tufte-inspired theme, ET Book serif, JetBrains Mono, margin notes — with a healthy PDF path for an eventual print edition.
- **Shape:** 15 chapters + an unnumbered coda + 4 appendices, organized in 7 narrative parts. Semester-shaped: one chapter ≈ one week, each with 4–6 sub-chapters.
- **Audience:** graduate students and practitioners with working Python and one stats course. Chapter 2 aligns everyone quickly; Appendices A/C/D carry anyone who needs more runway.
- **City anchoring:** one headline city and dataset per chapter, with cross-city cameos where they earn their place; the scaling chapter is deliberately *every city at once*. Fourteen anchors across six continents.
- **Data rules:** all anchor datasets are open; free registrations/API keys allowed but minimized (only Copernicus, SPTrans, ODPT-optional, OneMap, Mapillary, DataFirst). The repo ships pinned snapshots of every anchor so analyses stay reproducible as portals drift.
- **Chapter furniture:** every chapter carries (1) end-of-chapter exercises in graded difficulty, (2) an annotated further-reading shelf, and (3) a boxed **theory sidebar** tying the methods to classic urban thought.
- **Tone:** a rigorous survey — practical application first, math where it illuminates, no ritual proofs, no hand-waving about assumptions.

## The tour at a glance

| # | Chapter | Methods | Anchor city | Anchor dataset (verified June 2026) |
|---|---------|---------|-------------|--------------------------------------|
| 1 | The City as a Data System | framing, distributions, first maps | 🌍 the world | GHSL Urban Centre Database R2024A |
| 2 | The Urban Data Toolkit | pandas/GeoPandas, APIs, viz grammar | 🇺🇸 New York | 311 Service Requests (2010–19 + 2020–) |
| 3 | Statistical Foundations | distributions, testing, regression, Bayes | 🇳🇱 Amsterdam | Inside Airbnb + CBS neighborhoods |
| 4 | Machine Learning for Cities | ensembles, forecasting, clustering, anomalies | 🇦🇺 Melbourne | Pedestrian Counting System (2009–) |
| 5 | Spatial Statistics | autocorrelation, point patterns, spatial regression | 🇲🇽 Mexico City | Carpetas de investigación + CONAPO marginalization |
| 6 | Urban Networks | graphs, centrality, percolation, multilayer | 🇯🇵 Tokyo | MLIT N02 rail network (+ ODPT, OSM) |
| 7 | Human Mobility & Transportation | OD matrices, gravity/radiation, GTFS accessibility | 🇧🇷 São Paulo | Metrô OD Survey 2017 & 2023 + SPTrans GTFS |
| 8 | Causal Inference for Urban Policy | DiD, synthetic control, spatial RDD | 🇬🇧 London | LAQN air quality × congestion charge & ULEZ |
| 9 | Scaling, Complexity & the Science of Cities | Zipf, scaling laws, fractals | 🌍 every city | GHSL UCDB + OECD FUA economy dataflows |
| 10 | Simulating the City: Agent-Based Models | Schelling, calibration, epidemics, LUTI | 🇿🇦 Cape Town | Stats SA Census 2011 Small Area Layer |
| 11 | Urban Economics & the Value of Location | bid-rent, hedonics, agglomeration, complexity | 🇸🇬 Singapore | HDB Resale Flat Prices (1990–) + OneMap |
| 12 | Seeing the City: Deep Learning & Urban Imagery | CNNs, segmentation, change detection | 🇰🇪 Nairobi | Sentinel-2 + Open Buildings + WorldPop + Mapillary |
| 13 | Reading the City: LLMs & Urban Text | embeddings, LLM annotation, generative agents | 🇪🇸 Barcelona | Decidim citizen proposals (CA/ES) |
| 14 | Data, Power & the Right to the City | fairness audits, privacy, governance | 🇺🇸 Chicago | Strategic Subject List (Historical) |
| 15 | The Climate-Stressed City | hazard/exposure/vulnerability, flood mapping | 🇮🇩 Jakarta | PetaBencana + Satu Data floods + Sentinel-1 |
| — | Coda: Toward a Science of Cities | synthesis, open problems | — | — |

Continental spread: North America ×3, South America ×1, Europe ×3, Asia ×3, Africa ×2, Oceania ×1, global ×2.

---

## Part I · Foundations

### 1. The City as a Data System — *the world's cities*

Why cities, why data, why now. Opens global: one table containing every urban centre on Earth.

1.1 Why cities, why data, why now · 1.2 A brief history of counting the city (censuses → sensors → satellites) · 1.3 What is a city, exactly? (administrative/morphological/functional definitions) · 1.4 The world's cities in one table (first maps and distributions from the UCDB) · 1.5 How to read this book

- **Anchor:** [GHSL Urban Centre Database R2024A](https://human-settlement.emergency.copernicus.eu/ghs_ucdb_2024.php) — 11,422 urban centres, 473 indicators, 1975–2030, CC BY 4.0, keyless download. Cameo: UN World Urbanization Prospects.
- **Theory sidebar:** Jane Jacobs — the city as a problem of *organized complexity*.

### 2. The Urban Data Toolkit — *New York City*

The book's skills alignment, taught through the "hello world" of civic data: 311.

2.1 The stack, quickly (pandas/GeoPandas in urban context) · 2.2 Portals and APIs (Socrata/CKAN ecosystems; paging, tokens) · 2.3 Shapes of the city (projections, spatial joins) · 2.4 A visual grammar for urban data (the book's house style) · 2.5 Reproducibility and the snapshot discipline

- **Anchor:** NYC 311 Service Requests — 40M+ records, split across [2020–present](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9) and [2010–2019](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-2019/76ig-c548); no registration (the recent dataset split is itself taught as portal archaeology).
- **Theory sidebar:** what does a complaint measure? Reporting propensity vs. underlying conditions.

## Part II · Pattern & Prediction

### 3. Statistical Foundations — *Amsterdam*

Statistics the way cities serve it: skewed, heavy-tailed, politically charged. Anchored in Europe's most contested short-term-rental market.

3.1 Urban distributions and their heavy tails · 3.2 Describing neighborhoods (robust summaries, inequality indices) · 3.3 Uncertainty, sampling, and the bootstrap · 3.4 Comparison and testing (and the multiple-comparisons trap) · 3.5 Regression I: hedonic pricing of the city · 3.6 Bayesian thinking: borrowing strength across neighborhoods

- **Anchor:** [Inside Airbnb Amsterdam](https://insideairbnb.com/amsterdam/) — CC BY 4.0, quarterly snapshots (trailing year free; book pins + mirrors one), joined to [CBS Wijk- en Buurtkaart](https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data) neighborhood statistics (CC BY 4.0).
- **Theory sidebar:** the contested platform city — the "Airbnb effect" literature and Amsterdam's regulatory experiments.

### 4. Machine Learning for Cities — *Melbourne*

The prediction toolkit on one of the world's longest-running urban sensing programs — with COVID lockdowns as the canonical anomaly.

4.1 Prediction versus explanation · 4.2 Trees, forests, and boosting · 4.3 Urban rhythms: time series and forecasting · 4.4 Cities without labels: clustering and embedding street personalities · 4.5 The day everything changed: anomaly detection · 4.6 Honest evaluation: leakage in space and time

- **Anchor:** [Melbourne Pedestrian Counting System](https://data.melbourne.vic.gov.au/explore/dataset/pedestrian-counting-system-monthly-counts-per-hour/) — hourly counts, 60–100+ sensors, 2009–present, CC BY 4.0, keyless (2009–2022 archive ZIP + live API).
- **Theory sidebar:** Whyte's Street Life Project and Gehl's public-life surveys — the clipboard tradition the sensors automated.

### 5. Spatial Statistics — *Mexico City*

Space as signal. Latin America's richest open crime data meets a census-based deprivation index.

5.1 Tobler's law and spatial weights · 5.2 Global and local autocorrelation (Moran's I, LISA, hot spots) · 5.3 Point patterns (KDE, Ripley's K) · 5.4 Spatial regression (lag/error; crime vs. marginalization) · 5.5 The modifiable areal unit problem

- **Anchor:** [Carpetas de investigación FGJ-CDMX](https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico) — ~2M point-located investigations since 2016, monthly updates, keyless; joined to [CONAPO urban marginalization index 2020](https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372) at AGEB level.
- **Theory sidebar:** from Burgess's concentric zones to Shaw & McKay — a century of crime cartography and what it criminalized.

## Part III · Structure & Flow

### 6. Urban Networks — *Tokyo*

Network science on the world's densest rail system: which five stations matter most?

6.1 The city as graph · 6.2 Street networks and urban morphology (OSMnx; 30-city cameo gallery) · 6.3 Centrality: where the city concentrates · 6.4 Communities and cores · 6.5 Breaking the network: resilience and percolation · 6.6 Multilayer and temporal networks

- **Anchor:** [MLIT National Land Numerical Information N02 rail data](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-2025.html) — all lines/stations as GeoJSON, keyless, gov't open license (CC BY 4.0-compatible); N05 edition adds network history since 1950. Optional extension: [ODPT](https://developer.odpt.org/) timetables (free registration). Streets via OSM/OSMnx.
- **Theory sidebar:** Christopher Alexander, "A City Is Not a Tree."

### 7. Human Mobility & Transportation — *São Paulo*

Mobility laws, flow models, and the accessibility turn — on South America's longest-running travel survey.

7.1 Laws of motion (travel-time budgets, the daily pulse) · 7.2 Gravity and radiation (fit to observed OD) · 7.3 Timetables as data: GTFS and accessibility (r5py isochrones, access to jobs) · 7.4 Unequal mobility (accessibility by income/race/zone) · 7.5 New sensors of movement (NYC taxi cameo; privacy hand-off to ch. 14)

- **Anchor:** [Metrô-SP Origin–Destination Survey](https://transparencia.metrosp.com.br/dataset/pesquisa-origem-e-destino) — public microdata for 2017 *and* the 2023 edition (published Jan 2025), keyless; [SPTrans GTFS](https://www.sptrans.com.br/desenvolvedores/) (free registration); IBGE census geography.
- **Theory sidebar:** Marchetti's constant — the universal travel-time budget and its limits under imposed commutes.

## Part IV · Causes & Laws

### 8. Causal Inference for Urban Policy — *London*

Twenty years of pricing the city's own air, recorded by a hundred monitors: the perfect causal classroom.

8.1 Why correlation fails in cities · 8.2 Potential outcomes and natural experiments · 8.3 Difference-in-differences (the staged ULEZ rollout) · 8.4 Synthetic control (the 2003 Congestion Charge) · 8.5 Borders and thresholds: spatial regression discontinuity · 8.6 What evaluation cannot see

- **Anchor:** [London Air Quality Network](https://www.londonair.org.uk/Londonair/API/) — hourly NO₂/PM at 100+ stations since 1993, open API, no key (educational-use license; Defra [AURN](https://uk-air.defra.gov.uk/data/) under OGL as fully-open companion); zone boundaries & traffic context via [TfL open data](https://tfl.gov.uk/info-for/open-data-users/) (free key).
- **Theory sidebar:** John Snow's London — the founding natural experiment of urban science.

### 9. Scaling, Complexity & the Science of Cities — *every city at once*

The book's "laws" chapter: the regularities of the urban system, and the craft of fitting them honestly.

9.1 Zipf and the size of cities · 9.2 Urban scaling (Bettencourt–West, superlinear and sublinear) · 9.3 Why scaling? Interaction and agglomeration · 9.4 Fractal cities (box-counting on built form) · 9.5 Ranking cities fairly (scale-adjusted indicators)

- **Anchor:** [GHSL UCDB R2024A](https://human-settlement.emergency.copernicus.eu/ghs_ucdb_2024.php) (CC BY 4.0) + [OECD Cities & FUA dataflows](https://data-explorer.oecd.org/) (GDP/jobs for FUAs >250k; free SDMX API — note: the legacy "Metropolitan areas" database is archived; the book targets the current FUA dataflow IDs).
- **Theory sidebar:** from mouse to metropolis — Kleiber's law and whether cities are "social reactors."

## Part V · Models & Markets

### 10. Simulating the City: Agent-Based Models — *Cape Town*

Schelling's emergent segregation collides with a city where segregation was engineered — the collision is the point.

10.1 Emergence and the bottom-up city · 10.2 Schelling from scratch (Mesa) · 10.3 Measuring real segregation (dissimilarity/entropy on census small areas) · 10.4 When the model meets the city (calibration; why the fit fails informatively) · 10.5 Contagion on networks (SIR; COVID's lessons) · 10.6 The big simulators (LUTI, MATSim, digital twins)

- **Anchor:** Stats SA **Census 2011 Small Area Layer** via [DataFirst](https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/517) — population-group counts for ~5.5k Cape Town small areas; free registration. (Census 2022 small areas are not yet open — ward level only; revisit when released.)
- **Theory sidebar:** Micromotives, macrobehavior — and the Group Areas Act: emergence must not become an alibi for design.

### 11. Urban Economics & the Value of Location — *Singapore*

Why cities exist and what location costs, taught on a near-census of a housing market with a built-in present-value experiment (lease decay).

11.1 Why cities exist: agglomeration · 11.2 Land and location: bid-rent (price–distance gradients) · 11.3 Hedonic regression: pricing the unpriceable · 11.4 Housing policy in the data (Ethnic Integration Policy; cooling measures as natural experiments) · 11.5 The economic complexity of cities

- **Anchor:** [HDB Resale Flat Prices](https://data.gov.sg/collections/189/view) — ~1M transactions 1990–present incl. remaining lease, Singapore Open Data Licence, keyless; geocoding via [OneMap API](https://www.onemap.gov.sg/apidocs/) (free registration).
- **Theory sidebar:** the isolated state, downtown — von Thünen to Alonso.

## Part VI · Seeing & Reading the City

### 12. Seeing the City: Deep Learning & Urban Imagery — *Nairobi*

Practical deep learning on satellite and street imagery, pointed where it matters most: the fast-growing, under-mapped city.

12.1 The view from above: remote sensing primer · 12.2 Convolutional networks, briefly (transfer learning) · 12.3 Watching Nairobi grow (Sentinel-2 change detection) · 12.4 The informal city (Open Buildings over Kibera; dasymetric population with WorldPop) · 12.5 The view from the street (Mapillary; coverage bias as a finding) · 12.6 Ground truth and its discontents (domain shift between cities)

- **Anchor stack:** [Sentinel-2 via Copernicus Data Space](https://dataspace.copernicus.eu/) (free registration) · [Google Open Buildings v3 + 2.5D Temporal](https://sites.research.google/gr/open-buildings/) (footprints and heights 2016–2023; CC BY 4.0/ODbL) · [WorldPop](https://www.worldpop.org/) 100 m grids (CC BY 4.0) · [Mapillary](https://www.mapillary.com/developer) (free token, CC BY-SA).
- **Theory sidebar:** Scott's *Seeing Like a State* — legibility from above, counter-mapping (Map Kibera) from below.

### 13. Reading the City: LLMs & Urban Text — *Barcelona*

NLP and language models as research instruments, on the world's most-copied civic participation platform.

13.1 The city in words · 13.2 From bags of words to embeddings (multilingual: Catalan + Spanish in one space) · 13.3 Mapping citizen voice (clustering the demand map by district) · 13.4 Language models as research instruments (LLM annotation validated against hand-coding) · 13.5 Synthetic citizens? (generative agents meet ch. 10) · 13.6 Failure modes (hallucination, multilingual bias, reproducibility)

- **Anchor:** [Decidim Barcelona open-data export](https://www.decidim.barcelona/open-data) — tens of thousands of citizen proposals 2016–present with districts, supports, responses; keyless CSV + GraphQL API. Caveats: no prominent license statement (treated as attributed municipal open data) and occasional export outages — the book ships a frozen snapshot. Fallback corpus: Inside Airbnb Barcelona reviews (~1M, multilingual, CC BY 4.0).
- **Theory sidebar:** Arnstein's ladder of participation, digitized.

## Part VII · The City at Stake

### 14. Data, Power & the Right to the City — *Chicago*

The chapter where the book audits its own discipline — anchored in a real, public, decommissioned predictive policing score.

14.1 Who gets counted (undercounts; differential privacy at the census) · 14.2 Anatomy of a predictive policing system · 14.3 Auditing the algorithm (fairness definitions and impossibility results) · 14.4 Surveillance and re-identification (taxi de-anonymization callback) · 14.5 Governing urban algorithms (Amsterdam/Helsinki AI registers; CCOPS) · 14.6 The politics of open data

- **Anchor:** [Strategic Subject List — Historical](https://data.cityofchicago.org/Public-Safety/Strategic-Subject-List-Historical/4aki-r3np) — 398,684 de-identified scored records (2012–2016) with model inputs and demographics, keyless. Archived dataset: the book mirrors a snapshot. Companion: [NYPD Stop, Question & Frisk](https://www.nyc.gov/site/nypd/stats/reports-analysis/stopfrisk.page) (2003–present).
- **Theory sidebar:** Lefebvre's right to the city, read against the dashboard.

### 15. The Climate-Stressed City — *Jakarta*

The climate analyst's toolkit — hazard, exposure, vulnerability — in the planet's starkest urban case.

15.1 Hazard, exposure, vulnerability · 15.2 The sinking metropolis (subsidence; Sentinel-1 flood mapping; crowd reports as sensor network) · 15.3 Urban heat (LST; cameo tour of heat inequity) · 15.4 Who lives in the floodplain (exposure × social vulnerability) · 15.5 Deciding under uncertainty (scenarios; the new-capital question)

- **Anchor:** [PetaBencana](https://docs.petabencana.id/) flood report archives (open API, CC BY 4.0) + official per-event impact tables via [Satu Data Jakarta](https://satudata.jakarta.go.id/) and national catalog mirrors + Sentinel-1 (Copernicus, free registration) + WorldPop/GHSL exposure grids. (Legacy data.jakarta.go.id is decaying; the book cites successor portals.)
- **Theory sidebar:** Holling's resilience and its critics — resilience of what, for whom?

### Coda: Toward a Science of Cities *(unnumbered)*

The methods × cities matrix reprised; open problems (digital twins, foundation models, the Global South data gap, adaptation, evaluation); the annotated book shelf, carried over from the first edition; a closing argument about what the field is for.

## Appendices

- **A. Setting Up** — environment, geospatial stack, the one consolidated list of free registrations, the data-snapshot system.
- **B. An Atlas of Open Data Portals** — annotated directory by continent; aggregators; global layers; platform patterns (Socrata/CKAN/ArcGIS).
- **C. Mathematical Refresher** — probability, linear algebra to PageRank, logs & power laws, optimization in one page.
- **D. Data Engineering for Urban Analysts** — DuckDB/SQL, Parquet, polite APIs, scraping ethics, sensor streams.

---

## Mapping from the first edition

| First edition part | Where it lives now |
|---|---|
| 0. Introduction | Ch. 1 (+ preface) |
| 1. Statistical Foundations | Ch. 3 (causality promoted to Ch. 8) |
| 2. Advanced Stats & ML | Ch. 4 (Bayes → Ch. 3; time series → Ch. 4.3) |
| 3. Network Science | Ch. 6 (routing folded into 6.3/6.5) |
| 4. Geospatial Analytics | Ch. 5 (+ basics moved earlier, into Ch. 2) |
| 5. Complexity & Urban Science | Ch. 9 |
| 6. Urban Economics | Ch. 11 (game theory → sidebar material) |
| 7. Modeling | Ch. 10 (epidemics 10.5; LUTI 10.6) |
| 8. Gathering Good Data | distributed: portals/APIs → Ch. 2; satellite → Ch. 12; sensing → Ch. 4; SQL/scraping → App. D |
| 9. Architecture & Design | absorbed: morphology → Ch. 6.2; built form → Ch. 12 |
| 10. Governance & Policy | Ch. 14 (voting methods cut; participation → Ch. 13) |
| 11. Closing Thoughts (ethics, recs, limits) | Ch. 14 + Coda |
| 12. Additional Resources | Appendices A–D |
| *(new, not in first edition)* | Ch. 7 Mobility · Ch. 8 Causal inference · Ch. 12 Deep learning · Ch. 13 LLMs · Ch. 15 Climate |

## Dataset verification summary (June 2026)

All 15 anchors were verified against the live web in June 2026 (three research passes; URLs in each chapter stub). Statuses: **all exist and are accessible.** Flags worth tracking:

| Dataset | Status | Flag |
|---|---|---|
| GHSL UCDB | ✅ keyless, CC BY 4.0 | current version R2024A; watch for successor |
| NYC 311 | ✅ keyless | dataset split (2010–19 / 2020–) — old tutorials' URLs are stale |
| Inside Airbnb AMS | ✅ keyless, CC BY 4.0 | only trailing 12 months free → pin + mirror snapshot |
| Melbourne pedestrians | ✅ keyless, CC BY 4.0 | history = archive ZIP + live API (two-step); the live API serves a rolling ~2-year window, so Nov 2022 – Jun 2024 is currently unpublished — ch. 4 teaches the gap rather than hiding it |
| CDMX carpetas + CONAPO | ✅ keyless | geocoding partly to colonia centroids — note in text |
| Tokyo MLIT N02 | ✅ keyless, CC BY-compatible | ODPT optional (registration, ~2-day approval) |
| São Paulo OD + GTFS | ✅ OD keyless | **OD 2023 microdata now public** (use 2017+2023); GTFS needs free SPTrans account |
| London LAQN | ✅ keyless API | educational-use license (not OGL) → AURN as open companion |
| OECD FUA | ✅ keyless SDMX | legacy "Metropolitan areas" DB archived → use FUA dataflows |
| Stats SA Census SAL | ✅ free registration (DataFirst) | 2022 small areas not yet open → anchor on 2011 |
| Singapore HDB + OneMap | ✅ keyless (OneMap free reg) | none — exemplary portal |
| Nairobi stack | ✅ free reg (Copernicus, Mapillary) | Mapillary coverage uneven in informal areas → pre-check AOI |
| Barcelona Decidim | ✅ keyless export | license not stated + export outages → ship frozen snapshot |
| Chicago SSL | ✅ keyless | archived dataset — **mirror immediately**; SQF as fallback |
| Jakarta floods | ✅ keyless API | legacy city portal decaying → cite Satu Data successors |

**Standing action items:** mirror SSL and Decidim snapshots into `data/snapshots/` as the first data-engineering task; re-verify all anchors annually.

## Decisions log

1. **Licensing (decided June 2026):** text and figures CC BY-NC-SA 4.0 (`LICENSE-CONTENT.md`); code MIT (`LICENSE`); datasets under their original licenses.
2. **Hosting (decided June 2026):** GitHub Pages via Actions (`.github/workflows/publish.yml`), rendering from committed `_freeze/` so CI needs no Python. Enable Pages (Settings → Pages → Source: GitHub Actions) once.
3. **"Take it to your city" prompts** were considered and dropped from standard furniture — may return as an occasional feature.
4. **Writing order:** Chapters 2 and 4 first (in progress), then 3, 5, 6.
