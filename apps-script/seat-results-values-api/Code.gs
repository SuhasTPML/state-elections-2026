function doGet(e) {
  try {
    const params = (e && e.parameter) || {};
    const action = String(params.action || 'values').trim().toLowerCase();
    if (action !== 'values') {
      return jsonResponse({ error: 'Unsupported action. Use action=values.' }, 400);
    }

    const sheetId = extractSheetId(params.sheetId || params.sheetUrl || '');
    const tabName = String(params.tab || '').trim();
    const stateFilter = String(params.stateFilter || '').trim().toUpperCase();

    if (!sheetId) {
      return jsonResponse({ error: 'Missing sheetId or sheetUrl.' }, 400);
    }
    if (!tabName) {
      return jsonResponse({ error: 'Missing tab.' }, 400);
    }

    const accessToken = getServiceAccountToken();
    const data = getSheetValues(accessToken, sheetId, tabName);

    var values = data.values || [];
    if (stateFilter && values.length > 1) {
      var headers = values[0];
      var STATE_COLS = ['state_key', 'state_code', 'state'];
      var colIdx = -1;
      for (var i = 0; i < STATE_COLS.length; i++) {
        for (var j = 0; j < headers.length; j++) {
          if (String(headers[j] || '').trim().toLowerCase() === STATE_COLS[i]) {
            colIdx = j;
            break;
          }
        }
        if (colIdx >= 0) break;
      }
      if (colIdx >= 0) {
        var filtered = values.slice(1).filter(function(row) {
          return String(row[colIdx] || '').trim().toUpperCase() === stateFilter;
        });
        values = [headers].concat(filtered);
      }
    }

    return jsonResponse({
      range: data.range || (tabName + '!A1'),
      majorDimension: data.majorDimension || 'ROWS',
      values: values
    });
  } catch (error) {
    return jsonResponse({
      error: String(error && error.message ? error.message : error)
    }, 500);
  }
}

/**
 * Generates a short-lived OAuth2 access token using the service account credentials
 * stored in Script Properties (SERVICE_ACCOUNT_EMAIL and SERVICE_ACCOUNT_PRIVATE_KEY).
 */
function getServiceAccountToken() {
  const props = PropertiesService.getScriptProperties();
  const email = props.getProperty('SERVICE_ACCOUNT_EMAIL');
  const privateKey = props.getProperty('SERVICE_ACCOUNT_PRIVATE_KEY');

  if (!email || !privateKey) {
    throw new Error(
      'Service account credentials not found in Script Properties. ' +
      'Set SERVICE_ACCOUNT_EMAIL and SERVICE_ACCOUNT_PRIVATE_KEY.'
    );
  }

  // Normalize the private key: replace literal \n sequences with real newlines
  const normalizedKey = privateKey.replace(/\\n/g, '\n');

  const now = Math.floor(Date.now() / 1000);
  const claim = {
    iss: email,
    scope: 'https://www.googleapis.com/auth/spreadsheets.readonly',
    aud: 'https://oauth2.googleapis.com/token',
    iat: now,
    exp: now + 3600
  };

  const header = base64UrlEncode(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
  const payload = base64UrlEncode(JSON.stringify(claim));
  const signingInput = header + '.' + payload;

  const signature = Utilities.computeRsaSha256Signature(
    signingInput,
    normalizedKey,
    Utilities.Charset.UTF_8
  );
  const jwt = signingInput + '.' + base64UrlEncode(signature);

  const tokenResponse = UrlFetchApp.fetch('https://oauth2.googleapis.com/token', {
    method: 'post',
    contentType: 'application/x-www-form-urlencoded',
    payload:
      'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer' +
      '&assertion=' + jwt,
    muteHttpExceptions: true
  });

  const tokenData = JSON.parse(tokenResponse.getContentText());
  if (!tokenData.access_token) {
    throw new Error('Failed to obtain access token: ' + JSON.stringify(tokenData));
  }
  return tokenData.access_token;
}

/**
 * Fetches sheet values via the Sheets REST API using a bearer token.
 */
function getSheetValues(accessToken, sheetId, tabName) {
  const encodedTab = encodeURIComponent(tabName);
  const url =
    'https://sheets.googleapis.com/v4/spreadsheets/' +
    encodeURIComponent(sheetId) +
    '/values/' +
    encodedTab +
    '?valueRenderOption=FORMATTED_VALUE&majorDimension=ROWS';

  const response = UrlFetchApp.fetch(url, {
    headers: { Authorization: 'Bearer ' + accessToken },
    muteHttpExceptions: true
  });

  const data = JSON.parse(response.getContentText());
  if (response.getResponseCode() !== 200) {
    const msg = (data.error && data.error.message) || JSON.stringify(data);
    throw new Error('Sheets API error (' + response.getResponseCode() + '): ' + msg);
  }
  return data;
}

/** Base64url-encodes a string or byte array (no padding). */
function base64UrlEncode(input) {
  var bytes = (typeof input === 'string')
    ? Utilities.newBlob(input).getBytes()
    : input;
  return Utilities.base64EncodeWebSafe(bytes).replace(/=+$/, '');
}

function extractSheetId(value) {
  var raw = String(value || '').trim();
  if (!raw) return '';
  var match = raw.match(/\/spreadsheets\/d\/([a-zA-Z0-9-_]+)/);
  if (match && match[1]) return match[1];
  return raw;
}

function jsonResponse(payload, statusCode) {
  var body = Object.assign({ status: statusCode || 200 }, payload || {});
  return ContentService
    .createTextOutput(JSON.stringify(body))
    .setMimeType(ContentService.MimeType.JSON);
}
