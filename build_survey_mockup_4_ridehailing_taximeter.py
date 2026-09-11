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

# Add ride-hailing usage/trust questions + "Taxi meter" rename to RP, and a
# pooled ride-hailing option to SP Module 1. Example services shown to
# respondents: Grab, Line Man, inDrive, Bolt.

# 1) T dict - escort-mode/reasons/weather block: rename Taxi -> Taxi meter,
#    add ride-hailing-as-backup reason + frequency/trust question translations
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

# 2) T dict - SP labels block: add "Medium" + third-party ride-hailing card title
rep(
'"School buddy":"เพื่อนไปโรงเรียนด้วยกัน","Guardian":"ผู้ปกครอง/ผู้ดูแล","Poor":"แย่","Good":"ดี","Moderate":"ปานกลาง","High":"สูง","Low":"ต่ำ",',
'"School buddy":"เพื่อนไปโรงเรียนด้วยกัน","Guardian":"ผู้ปกครอง/ผู้ดูแล","Poor":"แย่","Good":"ดี","Moderate":"ปานกลาง","High":"สูง","Low":"ต่ำ","Medium":"ปานกลาง",\n'
'"Third-party escort (ride-hailing)":"บุคคลที่สามรับส่ง (เรียกรถผ่านแอป)",'
)

# 3) RP "Escorting - Travel Mode" step: rename Taxi->Taxi meter in mode list,
#    add ride-hailing reason, and the two new frequency/trust questions
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

# 4) SP buildModule1: add a 6th round pooling ride-hailing into the third-party card
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

with open(path,'w',encoding='utf-8') as f:
    f.write(c)
print("part4 done")
