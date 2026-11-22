"""Layout editors for the rice mill, oil mill and poultry farm: the same editor as Koyo 1,
opened on each plant's own layout with its industry pack in the palette."""
from ff import *
import symbols as S
import symbols_ind as I
import s_industry as SI
from s_layout import editor

def sel_box(svg, x, y, w, h, label):
    hs = ''.join(f'<rect x="{px-3.5}" y="{py-3.5}" width="7" height="7"/>' for px, py in
                 [(x, y), (x+w/2, y), (x+w, y), (x, y+h/2), (x+w, y+h/2), (x, y+h), (x+w/2, y+h), (x+w, y+h)])
    lw = 8 + len(label) * 6.4
    ov = (f'<g aria-label="Selected {label}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="var(--ink-blue-7)" stroke-width="1.25"/>'
          f'<g fill="var(--surface-base)" stroke="var(--ink-blue-7)" stroke-width="1.25">{hs}</g>'
          f'<rect x="{x}" y="{y+h+8}" width="{lw:.0f}" height="20" rx="4" fill="var(--ink-blue-7)"/><text x="{x+lw/2:.0f}" y="{y+h+22}" text-anchor="middle" font-size="11" font-weight="500" fill="#fff">{label}</text></g>')
    return svg.replace('</svg>', ov + '</svg>')

GEN = [('Handling', [(n, f()) for n, f in I.GENERAL[:5]]),
       ('Utilities', [('Fan', I.fan()), ('Vertical tank', S.tank_v(0.6)), ('Centrifugal pump', S.pump(True)), ('Generator', S.generator())]),
       ('Instruments', [('Analyser', S.analyser()), ('Level', S.level()), ('Flow meter', S.flow())])]
OK = lambda n: f'<span style="color:var(--ink-green-7);display:flex">{ic("check","i s35")}</span><span style="color:var(--ink-gray-8)">No problems</span><span class="qs">{n} symbols bound</span>'

editor('LayoutRice.dc.html', [('Rice milling', [(n, f()) for n, f in I.RICE])] + GEN,
       sel_box(SI.rice_svg, 436, 246, 68, 68, 'W-2 · whitener'), I.whitener(), 'W-2', 'Whitener · rice pack v2', 'W-2 · Whitener 2',
       [('running', 'PLC-R1 · W2.RUN', 'bool', True, 'On'), ('load', 'PLC-R1 · W2.LOAD', 'number · %', True, '96'), ('fault', 'PLC-R1 · W2.TRIP', 'bool', True, 'Off')],
       'Milling line', 'Rice mill', 'RiceMill.dc.html', 'Draft · v3', 'Live: v2', 31, OK(16),
       dict(plant=('RM', 'Rice mill'), plant_href='RiceMill.dc.html', counts={'Alarms': '2'}, layout_href='LayoutRice.dc.html'), top=110, pos=('440','250'))

editor('LayoutOil.dc.html', [('Edible oil', [(n, f()) for n, f in I.OIL])] + GEN,
       sel_box(SI.oil_svg, 516, 26, 68, 68, 'EX-3 · expeller'), I.expeller(False, True), 'EX-3', 'Expeller · oil pack v1', 'EX-3 · Screw press 3',
       [('running', 'PLC-O1 · EX3.RUN', 'bool', True, 'Off'), ('current', 'PLC-O1 · EX3.AMPS', 'number · A', True, '0'), ('fault', 'PLC-O1 · EX3.OL', 'bool', True, 'On')],
       'Pressing and refining', 'Oil mill', 'OilMill.dc.html', 'Draft · v2', 'Live: v1', 30, OK(16),
       dict(plant=('OM', 'Oil mill'), plant_href='OilMill.dc.html', counts={'Alarms': '2'}, layout_href='LayoutOil.dc.html'), top=110, pos=('520','30'))

editor('LayoutPoultry.dc.html', [('Poultry farm', [(n, f()) for n, f in I.POULTRY])] + GEN,
       sel_box(SI.poultry_svg, 436, 132, 198, 124, 'H3 · layer house'), I.poultry_house(), 'H3', 'Layer house · poultry pack v1', 'H3 · Layer house 3',
       [('temperature', 'EDGE-P1 · H3.TEMP', 'number · °C', True, '31.8'), ('humidity', 'EDGE-P1 · H3.RH', 'number · %', True, '71'),
        ('ammonia', 'EDGE-P1 · H3.NH3', 'number · ppm', True, '14'), ('fans running', 'EDGE-P1 · H3.FANS', 'number', True, '6'), ('pad pump', '', 'bool', False)],
       'Layer houses and egg room', 'Poultry farm', 'PoultryFarm.dc.html', 'Draft · v2', 'Live: v1', 35,
       '<span style="color:var(--ink-amber-7);display:flex">' + ic("alert-t","i s35") + '</span><span style="color:var(--ink-gray-8)">1 problem</span><span class="qs">H3 pad pump not bound</span>',
       dict(plant=('PF', 'Poultry farm'), plant_href='PoultryFarm.dc.html', counts={'Alarms': '2', 'Downtime': '1', 'Quality holds': '1'}, layout_href='LayoutPoultry.dc.html'), top=110, pos=('440','136'))
