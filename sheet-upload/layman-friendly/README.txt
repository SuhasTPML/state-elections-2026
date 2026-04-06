Layman-friendly Google Sheet tabs for map widget

Use these tab names when uploading CSVs:
1) Constituency_Static
2) Live_Results_2026
3) Party_Alliance_Map
4) Live_Alliance_2026 (optional but recommended if live tab has no alliance column)
5) Party_Color
6) Alliance_Color
7) Kannada_Labels

CSV files in this folder:
- constituency_static.csv
- live_results_2026.csv
- party_alliance_map.csv
- live_alliance_2026.csv
- party_color.csv
- alliance_color.csv
- kannada_labels.csv

Single workbook in this folder:
- election-upload-layman-friendly.xlsx

Widget URL example:
http://127.0.0.1:8000/map-widget.html?state=KERALA&sheetId=YOUR_SHEET_ID&resultsTab=Constituency_Static&resultsLiveTab=Live_Results_2026&mappingTab=Party_Alliance_Map&mappingLiveTab=Live_Alliance_2026&partiesTab=Party_Color&alliancesTab=Alliance_Color&i18nTab=Kannada_Labels

If you skip the live alliance override tab, remove mappingLiveTab from the URL.
