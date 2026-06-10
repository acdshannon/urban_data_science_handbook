# Data snapshots

Pinned copies of every dataset the book analyzes, so that each chapter runs
top-to-bottom on a laptop, offline, years from now — regardless of what the
live portals do in the meantime. Chapter code prefers the snapshot and tells
you how to refresh it from the source.

Each subdirectory carries a `MANIFEST.md` recording: source URL, retrieval
date, query used, row count, license, and any filtering applied. Snapshots are
small by design (aggregates and samples, not raw dumps); anything bulky stays
out of git and is re-derived by the chapter's fetch code.

| Snapshot | Chapter | Source | License |
|---|---|---|---|
| `nyc_311/` | 2 | NYC Open Data (Socrata) | NYC Open Data Terms |
| `melbourne_pedestrians/` | 4 | City of Melbourne (Opendatasoft) | CC BY 4.0 |
