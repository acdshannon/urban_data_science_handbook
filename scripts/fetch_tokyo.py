"""Build the Chapter 6 snapshots: Tokyo's rail network + street morphology.

Run from the repository root:  python scripts/fetch_tokyo.py

Rail comes from MLIT's National Land Numerical Information railway file
(N02, 2025 edition): every line and station in Japan as GeoJSON, keyless,
under the government's CC BY 4.0-compatible open license. The script trims
to Greater Tokyo (45 km around Tokyo Station), drops the Shinkansen (a
deliberate modeling choice the chapter defends), and constructs the station
graph: platforms clustered into named stations, consecutive stops linked
along each line's merged geometry, fragments bridged, and walk transfers
added between stations within 300 m.

Street morphology comes from two places. The thirty-city gallery is sliced
from Boeing's "Global Urban Street Networks Indicators" (Harvard Dataverse,
doi:10.7910/DVN/ZTFPTB, CC0) — the canonical measurements, not a re-scrape.
Tokyo's own orientation histogram is computed fresh from the Geofabrik
Kanto extract, cropped with osmium; that path needs ~500 MB of download
and the osmium-tool binary, so it only runs if its output is missing.

  data/snapshots/tokyo_rail/
    nodes.csv            station nodes: id, name, romaji, lon, lat, x, y (UTM 54N)
    edges.csv            u, v, line, operator, kind (rail|transfer), km
    street_gallery.csv   30 cities from Boeing's indicators (entropy, grid stats)
    tokyo_bearings.csv   length-weighted street bearings, 36 x 5° bins (0-180°)
    MANIFEST.md

Skips any output that already exists; delete a file to refetch it.
"""

import io
import subprocess
import sys
import zipfile
from datetime import date
from pathlib import Path

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
import requests
from scipy.spatial import cKDTree
from shapely.geometry import Point
from shapely.ops import linemerge

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "snapshots" / "tokyo_rail"
RAW = ROOT / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)

N02_URL = "https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-25/N02-25_GML.zip"
BOEING_URL = "https://dataverse.harvard.edu/api/access/datafile/11058506?format=original"
KANTO_URL = "https://download.geofabrik.de/asia/japan/kanto-latest.osm.pbf"

RADIUS_M = 45_000          # of Tokyo Station
CLUSTER_M = 600            # same-name platforms within this distance = one station
MATCH_M = 300              # station-to-track snap distance
TRANSFER_M = 300           # walk-transfer edges between distinct stations
BRIDGE_M = 3_000           # max gap when stitching a line's broken geometry

GALLERY = [
    "tokyo", "osaka", "new_york_city", "chicago", "detroit", "houston",
    "washington", "philadelphia", "mexico_city", "buenos_aires", "sao_paulo",
    "brasilia", "london", "paris", "amsterdam", "barcelona", "berlin", "rome",
    "moscow", "istanbul", "cairo", "nairobi", "cape_town", "mumbai", "beijing",
    "seoul", "singapore", "jakarta", "melbourne", "north_canberra_canberra",
]

# Hepburn romanization for every station the chapter might name. Anything
# not listed keeps its Japanese name — which is also a fine outcome.
ROMAJI = {
    "東京": "Tokyo", "新宿": "Shinjuku", "渋谷": "Shibuya", "池袋": "Ikebukuro",
    "上野": "Ueno", "品川": "Shinagawa", "横浜": "Yokohama", "大宮": "Omiya",
    "千葉": "Chiba", "西船橋": "Nishi-Funabashi", "武蔵小杉": "Musashi-Kosugi",
    "有楽町": "Yurakucho", "新橋": "Shimbashi", "浅草橋": "Asakusabashi",
    "大手町": "Otemachi", "秋葉原": "Akihabara", "神田": "Kanda",
    "御茶ノ水": "Ochanomizu", "代々木": "Yoyogi", "北千住": "Kita-Senju",
    "西国分寺": "Nishi-Kokubunji", "国分寺": "Kokubunji", "元住吉": "Motosumiyoshi",
    "日吉": "Hiyoshi", "南流山": "Minami-Nagareyama", "武蔵浦和": "Musashi-Urawa",
    "多摩川": "Tamagawa", "北朝霞": "Kita-Asaka", "朝霞台": "Asakadai",
    "新秋津": "Shin-Akitsu", "秋津": "Akitsu", "田園調布": "Den-en-chofu",
    "天王洲アイル": "Tennozu Isle", "大崎": "Osaki", "田端": "Tabata",
    "日暮里": "Nippori", "西日暮里": "Nishi-Nippori", "押上": "Oshiage",
    "中目黒": "Naka-Meguro", "中野": "Nakano", "高田馬場": "Takadanobaba",
    "小竹向原": "Kotake-Mukaihara", "赤羽": "Akabane", "拝島": "Haijima",
    "分倍河原": "Bubaigawara", "府中本町": "Fuchu-Hommachi",
    "新松戸": "Shin-Matsudo", "錦糸町": "Kinshicho", "戸塚": "Totsuka",
    "長津田": "Nagatsuta", "登戸": "Noborito", "武蔵境": "Musashi-Sakai",
    "東神奈川": "Higashi-Kanagawa", "菊名": "Kikuna", "大口": "Oguchi",
    "新横浜": "Shin-Yokohama", "蒲田": "Kamata", "京急蒲田": "Keikyu Kamata",
    "四ツ谷": "Yotsuya", "市ケ谷": "Ichigaya", "飯田橋": "Iidabashi",
    "九段下": "Kudanshita", "永田町": "Nagatacho", "赤坂見附": "Akasaka-Mitsuke",
    "明治神宮前": "Meiji-Jingumae", "原宿": "Harajuku", "目黒": "Meguro",
    "五反田": "Gotanda", "恵比寿": "Ebisu", "大門": "Daimon",
    "浜松町": "Hamamatsucho", "津田沼": "Tsudanuma", "船橋": "Funabashi",
    "立川": "Tachikawa", "八王子": "Hachioji", "町田": "Machida",
    "吉祥寺": "Kichijoji", "三鷹": "Mitaka", "川崎": "Kawasaki",
    "浦和": "Urawa", "松戸": "Matsudo", "柏": "Kashiwa",
}


def get(url, **kw):
    r = requests.get(url, timeout=600, **kw)
    r.raise_for_status()
    return r


def fresh(name: str) -> bool:
    if (OUT / name).exists():
        print(f"{name} exists; skipping (delete it to refetch)")
        return False
    print(f"{name}…")
    return True


def build_rail_graph() -> nx.Graph:
    zpath = RAW / "N02-25_GML.zip"
    if not zpath.exists():
        zpath.write_bytes(get(N02_URL).content)
    with zipfile.ZipFile(zpath) as z:
        st = gpd.read_file(io.BytesIO(z.read("N02-25_GML/UTF-8/N02-25_Station.geojson")))
        rs = gpd.read_file(io.BytesIO(z.read("N02-25_GML/UTF-8/N02-25_RailroadSection.geojson")))
    st, rs = st.to_crs("EPSG:32654"), rs.to_crs("EPSG:32654")

    # The Shinkansen is excluded: intercity shortcuts swamp every shortest
    # path and answer a question about Japan, not about Tokyo.
    st = st[~st.N02_003.str.contains("新幹線", na=False)]
    rs = rs[~rs.N02_003.str.contains("新幹線", na=False)]

    tokyo_st = Point(
        gpd.points_from_xy([139.767], [35.681], crs="EPSG:4326").to_crs("EPSG:32654")[0].coords[0]
    )
    st["pt"] = st.geometry.interpolate(0.5, normalized=True)
    st = st.set_geometry("pt")
    st = st[st.distance(tokyo_st) <= RADIUS_M].copy()

    # Platforms with the same name within CLUSTER_M form one station node.
    st["node"] = None
    for name, g in st.groupby("N02_005"):
        ids = list(g.index)
        parent = {i: i for i in ids}

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        for i in ids:
            for j in ids:
                if i < j and g.pt[i].distance(g.pt[j]) < CLUSTER_M:
                    parent[find(i)] = find(j)
        labels = {r: k for k, r in enumerate(sorted({find(i) for i in ids}))}
        for i in ids:
            st.loc[i, "node"] = f"{name}_{labels[find(i)]}"

    G = nx.Graph()
    pos = st.dissolve(by="node", aggfunc={"N02_005": "first"})
    pos["xy"] = pos.geometry.centroid
    for n, row in pos.iterrows():
        G.add_node(n, name=row["N02_005"], x=row["xy"].x, y=row["xy"].y)

    # Consecutive stations along each line's merged geometry become edges;
    # a line whose geometry merges into fragments is stitched at the nearest
    # endpoints, and ring lines (the Yamanote) are closed explicitly.
    for (op, line), g in st.groupby(["N02_004", "N02_003"]):
        secs = rs[(rs.N02_004 == op) & (rs.N02_003 == line)]
        if len(g) < 2 or secs.empty:
            continue
        merged = linemerge(secs.geometry.union_all())
        geoms = list(merged.geoms) if merged.geom_type == "MultiLineString" else [merged]
        frags = []
        for geom in geoms:
            on = g[g.pt.distance(geom) < MATCH_M].copy()
            if on.empty:
                continue
            on["s"] = on.pt.map(geom.project)
            on = on.sort_values("s")
            seq = [(n, s) for i, (n, s) in enumerate(zip(on.node, on.s))
                   if i == 0 or n != on.node.iloc[i - 1]]
            for (a, sa), (b, sb) in zip(seq, seq[1:]):
                G.add_edge(a, b, line=line, operator=op, kind="rail", km=abs(sb - sa) / 1000)
            if geom.is_ring and len(seq) > 2:
                G.add_edge(seq[-1][0], seq[0][0], line=line, operator=op, kind="rail",
                           km=(geom.length - seq[-1][1] + seq[0][1]) / 1000)
            if seq:
                frags.append([n for n, _ in seq])
        while len(frags) > 1:
            best = None
            for i in range(len(frags)):
                for j in range(i + 1, len(frags)):
                    for a in (frags[i][0], frags[i][-1]):
                        for b in (frags[j][0], frags[j][-1]):
                            d = Point(G.nodes[a]["x"], G.nodes[a]["y"]).distance(
                                Point(G.nodes[b]["x"], G.nodes[b]["y"]))
                            if best is None or d < best[0]:
                                best = (d, i, j, a, b)
            d, i, j, a, b = best
            if d > BRIDGE_M:
                break
            G.add_edge(a, b, line=line, operator=op, kind="rail", km=d / 1000)
            frags[i] += frags.pop(j)

    G.remove_nodes_from(list(nx.isolates(G)))
    ns = list(G.nodes)
    xy = np.array([[G.nodes[n]["x"], G.nodes[n]["y"]] for n in ns])
    for i, j in cKDTree(xy).query_pairs(TRANSFER_M):
        if not G.has_edge(ns[i], ns[j]):
            d = float(np.hypot(*(xy[i] - xy[j])))
            G.add_edge(ns[i], ns[j], kind="transfer", line="(walk)", operator="(walk)",
                       km=max(d, 50) / 1000)

    gcc = max(nx.connected_components(G), key=len)
    dropped = G.number_of_nodes() - len(gcc)
    print(f"  giant component keeps {len(gcc)} stations; {dropped} rim stubs dropped")
    return G.subgraph(gcc).copy()


def main():
    if fresh("nodes.csv") or fresh("edges.csv"):
        G = build_rail_graph()
        lonlat = gpd.GeoSeries(
            [Point(G.nodes[n]["x"], G.nodes[n]["y"]) for n in G.nodes], crs="EPSG:32654"
        ).to_crs("EPSG:4326")
        nodes = pd.DataFrame({
            "id": list(G.nodes),
            "name": [G.nodes[n]["name"] for n in G.nodes],
            "romaji": [ROMAJI.get(G.nodes[n]["name"], G.nodes[n]["name"]) for n in G.nodes],
            "x": [G.nodes[n]["x"] for n in G.nodes],
            "y": [G.nodes[n]["y"] for n in G.nodes],
            "lon": lonlat.x, "lat": lonlat.y,
        })
        edges = pd.DataFrame([
            {"u": u, "v": v, "line": d["line"], "operator": d["operator"],
             "kind": d["kind"], "km": round(d["km"], 3)}
            for u, v, d in G.edges(data=True)
        ])
        nodes.to_csv(OUT / "nodes.csv", index=False)
        edges.to_csv(OUT / "edges.csv", index=False)
        print(f"  {len(nodes)} nodes, {len(edges)} edges "
              f"({(edges.kind == 'transfer').sum()} walk transfers)")

    if fresh("street_gallery.csv"):
        b = pd.read_csv(io.BytesIO(get(BOEING_URL).content))
        cols = ["core_city", "country", "orientation_entropy", "prop_4way",
                "prop_deadend", "straightness", "k_avg", "node_count"]
        sel = (b[b.core_city.isin(GALLERY)]
               .sort_values("node_count", ascending=False)
               .drop_duplicates("core_city")[cols]
               .sort_values("orientation_entropy"))
        sel.to_csv(OUT / "street_gallery.csv", index=False)
        print(f"  {len(sel)} of {len(GALLERY)} gallery cities matched")

    if fresh("tokyo_bearings.csv"):
        # Heavy, optional path: ~500 MB download + osmium-tool. The committed
        # snapshot spares readers this; delete the CSV to rebuild it.
        kanto = RAW / "kanto-latest.osm.pbf"
        crop = RAW / "central_tokyo.osm.pbf"
        if not crop.exists():
            if not kanto.exists():
                print("  downloading Kanto extract (~500 MB)…")
                kanto.write_bytes(get(KANTO_URL).content)
            subprocess.run(["osmium", "extract", "-b", "139.69,35.64,139.83,35.74",
                            "-o", str(crop), "--overwrite", str(kanto)], check=True)
        from pyrosm import OSM
        net = OSM(str(crop)).get_network(network_type="driving")
        lat0, a_all, w_all = 35.69, [], []
        for geom in net.geometry:
            if geom is None:
                continue
            for ls in (geom.geoms if geom.geom_type == "MultiLineString" else [geom]):
                c = np.asarray(ls.coords)
                if len(c) < 2:
                    continue
                d = np.diff(c, axis=0)
                dx, dy = d[:, 0] * np.cos(np.radians(lat0)), d[:, 1]
                a_all.append(np.degrees(np.arctan2(dx, dy)) % 180)
                w_all.append(np.hypot(dx, dy))
        a, w = np.concatenate(a_all), np.concatenate(w_all)
        counts, edges_ = np.histogram(a, bins=36, range=(0, 180), weights=w)
        pd.DataFrame({"bin_deg": edges_[:-1], "length_weight": counts}).to_csv(
            OUT / "tokyo_bearings.csv", index=False)
        print(f"  {len(net):,} ways binned")

    nodes = pd.read_csv(OUT / "nodes.csv")
    edges = pd.read_csv(OUT / "edges.csv")
    gallery = pd.read_csv(OUT / "street_gallery.csv")
    manifest = f"""# Tokyo rail network + street morphology snapshot

Fetched: {date.today().isoformat()}
Rail: MLIT National Land Numerical Information N02 (2025 edition),
keyless GeoJSON, government open license (CC BY 4.0-compatible).
Graph: {len(nodes)} station nodes and {len(edges)} edges within 45 km of
Tokyo Station — platforms clustered by name within {CLUSTER_M} m, stations
linked in sequence along each line's geometry, walk transfers added under
{TRANSFER_M} m, Shinkansen excluded, giant component kept. Construction
choices are modeling decisions; the chapter discusses them.
Streets: gallery of {len(gallery)} world cities from Boeing, "Global Urban
Street Networks Indicators" (Harvard Dataverse, doi:10.7910/DVN/ZTFPTB,
CC0). Tokyo bearing histogram computed from the Geofabrik Kanto extract
(OpenStreetMap, ODbL), cropped to the 13 x 11 km core with osmium.
Rebuild: `python scripts/fetch_tokyo.py` from the repository root.
"""
    (OUT / "MANIFEST.md").write_text(manifest)
    print("done.")


if __name__ == "__main__":
    sys.exit(main())
