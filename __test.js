const fs = require('fs');
const { JSDOM } = require('jsdom');

const bodyHtml = fs.readFileSync('/tmp/body.html', 'utf8');
const mainScript = fs.readFileSync('/tmp/extracted.js', 'utf8');

const dom = new JSDOM(`<!DOCTYPE html><html><body>${bodyHtml}</body></html>`, { runScripts: 'dangerously', url: 'https://example.com/' });
const doc = dom.window.document;

const s1 = doc.createElement('script');
s1.textContent = mainScript;
doc.body.appendChild(s1);

const testCode = `
window.__log = [];
try {
  // set up a household: 1 adult (work registered), 1 child (school registered)
  nAdultsTarget = 1; nChildrenTarget = 1;
  createCharacters();
  const adult = characters.find(c=>c.kind==='adult');
  const child = characters.find(c=>c.kind==='child');
  A[adult.id+'_name'] = 'Somchai';
  A[child.id+'_name'] = 'Nong';

  // set trip person to the adult, generating default stops via newStop()
  setTripPerson(adult.id);
  window.__log.push(['stopsHaveIds', stops.every(s=>!!s.id)]);
  window.__log.push(['stopsHaveLocNull', stops.every(s=>s.loc===null)]);

  const stopA = stops[0];
  // pick "home" for stop A
  pickStopLoc(stopA.id, undefined);
  window.__log.push(['stopA_loc_type', stops[0].loc && stops[0].loc.type]);
  window.__log.push(['stopA_label', stopLocLabel(stops[0])]);

  // pick registered school for the middle stop
  const stopB = stops[1];
  pickStopLoc(stopB.id, 'school', child.id);
  window.__log.push(['stopB_loc_type', stops[1].loc && stops[1].loc.type]);
  window.__log.push(['stopB_label', stopLocLabel(stops[1])]);

  // add a new stop and mark custom
  stops.splice(stops.length-1, 0, newStop('Market'));
  const stopC = stops[stops.length-2];
  A[stopC.id+'_name'] = 'Fresh Market';
  confirmStopLocCustom(stopC.id);
  window.__log.push(['stopC_loc_type', stops[stops.length-2].loc && stops[stops.length-2].loc.type]);
  window.__log.push(['stopC_label', stopLocLabel(stops[stops.length-2])]);

  // render the trip-details step markup to make sure Edit buttons + labels are present, no crash
  rpIdx = rpSteps.findIndex(s=>s.name==='Travel Diary - Register a Trip');
  const html = rpSteps[rpIdx].render();
  window.__log.push(['renderHasEditStop', html.includes('edit-stop')]);
  window.__log.push(['renderHasHomeLabel', html.includes('Home (registered)')]);
  window.__log.push(['renderHasSchoolLabel', html.includes('school (registered)')]);
  window.__log.push(['renderHasCustomLabel', html.includes('Fresh Market')]);

  // openStopLocationPicker should populate modal without throwing
  openStopLocationPicker(stops[0].id);
  window.__log.push(['modalOpened', document.getElementById('modal-overlay').classList.contains('open')]);
  window.__log.push(['modalHasAdult', document.getElementById('modal-body').innerHTML.includes('Somchai')]);
  window.__log.push(['modalHasChild', document.getElementById('modal-body').innerHTML.includes('Nong')]);

  window.__ok = true;
} catch(e) {
  window.__err = e.stack || String(e);
}
`;
const s2 = doc.createElement('script');
s2.textContent = testCode;
doc.body.appendChild(s2);

setTimeout(()=>{
  const w = dom.window;
  if (w.__err) {
    console.log('ERROR:', w.__err);
    process.exit(1);
  }
  console.log('OK:', w.__ok);
  console.log(JSON.stringify(w.__log, null, 2));
}, 200);
