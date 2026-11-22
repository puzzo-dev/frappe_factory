"""Company-wide lists (alarms, trips, production, downtime, quality holds, maintenance, reports) and the plant-level
lists behind the breadcrumbs (interlock trips, quality holds, past handovers), plus pinned tags and the hold template."""
from ff import *

AMB, RED = 'oklch(0.723 0.152 71.82)', 'oklch(0.556 0.198 26.552)'
def kpi(k, v, d, ink=''):
    st = f';color:{ink}' if ink else ''
    return f'<div class="card kpi"><span class="k">{k}</span><span class="v" style="font-size:20px{st}">{v}</span><span class="d">{d}</span></div>'
def kpis(*ks):
    return f'<section style="display:grid;grid-template-columns:repeat({len(ks)},minmax(0,1fr));gap:12px">{"".join(kpi(*k) for k in ks)}</section>'
def prio(p):
    c = RED if p == '1' else AMB
    return f'<svg width="18" height="18" viewBox="0 0 18 18" aria-label="Priority {p}"><polygon points="9,0 18,9 9,18 0,9" fill="{c}"/><text x="9" y="13" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">{p}</text></svg>'
PLANTS = ['All 6', 'Koyo 1', 'Plant B', 'Plant D', 'Oil mill', 'Rice mill', 'Poultry farm']
def toolbar(search, extra='', note=''):
    return f'''<div style="display:flex;align-items:center;justify-content:space-between;gap:8px"><div style="display:flex;gap:8px;align-items:center"><span class="in muted" style="width:220px">{ic("search")}<span class="grow">{search}</span></span><span class="chip"><span class="k">Plant</span>All 6</span>{extra}</div><span class="qs">{note}</span></div>'''
def lst(cols, heads, rows):
    return f'<div class="list"><div class="lh" style="{cols}">{"".join(f"<span>{h}</span>" for h in heads)}</div>{"".join(rows)}</div>'
def row(cols, cells, href=None, h=52, extra=''):
    on = f' onclick="location.href=\'{href}\'"' if href else ''
    return f'<div class="lr" style="{cols};min-height:{h}px;{"" if href else "cursor:default;"}{extra}"{on}>{"".join(cells)}</div>'
def c2(a, b):
    return f'<span class="c"><div class="t1">{a}</div><div class="m">{b}</div></span>'
def co(name, active, crumbs, actions, body):
    write(name, page(name.replace('.dc.html', ''), shell(active, header(crumbs, actions), f'<div class="body" style="overflow:auto">{body}</div>', scope='company'), {"$preview": {"width": 1440, "height": 900}}))
PL = {'Koyo 1': 'Main.dc.html', 'Oil mill': 'OilMill.dc.html', 'Rice mill': 'RiceMill.dc.html', 'Poultry farm': 'PoultryFarm.dc.html', 'Plant B': 'PlantB.dc.html', 'Plant D': 'PlantD.dc.html'}
def plant_link(p):
    h = PL.get(p)
    return f'<a href="{h}" onclick="event.stopPropagation()">{p}</a>' if h else f'<span>{p}</span>'

# ---------------- Alarms, all plants
AC = 'grid-template-columns:28px minmax(0,1.6fr) 120px 80px 160px 120px'
alarms = [('1', 'AT-401 Lead trip', '9.4 µg/L · interlock IL-01', 'Koyo 1', '08:14', ('Acknowledged', 'gray'), 'Musa A.', 'Trip.dc.html'),
          ('2', 'T4 failed verification', '6.1 µg/L at SP-2', 'Koyo 1', '08:26', ('Active', 'red'), '', 'Alarms.dc.html'),
          ('2', 'H3 temperature high', '31.8 °C · alert at 30', 'Poultry farm', '08:05', ('Active', 'red'), '', 'PoultryFarm.dc.html'),
          ('2', 'EX-3 overload trip', '48 A against 40 A', 'Oil mill', '07:41', ('Acknowledged', 'gray'), 'Femi A.', 'OilMill.dc.html'),
          ('3', 'Feed bin FB-1 low', '18 % · mixer batch 4 of 6', 'Poultry farm', '08:31', ('Active', 'amber'), '', 'PoultryFarm.dc.html'),
          ('3', 'W-2 load high', '96 % · alert above 95', 'Rice mill', '07:58', ('Active', 'amber'), '', 'RiceMill.dc.html'),
          ('3', 'DP-102 carbon filter ΔP high', '1.3 bar · backwash at 1.2', 'Koyo 1', '07:52', ('Active', 'amber'), '', 'Alarms.dc.html'),
          ('3', 'Seed feed below plan', '2.7 of 4.1 t/h', 'Oil mill', '07:42', ('Active', 'amber'), '', 'OilMill.dc.html'),
          ('3', 'Silo S-2 nearly full', '92 % · switch intake to S-1', 'Rice mill', '07:20', ('Acknowledged', 'gray'), 'Halima S.', 'RiceMill.dc.html'),
          ('3', 'RO salt rejection low', '96.1 % · alert under 97', 'Plant B', '06:55', ('Acknowledged', 'gray'), 'Chidi O.', None),
          ('3', 'Diesel runway under 48 h', '41 h left', 'Koyo 1', '06:10', ('Acknowledged', 'gray'), 'Musa A.', 'Resources.dc.html')]
ar = [row(AC, [f'<span style="display:flex">{prio(p)}</span>', c2(t, m), plant_link(pl), f'<span class="tab">{s}</span>', f'<span style="display:flex;gap:6px;align-items:center">{bd(*st)}<span class="qs">{w}</span></span>', btn('Acknowledge', kind='xs') if st[0] == 'Active' else '<span></span>'], href) for p, t, m, pl, s, st, w, href in alarms]
co('CoAlarms.dc.html', 'CoAlarms.dc.html', crumb(('Alarms', None)), f'{btn("Export","download","ghost")}',
   kpis(('Active alarms', '11', '6 not acknowledged', ''), ('Priority 1', '1', 'Koyo 1 lead trip', 'var(--ink-red-7)'), ('Priority 2', '3', 'Koyo 1, Poultry farm, Oil mill', ''), ('Plants reporting', '5 of 6', 'Plant D offline since 05:34', 'var(--ink-amber-7)')) +
   f'<section style="display:flex;flex-direction:column;gap:12px">{toolbar("Search alarms", "<span class=chip><span class=k>Priority</span>All</span><div class=seg><span class=on>Active</span><span>Shelved</span><span>History</span></div>", "Newest first · priority 1 always on top")}{lst(AC, ["", "Alarm", "Plant", "Since", "State", ""], ar)}</section>')

# ---------------- Interlock trips, all plants
TC = 'grid-template-columns:minmax(0,1.5fr) 110px 150px 120px minmax(0,1.2fr) 24px'
trips = [('TRIP-0007', 'IL-01 Lead high-high · AT-401 9.4 µg/L', 'Koyo 1', '22 Nov · 08:14', ('Open · 32 min', 's-red'), 'Step 2 of 7 · QA samples · QH-0031', 'Trip.dc.html'),
         ('TRIP-0006', 'IL-01 Lead high-high · AT-401 8.6 µg/L', 'Koyo 1', '14 Nov · 11:02', ('Closed · 1 h 12 min', 'gray'), 'QA release Grace O. · QH-0029', None),
         ('B-TRIP-0012', 'IL-B2 Turbidity high · 4.6 NTU', 'Plant B', '12 Nov · 16:40', ('Closed · 48 min', 'gray'), 'QA release Chidi O. · QH-0027', None),
         ('O-TRIP-0004', 'IL-O1 Deodorizer vacuum lost · 9 mbar', 'Oil mill', '9 Nov · 13:25', ('Closed · 2 h 05 min', 'gray'), 'QA release Femi A. · QH-0026', None),
         ('R-TRIP-0002', 'IL-R1 Metal detector reject', 'Rice mill', '4 Nov · 10:10', ('Closed · 25 min', 'gray'), 'QA release Halima S. · QH-0024', None)]
tr = [row(TC, [c2(i, t), plant_link(p), f'<span class="tab">{w}</span>', f'<span>{bd(*s)}</span>', f'<span class="c qs">{n}</span>', f'<span style="color:var(--ink-gray-4);display:flex">{ic("chev-r","i s35")}</span>'], h, 56) for i, t, p, w, s, n, h in trips]
co('CoTrips.dc.html', 'CoTrips.dc.html', crumb(('Interlock trips', None)), f'{btn("Export","download","ghost")}',
   kpis(('Open trips', '1', 'Koyo 1 · 32 min', 'var(--ink-red-7)'), ('This month', '5', 'in 4 plants', ''), ('Median time to restart', '58 min', 'trip to QA release and restart', ''), ('Quality holds opened', '5', 'one per quality-related trip', '')) +
   f'<section style="display:flex;flex-direction:column;gap:12px">{toolbar("Search trips", "<div class=seg><span>Open</span><span class=on>All</span></div>", "Only the PLC can trip or reset an interlock; Frappe Factory runs the recovery")}{lst(TC, ["Trip and interlock", "Plant", "Tripped", "State", "Recovery", ""], tr)}</section>')

# ---------------- Production, all plants (needs ERPNext)
PC = 'grid-template-columns:minmax(0,1.6fr) 110px minmax(0,1.3fr) 100px 140px 24px'
wos = [('Pure water · 50 cl sachet', 'WO-0412 · PW-50CL', 'Koyo 1', 1743, 7200, 'bags of 20 sachets', 'Today · morning', ('Stopped by trip', 'red')),
       ('Pure water · 50 cl sachet', 'WO-0413 · PW-50CL', 'Koyo 1', 0, 7200, 'bags of 20 sachets', 'Today · afternoon', ('Not started', 'gray')),
       ('Bottled water · 75 cl', 'WO-0790 · BW-75CL', 'Plant B', 14200, 18000, 'bottles', 'Today', ('In process', 'blue')),
       ('Refined soybean oil · 1 L', 'WO-0118 · RSO-1L', 'Oil mill', 6.1, 8.4, 't', 'Today', ('In process', 'blue')),
       ('Parboiled long grain · 50 kg', 'WO-0233 · PLG-50', 'Rice mill', 432, 600, 'bags of 50 kg', 'Tomorrow', ('In process', 'blue')),
       ('Table eggs · tray of 30', 'WO-0051 · EGG-T30', 'Poultry farm', 329, 440, 'trays of 30 eggs', 'Today', ('In process', 'blue')),
       ('Layer mash · bulk', 'WO-0052 · FEED-LM', 'Poultry farm', 1.2, 2.0, 't', 'Today', ('In process', 'blue')),
       ('Pure water · 50 cl sachet', 'WO-0409 · PW-50CL', 'Plant D', 8820, 10000, 'bags of 20 sachets', 'Yesterday', ('Overdue', 'amber'))]
def prog(d, p, u):
    pct = round(d / p * 100)
    fd = f'{d:,}' if isinstance(d, int) else f'{d}'; fp = f'{p:,}' if isinstance(p, int) else f'{p}'
    return f'<span style="display:flex;flex-direction:column;gap:6px;min-width:0"><span class="tab" style="display:flex;justify-content:space-between;gap:8px"><span style="color:var(--ink-gray-8)">{fd} <span class="qs">of {fp} {u}</span></span><span class="qs">{pct}%</span></span><span class="bar"><i style="width:{pct}%"></i></span></span>'
pr = [row(PC, [c2(t, m), plant_link(p), prog(d, pl, u), f'<span class="qs">{due}</span>', f'<span>{bd(*st)}</span>', f'<span style="color:var(--ink-gray-4);display:flex">{ic("ext","i s35")}</span>'], 'RunDetail.dc.html' if m.startswith('WO-0412') else None, 56) for t, m, p, d, pl, u, due, st in wos]
co('CoProduction.dc.html', 'CoProduction.dc.html', crumb(('Production', None)), f'{bd("From ERPNext · synced 1 min ago","gray")}{btn("Open in ERPNext","ext","ghost")}',
   kpis(('Work orders open', '14', '3 due today · 1 overdue', ''), ('Completed today', '6', 'stock posted to ERPNext', ''), ('Plan attainment', '81%', 'good output ÷ plan so far', ''), ('Material shortages', '2', 'antiscalant, bleaching earth', 'var(--ink-amber-7)')) +
   f'<section style="display:flex;flex-direction:column;gap:12px">{toolbar("Search work orders", "<div class=seg><span class=on>Open</span><span>Completed</span></div>", "Each plant counts in its own pack unit")}{lst(PC, ["Item and work order", "Plant", "Progress", "Planned", "Status", ""], pr)}</section>')

# ---------------- Downtime, all plants
DC = 'grid-template-columns:72px minmax(0,1.3fr) 120px minmax(0,1fr) 80px 150px'
stops = [('08:14', 'Quality hold · interlock IL-01', 'Koyo 1', 'All fillers', '32 min', ('Running', 'red')),
         ('07:41', 'Motor overload', 'Oil mill', 'Expeller EX-3', '65 min', ('Running', 'red')),
         ('07:40', 'All fillers stopped · 3 min', 'Koyo 1', 'F1 – F8, F10', '3 min', ('Needs a reason', 'amber')),
         ('07:21', 'Film change or splice', 'Koyo 1', 'F4', '6 min', ('Closed', 'gray')),
         ('07:05', 'Screen blinding', 'Rice mill', 'Pre-cleaner', '9 min', ('Closed', 'gray')),
         ('06:55', 'Line stopped · 4 min', 'Rice mill', 'Husker H-1', '4 min', ('Needs a reason', 'amber')),
         ('06:40', 'Jaw jam', 'Koyo 1', 'F2', '4 min', ('Closed', 'gray')),
         ('06:12', 'Egg grader jam', 'Poultry farm', 'Egg grader', '5 min', ('Closed', 'gray')),
         ('05:10', 'Power dip', 'Plant B', 'Filler line 1', '7 min', ('Needs a reason', 'amber'))]
dr = [row(DC, [f'<span class="tab qs">{t}</span>', f'<span class="t1">{r}</span>', plant_link(p), f'<span class="c qs" style="color:var(--ink-gray-7)">{w}</span>', f'<span class="tab r" style="display:flex;justify-content:flex-end">{d}</span>', f'<span>{bd(*s)}</span>'], 'Downtime.dc.html' if p == 'Koyo 1' else None) for t, r, p, w, d, s in stops]
par = [('Motor overload', 65), ('Quality hold · interlock', 32), ('Needs a reason', 14), ('Screen blinding', 9), ('Film change or splice', 6), ('Egg grader jam', 5), ('Jaw jam', 4)]
mx = par[0][1]
pb = ''.join(f'<div style="display:grid;grid-template-columns:170px minmax(0,1fr) 56px;align-items:center;gap:10px;height:28px;font-size:13px"><span style="color:var(--ink-gray-8)">{r}</span><span style="height:12px"><i style="display:block;height:12px;border-radius:2px;width:{m/mx*100:.0f}%;background:var(--ink-gray-7)"></i></span><span class="tab" style="text-align:right">{m} min</span></div>' for r, m in par)
co('CoDowntime.dc.html', 'CoDowntime.dc.html', crumb(('Downtime', None)), f'{btn("Export","download","ghost")}',
   kpis(('Unplanned downtime today', '2 h 15 min', '9 stops in 5 plants', ''), ('Need a reason', '3', 'Koyo 1, Rice mill, Plant B', 'var(--ink-amber-7)'), ('Running now', '2', 'Koyo 1 trip, Oil mill EX-3', 'var(--ink-red-7)'), ('Biggest loss', 'Motor overload', 'Oil mill · 65 min', '')) +
   f'''<div style="display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:20px;align-items:start"><section style="display:flex;flex-direction:column;gap:12px">{toolbar("Search stops", "<div class=seg><span class=on>Today</span><span>This week</span></div>")}{lst(DC, ["Start", "Reason", "Plant", "Where", "Lost", "State"], dr)}</section>
<section class="card" style="display:flex;flex-direction:column;gap:8px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h3">Minutes lost by reason</h2><span class="qs">today, all plants</span></div>{pb}<span class="qs" style="margin-top:6px">Reasons come from each plant's list; stops the PLC picked up need one from the floor.</span></section></div>''')

# ---------------- Quality holds, all plants
HC = 'grid-template-columns:minmax(0,1.4fr) 120px minmax(0,1.3fr) 150px minmax(0,1fr) 24px'
holds = [('QH-0032', 'H3 eggs · 08:00 – 09:00', 'Poultry farm', '41 trays of 30 eggs', ('Open', 'amber'), 'Alarm rule: H3 above 30 °C for 30 min · shell and weight check', None),
         ('QH-0031', 'Lead trip TRIP-0007', 'Koyo 1', '256 bags + 14 sachets, T5 2.3 m³', ('Open', 'amber'), 'L2 scrap proposed · L1 waiting on lab', 'QualityHold.dc.html'),
         ('QH-0030', 'Coliform plate failed', 'Koyo 1', '40 bags', ('Closed', 'gray'), 'Scrapped · 18 Nov', None),
         ('QH-0029', 'Lead trip TRIP-0006', 'Koyo 1', '430 bags', ('Closed', 'gray'), '310 released with deviation, 120 scrapped', None),
         ('QH-0027', 'Turbidity trip B-TRIP-0012', 'Plant B', '2,400 bottles of 75 cl', ('Closed', 'gray'), 'Released · 13 Nov', None),
         ('QH-0026', 'Vacuum lost O-TRIP-0004', 'Oil mill', '1.8 t refined oil', ('Closed', 'gray'), 'Reworked: deodorized again', None),
         ('QH-0024', 'Metal detector R-TRIP-0002', 'Rice mill', '38 bags of 50 kg', ('Closed', 'gray'), 'Released after sieve check', None)]
hr = [row(HC, [c2(i, t), plant_link(p), f'<span class="c tab" style="color:var(--ink-gray-8)">{q}</span>', f'<span>{bd(*s)}</span>', f'<span class="c qs">{n}</span>', f'<span style="color:var(--ink-gray-4);display:flex">{ic("chev-r","i s35")}</span>'], h, 56) for i, t, p, q, s, n, h in holds]
co('CoHolds.dc.html', 'CoHolds.dc.html', crumb(('Quality holds', None)), f'{btn("Export","download","ghost")}',
   kpis(('Open holds', '2', 'Koyo 1 and Poultry farm', 'var(--ink-amber-7)'), ('Opened this month', '7', '5 by trips, 2 by alarm rules', ''), ('Released', '71%', 'of held product this month', ''), ('Scrapped', '160 bags', 'Koyo 1 · plus L2 if confirmed', '')) +
   f'<section style="display:flex;flex-direction:column;gap:12px">{toolbar("Search holds", "<div class=seg><span>Open</span><span class=on>All</span></div>", "Quantities in each product\'s pack unit")}{lst(HC, ["Hold", "Plant", "Held", "State", "Outcome", ""], hr)}</section>')

# ---------------- Maintenance, all plants
MC = 'grid-template-columns:minmax(0,1.6fr) 110px 110px 130px 150px'
jobs = [('MNT-0088', 'F9 · replace jaw heater, test 40 sachets', 'Koyo 1', 'Planned', 'Ibrahim K.', ('In progress', 'blue')),
        ('MNT-0087', 'EX-3 · inspect motor and screw after overload', 'Oil mill', 'Breakdown', 'Femi A.', ('Open · urgent', 'red')),
        ('MNT-0089', 'H3 · check cooling pad pump and float', 'Poultry farm', 'Breakdown', 'Amaka F.', ('In progress', 'blue')),
        ('MNT-0090', 'CF-102 · backwash the carbon filter', 'Koyo 1', 'Condition', 'Ibrahim K.', ('Due 16:00', 'gray')),
        ('MNT-0091', 'DP-1 · refill antiscalant from MR-0193', 'Koyo 1', 'Planned', 'Ibrahim K.', ('Waiting for parts', 'amber')),
        ('MNT-0085', 'W-2 · bearing check, every 500 h', 'Rice mill', 'Preventive', 'Sule M.', ('Due tomorrow', 'gray')),
        ('MNT-0080', 'RO-1 · clean in place', 'Plant B', 'Preventive', 'Chidi O.', ('Overdue 2 days', 'amber'))]
mr = [row(MC, [c2(t, i), plant_link(p), f'<span class="qs">{k}</span>', f'<span class="qs" style="color:var(--ink-gray-7)">{w}</span>', f'<span>{bd(*s)}</span>']) for i, t, p, k, w, s in jobs]
pm = [('UV-301 lamp', 'Koyo 1', 'at 9,000 h · 87 days'), ('Cartridges CF-201, CF-301', 'Koyo 1', 'every 30 days · 21 days'), ('Generator G-1 service', 'Koyo 1', 'every 250 h · 4 days'), ('Hammer mill screens', 'Poultry farm', 'every 400 t · 6 days'), ('Expeller worms', 'Oil mill', 'every 1,200 h · 11 days')]
pml = ''.join(f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 0;border-top:1px solid var(--outline-gray-1);font-size:13px"><span style="display:flex;flex-direction:column;gap:2px"><span style="color:var(--ink-gray-8)">{a}</span><span class="qs">{b}</span></span><span class="qs tab" style="text-align:right">{c}</span></div>' for a, b, c in pm)
co('CoMaint.dc.html', 'CoMaint.dc.html', crumb(('Maintenance', None)), f'{btn("Export","download","ghost")}<button type="button" class="btn solid">{ic("plus")}New job</button>',
   kpis(('Open jobs', '7', '2 in progress', ''), ('Breakdowns', '2', 'Oil mill EX-3, Poultry H3 pad', 'var(--ink-red-7)'), ('Overdue', '1', 'Plant B RO clean in place', 'var(--ink-amber-7)'), ('Mean time to repair', '1 h 40 min', 'last 30 days', '')) +
   f'''<div style="display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:20px;align-items:start"><section style="display:flex;flex-direction:column;gap:12px">{toolbar("Search jobs", "<div class=seg><span class=on>Open</span><span>Done</span></div>", "Jobs from kiosks, alarms and schedules")}{lst(MC, ["Job", "Plant", "Kind", "Assigned", "State"], mr)}</section>
<section class="card" style="display:flex;flex-direction:column;gap:4px"><div style="display:flex;justify-content:space-between;align-items:baseline;padding-bottom:6px"><h2 class="h3">Preventive, next due</h2><span class="qs">by hours, days or tonnes</span></div>{pml}<span class="qs" style="margin-top:8px">With ERPNext, jobs mirror to Maintenance Visits on the asset.</span></section></div>''')

# ---------------- Reports
RH = {'Shift production summary': 'Runs.dc.html', 'OEE by plant and machine': 'Dashboard.dc.html', 'Downtime by reason': 'CoDowntime.dc.html', 'Alarms and trips': 'CoAlarms.dc.html',
      'Quality holds and releases': 'CoHolds.dc.html', 'Resource use per unit': 'Resources.dc.html', 'Flock and lay rate': 'PoultryFarm.dc.html', 'Yield and recovery': 'RiceMill.dc.html'}
reps = [('Shift production summary', 'Output, plan, OEE, stops and rejects per plant and shift, in each plant\'s pack unit', 'Every shift end · WhatsApp to managers', 'bars'),
        ('OEE by plant and machine', 'Availability × performance × quality, trended by day', 'Weekly · Monday 07:00 email', 'gauge'),
        ('Downtime by reason', 'Minutes lost by reason, machine and plant; stops without a reason', '—', 'clock'),
        ('Alarms and trips', 'Standing alarms, floods, time to acknowledge, trips and time to restart', 'Weekly · Monday 07:00 email', 'bell'),
        ('Quality holds and releases', 'Held, released, reworked and scrapped, with QA sign-offs', 'Monthly · 1st, PDF', 'shield'),
        ('Resource use per unit', 'Water per bag, diesel per 1,000 bags, kWh per tonne, feed per dozen eggs', '—', 'droplet'),
        ('Flock and lay rate', 'Poultry: birds, mortality, lay rate, eggs per bird, feed and water per bird', 'Daily · 18:00 WhatsApp', 'chart'),
        ('Yield and recovery', 'Rice: head rice yield, broken %. Oil: oil yield, refining loss', '—', 'layers')]
rc = ''.join(f'''<div class="card" style="display:flex;flex-direction:column;gap:10px"><div style="display:flex;gap:10px;align-items:center"><span style="width:32px;height:32px;border-radius:8px;background:var(--surface-gray-2);display:grid;place-items:center;color:var(--ink-gray-7)">{ic(i)}</span><span style="font-weight:600;color:var(--ink-gray-9)">{t}</span></div>
<p class="ps" style="min-height:40px">{d}</p><div style="display:flex;justify-content:space-between;align-items:center;padding-top:10px;border-top:1px solid var(--outline-gray-1)"><span class="qs">{s}</span><span style="display:flex;gap:6px">{btn("Schedule",kind="ghost")}<a href="{RH[t]}" class="btn">Open</a></span></div></div>''' for t, d, s, i in reps)
co('CoReports.dc.html', 'CoReports.dc.html', crumb(('Reports', None)), f'{btn("New report","plus")}',
   f'''<div style="display:flex;align-items:center;justify-content:space-between"><div style="display:flex;gap:8px;align-items:baseline"><h2 class="h2">Reports</h2><span class="qs">8 built in · any can be scheduled to email or WhatsApp</span></div><span class="chip"><span class="k">Plant</span>All 6</span></div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px">{rc}</div>
<p class="qs" style="margin:0">Reports are Frappe Script and Query Reports, so they also open in Desk, export to Excel or PDF, and can be added to any Frappe workspace.</p>''')

# ================= Plant level (Koyo 1)
def pl(name, active, crumbs, actions, body):
    write(name, page(name.replace('.dc.html', ''), shell(active, header(crumbs, actions), f'<div class="body" style="overflow:auto">{body}</div>'), {"$preview": {"width": 1440, "height": 900}}))
K = ('Plants', 'Plants.dc.html'), ('Koyo 1', 'Main.dc.html')

TL = 'grid-template-columns:minmax(0,1.6fr) 150px 140px minmax(0,1.2fr) 24px'
ktrips = [('TRIP-0007', 'IL-01 Lead high-high · AT-401 9.4 µg/L', '22 Nov · 08:14', ('Open · 32 min', 's-red'), 'Step 2 of 7 · QA samples · QH-0031', 'Trip.dc.html'),
          ('TRIP-0006', 'IL-01 Lead high-high · AT-401 8.6 µg/L', '14 Nov · 11:02', ('Closed · 1 h 12 min', 'gray'), 'Cause: borehole pump restart · QH-0029', None),
          ('TRIP-0005', 'IL-02 Turbidity high · AT-303 4.3 NTU', '3 Nov · 19:47', ('Closed · 41 min', 'gray'), 'Cause: media filter backwash overdue', None),
          ('TRIP-0004', 'IL-03 UV intensity low · UV-301 64 %', '27 Oct · 09:15', ('Closed · 22 min', 'gray'), 'Cause: lamp sleeve fouled, cleaned', None)]
ktr = [row(TL, [c2(i, t), f'<span class="tab">{w}</span>', f'<span>{bd(*s)}</span>', f'<span class="c qs">{n}</span>', f'<span style="color:var(--ink-gray-4);display:flex">{ic("chev-r","i s35")}</span>'], h, 56) for i, t, w, s, n, h in ktrips]
pl('TripList.dc.html', 'TripList.dc.html', crumb(*K, ('Interlock trips', None)), btn("Export","download","ghost"),
   kpis(('Open', '1', 'TRIP-0007 · 32 min', 'var(--ink-red-7)'), ('Last 30 days', '3', '2 lead, 1 turbidity', ''), ('Median time to restart', '41 min', 'trip to restart', ''), ('Interlocks armed', '3 of 3', 'lead, turbidity, UV', '')) +
   f'<section style="display:flex;flex-direction:column;gap:12px">{lst(TL, ["Trip and interlock", "Tripped", "State", "Cause and hold", ""], ktr)}</section>')

HL = 'grid-template-columns:minmax(0,1.4fr) minmax(0,1.3fr) 120px minmax(0,1.3fr) 24px'
kholds = [('QH-0031', 'Lead trip TRIP-0007 · 22 Nov', '256 bags + 14 sachets, T5 2.3 m³', ('Open', 'amber'), 'L1 waiting on lab · L2 scrap · L3 reprocess', 'QualityHold.dc.html'),
          ('QH-0030', 'Coliform plate failed · 18 Nov', '40 bags · 800 sachets', ('Closed', 'gray'), 'Scrapped · signed Grace O.', None),
          ('QH-0029', 'Lead trip TRIP-0006 · 14 Nov', '430 bags · 8,600 sachets', ('Closed', 'gray'), '310 released with deviation (Tunde B.), 120 scrapped', None)]
khr = [row(HL, [c2(i, t), f'<span class="c tab" style="color:var(--ink-gray-8)">{q}</span>', f'<span>{bd(*s)}</span>', f'<span class="c qs">{n}</span>', f'<span style="color:var(--ink-gray-4);display:flex">{ic("chev-r","i s35")}</span>'], h, 56) for i, t, q, s, n, h in kholds]
pl('HoldList.dc.html', 'HoldList.dc.html', crumb(*K, ('Quality holds', None)), f'{btn("Hold product","plus")}',
   kpis(('Open', '1', 'QH-0031', 'var(--ink-amber-7)'), ('Held this month', '726 bags', '14,520 sachets · plus T5 water', ''), ('Released', '310 bags', '43% of held', ''), ('Scrapped', '160 bags', 'plus 156 bags in L2 if confirmed', '')) +
   f'<section style="display:flex;flex-direction:column;gap:12px">{lst(HL, ["Hold", "Held", "State", "Outcome", ""], khr)}<p class="qs" style="margin:0">A bag is 20 sachets of 50 cl. Hold product by hand with the button above, for a complaint or a failed routine check.</p></section>')

HH = 'grid-template-columns:150px minmax(0,1fr) 200px 140px 24px'
hos = [('22 Nov · 14:00', 'Morning to afternoon', 'Musa A. → Bola N.', ('Draft', 'amber'), 'Handover.dc.html'),
       ('22 Nov · 06:00', 'Night to morning', 'Ibrahim K. → Musa A.', ('Signed 06:04', 'gray'), None),
       ('21 Nov · 22:00', 'Afternoon to night', 'Bola N. → Ibrahim K.', ('Signed 22:06', 'gray'), None),
       ('21 Nov · 14:00', 'Morning to afternoon', 'Musa A. → Bola N.', ('Signed 14:02', 'gray'), None),
       ('21 Nov · 06:00', 'Night to morning', 'Ibrahim K. → Musa A.', ('Signed 06:11', 'gray'), None)]
hhr = [row(HH, [f'<span class="tab">{t}</span>', f'<span class="t1">{s}</span>', f'<span class="qs" style="color:var(--ink-gray-7)">{w}</span>', f'<span>{bd(*st)}</span>', f'<span style="color:var(--ink-gray-4);display:flex">{ic("chev-r","i s35")}</span>'], h) for t, s, w, st, h in hos]
pl('HandoverHistory.dc.html', 'HandoverHistory.dc.html', crumb(*K, ('Shift handover', 'Handover.dc.html'), ('All handovers', None)), btn("Export","download","ghost"),
   f'<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h2">Handovers</h2><span class="qs">Each one is signed by the outgoing supervisor; open items carry over as ToDos</span></div>{lst(HH, ["Shift change", "Handover", "From → to", "State", ""], hhr)}</section>')

# ---------------- Pinned tags (Koyo 1)
pins = [('AT-401 Lead', 'µg/L · trip at 8'), ('AT-301 pH', 'band 7.8 – 8.3'), ('AT-302 Conductivity', 'µS/cm · band 150 – 220'), ('AT-303 Turbidity', 'NTU · trip at 4'), ('UV-301 Intensity', '% · trip below 70'), ('FT-201 Permeate', 'm³/h')]
pinl = ''.join(f'<div style="display:grid;grid-template-columns:20px 24px minmax(0,1fr) 28px;gap:8px;align-items:center;height:48px;padding:0 10px;border-bottom:1px solid var(--outline-gray-1)"><span style="color:var(--ink-gray-4);display:flex">{ic("grip","i s35") if "grip" in IC else "⋮⋮"}</span><span class="tab qs">{i+1}</span><span class="c"><div class="t1">{n}</div><div class="m">{m}</div></span><span style="color:var(--ink-gray-5);display:flex">{ic("x","i s35")}</span></div>' for i, (n, m) in enumerate(pins))
cand = [('LT-201 T2 level', 'm³', False), ('LT-101 T1 level', 'm³', False), ('PT-201 HP pump outlet', 'bar', False), ('DP-102 Carbon filter ΔP', 'bar', True), ('F1 – F10 rate', 'sachets/h', False), ('G-1 Diesel level', 'L', False), ('TT-F1 … F10 jaw temp', '°C', False)]
candl = ''.join(f'<label style="display:flex;align-items:center;gap:10px;height:40px;padding:0 10px;border-bottom:1px solid var(--outline-gray-1);font-size:14px"><span class="cb{" on" if on else ""}"></span><span style="flex:1;color:var(--ink-gray-8)">{n}</span><span class="qs">{u}</span></label>' for n, u, on in cand)
pl('PinnedTags.dc.html', 'PinnedTags.dc.html', crumb(*K, ('Pinned tags', None)), f'{btn("Cancel",kind="ghost")}<a href="Main.dc.html" class="btn solid">Save</a>',
   f'''<div style="display:flex;flex-direction:column;gap:4px"><h2 class="h2">Pinned tags on the plant screen</h2><p class="ps">Up to 6 cards across the top of Koyo 1. Drag to reorder. Each card shows the live value, unit and its limit.</p></div>
<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;align-items:start">
<section class="card" style="padding:0;display:flex;flex-direction:column"><div style="display:flex;justify-content:space-between;align-items:center;padding:12px 14px;border-bottom:1px solid var(--outline-gray-1)"><span class="h3">Pinned · 6 of 6</span><span class="qs">Remove one to add another</span></div>{pinl}</section>
<section class="card" style="padding:0;display:flex;flex-direction:column"><div style="padding:12px 14px;border-bottom:1px solid var(--outline-gray-1);display:flex;flex-direction:column;gap:10px"><span class="h3">Add a tag</span><span class="in muted">{ic("search")}<span class="grow">Search 148 tags at Koyo 1</span></span></div>{candl}
<div style="padding:12px 14px" class="qs">DP-102 is ticked but cannot be added while 6 are pinned.</div></section></div>
{section_pin()}''' if False else
   f'''<div style="display:flex;flex-direction:column;gap:4px"><h2 class="h2">Pinned tags on the plant screen</h2><p class="ps">Up to 6 cards across the top of Koyo 1. Drag to reorder. Each card shows the live value, unit and its limit.</p></div>
<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;align-items:start">
<section class="card" style="padding:0;display:flex;flex-direction:column"><div style="display:flex;justify-content:space-between;align-items:center;padding:12px 14px;border-bottom:1px solid var(--outline-gray-1)"><span class="h3">Pinned · 6 of 6</span><span class="qs">Remove one to add another</span></div>{pinl}</section>
<section class="card" style="padding:0;display:flex;flex-direction:column"><div style="padding:12px 14px;border-bottom:1px solid var(--outline-gray-1);display:flex;flex-direction:column;gap:10px"><span class="h3">Add a tag</span><span class="in muted">{ic("search")}<span class="grow">Search 148 tags at Koyo 1</span></span></div>{candl}
<div style="padding:12px 14px" class="qs">DP-102 is ticked but cannot be added while 6 are pinned.</div></section></div>
<section style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">Who sees this</h3><div style="display:flex;flex-direction:column;gap:2px">
<label style="display:flex;align-items:center;gap:8px;height:28px;font-size:14px"><span class="rd on"></span>Everyone at Koyo 1 <span class="qs">· needs Factory Manager</span></label>
<label style="display:flex;align-items:center;gap:8px;height:28px;font-size:14px"><span class="rd"></span>Only me</label></div></section>''')

# ---------------- Quality hold template editor (company setup)
QT = 'grid-template-columns:minmax(0,1.3fr) 130px minmax(0,1fr) 130px 120px 24px'
tests = [('Lead in finished sachets', 'Portable ASV meter', '3 per lot, different fillers', 'Under 5 µg/L', 'Every lot'),
         ('Lead in finished sachets', 'ICP-MS, outside lab', '1 per hold', 'Under 5 µg/L', 'Result within 48 h'),
         ('Lead at SP-1 for line release', 'Portable ASV meter', '2, at least 10 min apart', 'Under 3 µg/L', 'Before QA release')]
tr2 = ''.join(f'<div class="lr" style="{QT};cursor:default;min-height:48px"><span class="t1">{a}</span><span class="qs" style="color:var(--ink-gray-7)">{b}</span><span class="c qs" style="color:var(--ink-gray-7)">{c}</span><span class="tab">{d}</span><span class="qs">{e}</span><span style="color:var(--ink-gray-4);display:flex">{ic("more","i s35")}</span></div>' for a, b, c, d, e in tests)
def drow(name, on, note):
    return f'<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-top:1px solid var(--outline-gray-1)"><span class="cb{" on" if on else ""}"></span><span style="flex:1;display:flex;flex-direction:column;gap:2px"><span style="font-size:14px;color:var(--ink-gray-8)">{name}</span><span class="qs">{note}</span></span></div>'
qht_body = f'''<div style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:24px;align-items:start">
<div style="display:flex;flex-direction:column;gap:24px">
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px">
{field('Name', inp('Lead trip, sachet water', 'out'), req=True)}{field('Opens on', sel('Interlock IL-01 Lead high-high', 'out'), hint='Or an alarm rule marked "places a quality hold", or by hand.')}
{field('Hold window starts', sel('Last passing check before the fault', 'out'))}{field('Split lots where', sel('The checkpoint crosses its alert limit', 'out'))}
{field('Count lots in', sel('Sachets, shown as bags of 20 + loose sachets', 'out'))}{field('Hold tanks whole', inp('<span class="chip" style="height:20px">T4 verify</span> <span class="chip" style="height:20px">T5 quarantine</span>', 'out'))}</div>
<section style="display:flex;flex-direction:column;gap:8px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h3">Tests</h2>{btn("Add test","plus","ghost")}</div>
<div class="list" style="margin:0"><div class="lh" style="{QT}"><span>Test</span><span>Method</span><span>Samples</span><span>Pass if</span><span>When</span><span></span></div>{tr2}</div></section>
<section style="display:flex;flex-direction:column"><h2 class="h3" style="margin-bottom:6px">Decisions QA may take on a lot</h2>
{drow('Release', True, 'Only when every sample of the lot passes')}
{drow('Release with deviation', True, 'Also needs a Factory Manager, who is not the inspector')}
{drow('Rework or reprocess', True, 'Tanks only: back through IX-501. Not offered for sealed sachets')}
{drow('Scrap', True, 'Default when any sample of the lot fails')}</section>
</div>
<aside class="card" style="display:flex;flex-direction:column;gap:12px"><div class="divy" style="font-size:13px">
<div class="prow"><span>Template</span><span>QHT-003</span></div><div class="prow"><span>Process template</span><span><a href="CompanyTemplates.dc.html">Sachet water v3</a></span></div>
<div class="prow"><span>Used by</span><span>Koyo 1, Plant B, Plant D</span></div><div class="prow"><span>Last used</span><span><a href="QualityHold.dc.html">QH-0031</a> · today</span></div>
<div class="prow"><span>Edited</span><span>3 Nov · Tunde B.</span></div></div>
<p class="qs" style="margin:0;line-height:1.5">Plants keep their own copy. Push changes to them from here; each plant's Factory Manager accepts.</p>{btn("Push to 3 plants")}</aside></div>'''
co('QHTemplate.dc.html', 'QHTemplate.dc.html', crumb(('Process templates', 'CompanyTemplates.dc.html'), ('Sachet water', 'CompanyTemplates.dc.html'), ('QHT-003 Lead trip', None)), f'{btn("Discard",kind="ghost")}<button type="button" class="btn solid">Save</button>', qht_body)
