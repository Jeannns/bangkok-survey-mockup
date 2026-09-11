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

# Four fixes from a screenshot review round:
#  1. "+ Add a stop" always inserted before the last stop instead of at the
#     true end of the list.
#  2. The driver/passenger question only showed for "Private car", not for
#     "Private motorbike".
#  3. "Going to school (drop-off)" and "Return to school (pick-up)" were two
#     separate purpose options duplicating the To-school/From-school toggle
#     already asked in the escort extra-detail box - merged into one
#     "School escort" option.
#  4. Every embedded Google Map (keyless "output=embed" iframe) could not be
#     panned/zoomed reliably - added manual +/- zoom controls as a fallback
#     that don't depend on the map's own JS.

# 1) CSS for the zoom control buttons
rep(
'.loc-map-real{border-top:1px solid var(--line);background:#eef2f7}',
'.loc-map-real{border-top:1px solid var(--line);background:#eef2f7}\n'
'.map-zoom-ctrl{position:absolute;top:8px;right:8px;display:flex;flex-direction:column;gap:4px;z-index:2}\n'
'.map-zoom-ctrl button{width:28px;height:28px;border-radius:6px;border:1px solid var(--line);background:#fff;font-size:16px;font-weight:700;cursor:pointer;box-shadow:0 1px 3px rgba(0,0,0,.15);line-height:1}'
)

# 2) T dict: new driver/passenger label (car-or-motorbike), "School escort",
#    and the updated map-hint text mentioning the zoom buttons
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

# 3) mapSrc/zoomMap: a per-location zoom level, adjustable with +/-
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

# 4) locPicker: render the zoom buttons over the map iframe
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

# 5) "+ Add a stop" pushes to the true end of the array instead of before
#    the last (fixed) stop
rep(
"    <button class=\"add-btn\" onclick=\"stops.splice(stops.length-1,0,newStop(''));tripConfirmed=false;renderRP()\">${t('+ Add a stop')}</button>",
"    <button class=\"add-btn\" onclick=\"stops.push(newStop(''));tripConfirmed=false;renderRP()\">${t('+ Add a stop')}</button>"
)

# 6) isEscort / isCarMode / purpose list: merge the two school purposes,
#    and treat "Private motorbike" as a car-like mode for the driver/
#    passenger question
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

with open(path,'w',encoding='utf-8') as f:
    f.write(c)
print("part7 done")
