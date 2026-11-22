"""Koyo 1 · Utilities · power layout: grid incomer, meter, ATS, generator and its day tank, distribution boards."""
import symbols as S
from ff import *
from s_layout import editor, place, P, T, bind, KOYO_LAYOUTS

A = 'fill="none" stroke="var(--ink-amber-7)" stroke-width="2"'   # live path (on generator)
D = 'fill="none" stroke="var(--outline-gray-3)" stroke-width="1.5" stroke-dasharray="4 4"'  # dead path (grid off)
pipes = f'''
<path d="M72 96 H150" {D}/><path d="M178 96 H390 V162 H362" {D}/>
<path d="M108 308 H206" {P}/><path d="M238 300 H300 V162 H337" {A}/>
<path d="M350 222 V256 M350 256 H620 M420 256 V302 M520 256 V302 M620 256 V302" {A}/>
'''
syms = ''.join([
  place(S.grid_in(), 36, 72, 1.0, 'Grid', 'Off since 07:40'),
  place(S.meter(), 140, 72, 1.0, 'EM-1', '0 kW'),
  place(S.ats(True), 316, 140, 1.4, 'ATS-1', 'On generator'),
  place(S.tank_h(), 40, 274, 1.4, 'DT-1 · diesel', '28% · 560 L'),
  place(S.generator(), 196, 276, 1.0, 'GEN-1', '78 kW · running'),
  place(S.db(), 396, 296, 1.0, 'DB-RO', 'RO and pumps'), place(S.db(), 496, 296, 1.0, 'DB-FILL', 'Fillers F1 – F10'), place(S.db(), 596, 296, 1.0, 'DB-AUX', 'Lights, office, UV'),
  place(S.level(), 56, 210, 0.9), T(110, 238, 'LT-901', 11, 500, anchor='start'), T(110, 251, 'Diesel level', 10, 400, 'var(--ink-gray-5)', 'start'),
  T(380, 30, 'Utilities · power', 13, 600), T(380, 47, 'Amber is the live path. Dashed is dead.', 11, 400, 'var(--ink-gray-5)'),
])
SEL = '''<g aria-label="Selected ATS-1">
<rect x="312" y="136" width="75" height="75" fill="none" stroke="var(--ink-blue-7)" stroke-width="1.25"/>
<g fill="var(--surface-base)" stroke="var(--ink-blue-7)" stroke-width="1.25"><rect x="308.5" y="132.5" width="7" height="7"/><rect x="383.5" y="132.5" width="7" height="7"/><rect x="308.5" y="207.5" width="7" height="7"/><rect x="383.5" y="207.5" width="7" height="7"/></g>
<rect x="402" y="132" width="84" height="20" rx="4" fill="var(--ink-blue-7)"/><text x="444" y="146" text-anchor="middle" font-size="11" font-weight="500" fill="#fff">ATS-1 · switch</text></g>'''
canvas_svg = f'<svg viewBox="0 0 800 440" width="100%" role="img" aria-label="Utilities layout: grid, ATS, generator and diesel tank" style="display:block">{pipes}{syms}{SEL}</svg>'
cats = [
  ('Power', [('Grid incomer', S.grid_in()), ('Energy meter', S.meter()), ('Breaker', S.breaker()), ('Changeover · ATS', S.ats()), ('Generator', S.generator()), ('Distribution board', S.db())]),
  ('Fuel', [('Day tank', S.tank_h()), ('Level', S.level()), ('Flow meter', S.flow())]),
]
editor('LayoutUtilities.dc.html', cats, canvas_svg, S.ats(True), 'ATS-1', 'Changeover switch · v1', 'ATS-1 · Changeover switch',
       [('on_generator', 'PLC-1 · DI 0.4 · ATS.GEN', 'bool', True, 'On'), ('grid_ok', 'EM-1 · voltage present', 'bool', True, 'Off'), ('gen_ok', 'DSE-7320 · breaker closed', 'bool', True, 'On')],
       'Utilities · power', 'Koyo 1', 'Main.dc.html', 'Draft · v2', 'Live: v1', 9,
       '<span style="color:var(--ink-green-7);display:flex">' + ic("check","i s35") + '</span><span style="color:var(--ink-gray-8)">No problems</span><span class="qs">The source shown on Resources comes from ATS-1</span>',
       {}, pos=('316', '140'), layouts=KOYO_LAYOUTS, feeds='<span class="chip" style="height:20px">DB-RO</span> <span class="chip" style="height:20px">DB-FILL</span> <span class="chip" style="height:20px">DB-AUX</span>')
