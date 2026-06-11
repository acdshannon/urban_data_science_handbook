"""Build the Chapter 4 snapshots from the City of Melbourne open data portal.

Run from the repository root:  python scripts/fetch_melbourne.py

The Pedestrian Counting System lives in two pieces: a ZIP archive holding the
hourly history from May 2009 to 14 Dec 2022 attached to the dataset page, and
the live dataset, which carries a *rolling window* of roughly the last two
years (inspected June 2026: 2024-06-11 onward). Between the archive's end and
the window's start the published record simply has a hole — about eighteen
months the portal no longer serves. This script downloads both pieces,
normalizes them to one schema, and writes compact parquet snapshots:

  data/snapshots/melbourne_pedestrians/
    hourly.parquet        hourly counts, all sensors, both eras
                          (sensor_id, ts, count)
    sensors.csv           sensor id, description, location, install date
    MANIFEST.md

The full hourly table compresses to a manageable size in parquet; if that ever
stops being true, derive daily aggregates here instead and keep hourly for the
chapter's featured sensors only.
"""

import io
import sys
import zipfile
from datetime import date
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "snapshots" / "melbourne_pedestrians"
RAW = ROOT / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)

BASE = "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets"
COUNTS = "pedestrian-counting-system-monthly-counts-per-hour"
SENSORS = "pedestrian-counting-system-sensor-locations"


def get(url, **kw):
    r = requests.get(url, timeout=600, **kw)
    r.raise_for_status()
    return r


def fetch_archive() -> pd.DataFrame:
    """Find and download the 2009-2022 archive ZIP attached to the dataset.

    Archive schema: ID, Date_Time ("November 01, 2019 05:00:00 PM"), Year,
    Month, Mdate, Day, Time, Sensor_ID, Sensor_Name, Hourly_Counts. Only the
    timestamp, the sensor id, and the count survive normalization; the rest
    are derivable or live in sensors.csv.
    """
    meta = get(f"{BASE}/{COUNTS}/attachments").json()
    attachments = meta.get("attachments", meta if isinstance(meta, list) else [])
    zips = [a for a in attachments if a.get("href", a.get("url", "")).endswith(("zip", ".zip"))]
    if not zips:
        raise RuntimeError(f"no ZIP attachment found: {attachments!r}")
    href = zips[0].get("href") or zips[0]["url"]
    print(f"  archive: {href}")
    zpath = RAW / "melbourne_archive.zip"
    if not zpath.exists():
        zpath.write_bytes(get(href).content)
    frames = []
    with zipfile.ZipFile(zpath) as z:
        for name in z.namelist():
            if name.endswith(".csv") and not name.startswith("__MACOSX"):
                with z.open(name) as f:
                    frames.append(
                        pd.read_csv(f, usecols=["Date_Time", "Sensor_ID", "Hourly_Counts"])
                    )
    old = pd.concat(frames, ignore_index=True)
    return pd.DataFrame(
        {
            "sensor_id": old["Sensor_ID"].astype("int32"),
            "ts": pd.to_datetime(old["Date_Time"], format="%B %d, %Y %I:%M:%S %p"),
            "count": old["Hourly_Counts"].astype("int32"),
        }
    )


def fetch_live() -> pd.DataFrame:
    """Export the live rolling-window dataset as CSV via the Explore API.

    Live schema: id, location_id, sensing_date, hourday, direction_1,
    direction_2, pedestriancount, sensor_name, location. The live
    `location_id` is the archive's `Sensor_ID`; `pedestriancount` (both
    directions summed) is the archive's `Hourly_Counts`.
    """
    url = f"{BASE}/{COUNTS}/exports/csv"
    cpath = RAW / "melbourne_live.csv"
    if not cpath.exists():
        with requests.get(url, params={"delimiter": ","}, timeout=600, stream=True) as r:
            r.raise_for_status()
            with open(cpath, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 20):
                    f.write(chunk)
    new = pd.read_csv(cpath, usecols=["location_id", "sensing_date", "hourday", "pedestriancount"])
    return pd.DataFrame(
        {
            "sensor_id": new["location_id"].astype("int32"),
            "ts": pd.to_datetime(new["sensing_date"], format="ISO8601").dt.tz_localize(None)
            + pd.to_timedelta(new["hourday"], unit="h"),
            "count": new["pedestriancount"].astype("int32"),
        }
    )


def main():
    print("sensor locations…")
    sensors = pd.read_csv(
        io.StringIO(get(f"{BASE}/{SENSORS}/exports/csv", params={"delimiter": ","}).text)
    )
    sensors.to_csv(OUT / "sensors.csv", index=False)

    print("archive (2009-2022)…")
    old = fetch_archive()
    print(f"  {len(old):,} rows, {old.ts.min()} → {old.ts.max()}")

    print("live (rolling window)…")
    new = fetch_live()
    print(f"  {len(new):,} rows, {new.ts.min()} → {new.ts.max()}")

    print("reconciling…")
    # Keep the eras disjoint (the live window could one day grow back over
    # the archive), prefer live where both exist, and drop intra-source
    # duplicates from sensor replacements.
    combined = pd.concat([old[old.ts < new.ts.min()], new], ignore_index=True)
    combined = (
        combined.drop_duplicates(["sensor_id", "ts"], keep="last")
        .sort_values(["sensor_id", "ts"])
        .reset_index(drop=True)
    )
    combined.to_parquet(OUT / "hourly.parquet", index=False)
    gap = (new.ts.min() - old.ts.max()).days
    print(f"  {len(combined):,} rows; gap between eras: ~{gap} days")

    manifest = f"""# Melbourne Pedestrian Counting System snapshot

Fetched: {date.today().isoformat()}
Source: City of Melbourne open data portal, dataset `{COUNTS}`
(archive ZIP attachment for May 2009 - 14 Dec 2022; live export, which the
portal serves as a rolling window of roughly the last two years), plus
`{SENSORS}` for sensor metadata.
Coverage: {old.ts.min().date()} → {old.ts.max().date()} (archive) and
{new.ts.min().date()} → {new.ts.max().date()} (live). The ~{gap}-day hole
between the eras is the portal's, not ours: the archive froze (its label
says 14 Dec 2022; its rows stop earlier) and the rolling window has since
moved past it.
Schema: hourly.parquet has one row per (sensor_id, ts): sensor_id joins
sensors.csv `location_id`; count is pedestrians per hour, both directions.
License: CC BY 4.0.
Rows: archive={len(old):,}, live={len(new):,}, combined={len(combined):,}.
Rebuild: `python scripts/fetch_melbourne.py` from the repository root.
"""
    (OUT / "MANIFEST.md").write_text(manifest)
    print("done.")


if __name__ == "__main__":
    sys.exit(main())
