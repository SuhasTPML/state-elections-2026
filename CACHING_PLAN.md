# Caching Plan (Static + Live 2026 Split)

Date: 2026-04-06  
Repo: `CMS Widgets/Elections`

## Goal

Improve load time by caching static assets/data, while keeping 2026 live updates fresh.

## Current Status

- Map geometry is now cache-enabled in `map-widget.html` (`fetch(..., { cache: 'force-cache' })`).
- Election CSV fetches are still `no-store` (always fresh).

## Recommended Data Split

Use separate sheet tabs/files for static and live data.

### Static (cacheable)

- Constituency static fields: `state_key`, `no`, `constituency_name`, `reserved`, district/meta.
- Historical winner fields: 2016 and 2021.
- `party_master`
- `alliance_master`
- `statewise_party_alliance_mapping`
- `i18n_kn`

### Live (no-store)

- 2026 mutable fields only:
  - `y2026_winner_name`
  - `y2026_winner_party`
  - `y2026_winner_alliance`
  - `status`
  - `updated_at`

## Why This Split Is Needed

If 2016/2021 and 2026 are in one combined CSV, caching that file will also cache live 2026 values.  
Separating tabs/files is required to safely cache historical/static content.

## Map Widget Plan (`map-widget.html`)

1. Add explicit sources:
   - `resultsStaticTab` (or `resultsStaticCsvUrl`)
   - `resultsLive2026Tab` (or `resultsLive2026CsvUrl`)
2. Fetch policy:
   - static tab/files with `cache: 'force-cache'`
   - live 2026 tab/file with `cache: 'no-store'`
3. Join strategy:
   - merge by `state_key + no`
   - live fields override static where present
4. Keep existing fallback path temporarily for backward compatibility.
5. Add a switch flag to disable legacy combined mode once migration is complete.

## Seat Results Widget Plan (`seat-results-widget.html`)

1. Split party year-wise data into:
   - static year rows (historical)
   - live 2026 rows
2. Cache policy:
   - static: `force-cache`
   - live 2026: `no-store`
3. Merge by `state_key + year + party_code` before rendering.

## Cache Invalidation Strategy

Use one of these (recommended in order):

1. Version query param on static URLs/tabs (`?staticVersion=YYYYMMDD`).
2. New static tab names when schema/data changes.
3. Manual cache-bust param for emergency refresh.

## Rollout Steps

1. Create new static/live tabs in Google Sheet.
2. Backfill static tabs from current combined data.
3. Wire new query params in both widgets.
4. Keep old params supported for one transition window.
5. Validate state-by-state outputs (2016/2021 and 2026).
6. Remove legacy combined path after editorial sign-off.

## Validation Checklist

- Hard refresh and normal reload both render correctly.
- 2026 status/winner edits appear immediately.
- 2016/2021 remain stable and do not refetch on every reload.
- Party/alliance colors and legends match old behavior.
- Bottom sheet and map fill remain consistent for 2026 states.

