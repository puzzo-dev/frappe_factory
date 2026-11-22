"""Plant screens for three other industries (rice, oil, poultry), drawn from the same symbol library and the same
plant-screen template as Koyo 1: proof that the app is not tied to water."""
from ff import *
import symbols as S
import symbols_ind as I

S_ = 1.25  # symbol scale on the mimic

def put(svg, x, y, label, value='', s=S_, warn=None):
    w = 48 * s
    lab = f'<text x="{x+w/2:.0f}" y="{y+w+14:.0f}" text-anchor="middle" font-size="11" font-weight="500" fill="var(--ink-gray-8)">{label}</text>'
    if value:
        col = 'var(--ink-amber-7)' if warn == 'amber' else ('var(--ink-red-7)' if warn == 'red' else 'var(--ink-gray-5)')
        lab += f'<text x="{x+w/2:.0f}" y="{y+w+27:.0f}" text-anchor="middle" font-size="10" fill="{col}">{value}</text>'
    mark = ''
    if warn in ('amber', 'red'):
        c = 'oklch(0.723 0.152 71.82)' if warn == 'amber' else 'oklch(0.556 0.198 26.552)'
        mark = f'<g transform="translate({x+w-4:.0f} {y-4:.0f})"><polygon points="7,0 14,7 7,14 0,7" fill="{c}"/><text x="7" y="10.5" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">{"3" if warn=="amber" else "2"}</text></g>'
    return f'<g transform="translate({x} {y}) scale({s})">{svg}</g>{lab}{mark}'

def pipe(d, run=True):
    base = f'<path d="{d}" fill="none" stroke="var(--outline-gray-3)" stroke-width="3" stroke-linejoin="round"/>'
    flow = f'<path d="{d}" fill="none" stroke="var(--ink-gray-6)" stroke-width="1.5" class="flow" stroke-linejoin="round"/>' if run else ''
    return base + flow

def plant_screen(name, ini, href, area, status, pins, mimic_svg, legend_note, alarms, runway, shift, layout_href='LayoutEditor.dc.html', more_counts=None):
    st_word, st_bd, st_bg, st_border, st_msg = status
    pin_html = ''.join(
        f'<div class="card" style="padding:12px 14px;display:flex;flex-direction:column;gap:4px;{"border-color:var(--outline-amber-3)" if w else ""}"><span class="qs" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{n}</span><span class="tab" style="font-size:20px;font-weight:600;color:{"var(--ink-amber-7)" if w else "var(--ink-gray-9)"}">{v} <small style="font-size:13px;font-weight:400;color:var(--ink-gray-5)">{u}</small></span><span class="qs" style="font-size:12px">{m}</span></div>'
        for n, v, u, m, w in pins)
    al_html = ''.join(
        f'<div style="display:flex;gap:10px;align-items:flex-start;padding:10px 0;border-top:1px solid var(--outline-gray-1)"><svg width="18" height="18" viewBox="0 0 18 18" style="flex:0 0 18px;margin-top:1px" aria-label="Priority {p}"><polygon points="9,0 18,9 9,18 0,9" fill="{c}"/><text x="9" y="13" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">{p}</text></svg><div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:4px"><span style="color:var(--ink-gray-8)">{t}</span><span class="qs">{m}</span></div>{btn("Acknowledge", kind="xs")}</div>'
        for p, c, t, m in alarms)
    rw_html = ''.join(
        f'<div style="display:flex;flex-direction:column;gap:6px"><div style="display:flex;justify-content:space-between;font-size:13px"><span style="color:var(--ink-gray-7)">{n}</span><span class="tab" style="font-weight:500;color:{"var(--ink-amber-7)" if w else "var(--ink-gray-8)"}">{v}</span></div><span class="bar"><i class="{"a" if w else ""}" style="width:{p}"></i></span></div>'
        for n, v, p, w in runway)
    head = header(crumb(('Plants', 'Plants.dc.html'), (name, href)) .replace('</div>', f'<span class="sep" aria-hidden="true">/</span><button type="button" class="btn ghost" style="font:600 18px Inter,sans-serif;color:var(--ink-gray-9);padding:0 6px">{area}{ic("chev-d")}</button></div>', 1),
                  f'<span class="bd gray"><span class="dot g"></span>Live · 2 s</span><a href="{layout_href}" class="btn">{ic("pen")}Edit layout</a>')
    body = f'''<div class="body">
<div class="alert" style="align-items:center;background:{st_bg};border-color:{st_border}">{bd(st_word, st_bd)}<span style="font-size:14px;color:var(--ink-gray-8)">{st_msg}</span></div>
<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h2">Pinned tags</h2><a href="PinnedTags.dc.html" style="font-size:13px">Edit pinned tags</a></div>
<div style="display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px">{pin_html}</div></section>
<div style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:20px;align-items:start">
<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><div style="display:flex;gap:8px;align-items:baseline"><h2 class="h2">Layout</h2><span class="qs">{legend_note}</span></div>
<div style="display:flex;gap:14px" class="qs"><span style="display:inline-flex;align-items:center;gap:6px"><i style="width:10px;height:10px;border-radius:50%;background:var(--ink-gray-6)"></i>Running</span><span style="display:inline-flex;align-items:center;gap:6px"><i style="width:10px;height:10px;border-radius:50%;border:1.5px solid var(--ink-gray-5)"></i>Stopped</span><span style="display:inline-flex;align-items:center;gap:6px"><i style="width:10px;height:10px;border-radius:50%;border:1.5px solid var(--ink-red-7)"></i>Fault</span></div></div>
<div class="card" style="background:var(--surface-gray-1);padding:12px">{mimic_svg}</div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px">{"".join(f'<div class="kpi"><span class="k">{k}</span><span class="v" style="font-size:18px">{v}</span><span class="d">{d}</span></div>' for k, v, d in shift)}</div></section>
<aside style="display:flex;flex-direction:column;gap:24px"><section><div style="display:flex;justify-content:space-between;align-items:baseline;padding-bottom:8px"><h2 class="h2">Active alarms</h2><a href="CoAlarms.dc.html" style="font-size:13px">View all</a></div>{al_html}</section>
<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h2">Runway</h2><span class="qs">time left at current use</span></div>{rw_html}</section></aside>
</div></div>'''
    counts = {'Alarms': str(len(alarms)), 'Downtime': '1', **(more_counts or {})}
    return page(name, shell(href, head, body, plant=(ini, name), plant_href=href, counts=counts, layout_href=layout_href), {"$preview": {"width": 1440, "height": 900}})

# ------------------------------------------------------------------ Rice mill
y1, y2 = 30, 250
mid1, mid2 = y1 + 30, y2 + 30
rice = ''.join([
  pipe(f'M75 {mid1} H760'),
  pipe(f'M790 {y1+46} H815 V{y2-14} H770 V{y2+2}'),
  pipe(f'M770 {mid2} H100'),
  pipe(f'M790 {y2+12} H840'),
  pipe(f'M703 {y2+44} V370 H848 V16 H760 V{y1+2}'),
  pipe(f'M512 {y2+44} V340 H612 V{y2+44}'),
])
rice += ''.join([
  put('<path d="M6 10 h36 l-10 22 h-16 z" fill="var(--surface-base)" stroke="var(--ink-gray-6)" stroke-width="1.5"/><text x="24" y="24" text-anchor="middle" font-size="7" fill="var(--ink-gray-6)">PADDY</text>', 20, y1, 'Intake pit', '6.2 t/h'),
  put(I.bucket_elevator(), 105, y1, 'E-1'),
  put(I.pre_cleaner(), 190, y1, 'Pre-cleaner'),
  put(I.dryer(), 290, y1, 'Dryer D-1', '13.8 % out'),
  put(I.silo(0.55), 390, y1, 'S-1', '55 %', s=1.25),
  put(I.silo(0.92), 470, y1, 'S-2', '92 %', s=1.25, warn='amber'),
  put(I.bucket_elevator(), 545, y1, 'E-2'),
  put(I.destoner(), 630, y1, 'Destoner'),
  put(I.husker(), 730, y1, 'Husker H-1', '92 A'),
  put(I.cyclone(), 740, y2, 'Aspirator', 'husk 1.3 t/h'),
  put(I.paddy_separator(), 640, y2, 'Separator', 'return 8 %'),
  put(I.whitener(), 540, y2, 'Whitener W-1', '74 % load'),
  put(I.whitener(), 440, y2, 'Whitener W-2', '96 % load', warn='amber'),
  put(I.grader(), 340, y2, 'Grader'),
  put(I.color_sorter(), 240, y2, 'Color sorter', 'reject 1.1 %'),
  put(I.bagger(), 140, y2, 'Bagger B-1', '50 kg · 7/min'),
  f'<text x="40" y="{mid2+4}" text-anchor="middle" font-size="11" fill="var(--ink-gray-6)">Bags →</text>',
  f'<text x="842" y="{y2+4}" text-anchor="end" font-size="10" fill="var(--ink-gray-5)">husk to boiler</text>',
  f'<text x="562" y="354" text-anchor="middle" font-size="10" fill="var(--ink-gray-5)">bran to bran bin</text>',
  f'<text x="760" y="384" text-anchor="middle" font-size="10" fill="var(--ink-gray-5)">unhusked paddy back to husker</text>',
])
rice_svg = f'<svg viewBox="0 0 860 400" width="100%" role="img" aria-label="Rice mill line: intake, cleaning, drying, silos, destoner, husker, separator, two whiteners, grader, color sorter, bagger. All running; whitener W-2 load high." style="display:block">{rice}</svg>'

write('RiceMill.dc.html', plant_screen(
  'Rice mill', 'RM', 'RiceMill.dc.html', 'Milling line',
  ('Running', 'green', 'var(--surface-green-2)', 'var(--outline-green-3)', 'All 16 machines running. Whitener W-2 is near full load; head rice yield is in band.'),
  [('Paddy intake', '6.2', 't/h', 'Plan 6.0', False), ('Head rice yield', '64.5', '%', 'Band 62–68', False), ('Broken', '7.8', '%', 'Alert above 10', False),
   ('Dryer outlet moisture', '13.8', '%', 'Band 13–14.5', False), ('W-2 motor load', '96', '%', 'Alert above 95', True), ('Husk to boiler', '1.3', 't/h', 'Fuel for D-1', False)],
  rice_svg, 'Rice mill v2 · 16 symbols from the rice milling pack',
  [('3', 'oklch(0.723 0.152 71.82)', 'Whitener W-2 load high', '96 % · since 07:58'), ('3', 'oklch(0.723 0.152 71.82)', 'Silo S-2 nearly full', '92 % · switch intake to S-1')],
  [('Paddy in silos', '9.5 h', '62%', False), ('50 kg bags', '1.8 days', '45%', False), ('Diesel', '33 h', '24%', True)],
  [('Milled rice this shift', '21.6 t', 'of 30 t planned'), ('Uptime this shift', '96%', '1 stop · 9 min'), ('Production run', 'RUN-0233', 'Parboiled long grain')], 'LayoutRice.dc.html'))

# ------------------------------------------------------------------ Oil mill
y1, y2 = 30, 250
mid1, mid2 = y1 + 30, y2 + 30
oil = ''.join([
  pipe(f'M75 {mid1} H300'),
  pipe(f'M318 {mid1-6} H330 V22 H535 M365 22 V38 M450 22 V38 M535 22 V38'),
  pipe(f'M405 {y1+26} H640 M490 {y1+26} H500 M575 {y1+26} H640'),
  pipe(f'M354 {y1+44} V150 M439 {y1+44} V150 M354 150 H439 M354 150 H40 V{mid2+12} H74'),
  pipe(f'M524 {y1+44} V150 H439', run=False),
  pipe(f'M130 {mid2+10} H700'),
])
oil += ''.join([
  put(I.silo(0.7), 20, y1, 'Seed silo', '70 %'),
  put(I.bucket_elevator(), 100, y1, 'E-1'),
  put(I.pre_cleaner(), 175, y1, 'Cleaner'),
  put(I.cooker(), 255, y1, 'Cooker', '105 °C'),
  put(I.expeller(), 350, y1, 'EX-1', '31 A'),
  put(I.expeller(), 435, y1, 'EX-2', '30 A'),
  put(I.expeller(False, True), 520, y1, 'EX-3', 'tripped', warn='red'),
  put(I.screw_conveyor(), 640, y1, 'Cake to store', '1.9 t/h'),
  put(S.tank_v(0.45), 70, y2, 'Crude oil', '45 %'),
  put(I.filter_press(), 150, y2, 'Filter press'),
  put(I.reactor(), 240, y2, 'Neutralizer'),
  put(I.reactor(), 330, y2, 'Bleacher'),
  put(I.heat_exchanger(), 420, y2, 'Heater', '238 °C'),
  put(I.column(), 510, y2, 'Deodorizer', '240 °C · 3 mbar'),
  put(S.tank_v(0.62), 600, y2, 'Refined oil', '62 %'),
  put(I.bottle_filler(), 700, y2, 'Bottling', '1 L · 42/min'),
  f'<text x="200" y="144" text-anchor="middle" font-size="10" fill="var(--ink-gray-5)">crude oil to tank</text>',
])
oil_svg = f'<svg viewBox="0 0 860 400" width="100%" role="img" aria-label="Edible oil line: seed silo, elevator, cleaner, cooker, three expellers, crude oil tank, filter press, neutralizer, bleacher, heater, deodorizer, refined tank, bottling. Expeller EX-3 tripped on overload." style="display:block">{oil}</svg>'

write('OilMill.dc.html', plant_screen(
  'Oil mill', 'OM', 'OilMill.dc.html', 'Pressing and refining',
  ('Alert', 'amber', 'var(--surface-amber-2)', 'var(--outline-amber-3)', 'Expeller EX-3 tripped on motor overload at 07:41. EX-1 and EX-2 carry the line at 67 % of seed rate.'),
  [('Seed feed', '2.7', 't/h', 'Plan 4.1 with 3 expellers', True), ('Oil yield', '31.2', '%', 'Of seed weight', False), ('Cooker', '105', '°C', 'Band 100–110', False),
   ('Deodorizer', '240', '°C', '3 mbar vacuum', False), ('Refined FFA', '0.05', '%', 'Spec under 0.1', False), ('Refined oil tank', '62', '%', '18.6 of 30 t', False)],
  oil_svg, 'Oil mill v1 · 16 symbols from the edible oil pack',
  [('2', 'oklch(0.556 0.198 26.552)', 'Expeller EX-3 overload trip', '48 A against 40 A · 07:41'), ('3', 'oklch(0.723 0.152 71.82)', 'Seed feed below plan', '2.7 of 4.1 t/h · since 07:42')],
  [('Seed in silo', '1.9 days', '70%', False), ('Bleaching earth', '26 h', '30%', True), ('1 L bottles', '3.2 days', '64%', False)],
  [('Oil this shift', '6.1 t', 'of 8.4 t planned'), ('Uptime this shift', '88%', 'EX-3 down 1 h 05 min'), ('Production run', 'RUN-0118', 'Refined soybean oil')], 'LayoutOil.dc.html'))

# ------------------------------------------------------------------ Poultry farm (layers)
HX = [20, 230, 440, 650]; HY, HW, HH = 136, 190, 116
houses = [('H1', '5,000 birds', '24.6 °C', 'RH 62 % · NH₃ 8 ppm', 'Lay 91 %', 'ok'),
          ('H2', '5,000 birds', '25.1 °C', 'RH 64 % · NH₃ 9 ppm', 'Lay 89 %', 'ok'),
          ('H3', '4,960 birds', '31.8 °C', 'RH 71 % · NH₃ 14 ppm', 'Lay 84 %', 'hot'),
          ('H4', 'Empty', 'Cleaning', 'Flock out 14 Nov', 'Next flock 1 Dec', 'off')]
def house(x, tag, birds, temp, env, lay, st):
    run = st != 'off'
    edge = 'var(--ink-amber-7)' if st == 'hot' else 'var(--ink-gray-6)'
    tcol = 'var(--ink-amber-7)' if st == 'hot' else ('var(--ink-gray-5)' if st == 'off' else 'var(--ink-gray-9)')
    o = f'<rect x="{x}" y="{HY}" width="{HW}" height="{HH}" rx="6" fill="var(--surface-base)" stroke="{edge}" stroke-width="{2 if st=="hot" else 1.5}"/>'
    o += f'<text x="{x+10}" y="{HY+18}" font-size="12" font-weight="600" fill="var(--ink-gray-9)">{tag}</text><text x="{x+32}" y="{HY+18}" font-size="10" fill="var(--ink-gray-5)">{birds}</text>'
    o += f'<text x="{x+HW-10}" y="{HY+18}" text-anchor="end" font-size="12" font-weight="600" fill="{tcol}">{temp}</text>'
    o += f'<g transform="translate({x+4} {HY+30}) scale(0.9)">{I.cooling_pad(run and st=="hot")}</g>'
    o += f'<g transform="translate({x+48} {HY+22}) scale(1.9 0.8)">{I.feeder_line(run)}</g>'
    o += f'<g transform="translate({x+48} {HY+52}) scale(1.9 0.8)">{I.drinker_line(run)}</g>'
    o += f'<g transform="translate({x+HW-26} {HY+28}) scale(0.48)">{I.exhaust_fan(run)}</g><g transform="translate({x+HW-26} {HY+54}) scale(0.48)">{I.exhaust_fan(run and st=="hot")}</g>'
    o += f'<text x="{x+10}" y="{HY+HH-22}" font-size="10" fill="var(--ink-gray-6)">{env}</text><text x="{x+10}" y="{HY+HH-8}" font-size="10" fill="var(--ink-gray-6)">{lay}</text>'
    fans = '6 of 6 fans · pad on' if st == 'hot' else ('fans off' if st == 'off' else '2 of 6 fans')
    o += f'<text x="{x+HW-10}" y="{HY+HH-8}" text-anchor="end" font-size="10" fill="{"var(--ink-amber-7)" if st=="hot" else "var(--ink-gray-5)"}">{fans}</text>'
    if st == 'hot':
        o += f'<g transform="translate({x+HW-8} {HY-8})"><polygon points="7,0 14,7 7,14 0,7" fill="oklch(0.723 0.152 71.82)"/><text x="7" y="10.5" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">2</text></g>'
    return o
poul = ''.join([
  pipe('M75 50 H100 M135 50 H180 M235 50 H262 M318 50 H340'),
  pipe('M383 44 H410 V110 H560'),
  pipe('M115 110 H410'),
  pipe('M560 110 H745', run=False),
  ''.join(pipe(f'M{x+95} 110 V{HY}') for x in HX[:3]),
  pipe(f'M{HX[3]+95} 110 V{HY}', run=False),
  pipe('M548 50 H600 M630 50 H680 M712 50 H780 V123 H105'),
  ''.join(pipe(f'M{x+120} 123 V{HY}') for x in HX[:3]),
  ''.join(pipe(f'M{x+95} {HY+HH} V312') for x in HX[:3]),
  pipe('M115 312 H560'),
  pipe('M620 312 H650 M710 312 H740'),
])
poul += ''.join(house(x, *h) for x, h in zip(HX, houses))
poul += ''.join([
  put(I.silo(0.42), 20, 20, 'Maize silo', '42 %', s=1.15),
  put(I.bucket_elevator(), 85, 20, 'E-1', s=1.15),
  put(I.hammer_mill(), 165, 20, 'Hammer mill', '1.8 t/h', s=1.15),
  put(I.ribbon_mixer(), 245, 20, 'Mixer', 'batch 4 of 6', s=1.15),
  put(I.silo(0.18), 330, 14, 'Feed bin FB-1', '18 %', s=1.15, warn='amber'),
  put(S.tank_v(0.66), 490, 20, 'Water T1', '66 %', s=1.15),
  put(S.dosing(), 575, 20, 'Medicator', 'vitamins', s=1.15),
  put(S.pump(True), 655, 20, 'P-1', '3.1 m³/h', s=1.15),
  put(I.egg_grader(), 560, 282, 'Egg grader', '3,240 eggs/h', s=1.25),
  put(I.egg_packer(), 650, 282, 'Packer', 'trays of 30', s=1.25),
  put(I.cold_room(), 740, 282, 'Cold room', '12 °C', s=1.25),
  f'<text x="800" y="113" text-anchor="start" font-size="10" fill="var(--ink-gray-5)">feed</text>',
  f'<text x="800" y="127" text-anchor="start" font-size="10" fill="var(--ink-gray-5)">water</text>',
  f'<text x="440" y="306" text-anchor="middle" font-size="10" fill="var(--ink-gray-5)">egg belts to the cross conveyor</text>',
])
poultry_svg = f'<svg viewBox="0 0 860 390" width="100%" role="img" aria-label="Layer farm: maize silo, elevator, hammer mill, mixer and feed bin feed four layer houses by auger; water tank, medicator and pump feed the drinker lines; egg belts run to the grader, packer and cold room. House H3 is hot at 31.8 °C; H4 is empty for cleaning." style="display:block">{poul}</svg>'

write('PoultryFarm.dc.html', plant_screen(
  'Poultry farm', 'PF', 'PoultryFarm.dc.html', 'Layer houses and egg room',
  ('Alert', 'amber', 'var(--surface-amber-2)', 'var(--outline-amber-3)', 'House H3 is at 31.8 °C with all 6 tunnel fans and the cooling pad on. Heat stress cuts lay rate: check the pad pump and drinker flow.'),
  [('Eggs so far today', '9,870', 'eggs', '329 trays of 30', False), ('Lay rate', '88.4', '%', '14,960 birds in lay', False), ('H3 temperature', '31.8', '°C', 'Alert above 30', True),
   ('H3 ammonia', '14', 'ppm', 'Alert above 25', False), ('Feed per bird', '112', 'g/day', 'Band 105–120', False), ('Water per bird', '228', 'ml/day', 'About 2× feed', False)],
  poultry_svg, 'Layer farm v1 · 22 symbols from the poultry pack',
  [('2', 'oklch(0.723 0.152 71.82)', 'H3 temperature high', '31.8 °C · alert at 30 · since 08:05'), ('3', 'oklch(0.723 0.152 71.82)', 'Feed bin FB-1 low', '18 % · mixer batch 4 of 6 running')],
  [('Feed in bin', '7 h', '18%', True), ('Maize in silo', '4.2 days', '42%', False), ('Egg trays', '2.5 days', '50%', False), ('Diesel', '52 h', '48%', False)],
  [('Eggs this shift', '9,870', '329 trays of 30'), ('Mortality today', '3 birds', '0.02 % of the flock'), ('Feed used today', '1.1 t', 'of 1.7 t planned')], 'LayoutPoultry.dc.html', {'Quality holds': '1'}))
