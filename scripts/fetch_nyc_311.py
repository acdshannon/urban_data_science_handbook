"""Build the Chapter 2 snapshots from NYC Open Data (Socrata).

Run from the repository root:  python scripts/fetch_nyc_311.py

Produces, under data/snapshots/nyc_311/:
  daily_by_type.csv      daily complaint counts for selected types, 2024-2025
  type_totals.csv        total counts by complaint type, 2024-2025
  rhythms.csv            counts by (type, day-of-week, hour), 2024-2025
  rat_sightings.csv      point-located rat sightings, 2025
  nta_2020.geojson       Neighborhood Tabulation Area boundaries (2020)
  nta_population.csv     2020 census population by NTA
  MANIFEST.md            what was fetched, when, and how

All queries use server-side SoQL aggregation, so nothing here downloads more
than a few megabytes. An app token is unnecessary at these volumes.
"""

import json
import sys
import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "snapshots" / "nyc_311"
OUT.mkdir(parents=True, exist_ok=True)

DOMAIN = "https://data.cityofnewyork.us"
DATASET_2020S = "erm2-nwe9"  # 311 Service Requests from 2020 to Present
START, END = "2024-01-01", "2026-01-01"

# The complaint types the chapter follows. Chosen for seasonal character,
# volume, and variety of agency. (Names must match the portal exactly.)
TYPES = [
    "Noise - Residential",
    "Noise - Street/Sidewalk",
    "HEAT/HOT WATER",
    "Illegal Parking",
    "Illegal Fireworks",
    "Rodent",
    "Dirty Condition",
    "Street Condition",
    "Christmas Tree Removal",
    "Dead Tree",
    "Snow or Ice",
    "Blocked Driveway",
]


def soql(dataset: str, query: dict, paginate: bool = True) -> pd.DataFrame:
    """Run a SoQL query with paging; return all rows as a DataFrame."""
    url = f"{DOMAIN}/resource/{dataset}.json"
    frames, offset, page = [], 0, 50_000
    while True:
        params = dict(query)
        if paginate:
            params["$limit"] = page
            params["$offset"] = offset
        r = requests.get(url, params=params, timeout=120)
        r.raise_for_status()
        rows = r.json()
        frames.append(pd.DataFrame(rows))
        if not paginate or len(rows) < page:
            break
        offset += page
        time.sleep(0.5)
    return pd.concat(frames, ignore_index=True)


def in_list(values):
    quoted = ", ".join("'" + v.replace("'", "''") + "'" for v in values)
    return f"complaint_type in ({quoted})"


def main():
    window = f"created_date >= '{START}' and created_date < '{END}'"

    print("type_totals…")
    totals = soql(
        DATASET_2020S,
        {
            "$select": "complaint_type, count(*) as n",
            "$where": window,
            "$group": "complaint_type",
            "$order": "n DESC",
        },
    )
    totals.to_csv(OUT / "type_totals.csv", index=False)

    print("daily_by_type…")
    daily = soql(
        DATASET_2020S,
        {
            "$select": "date_trunc_ymd(created_date) as day, complaint_type, count(*) as n",
            "$where": f"{window} and {in_list(TYPES)}",
            "$group": "day, complaint_type",
            "$order": "day",
        },
    )
    daily.to_csv(OUT / "daily_by_type.csv", index=False)

    print("rhythms…")
    rhythms = soql(
        DATASET_2020S,
        {
            "$select": (
                "complaint_type, date_extract_dow(created_date) as dow, "
                "date_extract_hh(created_date) as hour, count(*) as n"
            ),
            "$where": f"{window} and {in_list(['Noise - Residential', 'Rodent', 'Illegal Parking', 'HEAT/HOT WATER'])}",
            "$group": "complaint_type, dow, hour",
        },
    )
    rhythms.to_csv(OUT / "rhythms.csv", index=False)

    print("rat_sightings…")
    rats = soql(
        DATASET_2020S,
        {
            "$select": "unique_key, created_date, descriptor, borough, latitude, longitude",
            "$where": (
                "created_date >= '2025-01-01' and created_date < '2026-01-01' "
                "and complaint_type = 'Rodent' and descriptor = 'Rat Sighting' "
                "and latitude IS NOT NULL"
            ),
        },
    )
    rats.to_csv(OUT / "rat_sightings.csv", index=False)

    print("nta boundaries…")
    # 2020 Neighborhood Tabulation Areas (water-clipped)
    r = requests.get(
        f"{DOMAIN}/api/geospatial/9nt8-h7nd",
        params={"method": "export", "format": "GeoJSON"},
        timeout=300,
    )
    r.raise_for_status()
    (OUT / "nta_2020.geojson").write_text(r.text)

    print("nta population…")
    # Census 2020 demographics at NTA level
    pop = soql(
        "rnsn-acs2",
        {"$select": "*", "$limit": "500"},
        paginate=False,
    )
    pop.to_csv(OUT / "nta_population.csv", index=False)

    manifest = f"""# NYC 311 snapshot

Fetched: {date.today().isoformat()}
Source: NYC Open Data, dataset `{DATASET_2020S}` (311 Service Requests from
2020 to Present), via SoQL aggregation; NTA 2020 boundaries (`9nt8-h7nd`);
census demographics by NTA (`rnsn-acs2`).
Window: {START} to {END} (rat sightings: 2025 only).
License: NYC Open Data Terms of Use (free use, no registration).
Rows: totals={len(totals)}, daily={len(daily)}, rhythms={len(rhythms)}, rats={len(rats)}.
Rebuild: `python scripts/fetch_nyc_311.py` from the repository root.
"""
    (OUT / "MANIFEST.md").write_text(manifest)
    print("done.")


if __name__ == "__main__":
    sys.exit(main())
