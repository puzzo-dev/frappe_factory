from ff import *

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Downtime',None)),
  f'{btn("Export","download","ghost")}<button type="button" class="btn solid">{ic("plus")}Log downtime</button>')

kpis = f'''<section style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">
<div class="card kpi"><span class="k">Unplanned · today</span><span class="v">1 h 06 min</span><span class="d">7 stops · 32 min still running</span></div>
<div class="card kpi"><span class="k">Planned · today</span><span class="v">3 h 14 min</span><span class="d">F9 maintenance since 05:32</span></div>
<div class="card kpi"><span class="k">Needs a reason</span><span class="v" style="color:var(--ink-amber-8)">3</span><span class="d">Short stops the PLC logged</span></div>
<div class="card kpi"><span class="k">Mean time between stops</span><span class="v">1 h 08 min</span><span class="d"><span class="d-dn">−22 min</span> vs 7-day average</span></div>
</section>'''

# ---- timeline 00:00 -> 08:46 (526 min) ----
T0, TN = 0, 526
def seg(a, b, kind):
    col = {'run':'var(--surface-green-3)','stop':'var(--surface-red-6)','unc':'var(--surface-amber-5)','plan':'var(--surface-violet-3)','idle':'var(--surface-gray-3)'}[kind]
    return f'<span title="" style="position:absolute;top:0;bottom:0;left:{a/TN*100:.2f}%;width:{max((b-a)/TN*100,0.35):.2f}%;background:{col}"></span>'
lanes = {f'F{i}': [] for i in range(1, 11)}
stops = {  # filler: [(start, end, kind)]
  'F2': [(400, 404, 'stop')], 'F3': [(78, 83, 'unc')], 'F4': [(441, 447, 'stop')], 'F7': [(332, 334, 'unc')],
  'F9': [(130, 144, 'stop'), (332, 526, 'plan')],
}
def mins(h, m): return h*60+m
lane_html = []
for i in range(1, 11):
    f = f'F{i}'
    parts = [seg(0, TN, 'run')]
    for a, b, k in stops.get(f, []): parts.append(seg(a, b, k))
    parts.append(seg(mins(7,40), mins(7,43), 'unc'))
    if f != 'F9': parts.append(seg(mins(8,14), TN, 'stop'))
    lane_html.append(f'<div style="display:grid;grid-template-columns:40px minmax(0,1fr);align-items:center;gap:8px;height:22px"><span class="qs" style="color:var(--ink-gray-7)">{f}</span><span style="position:relative;height:14px;border-radius:3px;overflow:hidden">{"".join(parts)}</span></div>')
ticks = ''.join(f'<span class="qs tab" style="position:absolute;left:{m/TN*100:.2f}%;transform:translateX({"0" if m==0 else "-50%"})">{m//60:02d}:00</span>' for m in range(0, 361, 120))
ticks += '<span class="qs tab" style="position:absolute;right:0">08:46</span>'
legend = ''.join(f'<span style="display:inline-flex;align-items:center;gap:6px"><i style="width:10px;height:10px;border-radius:2px;background:{c}"></i>{l}</span>' for l, c in (('Running','var(--surface-green-3)'),('Stopped','var(--surface-red-6)'),('Needs a reason','var(--surface-amber-5)'),('Planned','var(--surface-violet-3)')))
timeline = f'''<section class="card" style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:center"><h2 class="h3">Fillers today</h2><div style="display:flex;gap:14px" class="qs">{legend}</div></div>
<div style="display:flex;flex-direction:column;gap:2px">{''.join(lane_html)}<div style="display:grid;grid-template-columns:40px minmax(0,1fr);gap:8px;margin-top:6px"><span></span><span style="position:relative;height:16px">{ticks}</span></div></div></section>'''

# ---- pareto ----
par = [('Quality hold · interlock', 108), ('Film change or splice', 72), ('Jaw jam', 58), ('Power dip or changeover', 46), ('Waiting for treated water', 31), ('Seal temperature low', 22), ('Needs a reason', 14)]
mx = par[0][1]; tot = sum(v for _, v in par); cum = 0; prow_ = []
for lab, v in par:
    cum += v
    col = 'var(--surface-amber-5)' if lab == 'Needs a reason' else 'var(--ink-gray-7)'
    prow_.append(f'<div style="display:grid;grid-template-columns:172px minmax(0,1fr) 64px 40px;align-items:center;gap:10px;height:26px;font-size:13px"><span style="color:var(--ink-gray-7);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{lab}</span><span style="height:12px"><i style="display:block;height:12px;border-radius:2px;width:{v/mx*100:.0f}%;background:{col}"></i></span><span class="tab r" style="display:flex;color:var(--ink-gray-8)">{v//60} h {v%60:02d}</span><span class="tab r qs" style="display:flex">{round(cum/tot*100)}%</span></div>' if v >= 60 else
                 f'<div style="display:grid;grid-template-columns:172px minmax(0,1fr) 64px 40px;align-items:center;gap:10px;height:26px;font-size:13px"><span style="color:var(--ink-gray-7);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{lab}</span><span style="height:12px"><i style="display:block;height:12px;border-radius:2px;width:{v/mx*100:.0f}%;background:{col}"></i></span><span class="tab r" style="display:flex;color:var(--ink-gray-8)">{v} min</span><span class="tab r qs" style="display:flex">{round(cum/tot*100)}%</span></div>')
pareto = f'''<section class="card" style="display:flex;flex-direction:column;gap:10px"><div style="display:flex;justify-content:space-between;align-items:center"><h2 class="h3">Unplanned by reason · this week</h2><span class="qs">Cumulative %</span></div>{''.join(prow_)}
<span class="qs" style="margin-top:4px">The top three reasons cause 67% of lost time.</span></section>'''

# ---- events table ----
C = 'grid-template-columns:64px 148px 88px minmax(0,1.4fr) 104px minmax(0,1fr) 24px'
def reason_cell(r):
    if r is None:
        return f'<span class="in" style="background:var(--surface-amber-2);border-color:var(--surface-amber-2);color:var(--ink-amber-8);height:24px;width:100%"><span class="grow">Pick a reason</span>{ic("chev-d","i s35")}</span>'
    return f'<span class="t1">{r}</span>'
ev = [
  ('08:14', '32 min', 'running', 'All fillers', 'Quality hold · interlock IL-01', 'Unplanned', 'From TRIP-0007', False),
  ('07:40', '3 min', '', 'All fillers', None, 'Unplanned', 'PLC · all filler permissives dropped', True),
  ('07:21', '6 min', '', 'F4', 'Film change or splice', 'Unplanned', 'Kemi E.', False),
  ('06:40', '4 min', '', 'F2', 'Jaw jam', 'Unplanned', 'Sani I.', False),
  ('05:32', '3 h 14 min', 'running', 'F9', 'Maintenance · jaw heater', 'Planned', 'Musa A. · MNT-0088', False),
  ('05:32', '2 min', '', 'F7', None, 'Unplanned', 'PLC', False),
  ('02:10', '14 min', '', 'F9', 'Seal temperature low', 'Unplanned', 'Ibrahim K.', False),
  ('01:18', '5 min', '', 'F3', None, 'Unplanned', 'PLC', False),
]
rows = []
for t, d, run, w, r, cat, by, act in ev:
    dur = f'<span class="tab" style="{"color:var(--ink-red-7);font-weight:500" if run and cat=="Unplanned" else ""}">{d}</span>' + (f' <span class="qs">· ongoing</span>' if run else '')
    catb = bd(cat, 'violet' if cat == 'Planned' else 'gray')
    rows.append(f'<div class="lr{" act" if act else ""}" style="{C}"><span class="tab qs">{t}</span><span style="white-space:nowrap">{dur}</span><span>{w}</span><span class="c" style="overflow:visible">{reason_cell(r)}</span><span>{catb}</span><span class="c qs">{by}</span><span style="color:var(--ink-gray-4);display:flex">{ic("more","i s35")}</span></div>')

menu_groups = [('Power', ['Power dip', 'Generator changeover']), ('Mechanical', ['Jaw jam', 'Film change or splice', 'Seal temperature low']), ('Waiting', ['Waiting for treated water', 'Waiting for film', 'No operator'])]
mg = ''
for g, items in menu_groups:
    mg += f'<div style="display:flex;align-items:center;height:24px;padding:0 8px;font-size:12px;color:var(--ink-gray-6)">{g}</div>'
    for it in items:
        on = ' on' if it == 'Power dip' else ''
        tick = ic('check','i s35') if it == 'Power dip' else '<span style="width:14px"></span>'
        mg += f'<div class="mi{on}" style="font-size:13px">{tick}{it}</div>'
popover = f'''<div class="pop" role="listbox" style="left:296px;top:150px;width:256px;z-index:3">
<div style="padding:4px 4px 6px"><span class="in muted" style="height:28px">{ic("search")}<span class="grow">Search reasons</span></span></div>
{mg}
<div style="border-top:1px solid var(--outline-gray-1);margin:4px -4px 0;padding:4px 4px 0"><div class="mi" style="font-size:13px;color:var(--ink-gray-6)">{ic("plus")}Add reason in Plant settings</div></div>
</div>'''

table = f'''<section style="display:flex;flex-direction:column;gap:12px;position:relative">
<div style="display:flex;justify-content:space-between;align-items:center"><div style="display:flex;align-items:center;gap:8px"><h2 class="h2">Stops today</h2>{bd("3 need a reason","amber")}</div>
<div style="display:flex;gap:8px"><div class="seg"><span class="on">All</span><span>Needs a reason</span><span>Planned</span></div></div></div>
<div class="list"><div class="lh" style="{C}"><span>Start</span><span>Lost</span><span>Where</span><span>Reason</span><span>Type</span><span>Logged by</span><span></span></div>{''.join(rows)}</div>
<p class="qs" style="margin:0">The PLC opens a stop whenever a filler's run signal drops for more than 30 s. Anyone on shift can pick the reason; supervisors can split or merge stops.</p>
{closer('pop')}<div class="ffov"><label for="pop" class="scrim" style="position:absolute;inset:0;z-index:2" aria-label="Close"></label>{popover}</div>
</section>'''

body = f'<div class="body" style="overflow:auto">{kpis}<div style="display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:12px">{timeline}{pareto}</div>{table}</div>'
write('Downtime.dc.html', page('Downtime', shell('Downtime.dc.html', head, body), {"$preview": {"width": 1440, "height": 900}}))
