# AGENTS.md

## Codex Failure Memory

Use this rule to avoid repeating the same failed approach across future Codex runs, including both codebase-specific mistakes and Codex workflow mistakes.

### When to log

- If a Codex command, patch, workflow, search pattern, file-reading method, replace/edit attempt, tooling choice, or assumption fails and a different approach is later used successfully, record it.
- Log only reusable lessons, not one-off typos or trivial retries.

### Where to log

- Append the note to `.agents/codex-failure-log.md`.

### What to log

Keep each entry short and actionable:

- date
- task context
- command or workflow context
- failed approach
- failure symptom or error
- working approach
- rule to follow next time

Examples of things worth logging:

- a shell command pattern that failed in this environment
- a `rg` or search pattern that was misleading or too broad
- an `apply_patch` approach that was fragile
- a file replacement/edit pattern that caused unnecessary churn
- a browser-testing or local-hosting step that failed
- a Git workflow mistake that should be avoided next time

### Entry format

Use this template:

```md
## YYYY-MM-DD - Short title
- Context: ...
- Command/workflow: ...
- Failed approach: ...
- Symptom: ...
- Working approach: ...
- Next-time rule: ...
```

### Current expectation

- Before finishing a task that required recovering from a failed attempt, update `.agents/codex-failure-log.md`.
- Before retrying a similar workflow, scan `.agents/codex-failure-log.md` for relevant past failures.

## Command Preference

- Run `curl` requests with elevated permissions in this repo by default, because networked `curl` checks may fail or behave inconsistently under the sandbox.

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

## Widget Auto-Update Checks

Use this checklist when verifying auto-refresh behavior for widgets.

### Scope

- `map-widget.html`
- `seat-results-widget.html`
- `key-battles-widget.html`

### Interval parameters

Use one of these query params to define refresh cadence:

- `refreshSeconds=<number>`
- `refreshMs=<number>`

Recommended QA values:

- quick check: `refreshSeconds=10`
- normal check: `refreshSeconds=30`

### Verification steps

1. Open the widget URL with a refresh param.
2. Confirm initial render succeeds.
3. Keep the page open for at least 2 refresh cycles.
4. Verify periodic data requests are made again at the expected interval.
5. Confirm UI updates without full page reload and without losing active UI state (selected state/tab/year where applicable).

### Example URLs

```text
http://127.0.0.1:8000/map-widget.html?state=KERALA&refreshSeconds=30
http://127.0.0.1:8000/seat-results-widget.html?refreshSeconds=30
http://127.0.0.1:8000/key-battles-widget.html?refreshSeconds=30
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

- per-tab sheet data from your backend `values` endpoint

Required query params for the new backend path:

- `apiUrl=<apps-script-or-api-endpoint>`
- `sheetId=<google-sheet-id>` (or `sheetUrl=<full-google-sheet-url>`)

Optional tab params:

- `partyYearTab=<tab-name>` (default: `Partywise_Static`)
- `partyYearLiveTab=<tab-name>` (default: `Live_Partywise_2026`)
- `mappingTab=<tab-name>` (default: `Party_Alliance_Map`)
- `mappingLiveTab=<tab-name>` (default: `Live_Alliance_2026`)
- `partiesTab=<tab-name>` (default: `Party_Color`)
- `alliancesTab=<tab-name>` (default: `Alliance_Color`)

Expected backend request shape:

```text
<apiUrl>?action=values&sheetId=<sheet-id>&tab=<tab-name>
```

Expected backend response shape:

```json
{
  "range": "Partywise_Static!A1:G100",
  "majorDimension": "ROWS",
  "values": [
    ["state_key", "year", "party_code", "wins", "leads"],
    ["ASSAM", "2021", "BJP", "60", "0"]
  ]
}
```

Legacy published-sheet/CSV loading still exists only as an explicit fallback if `apiUrl` is not supplied.

It also depends on:

- D3: `https://d3js.org/d3.v7.min.js`
- Prajavani headline font: `https://fea.assettype.com/tpml/assets/PvHeadlineSemibold3.woff2`
- Prajavani text semibold font: `https://fea.assettype.com/tpml/assets/PrajavaniTextSemibold.woff2`
- Prajavani text regular font: `https://fea.assettype.com/tpml/assets/PrajavaniTextRegular.woff2`

## Seat Results API Plan

This is the migration plan for moving `seat-results-widget.html` away from published-sheet/CSV loading and toward a private-sheet backend that can scale.

### Target architecture

The long-term production path should be:

```text
Widget -> CloudFront -> Lambda/API -> Google Sheets API (service account) -> Private Sheet
```

The short-term development path should use the same widget contract, but swap the backend for Apps Script:

```text
Widget -> Apps Script Web App -> Private Sheet
```

### Important design rule

- The widget must depend on **our API contract**, not on Apps Script specifics.
- Apps Script is the first backend implementation.
- CloudFront + Lambda is the scale-focused backend replacement.
- The widget request/response contract should remain the same across both.

### Why this matches the older Bihar pattern

The older Bihar implementation used a CloudFront-backed endpoint that behaved like Google Sheets API `values` reads and left most parsing/merging in the browser.

The new system should follow that same broad pattern:

- fetch tab-level data from a backend endpoint
- keep the sheet private
- keep credentials off the browser
- allow the backend implementation to change later without changing widget embeds

### Apps Script phase

Apps Script should act as a secure transport layer for development and early rollout.

Recommended request shape:

```text
<apps-script-url>?action=values&sheetId=<sheet-id>&tab=<tab-name>
```

Recommended response shape should mimic Google Sheets API `spreadsheets.values.get`:

```json
{
  "range": "Partywise_Static!A:Z",
  "majorDimension": "ROWS",
  "values": [
    ["state_key", "state", "year", "party_code", "party", "wins", "leads"],
    ["ASSAM", "Assam", "2021", "BJP", "BJP", "60", "0"]
  ]
}
```

Apps Script deployment assumptions:

- deploy as Web App
- `Execute as: Me`
- the script owner has access to the private spreadsheet
- the widget only calls the Apps Script URL

### CloudFront/Lambda phase

When traffic grows, replace the Apps Script backend with a CloudFront-fronted Lambda or similar API service.

The CloudFront/Lambda endpoint should keep the same logical contract:

```text
<api-url>?action=values&sheetId=<sheet-id>&tab=<tab-name>
```

Lambda/API responsibilities:

- authenticate to Google Sheets API using a service account
- read the requested tab from the private spreadsheet
- return the same `values`-style JSON shape
- cache static tabs longer and live tabs briefly

### Seat-results tabs to support

The backend must support these tabs for `seat-results-widget.html`:

- `Partywise_Static` or configured `partyYearTab`
- `Live_Partywise_2026` or configured `partyYearLiveTab`
- `Party_Alliance_Map` or configured `mappingTab`
- `Live_Alliance_2026` or configured `mappingLiveTab`
- `Party_Color` or configured `partiesTab`
- `Alliance_Color` or configured `alliancesTab`

Required base tabs:

- `partyYearTab`
- `mappingTab`
- `partiesTab`
- `alliancesTab`

Optional live tabs:

- `partyYearLiveTab`
- `mappingLiveTab`

### Widget behavior

`seat-results-widget.html` should:

- stop depending on:
  - published sheet HTML lookup
  - gid discovery
  - direct gviz/published CSV loading
- start depending on:
  - one backend base URL such as `apiUrl=<backend-url>`
  - one request per tab using the same tab params it already exposes

The widget should continue to do these things client-side:

- normalize headers
- parse rows
- merge static + live partywise rows
- merge static + live alliance mapping rows
- apply party/alliance colors
- build the `DATA` structure
- render state tabs, year tabs, chart, legend, and table

### Caching

Use both backend and browser caching.

Backend:

- static tabs: cache for about 300 seconds
- live tabs: cache for about 15 to 30 seconds

Widget:

- keep lightweight request caching to avoid duplicate same-session fetches
- refresh logic should re-fetch live-sensitive data without full page reload

### Credentials and privacy

- The sheet should remain private.
- The browser must never receive service account credentials.
- Apps Script uses the script owner’s Google access.
- Lambda/API uses service account credentials stored only as backend secrets.
- The service account should be shared to the sheet as `Viewer` only.

### Testing checklist

- private sheet loads through Apps Script without exposing credentials
- the same widget params work when switching backend URL
- static + live partywise merge behaves correctly
- static + live alliance mapping override behaves correctly
- colors still come from `Party_Color` and `Alliance_Color`
- the backend can later be swapped from Apps Script to CloudFront/Lambda without changing the widget request contract

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
