# Tokyo rail network + street morphology snapshot

Fetched: 2026-06-11
Rail: MLIT National Land Numerical Information N02 (2025 edition),
keyless GeoJSON, government open license (CC BY 4.0-compatible).
Graph: 1223 station nodes and 1502 edges within 45 km of
Tokyo Station — platforms clustered by name within 600 m, stations
linked in sequence along each line's geometry, walk transfers added under
300 m, Shinkansen excluded, giant component kept. Construction
choices are modeling decisions; the chapter discusses them.
Streets: gallery of 30 world cities from Boeing, "Global Urban
Street Networks Indicators" (Harvard Dataverse, doi:10.7910/DVN/ZTFPTB,
CC0). Tokyo bearing histogram computed from the Geofabrik Kanto extract
(OpenStreetMap, ODbL), cropped to the 13 x 11 km core with osmium.
Rebuild: `python scripts/fetch_tokyo.py` from the repository root.
