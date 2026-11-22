from ff import *

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Resources',None)),
  f'<span class="bd gray"><span class="dot g"></span>Live · 10 s</span><button type="button" class="btn solid">{ic("package")}Request materials</button>')

def tank(name, desc, pct, vol, cap, note, color='var(--ink-gray-7)', warn=''):
    h = 112
    lvl = h*pct/100
    marks = ''.join(f'<line x1="0" x2="6" y1="{h-h*p/100:.0f}" y2="{h-h*p/100:.0f}" stroke="var(--outline-gray-3)"/>' for p in (25,50,75))
    return f'''<div style="display:flex;flex-direction:column;gap:12px">
<svg width="56" height="{h+2}" viewBox="0 0 56 {h+2}" role="img" aria-label="{name} {pct}%"><rect x="0.5" y="0.5" width="55" height="{h}" rx="6" fill="var(--surface-gray-1)" stroke="var(--outline-gray-2)"/><rect x="1" y="{h-lvl+0.5:.1f}" width="54" height="{lvl:.1f}" rx="5" fill="{color}" opacity=".85"/>{marks}</svg>
<div style="display:flex;flex-direction:column;gap:4px;min-width:0"><span style="font-weight:600;color:var(--ink-gray-9)">{name}</span><span class="qs">{desc}</span><span class="tab" style="font-size:20px;font-weight:600;color:var(--ink-gray-9);margin-top:4px">{pct}%</span><span class="qs tab">{vol} of {cap} m³</span><span style="font-size:13px;color:{warn or 'var(--ink-gray-7)'}">{note}</span></div></div>'''

tanks = f'''<section class="card" style="display:flex;flex-direction:column;gap:16px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h3">Water</h2><span class="qs">Level transmitters LT-101 … LT-501</span></div>
<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px">
{tank('T1 · Raw', 'Borehole feed', 58, '11.6', '20', 'Lasts 14 h at 4.8 m³/h net draw')}
{tank('T2 · Permeate', 'After RO', 70, '3.5', '5', 'Lasts 3.1 h with RO stopped')}
{tank('T4 · Verification', 'Before fillers', 0, '0.0', '2', 'Drained for the trip', 'var(--ink-gray-7)', 'var(--ink-gray-5)')}
{tank('T5 · Quarantine', 'Rejected water', 46, '2.3', '5', 'Full in 1 h 10 min', 'var(--surface-red-6)', 'var(--ink-red-7)')}
</div></section>'''

# diesel 7-day level with refills
lv = [62,58,54,50,46,42,38,34,30,90,86,82,78,74,70,66,62,58,54,50,46,42,38,34,30,28]
diesel_chart = spark(lv, 420, 70, 'var(--ink-gray-8)', 0, 100, lines=((25, 'var(--ink-amber-7)'),))
energy = f'''<section class="card" style="display:flex;flex-direction:column;gap:14px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h3">Power</h2>{bd("On generator","amber")}</div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">
<div class="kpi"><span class="k">Diesel</span><span class="v" style="color:var(--ink-amber-7)">41 h</span><span class="d tab">560 of 2,000 L · 13.7 L/h</span></div>
<div class="kpi"><span class="k">Grid today</span><span class="v">62%</span><span class="d">Off since 07:40</span></div>
<div class="kpi"><span class="k">Gen service</span><span class="v">188 h</span><span class="d tab">4,812 of 5,000 run hours</span></div>
</div>
<div class="inset" style="display:flex;flex-direction:column;gap:6px"><div style="display:flex;justify-content:space-between" class="qs"><span>Diesel level · last 7 days</span><span>Refilled 18 Nov · 1,200 L</span></div>{diesel_chart}<div style="display:flex;justify-content:space-between" class="qs"><span>16 Nov</span><span style="display:inline-flex;align-items:center;gap:4px"><i style="width:12px;border-top:1px dashed var(--ink-amber-7)"></i>Reorder at 25% · 500 L</span><span>Now</span></div></div>
</section>'''

C = 'grid-template-columns:minmax(0,1.5fr) 100px 96px 88px minmax(0,1.1fr) 168px 80px'
items = [
  ('Antiscalant', 'Dosing pump DP-1 · before RO', '38 L', '1.7 L/h', 22, 48, '22 h', 'amber', '2 drums · 25 L'),
  ('Remineralization A · CaCl₂', 'Dosing pump DP-3A', '46 L', '1.2 L/h', 38, 48, '38 h', 'amber', '4 drums · 25 L'),
  ('Remineralization B · NaHCO₃', 'Dosing pump DP-3B', '51 L', '1.2 L/h', 42, 48, '42 h', 'amber', '6 bags · 25 kg'),
  ('Remineralization C · MgSO₄', 'Dosing pump DP-3C', '60 L', '0.8 L/h', 75, 48, '3.1 days', '', '5 bags · 25 kg'),
  ('Sachet film 320 mm', 'Fillers F1 – F10', '52 rolls · 25 kg', '34 rolls/day', 36, 24, '1.5 days', '', '70 rolls'),
  ('Cartridge filter 5 µm', 'CF-201 · ΔP 0.6 of 1.0 bar', '9 days old', '—', 504, 72, '21 days', '', '12 cartridges'),
  ('Cartridge filter 1 µm', 'CF-301 · ΔP 0.3 of 1.0 bar', '9 days old', '—', 504, 72, '21 days', '', '10 cartridges'),
  ('UV lamp', 'UV-301 · 96% intensity', '6,920 h', '24 h/day', 2088, 720, '87 days', '', '1 spare'),
  ('Ion-exchange resin', 'IX-501 · quarantine loop', '12% used', 'by volume', 9999, 0, 'by throughput', '', 'Regenerate at 80%'),
]
rows = []
for n, w, oh, rate, hrs, reorder, run, warn, stock in items:
    pct = min(hrs/ (reorder*3 if reorder else 1) * 100, 100) if reorder else 88
    barcls = 'a' if warn else ''
    rc = 'color:var(--ink-amber-7);font-weight:500' if warn else 'color:var(--ink-gray-8)'
    act = btn('Request', kind='xs') if warn else '<span class="qs">—</span>'
    reo = (f'{reorder} h' if reorder < 200 else f'{reorder//24} days') if reorder else '—'
    rows.append(f'''<div class="lr" style="{C};min-height:56px;cursor:default"><span class="c"><div class="t1">{n}</div><div class="m">{w}</div></span><span class="tab">{oh}</span><span class="tab qs" style="color:var(--ink-gray-7)">{rate}</span><span class="tab qs" style="color:var(--ink-gray-7)">{reo}</span>
<span style="display:flex;flex-direction:column;gap:6px;min-width:0"><span class="tab" style="{rc}">{run}</span><span class="bar"><i class="{barcls}" style="width:{pct:.0f}%"></i></span></span><span class="qs c">{stock}</span><span style="display:flex;justify-content:flex-end">{act}</span></div>''')
table = f'''<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><div style="display:flex;gap:8px;align-items:center"><h2 class="h2">Consumables</h2>{bd("3 under reorder point","amber")}</div><span class="qs">Stock from ERPNext warehouse Koyo 1 · Stores</span></div>
<div class="list"><div class="lh" style="{C}"><span>Item</span><span>On hand</span><span>Use rate</span><span>Reorder at</span><span>Runway</span><span>In store</span><span></span></div>{''.join(rows)}</div>
<p class="qs" style="margin:0">Runway uses the last 24 h of use. Request creates an ERPNext Material Request for the plant's store, with the drum or bag size as the unit.</p></section>'''

body = f'<div class="body" style="overflow:auto"><div style="display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:12px">{tanks}{energy}</div>{table}</div>'
write('Resources.dc.html', page('Resources', shell('Resources.dc.html', head, body), {"$preview": {"width": 1440, "height": 900}}))
