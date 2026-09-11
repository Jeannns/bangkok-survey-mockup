const fs = require('fs');
const { JSDOM } = require('jsdom');
const bodyHtml = fs.readFileSync('/tmp/body.html', 'utf8');
const mainScript = fs.readFileSync('/tmp/extracted.js', 'utf8');
const dom = new JSDOM(`<!DOCTYPE html><html><body>${bodyHtml}</body></html>`, { runScripts: 'dangerously', url: 'https://example.com/' });
const doc = dom.window.document;
const s1 = doc.createElement('script'); s1.textContent = mainScript; doc.body.appendChild(s1);
const testCode = `
window.__log = [];
try {
  nAdultsTarget = 1; nChildrenTarget = 1;
  createCharacters();
  const adult = characters.find(c=>c.kind==='adult');
  setTripPerson(adult.id);
  const stopId = stops[0].id;

  // no loc yet -> Edit should show the quick-pick list
  openStopLocationPicker(stopId);
  window.__log.push(['freshShowsList', document.getElementById('modal-body').innerHTML.includes('stop-item')]);
  window.__log.push(['freshShowsManualLink', document.getElementById('modal-body').innerHTML.includes('Not in this list')]);

  // set as custom via the manual flow
  A[stopId+'_name'] = 'Hospital';
  confirmStopLocCustom(stopId);
  window.__log.push(['isCustomNow', stops[0].loc.type === 'custom']);

  // Edit again -> should jump straight into the location edit form (locpicker), not the list
  openStopLocationPicker(stopId);
  const body = document.getElementById('modal-body').innerHTML;
  window.__log.push(['customEditShowsLocpicker', body.includes('locpicker')]);
  window.__log.push(['customEditPrefillsName', body.includes('value="Hospital"')]);
  window.__log.push(['customEditHasBackToList', body.includes('showStopLocList')]);
  window.__log.push(['customEditNotShowingBareList', !body.includes('class="stop-list"')]);

  // going back to list works
  showStopLocList(stopId);
  window.__log.push(['backToListWorks', document.getElementById('modal-body').innerHTML.includes('class="stop-list"')]);

  window.__ok = true;
} catch(e) { window.__err = e.stack || String(e); }
`;
const s2 = doc.createElement('script'); s2.textContent = testCode; doc.body.appendChild(s2);
setTimeout(()=>{
  const w = dom.window;
  if (w.__err) { console.log('ERROR:', w.__err); process.exit(1); }
  console.log('OK:', w.__ok);
  console.log(JSON.stringify(w.__log, null, 2));
}, 200);
