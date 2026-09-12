"""
Patch script (audit trail, not an active build pipeline): adds the RP-mockup
equivalent of this round's 3 Okinawa PT-survey-derived docx additions (see
build_rp_okinawa.py / project memory for the docx side):

  1. 5 new items on the "why this mode?" escort-reason checklist (Escorting -
     Travel Mode step): physical condition/disability, destination far,
     punctuality, heavy/bulky items, extra free time.
  2. A new household-vs-non-household escort question (Escorting - Habit
     step), right after the "which children are escorted" field.
  3. A "did you make any trips at all today?" gate + reason-for-not-going-out
     fallback question on the Travel Diary - Register a Trip step, plus the
     supporting state-management changes (setTripPerson/saveNoTrip/
     openTripEditPicker/jumpToSegment/Trip Details) needed so a no-trip day
     can be saved and edited without breaking the existing per-segment flow.

Run against a checkout of the commit *before* this change to reproduce it:
    git show <prev_commit>:survey_mockup.html > /tmp/survey_mockup_prev.html
    python3 build_survey_mockup_8_okinawa_additions.py /tmp/survey_mockup_prev.html /tmp/out.html
    diff /tmp/out.html survey_mockup.html   # should be empty
"""
import sys


def rep(text, old, new, expect=1):
    count = text.count(old)
    if count != expect:
        raise SystemExit(f"Expected {expect} occurrence(s) of {old!r}, found {count}")
    return text.replace(old, new)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "survey_mockup.html"
    dst = sys.argv[2] if len(sys.argv) > 2 else src
    html = open(src, encoding="utf-8").read()

    # --- 1. mode_reason: append 5 new escort-reason items ---
    html = rep(
        html,
        "'Combined with own commute/errand (trip-chaining)','Ride-hailing as backup when I cannot escort in person'],true)}</div>",
        "'Combined with own commute/errand (trip-chaining)','Ride-hailing as backup when I cannot escort in person',"
        "'Physical condition/disability makes independent travel difficult','Destination is far from home','To make sure we arrive on time','Carrying heavy or bulky items','I happen to have extra free time'],true)}</div>",
    )

    # --- 2. Habit step: household vs. non-household escort question ---
    html = rep(
        html,
        """    }).join('')||`<span class="q-help">${t('No child characters created yet.')}</span>`}</div></div>
  <div class="field"><div class="q-label">${t('Which adults usually do the escorting?')}</div>""",
        """    }).join('')||`<span class="q-help">${t('No child characters created yet.')}</span>`}</div></div>
  <div class="field"><div class="q-label">${t("Do you also regularly escort any child(ren) who are NOT members of your household (e.g. a neighbor's child, or as part of a carpool)?")}</div>${opts('escorts_nonhousehold',['Yes','No'])}
    ${val('escorts_nonhousehold')==='Yes'?`<input type="text" placeholder="${t('Briefly note the relationship and school for each')}" style="margin-top:8px;width:100%" value="${val('nonhousehold_detail','')}" oninput="A['nonhousehold_detail']=this.value">`:''}</div>
  <div class="field"><div class="q-label">${t('Which adults usually do the escorting?')}</div>""",
    )

    # --- 3a. state: setTripPerson must tolerate the 'NO_TRIP' sentinel ---
    html = rep(
        html,
        "window.setTripPerson = (id)=>{\n  tripPerson = id;\n  stops = tripsByPerson[id] ? tripsByPerson[id].map(s=>({...s})) : [newStop('Home'), newStop('School'), newStop('Home')];\n  tripConfirmed = !!tripsByPerson[id];\n  segIdx = 0; showTripDonePrompt = false;\n  renderRP();\n};\nwindow.saveTrip = ()=>{ tripConfirmed = true; tripsByPerson[tripPerson] = stops.map(s=>({...s})); renderRP(); };",
        "window.setTripPerson = (id)=>{\n  tripPerson = id;\n  const saved = tripsByPerson[id];\n  stops = (saved && saved!=='NO_TRIP') ? saved.map(s=>({...s})) : [newStop('Home'), newStop('School'), newStop('Home')];\n  tripConfirmed = !!saved;\n  segIdx = 0; showTripDonePrompt = false;\n  renderRP();\n};\nwindow.saveTrip = ()=>{ tripConfirmed = true; tripsByPerson[tripPerson] = stops.map(s=>({...s})); renderRP(); };\nwindow.saveNoTrip = ()=>{ tripConfirmed = true; tripsByPerson[tripPerson] = 'NO_TRIP'; renderRP(); };",
    )

    # --- 3b. state: openTripEditPicker must handle a 'NO_TRIP' entry ---
    html = rep(
        html,
        """window.openTripEditPicker = (id)=>{
  const c = characters.find(c=>c.id===id);
  const nm = c ? (A[id+'_name']||(c.kind==='adult'?t('Adult'):t('Child'))) : id;
  document.getElementById('modal-title').textContent = t('Edit trip for')+' '+nm;
  const segs = tripsByPerson[id] || [];
  const rows = segs.slice(0,-1).map((s,i)=>`<div class="stop-item"><span style="flex:1">${t('Segment')} ${i+1}: ${s.place||'?'} -&gt; ${(segs[i+1]||{}).place||'?'}</span><button class="btn btn-ghost" style="border:1px solid var(--line);padding:6px 14px" onclick="jumpToSegment('${id}',${i})">${t('Edit')}</button></div>`).join('');
  document.getElementById('modal-body').innerHTML = `
    <div class="stop-list">${rows || `<div class="empty-hint">${t('No segments yet.')}</div>`}</div>
    <div class="nav-row"><span></span><button class="btn btn-ghost" style="border:1px solid var(--line)" onclick="jumpToStopList('${id}')">${t('Edit the list of places instead')}</button></div>
  `;
  document.getElementById('modal-overlay').classList.add('open');
};""",
        """window.openTripEditPicker = (id)=>{
  const c = characters.find(c=>c.id===id);
  const nm = c ? (A[id+'_name']||(c.kind==='adult'?t('Adult'):t('Child'))) : id;
  document.getElementById('modal-title').textContent = t('Edit trip for')+' '+nm;
  const saved = tripsByPerson[id];
  if(saved==='NO_TRIP'){
    document.getElementById('modal-body').innerHTML = `
      <div class="q-note">${t('This person was recorded as making no trips at all that day.')}</div>
      <div class="nav-row"><span></span><button class="btn btn-ghost" style="border:1px solid var(--line)" onclick="jumpToStopList('${id}')">${t('Register a trip for them instead')}</button></div>
    `;
    document.getElementById('modal-overlay').classList.add('open');
    return;
  }
  const segs = saved || [];
  const rows = segs.slice(0,-1).map((s,i)=>`<div class="stop-item"><span style="flex:1">${t('Segment')} ${i+1}: ${s.place||'?'} -&gt; ${(segs[i+1]||{}).place||'?'}</span><button class="btn btn-ghost" style="border:1px solid var(--line);padding:6px 14px" onclick="jumpToSegment('${id}',${i})">${t('Edit')}</button></div>`).join('');
  document.getElementById('modal-body').innerHTML = `
    <div class="stop-list">${rows || `<div class="empty-hint">${t('No segments yet.')}</div>`}</div>
    <div class="nav-row"><span></span><button class="btn btn-ghost" style="border:1px solid var(--line)" onclick="jumpToStopList('${id}')">${t('Edit the list of places instead')}</button></div>
  `;
  document.getElementById('modal-overlay').classList.add('open');
};""",
    )

    # --- 3c. "Trips already registered" list: show a (no trip) label instead of implying segments ---
    html = rep(
        html,
        """      const nm = c ? (A[id+'_name']||(c.kind==='adult'?t('Adult'):t('Child'))) : id;
      return `<div class="stop-item"><span style="flex:1">${nm}</span><button class="btn btn-ghost" style="border:1px solid var(--line);padding:6px 14px" onclick="openTripEditPicker('${id}')">${t('Edit')}</button></div>`;""",
        """      const nm = c ? (A[id+'_name']||(c.kind==='adult'?t('Adult'):t('Child'))) : id;
      const noTrip = tripsByPerson[id]==='NO_TRIP';
      return `<div class="stop-item"><span style="flex:1">${nm}${noTrip?` <span class="q-help" style="font-size:11px">(${t('no trip that day')})</span>`:''}</span><button class="btn btn-ghost" style="border:1px solid var(--line);padding:6px 14px" onclick="openTripEditPicker('${id}')">${t('Edit')}</button></div>`;""",
    )

    # --- 3d. Register a Trip step: add the made-a-trip gate + no-trip reason question ---
    html = rep(
        html,
        """  ${tripPerson?`
  <div class="q-note">${dl('The questions below refer to [date], the day covered by this trip diary. Who traveled together on each leg is asked later, per segment, in Trip Details.')}</div>
  <div class="grid2">
    <div class="field"><div class="q-label">${dl('Sleep time (night before [date])')}</div><input type="time"></div>
    <div class="field"><div class="q-label">${dl('Wake time (on [date])')}</div><input type="time"></div>
  </div>
  <div class="field"><div class="q-label">${dl('List every place visited on [date], in order')}</div>""",
        """  ${tripPerson?`
  <div class="q-note">${dl('The questions below refer to [date], the day covered by this trip diary. Who traveled together on each leg is asked later, per segment, in Trip Details.')}</div>
  <div class="field"><div class="q-label">${dl('Did this person leave home at all on [date]?')}</div>${opts('madetrip_'+tripPerson,['Yes, at least one trip','No trips at all'])}</div>
  ${val('madetrip_'+tripPerson)==='No trips at all'?`
  <div class="field"><div class="q-label">${dl('What was the main reason this person did not leave home at all on [date]?')}</div>
    ${opts('no_trip_reason_'+tripPerson,['Working/studying from home or online class','Workplace/school was closed','Had no reason to go out','Other'])}</div>
  <div style="margin-top:12px"><button class="btn btn-primary" onclick="saveNoTrip()">${t('Save (no trip this day)')}</button></div>
  ${tripConfirmed && tripsByPerson[tripPerson]==='NO_TRIP'?`<div class="confirm-box">${t('Recorded: no trips for this person on')} ${diaryDate}.</div>`:''}
  `:`
  <div class="grid2">
    <div class="field"><div class="q-label">${dl('Sleep time (night before [date])')}</div><input type="time"></div>
    <div class="field"><div class="q-label">${dl('Wake time (on [date])')}</div><input type="time"></div>
  </div>
  <div class="field"><div class="q-label">${dl('List every place visited on [date], in order')}</div>""",
    )

    # close the new outer branch we opened above (wrap the pre-existing stop-list block, which
    # ends right before the closing "`:`<div class=\"empty-hint\">...` fallback)
    html = rep(
        html,
        """    ${tripConfirmed?`<div class="confirm-box"><b>${stops.length-1} ${t('segment(s) saved:')}</b><br>${stops.slice(0,-1).map((s,i)=>(s.place||'?')+' -&gt; '+(stops[i+1].place||'?')).join('<br>')}<br><span style="font-size:12px">${t("Check this looks right, then press Next to fill in each segment's details.")}</span></div>`:''}
  </div>
  `:`<div class="empty-hint">${t('Pick a household member above to start their trip diary.')}</div>`}`},""",
        """    ${tripConfirmed && tripsByPerson[tripPerson]!=='NO_TRIP'?`<div class="confirm-box"><b>${stops.length-1} ${t('segment(s) saved:')}</b><br>${stops.slice(0,-1).map((s,i)=>(s.place||'?')+' -&gt; '+(stops[i+1].place||'?')).join('<br>')}<br><span style="font-size:12px">${t("Check this looks right, then press Next to fill in each segment's details.")}</span></div>`:''}
  </div>
  `}
  `:`<div class="empty-hint">${t('Pick a household member above to start their trip diary.')}</div>`}`},""",
    )

    # --- 3e. Trip Details step: a NO_TRIP person has 0 segments; make that explicit rather
    # than silently falling through the generic "totalSegs===0" branch ---
    html = rep(
        html,
        """{name:'Travel Diary - Trip Details', tag:'Section 3 - Trip Details (per segment)', customNav:true, render:()=>{
  if(!tripPerson) return `<div class="empty-hint">${t('Go back and register a trip first.')}</div>
    <div class="nav-row"><button class="btn btn-ghost" onclick="rpIdx--;renderRP()">${t('<- Back')}</button>${tempSaveBtn()}${devMode?`<button class="btn btn-primary" onclick="rpIdx++;renderRP()">${t('Next ->')}</button>`:'<span></span>'}</div>`;

  const totalSegs = Math.max(0, stops.length-1);""",
        """{name:'Travel Diary - Trip Details', tag:'Section 3 - Trip Details (per segment)', customNav:true, render:()=>{
  if(!tripPerson) return `<div class="empty-hint">${t('Go back and register a trip first.')}</div>
    <div class="nav-row"><button class="btn btn-ghost" onclick="rpIdx--;renderRP()">${t('<- Back')}</button>${tempSaveBtn()}${devMode?`<button class="btn btn-primary" onclick="rpIdx++;renderRP()">${t('Next ->')}</button>`:'<span></span>'}</div>`;

  if(tripsByPerson[tripPerson]==='NO_TRIP' && !showTripDonePrompt){
    return `<div class="empty-hint">${t('This person made no trips that day - nothing to detail. Continue to see if anyone else needs a trip registered.')}</div>
      <div class="nav-row"><button class="btn btn-ghost" onclick="rpIdx--;renderRP()">${t('<- Back')}</button>${tempSaveBtn()}<button class="btn btn-primary" onclick="showTripDonePrompt=true;renderRP()">${t('Next ->')}</button></div>`;
  }

  const totalSegs = Math.max(0, stops.length-1);""",
    )

    open(dst, "w", encoding="utf-8").write(html)
    print(f"Wrote {dst} ({len(html)} chars)")


if __name__ == "__main__":
    main()
