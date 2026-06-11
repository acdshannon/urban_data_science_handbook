"""Build the Chapter 3 snapshots: Inside Airbnb Amsterdam + CBS neighborhoods.

Run from the repository root:  python scripts/fetch_amsterdam.py

Inside Airbnb publishes quarterly scrapes of every Airbnb listing, but only
the trailing year stays freely downloadable — so the book pins one snapshot
(2025-09-11) and mirrors what the chapter needs. CBS (Statistics Netherlands)
supplies neighborhood population via the Wijk- en Buurtkaart service on PDOK;
its ~500 Amsterdam buurten are aggregated by centroid into the 22 areas
Inside Airbnb uses, which are the city's own "gebieden".

  data/snapshots/amsterdam_airbnb/
    listings.parquet     one row per listing, trimmed to the chapter's columns,
                         price parsed to numeric EUR (the portal's "$" is
                         formatting, not currency)
    areas.geojson        the 22 Inside Airbnb areas (city "gebieden")
    area_population.csv  residents per area, aggregated from CBS buurten
    MANIFEST.md

Skips any output that already exists; delete a file to refetch it.
"""

import io
import json
import sys
from datetime import date
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "snapshots" / "amsterdam_airbnb"
OUT.mkdir(parents=True, exist_ok=True)

SNAPSHOT = "2025-09-11"  # the pinned scrape; later ones at insideairbnb.com/get-the-data
BASE = f"https://data.insideairbnb.com/the-netherlands/north-holland/amsterdam/{SNAPSHOT}"
PDOK = "https://service.pdok.nl/cbs/wijkenbuurten/2024/wfs/v1_0"

COLUMNS = [
    "id", "host_id", "host_listings_count", "host_is_superhost",
    "neighbourhood_cleansed", "latitude", "longitude",
    "property_type", "room_type", "accommodates", "bedrooms", "beds",
    "bathrooms", "bathrooms_text", "amenities", "price", "minimum_nights",
    "number_of_reviews", "reviews_per_month", "review_scores_rating",
    "license",
]


def get(url, **kw):
    r = requests.get(url, timeout=300, **kw)
    r.raise_for_status()
    return r


def fresh(name: str) -> bool:
    if (OUT / name).exists():
        print(f"{name} exists; skipping (delete it to refetch)")
        return False
    print(f"{name}…")
    return True


def main():
    if fresh("listings.parquet"):
        raw = pd.read_csv(io.BytesIO(get(f"{BASE}/data/listings.csv.gz").content),
                          compression="gzip", low_memory=False)
        df = raw[COLUMNS].rename(columns={"neighbourhood_cleansed": "area"})
        df["price"] = df["price"].str.replace(r"[$,]", "", regex=True).astype(float)
        df.to_parquet(OUT / "listings.parquet", index=False)
        print(f"  {len(df):,} listings, {df.price.notna().sum():,} with a price")

    if fresh("areas.geojson"):
        (OUT / "areas.geojson").write_bytes(
            get(f"{BASE}/visualisations/neighbourhoods.geojson").content
        )

    if fresh("area_population.csv"):
        # CBS buurten (with key figures) for the Amsterdam bounding box, in
        # RD New; PDOK's WFS takes no attribute filter, so trim client-side.
        r = get(
            PDOK,
            params={
                "service": "WFS", "version": "2.0.0", "request": "GetFeature",
                "typeNames": "wijkenbuurten:buurten",
                "outputFormat": "application/json", "count": 1000,
                "bbox": "109000,476000,136000,498000,urn:ogc:def:crs:EPSG::28992",
            },
        )
        buurten = gpd.GeoDataFrame.from_features(json.loads(r.text), crs="EPSG:28992")
        buurten = buurten[buurten.gemeentenaam == "Amsterdam"]
        buurten["pop"] = buurten.aantalInwoners.clip(lower=0)  # -99997 = missing

        areas = gpd.read_file(OUT / "areas.geojson").to_crs("EPSG:28992")
        pts = buurten.copy()
        pts["geometry"] = pts.geometry.centroid
        joined = gpd.sjoin(pts, areas[["neighbourhood", "geometry"]],
                           how="inner", predicate="within")
        pop = (joined.groupby("neighbourhood")["pop"].sum().astype(int)
               .rename("population").reset_index().rename(columns={"neighbourhood": "area"}))
        pop.to_csv(OUT / "area_population.csv", index=False)
        print(f"  {len(buurten)} buurten → {len(pop)} areas, "
              f"{pop.population.sum():,} residents")

    listings = pd.read_parquet(OUT / "listings.parquet")
    pop = pd.read_csv(OUT / "area_population.csv")
    manifest = f"""# Inside Airbnb Amsterdam snapshot

Fetched: {date.today().isoformat()}
Source: Inside Airbnb (insideairbnb.com), Amsterdam scrape of {SNAPSHOT},
`listings.csv.gz` (detailed) and `neighbourhoods.geojson` — CC BY 4.0.
Only the trailing year of scrapes stays freely downloadable, hence this
pinned mirror. Prices are nightly displayed rates in euros (the source
file's "$" is formatting); {listings.price.isna().sum():,} of
{len(listings):,} listings carry no price because they had no bookable
availability at scrape time.
Population: CBS Wijk- en Buurtkaart 2024 via PDOK WFS (CC BY 4.0),
{pop.population.sum():,} residents across {len(pop)} areas, aggregated
from buurt centroids to Inside Airbnb's 22 areas (the city's gebieden).
Rebuild: `python scripts/fetch_amsterdam.py` from the repository root.
"""
    (OUT / "MANIFEST.md").write_text(manifest)
    print("done.")


if __name__ == "__main__":
    sys.exit(main())
