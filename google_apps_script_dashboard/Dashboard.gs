/**
 * Restricted admin dashboard for the Bangkok school-escorting survey
 * responses. THIS IS A SEPARATE APPS SCRIPT PROJECT from the one that
 * powers survey_mockup.html's Save draft / Submit (google_apps_script/Code.gs).
 * Keeping them separate means the public survey endpoint (access: Anyone)
 * and this admin view (access: Only myself) can never accidentally share a
 * deployment's access setting -- see SETUP_ADMIN_DASHBOARD.md for why this
 * matters and how to deploy it correctly.
 *
 * SECURITY: when you deploy this as a Web App, set:
 *   Execute as:      Me
 *   Who has access:  Only myself   (add specific people's emails later if needed)
 * Do NOT set this to "Anyone" -- the data behind it includes respondents'
 * household composition, home location, income, and safety-concern answers.
 *
 * Setup: fill in SHEET_ID below (from the survey response Sheet's URL:
 * https://docs.google.com/spreadsheets/d/ THIS_PART /edit), then deploy.
 * See SETUP_ADMIN_DASHBOARD.md for the full walkthrough.
 */

const SHEET_ID = ''; // <- paste the Google Sheet ID here (the long id in its URL)
const SHEET_NAME = 'Responses'; // must match the tab name used by google_apps_script/Code.gs

function doGet(e) {
  const action = e.parameter.action;
  if (action === 'listResponses') {
    return jsonOut(listResponses());
  }
  return HtmlService.createHtmlOutput(DASHBOARD_HTML)
    .setTitle('Survey Dashboard')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function listResponses() {
  if (!SHEET_ID) return { ok: false, error: 'not_configured' };
  try {
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    if (!sheet) return { ok: false, error: 'sheet_not_found' };
    const lastRow = sheet.getLastRow();
    if (lastRow < 2) return { ok: true, responses: [] };
    const values = sheet.getRange(2, 1, lastRow - 1, 5).getValues();
    const responses = values.map(function (row) {
      let data = {};
      try { data = JSON.parse(row[4] || '{}'); } catch (err) { data = {}; }
      return {
        code: row[0],
        status: row[1],
        created_at: row[2],
        updated_at: row[3],
        data: data
      };
    });
    return { ok: true, responses: responses };
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}

function jsonOut(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

const DASHBOARD_HTML = '<!DOCTYPE html>' +
'<html><head><base target="_top">' +
'<style>' +
'  body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#f6f7f9;color:#1f2430}' +
'  header{background:#1f2430;color:#fff;padding:16px 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}' +
'  header h1{font-size:17px;margin:0}' +
'  .meta{font-size:12px;color:#b8bfd1}' +
'  main{padding:20px;max-width:1100px;margin:0 auto}' +
'  .cards{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:20px}' +
'  .card{background:#fff;border-radius:10px;padding:14px 18px;box-shadow:0 1px 3px rgba(0,0,0,.08);min-width:140px}' +
'  .card .num{font-size:26px;font-weight:700}' +
'  .card .lbl{font-size:12px;color:#666}' +
'  .panel{background:#fff;border-radius:10px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:20px}' +
'  .controls{display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end;margin-bottom:14px}' +
'  .ctrl{display:flex;flex-direction:column;gap:4px}' +
'  .ctrl label{font-size:12px;color:#666}' +
'  select,input[type=checkbox]{font-size:13px;padding:6px 8px;border-radius:6px;border:1px solid #d5d8e0}' +
'  table{width:100%;border-collapse:collapse;font-size:13px}' +
'  th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #eee}' +
'  th{color:#666;font-weight:600}' +
'  .empty{color:#888;padding:30px;text-align:center}' +
'  .refresh-row{display:flex;align-items:center;gap:8px;font-size:12px;color:#666}' +
'</style></head><body>' +
'<header><h1>School Escorting Survey - Response Dashboard</h1>' +
'<div class="refresh-row"><span id="last-updated" class="meta">Loading...</span>' +
'<label style="display:flex;align-items:center;gap:5px;color:#fff"><input type="checkbox" id="auto-refresh" checked> Auto-refresh (30s)</label>' +
'<button id="refresh-btn" style="padding:6px 12px;border-radius:6px;border:none;cursor:pointer">Refresh now</button></div>' +
'</header>' +
'<main>' +
'  <div class="cards" id="summary-cards"></div>' +
'  <div class="panel">' +
'    <div class="controls">' +
'      <div class="ctrl"><label>Group by (chart)</label><select id="group-field"></select></div>' +
'      <div class="ctrl"><label>Filter by (optional)</label><select id="filter-field"><option value="">(none)</option></select></div>' +
'      <div class="ctrl" id="filter-value-wrap" style="display:none"><label>Filter value</label><select id="filter-value"></select></div>' +
'      <div class="ctrl"><label>Include</label><select id="status-scope"><option value="submitted">Submitted only</option><option value="all">Submitted + in-progress</option></select></div>' +
'    </div>' +
'    <canvas id="chart" height="90"></canvas>' +
'    <div id="chart-empty" class="empty" style="display:none">No data yet for this selection.</div>' +
'  </div>' +
'  <div class="panel">' +
'    <h3 style="margin-top:0;font-size:14px">Recent responses</h3>' +
'    <table id="recent-table"><thead><tr><th>Code</th><th>Status</th><th>Updated</th></tr></thead><tbody></tbody></table>' +
'    <div id="recent-empty" class="empty" style="display:none">No responses yet.</div>' +
'  </div>' +
'</main>' +
'<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>' +
'<script>' +
'var allResponses = [];' +
'var chart = null;' +
'function fieldKeys(rows){' +
'  var seen = {};' +
'  rows.forEach(function(r){ var a = (r.data && r.data.A) || {}; Object.keys(a).forEach(function(k){ seen[k]=true; }); });' +
'  return Object.keys(seen).sort();' +
'}' +
'function scopedRows(){' +
'  var scope = document.getElementById("status-scope").value;' +
'  return allResponses.filter(function(r){ return scope==="all" || r.status==="submitted"; });' +
'}' +
'function filteredRows(){' +
'  var rows = scopedRows();' +
'  var ff = document.getElementById("filter-field").value;' +
'  var fv = document.getElementById("filter-value").value;' +
'  if(!ff || !fv) return rows;' +
'  return rows.filter(function(r){ var a=(r.data && r.data.A)||{}; return String(a[ff])===fv; });' +
'}' +
'function populateFieldSelectors(){' +
'  var keys = fieldKeys(allResponses);' +
'  var groupSel = document.getElementById("group-field");' +
'  var filterSel = document.getElementById("filter-field");' +
'  var prevGroup = groupSel.value, prevFilter = filterSel.value;' +
'  groupSel.innerHTML = keys.map(function(k){return "<option value=\\""+k+"\\">"+k+"</option>";}).join("");' +
'  filterSel.innerHTML = "<option value=\\"\\">(none)</option>" + keys.map(function(k){return "<option value=\\""+k+"\\">"+k+"</option>";}).join("");' +
'  if(keys.indexOf(prevGroup)>=0) groupSel.value = prevGroup;' +
'  if(keys.indexOf(prevFilter)>=0) filterSel.value = prevFilter;' +
'}' +
'function populateFilterValues(){' +
'  var ff = document.getElementById("filter-field").value;' +
'  var wrap = document.getElementById("filter-value-wrap");' +
'  if(!ff){ wrap.style.display="none"; renderChart(); return; }' +
'  wrap.style.display="flex";' +
'  var vals = {};' +
'  scopedRows().forEach(function(r){ var a=(r.data && r.data.A)||{}; if(a[ff]!==undefined) vals[String(a[ff])]=true; });' +
'  var valSel = document.getElementById("filter-value");' +
'  var keys = Object.keys(vals).sort();' +
'  valSel.innerHTML = keys.map(function(k){return "<option value=\\""+k+"\\">"+k+"</option>";}).join("");' +
'  renderChart();' +
'}' +
'function renderChart(){' +
'  var field = document.getElementById("group-field").value;' +
'  var rows = filteredRows();' +
'  var counts = {};' +
'  rows.forEach(function(r){ var a=(r.data && r.data.A)||{}; var v = a[field]; if(v===undefined||v===null||v==="") return; counts[v]=(counts[v]||0)+1; });' +
'  var labels = Object.keys(counts).sort();' +
'  var data = labels.map(function(l){ return counts[l]; });' +
'  var empty = document.getElementById("chart-empty");' +
'  var canvas = document.getElementById("chart");' +
'  if(labels.length===0){ empty.style.display="block"; canvas.style.display="none"; return; }' +
'  empty.style.display="none"; canvas.style.display="block";' +
'  if(chart) chart.destroy();' +
'  chart = new Chart(canvas.getContext("2d"), { type:"bar", data:{ labels:labels, datasets:[{ label:field, data:data, backgroundColor:"#4f6df5" }] }, options:{ responsive:true, plugins:{ legend:{ display:false } }, scales:{ y:{ beginAtZero:true, ticks:{ precision:0 } } } } });' +
'}' +
'function renderSummary(){' +
'  var total = allResponses.length;' +
'  var submitted = allResponses.filter(function(r){return r.status==="submitted";}).length;' +
'  var inprog = total - submitted;' +
'  document.getElementById("summary-cards").innerHTML = ' +
'    "<div class=\\"card\\"><div class=\\"num\\">"+total+"</div><div class=\\"lbl\\">Total respondents</div></div>" +' +
'    "<div class=\\"card\\"><div class=\\"num\\">"+submitted+"</div><div class=\\"lbl\\">Submitted</div></div>" +' +
'    "<div class=\\"card\\"><div class=\\"num\\">"+inprog+"</div><div class=\\"lbl\\">In progress</div></div>";' +
'}' +
'function renderRecent(){' +
'  var rows = allResponses.slice().sort(function(a,b){ return (b.updated_at||"").localeCompare(a.updated_at||""); }).slice(0,20);' +
'  var tbody = document.querySelector("#recent-table tbody");' +
'  var empty = document.getElementById("recent-empty");' +
'  if(rows.length===0){ empty.style.display="block"; tbody.innerHTML=""; return; }' +
'  empty.style.display="none";' +
'  tbody.innerHTML = rows.map(function(r){ return "<tr><td>"+r.code+"</td><td>"+r.status+"</td><td>"+(r.updated_at||"")+"</td></tr>"; }).join("");' +
'}' +
'function renderAll(){ renderSummary(); populateFieldSelectors(); populateFilterValues(); renderRecent(); document.getElementById("last-updated").textContent = "Last updated: " + new Date().toLocaleTimeString(); }' +
'function loadData(){' +
'  fetch(window.location.href.split("?")[0] + "?action=listResponses")' +
'    .then(function(res){ return res.json(); })' +
'    .then(function(json){' +
'      if(!json.ok){ document.getElementById("last-updated").textContent = "Error: " + json.error; return; }' +
'      allResponses = json.responses || [];' +
'      renderAll();' +
'    })' +
'    .catch(function(err){ document.getElementById("last-updated").textContent = "Error: " + err; });' +
'}' +
'document.getElementById("group-field").addEventListener("change", renderChart);' +
'document.getElementById("filter-field").addEventListener("change", populateFilterValues);' +
'document.getElementById("filter-value").addEventListener("change", renderChart);' +
'document.getElementById("status-scope").addEventListener("change", function(){ populateFilterValues(); });' +
'document.getElementById("refresh-btn").addEventListener("click", loadData);' +
'var autoTimer = setInterval(function(){ if(document.getElementById("auto-refresh").checked) loadData(); }, 30000);' +
'loadData();' +
'</script>' +
'</body></html>';
