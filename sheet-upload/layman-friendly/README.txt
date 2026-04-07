Layman-friendly Google Sheet tabs for map + seats widgets

Use these tab names when uploading CSVs:
1) Constituency_Static
2) Partywise_Static (seat widget static party-wise historical data)
3) Live_Results_2026
4) Live_Partywise_2026 (seat widget 2026 live wins/leads source)
5) Party_Alliance_Map
6) Live_Alliance_2026 (optional but recommended if live tab has no alliance column)
7) Party_Color
8) Alliance_Color
9) Kannada_Labels

CSV files in this folder:
- constituency_static.csv
- partywise_static.csv
- live_results_2026.csv
- live_partywise_2026.csv
- party_alliance_map.csv
- live_alliance_2026.csv
- party_color.csv
- alliance_color.csv
- kannada_labels.csv

Single workbook in this folder:
- election-upload-layman-friendly.xlsx

Map widget URL example:
http://127.0.0.1:8000/map-widget.html?state=KERALA&sheetId=YOUR_SHEET_ID&resultsTab=Constituency_Static&resultsLiveTab=Live_Results_2026&mappingTab=Party_Alliance_Map&mappingLiveTab=Live_Alliance_2026&partiesTab=Party_Color&alliancesTab=Alliance_Color&i18nTab=Kannada_Labels

Seat widget URL example:
http://127.0.0.1:8000/seat-results-widget.html?sheetId=YOUR_SHEET_ID&partyYearTab=Partywise_Static&partyYearLiveTab=Live_Partywise_2026&mappingTab=Party_Alliance_Map&partiesTab=Party_Color&alliancesTab=Alliance_Color

If you skip the live alliance override tab, remove mappingLiveTab from the map URL.

Widget dependency map

Map widget (map-widget.html)
- Required static tabs:
  - Constituency_Static
  - Party_Alliance_Map
  - Party_Color
- Required live tabs:
  - Live_Results_2026
- Optional live/visual tabs:
  - Live_Alliance_2026 (live alliance override)
  - Alliance_Color (alliance color control)
  - Kannada_Labels (UI translations)

Seats widget (seat-results-widget.html)
- Required static tabs:
  - Partywise_Static
  - Party_Alliance_Map
  - Party_Color
- Required live tabs:
  - Live_Partywise_2026
- Optional visual tab:
  - Alliance_Color

Notes
- Seats widget does not use constituency rows.
- Live_Alliance_2026 can be shared by both widgets.

Key Battles widget
- File: key-battles-widget.html
- Template CSV: key_battles_template.csv
- Recommended tab name: Key_Battles
- No-param default (uses default published sheet + Key_Battles tab):
  http://127.0.0.1:8000/key-battles-widget.html
- URL example:
  http://127.0.0.1:8000/key-battles-widget.html?sheetId=YOUR_SHEET_ID&tab=Key_Battles
- Story embed for one battle:
  http://127.0.0.1:8000/key-battles-widget.html?sheetId=YOUR_SHEET_ID&tab=Key_Battles&battle=dharmadam_2026
- Before/After result versions:
  - before: `.../key-battles-widget.html?...&view=before`
  - after: `.../key-battles-widget.html?...&view=after`
  - auto (default): `.../key-battles-widget.html?...&view=auto`
