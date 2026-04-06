# AGENTS.md

## Local Hosting

Use these steps when you need to host the widgets locally for QA or browser testing.

### What to host

- Serve the repository root so the widgets can load relative assets from `root/`.
- Map widget entry point: `map-widget.html`
- Seat results widget entry point: `seat-results-widget.html`

### Start a local server

From the repo root, run:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:8000/map-widget.html
```

### Persistent local server

If you need the server to keep running independently of the current terminal session, start it as a detached process:

```powershell
Start-Process python -WorkingDirectory "C:\Users\suhas.bhandari\Downloads\Claude\Experiments\Elections" -ArgumentList '-m','http.server','8000','--bind','127.0.0.1'
```

### Stop the server

If you started it in the current terminal, use `Ctrl+C`.

If you started it as a detached process, stop it by PID:

```powershell
Stop-Process -Id <PID>
```

### Notes

- Use HTTP, not `file://`, so the page can fetch JSON and map assets correctly.
- Serve from the repo root, not from a subfolder.
- Default test URL can include query params, for example:

```text
http://127.0.0.1:8000/map-widget.html?state=KERALA
```

## Map Widget Data Sources

`map-widget.html` loads its runtime data from these sources.

### Google Sheet Tabs

`map-widget.html` reads all non-geometry runtime data from a Google Sheet (CSV over gviz).

Required query params:

- `sheetId=<google-sheet-id>` (or `sheetUrl=<full-google-sheet-url>`)
- optional `resultsTab=<tab-name>` (default: `statewise_party_results`)
- optional `partyWiseTab=<tab-name>` (default: `statewise_party_wise`)
- optional `resultsLiveTab=<tab-name>` (default: none)
- optional `partyWiseLiveTab=<tab-name>` (default: mirrors `resultsLiveTab` when provided)
- optional `mappingLiveTab=<tab-name>` (default: none)
- optional `mappingTab=<tab-name>` (default: `statewise_party_alliance_mapping`)
- optional `partiesTab=<tab-name>` (default: `party_master`)
- optional `alliancesTab=<tab-name>` (default: `alliance_master`)
- optional `i18nTab=<tab-name>` (default: `i18n_kn`)

Example:

```text
http://127.0.0.1:8000/map-widget.html?state=KERALA&sheetId=YOUR_SHEET_ID&resultsTab=statewise_party_results&partyWiseTab=statewise_party_wise&mappingTab=statewise_party_alliance_mapping&partiesTab=party_master&alliancesTab=alliance_master&i18nTab=i18n_kn
```

Split static/live example:

```text
http://127.0.0.1:8000/map-widget.html?state=KERALA&sheetId=YOUR_SHEET_ID&resultsTab=statewise_combined_results_static&resultsLiveTab=statewise_live_2026&partyWiseLiveTab=statewise_live_2026&mappingTab=statewise_party_alliance_mapping&partiesTab=party_master&alliancesTab=alliance_master&i18nTab=i18n_kn
```

Expected `resultsTab` columns (minimum):

- `state` or `state_key` (e.g. `KERALA`)
- `no` (constituency number)
- constituency/detail fields, for example:
  - `constituency_name`
  - `reserved`
  - `y2021_winner_name`
  - `y2016_winner_name`
  - `y2026_winner_name`
  - `status`
  - `updated_at`

Expected `partyWiseTab` columns:

- `state` or `state_key`
- `no`
- party/alliance fields used by the widget, such as:
  - `y2021_winner_party`, `y2021_winner_alliance`
  - `y2016_winner_party`, `y2016_winner_alliance`
  - `y2026_winner_party`, `y2026_winner_alliance`

Expected `resultsLiveTab` / `partyWiseLiveTab` columns (for live split mode):

- `state` or `state_key`
- `no`
- mutable 2026 fields only, for example:
  - `y2026_winner_name`
  - `y2026_winner_party`
  - `y2026_winner_alliance`
  - `status`
  - `updated_at`

Expected `mappingTab` columns:

- `state` or `state_key`
- `party` or `party_code`
- either:
  - `year` + `alliance` rows, or
  - per-year columns like `alliance_2016`, `alliance_2021`, `alliance_2026`

Alliance values are auto-resolved from this mapping tab when alliance fields are missing in results rows.

Expected `mappingLiveTab` columns (optional, for live override):

- same shape as `mappingTab`, typically only 2026 rows that should override static mapping.

Expected `partiesTab` columns:

- `party_code` (or `party`)
- `color`
- optional `state` or `state_key`
- optional `alliance`
- optional per-year alliance columns (for example `alliance_2016`, `alliance_2021`, `alliance_2026`)
- optional `alliance_color`

Expected `alliancesTab` columns:

- `alliance`
- `color`

Expected `i18nTab` columns:

- `key`
- `kn`
- optional `type` (`string` or `reserved`)

### Map geometry data

Per-state map shapes are loaded from `root/`:

- `root/TAMIL_NADU_ASSEMBLY_optimized.geojson`
- `root/KERALA_ASSEMBLY_optimized.geojson`
- `root/WEST_BENGAL_ASSEMBLY_optimized.geojson`
- `root/PUDUCHERRY_ASSEMBLY_optimized_compact.geojson`
- `root/ASSAM_2023_keyed.svg`

### External runtime assets

These are not election data, but `map-widget.html` depends on them at runtime:

- D3: `https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js`
- Prajavani headline font: `https://fea.assettype.com/tpml/assets/PvHeadlineSemibold3.woff2`
- Prajavani text semibold font: `https://fea.assettype.com/tpml/assets/PrajavaniTextSemibold.woff2`
- Prajavani text regular font: `https://fea.assettype.com/tpml/assets/PrajavaniTextRegular.woff2`

## Seat Results Widget Data Source

`seat-results-widget.html` loads:

- `hosted-json/parliament-data.json`

It also depends on:

- D3: `https://d3js.org/d3.v7.min.js`
- Prajavani headline font: `https://fea.assettype.com/tpml/assets/PvHeadlineSemibold3.woff2`
- Prajavani text semibold font: `https://fea.assettype.com/tpml/assets/PrajavaniTextSemibold.woff2`
- Prajavani text regular font: `https://fea.assettype.com/tpml/assets/PrajavaniTextRegular.woff2`

## Data Organization Guidance

For this widget, it generally makes sense to keep stable reference data in one place and frequently changing `2026` data in another.

### Recommended split

Keep `static` data for:

- map geometry
- constituency metadata
- district names
- translations
- party metadata
- alliance metadata
- historical locked results

Keep `dynamic` data for:

- `2026` projections
- `2026` live updates
- `2026` winner/status refreshes

### Important rule

- Keep canonical shared metadata in the static layer.
- Keep only mutable `2026` fields in the dynamic layer.
- Join the two using a stable constituency key such as `ac_no`.

### Why this helps

- Static files can be cached aggressively.
- Dynamic `2026` updates can be refreshed without re-downloading all map/reference data.
- Editorial fixes to live data are easier to patch and roll back.
- It reduces unnecessary churn in the base data files.

### Avoid

- Do not duplicate shared fields like constituency name, district name, reserved category, or party display metadata across both layers unless there is a clear reason.
- If duplicated, those values will drift.

### Example shape

- `static/constituencies.json`
- `static/parties.json`
- `static/alliances.json`
- `static/i18n.kn.json`
- `dynamic/results-2026.json`

Example `dynamic/results-2026.json` fields:

- `ac_no`
- `winner_name`
- `winner_party`
- `winner_alliance`
- `status`
- `updated_at`
