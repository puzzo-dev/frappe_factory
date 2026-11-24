"""Resources · Koyo 1: water tanks, power (grid, generator and its diesel tank) and consumables.
Clicking a consumable, the grid or the generator opens its detail in the panel on the right."""
from ff import *

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Resources',None)),
  f'<span class="bd gray"><span class="dot g"></span>Live · 10 s</span><button type="button" class="btn solid">{ic("package")}Request materials</button>')

def tank(name, desc, pct, vol, cap, note, color='oklch(0.925 0.039 243.489)', warn=''):
    h = 112
    lvl = h*pct/100
    marks = ''.join(f'<line x1="0" x2="6" y1="{h-h*p/100:.0f}" y2="{h-h*p/100:.0f}" stroke="var(--outline-gray-3)"/>' for p in (25,50,75))
    return f'''<div style="display:flex;flex-direction:column;gap:12px">
<svg width="56" height="{h+2}" viewBox="0 0 56 {h+2}" role="img" aria-label="{name} {pct}%"><rect x="0.5" y="0.5" width="55" height="{h}" rx="6" fill="var(--surface-gray-1)" stroke="var(--outline-gray-2)"/><rect x="1" y="{h-lvl+0.5:.1f}" width="54" height="{lvl:.1f}" rx="5" fill="{color}" />{marks}</svg>
<div style="display:flex;flex-direction:column;gap:4px;min-width:0"><span style="font-weight:600;color:var(--ink-gray-9)">{name}</span><span class="qs">{desc}</span><span class="tab" style="font-size:20px;font-weight:600;color:var(--ink-gray-9);margin-top:4px">{pct}%</span><span class="qs tab">{vol} of {cap} m³</span><span style="font-size:13px;color:{warn or 'var(--ink-gray-7)'}">{note}</span></div></div>'''

tanks = f'''<section class="card" style="display:flex;flex-direction:column;gap:16px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h3">Water</h2><span class="qs">Level transmitters LT-101 … LT-501</span></div>
<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px">
{tank('T1 · Raw', 'Borehole feed', 58, '11.6', '20', 'Lasts 14 h at 4.8 m³/h')}
{tank('T2 · Permeate', 'After RO', 70, '3.5', '5', 'Lasts 3.1 h, RO stopped')}
{tank('T4 · Verification', 'Before fillers', 0, '0.0', '2', 'Drained for the trip', warn='var(--ink-gray-6)')}
{tank('T5 · Quarantine', 'Rejected water', 46, '2.3', '5', 'Full in 1 h 10 min', 'var(--surface-amber-3)', 'var(--ink-red-7)')}
</div></section>'''

# ---------- power: the source is detected, not typed in
def src_tile(key, title, state, sub, on):
    border = 'var(--ink-amber-7)' if on else 'var(--outline-gray-2)'
    return (f'<div class="rtile {{{{cls_rsel__{key}}}}}" role="button" tabindex="0" onClick="{{{{set_rsel__{key}}}}}" style="display:flex;flex-direction:column;gap:6px;padding:12px;border-radius:10px;border:1px solid {border};cursor:pointer;min-width:0">'
            f'<div style="display:flex;justify-content:space-between;align-items:center"><span style="font-weight:600;color:var(--ink-gray-9)">{title}</span>{state}</div><span class="qs" style="font-size:13px;line-height:1.4">{sub}</span></div>')
energy = f'''<section class="card" style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h3">Power</h2>{bd("On generator","amber")}</div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;align-items:stretch">
{src_tile('grid', 'Grid', bd('Off', 'gray'), 'Off since 07:40 · 62% of today', False)}
{src_tile('gen', 'Generator', bd('Running', 'amber'), 'GEN-1 · 78 kW of 120 · diesel 41 h left', True)}
<div style="display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.45;color:var(--ink-gray-7);padding:4px 2px"><span style="display:flex;color:var(--ink-gray-6);margin-top:2px">{ic("info","i s35")}</span><span>Switched by itself at 07:40. Read from the changeover switch ATS-1 (PLC-1 input DI 0.4) and confirmed by the generator controller. Click a source for details; the generator shows its diesel tank.</span></div></div>
</section>'''

# ---------- consumables
C = 'grid-template-columns:minmax(0,1.5fr) 100px 96px 88px minmax(0,1.1fr) 150px'
items = [
  ('anti', 'Antiscalant', 'Dosing pump DP-1 · before RO', '38 L', '1.7 L/h', 22, 48, '22 h', 'amber', '2 drums · 25 L', 'Drum · 25 L', 'ANTI-25L', [52, 50, 48, 47, 45, 43, 41, 40, 38]),
  ('rema', 'Remineralization A · CaCl₂', 'Dosing pump DP-3A', '46 L', '1.2 L/h', 38, 48, '38 h', 'amber', '4 drums · 25 L', 'Drum · 25 L', 'REM-A-25L', [66, 63, 60, 58, 55, 53, 51, 48, 46]),
  ('remb', 'Remineralization B · NaHCO₃', 'Dosing pump DP-3B', '51 L', '1.2 L/h', 42, 48, '42 h', 'amber', '6 bags · 25 kg', 'Bag · 25 kg', 'REM-B-25KG', [70, 68, 65, 62, 60, 58, 56, 53, 51]),
  ('remc', 'Remineralization C · MgSO₄', 'Dosing pump DP-3C', '60 L', '0.8 L/h', 75, 48, '3.1 days', '', '5 bags · 25 kg', 'Bag · 25 kg', 'REM-C-25KG', [74, 72, 70, 69, 67, 65, 63, 62, 60]),
  ('film', 'Sachet film 320 mm', 'Fillers F1 – F10', '52 rolls', '34 rolls/day', 36, 24, '1.5 days', '', '70 rolls', 'Roll · 25 kg', 'FILM-320', [120, 110, 98, 88, 80, 72, 64, 58, 52]),
  ('cf5', 'Cartridge filter 5 µm', 'CF-201 · ΔP 0.6 of 1.0 bar', '9 days old', '—', 504, 72, '21 days', '', '12 cartridges', 'Cartridge', 'CF-5UM-40', [0.3, 0.35, 0.38, 0.42, 0.45, 0.5, 0.53, 0.57, 0.6]),
  ('cf1', 'Cartridge filter 1 µm', 'CF-301 · ΔP 0.3 of 1.0 bar', '9 days old', '—', 504, 72, '21 days', '', '10 cartridges', 'Cartridge', 'CF-1UM-40', [0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.25, 0.27, 0.3]),
  ('uv', 'UV lamp', 'UV-301 · 96% intensity', '6,920 h', '24 h/day', 2088, 720, '87 days', '', '1 spare', 'Lamp', 'UV-LAMP-55W', [99, 99, 98, 98, 97, 97, 97, 96, 96]),
]
rows = []
for k, n, w, oh, rate, hrs, reorder, run, warn, stock, *_ in items:
    pct = min(hrs/(reorder*3) * 100, 100)
    rc = 'color:var(--ink-amber-8);font-weight:500' if warn else 'color:var(--ink-gray-8)'
    reo = f'{reorder} h' if reorder < 200 else f'{reorder//24} days'
    rows.append(f'''<div class="lr {{{{cls_rsel__{k}}}}}" role="button" tabindex="0" onClick="{{{{set_rsel__{k}}}}}" style="{C};min-height:56px;cursor:pointer"><span class="c"><div class="t1">{n}</div><div class="m">{w}</div></span><span class="tab">{oh}</span><span class="tab qs" style="color:var(--ink-gray-7)">{rate}</span><span class="tab qs" style="color:var(--ink-gray-7)">{reo}</span>
<span style="display:flex;flex-direction:column;gap:6px;min-width:0"><span class="tab" style="{rc}">{run}</span><span class="bar"><i class="{'a' if warn else ''}" style="width:{pct:.0f}%"></i></span></span><span class="qs c">{stock}</span></div>''')
table = f'''<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><div style="display:flex;gap:8px;align-items:center"><h2 class="h2">Consumables</h2>{bd("3 under reorder point","amber")}</div><span class="qs">Stock from ERPNext · Koyo 1 · Stores</span></div>
<div class="list"><div class="lh" style="{C}"><span>Item</span><span>On hand</span><span>Use rate</span><span>Reorder at</span><span>Runway</span><span>In store</span></div>{''.join(rows)}</div>
<p class="qs" style="margin:0">Click an item for its details. Runway uses the last 24 h of use.</p></section>'''

# ---------- detail panel (one per selectable thing)
def kv(rows_):
    return '<div style="display:flex;flex-direction:column">' + ''.join(f'<div style="display:grid;grid-template-columns:120px minmax(0,1fr);gap:8px;padding:8px 0;border-bottom:1px solid var(--outline-gray-1);font-size:14px"><span class="qs">{a}</span><span style="color:var(--ink-gray-8)">{b}</span></div>' for a, b in rows_) + '</div>'
def phead(title, sub, badge=''):
    return f'<div style="display:flex;flex-direction:column;gap:6px;padding:16px 16px 4px"><div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><h2 class="h2" style="margin:0">{title}</h2>{badge}</div><span class="qs">{sub}</span></div>'
def pfoot(*btns):
    return f'<div style="padding:12px 16px;border-top:1px solid var(--outline-gray-1);display:flex;gap:8px;flex-wrap:wrap">{"".join(btns)}</div>'
def pane(key, inner):
    return f'<sc-if value="{{{{is_rsel__{key}}}}}" hint-placeholder-val="{{{{ {"true" if key == "anti" else "false"} }}}}"><div style="display:flex;flex-direction:column;flex:1;min-height:0"><div style="flex:1;overflow:auto">{inner[0]}</div>{inner[1]}</div></sc-if>'

panes = ''
for k, n, w, oh, rate, hrs, reorder, run, warn, stock, unit, code, hist in items:
    lo, hi = min(hist), max(hist)
    chart = spark(hist, 286, 64, 'var(--ink-gray-8)', lo - (hi - lo) * .2, hi + (hi - lo) * .2)
    is_filter = k in ('cf5', 'cf1')
    life = k in ('cf5', 'cf1', 'uv')
    big = f'<div style="display:flex;flex-direction:column;gap:2px"><span class="qs">{"Replace in" if life else "Runs out in"}</span><span class="tab" style="font-size:28px;font-weight:600;color:{"var(--ink-amber-7)" if warn else "var(--ink-gray-9)"}">{run}</span></div>'
    hist_label = 'ΔP across the filter · last 9 days' if is_filter else ('Lamp intensity · last 9 days' if k == 'uv' else 'On hand · last 9 days')
    body_ = f'''{phead(n, w, bd("Under reorder point", "amber") if warn else "")}
<div style="padding:12px 16px;display:flex;flex-direction:column;gap:16px">{big}
<div class="inset" style="display:flex;flex-direction:column;gap:6px"><span class="qs">{hist_label}</span>{chart}</div>
{kv([("On hand", oh), ("Use rate", rate), ("Reorder at", f"{reorder} h of runway" if reorder < 200 else f"{reorder // 24} days left"), ("In store", stock), ("Pack", unit), ("ERPNext item", f'<span class="tab">{code}</span>'), ("Warehouse", "Koyo 1 · Stores")])}
<div class="qs" style="line-height:1.5">{"Replaced when ΔP reaches 1.0 bar or after 30 days. Replacing logs a Stock Entry and resets the counter." if is_filter else ("Replaced at 9,000 h or under 90% intensity." if k == "uv" else "Use rate comes from the dosing pump stroke counter, checked against tank level each shift.")}</div></div>'''
    foot = pfoot(f'<button type="button" class="btn">{ic("package")}{"Request" if warn or not life else "Order spare"}</button>', btn('Log a refill' if not life else 'Log replacement'), btn('Open in ERPNext', 'ext', 'ghost'))
    panes += pane(k, (body_, foot))

# generator and its diesel day tank
lv = [62,58,54,50,46,42,38,34,30,90,86,82,78,74,70,66,62,58,54,50,46,42,38,34,30,28]
dchart = spark(lv, 286, 64, 'var(--ink-gray-8)', 0, 100, lines=((25, 'var(--ink-amber-7)'),))
def day_tank(pct, cap):
    w, h = 280, 120; lvl = h * pct / 100
    re_y = h - h * 0.25
    return (f'<svg width="100%" viewBox="0 0 {w+20} {h+36}" role="img" aria-label="Diesel tank {pct}%"><rect x="10" y="10" width="{w}" height="{h}" rx="14" fill="var(--surface-gray-1)" stroke="var(--outline-gray-3)" stroke-width="1.5"/>'
            f'<clipPath id="dtc"><rect x="10" y="10" width="{w}" height="{h}" rx="14"/></clipPath><rect x="10" y="{10 + h - lvl:.1f}" width="{w}" height="{lvl:.1f}" fill="var(--surface-amber-3)" clip-path="url(#dtc)"/>'
            f'<line x1="10" x2="{w+10}" y1="{10+re_y:.1f}" y2="{10+re_y:.1f}" stroke="var(--ink-amber-7)" stroke-dasharray="4 4"/><text x="{w+6}" y="{6+re_y:.1f}" text-anchor="end" font-size="12" fill="var(--ink-amber-8)">Reorder 25%</text>'
            f'<rect x="{w-40}" y="4" width="24" height="8" rx="2" fill="var(--outline-gray-3)"/>'
            f'<text x="{10 + w/2}" y="{10 + h/2 - 4}" text-anchor="middle" font-size="26" font-weight="600" fill="var(--ink-gray-9)">{pct}%</text><text x="{10 + w/2}" y="{10 + h/2 + 18}" text-anchor="middle" font-size="13" fill="var(--ink-gray-7)">560 of {cap:,} L</text>'
            f'<text x="10" y="{h+30}" font-size="12" fill="var(--ink-gray-6)">DT-1 day tank · level from LT-901</text></svg>')
gen_body = f'''{phead('Generator · GEN-1', '120 kW diesel set · feeds the whole plant through ATS-1', bd('Running', 'amber'))}
<div style="padding:12px 16px;display:flex;flex-direction:column;gap:16px">
<div style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">Diesel tank</h3>{day_tank(28, 2000)}</div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px">
<div class="kpi"><span class="k">Runs out in</span><span class="v" style="color:var(--ink-amber-8)">41 h</span><span class="d">at today's load</span></div>
<div class="kpi"><span class="k">Burn rate</span><span class="v">13.7</span><span class="d">L/h at 78 kW</span></div></div>
<div class="inset" style="display:flex;flex-direction:column;gap:6px"><div style="display:flex;justify-content:space-between" class="qs"><span>Level · last 7 days</span><span>Refilled 18 Nov · 1,200 L</span></div>{dchart}</div>
<h3 class="h3" style="margin-top:4px">Generator</h3>
{kv([("Load", "78 kW of 120 · 65%"), ("Voltage", "415 V · 50.1 Hz"), ("Run hours", "4,812 · service at 5,000 (188 h)"), ("Coolant", "84 °C"), ("Oil pressure", "4.1 bar"), ("Read from", "Controller DSE-7320 over Modbus via OpsEdge K1")])}
<h3 class="h3" style="margin-top:4px">Refuels</h3>
{kv([("18 Nov", "1,200 L · Halima S. · DN-0219"), ("11 Nov", "1,000 L · Halima S. · DN-0204"), ("4 Nov", "1,100 L · Musa A. · DN-0191")])}
</div>'''
gen_foot = pfoot(f'<button type="button" class="btn">{ic("package")}Request diesel</button>', btn('Log a refuel'), f'<a class="btn ghost" href="Trends.dc.html">{ic("chart")}Trends</a>')
grid_body = f'''{phead('Grid', 'Utility supply through ATS-1', bd('Off', 'gray'))}
<div style="padding:12px 16px;display:flex;flex-direction:column;gap:16px">
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px">
<div class="kpi"><span class="k">Off for</span><span class="v">1 h 06 min</span><span class="d">since 07:40</span></div>
<div class="kpi"><span class="k">On today</span><span class="v">62%</span><span class="d">3 outages</span></div></div>
<div class="inset" style="display:flex;flex-direction:column;gap:8px"><span class="qs">Today · grid and generator</span>
<div style="display:flex;height:14px;border-radius:4px;overflow:hidden"><i style="flex:22;background:var(--ink-gray-7)"></i><i style="flex:3;background:var(--ink-amber-6, var(--ink-amber-7))"></i><i style="flex:18;background:var(--ink-gray-7)"></i><i style="flex:6;background:var(--ink-amber-7)"></i><i style="flex:4;background:var(--ink-gray-7)"></i><i style="flex:13;background:var(--ink-amber-7)"></i><i style="flex:34;background:var(--surface-gray-2)"></i></div>
<div style="display:flex;gap:14px" class="qs"><span style="display:flex;align-items:center;gap:6px"><i style="width:10px;height:10px;border-radius:2px;background:var(--ink-gray-7)"></i>Grid</span><span style="display:flex;align-items:center;gap:6px"><i style="width:10px;height:10px;border-radius:2px;background:var(--ink-amber-7)"></i>Generator</span></div></div>
{kv([("Last on", "06:02 – 07:40 · 400 V · 49.8 Hz"), ("Energy today", "212 kWh from grid · meter EM-1"), ("Switch-over", "ATS-1 · 8 s gap · fillers paused, not tripped"), ("Read from", "ATS-1 position input DI 0.4 and meter EM-1 over Modbus")])}
<div class="qs" style="line-height:1.5">Each change of source is logged with its time. A gap longer than the fillers' ride-through is recorded as a Power dip stop.</div>
</div>'''
grid_foot = pfoot(f'<a class="btn" href="Downtime.dc.html">{ic("clock")}Power dips in downtime</a>')
panes += pane('gen', (gen_body, gen_foot)) + pane('grid', (grid_body, grid_foot))

panel = f'<aside class="panel" aria-label="Details" style="flex-basis:22rem;width:22rem">{sdef("rsel","anti")}{panes}</aside>'
css = '.lr.on{background:var(--surface-gray-2)}.rtile.on{background:var(--surface-gray-2)}.rtile:hover{background:var(--surface-gray-1)}'
body = f'<div style="display:flex;flex:1;min-height:0"><div class="body" style="overflow:auto;flex:1;min-width:0"><div style="display:flex;flex-direction:column;gap:12px">{tanks}{energy}</div>{table}</div>{panel}</div>'
write('Resources.dc.html', page('Resources', shell('Resources.dc.html', head, body), {"$preview": {"width": 1440, "height": 900}}, helmet_extra=css))
