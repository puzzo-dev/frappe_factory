from ff import *

COLS = 'grid-template-columns:16px 84px minmax(0,1fr) 104px 132px 76px'

rows = [
  # prio, prio cls, title, meta, value, limit, state, state cls, time, dur, unack, active
  ('1', 's-red', 'AT-401 Lead trip', 'AT-401 · Polishing · interlock', '9.4 µg/L', 'trip ≥ 8', 'Acknowledged', 'gray', '08:14', '32 min', False, False),
  ('2', 's-amber', 'T4 failed verification', 'SP-2 grab sample · Verification', '6.1 µg/L', 'alert ≥ 5', 'Unacknowledged', 'red', '08:26', '20 min', True, True),
  ('3', 'amber', 'DP-102 Carbon filter ΔP high', 'DP-102 · Pretreatment', '1.3 bar', 'alert ≥ 1.2', 'Acknowledged', 'gray', '07:52', '54 min', False, False),
  ('3', 'amber', 'Diesel runway under 48 h', 'LT-901 · Utilities', '41 h', 'alert < 48 h', 'Acknowledged', 'gray', '06:10', '2 h 36 min', False, False),
]

def prio(p, c):
    return f'<span class="bd {c}" style="min-width:24px;justify-content:center">P{p}</span>'

def row(r):
    p, pc, t, m, v, lim, s, sc, tm, dur, unack, act = r
    cls = ' act' if act else ''
    tcls = ' b' if unack else ''
    return f'''<div class="lr{cls}" style="{COLS};min-height:56px">
<span class="cb" aria-hidden="true"></span>
<span>{prio(p, pc)}</span>
<span class="c"><div class="t1{tcls}">{t}</div><div class="m">{m}</div></span>
<span class="c r tab" style="display:flex;flex-direction:column;align-items:flex-end"><span style="color:var(--ink-gray-8)">{v}</span><span class="m" style="margin-top:4px">{lim}</span></span>
<span>{bd(s, sc)}</span>
<span class="r tab" style="display:flex;flex-direction:column;align-items:flex-end"><span>{tm}</span><span class="m" style="margin-top:4px">{dur}</span></span>
</div>'''

shelved_row = f'''<div class="lr" style="{COLS};min-height:56px;opacity:.75">
<span class="cb" aria-hidden="true"></span><span>{bd('P3','gray')}</span>
<span class="c"><div class="t1">F9 jaw temperature low</div><div class="m">TT-F9 · Filling · shelved by Musa A. for maintenance</div></span>
<span class="c r tab" style="display:flex;flex-direction:column;align-items:flex-end"><span>96 °C</span><span class="m" style="margin-top:4px">alert &lt; 130</span></span>
<span>{bd('Shelved','violet')}</span>
<span class="r tab" style="display:flex;flex-direction:column;align-items:flex-end"><span>until 12:00</span><span class="m" style="margin-top:4px">3 h 14 min</span></span>
</div>'''

trend = [3.1,3.0,3.2,3.4,3.3,3.6,3.9,4.2,4.6,5.2,5.8,6.1,6.0,6.1]
chart = spark(trend, 280, 64, 'var(--ink-gray-8)', 0, 9, lines=((5, 'var(--ink-amber-7)'), (8, 'var(--ink-red-7)')))

panel = f'''<aside class="panel" aria-label="Selected alarm">
<div style="display:flex;align-items:center;justify-content:space-between;height:48px;padding:0 16px;border-bottom:1px solid var(--outline-gray-1)">
<div style="display:flex;align-items:center;gap:6px">{prio('2','s-amber')}{bd('Unacknowledged','red')}</div>
<div style="display:flex;gap:4px">{btn(icon='ext', kind='ghost', attrs='Open on plant screen')}{btn(icon='x', kind='ghost', attrs='Close')}</div>
</div>
<div style="flex:1;overflow:auto;padding:16px;display:flex;flex-direction:column;gap:20px">
<div style="display:flex;flex-direction:column;gap:6px">
<h2 class="h2">T4 failed verification</h2>
<p class="ps">The grab sample from the verification tank read over the alert limit, so this batch cannot go to the fillers.</p>
</div>
<div class="inset" style="display:flex;flex-direction:column;gap:8px">
<div style="display:flex;align-items:baseline;justify-content:space-between"><span class="qs">SP-2 lead, last 70 min</span><span class="tab" style="font-size:20px;font-weight:600;color:var(--ink-gray-9)">6.1 <span class="qs" style="font-weight:400">µg/L</span></span></div>
{chart}
<div style="display:flex;gap:12px" class="qs"><span style="display:inline-flex;align-items:center;gap:4px"><i style="width:12px;border-top:1px dashed var(--ink-amber-7)"></i>Alert 5</span><span style="display:inline-flex;align-items:center;gap:4px"><i style="width:12px;border-top:1px dashed var(--ink-red-7)"></i>Trip 8</span><span style="margin-left:auto">07:36 – 08:46</span></div>
</div>
<div class="divy">
<div class="prow"><span>Tag</span><span>SP-2 · AT-402 grab</span></div>
<div class="prow"><span>Definition</span><span><a href="AlarmDefs.dc.html">ALD-0014 · Verification high</a></span></div>
<div class="prow"><span>Area</span><span>Verification · T4</span></div>
<div class="prow"><span>Raised</span><span class="tab">08:26 · 20 min ago</span></div>
<div class="prow"><span>Linked trip</span><span><a href="Trip.dc.html">TRIP-0007 · AT-401</a></span></div>
</div>
<div style="display:flex;flex-direction:column;gap:10px">
<h3 class="h3">What to do</h3>
<div class="divy" style="font-size:13px;line-height:1.5;color:var(--ink-gray-7)">
<div style="padding:0 0 8px"><span class="qs">Likely cause</span><br>Water that passed SP-1 before the trip reached T4.</div>
<div style="padding:8px 0"><span class="qs">If ignored</span><br>Contaminated water reaches the sachets.</div>
<div style="padding:8px 0 0"><span class="qs">Action</span><br>Keep XV-402 open to T5. Do not release T4. Take a second sample after T4 is drained and rinsed.</div>
</div>
<span class="qs">Respond within 15 min · from the alarm definition</span>
</div>
<div style="display:flex;flex-direction:column;gap:10px">
<h3 class="h3">Activity</h3>
<div class="tline">
<div class="ev"><span class="ic">{ic('msg')}</span><span><b>WhatsApp</b> to Floor Supervisor on duty, delivered <span class="w">· 08:26</span></span></div>
<div class="ev"><span class="ic">{ic('bell')}</span><span>Raised from Quality Inspector entry by <b>Grace O.</b> <span class="w">· 08:26</span></span></div>
</div>
</div>
</div>
<div style="display:flex;gap:8px;padding:12px 16px;border-top:1px solid var(--outline-gray-1)">
<button type="button" class="btn solid" style="flex:1">{ic('check')}Acknowledge</button>
<button type="button" class="btn">{ic('bell-off')}Shelve</button>
{btn(icon='more', attrs='More actions')}
</div>
</aside>'''

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Alarms',None)),
  f'<span class="bd gray"><span class="dot g"></span>Live · 2 s</span>{btn("Export", "download", "ghost")}')

tabs = f'''<div class="tabs" role="tablist">
<span class="t on" role="tab" aria-selected="true">Active <span class="bd gray">4</span></span>
<span class="t" role="tab">Shelved <span class="bd gray">1</span></span>
<span class="t" role="tab">History</span>
</div>'''

toolbar = f'''<div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap">
<div style="display:flex;align-items:center;gap:8px">
<span class="in muted" style="width:220px">{ic('search')}<span class="grow">Search tag or message</span></span>
<button type="button" class="btn">{ic('filter')}Filter</button>
<span class="chip"><span class="k">Area</span>All</span>
<span class="chip"><span class="k">Priority</span>All</span>
</div>
<span class="qs">Alarm rate: 1 in the last 10 min · target 1 or fewer</span>
</div>'''

listv = f'''<div class="list" role="table" aria-label="Active alarms">
<div class="lh" style="{COLS}" role="row"><span class="cb" aria-hidden="true"></span><span class="sort">Priority{ic('chev-d','i s35')}</span><span>Alarm</span><span class="r" style="display:flex">Value</span><span>State</span><span class="r" style="display:flex">Raised</span></div>
{''.join(row(r) for r in rows)}
</div>
<p class="qs" style="margin:0">Sorted by priority, then unacknowledged first. Cleared alarms that were never acknowledged stay here until someone acknowledges them.</p>'''

content = f'''<div style="display:flex;flex:1;min-height:0">
<div style="flex:1;min-width:0;display:flex;flex-direction:column">
{tabs}
<div class="body" style="gap:16px;padding-top:16px">{toolbar}{listv}</div>
</div>
{panel}
</div>'''

write('Alarms.dc.html', page('Alarms', shell('Alarms.dc.html', head, content), {"$preview": {"width": 1440, "height": 900}}))
