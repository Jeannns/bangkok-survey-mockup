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

old_details = """{name:'Travel Diary - Trip Details', tag:'Section 3 - Trip Details (per segment)', render:()=>{
  if(!tripPerson) return `<div class="empty-hint">Go back and register a trip first.</div>`;
  let segs='';
  for(let i=0;i<stops.length-1;i++){
    const purposeKey='purpose_'+i;
    const isEscort = (val(purposeKey)||'').indexOf('Escorting')>=0 || (val(purposeKey)||'').indexOf('drop-off')>=0 || (val(purposeKey)||'').indexOf('pick-up')>=0;
    segs += `<div class="segment-card"><div class="segment-title">Segment ${i+1}: ${stops[i].place||'?'} -&gt; ${stops[i+1].place||'?'}</div>
    <div class="grid2">
      <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Departure time</div><input type="time"></div>
      <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Arrival time</div><input type="time"></div>
    </div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Travel mode (main mode for this segment)</div>
      ${opts('mode_'+i,['Walk','Bike','School bus','Private car','Private motorbike','Ride-hailing - car','Ride-hailing - motorbike','Regular taxi','MRT','BTS Skytrain','Bus'])}</div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Did you use more than one way of getting there? If yes, list them in order</div>
      ${opts('multimode_'+i,['No, one mode only','Yes'])}<input type="text" placeholder="e.g. walk, then bus, then train" style="margin-top:8px"></div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">If BTS or MRT: boarding station / alighting station</div>
      <div class="grid2"><input type="text" placeholder="Boarding station"><input type="text" placeholder="Alighting station"></div></div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">If by car: were you the driver or a passenger?</div>
      ${opts('driverpax_'+i,['Driver','Passenger'])}</div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Main purpose of this trip</div>
      ${opts(purposeKey,['Commuting to work','Going to school (drop-off)','Going to school (for children)','Return home','Return to workplace','Return to school (pick-up)','Escorting (other)','Shopping','Leisure','Medical-related','Other private purpose','Business/work-related'])}</div>
    ${isEscort?`
    <div class="escort-box"><span class="tag">Escort trip - extra detail</span>
      <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Taking the child TO school, or bringing them FROM school?</div>
        ${opts('escdir_'+i,['To school','From school'])}</div>
      <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Drop-off / pick-up point</div>${locPicker('dropoff_'+i)}</div>
      <div class="field" style="border:none;padding:0"><div class="q-label" style="font-size:13px">After arriving, how long do you usually wait?</div><input type="number" placeholder="minutes" style="width:140px"></div>
    </div>`:''}
    <div class="field" style="border:none;padding:0;margin-top:10px"><div class="q-label" style="font-size:13px">Fare/cost (THB, 0 if free)</div><input type="number" style="width:120px"></div>
    </div>`;
  }
  return `<div class="q-help">Auto-generated from your trip roster above - one card per segment between consecutive stops. If a segment's purpose is escorting, extra questions appear automatically.</div>${segs}`;
}},"""

new_details = """{name:'Travel Diary - Trip Details', tag:'Section 3 - Trip Details (per segment)', customNav:true, render:()=>{
  if(!tripPerson) return `<div class="empty-hint">Go back and register a trip first.</div>
    <div class="nav-row"><button class="btn btn-ghost" onclick="rpIdx--;renderRP()">&lt;- Back</button>${tempSaveBtn()}<span></span></div>`;

  const totalSegs = Math.max(0, stops.length-1);

  if(showTripDonePrompt || totalSegs===0){
    return `<div class="prompt-box"><h4>Does anyone else in the household have a trip on [date] too?</h4>
      <div class="nav-row" style="justify-content:center;gap:14px">
        <button class="btn btn-primary" onclick="resetTripState();rpIdx=rpSteps.findIndex(s=>s.name==='Travel Diary - Register a Trip');renderRP()">Yes, register their trip</button>
        <button class="btn btn-ghost" style="border:1px solid var(--line)" onclick="showTripDonePrompt=false;rpIdx++;renderRP()">No, continue</button>
      </div></div>`;
  }

  const i = segIdx;
  const purposeKey='purpose_'+i;
  const isEscort = (val(purposeKey)||'').indexOf('Escorting')>=0 || (val(purposeKey)||'').indexOf('drop-off')>=0 || (val(purposeKey)||'').indexOf('pick-up')>=0;
  const seg = `<div class="q-help">Segment ${i+1} of ${totalSegs}</div>
    <div class="segment-card"><div class="segment-title">${stops[i].place||'?'} -&gt; ${stops[i+1].place||'?'}</div>
    <div class="grid2">
      <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Departure time</div><input type="time"></div>
      <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Arrival time</div><input type="time"></div>
    </div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Who traveled with you on this segment?</div>
      <div class="opt-row">${characters.filter(c=>c.id!==tripPerson).map(c=>{
        const nm = A[c.id+'_name']||(c.kind==='adult'?'Adult':'Child');
        const key = 'seg'+i+'_companion_'+c.id;
        const on = val(key,false)?'checked':'';
        return `<label class="opt ${on}" onclick="A['${key}']=!A['${key}'];this.classList.toggle('checked')">${nm}</label>`;
      }).join('') || '<span class="q-help">No other household members yet.</span>'}</div></div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Travel mode (main mode for this segment)</div>
      ${opts('mode_'+i,['Walk','Bike','School bus','Private car','Private motorbike','Ride-hailing - car','Ride-hailing - motorbike','Regular taxi','MRT','BTS Skytrain','Bus'])}</div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Did you use more than one way of getting there? If yes, list them in order</div>
      ${opts('multimode_'+i,['No, one mode only','Yes'])}<input type="text" placeholder="e.g. walk, then bus, then train" style="margin-top:8px"></div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">If BTS or MRT: boarding station / alighting station</div>
      <div class="grid2"><input type="text" placeholder="Boarding station"><input type="text" placeholder="Alighting station"></div></div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">If by car: were you the driver or a passenger?</div>
      ${opts('driverpax_'+i,['Driver','Passenger'])}</div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Main purpose of this trip</div>
      ${opts(purposeKey,['Commuting to work','Going to school (drop-off)','Going to school (for children)','Return home','Return to workplace','Return to school (pick-up)','Escorting (other)','Shopping','Leisure','Medical-related','Other private purpose','Business/work-related'])}</div>
    ${isEscort?`
    <div class="escort-box"><span class="tag">Escort trip - extra detail</span>
      <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Taking the child TO school, or bringing them FROM school?</div>
        ${opts('escdir_'+i,['To school','From school'])}</div>
      <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">Drop-off / pick-up point</div>${locPicker('dropoff_'+i)}</div>
      <div class="field" style="border:none;padding:0"><div class="q-label" style="font-size:13px">After arriving, how long do you usually wait?</div><input type="number" placeholder="minutes" style="width:140px"></div>
    </div>`:''}
    <div class="field" style="border:none;padding:0;margin-top:10px"><div class="q-label" style="font-size:13px">Fare/cost (THB, 0 if free)</div><input type="number" style="width:120px"></div>
    </div>`;

  const backAction = i>0 ? `segIdx=${i-1};renderRP()` : `rpIdx--;renderRP()`;
  const nextAction = i<totalSegs-1 ? `segIdx=${i+1};renderRP()` : `showTripDonePrompt=true;renderRP()`;
  const nextLabel = i<totalSegs-1 ? 'Next segment ->' : 'Finish trip ->';
  return `${seg}<div class="nav-row">
    <button class="btn btn-ghost" onclick="${backAction}">&lt;- Back</button>
    ${tempSaveBtn()}
    <button class="btn btn-primary" onclick="${nextAction}">${nextLabel}</button>
  </div>`;
}},"""

rep(old_details, new_details)

# renderRP(): support customNav steps (skip default nav-row) and add tempSaveBtn to the default nav-row
old_renderrp = """  document.getElementById('rp-card').innerHTML = `
    ${step.tag?`<div class="section-tag">${step.tag}</div>`:''}
    <div class="step-title">${step.name}</div>
    <div class="step-sub">&nbsp;</div>
    ${step.render()}
    <div class="nav-row">
      <button class="btn btn-ghost" onclick="rpIdx=Math.max(0,rpIdx-1);renderRP()" ${rpIdx===0?'style=visibility:hidden':''}>&lt;- Back</button>
      <button class="btn btn-primary" onclick="rpIdx=Math.min(${rpSteps.length-1},rpIdx+1);renderRP()">${rpIdx===rpSteps.length-1?'Done':'Next ->'}</button>
    </div>`;
}"""
new_renderrp = """  document.getElementById('rp-card').innerHTML = `
    ${step.tag?`<div class="section-tag">${step.tag}</div>`:''}
    <div class="step-title">${step.name}</div>
    <div class="step-sub">&nbsp;</div>
    ${step.render()}
    ${step.customNav?'':`<div class="nav-row">
      <button class="btn btn-ghost" onclick="rpIdx=Math.max(0,rpIdx-1);renderRP()" ${rpIdx===0?'style=visibility:hidden':''}>&lt;- Back</button>
      ${tempSaveBtn()}
      <button class="btn btn-primary" onclick="rpIdx=Math.min(${rpSteps.length-1},rpIdx+1);renderRP()">${rpIdx===rpSteps.length-1?'Done':'Next ->'}</button>
    </div>`}`;
}"""
rep(old_renderrp, new_renderrp)

with open(path,'w',encoding='utf-8') as f:
    f.write(c)
print("details-step + renderRP patched")
