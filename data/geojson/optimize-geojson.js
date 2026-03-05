#!/usr/bin/env node

/*
  Optimizes GeoJSON files by:
  - Keeping only AC_NO, AC_NAME, DIST_NAME properties
  - Normalizing DIST_NAME (remove trailing *)
  - Rounding coordinates to 5 decimals
  - Writing <name>_optimized.geojson
*/

const fs = require("fs");
const path = require("path");

const targetDir = process.argv[2] ? path.resolve(process.argv[2]) : process.cwd();
const KEEP_PROPERTIES = ["AC_NO", "AC_NAME", "DIST_NAME"];

function round5(n) {
  return Math.round(n * 1e5) / 1e5;
}

function roundCoords(coords) {
  if (!Array.isArray(coords)) return coords;
  if (coords.length && typeof coords[0] === "number") {
    return coords.map((v) => (typeof v === "number" ? round5(v) : v));
  }
  return coords.map((c) => (Array.isArray(c) ? roundCoords(c) : c));
}

function processGeometry(geom) {
  if (!geom) return;
  if (geom.type === "GeometryCollection" && Array.isArray(geom.geometries)) {
    geom.geometries.forEach((g) => processGeometry(g));
    return;
  }
  if (Array.isArray(geom.coordinates)) {
    geom.coordinates = roundCoords(geom.coordinates);
  }
}

function bytesToMB(bytes) {
  return (bytes / 1024 / 1024).toFixed(2);
}

function optimizeFile(filePath) {
  const input = fs.readFileSync(filePath, "utf8").replace(/^\uFEFF/, "");
  const originalSize = Buffer.byteLength(input, "utf8");
  const geo = JSON.parse(input);

  if (!geo.features || !Array.isArray(geo.features)) {
    throw new Error(`Invalid GeoJSON (no features array): ${filePath}`);
  }

  for (const f of geo.features) {
    const oldProps = f.properties || {};
    const clean = {};
    for (const key of KEEP_PROPERTIES) {
      if (Object.prototype.hasOwnProperty.call(oldProps, key)) clean[key] = oldProps[key];
    }
    if (typeof clean.DIST_NAME === "string") {
      clean.DIST_NAME = clean.DIST_NAME.replace(/\s*\*$/, "").trim();
    }
    f.properties = clean;
    processGeometry(f.geometry);
  }

  const outputName = path.basename(filePath).replace(/\.geojson$/i, "_optimized.geojson");
  const outputPath = path.join(path.dirname(filePath), outputName);
  const output = JSON.stringify(geo);
  fs.writeFileSync(outputPath, output, "utf8");
  const optimizedSize = Buffer.byteLength(output, "utf8");

  return {
    file: path.basename(filePath),
    output: outputName,
    originalSize,
    optimizedSize,
    saved: originalSize - optimizedSize,
  };
}

function main() {
  if (!fs.existsSync(targetDir) || !fs.statSync(targetDir).isDirectory()) {
    throw new Error(`Directory not found: ${targetDir}`);
  }

  const files = fs
    .readdirSync(targetDir)
    .filter(
      (f) =>
        f.toLowerCase().endsWith(".geojson") &&
        !f.toLowerCase().endsWith("_optimized.geojson")
    )
    .map((f) => path.join(targetDir, f));

  if (!files.length) {
    console.log(`No source .geojson files found in ${targetDir}`);
    return;
  }

  const results = files.map(optimizeFile);
  let totalIn = 0;
  let totalOut = 0;

  for (const r of results) {
    totalIn += r.originalSize;
    totalOut += r.optimizedSize;
    const pct = ((r.saved / r.originalSize) * 100).toFixed(2);
    console.log(
      `${r.file} -> ${r.output} | ${bytesToMB(r.originalSize)} MB -> ${bytesToMB(
        r.optimizedSize
      )} MB | saved ${bytesToMB(r.saved)} MB (${pct}%)`
    );
  }

  const totalSaved = totalIn - totalOut;
  const totalPct = ((totalSaved / totalIn) * 100).toFixed(2);
  console.log(
    `TOTAL | ${bytesToMB(totalIn)} MB -> ${bytesToMB(totalOut)} MB | saved ${bytesToMB(
      totalSaved
    )} MB (${totalPct}%)`
  );
}

main();
