# Data Architecture Plan — Elections Widget

## Sheet Access
Share the Google Sheet **only** with the service account email as a viewer:
```
election-widgets@sheets-api-testing-492608.iam.gserviceaccount.com
```
The sheet stays completely private — not published to web, not shared publicly.

---

## Architecture

```
Widget → CloudFront → Lambda → Sheets API (service account auth) → Private Sheet
```

---

## Phases

### Phase 1 — Dev (Now)
- **Proxy:** Google Apps Script Web App (deployed as Web App, runs as sheet owner)
- **Widget config:** `?csvUrl=https://script.google.com/macros/s/DEPLOY_ID/exec`
- **Sheet:** Share with service account email (viewer)
- Apps Script authenticates automatically as the sheet owner — no credentials needed in code

```js
// Apps Script
function doGet() {
  const sheet = SpreadsheetApp.openById('SHEET_ID').getSheetByName('Key_Battles');
  const rows = sheet.getDataRange().getValues();
  const csv = rows.map(r =>
    r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',')
  ).join('\n');
  return ContentService
    .createTextOutput(csv)
    .setMimeType(ContentService.MimeType.CSV);
}
```

### Phase 2 — Production (CloudFront)
- **Proxy:** AWS Lambda behind CloudFront
- **Widget config:** `?csvUrl=https://d123.cloudfront.net/api/key-battles`
- **Auth:** Lambda uses service account JSON (`sheets-api-testing-492608-4d057136ce27.json`) stored as an environment secret
- **Sheet sharing:** unchanged — same service account, same viewer access

```python
# Lambda (Python, google-auth library)
from google.oauth2 import service_account
from googleapiclient.discovery import build

def handler(event, context):
    creds = service_account.Credentials.from_service_account_info(
        json.loads(os.environ['SERVICE_ACCOUNT_JSON']),
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range='Key_Battles'
    ).execute()
    # convert to CSV and return
```

---

## Key Points
- **No API key needed** at any phase — service account handles all auth server-side
- **Widget code never changes** between phases — just swap the `csvUrl`
- **Sheet never goes public** — only the service account has access
- **Service account JSON** must never be committed to git (covered by `*.json` in `.gitignore`)

---

## Credentials
| File | Location | Usage |
|---|---|---|
| `sheets-api-testing-492608-4d057136ce27.json` | repo root (gitignored) | Lambda env secret in production |
| Service account email | see JSON `client_email` | Sheet viewer access |
