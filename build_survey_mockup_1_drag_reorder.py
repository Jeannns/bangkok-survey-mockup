import io
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

# 1) CSS additions - insert after .remove{...} rule
rep(
'.remove{margin-left:auto;color:#ef4444;cursor:pointer;font-size:12px;font-weight:700}',
'.remove{margin-left:auto;color:#ef4444;cursor:pointer;font-size:12px;font-weight:700}\n'
'.drag-handle{margin-left:8px;color:var(--sub);font-size:11px;cursor:grab;border:1px solid var(--line);border-radius:6px;padding:2px 6px;background:#fff;user-select:none}\n'
'.stop-item.drag-over{outline:2px dashed var(--blue)}\n'
'.confirm-box{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:12px 14px;margin-top:10px;font-size:13px;color:#166534}\n'
'.prompt-box{background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:20px;text-align:center}\n'
'.prompt-box h4{margin:0 0 14px;font-size:16px}'
)

# 2) Global state + helper functions - insert after "window.toggleCompanion = ..." line
rep(
"window.toggleCompanion = (id)=>{ const k='companion_'+id; A[k]=!A[k]; renderRP(); };",
"""window.toggleCompanion = (id)=>{ const k='companion_'+id; A[k]=!A[k]; renderRP(); };

let tripConfirmed = false;
let segIdx = 0;
let showTripDonePrompt = false;
let dragSrcIdx = null;
window.dragStart = (i)=>{ dragSrcIdx = i; };
window.dropStop = (i)=>{
  if(dragSrcIdx===null || dragSrcIdx===i) return;
  const item = stops.splice(dragSrcIdx,1)[0];
  stops.splice(i,0,item);
  dragSrcIdx = null;
  tripConfirmed = false;
  renderRP();
};
function resetTripState(){
  tripPerson = null; stops = [{place:'Home'},{place:'School'},{place:'Home'}];
  tripConfirmed = false; segIdx = 0; showTripDonePrompt = false;
}

let lastSavedAt = null;
window.tempSave = ()=>{ lastSavedAt = new Date().toLocaleTimeString(); renderRP(); };
function tempSaveBtn(){
  return `<button class="btn btn-ghost" style="border:1px solid var(--line)" onclick="tempSave()">${lastSavedAt?'Draft saved '+lastSavedAt:'Save draft'}</button>`;
}"""
)

with open(path,'w',encoding='utf-8') as f:
    f.write(c)
print("part1 done")
