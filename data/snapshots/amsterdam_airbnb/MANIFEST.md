# Inside Airbnb Amsterdam snapshot

Fetched: 2026-06-10
Source: Inside Airbnb (insideairbnb.com), Amsterdam scrape of 2025-09-11,
`listings.csv.gz` (detailed) and `neighbourhoods.geojson` — CC BY 4.0.
Only the trailing year of scrapes stays freely downloadable, hence this
pinned mirror. Prices are nightly displayed rates in euros (the source
file's "$" is formatting); 4,606 of
10,480 listings carry no price because they had no bookable
availability at scrape time.
Population: CBS Wijk- en Buurtkaart 2024 via PDOK WFS (CC BY 4.0),
904,755 residents across 22 areas, aggregated
from buurt centroids to Inside Airbnb's 22 areas (the city's gebieden).
Rebuild: `python scripts/fetch_amsterdam.py` from the repository root.
