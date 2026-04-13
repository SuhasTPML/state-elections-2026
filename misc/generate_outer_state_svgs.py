#!/usr/bin/env python3
"""Generate state outer-boundary SVGs from constituency geometries.

This removes internal constituency lines by:
1) splitting polygons into edges
2) keeping only edges that occur once
3) stitching those edges into boundary loops
"""

from __future__ import annotations

import json
import math
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ROOT_DIR = ROOT / "root"
DEFAULT_FILL = "#9ca3af"
DEFAULT_STROKE = "#1f2937"
DEFAULT_STROKE_WIDTH = 2

STATE_INPUTS = {
    "KERALA": {"type": "geojson", "src": ROOT_DIR / "KERALA_ASSEMBLY_optimized.geojson"},
    "TAMIL_NADU": {"type": "geojson", "src": ROOT_DIR / "TAMIL_NADU_ASSEMBLY_optimized.geojson"},
    "WEST_BENGAL": {"type": "geojson", "src": ROOT_DIR / "WEST_BENGAL_ASSEMBLY_optimized.geojson"},
    "PUDUCHERRY": {"type": "geojson", "src": ROOT_DIR / "PUDUCHERRY_ASSEMBLY_optimized_compact.geojson"},
    "ASSAM": {"type": "svg", "src": ROOT_DIR / "ASSAM_2023_keyed.svg"},
}


Point = Tuple[float, float]
QPoint = Tuple[int, int]


def ensure_closed(ring: Sequence[Point]) -> List[Point]:
    out = list(ring)
    if len(out) < 2:
        return out
    if out[0] != out[-1]:
        out.append(out[0])
    return out


def ring_area(ring: Sequence[Point]) -> float:
    if len(ring) < 3:
        return 0.0
    area = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        area += x1 * y2 - x2 * y1
    return area / 2.0


def load_geojson_rings(path: Path) -> List[List[Point]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    features = data.get("features", [])
    rings: List[List[Point]] = []

    def collect_geom(geom: Dict):
        gtype = (geom or {}).get("type")
        coords = (geom or {}).get("coordinates")
        if not gtype or coords is None:
            return
        if gtype == "Polygon":
            for ring in coords:
                pts = [(float(x), float(y)) for x, y in ring]
                if len(pts) >= 4:
                    rings.append(ensure_closed(pts))
        elif gtype == "MultiPolygon":
            for poly in coords:
                for ring in poly:
                    pts = [(float(x), float(y)) for x, y in ring]
                    if len(pts) >= 4:
                        rings.append(ensure_closed(pts))
        elif gtype == "GeometryCollection":
            for child in geom.get("geometries", []):
                collect_geom(child)

    for f in features:
        collect_geom(f.get("geometry"))
    return rings


def parse_points_attr(points: str) -> List[Point]:
    nums = re.findall(r"-?\d*\.?\d+(?:[eE][+-]?\d+)?", points or "")
    out: List[Point] = []
    for i in range(0, len(nums) - 1, 2):
        out.append((float(nums[i]), float(nums[i + 1])))
    return out


def load_svg_polygon_rings(path: Path) -> List[List[Point]]:
    tree = ET.parse(path)
    root = tree.getroot()
    rings: List[List[Point]] = []
    for el in root.iter():
        if el.tag.lower().endswith("polygon"):
            pts = parse_points_attr(el.attrib.get("points", ""))
            if len(pts) >= 4:
                rings.append(ensure_closed(pts))
    return rings


def extract_outer_from_svg_polygons_raster(
    path: Path, scale: int = 8, padding: int = 12, epsilon_px: float = 1.25
) -> List[List[Point]]:
    """Build a single external boundary by raster-unioning polygon fills."""
    rings = load_svg_polygon_rings(path)
    if not rings:
        return []

    pts = [pt for ring in rings for pt in ring]
    minx = min(x for x, _ in pts)
    maxx = max(x for x, _ in pts)
    miny = min(y for _, y in pts)
    maxy = max(y for _, y in pts)

    width = int(math.ceil((maxx - minx) * scale)) + 2 * padding + 1
    height = int(math.ceil((maxy - miny) * scale)) + 2 * padding + 1
    if width <= 2 or height <= 2:
        return []

    mask = np.zeros((height, width), dtype=np.uint8)

    for ring in rings:
        arr = np.array(
            [
                [
                    int(round((x - minx) * scale + padding)),
                    int(round((y - miny) * scale + padding)),
                ]
                for x, y in ring
            ],
            dtype=np.int32,
        )
        if len(arr) >= 3:
            cv2.fillPoly(mask, [arr], 255)

    # Close small cracks introduced by inconsistent constituency boundaries.
    kernel = np.ones((3, 3), dtype=np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return []

    contour = max(contours, key=cv2.contourArea)
    approx = cv2.approxPolyDP(contour, epsilon=epsilon_px, closed=True)
    seq = approx[:, 0, :] if len(approx.shape) == 3 else approx

    ring: List[Point] = []
    for p in seq:
        px, py = float(p[0]), float(p[1])
        x = (px - padding) / scale + minx
        y = (py - padding) / scale + miny
        ring.append((x, y))

    if ring and ring[0] != ring[-1]:
        ring.append(ring[0])
    return [ring] if len(ring) >= 4 else []


def q_point(pt: Point, scale: float) -> QPoint:
    return (int(round(pt[0] * scale)), int(round(pt[1] * scale)))


def edge_key(a: QPoint, b: QPoint) -> Tuple[QPoint, QPoint]:
    return (a, b) if a <= b else (b, a)


def extract_boundary_loops(rings: Iterable[Sequence[Point]], quant_scale: float) -> List[List[Point]]:
    edge_count: Dict[Tuple[QPoint, QPoint], int] = defaultdict(int)
    neighbors: Dict[QPoint, set[QPoint]] = defaultdict(set)
    q_to_point: Dict[QPoint, Point] = {}

    for ring in rings:
        if len(ring) < 2:
            continue
        qring = [q_point(pt, quant_scale) for pt in ring]
        for i in range(len(qring) - 1):
            a = qring[i]
            b = qring[i + 1]
            if a == b:
                continue
            q_to_point.setdefault(a, ring[i])
            q_to_point.setdefault(b, ring[i + 1])
            key = edge_key(a, b)
            edge_count[key] += 1

    boundary_edges = [e for e, c in edge_count.items() if c == 1]
    for a, b in boundary_edges:
        neighbors[a].add(b)
        neighbors[b].add(a)

    unused = set(boundary_edges)
    loops: List[List[Point]] = []

    def choose_next(prev: QPoint, cur: QPoint, cands: List[QPoint]) -> QPoint:
        if len(cands) == 1:
            return cands[0]
        # Prefer smallest left turn to keep traversal consistent.
        vx = cur[0] - prev[0]
        vy = cur[1] - prev[1]

        def score(n: QPoint) -> float:
            wx = n[0] - cur[0]
            wy = n[1] - cur[1]
            cross = vx * wy - vy * wx
            dot = vx * wx + vy * wy
            ang = math.atan2(cross, dot)
            if ang <= 0:
                ang += 2 * math.pi
            return ang

        return min(cands, key=score)

    while unused:
        start_edge = next(iter(unused))
        start, nxt = start_edge
        chain = [start, nxt]
        unused.remove(start_edge)
        prev, cur = start, nxt

        while True:
            if cur == start:
                break
            cands = [n for n in neighbors[cur] if edge_key(cur, n) in unused]
            if not cands:
                break
            nxt2 = choose_next(prev, cur, cands)
            unused.remove(edge_key(cur, nxt2))
            chain.append(nxt2)
            prev, cur = cur, nxt2

        if len(chain) >= 4 and chain[0] == chain[-1]:
            loop = [q_to_point[q] for q in chain]
            if abs(ring_area(loop)) > 0:
                loops.append(loop)

    return loops


def normalize_loops_for_svg(loops: List[List[Point]], invert_y: bool) -> Tuple[List[List[Point]], float, float]:
    pts = []
    for ring in loops:
        for x, y in ring:
            pts.append((x, -y if invert_y else y))
    if not pts:
        return [], 0.0, 0.0
    minx = min(p[0] for p in pts)
    maxx = max(p[0] for p in pts)
    miny = min(p[1] for p in pts)
    maxy = max(p[1] for p in pts)
    w = maxx - minx
    h = maxy - miny
    if w <= 0 or h <= 0:
        return [], 0.0, 0.0

    target = 1000.0
    scale = target / max(w, h)
    norm_loops: List[List[Point]] = []
    for ring in loops:
        nr: List[Point] = []
        for x, y in ring:
            tx = (x - minx) * scale
            ty = ((-y if invert_y else y) - miny) * scale
            nr.append((tx, ty))
        norm_loops.append(nr)
    return norm_loops, w * scale, h * scale


def loops_to_path_d(loops: List[List[Point]]) -> str:
    parts = []
    for ring in loops:
        if len(ring) < 4:
            continue
        coords = " ".join(f"{x:.3f},{y:.3f}" for x, y in ring[:-1])
        parts.append(f"M {coords} Z")
    return " ".join(parts)


def write_svg(path: Path, loops: List[List[Point]], invert_y: bool):
    norm_loops, width, height = normalize_loops_for_svg(loops, invert_y=invert_y)
    if not norm_loops or width <= 0 or height <= 0:
        raise RuntimeError(f"No loops available for {path.name}")
    d = loops_to_path_d(norm_loops)
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.3f} {height:.3f}">\n'
        f'  <path d="{d}" fill="{DEFAULT_FILL}" stroke="{DEFAULT_STROKE}" stroke-width="{DEFAULT_STROKE_WIDTH}"/>\n'
        '</svg>\n'
    )
    path.write_text(svg, encoding="utf-8")


def main():
    for state, cfg in STATE_INPUTS.items():
        src: Path = cfg["src"]
        typ = cfg["type"]
        if typ == "geojson":
            rings = load_geojson_rings(src)
            loops = extract_boundary_loops(rings, quant_scale=1_000_000.0)
            out = ROOT_DIR / f"{state}_outer.svg"
            write_svg(out, loops, invert_y=True)
        elif typ == "svg":
            # Assam source polygons have slight shared-edge mismatch; raster union
            # yields a clean single exterior boundary without inner constituency lines.
            loops = extract_outer_from_svg_polygons_raster(src)
            out = ROOT_DIR / f"{state}_outer.svg"
            write_svg(out, loops, invert_y=False)
        else:
            raise RuntimeError(f"Unsupported type: {typ}")
        print(f"Generated {out}")


if __name__ == "__main__":
    main()
