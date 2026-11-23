from ff import *
import symbols as S
import symbols_ind as I

head = header(crumb(('Plants', 'Plants.dc.html'), ('New plant', None)), f'{btn("Cancel", kind="ghost")}')

def steps():
    items = [('Details', 'done'), ('Industry', 'now'), ('Edge box', 'todo'), ('Layout', 'todo')]
    out = []
    for i, (n, st) in enumerate(items, 1):
        if st == 'done':
            mk = f'<span style="width:22px;height:22px;border-radius:50%;background:var(--surface-gray-10);color:var(--ink-base);display:grid;place-items:center">{ic("check","i s35")}</span>'
        elif st == 'now':
            mk = f'<span style="width:22px;height:22px;border-radius:50%;border:1.5px solid var(--ink-gray-9);display:grid;place-items:center;font-size:12px;font-weight:600">{i}</span>'
        else:
            mk = f'<span style="width:22px;height:22px;border-radius:50%;background:var(--surface-gray-2);color:var(--ink-gray-6);display:grid;place-items:center;font-size:12px">{i}</span>'
        col = 'var(--ink-gray-9)' if st != 'todo' else 'var(--ink-gray-5)'
        out.append(f'<div style="display:flex;align-items:center;gap:8px">{mk}<span style="font-size:14px;font-weight:{"600" if st=="now" else "400"};color:{col}">{n}</span></div>')
    return '<div style="display:flex;align-items:center;gap:12px">' + '<span style="flex:0 0 32px;height:1px;background:var(--outline-gray-2)"></span>'.join(out) + '</div>'

def strip(svgs):
    return '<div style="display:flex;align-items:center;gap:2px;height:64px;padding:0 8px;border-radius:8px;background:var(--surface-gray-1)">' + \
        '<span style="flex:0 0 6px;height:1.5px;background:var(--ink-gray-5)"></span>'.join(S.box(s, 40) for s in svgs) + '</div>'

templates = [
  ('Sachet and bottled water', 'Borehole to RO, UV, lead or quality interlocks, fillers', strip([S.tank_v(0.6), S.pump(True), S.ro(), S.uv(), S.filler(True)]), 'Koyo 1, Plant B', False),
  ('Rice milling', 'Paddy intake to drying, husking, whitening, sorting, bagging', strip([I.silo(0.6), I.husker(), I.whitener(), I.color_sorter(), I.bagger()]), 'Rice mill', True),
  ('Edible oil', 'Seed cleaning, cooking, pressing, refining, bottling', strip([I.cooker(), I.expeller(), I.filter_press(), I.column(), I.bottle_filler()]), 'Oil mill', False),
  ('Poultry farm', 'Feed mill, layer or broiler houses, climate, water, eggs', strip([I.hammer_mill(), I.poultry_house(), I.exhaust_fan(), I.egg_grader(), I.cold_room()]), 'Poultry farm', False),
  ('Start blank', 'General symbols only; add your own machines', strip([S.tank_v(0.5), I.conveyor(), I.fan(), '<rect x="6" y="12" width="36" height="24" rx="3" fill="var(--surface-base)" stroke="var(--ink-gray-6)" stroke-width="1.5" stroke-dasharray="3 2"/><text x="24" y="27" text-anchor="middle" font-size="7" fill="var(--ink-gray-6)">machine</text>']), '', False),
]
tc = ''
for name, desc, pic, used, on in templates:
    bord = 'border:1px solid var(--ink-gray-9);box-shadow:var(--shadow-sm)' if on else 'border:1px solid var(--outline-gray-2)'
    u = f'<span class="qs">Used by {used}</span>' if used else '<span class="qs">&nbsp;</span>'
    tc += f'''<label style="display:flex;flex-direction:column;gap:10px;padding:14px;border-radius:12px;{bord};cursor:pointer">
<div style="display:flex;align-items:flex-start;gap:10px"><span class="rd{" on" if on else ""}" style="margin-top:2px"></span><span style="display:flex;flex-direction:column;gap:3px;flex:1"><span style="font-weight:600;color:var(--ink-gray-9)">{name}</span><span class="qs" style="line-height:1.45">{desc}</span></span></div>
{pic}{u}</label>'''

gets = [('Symbol pack', 'Rice milling, 8 symbols, plus the 15 general ones'),
        ('Asset types', '14: pre-cleaner, destoner, husker, whitener, color sorter and more'),
        ('Tag templates', '61, e.g. motor current, roll gap, head rice yield, moisture'),
        ('Alarm definitions', '18 starter rules with cause and action filled in'),
        ('Downtime reasons', '22: roll change, screen blinding, choke, power dip'),
        ('KPIs', 'Head rice yield, broken %, milling recovery, kWh per tonne'),
        ('Starter layout', 'A milling line you rearrange to match your floor')]
gl = ''.join(f'<div style="display:grid;grid-template-columns:124px minmax(0,1fr);gap:8px;padding:8px 0;font-size:13px;line-height:1.45"><span style="color:var(--ink-gray-6)">{a}</span><span style="color:var(--ink-gray-8)">{b}</span></div>' for a, b in gets)

body = f'''<div class="body" style="max-width:1040px;margin:0 auto;width:100%;gap:24px">
{steps()}
<div style="display:flex;flex-direction:column;gap:4px"><h2 style="margin:0;font-size:20px;font-weight:600;color:var(--ink-gray-9)">What does Abuja rice mill make?</h2><p class="ps">The template fills in symbols, machines, tags, alarms and downtime reasons for that industry. You can change all of it later.</p></div>
<div style="display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:24px;align-items:start">
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px">{tc}</div>
<section class="card" style="display:flex;flex-direction:column;gap:6px"><h3 class="h3">Rice milling sets up</h3><div class="divy">{gl}</div>
<p class="qs" style="margin:6px 0 0">Templates are records (Process Template). I-Varse ships these five; a company can save any plant as its own template.</p></section>
</div>
<div style="display:flex;justify-content:space-between;padding-top:16px;border-top:1px solid var(--outline-gray-1)">{btn("Back","arrow-l")}<button type="button" class="btn solid">Continue</button></div>
</div>'''

write('AddPlant.dc.html', page('New plant', shell('AddPlant.dc.html', head, body, scope='company'), {"$preview": {"width": 1440, "height": 900}}))
