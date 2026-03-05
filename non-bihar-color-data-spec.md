# Non-Bihar Map: Color/Data Behavior Spec

This document captures the color and data behavior in:

- `Bihar elections/widget-embeds-json hosted/map.html`

and defines what should be wired into:

- `map-non-bihar.html`

using hosted JSON only (no CloudFront/CDN-specific logic).

## 1) Bihar Map Behavior (Reference)

### 1.1 Color modes in reference map

Reference logic supports these modes in `getColorForMode()`:

- `alliance-2025`
- `party-2025`
- `alliance-2020`
- `party-2020`
- `alliance-2015`
- `party-2015`
- `alliance-2010`
- `party-2010`
- `reserved` (implemented in color function, not shown in current dropdown options)

Dropdown options are built in `createMapControls()` from:

- 2025 modes only if `ENABLE_2025_MODES` is true.
- Always includes 2020/2015/2010 alliance+party modes when election data exists.

### 1.2 Color sources

- Party colors:
  - from `parties.json` field `party.color`, then pastelized for fills.
- Alliance colors:
  - resolved from `alliances.json` override first, then derived from parties data.
  - stored as original + pastelized variants.
- Reserved mode:
  - `GEN`, `SC`, `ST`, `NA` mapped to fixed colors.

### 1.3 Legend behavior

- For alliance modes:
  - counts seats by alliance for selected year and shows all alliances with `(count)`.
- For party modes:
  - counts seats by party for selected year and shows top 6 by count.
- Hidden when no election data.

### 1.4 Data shown in bottom sheet

Always from map feature:

- Constituency name
- District

When election row exists:

- Label:
  - `Winner` in 2025 mode path
  - `Current MLA` otherwise
- Person name:
  - `y2025_winner_name` (if 2025 mode enabled)
  - otherwise `current_mla_name`
- Party:
  - `y2025_winner_party` or `current_mla_party`
- Alliance:
  - resolved from party-year mapping (or `current_mla_alliance`)
- Color swatches for party and alliance.

When election row missing:

- `"No election data available for this constituency."`

## 2) State Change Behavior (Reference)

On state change:

- clears selection/search/bottom sheet
- clears URL params `ac` and `name`
- loads new GeoJSON
- loads election data only if `hasElectionData`
- rebuilds controls and legend
- applies fills for active color mode
- updates URL param `state`

## 3) Hosted JSON Strategy For Non-Bihar

Use one hosted JSON base URL only.

- No CloudFront-specific handling.
- No multi-CDN fallback logic.

Suggested base:

- query param override: `?dataBase=https://...`
- fallback default: `./hosted-json`

## 4) Hosted JSON Files (Proposed)

Under `${DATA_BASE}`:

- `states-manifest.json`
- `parties.json`
- optional `alliances.json`
- one results file per state (path declared in manifest)
- GeoJSON can be loaded via URLs declared in manifest per state.

### 4.1 `states-manifest.json` (proposed shape)

```json
{
  "default_state": "ASSAM",
  "states": [
    {
      "key": "ASSAM",
      "label": "Assam",
      "title": "Assam Assembly Constituency Map",
      "description": "Tap on a constituency to view details, or search by number/name/district.",
      "geojson_url": "./data/geojson/ASSAM_ASSEMBLY_optimized.geojson",
      "results_url": "./hosted-json/results/ASSAM_results.json",
      "supported_modes": ["alliance-2025","party-2025","alliance-2020","party-2020","alliance-2015","party-2015","alliance-2010","party-2010","reserved"]
    }
  ]
}
```

### 4.2 `parties.json` (same intent as Bihar)

Required fields:

- `code` (party code)
- `color` (hex)
- `alliances` (optional year map)
- `alliance_2020` / `alliance` fallback fields
- optional alliance color hints

### 4.3 `alliances.json` (optional override)

Map of alliance name -> hex color:

```json
{
  "NDA": "#f0a500",
  "INDIA": "#0099cc",
  "OTHERS": "#888888"
}
```

### 4.4 per-state results JSON

One row per constituency with AC number key compatibility.

Expected fields (Bihar-compatible):

- `no`
- `constituency_name`
- `current_mla_name`
- `current_mla_party`
- `current_mla_alliance`
- `reserved`
- `y2025_winner_name`, `y2025_winner_party`
- `y2020_winner_name`, `y2020_winner_party`
- `y2015_winner_name`, `y2015_winner_party`
- `y2010_winner_name`, `y2010_winner_party`

## 5) Wiring Goal For `map-non-bihar.html`

1. Keep current non-Bihar map interactions (search, hover tooltip, select, zoom, reset).
2. Add Bihar-like color mode dropdown + legend.
3. Load all color/data inputs from hosted JSON base.
4. Apply party/alliance/reserved fills by selected mode.
5. Show winner/current MLA cards with swatches in bottom sheet.
6. Support missing data gracefully (neutral fill + no-data text).
