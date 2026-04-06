# AGENTS.md

## Local Hosting

Use these steps when you need to host the widgets locally for QA or browser testing.

### What to host

- Serve the repository root so the widgets can load relative assets from `root/`, `hosted-json/`, and `data/`.
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

### Base data directory

- Default JSON base: `./hosted-json`
- Override supported via query param:

```text
?dataBase=/some/other/base/path
```

From that base, `map-widget.html` loads:

- `hosted-json/parties.json`
- `hosted-json/alliances.json`
- `hosted-json/i18n.kn.json`

### Results data

Per-state election results are loaded from:

- `hosted-json/results/TAMIL_NADU_results.json`
- `hosted-json/results/KERALA_results.json`
- `hosted-json/results/WEST_BENGAL_results.json`
- `hosted-json/results/ASSAM_results.json`
- `hosted-json/results/PUDUCHERRY_results.json`

Note:

- `hosted-json/results/ASSAM_2021_legacy_results.json` exists in the repo but is not used by `map-widget.html`.

### Map geometry data

Per-state map shapes are loaded from `root/`:

- `root/TAMIL_NADU_ASSEMBLY_optimized.geojson`
- `root/KERALA_ASSEMBLY_optimized.geojson`
- `root/WEST_BENGAL_ASSEMBLY_optimized.geojson`
- `root/PUDUCHERRY_ASSEMBLY_optimized_compact.geojson`
- `root/ASSAM_2023_keyed.svg`

Fallback candidates also exist in code for non-optimized or alternate relative paths, but the above are the primary local files the page uses from repo root.

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
