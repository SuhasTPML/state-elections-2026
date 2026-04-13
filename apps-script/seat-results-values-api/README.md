# Seat Results Values API

This Apps Script web app exposes either one sheet tab at a time or multiple tabs in one request, using a Google Sheets API `values`-style shape.

## Contract

Request:

```text
<web-app-url>?action=values&sheetId=<sheet-id>&tab=<tab-name>
```

Response:

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

Multi-tab request:

```text
<web-app-url>?action=multiValues&sheetId=<sheet-id>&request=summary|Partywise_Static|ASSAM&request=mapping|Party_Alliance_Map|
```

Multi-tab response:

```json
{
  "results": {
    "summary": {
      "range": "Partywise_Static!A1:G100",
      "majorDimension": "ROWS",
      "values": [
        ["state_key", "year", "party_code", "wins", "leads"],
        ["ASSAM", "2021", "BJP", "60", "0"]
      ]
    },
    "mapping": {
      "range": "Party_Alliance_Map!A1:G100",
      "majorDimension": "ROWS",
      "values": [
        ["party_code", "alliance"],
        ["BJP", "NDA"]
      ]
    }
  }
}
```

`request` is repeatable and uses `alias|tab|stateFilter`.

## Deployment

1. Create a new Apps Script project.
2. Copy `Code.gs` and `appsscript.json`.
3. Deploy as a Web App.
4. Use `Execute as: Me`.
5. Grant the script owner account access to the private spreadsheet.

## Widget usage

Example:

```text
http://127.0.0.1:8000/seat-results-widget.html?apiUrl=https://script.google.com/macros/s/DEPLOY_ID/exec&sheetId=YOUR_SHEET_ID
```

Optional tab params still work:

- `partyYearTab`
- `partyYearLiveTab`
- `mappingTab`
- `mappingLiveTab`
- `partiesTab`
- `alliancesTab`
