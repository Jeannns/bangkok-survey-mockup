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

# The BTS/MRT line+station fields and the car driver/passenger field used to
# show on every trip segment regardless of the mode picked, which looked
# cluttered. Compute the segment's mode once and only render those fields
# when a matching mode is actually selected.

# 1) compute isRailMode / isCarMode from the segment's chosen mode
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

# 2) wrap the rail fields and the car field in the new conditionals
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

with open(path,'w',encoding='utf-8') as f:
    f.write(c)
print("part5 done")
