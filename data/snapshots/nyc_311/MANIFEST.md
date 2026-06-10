# NYC 311 snapshot

Fetched: 2026-06-10
Source: NYC Open Data, dataset `erm2-nwe9` (311 Service Requests from
2020 to Present), via SoQL aggregation; NTA 2020 boundaries (`9nt8-h7nd`);
census demographics by NTA (`rnsn-acs2` — 2010 vintage, 2000/2010 populations
keyed by 2010 NTA codes; the portal has no 2020-census-by-NTA2020 table).
Window: 2024-01-01 to 2026-01-01 (rat sightings: 2025 only).
License: NYC Open Data Terms of Use (free use, no registration).
Rows: totals=203, daily=8071,
rhythms=672, rats=19846.
Rebuild: `python scripts/fetch_nyc_311.py` from the repository root.
