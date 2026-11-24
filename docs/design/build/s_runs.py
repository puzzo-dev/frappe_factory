from ff import *

# ---------------- Runs list ----------------
COLS = 'grid-template-columns:minmax(0,1.3fr) 88px 172px minmax(0,1.3fr) 72px 64px 132px 24px'
runs = [
  ('RUN-0412', 'Morning', '22 Nov · 06:00 – 08:14', 1743, 2490, '1.4%', '70%', ('Stopped by trip', 'red'), True),
  ('RUN-0411', 'Night', '21 Nov · 22:00 – 06:00', 4780, 7200, '1.9%', '64%', ('Completed', 'gray'), False),
  ('RUN-0410', 'Afternoon', '21 Nov · 14:00 – 22:00', 6935, 7200, '2.2%', '86%', ('Completed', 'gray'), False),
  ('RUN-0409', 'Morning', '21 Nov · 06:00 – 14:00', 5746, 7200, '1.7%', '73%', ('Completed', 'gray'), False),
  ('RUN-0408', 'Night', '20 Nov · 22:00 – 06:00', 7090, 7200, '1.5%', '89%', ('Completed', 'gray'), False),
  ('RUN-0407', 'Afternoon', '20 Nov · 14:00 – 22:00', 6770, 8000, '2.0%', '78%', ('Completed', 'gray'), False),
]
def rrow(r):
    rid, sh, tm, good, plan, rej, oee, (st, sc), act = r
    pct = round(good/plan*100)
    href = ' onclick="location.href=\'RunDetail.dc.html\'"' if act else ''
    return f'''<div class="lr{' act' if act else ''}" style="{COLS};min-height:56px"{href}>
<span class="c"><div class="t1">Pure water · 50 cl sachet</div><div class="m"><span class="id">{rid}</span> · WO-{rid[4:]} · {10 if plan == 8000 else 9} fillers</div></span>
<span>{sh}</span>
<span class="c tab" style="font-size:13px">{tm}</span>
<span style="display:flex;flex-direction:column;gap:6px;min-width:0"><span class="tab" style="display:flex;justify-content:space-between;gap:8px"><span style="color:var(--ink-gray-8)">{good:,}</span><span class="qs">of {plan:,} · {pct}%</span></span><span class="bar"><i style="width:{pct}%"></i></span></span>
<span class="r tab" style="display:flex">{rej}</span>
<span class="r tab" style="display:flex">{oee}</span>
<span>{bd(st, sc)}</span>
<span style="color:var(--ink-gray-4);display:flex">{ic('chev-r','i s35')}</span>
</div>'''

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Production runs',None)),
  f'{btn("Export","download","ghost")}<button type="button" class="btn solid">{ic("plus")}Start run</button>')

kpis = f'''<section aria-label="This week" style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">
<div class="card kpi"><span class="k">Good output · this week</span><span class="v">33,064 <small>bags</small></span><span class="d">661,280 sachets · of 39,290 bags planned · 84%</span></div>
<div class="card kpi"><span class="k">OEE · this week</span><span class="v">77%</span><span class="d"><span class="d-dn">−4 pts</span> vs last week</span></div>
<div class="card kpi"><span class="k">Rejects</span><span class="v">1.8%</span><span class="d">12,120 sachets · target under 2%</span></div>
<div class="card kpi"><span class="k">Runs</span><span class="v">6</span><span class="d">1 stopped by a trip</span></div>
</section>'''

toolbar = f'''<div style="display:flex;align-items:center;justify-content:space-between;gap:8px">
<div style="display:flex;gap:8px;align-items:center"><div class="seg"><span>Today</span><span class="on">This week</span><span>This month</span></div>
<span class="in muted" style="width:200px">{ic('search')}<span class="grow">Search runs</span></span>
<button type="button" class="btn">{ic('filter')}Filter</button></div>
<span class="qs">1 bag = 20 × 50 cl sachets · Morning 06–14, Afternoon 14–22, Night 22–06</span></div>'''

lst = f'''<div class="list"><div class="lh" style="{COLS}"><span>Product and run</span><span>Shift</span><span>Time</span><span>Good output · bags</span><span class="r" style="display:flex">Rejects</span><span class="r" style="display:flex">OEE</span><span>Status</span><span></span></div>
{''.join(rrow(r) for r in runs)}</div>'''

body = f'<div class="body" style="overflow:auto">{kpis}<section style="display:flex;flex-direction:column;gap:12px">{toolbar}{lst}</section></div>'
write('Runs.dc.html', page('Production runs', shell('Runs.dc.html', head, body), {"$preview": {"width": 1440, "height": 900}}))

# ---------------- Run detail ----------------
fillers = [('F1',3890,1),('F2',3850,2),('F3',3920,0),('F4',3780,1),('F5',3880,0),('F6',3900,1),('F7',3910,0),('F8',3860,0),('F9',None,0),('F10',3870,1)]
assert sum(g for _,g,_ in fillers if g) == 34860
rejects = [56,83,46,65,46,65,46,47,0,46]  # sachets, sums to 500

def hourly():
    W,H,L,B,T = 400,190,44,24,14
    data = [('06:00',800,'full'),('07:00',760,'full'),('08:00',183,'part')]
    plan = 900
    pw, ph_ = W-L-8, H-T-B
    y = lambda v: T+ph_-v/1200*ph_
    bw = 48; gap = (pw - bw*3)/3
    out = []
    for v in (0,300,600,900,1200):
        out.append(f'<line x1="{L}" x2="{W-8}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="var(--outline-gray-1)"/><text x="{L-8}" y="{y(v)+4:.1f}" text-anchor="end" font-size="12" fill="var(--ink-gray-6)">{v:,}</text>')
    for i,(lab,v,k) in enumerate(data):
        x = L+gap/2+i*(bw+gap)
        out.append(f'<rect x="{x:.1f}" y="{y(v):.1f}" width="{bw}" height="{y(0)-y(v):.1f}" rx="3" fill="var(--ink-gray-7)"/>')
        out.append(f'<text x="{x+bw/2:.1f}" y="{y(v)-6:.1f}" text-anchor="middle" font-size="12" fill="var(--ink-gray-8)">{v:,}</text>')
        out.append(f'<text x="{x+bw/2:.1f}" y="{H-6}" text-anchor="middle" font-size="12" fill="var(--ink-gray-6)">{lab}</text>')
    out.append(f'<line x1="{L}" x2="{W-8}" y1="{y(plan):.1f}" y2="{y(plan):.1f}" stroke="var(--ink-gray-9)" stroke-dasharray="4 4"/><text x="{W-8}" y="{y(plan)-6:.1f}" text-anchor="end" font-size="12" fill="var(--ink-gray-7)">Plan 900 bags / h</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Good bags per hour: 06:00 800, 07:00 760, 08:00 183 until the trip at 08:14. Plan 900 bags per hour, 9 fillers at 100 bags each." style="display:block">{"".join(out)}</svg>'

def oee_row(label, pct, note):
    return f'''<div style="display:grid;grid-template-columns:96px minmax(0,1fr) 48px;align-items:center;gap:12px;min-height:36px"><span style="font-size:13px;color:var(--ink-gray-7)">{label}</span><span style="display:flex;flex-direction:column;gap:4px"><span class="bar lg"><i style="width:{pct}%"></i></span><span class="qs">{note}</span></span><span class="tab r" style="display:flex;font-weight:600;color:var(--ink-gray-9)">{pct}%</span></div>'''

FC = 'grid-template-columns:48px minmax(0,1fr) 72px 64px 64px 72px 112px'
def frow(i, f):
    name, good, stops = f
    if good is None:
        return f'<div class="lr" style="{FC};cursor:default;color:var(--ink-gray-6)"><span style="font-weight:500">{name}</span><span>—</span><span class="r tab" style="display:flex">—</span><span class="r tab" style="display:flex">—</span><span class="r tab" style="display:flex">—</span><span class="r tab" style="display:flex">—</span><span>{bd("Maintenance","violet")}</span></div>'
    rate = round(good/(124/60))
    rj = rejects[i]
    return f'<div class="lr" style="{FC};cursor:default"><span style="font-weight:500;color:var(--ink-gray-8)">{name}</span><span style="display:flex;align-items:center;gap:8px;min-width:0"><span class="tab" style="width:44px;color:var(--ink-gray-8)">{good:,}</span><span class="bar" style="flex:1"><i style="width:{good/4200*100:.0f}%"></i></span></span><span class="r tab" style="display:flex">{rate:,}/h</span><span class="r tab" style="display:flex">{stops}</span><span class="r tab" style="display:flex">{rj}</span><span class="r tab" style="display:flex">{[142,138,145,140,143,139,141,144,0,140][i]} °C</span><span>{bd("Stopped","red")}</span></div>'

head2 = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Production runs','Runs.dc.html'),('RUN-0412',None)),
  f'{bd("Stopped by trip","red")}{btn("Work order","ext","ghost")}<button type="button" class="btn solid">End run</button>')

k2 = f'''<section style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">
<div class="card kpi"><span class="k">Good output</span><span class="v">1,743 <small>bags</small></span><span class="d">34,860 sachets · 70% of 2,490 bags planned</span></div>
<div class="card kpi"><span class="k">OEE</span><span class="v">70%</span><span class="d">Target 80%</span></div>
<div class="card kpi"><span class="k">Rejects</span><span class="v">500 <small>sachets</small></span><span class="d">1.4% · seal and weight · 25 bags' worth</span></div>
<div class="card kpi"><span class="k">Run time</span><span class="v">2 h 04 min</span><span class="d">of 2 h 46 min since start</span></div>
</section>'''

oee = f'''<section class="card" style="display:flex;flex-direction:column;gap:8px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h3">OEE breakdown</h2><span class="qs">70% = 75% × 95% × 98.6%</span></div>
{oee_row('Availability', 75, 'Ran 2 h 04 min of 2 h 46 min. Lost 32 min to the trip and 10 min to small stops.')}
{oee_row('Performance', 95, '35,360 sachets made against 37,200 at the rated 2,000 sachets (100 bags) per filler per hour, 9 fillers.')}
{oee_row('Quality', 98.6, '34,860 good of 35,360 sachets made. 500 rejected at the checkweigher.')}
</section>'''

chart = f'<section class="card" style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h3">Good bags per hour</h2><span class="qs">08:00 hour cut short at 08:14</span></div>{hourly()}</section>'

flist = f'''<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h2">Fillers</h2><span class="qs">Sachets from each filler's PLC counter · good rate over run time · 20 sachets = 1 bag</span></div>
<div class="list"><div class="lh" style="{FC}"><span>Filler</span><span>Good sachets</span><span class="r" style="display:flex">Sachets/h</span><span class="r" style="display:flex">Stops</span><span class="r" style="display:flex">Rejects</span><span class="r" style="display:flex">Jaw temp</span><span>State</span></div>
{''.join(frow(i,f) for i,f in enumerate(fillers))}</div></section>'''

DC = 'grid-template-columns:64px minmax(0,1fr) 120px 72px'
dts = [('08:14','Quality hold · lead interlock IL-01','All fillers','32 min','red'),('07:21','Film splice','F4','6 min',''),('06:40','Jaw jam cleared','F2','4 min','')]
dl = ''.join(f'<div class="lr" style="{DC}"><span class="tab qs">{t}</span><span class="t1">{r}</span><span>{w}</span><span class="r tab" style="display:flex;{"color:var(--ink-red-7);font-weight:500" if c else ""}">{d}</span></div>' for t,r,w,d,c in dts)
dsec = f'<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h2">Downtime in this run</h2><a href="Downtime.dc.html" style="font-size:13px">Open downtime</a></div><div class="list"><div class="lh" style="{DC}"><span>Start</span><span>Reason</span><span>Where</span><span class="r" style="display:flex">Lost</span></div>{dl}</div></section>'

panel = f'''<aside class="panel"><div style="padding:16px;display:flex;flex-direction:column;gap:20px">
<div class="divy">
<div class="prow"><span>Product</span><span>Pure water · 50 cl sachet</span></div>
<div class="prow"><span>Item</span><span class="tab">PW-50CL</span></div>
<div class="prow"><span>Pack</span><span>Bag of 20 sachets</span></div>
<div class="prow"><span>Per bag</span><span class="tab">20 × 50 cl = 10 L</span></div>
<div class="prow"><span>Work order</span><span><a href="CoProduction.dc.html">WO-0412</a> · ERPNext</span></div>
<div class="prow"><span>Shift</span><span>Morning · 06:00 – 14:00</span></div>
<div class="prow"><span>Supervisor</span><span>Musa A.</span></div>
<div class="prow"><span>Started</span><span class="tab">22 Nov · 06:00:12</span></div>
<div class="prow"><span>Fillers</span><span>F1 – F10, F9 out</span></div>
</div>
<div style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">Materials used</h3><div class="divy" style="font-size:13px">
<div style="display:flex;justify-content:space-between;padding:6px 0"><span style="color:var(--ink-gray-7)">Treated water</span><span class="tab">17.7 m³</span></div>
<div style="display:flex;justify-content:space-between;padding:6px 0"><span style="color:var(--ink-gray-7)">Sachet film 320 mm</span><span class="tab">84.9 kg · 3.4 rolls</span></div>
<div style="display:flex;justify-content:space-between;padding:6px 0"><span style="color:var(--ink-gray-7)">Date-code ribbon</span><span class="tab">42 m</span></div>
</div><span class="qs">Posted to ERPNext as a Manufacture stock entry when the run ends.</span></div>
<div style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">Operators</h3><div class="divy" style="font-size:13px">
<div style="display:flex;align-items:center;gap:8px;padding:6px 0"><span class="av">KE</span><span style="flex:1">Kemi E.</span><span class="qs">F1 – F5</span></div>
<div style="display:flex;align-items:center;gap:8px;padding:6px 0"><span class="av">SI</span><span style="flex:1">Sani I.</span><span class="qs">F6 – F10</span></div>
<div style="display:flex;align-items:center;gap:8px;padding:6px 0"><span class="av">GO</span><span style="flex:1">Grace O.</span><span class="qs">Quality</span></div>
</div></div>
</div></aside>'''

main2 = f'<div style="flex:1;min-width:0;overflow:auto"><div class="body">{k2}<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px">{oee}{chart}</div>{flist}{dsec}</div></div>'
write('RunDetail.dc.html', page('RUN-0412', shell('Runs.dc.html', head2, f'<div style="display:flex;flex:1;min-height:0">{main2}{panel}</div>'), {"$preview": {"width": 1440, "height": 900}}))
