from ff import *
import math, random
random.seed(7)
N = 481  # 1-min points 00:46 -> 08:46
TRIP = 448  # 08:14
def lead(i):
    base = 1.4 + 0.15*math.sin(i/37)
    if 420 <= i <= 480:
        k = i - 420
        bump = 8.0*math.exp(-((k-28)/9.5)**2)
        return base + bump + random.uniform(-0.05, 0.05)
    return base + random.uniform(-0.08, 0.08)
def cond(i):
    v = 186 + 4*math.sin(i/53) + random.uniform(-1.2, 1.2)
    if 425 <= i <= 452: v += (i-425)*1.4
    if i > 452: v = 224 - (i-452)*1.2 if i < 480 else 190
    return v
def t4(i):
    if i < TRIP: return 1.55 + 0.25*math.sin(i/14) + random.uniform(-0.02, 0.02)
    if i < TRIP+17: return max(1.6 - (i-TRIP)*0.094, 0.02)
    return 0.02
LEAD = [lead(i) for i in range(N)]; LEAD[TRIP] = 9.4
S = [
  ('AT-401 Lead', 'µg/L', LEAD, 0, 10, 'var(--ink-gray-9)', [(8, 'Trip 8', 'var(--ink-red-7)'), (5, 'Alert 5', 'var(--ink-amber-7)')]),
  ('AT-302 Conductivity', 'µS/cm', [cond(i) for i in range(N)], 140, 240, 'oklch(0.55 0.16 252)', [(220, 'High 220', 'var(--ink-amber-7)')]),
  ('LT-401 T4 level', 'm³', [t4(i) for i in range(N)], 0, 2, 'oklch(0.55 0.15 300)', []),
]
W, L, R = 860, 48, 12
PH = 120
CUR = 439  # 08:05
def panel(name, unit, vals, lo, hi, col, lines, last):
    T, B = 8, (26 if last else 6)
    H = PH + T + B
    y = lambda v: T + PH - (v-lo)/(hi-lo)*PH
    x = lambda i: L + i*(W-L-R)/(N-1)
    pts = ' '.join(f'{x(i):.1f},{y(v):.1f}' for i, v in enumerate(vals) if i % 2 == 0 or i > 400)
    g = ''.join(f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="var(--outline-gray-1)"/><text x="{L-8}" y="{y(v)+4:.1f}" text-anchor="end" font-size="12" fill="var(--ink-gray-6)">{v:g}</text>' for v in (lo, (lo+hi)/2, hi))
    lim = ''.join(f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{c}" stroke-dasharray="4 4"/><text x="{L+6}" y="{y(v)-4:.1f}" font-size="12" fill="{c}">{t}</text>' for v, t, c in lines)
    band = f'<rect x="{x(TRIP):.1f}" y="{T}" width="{W-R-x(TRIP):.1f}" height="{PH}" fill="var(--surface-red-2)" opacity=".6"/><line x1="{x(TRIP):.1f}" x2="{x(TRIP):.1f}" y1="{T}" y2="{T+PH}" stroke="var(--ink-red-7)" stroke-width="1"/>'
    cur = f'<line x1="{x(CUR):.1f}" x2="{x(CUR):.1f}" y1="{T}" y2="{T+PH}" stroke="var(--ink-gray-6)" stroke-width="1"/><circle cx="{x(CUR):.1f}" cy="{y(vals[CUR]):.1f}" r="3.5" fill="var(--surface-base)" stroke="{col}" stroke-width="2"/>'
    ticks = ''
    if last:
        for i, lab in ((14, '01:00'), (134, '03:00'), (254, '05:00'), (374, '07:00')):
            ticks += f'<text x="{x(i):.1f}" y="{H-8}" text-anchor="middle" font-size="12" fill="var(--ink-gray-6)">{lab}</text>'
        ticks += f'<text x="{x(TRIP):.1f}" y="{H-8}" text-anchor="middle" font-size="12" font-weight="500" fill="var(--ink-red-7)">Trip 08:14</text>'
    return f'''<div style="display:flex;flex-direction:column;gap:4px"><div style="display:flex;align-items:center;gap:8px;padding-left:{L}px"><i style="width:10px;height:2px;border-radius:1px;background:{col}"></i><span style="font-size:13px;font-weight:500;color:var(--ink-gray-8)">{name}</span><span class="qs">{unit}</span></div>
<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{name} from 00:46 to 08:46" style="display:block">{band}{g}{lim}<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="1.5" stroke-linejoin="round"/>{cur}{ticks}</svg></div>'''

charts = ''.join(panel(*s, last=(k == len(S)-1)) for k, s in enumerate(S))
tip_x = L + CUR*(W-L-R)/(N-1)
tooltip = f'''<div style="position:absolute;left:calc({tip_x/W*100:.2f}% - 214px);top:44px;width:200px;padding:8px 10px;border-radius:10px;background:var(--surface-elevation-2);box-shadow:var(--shadow-2xl);font-size:13px;display:flex;flex-direction:column;gap:6px">
<span class="qs tab">22 Nov · 08:05 · 1-min avg</span>
{''.join(f'<span style="display:flex;align-items:center;gap:6px"><i style="width:8px;height:8px;border-radius:2px;background:{c}"></i><span style="flex:1;color:var(--ink-gray-7)">{n.split(" ")[0]}</span><span class="tab" style="color:var(--ink-gray-9);font-weight:500">{v[CUR]:.{2 if u=="m³" else (0 if u=="µS/cm" else 1)}f} {u}</span></span>' for n, u, v, lo, hi, c, li in S)}
</div>'''

def stats_row(n, u, v, c):
    sl = v[-60:]
    dec = 2 if u == 'm³' else (0 if u == 'µS/cm' else 1)
    f = lambda z: f'{z:.{dec}f}'
    return f'<div class="lr" style="grid-template-columns:minmax(0,1.4fr) 72px 80px 80px 80px 80px 96px;cursor:default"><span style="display:flex;align-items:center;gap:8px"><i style="width:10px;height:2px;background:{c}"></i><span class="t1">{n}</span></span><span class="qs">{u}</span><span class="r tab" style="display:flex;color:var(--ink-gray-9);font-weight:500">{f(v[-1])}</span><span class="r tab" style="display:flex">{f(min(v))}</span><span class="r tab" style="display:flex">{f(sum(v)/len(v))}</span><span class="r tab" style="display:flex">{f(max(v))}</span><span class="r tab qs" style="display:flex">481</span></div>'
stats = f'''<div class="list"><div class="lh" style="grid-template-columns:minmax(0,1.4fr) 72px 80px 80px 80px 80px 96px"><span>Tag</span><span>Unit</span><span class="r" style="display:flex">Now</span><span class="r" style="display:flex">Min</span><span class="r" style="display:flex">Average</span><span class="r" style="display:flex">Max</span><span class="r" style="display:flex">Points</span></div>{''.join(stats_row(n,u,v,c) for n,u,v,lo,hi,c,li in S)}</div>'''

groups = [
  ('Water quality', [('AT-401 Lead','µg/L',True,'var(--ink-gray-9)'),('AT-301 pH','',False,None),('AT-302 Conductivity','µS/cm',True,'oklch(0.55 0.16 252)'),('AT-303 Turbidity','NTU',False,None),('UV-301 Intensity','%',False,None)]),
  ('Levels', [('LT-101 T1 level','m³',False,None),('LT-201 T2 level','m³',False,None),('LT-401 T4 level','m³',True,'oklch(0.55 0.15 300)'),('LT-501 T5 level','m³',False,None)]),
  ('Flow and pressure', [('FT-201 Permeate flow','m³/h',False,None),('PT-201 HP pump outlet','bar',False,None),('DP-102 Carbon filter ΔP','bar',False,None)]),
  ('Fillers', [('F1 – F10 rate','sachets/h',False,None),('TT-F1 … F10 jaw temp','°C',False,None)]),
]
gl = ''
for g, tags in groups:
    gl += f'<div style="display:flex;align-items:center;justify-content:space-between;height:28px;padding:0 8px;margin-top:8px;font-size:13px;color:var(--ink-gray-6)"><span>{g}</span>{ic("chev-d","i s35")}</div>'
    for n, u, on, c in tags:
        sw = f'<i style="width:8px;height:8px;border-radius:2px;background:{c}"></i>' if on else ''
        gl += f'<label class="si" style="height:28px;cursor:pointer;font-size:13px"><span class="cb{" on" if on else ""}"></span><span class="lbl" style="color:var(--ink-gray-{"8" if on else "7"})">{n}</span>{sw}</label>'
picker = f'''<div style="flex:0 0 16rem;width:16rem;border-right:1px solid var(--outline-gray-1);display:flex;flex-direction:column;min-height:0">
<div style="padding:12px 12px 8px;display:flex;flex-direction:column;gap:8px"><span class="in muted">{ic("search")}<span class="grow">Search 64 tags</span></span><div style="display:flex;justify-content:space-between" class="qs"><span>3 of 8 on chart</span><button type="button" style="border:0;background:none;padding:0;font:inherit;color:var(--ink-blue-7);cursor:pointer">Clear</button></div></div>
<div style="flex:1;overflow:auto;padding:0 4px 16px">{gl}</div>
<div style="border-top:1px solid var(--outline-gray-1);padding:10px 12px;display:flex;flex-direction:column;gap:6px"><span class="qs">Saved views</span><span class="si" style="height:28px;font-size:13px">{ic("layers")}<span class="lbl">Lead and polishing</span></span><span class="si" style="height:28px;font-size:13px">{ic("layers")}<span class="lbl">RO health</span></span></div>
</div>'''

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Trends',None)),
  f'{btn("Save view","layers","ghost")}{btn("Export CSV","download","ghost")}')

toolbar = f'''<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap">
<div style="display:flex;align-items:center;gap:8px"><div class="seg"><span>1 h</span><span class="on">8 h</span><span>24 h</span><span>7 days</span><span>30 days</span></div>
<span class="in" style="width:240px">{ic("cal")}<span class="grow tab">22 Nov · 00:46 – 08:46</span></span>
{btn(icon="chev-l",attrs="Earlier")}{btn(icon="chev-r",attrs="Later")}</div>
<div style="display:flex;align-items:center;gap:12px"><label style="display:inline-flex;align-items:center;gap:8px;font-size:13px;color:var(--ink-gray-7)"><span class="sw on"></span>Show events</label><span class="chip"><span class="k">Resolution</span>1 min</span></div>
</div>'''

events = f'''<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center" class="qs"><span>Events in range</span><span class="chip" style="background:var(--surface-red-2);color:var(--ink-red-7)">{ic("octagon","i s35")}TRIP-0007 · 08:14</span><span class="chip">{ic("zap","i s35")}Grid lost · 07:40</span><span class="chip">{ic("wrench","i s35")}F9 maintenance · 05:32</span></div>'''

right = f'''<div style="flex:1;min-width:0;overflow:auto"><div class="body" style="gap:16px">{toolbar}
<section class="card" style="position:relative;display:flex;flex-direction:column;gap:14px">{charts}{tooltip}</section>
{events}
<section style="display:flex;flex-direction:column;gap:10px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h3">Over this range</h2><span class="qs">1-min averages from the TimescaleDB continuous aggregate · raw 2 s data kept 30 days</span></div>{stats}</section>
</div></div>'''

write('Trends.dc.html', page('Trends', shell('Trends.dc.html', head, f'<div style="display:flex;flex:1;min-height:0">{picker}{right}</div>'), {"$preview": {"width": 1440, "height": 900}}))
