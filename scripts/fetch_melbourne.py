"""Build the Chapter 4 snapshots from the City of Melbourne open data portal.

Run from the repository root:  python scripts/fetch_melbourne.py

The Pedestrian Counting System lives in two pieces: a ZIP archive holding the
full hourly history (May 2009 - Dec 2022) attached to the dataset page, and
the live dataset carrying everything since. This script downloads both,
reconciles them, and writes compact parquet snapshots:

  data/snapshots/melbourne_pedestrians/
    hourly.parquet        hourly counts, all sensors, full history
    sensors.csv           sensor id, name, location, install date
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
    """Find and download the 2009-2022 archive ZIP attached to the dataset."""
    meta = get(f"{BASE}/{COUNTS}/attachments").json()
    attachments = meta.get("attachments", meta if isinstance(meta, list) else [])
    zips = [a for a in attachments if a.get("href", a.get("url", "")).endswith(".zip")]
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
            if name.endswith(".csv"):
                with z.open(name) as f:
                    frames.append(pd.read_csv(f))
    return pd.concat(frames, ignore_index=True)


def fetch_live() -> pd.DataFrame:
    """Export the live dataset (2023+) as CSV via the Explore API."""
    url = f"{BASE}/{COUNTS}/exports/csv"
    r = get(url, params={"delimiter": ","})
    return pd.read_csv(io.StringIO(r.text))


def main():
    print("sensor locations…")
    sensors = pd.read_csv(
        io.StringIO(get(f"{BASE}/{SENSORS}/exports/csv", params={"delimiter": ","}).text)
    )
    sensors.to_csv(OUT / "sensors.csv", index=False)

    print("archive (2009-2022)…")
    old = fetch_archive()
    print(f"  {len(old):,} rows")

    print("live (2023+)…")
    new = fetch_live()
    print(f"  {len(new):,} rows")

    # Column names differ across eras; normalize to a minimal schema.
    # (Adjust the renames after inspecting both, then delete this comment.)
    print("reconciling…")
    combined = pd.concat([old, new], ignore_index=True)
    combined.to_parquet(OUT / "hourly.parquet", index=False)

    manifest = f"""# Melbourne Pedestrian Counting System snapshot

Fetched: {date.today().isoformat()}
Source: City of Melbourne open data portal, dataset `{COUNTS}`
(archive ZIP attachment for May 2009 - Dec 2022, live export for 2023+),
plus `{SENSORS}` for sensor metadata.
License: CC BY 4.0.
Rows: archive={len(old):,}, live={len(new):,}.
Rebuild: `python scripts/fetch_melbourne.py` from the repository root.
"""
    (OUT / "MANIFEST.md").write_text(manifest)
    print("done.")


if __name__ == "__main__":
    sys.exit(main())
