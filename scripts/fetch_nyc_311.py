"""Build the Chapter 2 snapshots from NYC Open Data (Socrata).

Run from the repository root:  python scripts/fetch_nyc_311.py

Produces, under data/snapshots/nyc_311/:
  daily_by_type.csv      daily complaint counts for selected types, 2024-2025
  type_totals.csv        total counts by complaint type, 2024-2025
  rhythms.csv            counts by (type, day-of-week, hour), 2024-2025
  rat_sightings.csv      point-located rat sightings, 2025
  nta_2020.geojson       Neighborhood Tabulation Area boundaries (2020)
  nta_population.csv     census population by NTA (2010 vintage; see note below)
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
# volume, and variety of agency. (Names must match the portal exactly —
# e.g. "Dead Tree" was renamed "Dead/Dying Tree" sometime in the 2010s,
# and "Christmas Tree Removal" has never been a complaint type at all.)
TYPES = [
    "Noise - Residential",
    "Noise - Street/Sidewalk",
    "HEAT/HOT WATER",
    "Illegal Parking",
    "Illegal Fireworks",
    "Rodent",
    "Dirty Condition",
    "Street Condition",
    "Damaged Tree",
    "Dead/Dying Tree",
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
        # Cold aggregation queries can take minutes server-side; be patient
        # and retry once or twice before giving up.
        for attempt in range(3):
            try:
                r = requests.get(url, params=params, timeout=300)
                r.raise_for_status()
                break
            except requests.RequestException:
                if attempt == 2:
                    raise
                time.sleep(15 * (attempt + 1))
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


def soql_by_quarter(select: str, group: str, where_extra: str = "") -> pd.DataFrame:
    """A grouped query, one quarter at a time, summed client-side.

    Full-window aggregations over this table routinely outlast the server's
    patience; quarterly ones never do, and their sum is the same table.
    """
    quarters = pd.date_range(START, END, freq="QS")
    frames = []
    for q0, q1 in zip(quarters[:-1], quarters[1:]):
        where = f"created_date >= '{q0:%Y-%m-%d}' and created_date < '{q1:%Y-%m-%d}'"
        if where_extra:
            where += f" and {where_extra}"
        frames.append(
            soql(
                DATASET_2020S,
                {"$select": select, "$where": where, "$group": group},
            )
        )
        print(f"  {q0:%Y-%m}…", flush=True)
    keys = [k.strip() for k in group.split(",")]
    out = pd.concat(frames, ignore_index=True)
    out["n"] = out["n"].astype(int)
    return out.groupby(keys, as_index=False)["n"].sum()


def fresh(name: str) -> bool:
    """Skip outputs that already exist — delete a file to refetch it."""
    if (OUT / name).exists():
        print(f"{name} exists; skipping (delete it to refetch)")
        return False
    print(f"{name}…")
    return True


def main():
    if fresh("type_totals.csv"):
        totals = soql_by_quarter(
            select="complaint_type, count(*) as n",
            group="complaint_type",
        ).sort_values("n", ascending=False, ignore_index=True)
        totals.to_csv(OUT / "type_totals.csv", index=False)

    if fresh("daily_by_type.csv"):
        daily = soql_by_quarter(
            select="date_trunc_ymd(created_date) as day, complaint_type, count(*) as n",
            group="day, complaint_type",
            where_extra=in_list(TYPES),
        ).sort_values("day", ignore_index=True)
        daily.to_csv(OUT / "daily_by_type.csv", index=False)

    if fresh("rhythms.csv"):
        rhythms = soql_by_quarter(
            select=(
                "complaint_type, date_extract_dow(created_date) as dow, "
                "date_extract_hh(created_date) as hour, count(*) as n"
            ),
            group="complaint_type, dow, hour",
            where_extra=in_list(
                ["Noise - Residential", "Rodent", "Illegal Parking", "HEAT/HOT WATER"]
            ),
        )
        rhythms.to_csv(OUT / "rhythms.csv", index=False)

    if fresh("rat_sightings.csv"):
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

    if fresh("nta_2020.geojson"):
        # 2020 Neighborhood Tabulation Areas (water-clipped)
        r = requests.get(
            f"{DOMAIN}/api/geospatial/9nt8-h7nd",
            params={"method": "export", "format": "GeoJSON"},
            timeout=300,
        )
        r.raise_for_status()
        (OUT / "nta_2020.geojson").write_text(r.text)

    if fresh("nta_population.csv"):
        # Census demographics at NTA level (`rnsn-acs2`). 2010-vintage: 2000/2010
        # populations keyed by 2010 NTA codes. The portal hosts no 2020-census-by-
        # NTA2020 table; DCP publishes that only as Excel on nyc.gov. Joining this
        # to the 2020 boundaries therefore needs a crosswalk — see Exercise 3.
        pop = soql(
            "rnsn-acs2",
            {"$select": "*", "$limit": "500"},
            paginate=False,
        )
        pop.to_csv(OUT / "nta_population.csv", index=False)

    rows = {
        name: len(pd.read_csv(OUT / f"{name}.csv"))
        for name in ["type_totals", "daily_by_type", "rhythms", "rat_sightings"]
    }
    manifest = f"""# NYC 311 snapshot

Fetched: {date.today().isoformat()}
Source: NYC Open Data, dataset `{DATASET_2020S}` (311 Service Requests from
2020 to Present), via SoQL aggregation; NTA 2020 boundaries (`9nt8-h7nd`);
census demographics by NTA (`rnsn-acs2` — 2010 vintage, 2000/2010 populations
keyed by 2010 NTA codes; the portal has no 2020-census-by-NTA2020 table).
Window: {START} to {END} (rat sightings: 2025 only).
License: NYC Open Data Terms of Use (free use, no registration).
Rows: totals={rows["type_totals"]}, daily={rows["daily_by_type"]},
rhythms={rows["rhythms"]}, rats={rows["rat_sightings"]}.
Rebuild: `python scripts/fetch_nyc_311.py` from the repository root.
"""
    (OUT / "MANIFEST.md").write_text(manifest)
    print("done.")


if __name__ == "__main__":
    sys.exit(main())
