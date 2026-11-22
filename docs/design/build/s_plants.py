from ff import *

plants = [
  ('K1', 'Koyo 1', 'Sachet water · Koyo · pilot', 'Tripped', 'Lead interlock stopped filling at 08:14. Recovery 2 of 7 steps done.', '1,743 bags this shift', 'Main.dc.html'),
  ('OM', 'Oil mill', 'Edible oil · Ibadan · sample', 'Alert', 'Expeller EX-3 tripped on overload. EX-1 and EX-2 carry the line at 67 %.', '6.1 t oil this shift', 'OilMill.dc.html'),
  ('PB', 'Plant B', 'Bottled water · sample', 'Alert', 'RO salt rejection under the alert limit. Production continues.', '14,200 bottles today', '#'),
  ('PD', 'Plant D', 'Sachet water · sample', 'Offline', 'No data for 3 h. The plant keeps recording and syncs when the link returns.', 'Last seen 05:34', '#'),
  ('RM', 'Rice mill', 'Rice milling · Kano · sample', 'Running', 'All 16 machines running. Head rice yield 64.5 %.', '21.6 t milled this shift', 'RiceMill.dc.html'),
  ('PF', 'Poultry farm', 'Layer farm · Ogun · sample', 'Alert', 'House H3 at 31.8 °C with all tunnel fans on. Lay rate 84 % in H3.', '9,870 eggs today · 329 trays', 'PoultryFarm.dc.html'),
]
look = {
  'Tripped': ('s-red', 'var(--outline-red-3)', '#fff'),
  'Alert': ('amber', 'var(--outline-amber-3)', 'var(--surface-amber-6)'),
  'Offline': ('gray', 'var(--outline-gray-1)', None),
  'Running': ('green', 'var(--outline-gray-1)', 'var(--ink-green-7)'),
}
cards = ''
for ini, name, meta, st, note, foot, href in plants:
    bc, border, dot = look[st]
    d = f'<span class="dot" style="background:{dot}"></span>' if dot else '<span class="dot o"></span>'
    cards += f'''<a href="{href}" class="card" aria-label="Open {name}" style="display:flex;flex-direction:column;gap:12px;border-color:{border};color:inherit;cursor:pointer">
<div style="display:flex;align-items:center;gap:10px"><span aria-hidden="true" style="width:36px;height:36px;flex:0 0 36px;border-radius:8px;background:var(--surface-gray-2);color:var(--ink-gray-7);display:grid;place-items:center;font-weight:600;font-size:13px">{ini}</span>
<div style="display:flex;flex-direction:column;gap:2px;min-width:0;flex:1"><span style="font-size:15px;font-weight:600;color:var(--ink-gray-9)">{name}</span><span class="qs">{meta}</span></div>
<span class="bd {bc}">{d}{st}</span></div>
<p class="ps" style="min-height:39px">{note}</p>
<div style="display:flex;align-items:center;justify-content:space-between;padding-top:12px;border-top:1px solid var(--outline-gray-1);font-size:13px"><span class="qs">{foot}</span><span style="display:inline-flex;align-items:center;gap:4px;color:var(--ink-gray-8);font-weight:500">Open{ic("chev-r","i s35")}</span></div></a>'''
cards += f'<a href="AddPlant.dc.html" class="btn ghost" style="height:auto;min-height:160px;flex-direction:column;border:1px dashed var(--outline-gray-2);border-radius:12px;color:var(--ink-gray-6)">{ic("plus")}Add plant</a>'

head = header(f'<div class="crumb"><span class="cur">Plants</span></div>', f'<div class="seg"><span class="on">Cards</span><span>Table</span></div>')
body = f'''<div class="body"><div style="display:flex;align-items:center;justify-content:space-between;gap:8px"><div style="display:flex;align-items:baseline;gap:8px"><h2 class="h2">Your plants</h2><span class="qs">6 plants · open one to see it live</span></div><span class="in muted" style="width:240px">{ic("search")}<span class="grow">Search plants</span></span></div>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px">{cards}</div></div>'''
write('Plants.dc.html', page('Plants', shell('Plants.dc.html', head, body, scope='company'), {"$preview": {"width": 1440, "height": 900}}))
