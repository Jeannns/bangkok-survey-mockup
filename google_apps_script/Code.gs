/**
 * Backend for survey_mockup.html's "Save draft" / "Submit" / resume-by-code
 * flow. Deploy this bound to a Google Sheet as a Web App (Extensions > Apps
 * Script in the Sheet, paste this in, then Deploy > New deployment > Web
 * app, Execute as: Me, Who has access: Anyone). Paste the resulting /exec
 * URL into the `API_URL` constant near the top of survey_mockup.html.
 *
 * Data model: one row per respondent "progress code", upserted in place.
 * The full in-progress answer state is stored as a single JSON blob per row
 * (column E) rather than one spreadsheet column per survey question, so
 * adding/changing questions in the mockup never requires touching this
 * script or the sheet's columns. See flatten_responses.py in this repo for
 * a script that expands data_json into one column per question for
 * analysis, once fieldwork data starts coming in.
 *
 * Sheet columns: code | status | created_at | updated_at | data_json
 *   status is 'in_progress' until a 'submit' action sets it to 'submitted'.
 */

const SHEET_NAME = 'Responses';

function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
  } catch (err) {
    return jsonOut({ ok: false, error: 'server_busy' });
  }
  try {
    const body = JSON.parse(e.postData.contents);
    const action = body.action;
    const code = (body.code || '').trim();
    if (!code) return jsonOut({ ok: false, error: 'missing_code' });
    if (action !== 'saveDraft' && action !== 'submit') {
      return jsonOut({ ok: false, error: 'unknown_action' });
    }

    const sheet = getSheet();
    const rowIndex = findRow(sheet, code);
    const now = new Date().toISOString();
    const status = action === 'submit' ? 'submitted' : 'in_progress';
    const dataJson = JSON.stringify(body.data || {});

    if (rowIndex > 0) {
      sheet.getRange(rowIndex, 2).setValue(status);       // B: status
      sheet.getRange(rowIndex, 4).setValue(now);          // D: updated_at
      sheet.getRange(rowIndex, 5).setValue(dataJson);      // E: data_json
    } else {
      sheet.appendRow([code, status, now, now, dataJson]);
    }
    return jsonOut({ ok: true, status: status });
  } catch (err) {
    return jsonOut({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  const action = e.parameter.action;
  const code = (e.parameter.code || '').trim();
  if (action !== 'loadDraft') return jsonOut({ ok: false, error: 'unknown_action' });
  if (!code) return jsonOut({ ok: false, error: 'missing_code' });

  const sheet = getSheet();
  const rowIndex = findRow(sheet, code);
  if (rowIndex === 0) return jsonOut({ ok: true, found: false });

  const row = sheet.getRange(rowIndex, 1, 1, 5).getValues()[0];
  let data;
  try {
    data = JSON.parse(row[4] || '{}');
  } catch (err) {
    data = {};
  }
  return jsonOut({ ok: true, found: true, status: row[1], data: data });
}

function getSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow(['code', 'status', 'created_at', 'updated_at', 'data_json']);
  }
  return sheet;
}

function findRow(sheet, code) {
  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return 0;
  const values = sheet.getRange(2, 1, lastRow - 1, 1).getValues();
  for (let i = 0; i < values.length; i++) {
    if (values[i][0] === code) return i + 2;
  }
  return 0;
}

function jsonOut(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
