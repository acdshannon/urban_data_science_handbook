# The Urban Data Science Handbook

*Methods, models, and the world's cities.*

A graduate-level textbook surveying the methods of urban science and data science — statistics, machine learning, spatial analysis, networks, mobility, causal inference, scaling, simulation, economics, deep learning on imagery, language models, and the politics and climate stakes of it all. Practical and rigorous: real analyses, real assumptions, no ritual proofs.

**Every chapter is anchored in a world city and a verified open dataset.** We learn statistics in Amsterdam, machine learning in Melbourne, networks in Tokyo, causal inference in London, segregation models in Cape Town. See [`TABLE_OF_CONTENTS.md`](TABLE_OF_CONTENTS.md) for the full design: chapters, sub-chapters, anchor datasets, and verification notes.

| # | Chapter | Anchor city | Anchor data |
|---|---------|-------------|-------------|
| 1 | The City as a Data System | *the world* | GHSL Urban Centre Database |
| 2 | The Urban Data Toolkit | New York | 311 service requests |
| 3 | Statistical Foundations | Amsterdam | Inside Airbnb + CBS neighborhoods |
| 4 | Machine Learning for Cities | Melbourne | Pedestrian sensor counts |
| 5 | Spatial Statistics | Mexico City | Crime investigations + marginalization index |
| 6 | Urban Networks | Tokyo | Rail network (MLIT/ODPT) + OSM streets |
| 7 | Human Mobility & Transportation | São Paulo | Origin–Destination survey + GTFS |
| 8 | Causal Inference for Urban Policy | London | Air quality network × congestion pricing |
| 9 | Scaling, Complexity & the Science of Cities | *every city at once* | GHSL UCDB + OECD metros |
| 10 | Simulating the City: Agent-Based Models | Cape Town | Census small-area population groups |
| 11 | Urban Economics & the Value of Location | Singapore | HDB resale transactions |
| 12 | Seeing the City: Deep Learning & Urban Imagery | Nairobi | Sentinel-2, Open Buildings, Mapillary |
| 13 | Reading the City: LLMs & Urban Text | Barcelona | Decidim citizen proposals |
| 14 | Data, Power & the Right to the City | Chicago | Strategic Subject List (predictive policing) |
| 15 | The Climate-Stressed City | Jakarta | Flood reports + Sentinel-1 + exposure grids |
| — | Coda: Toward a Science of Cities | — | — |

## Building the book

This is a [Quarto](https://quarto.org) book (the second edition of a project that began as a Jupyter Book, keeping its Tufte-inspired design: navy and gold, ET Book, margin notes).

```bash
# install quarto >= 1.7, then:
quarto preview        # live-reloading local build
quarto render         # static build to _book/
```

Python environment for the analyses (as chapters gain code):

```bash
pip install -r requirements.txt
```

## Repository layout

```
_quarto.yml            book structure & format config
index.qmd              preface
chapters/              one .qmd per chapter
appendices/            setup, data-portal atlas, math refresher, data engineering
styles/                light & dark themes (Tufte-inspired identity)
references.bib         bibliography
TABLE_OF_CONTENTS.md   the full annotated design document
```

## Status

Early scaffold: structure, chapter abstracts, and anchor datasets are in place and verified; analyses are being written chapter by chapter.
