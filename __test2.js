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
  nAdultsTarget = 1; nChildrenTarget = 1;
  createCharacters();
  const adult = characters.find(c=>c.kind==='adult');
  A[adult.id+'_name'] = 'Somchai';

  setTripPerson(adult.id);
  // fix 1: Add a stop should push to the true end
  const beforeLen = stops.length;
  const lastPlaceBefore = stops[stops.length-1].place;
  stops.push(newStop('NewLast'));
  window.__log.push(['stopPushedAtEnd', stops[stops.length-1].place === 'NewLast']);
  window.__log.push(['prevLastNowMiddle', stops[stops.length-2].place === lastPlaceBefore]);

  // fix 2: isCarMode / driver-passenger question shows for Private motorbike
  rpIdx = rpSteps.findIndex(s=>s.name==='Travel Diary - Trip Details');
  segIdx = 0;
  const ns = tripPerson+'_0';
  A['mode_'+ns] = 'Private motorbike';
  let html = rpSteps[rpIdx].render();
  window.__log.push(['motorbikeShowsDriverPax', html.includes('driverpax_'+ns)]);
  A['mode_'+ns] = 'Private car';
  html = rpSteps[rpIdx].render();
  window.__log.push(['carShowsDriverPax', html.includes('driverpax_'+ns)]);
  A['mode_'+ns] = 'Walk';
  html = rpSteps[rpIdx].render();
  window.__log.push(['walkHidesDriverPax', !html.includes('driverpax_'+ns)]);

  // fix 3: purpose options merged into 'School escort', isEscort works
  window.__log.push(['purposeHasSchoolEscort', html.includes('School escort')]);
  window.__log.push(['purposeNoDropoff', !html.includes('Going to school (drop-off)')]);
  window.__log.push(['purposeNoPickup', !html.includes('Return to school (pick-up)')]);
  const purposeKey = 'purpose_'+ns;
  A[purposeKey] = 'School escort';
  html = rpSteps[rpIdx].render();
  window.__log.push(['schoolEscortTriggersExtraDetail', html.includes('Escort trip - extra detail')]);

  // fix 4: map zoom control present + zoomMap works
  window.openModal ? null : null;
  const locHtml = locPicker('testloc');
  window.__log.push(['mapHasZoomCtrl', locHtml.includes('map-zoom-ctrl')]);
  document.body.insertAdjacentHTML('beforeend', locHtml);
  const beforeZoom = A['testloc_zoom'] || 17;
  zoomMap('testloc', 1);
  window.__log.push(['zoomIncremented', A['testloc_zoom'] === beforeZoom+1]);
  window.__log.push(['mapSrcHasZ', mapSrc('testloc').includes('z='+(beforeZoom+1))]);

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
