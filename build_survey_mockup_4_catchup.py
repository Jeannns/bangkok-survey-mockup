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

# ============================================================================
# SECTION A - Ride-hailing questions + "Taxi meter" rename (RP + SP)
# ============================================================================
# Add ride-hailing usage/trust questions + "Taxi meter" rename to RP, and a
# pooled ride-hailing option to SP Module 1. Example services shown to
# respondents: Grab, Line Man, inDrive, Bolt.

# A1) T dict - escort-mode/reasons/weather block: rename Taxi -> Taxi meter,
#     add ride-hailing-as-backup reason + frequency/trust question translations
rep(
'"Ride-hailing":"เรียกรถผ่านแอป","Taxi":"แท็กซี่","BTS":"BTS",\n'
'"Why this mode? (top 3)":"เหตุใดจึงเลือกวิธีนี้ (เลือก 3 อันดับ)",\n'
'"Same mode as my work commute":"รูปแบบเดียวกับที่ใช้ไปทำงาน","Escort multiple children at once":"รับส่งบุตรหลายคนพร้อมกัน","Most convenient":"สะดวกที่สุด",\n'
'"Quality time with children":"ได้ใช้เวลาคุณภาพกับบุตรหลาน","Only mode available":"เป็นวิธีเดียวที่มี","Flexible work schedule":"เวลาทำงานยืดหยุ่น",\n'
'"Proximity to station (home)":"ใกล้สถานี (ฝั่งบ้าน)","Proximity to station (school)":"ใกล้สถานี (ฝั่งโรงเรียน)","Comfortable sidewalk access":"ทางเท้าเข้าถึงสะดวก",\n'
'"Timely PT schedule":"ตารางเวลาขนส่งสาธารณะตรงเวลา","PT is clean":"ขนส่งสาธารณะสะอาด","More affordable fare":"ค่าโดยสารประหยัดกว่า",\n'
'"Combined with own commute/errand (trip-chaining)":"รวมกับการเดินทางไปทำงาน/ธุระของตัวเอง (เดินทางต่อเนื่อง)",\n'
'"How often does weather (heavy rain/extreme heat) change your usual school-commute mode?":"สภาพอากาศ (ฝนตกหนัก/อากาศร้อนจัด) ทำให้ท่านเปลี่ยนวิธีเดินทางไปโรงเรียนตามปกติบ่อยเพียงใด",\n'
'"Never":"ไม่เคย","Rarely":"นานๆ ครั้ง","Sometimes":"บางครั้ง","Often":"บ่อยครั้ง","Always":"ทุกครั้ง",',

'"Ride-hailing":"เรียกรถผ่านแอป","Taxi":"แท็กซี่","Taxi meter":"แท็กซี่มิเตอร์","BTS":"BTS",\n'
'"Why this mode? (top 3)":"เหตุใดจึงเลือกวิธีนี้ (เลือก 3 อันดับ)",\n'
'"Same mode as my work commute":"รูปแบบเดียวกับที่ใช้ไปทำงาน","Escort multiple children at once":"รับส่งบุตรหลายคนพร้อมกัน","Most convenient":"สะดวกที่สุด",\n'
'"Quality time with children":"ได้ใช้เวลาคุณภาพกับบุตรหลาน","Only mode available":"เป็นวิธีเดียวที่มี","Flexible work schedule":"เวลาทำงานยืดหยุ่น",\n'
'"Proximity to station (home)":"ใกล้สถานี (ฝั่งบ้าน)","Proximity to station (school)":"ใกล้สถานี (ฝั่งโรงเรียน)","Comfortable sidewalk access":"ทางเท้าเข้าถึงสะดวก",\n'
'"Timely PT schedule":"ตารางเวลาขนส่งสาธารณะตรงเวลา","PT is clean":"ขนส่งสาธารณะสะอาด","More affordable fare":"ค่าโดยสารประหยัดกว่า",\n'
'"Combined with own commute/errand (trip-chaining)":"รวมกับการเดินทางไปทำงาน/ธุระของตัวเอง (เดินทางต่อเนื่อง)",\n'
'"Ride-hailing as backup when I cannot escort in person":"ใช้แอปเรียกรถเป็นทางเลือกสำรองเมื่อไปรับส่งเองไม่ได้",\n'
'"How often does weather (heavy rain/extreme heat) change your usual school-commute mode?":"สภาพอากาศ (ฝนตกหนัก/อากาศร้อนจัด) ทำให้ท่านเปลี่ยนวิธีเดินทางไปโรงเรียนตามปกติบ่อยเพียงใด",\n'
'"How often does your household use a ride-hailing app (e.g. Grab, Line Man, inDrive, Bolt) to send/pick up your child for school?":"ครอบครัวท่านใช้แอปเรียกรถ (เช่น Grab, Line Man, inDrive, Bolt) รับส่งบุตรหลานไปโรงเรียนบ่อยเพียงใด",\n'
'"If child travels by a ride-hailing app (Grab/Line Man/inDrive/Bolt), how much do you trust the driver?":"หากบุตรหลานเดินทางโดยแอปเรียกรถ (Grab/Line Man/inDrive/Bolt) ท่านไว้วางใจคนขับมากเพียงใด",\n'
'"Never":"ไม่เคย","Rarely":"นานๆ ครั้ง","Sometimes":"บางครั้ง","Often":"บ่อยครั้ง","Always":"ทุกครั้ง",'
)

# A2) T dict - SP labels block: add "Medium" + third-party ride-hailing card title
rep(
'"School buddy":"เพื่อนไปโรงเรียนด้วยกัน","Guardian":"ผู้ปกครอง/ผู้ดูแล","Poor":"แย่","Good":"ดี","Moderate":"ปานกลาง","High":"สูง","Low":"ต่ำ",',
'"School buddy":"เพื่อนไปโรงเรียนด้วยกัน","Guardian":"ผู้ปกครอง/ผู้ดูแล","Poor":"แย่","Good":"ดี","Moderate":"ปานกลาง","High":"สูง","Low":"ต่ำ","Medium":"ปานกลาง",\n'
'"Third-party escort (ride-hailing)":"บุคคลที่สามรับส่ง (เรียกรถผ่านแอป)",'
)

# A3) RP "Escorting - Travel Mode" step: rename Taxi->Taxi meter in mode list,
#     add ride-hailing reason, and the two new frequency/trust questions
rep(
"""{name:'Escorting - Travel Mode', tag:'Section 4 - Travel Mode', render:()=>`
  <div class="field"><div class="q-label">${t('How do you typically escort your children? (main mode)')}</div>
    ${opts('escort_mode',['Walk','Bike','School bus','Private car','Private motorbike','Ride-hailing','Taxi','MRT','BTS','Bus'])}</div>
  <div class="field"><div class="q-label">${t('Why this mode? (top 3)')}</div>
    ${opts('mode_reason',['Same mode as my work commute','Escort multiple children at once','Most convenient','Quality time with children','Only mode available','Flexible work schedule','Proximity to station (home)','Proximity to station (school)','Comfortable sidewalk access','Timely PT schedule','PT is clean','More affordable fare','Combined with own commute/errand (trip-chaining)'],true)}</div>
  <div class="field"><div class="q-label">${t('How often does weather (heavy rain/extreme heat) change your usual school-commute mode?')}</div>${opts('weather_mode_change',['Never','Rarely','Sometimes','Often','Always'])}</div>
  <div class="field"><div class="q-label">${t('Has your child ever used BTS Skytrain on their own, without an adult?')}</div>${opts('used_bts_alone',['Yes','No'])}</div>
  <div class="field"><div class="q-label">${t('Has your child ever used MRT on their own, without an adult?')}</div>${opts('used_mrt_alone',['Yes','No'])}</div>
  <div class="field"><div class="q-label">${t('Has your child ever used a city bus on their own, without an adult?')}</div>${opts('used_bus_alone',['Yes','No'])}</div>
  <div class="field"><div class="q-label">${t('How safe does it feel to escort your child by motorcycle (vs by car)?')}</div>${opts('moto_safety',['1','2','3','4','5'])}</div>
  <div class="field"><div class="q-label">${t('If child travels by school bus/songthaew/moto-taxi, how much do you trust the driver?')}</div>${opts('driver_trust',['1','2','3','4','5'])}</div>`},""",

"""{name:'Escorting - Travel Mode', tag:'Section 4 - Travel Mode', render:()=>`
  <div class="field"><div class="q-label">${t('How do you typically escort your children? (main mode)')}</div>
    ${opts('escort_mode',['Walk','Bike','School bus','Private car','Private motorbike','Ride-hailing','Taxi meter','MRT','BTS','Bus'])}</div>
  <div class="field"><div class="q-label">${t('Why this mode? (top 3)')}</div>
    ${opts('mode_reason',['Same mode as my work commute','Escort multiple children at once','Most convenient','Quality time with children','Only mode available','Flexible work schedule','Proximity to station (home)','Proximity to station (school)','Comfortable sidewalk access','Timely PT schedule','PT is clean','More affordable fare','Combined with own commute/errand (trip-chaining)','Ride-hailing as backup when I cannot escort in person'],true)}</div>
  <div class="field"><div class="q-label">${t('How often does weather (heavy rain/extreme heat) change your usual school-commute mode?')}</div>${opts('weather_mode_change',['Never','Rarely','Sometimes','Often','Always'])}</div>
  <div class="field"><div class="q-label">${t('How often does your household use a ride-hailing app (e.g. Grab, Line Man, inDrive, Bolt) to send/pick up your child for school?')}</div>${opts('ridehailing_freq',['Never','Rarely','Sometimes','Often','Always'])}</div>
  <div class="field"><div class="q-label">${t('Has your child ever used BTS Skytrain on their own, without an adult?')}</div>${opts('used_bts_alone',['Yes','No'])}</div>
  <div class="field"><div class="q-label">${t('Has your child ever used MRT on their own, without an adult?')}</div>${opts('used_mrt_alone',['Yes','No'])}</div>
  <div class="field"><div class="q-label">${t('Has your child ever used a city bus on their own, without an adult?')}</div>${opts('used_bus_alone',['Yes','No'])}</div>
  <div class="field"><div class="q-label">${t('How safe does it feel to escort your child by motorcycle (vs by car)?')}</div>${opts('moto_safety',['1','2','3','4','5'])}</div>
  <div class="field"><div class="q-label">${t('If child travels by school bus/songthaew/moto-taxi, how much do you trust the driver?')}</div>${opts('driver_trust',['1','2','3','4','5'])}</div>
  <div class="field"><div class="q-label">${t('If child travels by a ride-hailing app (Grab/Line Man/inDrive/Bolt), how much do you trust the driver?')}</div>${opts('ridehailing_trust',['1','2','3','4','5'])}</div>`},"""
)

# A4) SP buildModule1: add a 6th round pooling ride-hailing into the third-party card
rep(
"""      {title:'Third-party escort (songthaew)',icon:'VAN',time:20,fare:15,danger:2,crime:2,companion:'Third-party escort',trust:'Low'},
      {title:'Child travels alone by PT',icon:'BUS',time:30,fare:50,danger:2,crime:2,companion:'Escorted by guardian on arrival',wait:15,walkbike:7}
    ]},
  ];
}""",
"""      {title:'Third-party escort (songthaew)',icon:'VAN',time:20,fare:15,danger:2,crime:2,companion:'Third-party escort',trust:'Low'},
      {title:'Child travels alone by PT',icon:'BUS',time:30,fare:50,danger:2,crime:2,companion:'Escorted by guardian on arrival',wait:15,walkbike:7}
    ]},
    {round:6, options:[
      {title:escortTitle,icon:escortIcon,time:18,fare:0,danger:2,crime:2,companion:'Escorted by parent'},
      {title:'Third-party escort (ride-hailing)',icon:'VAN',time:20,fare:60,danger:2,crime:2,companion:'Third-party escort',trust:'Medium'},
      {title:'Child travels alone by PT',icon:'BUS',time:25,fare:20,danger:3,crime:2,companion:'Travels alone',wait:12,walkbike:6}
    ]},
  ];
}"""
)

# ============================================================================
# SECTION B - Conditional BTS/MRT and car fields per trip segment
# ============================================================================
# The BTS/MRT line+station fields and the car driver/passenger field used to
# show on every trip segment regardless of the mode picked. Compute the
# segment's mode once and only render those fields when a matching mode is
# actually selected.

# B1) compute isRailMode / isCarMode from the segment's chosen mode
rep(
"""  const purposeKey='purpose_'+ns;
  const isEscort = (val(purposeKey)||'').indexOf('Escorting')>=0 || (val(purposeKey)||'').indexOf('drop-off')>=0 || (val(purposeKey)||'').indexOf('pick-up')>=0;
  const seg = `<div class="q-help">${t('Segment')} ${i+1} ${t('of')} ${totalSegs}</div>""",
"""  const purposeKey='purpose_'+ns;
  const isEscort = (val(purposeKey)||'').indexOf('Escorting')>=0 || (val(purposeKey)||'').indexOf('drop-off')>=0 || (val(purposeKey)||'').indexOf('pick-up')>=0;
  const segMode = val('mode_'+ns);
  const isRailMode = segMode==='MRT' || segMode==='BTS Skytrain';
  const isCarMode = segMode==='Private car';
  const seg = `<div class="q-help">${t('Segment')} ${i+1} ${t('of')} ${totalSegs}</div>"""
)

# B2) wrap the rail fields and the car field in the new conditionals
rep(
"""    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('If BTS or MRT: which line?')}</div>
      ${selectOpts('line_'+ns,['Red Line (Bang Sue - Rangsit/Thammasat)','Red Line (Bang Sue - Taling Chan)','Airport Rail Link (Phaya Thai - Makkasan - Suvarnabhumi)','Green Line - Sukhumvit (Khu Khot - Kehha)','Green Line - Silom (National Stadium - Bang Wa)','Blue Line (Tha Phra - Bang Sue - Hua Lamphong - Lak Song)','Purple Line (Tao Poon - Khlong Bang Phai)','Pink Line (Khae Rai - Pak Kret - Min Buri)','Yellow Line (Lat Phrao - Phatthanakan - Samrong)'])}</div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('If BTS or MRT: boarding station / alighting station')}</div>
      <div class="grid2"><input type="text" placeholder="${t('Boarding station')}"><input type="text" placeholder="${t('Alighting station')}"></div></div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('If by car: were you the driver or a passenger?')}</div>
      ${opts('driverpax_'+ns,['Driver','Passenger'])}</div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('Main purpose of this trip')}</div>""",
"""    ${isRailMode?`
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('If BTS or MRT: which line?')}</div>
      ${selectOpts('line_'+ns,['Red Line (Bang Sue - Rangsit/Thammasat)','Red Line (Bang Sue - Taling Chan)','Airport Rail Link (Phaya Thai - Makkasan - Suvarnabhumi)','Green Line - Sukhumvit (Khu Khot - Kehha)','Green Line - Silom (National Stadium - Bang Wa)','Blue Line (Tha Phra - Bang Sue - Hua Lamphong - Lak Song)','Purple Line (Tao Poon - Khlong Bang Phai)','Pink Line (Khae Rai - Pak Kret - Min Buri)','Yellow Line (Lat Phrao - Phatthanakan - Samrong)'])}</div>
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('If BTS or MRT: boarding station / alighting station')}</div>
      <div class="grid2"><input type="text" placeholder="${t('Boarding station')}"><input type="text" placeholder="${t('Alighting station')}"></div></div>`:''}
    ${isCarMode?`
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('If by car: were you the driver or a passenger?')}</div>
      ${opts('driverpax_'+ns,['Driver','Passenger'])}</div>`:''}
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('Main purpose of this trip')}</div>"""
)

# ============================================================================
# SECTION C - Stop-location capture + Edit button in trip diary
# ============================================================================
# Each trip-diary stop now carries an optional location: Home, a household
# member's registered workplace/school (one-click), or a manually entered
# place via the existing locPicker component. An "Edit" button next to each
# stop's Remove/Move controls opens the picker.

# C1) CSS for the new Edit button
rep(
'.drag-handle{margin-left:8px;color:var(--sub);font-size:11px;cursor:grab;border:1px solid var(--line);border-radius:6px;padding:2px 6px;background:#fff;user-select:none}',
'.drag-handle{margin-left:8px;color:var(--sub);font-size:11px;cursor:grab;border:1px solid var(--line);border-radius:6px;padding:2px 6px;background:#fff;user-select:none}\n'
'.edit-stop{margin-left:8px;color:var(--blue-dark);font-size:11px;cursor:pointer;border:1px solid var(--line);border-radius:6px;padding:2px 8px;background:#fff;font-weight:700;user-select:none}'
)

# C2) give every stop a stable id (needed to key its location fields)
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

# C3) the location-picker modal itself, plus the label helper - inserted right
#     after resetTripState()
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

# C4) stop-list render: show each stop's location status + Edit button; the
#     "+ Add a stop" button now creates stops via newStop() too
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

# ============================================================================
# SECTION D - Trip diary fixes: add-stop-at-end, motorbike driver/pax,
# school-escort merge, map zoom controls
# ============================================================================
# 1. "+ Add a stop" always inserted before the last stop instead of at the
#    true end of the list.
# 2. The driver/passenger question only showed for "Private car", not for
#    "Private motorbike".
# 3. "Going to school (drop-off)" and "Return to school (pick-up)" were two
#    separate purpose options duplicating the To-school/From-school toggle
#    already asked in the escort extra-detail box - merged into one
#    "School escort" option.
# 4. Every embedded Google Map (keyless "output=embed" iframe) could not be
#    panned/zoomed reliably - added manual +/- zoom controls as a fallback
#    that don't depend on the map's own JS.

# D1) CSS for the zoom control buttons
rep(
'.loc-map-real{border-top:1px solid var(--line);background:#eef2f7}',
'.loc-map-real{border-top:1px solid var(--line);background:#eef2f7}\n'
'.map-zoom-ctrl{position:absolute;top:8px;right:8px;display:flex;flex-direction:column;gap:4px;z-index:2}\n'
'.map-zoom-ctrl button{width:28px;height:28px;border-radius:6px;border:1px solid var(--line);background:#fff;font-size:16px;font-weight:700;cursor:pointer;box-shadow:0 1px 3px rgba(0,0,0,.15);line-height:1}'
)

# D2) T dict: new driver/passenger label (car-or-motorbike), "School escort",
#     and the updated map-hint text mentioning the zoom buttons
rep(
'"If by car: were you the driver or a passenger?":"หากเดินทางโดยรถยนต์: ท่านเป็นผู้ขับหรือผู้โดยสาร","Driver":"ผู้ขับ","Passenger":"ผู้โดยสาร",',
'"If by car: were you the driver or a passenger?":"หากเดินทางโดยรถยนต์: ท่านเป็นผู้ขับหรือผู้โดยสาร","If by car or motorbike: were you the driver or a passenger?":"หากเดินทางโดยรถยนต์หรือรถจักรยานยนต์: ท่านเป็นผู้ขับหรือผู้โดยสาร","Driver":"ผู้ขับ","Passenger":"ผู้โดยสาร",'
)
rep(
'"Commuting to work":"เดินทางไปทำงาน","Going to school (drop-off)":"ไปโรงเรียน (ไปส่ง)","Going to school (for children)":"ไปโรงเรียน (สำหรับเด็ก)",',
'"Commuting to work":"เดินทางไปทำงาน","School escort":"รับส่งบุตรหลานไปโรงเรียน","Going to school (drop-off)":"ไปโรงเรียน (ไปส่ง)","Going to school (for children)":"ไปโรงเรียน (สำหรับเด็ก)",'
)
rep(
'"Real Google Map - search above to move the map, or paste coordinates below and press Confirm to drop a pin at an exact spot. On Google Maps, right-click (or long-press) a spot and choose \\"What\'s here?\\" to get its coordinates.":"แผนที่ Google จริง - ค้นหาด้านบนเพื่อขยับแผนที่ หรือวางพิกัดด้านล่างแล้วกดยืนยันเพื่อปักหมุดตำแหน่งที่แน่นอน บน Google Maps ให้คลิกขวา (หรือกดค้าง) ที่จุดนั้นแล้วเลือก \\"What\'s here?\\" เพื่อดูพิกัด",',
'"Real Google Map - search above to move the map, or paste coordinates below and press Confirm to drop a pin at an exact spot. On Google Maps, right-click (or long-press) a spot and choose \\"What\'s here?\\" to get its coordinates.":"แผนที่ Google จริง - ค้นหาด้านบนเพื่อขยับแผนที่ หรือวางพิกัดด้านล่างแล้วกดยืนยันเพื่อปักหมุดตำแหน่งที่แน่นอน บน Google Maps ให้คลิกขวา (หรือกดค้าง) ที่จุดนั้นแล้วเลือก \\"What\'s here?\\" เพื่อดูพิกัด",\n'
'"Real Google Map - search above to move the map, use the +/- buttons to zoom, or paste coordinates below and press Confirm to drop a pin at an exact spot. On Google Maps, right-click (or long-press) a spot and choose \\"What\'s here?\\" to get its coordinates.":"แผนที่ Google จริง - ค้นหาด้านบนเพื่อขยับแผนที่ กดปุ่ม +/- เพื่อซูม หรือวางพิกัดด้านล่างแล้วกดยืนยันเพื่อปักหมุดตำแหน่งที่แน่นอน บน Google Maps ให้คลิกขวา (หรือกดค้าง) ที่จุดนั้นแล้วเลือก \\"What\'s here?\\" เพื่อดูพิกัด",'
)

# D3) mapSrc/zoomMap: a per-location zoom level, adjustable with +/-
rep(
"""function mapSrc(id){
  if(A[id+'_confirmed'] && A[id+'_lat'] && A[id+'_lng']){
    return 'https://www.google.com/maps?q='+encodeURIComponent(A[id+'_lat']+','+A[id+'_lng'])+'&z=17&output=embed';
  }
  const q = encodeURIComponent(A[id+'_search'] || A[id+'_name'] || 'Bangkok, Thailand');
  return 'https://www.google.com/maps?q='+q+'&output=embed';
}""",
"""function mapSrc(id){
  const z = A[id+'_zoom'] || 17;
  if(A[id+'_confirmed'] && A[id+'_lat'] && A[id+'_lng']){
    return 'https://www.google.com/maps?q='+encodeURIComponent(A[id+'_lat']+','+A[id+'_lng'])+'&z='+z+'&output=embed';
  }
  const q = encodeURIComponent(A[id+'_search'] || A[id+'_name'] || 'Bangkok, Thailand');
  return 'https://www.google.com/maps?q='+q+'&z='+z+'&output=embed';
}
window.zoomMap = (id,delta)=>{
  const z = Math.min(20, Math.max(3, (A[id+'_zoom']||17)+delta));
  A[id+'_zoom'] = z;
  const ifr = document.getElementById('map_'+id);
  if(ifr) ifr.src = mapSrc(id);
};"""
)

# D4) locPicker: render the zoom buttons over the map iframe
rep(
"""    <div class="loc-map-real"><iframe id="map_${id}" width="100%" height="180" style="border:0;display:block" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="${mapSrc(id)}"></iframe></div>
    <div class="loc-hint-real">${t('Real Google Map - search above to move the map, or paste coordinates below and press Confirm to drop a pin at an exact spot. On Google Maps, right-click (or long-press) a spot and choose "What\\'s here?" to get its coordinates.')}</div>""",
"""    <div class="loc-map-real" style="position:relative">
      <iframe id="map_${id}" width="100%" height="180" style="border:0;display:block" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="${mapSrc(id)}"></iframe>
      <div class="map-zoom-ctrl">
        <button type="button" onclick="zoomMap('${id}',1)">+</button>
        <button type="button" onclick="zoomMap('${id}',-1)">-</button>
      </div>
    </div>
    <div class="loc-hint-real">${t('Real Google Map - search above to move the map, use the +/- buttons to zoom, or paste coordinates below and press Confirm to drop a pin at an exact spot. On Google Maps, right-click (or long-press) a spot and choose "What\\'s here?" to get its coordinates.')}</div>"""
)

# D5) "+ Add a stop" pushes to the true end of the array instead of before
#     the last (fixed) stop
rep(
"    <button class=\"add-btn\" onclick=\"stops.splice(stops.length-1,0,newStop(''));tripConfirmed=false;renderRP()\">${t('+ Add a stop')}</button>",
"    <button class=\"add-btn\" onclick=\"stops.push(newStop(''));tripConfirmed=false;renderRP()\">${t('+ Add a stop')}</button>"
)

# D6) isEscort / isCarMode / purpose list: merge the two school purposes,
#     and treat "Private motorbike" as a car-like mode for the driver/
#     passenger question
rep(
"  const isEscort = (val(purposeKey)||'').indexOf('Escorting')>=0 || (val(purposeKey)||'').indexOf('drop-off')>=0 || (val(purposeKey)||'').indexOf('pick-up')>=0;",
"  const isEscort = (val(purposeKey)||'').indexOf('Escorting')>=0 || (val(purposeKey)||'').indexOf('School escort')>=0;"
)
rep(
"  const isCarMode = segMode==='Private car';",
"  const isCarMode = segMode==='Private car' || segMode==='Private motorbike';"
)
rep(
"""    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('If by car: were you the driver or a passenger?')}</div>
      ${opts('driverpax_'+ns,['Driver','Passenger'])}</div>`:''}
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('Main purpose of this trip')}</div>
      ${opts(purposeKey,['Commuting to work','Going to school (drop-off)','Going to school (for children)','Return home','Return to workplace','Return to school (pick-up)','Escorting (other)','Shopping','Leisure','Medical-related','Other private purpose','Business/work-related'])}</div>""",
"""    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('If by car or motorbike: were you the driver or a passenger?')}</div>
      ${opts('driverpax_'+ns,['Driver','Passenger'])}</div>`:''}
    <div class="field" style="border:none;padding:0;margin-bottom:10px"><div class="q-label" style="font-size:13px">${t('Main purpose of this trip')}</div>
      ${opts(purposeKey,['Commuting to work','School escort','Going to school (for children)','Return home','Return to workplace','Escorting (other)','Shopping','Leisure','Medical-related','Other private purpose','Business/work-related'])}</div>"""
)

# ============================================================================
# SECTION E - Edit routes straight to a stop's custom location + Thai
# translations for the whole stop-location feature
# ============================================================================
# Previously, pressing Edit on a stop that already had a custom (manually
# entered) location re-opened the quick-pick list every time. Now Edit routes
# straight into the location edit form when a custom location is already
# set, with a way back to the quick-pick list. Also fills in the Thai
# translations the stop-location feature was still missing.

# E1) Thai translations for the stop-location feature
rep(
'"Adult":"ผู้ใหญ่","Child":"เด็ก","Tap to set up":"แตะเพื่อกรอกข้อมูล",',
'"Adult":"ผู้ใหญ่","Child":"เด็ก","Tap to set up":"แตะเพื่อกรอกข้อมูล",\n'
'"Home":"บ้าน","Use this":"ใช้อันนี้","- workplace":"- ที่ทำงาน","- school":"- โรงเรียน",\n'
'" - workplace (registered)":" - ที่ทำงาน (ลงทะเบียนไว้)"," - school (registered)":" - โรงเรียน (ลงทะเบียนไว้)","Home (registered)":"บ้าน (ลงทะเบียนไว้)",\n'
'"No location set yet":"ยังไม่ได้ระบุตำแหน่ง",\n'
'"Set location for":"ระบุตำแหน่งของ","Choose a registered place, or enter a new one below.":"เลือกสถานที่ที่ลงทะเบียนไว้ หรือกรอกสถานที่ใหม่ด้านล่าง",\n'
'"Not in this list - enter manually":"ไม่มีในนี้ - กรอกเอง","Enter location":"กรอกตำแหน่ง","Choose a registered place instead":"เลือกจากสถานที่ที่ลงทะเบียนไว้แทน",'
)

# E2) split the quick-pick list out into its own function (showStopLocList)
#     so it can be reopened later from the custom-location edit form
rep(
"""window.openStopLocationPicker = (stopId)=>{
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
};""",
"""window.showStopLocList = (stopId)=>{
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
};
window.openStopLocationPicker = (stopId)=>{
  const s = stops.find(x=>x.id===stopId);
  if(!s) return;
  document.getElementById('modal-overlay').classList.add('open');
  if(s.loc && s.loc.type==='custom'){ stopLocCustom(stopId); }
  else { showStopLocList(stopId); }
};"""
)

# E3) the custom-location edit form now offers a way back to the quick-pick
#     list instead of only a "Save & close" button
rep(
"""window.stopLocCustom = (stopId)=>{
  document.getElementById('modal-title').textContent = t('Enter location');
  document.getElementById('modal-body').innerHTML = `
    ${locPicker(stopId)}
    <div class="nav-row"><span></span><button class="btn btn-primary" onclick="confirmStopLocCustom('${stopId}')">${t('Save & close')}</button></div>
  `;
};""",
"""window.stopLocCustom = (stopId)=>{
  document.getElementById('modal-title').textContent = t('Enter location');
  document.getElementById('modal-body').innerHTML = `
    ${locPicker(stopId)}
    <div class="nav-row">
      <button class="btn btn-ghost" style="border:1px solid var(--line)" onclick="showStopLocList('${stopId}')">${t('Choose a registered place instead')}</button>
      <button class="btn btn-primary" onclick="confirmStopLocCustom('${stopId}')">${t('Save & close')}</button>
    </div>
  `;
};"""
)

with open(path,'w',encoding='utf-8') as f:
    f.write(c)
print("part4 (catchup) done")
