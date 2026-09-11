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

# Previously, pressing Edit on a stop that already had a custom (manually
# entered) location re-opened the quick-pick list every time, forcing an
# extra click through "Not in this list" to actually see/edit that
# location's details. Now Edit routes straight into the location edit form
# when a custom location is already set, with a way back to the quick-pick
# list. Also fills in the Thai translations the whole stop-location feature
# was still missing.

# 1) Thai translations for the stop-location feature (previously fell back
#    to English via the t() function's untranslated-key fallback)
rep(
'"Adult":"ผู้ใหญ่","Child":"เด็ก","Tap to set up":"แตะเพื่อกรอกข้อมูล",',
'"Adult":"ผู้ใหญ่","Child":"เด็ก","Tap to set up":"แตะเพื่อกรอกข้อมูล",\n'
'"Home":"บ้าน","Use this":"ใช้อันนี้","- workplace":"- ที่ทำงาน","- school":"- โรงเรียน",\n'
'" - workplace (registered)":" - ที่ทำงาน (ลงทะเบียนไว้)"," - school (registered)":" - โรงเรียน (ลงทะเบียนไว้)","Home (registered)":"บ้าน (ลงทะเบียนไว้)",\n'
'"No location set yet":"ยังไม่ได้ระบุตำแหน่ง",\n'
'"Set location for":"ระบุตำแหน่งของ","Choose a registered place, or enter a new one below.":"เลือกสถานที่ที่ลงทะเบียนไว้ หรือกรอกสถานที่ใหม่ด้านล่าง",\n'
'"Not in this list - enter manually":"ไม่มีในนี้ - กรอกเอง","Enter location":"กรอกตำแหน่ง","Choose a registered place instead":"เลือกจากสถานที่ที่ลงทะเบียนไว้แทน",'
)

# 2) split the quick-pick list out into its own function (showStopLocList)
#    so it can be reopened later from the custom-location edit form
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

# 3) the custom-location edit form now offers a way back to the quick-pick
#    list instead of only a "Save & close" button
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
print("part8 done")
