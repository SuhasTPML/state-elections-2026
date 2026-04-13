# Widget Query Parameters

Reference for all supported URL query parameters across the three election widgets.

---

## map-widget.html

### Display / Behaviour

| Parameter | Values | What it shows |
|---|---|---|
| `state` | `TAMIL_NADU`, `KERALA`, `WEST_BENGAL`, `ASSAM`, `PUDUCHERRY` | Opens the widget on that state instead of the default (Tamil Nadu) |
| `hideTabs` | `true` | Hides the state tab bar — use when embedding for a specific state |
| `ac` | AC number e.g. `001` | Pre-selects and highlights that constituency on load |
| `name` | Constituency name e.g. `Thiruvananthapuram` | Pre-selects the matching constituency on load |
| `lang` | `kn` | Switches labels to Kannada |

### Data source (advanced)

| Parameter | What it does |
|---|---|
| `sheetId` / `sheetUrl` | Use a different Google Sheet |
| `apiUrl` / `appsScriptUrl` | Use a different Apps Script deployment |
| `resultsTab` | Override the static results tab name (default: `Constituency_Static`) |
| `resultsLiveTab` / `liveResultsTab` | Override the live results tab name (default: `Live_Results_2026`) |
| `mappingTab` | Override the party-alliance mapping tab (default: `Party_Alliance_Map`) |
| `mappingLiveTab` / `liveMappingTab` | Override the live mapping tab (default: `Live_Alliance_2026`) |
| `partiesTab` | Override the party colour tab (default: `Party_Color`) |
| `alliancesTab` | Override the alliance colour tab (default: `Alliance_Color`) |
| `publishedKey` | Published sheet key for CSV fallback |

### Example URLs

```
# Open on Kerala, hide tabs (for CMS embed)
map-widget.html?state=KERALA&hideTabs=true

# Open on Assam, pre-select constituency 42
map-widget.html?state=ASSAM&ac=042

# Kannada language, Tamil Nadu
map-widget.html?state=TAMIL_NADU&lang=kn
```

---

## key-battles-widget.html

### Display / Behaviour

| Parameter | Values | What it shows |
|---|---|---|
| `state` | `TAMIL_NADU`, `KERALA`, `WEST_BENGAL`, `ASSAM`, `PUDUCHERRY` | Selects that state tab and filters cards to that state (default: Tamil Nadu) |
| `hideTabs` | `true` | Hides the state tab bar — use when embedding for a specific state |
| `constituency` / `ac` / `acName` | Constituency name or AC number e.g. `Thiruvananthapuram` or `001` | Shows **only that constituency's card**, hides tabs and search bar entirely |
| `battle` / `battleId` | Battle ID slug e.g. `thiruvananthapuram_2026` | Shows only the card matching that battle ID |
| `view` / `phase` | `live`, `static`, `auto` | Forces live or static result view (default: `auto`) |

### Data source (advanced)

| Parameter | What it does |
|---|---|
| `sheetId` / `sheetUrl` | Use a different Google Sheet |
| `apiUrl` / `appsScriptUrl` | Use a different Apps Script deployment |
| `tab` / `keyBattlesTab` | Override the key battles tab name (default: `Key_Battles`) |
| `mappingLiveTab` | Override the live mapping tab (default: `Live_Alliance_2026`) |
| `partiesTab` | Override the party colour tab (default: `Party_Color`) |
| `alliancesTab` | Override the alliance colour tab (default: `Alliance_Color`) |

### Example URLs

```
# Show Kerala battles, hide tabs (for CMS embed)
key-battles-widget.html?state=KERALA&hideTabs=true

# Show only the Thiruvananthapuram card (no tabs, no search)
key-battles-widget.html?constituency=Thiruvananthapuram

# Show only Dharmadam by AC number
key-battles-widget.html?ac=011

# Show Assam battles with tabs visible
key-battles-widget.html?state=ASSAM
```

---

## seat-results-widget.html

### Display / Behaviour

| Parameter | Values | What it shows |
|---|---|---|
| `state` | `TAMIL_NADU`, `KERALA`, `WEST_BENGAL`, `ASSAM`, `PUDUCHERRY` | Opens on that state's seat result chart (default: first state in tab order) |
| `hideTabs` | `true` | Hides the state tab bar — use when embedding for a specific state |
| `refreshMs` | milliseconds e.g. `30000` | Auto-refreshes live data every N milliseconds |
| `refreshSeconds` | seconds e.g. `30` | Same as `refreshMs` but in seconds |

### Data source (advanced)

| Parameter | What it does |
|---|---|
| `sheetId` / `sheetUrl` | Use a different Google Sheet |
| `apiUrl` / `appsScriptUrl` | Use a different Apps Script deployment |
| `partyYearTab` / `partySummaryTab` / `partyWiseTab` | Override the static results tab |
| `partyYearLiveTab` / `partySummaryLiveTab` / `partyWiseLiveTab` | Override the live results tab |
| `mappingTab` | Override the party-alliance mapping tab (default: `Party_Alliance_Map`) |
| `mappingLiveTab` | Override the live mapping tab (default: `Live_Alliance_2026`) |
| `partiesTab` | Override the party colour tab (default: `Party_Color`) |
| `alliancesTab` | Override the alliance colour tab (default: `Alliance_Color`) |

### Example URLs

```
# Show Kerala seat results, hide tabs (for CMS embed)
seat-results-widget.html?state=KERALA&hideTabs=true

# Show West Bengal with auto-refresh every 30s
seat-results-widget.html?state=WEST_BENGAL&refreshSeconds=30

# Puducherry, tabs hidden, auto-refresh
seat-results-widget.html?state=PUDUCHERRY&hideTabs=true&refreshSeconds=60
```

---

## Parameter priority rules

- `constituency` / `ac` takes precedence in key-battles — it overrides state filtering and hides everything else
- `state` without `hideTabs` shows tabs with that state pre-selected
- `state` with `hideTabs=true` shows that state's data with no tab bar
- All data source params (`sheetId`, `apiUrl`, tab names) override the defaults but fall back to defaults if omitted
