path = '/sessions/adoring-amazing-cerf/mnt/outputs/survey_mockup.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

def rep(old, new, expect=1):
    global c
    n = c.count(old)
    status = "OK" if n==expect else f"MISMATCH (found {n}, expected {expect})"
    print(status, "::", old[:70].replace(chr(10),' '))
    if n>0:
        c = c.replace(old, new)

old_register = """{name:'Travel Diary - Register a Trip', tag:'Section 3 - Trip Roster &amp; Morning Schedule', render:()=>`
  <div class="field"><div class="q-label">Whose trip diary is this?</div>${personChipRow(tripPerson,'setTripPerson')}</div>
  ${tripPerson?`
  <div class="q-note">The questions below refer to [date], the day covered by this trip diary.</div>
  <div class="grid2">
    <div class="field"><div class="q-label">Sleep time (night before [date])</div><input type="time"></div>
    <div class="field"><div class="q-label">Wake time (on [date])</div><input type="time"></div>
  </div>
  <div class="field"><div class="q-label">Work / school start time (typical weekday)</div><input type="time" style="width:160px"></div>
  <div class="field"><div class="q-label">Who traveled with this person at any point today?</div>
    <div class="opt-row">${characters.filter(c=>c.id!==tripPerson).map(c=>{
      const nm = A[c.id+'_name']||(c.kind==='adult'?'Adult':'Child');
      const on = val('companion_'+c.id,false)?'checked':'';
      return `<label class="opt ${on}" onclick="toggleCompanion('${c.id}')">${nm}</label>`;
    }).join('') || '<span class="q-help">No other household members yet.</span>'}</div></div>
  <div class="field"><div class="q-label">List every place visited on [date], in order</div>
    <div class="q-help">Include short stops like drop-offs, pick-ups, or mode transfers.</div>
    <div class="stop-list">${stops.map((s,i)=>`<div class="stop-item"><span class="idx">${String.fromCharCode(65+i)}</span>
      <input type="text" value="${s.place}" oninput="stops[${i}].place=this.value" style="border:none;background:transparent;flex:1">
      ${stops.length>2?`<span class="remove" onclick="stops.splice(${i},1);renderRP()">Remove</span>`:''}</div>`).join('')}</div>
    <button class="add-btn" onclick="stops.splice(stops.length-1,0,{place:''});renderRP()">+ Add a stop</button></div>
  <div class="field"><div class="q-label">Maintenance time (typical weekday, minimum vs preferred)</div>
    <table class="likert-table"><tr><td></td><td class="likert-head">Minimum (min)</td><td class="likert-head">Preferred (min)</td></tr>
    ${['Sleeping','Getting ready/bathing','Breakfast','Escorting children','Other'].map(a=>`<tr><td class="lbl">${a}</td><td><input type="number" style="width:70px"></td><td><input type="number" style="width:70px"></td></tr>`).join('')}
    </table></div>
  `:'<div class="empty-hint">Pick a household member above to start their trip diary.</div>'}`},"""

new_register = """{name:'Travel Diary - Register a Trip', tag:'Section 3 - Trip Roster &amp; Morning Schedule', render:()=>`
  <div class="field"><div class="q-label">Whose trip diary is this?</div>${personChipRow(tripPerson,'setTripPerson')}</div>
  ${tripPerson?`
  <div class="q-note">The questions below refer to [date], the day covered by this trip diary. Who traveled together on each leg is asked later, per segment, in Trip Details.</div>
  <div class="grid2">
    <div class="field"><div class="q-label">Sleep time (night before [date])</div><input type="time"></div>
    <div class="field"><div class="q-label">Wake time (on [date])</div><input type="time"></div>
  </div>
  <div class="field"><div class="q-label">Work / school start time (typical weekday)</div><input type="time" style="width:160px"></div>
  <div class="field"><div class="q-label">List every place visited on [date], in order</div>
    <div class="q-help">Include short stops like drop-offs, pick-ups, or mode transfers. Drag the handle on the right to reorder a stop.</div>
    <div class="stop-list">${stops.map((s,i)=>`<div class="stop-item" draggable="true" ondragstart="dragStart(${i})" ondragover="event.preventDefault()" ondrop="dropStop(${i})"><span class="idx">${String.fromCharCode(65+i)}</span>
      <input type="text" value="${s.place}" oninput="stops[${i}].place=this.value;tripConfirmed=false" style="border:none;background:transparent;flex:1">
      ${stops.length>2?`<span class="remove" onclick="stops.splice(${i},1);tripConfirmed=false;renderRP()">Remove</span>`:''}
      <span class="drag-handle">Move</span></div>`).join('')}</div>
    <button class="add-btn" onclick="stops.splice(stops.length-1,0,{place:''});tripConfirmed=false;renderRP()">+ Add a stop</button>
    <div style="margin-top:12px"><button class="btn btn-primary" onclick="tripConfirmed=true;renderRP()">Save trip</button></div>
    ${tripConfirmed?`<div class="confirm-box"><b>${stops.length-1} segment(s) saved:</b><br>${stops.slice(0,-1).map((s,i)=>(s.place||'?')+' -&gt; '+(stops[i+1].place||'?')).join('<br>')}<br><span style="font-size:12px">Check this looks right, then press Next to fill in each segment's details.</span></div>`:''}
  </div>
  <div class="field"><div class="q-label">Maintenance time (typical weekday, minimum vs preferred)</div>
    <table class="likert-table"><tr><td></td><td class="likert-head">Minimum (min)</td><td class="likert-head">Preferred (min)</td></tr>
    <tr><td class="lbl">Sleeping</td><td colspan="2" style="font-size:12px;color:var(--sub);text-align:left">Calculated automatically from the sleep/wake time above</td></tr>
    ${['Getting ready/bathing','Breakfast','Escorting children','Other'].map(a=>`<tr><td class="lbl">${a}</td><td><input type="number" style="width:70px"></td><td><input type="number" style="width:70px"></td></tr>`).join('')}
    </table></div>
  `:'<div class="empty-hint">Pick a household member above to start their trip diary.</div>'}`},"""

rep(old_register, new_register)

with open(path,'w',encoding='utf-8') as f:
    f.write(c)
print("register-step patched")
