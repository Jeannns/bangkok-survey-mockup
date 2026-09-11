import os
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'survey_mockup.html')
with open(path, encoding='utf-8') as f:
    c = f.read()

def rep(old, new, expect=1):
    global c
    n = c.count(old)
    status = "OK" if n==expect else f"MISMATCH (found {n}, expected {expect})"
    print(status, "::", old[:70].replace(chr(10),' '))
    if n>0:
        c = c.replace(old, new)

# Each trip-diary stop now carries an optional location: Home, a household
# member's registered workplace/school (one-click), or a manually entered
# place via the existing locPicker component. An "Edit" button next to each
# stop's Remove/Move controls opens the picker.

# 1) CSS for the new Edit button
rep(
'.drag-handle{margin-left:8px;color:var(--sub);font-size:11px;cursor:grab;border:1px solid var(--line);border-radius:6px;padding:2px 6px;background:#fff;user-select:none}',
'.drag-handle{margin-left:8px;color:var(--sub);font-size:11px;cursor:grab;border:1px solid var(--line);border-radius:6px;padding:2px 6px;background:#fff;user-select:none}\n'
'.edit-stop{margin-left:8px;color:var(--blue-dark);font-size:11px;cursor:pointer;border:1px solid var(--line);border-radius:6px;padding:2px 8px;background:#fff;font-weight:700;user-select:none}'
)

# 2) give every stop a stable id (needed to key its location fields)
rep(
"""/* travel diary state */
let stops = [{place:'Home'},{place:'School'},{place:'Home'}];
let maintActivities = [{name:''}];""",
"""/* travel diary state */
let stopSeq = 0;
function newStop(place){ return {id:'stop'+(++stopSeq), place, loc:null}; }
let stops = [newStop('Home'), newStop('School'), newStop('Home')];
let maintActivities = [{name:''}];"""
)
rep(
"  stops = tripsByPerson[id] ? tripsByPerson[id].map(s=>({...s})) : [{place:'Home'},{place:'School'},{place:'Home'}];",
"  stops = tripsByPerson[id] ? tripsByPerson[id].map(s=>({...s})) : [newStop('Home'), newStop('School'), newStop('Home')];"
)
rep(
"""function resetTripState(){
  tripPerson = null; stops = [{place:'Home'},{place:'School'},{place:'Home'}];
  tripConfirmed = false; segIdx = 0; showTripDonePrompt = false;
}""",
"""function resetTripState(){
  tripPerson = null; stops = [newStop('Home'), newStop('School'), newStop('Home')];
  tripConfirmed = false; segIdx = 0; showTripDonePrompt = false;
}"""
)

# 3) the location-picker modal itself, plus the label helper - inserted right
#    after resetTripState()
rep(
"""function resetTripState(){
  tripPerson = null; stops = [newStop('Home'), newStop('School'), newStop('Home')];
  tripConfirmed = false; segIdx = 0; showTripDonePrompt = false;
}

let lastSavedAt = null;""",
"""function resetTripState(){
  tripPerson = null; stops = [newStop('Home'), newStop('School'), newStop('Home')];
  tripConfirmed = false; segIdx = 0; showTripDonePrompt = false;
}
function stopLocLabel(s){
  if(!s.loc) return '';
  if(s.loc.type==='home') return t('Home (registered)');
  if(s.loc.type==='registered'){
    const c = characters.find(c=>c.id===s.loc.personId);
    const nm = c ? (A[c.id+'_name']||(c.kind==='adult'?t('Adult'):t('Child'))) : '';
    return nm + (s.loc.kind==='work' ? t(' - workplace (registered)') : t(' - school (registered)'));
  }
  if(s.loc.type==='custom') return A[s.id+'_name'] || A[s.id+'_addr'] || t('Custom location set');
  return '';
}
window.openStopLocationPicker = (stopId)=>{
  const s = stops.find(x=>x.id===stopId);
  if(!s) return;
  document.getElementById('modal-title').textContent = t('Set location for')+' "'+(s.place||'?')+'"';
  const adults = characters.filter(c=>c.kind==='adult');
  const kids = characters.filter(c=>c.kind==='child');
  const rows = [];
  rows.push(`<div class="stop-item" style="cursor:pointer" onclick="pickStopLoc('${stopId}','home')"><span style="flex:1">${t('Home')}</span><span class="drag-handle">${t('Use this')}</span></div>`);
  adults.forEach(c=>{
    const nm = A[c.id+'_name']||t('Adult');
    rows.push(`<div class="stop-item" style="cursor:pointer" onclick="pickStopLoc('${stopId}','work','${c.id}')"><span style="flex:1">${nm} ${t("- workplace")}</span><span class="drag-handle">${t('Use this')}</span></div>`);
  });
  kids.forEach(c=>{
    const nm = A[c.id+'_name']||t('Child');
    rows.push(`<div class="stop-item" style="cursor:pointer" onclick="pickStopLoc('${stopId}','school','${c.id}')"><span style="flex:1">${nm} ${t("- school")}</span><span class="drag-handle">${t('Use this')}</span></div>`);
  });
  document.getElementById('modal-body').innerHTML = `
    <div class="q-note">${t('Choose a registered place, or enter a new one below.')}</div>
    <div class="stop-list">${rows.join('')}</div>
    <div class="nav-row"><span></span><button class="btn btn-ghost" style="border:1px solid var(--line)" onclick="stopLocCustom('${stopId}')">${t('Not in this list - enter manually')}</button></div>
  `;
  document.getElementById('modal-overlay').classList.add('open');
};
window.pickStopLoc = (stopId,type,personId)=>{
  const s = stops.find(x=>x.id===stopId);
  if(!s) return;
  s.loc = personId ? {type:'registered',kind:type,personId} : {type:'home'};
  document.getElementById('modal-overlay').classList.remove('open');
  renderRP();
};
window.stopLocCustom = (stopId)=>{
  document.getElementById('modal-title').textContent = t('Enter location');
  document.getElementById('modal-body').innerHTML = `
    ${locPicker(stopId)}
    <div class="nav-row"><span></span><button class="btn btn-primary" onclick="confirmStopLocCustom('${stopId}')">${t('Save & close')}</button></div>
  `;
};
window.confirmStopLocCustom = (stopId)=>{
  const s = stops.find(x=>x.id===stopId);
  if(s) s.loc = {type:'custom'};
  document.getElementById('modal-overlay').classList.remove('open');
  renderRP();
};

let lastSavedAt = null;"""
)

# 4) stop-list render: show each stop's location status + Edit button; the
#    "+ Add a stop" button now creates stops via newStop() too
rep(
"""    <div class="stop-list">${stops.map((s,i)=>`<div class="stop-item" draggable="true" ondragstart="dragStart(${i})" ondragover="event.preventDefault()" ondrop="dropStop(${i})"><span class="idx">${String.fromCharCode(65+i)}</span>
      <input type="text" value="${s.place}" oninput="stops[${i}].place=this.value;tripConfirmed=false" style="border:none;background:transparent;flex:1">
      ${stops.length>2?`<span class="remove" onclick="stops.splice(${i},1);tripConfirmed=false;renderRP()">${t('Remove')}</span>`:''}
      <span class="drag-handle">${t('Move')}</span></div>`).join('')}</div>
    <button class="add-btn" onclick="stops.splice(stops.length-1,0,{place:''});tripConfirmed=false;renderRP()">${t('+ Add a stop')}</button>""",
"""    <div class="stop-list">${stops.map((s,i)=>`<div class="stop-item" draggable="true" ondragstart="dragStart(${i})" ondragover="event.preventDefault()" ondrop="dropStop(${i})"><span class="idx">${String.fromCharCode(65+i)}</span>
      <div style="flex:1;min-width:0">
        <input type="text" value="${s.place}" oninput="stops[${i}].place=this.value;tripConfirmed=false" style="border:none;background:transparent;width:100%">
        <div style="font-size:11px;color:${s.loc?'var(--blue-dark)':'var(--sub)'}">${s.loc?('&#128205; '+stopLocLabel(s)):t('No location set yet')}</div>
      </div>
      <span class="edit-stop" onclick="openStopLocationPicker('${s.id}')">${t('Edit')}</span>
      ${stops.length>2?`<span class="remove" onclick="stops.splice(${i},1);tripConfirmed=false;renderRP()">${t('Remove')}</span>`:''}
      <span class="drag-handle">${t('Move')}</span></div>`).join('')}</div>
    <button class="add-btn" onclick="stops.splice(stops.length-1,0,newStop(''));tripConfirmed=false;renderRP()">${t('+ Add a stop')}</button>"""
)

with open(path,'w',encoding='utf-8') as f:
    f.write(c)
print("part6 done")
