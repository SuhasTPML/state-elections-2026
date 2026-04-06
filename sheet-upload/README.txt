Google Sheets upload package

Layman-friendly package:
- see `sheet-upload/layman-friendly/README.txt`
- includes simple tab names + one XLSX: `election-upload-layman-friendly.xlsx`

Option A (recommended): single combined results tab
1) statewise_combined_results (constituency + winner party/alliance fields)
2) statewise_party_alliance_mapping
3) party_master
4) alliance_master
5) i18n_kn

Widget URL example (combined tab, no separate partyWiseTab needed)
http://127.0.0.1:8000/map-widget.html?state=KERALA&sheetId=YOUR_SHEET_ID&resultsTab=statewise_combined_results&mappingTab=statewise_party_alliance_mapping&partiesTab=party_master&alliancesTab=alliance_master&i18nTab=i18n_kn

Option A2 (recommended for caching): static + live split
1) statewise_combined_results_static (map static constituency data)
2) statewise_party_yearwise (seat static party-wise historical data)
3) statewise_live_2026 (map live 2026 constituency data)
4) statewise_partywise_live_2026 (seat widget 2026 live wins/leads source)
5) statewise_party_alliance_mapping
6) party_master
7) i18n_kn

Widget URL example (split live tabs)
http://127.0.0.1:8000/map-widget.html?state=KERALA&sheetId=YOUR_SHEET_ID&resultsTab=statewise_combined_results_static&resultsLiveTab=statewise_live_2026&mappingTab=statewise_party_alliance_mapping&partiesTab=party_master&i18nTab=i18n_kn

Seat widget URL example (split static/live party-wise)
http://127.0.0.1:8000/seat-results-widget.html?sheetId=YOUR_SHEET_ID&partyYearTab=statewise_party_yearwise&partyYearLiveTab=statewise_partywise_live_2026&mappingTab=statewise_party_alliance_mapping&partiesTab=party_master&alliancesTab=alliance_master

Optional live alliance mapping override (2026):
- add `mappingLiveTab=<tab-name>` (or `mappingLiveCsvUrl=...`) with party+year+alliance rows for live updates.
- use `statewise_live_alliance_2026.csv` if live sheet does not include any alliance columns.

CSV files in this folder for split mode:
- statewise_combined_results_static.csv
- statewise_party_yearwise.csv
- statewise_live_2026.csv
- statewise_partywise_live_2026.csv
- statewise_live_alliance_2026.csv (optional, recommended when alliance is removed from live results)

Option B: separate tabs (legacy)
1) statewise_party_results
2) statewise_party_wise
3) statewise_party_alliance_mapping
4) party_master
5) alliance_master
6) i18n_kn

Legacy URL example
http://127.0.0.1:8000/map-widget.html?state=KERALA&sheetId=YOUR_SHEET_ID&resultsTab=statewise_party_results&partyWiseTab=statewise_party_wise&mappingTab=statewise_party_alliance_mapping&partiesTab=party_master&alliancesTab=alliance_master&i18nTab=i18n_kn

Alliance columns in results can be omitted if mapping tab is complete for all state+party+year combinations.
Alliance columns in results are intentionally removed from the split files in this package.

If uploading the XLSX as-is, use mappingTab=statewise_party_alliance_map

Widget dependency map

Map widget (map-widget.html)
- Required static tabs:
  - statewise_combined_results_static
  - statewise_party_alliance_mapping
  - party_master
- Required live tabs:
  - statewise_live_2026
- Optional live/visual tabs:
  - statewise_live_alliance_2026
  - alliance_master
  - i18n_kn

Seats widget (seat-results-widget.html)
- Required static tabs:
  - statewise_party_yearwise
  - statewise_party_alliance_mapping
  - party_master
- Required live tabs:
  - statewise_partywise_live_2026
- Optional visual tab:
  - alliance_master

Notes
- Seats widget does not use constituency rows.
- statewise_live_alliance_2026 can be shared by both widgets.
