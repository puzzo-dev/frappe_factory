"""Company dashboard: factory metrics (Frappe Factory) + manufacturing metrics (ERPNext, needs the link)."""
from ff import *
import math

head = header('<div class="crumb"><span class="cur">Dashboard</span></div>',
  f'<span class="chip"><span class="k">Plants</span>All 6</span><div class="seg"><span class="on">Today</span><span>This week</span><span>This month</span></div>{btn("Export","download","ghost")}')

KPI_HREF = {'OEE': 'CoProduction.dc.html', 'Plan attainment': 'CoProduction.dc.html', 'Unplanned downtime': 'CoDowntime.dc.html', 'Open alarms': 'CoAlarms.dc.html', 'Interlock trips': 'CoTrips.dc.html',
            'Work orders open': 'CoProduction.dc.html', 'Completed today': 'CoProduction.dc.html', 'Material shortages': 'Resources.dc.html', 'Quality inspections': 'CoHolds.dc.html', 'Production plan': 'CoProduction.dc.html'}
def kpi(k, v, d, ink=''):
    st = f';color:{ink}' if ink else ''
    return f'<a href="{KPI_HREF[k]}" class="card kpi" style="color:inherit;text-decoration:none"><span class="k">{k}</span><span class="v" style="font-size:20px{st}">{v}</span><span class="d">{d}</span></a>'

plants = [('Rice mill', 88, 96), ('Plant B', 82, 91), ('Poultry farm', 79, 75), ('Koyo 1', 70, 70), ('Oil mill', 61, 73)]
def hbars():
    rows = ''
    for n, oee, att in plants:
        rows += f'''<div style="display:grid;grid-template-columns:96px minmax(0,1fr) 44px;align-items:center;gap:10px;height:28px;font-size:13px"><span style="color:var(--ink-gray-7)">{n}</span><span style="height:12px;background:var(--surface-gray-2);border-radius:3px;position:relative"><i style="position:absolute;left:0;top:0;bottom:0;width:{oee}%;border-radius:3px;background:var(--ink-gray-7)"></i><i style="position:absolute;left:80%;top:-3px;bottom:-3px;width:1.5px;background:var(--ink-gray-9)"></i></span><span class="tab r" style="display:flex;color:var(--ink-gray-9);font-weight:500">{oee}%</span></div>'''
    rows += '<div style="display:grid;grid-template-columns:96px minmax(0,1fr) 44px;align-items:center;gap:10px;height:28px;font-size:13px;color:var(--ink-gray-5)"><span>Plant D</span><span>Offline since 05:34</span><span class="r" style="display:flex">—</span></div>'
    return rows

def lines():
    W, H, L, B, T = 430, 190, 34, 24, 10
    days = 14
    series = [('Rice mill', 'oklch(0.55 0.15 300)', [92, 95, 94, 97, 93, 96, 98, 95, 94, 97, 96, 95, 97, 96]),
              ('Plant B', 'oklch(0.55 0.16 252)', [88, 90, 86, 92, 91, 89, 93, 90, 92, 88, 91, 93, 90, 91]),
              ('Koyo 1', 'var(--ink-gray-9)', [84, 86, 88, 83, 87, 90, 85, 88, 86, 89, 87, 84, 64, 70]),
              ('Oil mill', 'oklch(0.6 0.14 60)', [80, 78, 82, 79, 81, 77, 83, 80, 78, 82, 79, 81, 76, 73])]
    y = lambda v: T + (H - T - B) * (1 - (v - 50) / 50)
    x = lambda i: L + i * (W - L - 70) / (days - 1)
    g = ''.join(f'<line x1="{L}" x2="{W-70}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="var(--outline-gray-1)"/><text x="{L-6}" y="{y(v)+4:.1f}" text-anchor="end" font-size="11" fill="var(--ink-gray-5)">{v}%</text>' for v in (50, 75, 100))
    g += ''.join(f'<text x="{x(i):.1f}" y="{H-6}" text-anchor="middle" font-size="11" fill="var(--ink-gray-5)">{d}</text>' for i, d in ((0, '9 Nov'), (7, '16 Nov'), (13, '22 Nov')))
    for n, c, v in series:
        pts = ' '.join(f'{x(i):.1f},{y(vv):.1f}' for i, vv in enumerate(v))
        g += f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="{2 if n=="Koyo 1" else 1.5}"/><text x="{W-64}" y="{y(v[-1])+4:.1f}" font-size="11" fill="{c}" font-weight="500">{n}</text>'
    return f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Plan attainment per plant over 14 days; Koyo 1 drops to 64 and 70 percent on the last two days" style="display:block">{g}</svg>'

par = [('Quality hold · interlock', 'Koyo 1', 32), ('Motor overload', 'Oil mill', 65), ('Film change or splice', 'Koyo 1', 6), ('Screen blinding', 'Rice mill', 9), ('Power dip', 'all', 14)]
par.sort(key=lambda r: -r[2]); mx = par[0][2]
prow = ''.join(f'<div style="display:grid;grid-template-columns:150px minmax(0,1fr) 56px;align-items:center;gap:10px;height:28px;font-size:13px"><span style="display:flex;flex-direction:column;line-height:1.15"><span style="color:var(--ink-gray-8)">{r}</span><span class="qs" style="font-size:11px">{p}</span></span><span style="height:12px"><i style="display:block;height:12px;border-radius:2px;width:{m/mx*100:.0f}%;background:var(--ink-gray-7)"></i></span><span class="tab r" style="display:flex">{m} min</span></div>' for r, p, m in par)

WC = 'grid-template-columns:minmax(0,1.6fr) 100px minmax(0,1.2fr) 92px 132px 24px'
wos = [('Pure water · 50 cl sachet', 'WO-0412 · PW-50CL', 'Koyo 1', 1743, 7200, 'bags', 'Today', ('Stopped by trip', 'red')),
       ('Refined soybean oil · 1 L', 'WO-0118 · RSO-1L', 'Oil mill', 6.1, 8.4, 't', 'Today', ('In process', 'blue')),
       ('Parboiled long grain · 50 kg', 'WO-0233 · PLG-50', 'Rice mill', 432, 600, 'bags', 'Tomorrow', ('In process', 'blue')),
       ('Bottled water · 75 cl', 'WO-0790 · BW-75CL', 'Plant B', 14200, 18000, 'bottles', 'Today', ('In process', 'blue')),
       ('Pure water · 50 cl sachet', 'WO-0409 · PW-50CL', 'Plant D', 8820, 10000, 'bags', 'Yesterday', ('Overdue', 'amber'))]
wrows = ''
for t, m, p, done, plan, u, due, (st, sc) in wos:
    pct = round(done / plan * 100)
    fd = f'{done:,}' if isinstance(done, int) else f'{done}'
    fp = f'{plan:,}' if isinstance(plan, int) else f'{plan}'
    wrows += f'''<div class="lr" style="{WC};min-height:56px" onclick="location.href='{'RunDetail.dc.html' if m.startswith('WO-0412') else 'CoProduction.dc.html'}'"><span class="c"><div class="t1">{t}</div><div class="m tab">{m}</div></span><span>{p}</span>
<span style="display:flex;flex-direction:column;gap:6px;min-width:0"><span class="tab" style="display:flex;justify-content:space-between;gap:8px"><span style="color:var(--ink-gray-8)">{fd}</span><span class="qs">of {fp} {u} · {pct}%</span></span><span class="bar"><i style="width:{pct}%"></i></span></span>
<span class="qs" style="color:{"var(--ink-amber-7)" if due=="Yesterday" else "var(--ink-gray-7)"}">{due}</span><span>{bd(st, sc)}</span><span style="color:var(--ink-gray-4);display:flex" title="Open in ERPNext">{ic("ext","i s35")}</span></div>'''

body = f'''<div class="body">
<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;align-items:baseline;gap:8px"><h2 class="h2">Factory</h2><span class="qs">Live from the plants · works without ERPNext</span></div>
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px">
{kpi('OEE', '74%', '5 live plants · target 80%')}
{kpi('Plan attainment', '81%', 'Good output against plan so far')}
{kpi('Unplanned downtime', '2 h 15 min', '9 stops · 3 need a reason')}
{kpi('Open alarms', '11', '1 priority 1 · 6 not acknowledged')}
{kpi('Interlock trips', '1', 'Koyo 1 · 32 min', 'var(--ink-red-7)')}
</div>
<div style="display:grid;grid-template-columns:minmax(0,0.9fr) minmax(0,1.3fr) minmax(0,1fr);gap:12px">
<div class="card" style="display:flex;flex-direction:column;gap:10px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h3 class="h3">OEE by plant</h3><a href="Plants.dc.html" style="font-size:13px">Plants</a></div>{hbars()}</div>
<div class="card" style="display:flex;flex-direction:column;gap:10px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h3 class="h3">Plan attainment · 14 days</h3><span class="qs">good output ÷ plan, per day</span></div>{lines()}</div>
<div class="card" style="display:flex;flex-direction:column;gap:10px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h3 class="h3">Lost time by reason</h3><a href="CoDowntime.dc.html" style="font-size:13px">View all</a></div>{prow}</div>
</div></section>
<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;align-items:center;gap:8px"><h2 class="h2">Manufacturing</h2>{bd("From ERPNext · erp.ivarse.ng", "gray")}<span class="qs" style="margin-left:auto">Hidden when ERPNext is not linked</span></div>
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px">
{kpi('Work orders open', '14', '3 due today · 1 overdue')}
{kpi('Completed today', '6', 'Stock posted to ERPNext')}
{kpi('Material shortages', '2', 'Antiscalant, bleaching earth', 'var(--ink-amber-7)')}
{kpi('Quality inspections', '11', '1 rejected · Koyo 1 T4')}
{kpi('Production plan', '78%', 'PP-2026-047 · this week')}
</div>
<div class="list"><div class="lh" style="{WC}"><span>Work order</span><span>Plant</span><span>Done</span><span>Due</span><span>Status</span><span></span></div>{wrows}</div>
</section></div>'''

def build(name, menu=False):
    content = shell('Dashboard.dc.html', head, body, scope='company', menu_open=menu)
    if menu:
        content = f'<div style="position:relative">{content}<div class="ff" style="position:absolute;inset:0;display:block;min-height:0;background:transparent;pointer-events:none">{app_menu(8, 50)}</div></div>'
    write(name, page('Dashboard', content, {"$preview": {"width": 1440, "height": 900}}))

build('Dashboard.dc.html')
build('DashboardMenu.dc.html', True)
