# Melbourne Pedestrian Counting System snapshot

Fetched: 2026-06-10
Source: City of Melbourne open data portal, dataset `pedestrian-counting-system-monthly-counts-per-hour`
(archive ZIP attachment for May 2009 - 14 Dec 2022; live export, which the
portal serves as a rolling window of roughly the last two years), plus
`pedestrian-counting-system-sensor-locations` for sensor metadata.
Coverage: 2009-05-01 → 2022-10-31 (archive) and
2024-06-11 → 2026-06-10 (live). The ~588-day hole
between the eras is the portal's, not ours: the archive froze (its label
says 14 Dec 2022; its rows stop earlier) and the rolling window has since
moved past it.
Schema: hourly.parquet has one row per (sensor_id, ts): sensor_id joins
sensors.csv `location_id`; count is pedestrians per hour, both directions.
License: CC BY 4.0.
Rows: archive=4,562,230, live=1,601,924, combined=6,152,424.
Rebuild: `python scripts/fetch_melbourne.py` from the repository root.
