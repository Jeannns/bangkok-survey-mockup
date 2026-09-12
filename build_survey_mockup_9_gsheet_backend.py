"""
Patch script (audit trail, not an active build pipeline): wires the RP mockup
up to a real Google Sheet backend (via a Google Apps Script Web App the user
deploys themselves -- see google_apps_script/Code.gs and
SETUP_GOOGLE_SHEET_BACKEND.md added alongside this script).

Design (per the conversation that led to this): single shared survey link (no
pre-known household list, so per-household unique links don't work); each
visitor gets a random "progress code" generated client-side and stored in
localStorage, shown on the Welcome screen so they can write it down and type
it back in to resume on a different device. "Save draft" now actually POSTs
the full in-memory state to the Apps Script backend (upsert by code, via
LockService server-side to avoid write collisions); "Submit Survey" POSTs a
final copy and flips the row's status. Until API_URL is filled in after
deploying Code.gs, Save/Submit just show a "demo mode - not saved" message
instead of silently pretending to work.

Run against a checkout of the commit *before* this change to reproduce it:
    git show <prev_commit>:survey_mockup.html > /tmp/survey_mockup_prev.html
    python3 build_survey_mockup_9_gsheet_backend.py /tmp/survey_mockup_prev.html /tmp/out.html
    diff /tmp/out.html survey_mockup.html   # should be empty
"""
import sys


def rep(text, old, new, expect=1):
    count = text.count(old)
    if count != expect:
        raise SystemExit(f"Expected {expect} occurrence(s) of {old!r}, found {count}")
    return text.replace(old, new)


BACKEND_JS = '''
/* ================= BACKEND (Google Sheet via Apps Script) =================
   To enable real data capture: create a Google Sheet, open Extensions > Apps
   Script, paste in google_apps_script/Code.gs from this repo, deploy it as a
   Web App (Execute as: Me, Who has access: Anyone), then paste the
   deployment URL below. See SETUP_GOOGLE_SHEET_BACKEND.md for the full
   walkthrough. Until API_URL is set, Save Draft / Submit show a "demo mode -
   not saved" message instead of silently pretending to persist anything. */
const API_URL = ''; // <- paste your Apps Script Web App URL here after deploying

function genRespondentCode(){
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // no 0/O/1/I, avoids confusion when handwritten
  let s = '';
  for(let i=0;i<8;i++) s += chars[Math.floor(Math.random()*chars.length)];
  return s.slice(0,4)+'-'+s.slice(4);
}
let respondentCode = localStorage.getItem('bkk_survey_code') || genRespondentCode();
localStorage.setItem('bkk_survey_code', respondentCode);
let backendStatus = null; // null | 'saving' | 'saved' | 'error' | 'not_configured'
let alreadySubmitted = localStorage.getItem('bkk_survey_submitted_'+respondentCode) === '1';

function collectState(){
  return { A, characters, tripsByPerson, diaryDate, maintActivities, lang };
}
function restoreState(data){
  if(!data) return;
  Object.keys(A).forEach(k=>delete A[k]);
  Object.assign(A, data.A||{});
  characters = data.characters||[];
  tripsByPerson = data.tripsByPerson||{};
  diaryDate = data.diaryDate||'';
  maintActivities = data.maintActivities||[{name:''}];
  lang = data.lang||lang;
}

async function backendPost(action){
  if(!API_URL){ backendStatus='not_configured'; return {ok:false, error:'not_configured'}; }
  backendStatus='saving'; renderRP();
  try{
    const res = await fetch(API_URL, { method:'POST', body: JSON.stringify({action, code:respondentCode, data:collectState()}) });
    const json = await res.json();
    backendStatus = json.ok ? 'saved' : 'error';
    return json;
  }catch(err){
    backendStatus='error';
    return {ok:false, error:String(err)};
  }
}
async function backendLoad(code){
  if(!API_URL) return {ok:false, error:'not_configured'};
  try{
    const res = await fetch(API_URL + '?action=loadDraft&code=' + encodeURIComponent(code));
    return await res.json();
  }catch(err){
    return {ok:false, error:String(err)};
  }
}
window.resumeWithCode = async (code)=>{
  code = (code||'').trim().toUpperCase();
  if(!code) return;
  const result = await backendLoad(code);
  if(result.ok && result.found){
    restoreState(result.data);
    respondentCode = code;
    localStorage.setItem('bkk_survey_code', respondentCode);
    alreadySubmitted = result.status==='submitted';
    renderRP();
    alert(t('Draft loaded - continuing where you left off.'));
  } else {
    alert(t('No saved draft found for that code.'));
  }
};
async function tryAutoResume(){
  const result = await backendLoad(respondentCode);
  if(result.ok && result.found){
    restoreState(result.data);
    alreadySubmitted = result.status==='submitted';
    renderRP();
  }
}
'''


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "survey_mockup.html"
    dst = sys.argv[2] if len(sys.argv) > 2 else src
    html = open(src, encoding="utf-8").read()

    # --- 1. insert the backend module right after the shared `val()` helper ---
    html = rep(
        html,
        "const A = {};\nfunction val(id,d){return A[id]!==undefined?A[id]:d;}\n",
        "const A = {};\nfunction val(id,d){return A[id]!==undefined?A[id]:d;}\n" + BACKEND_JS,
    )

    # --- 2. Welcome step: show the progress code + a resume-with-code input ---
    html = rep(
        html,
        "  ${devMode?`<p style=\"color:var(--sub);font-size:12px;margin-top:10px\">${t('(dev mode on - completion checks are bypassed on every page)')}</p>`:''}\n  </div>`},",
        "  ${devMode?`<p style=\"color:var(--sub);font-size:12px;margin-top:10px\">${t('(dev mode on - completion checks are bypassed on every page)')}</p>`:''}\n"
        "  <div class=\"q-note\" style=\"margin-top:16px\">${t('Your progress code:')} <b>${respondentCode}</b> - ${t('write this down if you plan to continue later on a different device.')}</div>\n"
        "  <div class=\"field\" style=\"margin-top:10px\"><div class=\"q-label\" style=\"font-size:13px\">${t('Already started on another device? Enter your code to resume:')}</div>\n"
        "    <div style=\"display:flex;gap:8px\"><input type=\"text\" id=\"resume-code-input\" placeholder=\"XXXX-XXXX\" style=\"flex:1\"><button class=\"btn btn-ghost\" style=\"border:1px solid var(--line)\" onclick=\"resumeWithCode(document.getElementById('resume-code-input').value)\">${t('Resume')}</button></div></div>\n"
        "  </div>`},",
    )

    # --- 3. tempSaveBtn/tempSave: reflect real backend status + actually POST ---
    html = rep(
        html,
        "function tempSaveBtn(){\n  return `<button class=\"btn btn-ghost\" style=\"border:1px solid var(--line)\" onclick=\"tempSave()\">${lastSavedAt?t('Draft saved ')+lastSavedAt:t('Save draft')}</button>`;\n}",
        "function tempSaveBtn(){\n"
        "  const label = backendStatus==='saving' ? t('Saving...')\n"
        "    : backendStatus==='error' ? t('Save failed - tap to retry')\n"
        "    : backendStatus==='not_configured' ? t('Save draft (offline demo)')\n"
        "    : lastSavedAt ? t('Draft saved ')+lastSavedAt : t('Save draft');\n"
        "  return `<button class=\"btn btn-ghost\" style=\"border:1px solid var(--line)\" onclick=\"tempSave()\">${label}</button>`;\n"
        "}",
    )
    html = rep(
        html,
        "window.tempSave = ()=>{ lastSavedAt = new Date().toLocaleTimeString(); renderRP(); };",
        "window.tempSave = async ()=>{\n"
        "  const result = await backendPost('saveDraft');\n"
        "  if(result.ok) lastSavedAt = new Date().toLocaleTimeString();\n"
        "  renderRP();\n"
        "};",
    )

    # --- 4. finishSubmit: actually POST the final answers instead of just showing a thank-you screen ---
    html = rep(
        html,
        "window.finishSubmit = ()=>{\n  document.getElementById('modal-overlay').classList.remove('open');\n  document.getElementById('rp-card').innerHTML = `<div class=\"hero\"><h1>${t('Submitted - thank you!')}</h1><p>${t('Your responses have been recorded. You may now close this window.')}</p></div>`;\n};",
        "window.finishSubmit = async ()=>{\n"
        "  document.getElementById('modal-overlay').classList.remove('open');\n"
        "  document.getElementById('rp-card').innerHTML = `<div class=\"hero\"><h1>${t('Submitting...')}</h1></div>`;\n"
        "  const result = await backendPost('submit');\n"
        "  if(result.ok){\n"
        "    localStorage.setItem('bkk_survey_submitted_'+respondentCode,'1');\n"
        "    alreadySubmitted = true;\n"
        "    document.getElementById('rp-card').innerHTML = `<div class=\"hero\"><h1>${t('Submitted - thank you!')}</h1><p>${t('Your responses have been recorded. You may now close this window.')}</p></div>`;\n"
        "  } else if(result.error==='not_configured'){\n"
        "    document.getElementById('rp-card').innerHTML = `<div class=\"hero\"><h1>${t('Demo mode - not saved')}</h1><p>${t('This mockup is not yet connected to a real backend, so nothing was saved. See SETUP_GOOGLE_SHEET_BACKEND.md to connect one.')}</p></div>`;\n"
        "  } else {\n"
        "    document.getElementById('rp-card').innerHTML = `<div class=\"hero\"><h1>${t('Something went wrong')}</h1><p>${t('Your answers were not sent. Please check your internet connection and try Submit again from the Review page.')}</p><button class=\"btn btn-primary\" onclick=\"rpIdx=rpSteps.findIndex(s=>s.name==='Review & Submit');renderRP()\">${t('Back to Review')}</button></div>`;\n"
        "  }\n"
        "};",
    )

    # --- 5. bootstrap: try loading an existing draft for this code once, after first paint ---
    html = rep(
        html,
        "renderTabLabels();\nrenderRP();",
        "renderTabLabels();\nrenderRP();\ntryAutoResume();",
    )

    open(dst, "w", encoding="utf-8").write(html)
    print(f"Wrote {dst} ({len(html)} chars)")


if __name__ == "__main__":
    main()
