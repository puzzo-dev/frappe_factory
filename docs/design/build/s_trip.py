from ff import *

# AT-401 lead, 1-min points 07:46 -> 08:46 (trip at 08:14 = index 28)
lead = [1.3,1.4,1.3,1.5,1.4,1.4,1.6,1.5,1.7,1.8,2.0,2.3,2.6,3.0,3.4,3.9,4.4,5.0,5.5,6.1,6.6,7.1,7.4,7.8,8.0,8.3,8.7,9.1,9.4,9.3,9.0,8.6,8.1,7.5,6.8,6.0,5.2,4.5,3.9,3.4,3.0,2.7,2.5,2.3,2.2,2.1,2.0,2.0,1.9,1.9,1.8,1.8,1.8,1.7,1.7,1.7,1.6,1.6,1.6,1.6,1.6]

def trend_svg():
    W, H, L, R, T, B = 720, 196, 36, 8, 24, 22
    pw, ph_ = W-L-R, H-T-B
    y = lambda v: T + ph_ - v/10*ph_
    x = lambda i: L + i*pw/(len(lead)-1)
    pts = ' '.join(f'{x(i):.1f},{y(v):.1f}' for i, v in enumerate(lead))
    grid = ''.join(f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="var(--outline-gray-1)"/><text x="{L-8}" y="{y(v)+4:.1f}" text-anchor="end" font-size="11" fill="var(--ink-gray-5)">{v}</text>' for v in (0, 2, 4, 6, 8, 10))
    ticks = ''.join(f'<text x="{x(i):.1f}" y="{H-4}" text-anchor="{'end' if i==60 else ('start' if i==0 else 'middle')}" font-size="11" fill="var(--ink-gray-5)">{lab}</text>' for i, lab in ((0,'07:46'),(14,'08:00'),(28,'08:14'),(44,'08:30'),(60,'08:46')))
    lim = (f'<line x1="{L}" x2="{W-R}" y1="{y(8):.1f}" y2="{y(8):.1f}" stroke="var(--ink-red-7)" stroke-dasharray="4 4"/><text x="{W-R}" y="{y(8)-5:.1f}" text-anchor="end" font-size="11" fill="var(--ink-red-7)">Trip 8</text>'
           f'<line x1="{L}" x2="{W-R}" y1="{y(5):.1f}" y2="{y(5):.1f}" stroke="var(--ink-amber-7)" stroke-dasharray="4 4"/><text x="{W-R}" y="{y(5)-5:.1f}" text-anchor="end" font-size="11" fill="var(--ink-amber-7)">Alert 5</text>'
           f'<line x1="{L}" x2="{W-R}" y1="{y(3):.1f}" y2="{y(3):.1f}" stroke="var(--ink-gray-5)" stroke-dasharray="2 4"/><text x="{W-R}" y="{y(3)-5:.1f}" text-anchor="end" font-size="11" fill="var(--ink-gray-5)">Reset under 3</text>')
    tx = x(28)
    mark = (f'<rect x="{tx:.1f}" y="{T}" width="{W-R-tx:.1f}" height="{ph_}" fill="var(--surface-red-2)" opacity=".55"/>'
            f'<line x1="{tx:.1f}" x2="{tx:.1f}" y1="{T}" y2="{T+ph_}" stroke="var(--ink-red-7)"/>'
            f'<circle cx="{tx:.1f}" cy="{y(9.4):.1f}" r="3.5" fill="var(--surface-base)" stroke="var(--ink-red-7)" stroke-width="1.5"/>'
            f'<text x="{tx:.1f}" y="12" text-anchor="middle" font-size="11" font-weight="500" fill="var(--ink-red-7)">Trip 08:14 · 9.4</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="AT-401 lead from 07:46 to 08:46. Rose past the trip limit of 8 at 08:13, peaked at 9.4 at 08:14, now 1.6." style="display:block">{mark}{grid}{lim}<polyline points="{pts}" fill="none" stroke="var(--ink-gray-8)" stroke-width="1.75" stroke-linejoin="round"/>{ticks}</svg>'

def step(n, state, title, meta, body=''):
    if state == 'done':
        mk = f'<span style="width:24px;height:24px;border-radius:50%;background:var(--surface-gray-10);color:var(--ink-base);display:grid;place-items:center">{ic("check","i s35")}</span>'
    elif state == 'now':
        mk = f'<span style="width:24px;height:24px;border-radius:50%;border:1.5px solid var(--ink-gray-9);color:var(--ink-gray-9);display:grid;place-items:center;font-size:12px;font-weight:600">{n}</span>'
    elif state == 'wait':
        mk = f'<span style="width:24px;height:24px;border-radius:50%;border:1px dashed var(--outline-gray-3);color:var(--ink-gray-5);display:grid;place-items:center;font-size:12px">{n}</span>'
    else:
        mk = f'<span style="width:24px;height:24px;border-radius:50%;background:var(--surface-gray-2);color:var(--ink-gray-5);display:grid;place-items:center;font-size:12px">{n}</span>'
    last = n == 7
    line = '' if last else '<span style="position:absolute;left:11.5px;top:30px;bottom:-6px;width:1px;background:var(--outline-gray-2)"></span>'
    tcol = 'var(--ink-gray-5)' if state in ('todo','wait') else 'var(--ink-gray-9)'
    b = f'<div style="margin-top:12px">{body}</div>' if body else ''
    pad = '' if last else 'padding-bottom:24px;'
    return f'''<li style="position:relative;display:grid;grid-template-columns:24px minmax(0,1fr);gap:12px;{pad}">{line}{mk}
<div style="min-width:0;padding-top:2px"><div style="display:flex;align-items:center;justify-content:space-between;gap:8px"><span style="font-size:14px;font-weight:600;color:{tcol}">{title}</span><span class="qs tab" style="white-space:nowrap">{meta}</span></div>{b}</div></li>'''

check_rows = ''.join(f'<div style="display:flex;align-items:center;gap:8px;height:28px;font-size:13px;color:var(--ink-gray-7)"><span style="color:var(--ink-green-7);display:inline-flex">{ic("check","i s35")}</span><span style="flex:1">{a}</span><span class="tab" style="color:var(--ink-gray-5)">{b}</span></div>' for a, b in (
  ('Filler run permissive off (PLC)', 'IL-01.PERM = 0'),
  ('XV-301 routed to T5 quarantine', 'ZS-301 = T5'),
  ('XV-402 open to T5', 'ZS-402 = open'),
  ('Return loop P-501 → IX-501 → T1 running', 'P-501 = run')))
s1 = f'<div class="inset" style="padding:4px 12px">{check_rows}</div><p class="qs" style="margin:8px 0 0">Checked from live tags. Nothing to do here.</p>'

s2 = f'''<div class="inset" style="padding:4px 12px">
<div style="display:flex;align-items:center;gap:8px;height:28px;font-size:13px;color:var(--ink-gray-7)"><span style="color:var(--ink-green-7);display:inline-flex">{ic("check","i s35")}</span><span style="flex:1">T4 drained to T5</span><span class="tab" style="color:var(--ink-gray-5)">LT-401 0.02 m³ · 08:31</span></div>
<div style="display:flex;align-items:center;gap:8px;height:28px;font-size:13px;color:var(--ink-gray-7)"><span style="color:var(--ink-green-7);display:inline-flex">{ic("check","i s35")}</span><span style="flex:1">T4 rinsed with permeate</span><span class="tab" style="color:var(--ink-gray-5)">Musa A. · 08:38</span></div>
</div>'''

sample1 = f'''<div style="display:grid;grid-template-columns:20px minmax(0,1fr) auto;align-items:center;gap:8px;padding:10px 12px;border:1px solid var(--outline-gray-1);border-radius:8px">
<span style="color:var(--ink-green-7);display:inline-flex">{ic("check-c")}</span>
<span><span style="color:var(--ink-gray-8)">Sample 1 · SP-1 · <b class="tab" style="font-weight:600">2.1 µg/L</b></span><br><span class="qs">Grace O. · taken 08:36 · ICP-MS lab result · certificate attached</span></span>
<span class="bd green">Under 3</span></div>'''

sample2 = f'''<div style="display:flex;flex-direction:column;gap:12px;padding:12px;border:1px solid var(--outline-gray-2);border-radius:8px;box-shadow:var(--shadow-sm)">
<div style="display:flex;align-items:center;justify-content:space-between"><span style="font-weight:500;color:var(--ink-gray-8)">Sample 2</span><span class="qs">Take at least 10 min after sample 1</span></div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">
{field('Result', inp('<span class="tab">1.8</span>', 'focus', right='<span class="qs">µg/L</span>'), req=True)}
{field('Sample point', sel('SP-1 · after UV'), req=True)}
{field('Taken at', inp('<span class="tab">08:47</span>', icon='clock'), req=True)}
</div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;align-items:end">
{field('Method', sel('Portable ASV meter'))}
<div class="fl" style="grid-column:span 2"><span class="lab">Certificate or photo</span><span class="in" style="border:1px dashed var(--outline-gray-3);background:var(--surface-base)">{ic('paperclip')}<span class="grow" style="color:var(--ink-gray-5)">Drop a file or <a href="#">browse</a></span></span></div>
</div>
<div style="display:flex;align-items:center;justify-content:space-between;gap:8px"><span class="qs" style="display:inline-flex;align-items:center;gap:6px">{ic('info','i s35')}Logged as Quality Inspection QI-0931, linked to this trip.</span>{btn('Save result','check')}</div>
</div>'''
s3 = f'<div style="display:flex;flex-direction:column;gap:8px">{sample1}{sample2}</div>'

s4 = f'''<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px">
{field('Cause', sel('Choose a cause', ph=True), req=True)}
{field('Found by', sel('Musa A.'))}
<div style="grid-column:span 2">{field('What happened', inp('Borehole pump restarted after the 07:40 power dip; T1 stirred up sediment…', 'ta', ph=True), hint='Shown in the trip report and the next shift handover.')}</div>
</div>'''

s5 = f'''<div class="alert" style="background:var(--surface-gray-1);border-color:var(--outline-gray-1)"><span class="ai" style="color:var(--ink-gray-6)">{ic('key')}</span>
<div style="display:flex;flex-direction:column;gap:4px;font-size:13px;line-height:1.5;color:var(--ink-gray-7)"><span class="ttl" style="font-size:14px">Reset at panel LCP-1</span>Frappe Factory cannot reset an interlock. After QA release, a supervisor turns the key at the panel. The PLC accepts it only if AT-401 has stayed under 3 µg/L for 10 min.
<span class="tab" style="display:flex;gap:16px;margin-top:4px"><span>KS-401 <b style="font-weight:500;color:var(--ink-gray-8)">Not reset</b></span><span>AT-401 under 3 for <b style="font-weight:500;color:var(--ink-gray-8)">8 of 10 min</b></span></span></div></div>'''

s_qa = f'''<div style="display:flex;flex-direction:column;gap:10px">
<p class="ps">The Quality Inspector decides whether filling may continue, on the lab results, not on the analyser reading. AT-401 back under the limit does not count: the analyser itself may be the fault.</p>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px">
<label style="display:flex;gap:8px;align-items:flex-start;padding:10px 12px;border-radius:8px;border:1px solid var(--outline-gray-2)"><span class="rd" style="margin-top:1px"></span><span style="display:flex;flex-direction:column;gap:2px"><span style="font-weight:500;color:var(--ink-gray-8)">Release the line</span><span class="qs" style="font-size:12px">Both results under 3 µg/L</span></span></label>
<label style="display:flex;gap:8px;align-items:flex-start;padding:10px 12px;border-radius:8px;border:1px solid var(--outline-gray-2)"><span class="rd" style="margin-top:1px"></span><span style="display:flex;flex-direction:column;gap:2px"><span style="font-weight:500;color:var(--ink-gray-8)">More samples</span><span class="qs" style="font-size:12px">Adds a sample step</span></span></label>
<label style="display:flex;gap:8px;align-items:flex-start;padding:10px 12px;border-radius:8px;border:1px solid var(--outline-gray-2)"><span class="rd" style="margin-top:1px"></span><span style="display:flex;flex-direction:column;gap:2px"><span style="font-weight:500;color:var(--ink-gray-8)">Keep the line stopped</span><span class="qs" style="font-size:12px">Escalates to Factory Manager</span></span></label></div>
<div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><span class="qs">The product made around the trip is judged separately in <a href="QualityHold.dc.html">QH-0031</a>.</span><button type="button" class="btn" disabled>{ic('lock')}QA release · user and PIN</button></div></div>'''
s6 = f'''<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap"><span class="qs">Floor Supervisor. Allowed only after QA release and the key reset. Closes the trip, ends Machine Stop MS-0412 and lets the fillers run.</span>
<button type="button" class="btn solid" disabled>Restart and close trip</button></div>'''

steps = '<ol style="list-style:none;margin:0;padding:0">' + ''.join([
  step(1, 'done', 'Line stopped and water diverted', '08:14 · automatic', s1),
  step(2, 'done', 'Drain and rinse T4', 'Floor Supervisor · 08:38', s2),
  step(3, 'now', 'Two lab results under 3 µg/L', 'Quality Inspector · 1 of 2', s3),
  step(4, 'todo', 'Record the cause', 'Floor Supervisor', s4),
  step(5, 'wait', 'QA release', 'Quality Inspector', s_qa),
  step(6, 'wait', 'Key reset at the panel', 'Floor Supervisor at LCP-1', s5),
  step(7, 'todo', 'Restart the line', 'Floor Supervisor', s6),
]) + '</ol>'

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Interlock trips','#'),('TRIP-0007',None)),
  f'{bd("Tripped · 32 min","s-red")}{btn("Report","file","ghost")}{btn(icon="more",kind="ghost",attrs="More")}')

banner = f'''<div class="alert red" style="border-color:var(--outline-red-3);background:var(--surface-red-2)"><span class="ai">{ic('octagon')}</span>
<div style="display:flex;flex-direction:column;gap:4px"><span class="ttl">Filling stopped by the lead interlock at 08:14</span>
<span style="font-size:13px;line-height:1.5;color:var(--ink-gray-7)">AT-401 read 9.4 µg/L against a trip limit of 8. Treated water is going to T5 quarantine and back through the resin. Filling restarts only after a Quality Inspector releases the line on lab results and a supervisor resets the key at the panel.</span></div></div>'''

trendcard = f'''<section class="card" aria-labelledby="tr-h" style="display:flex;flex-direction:column;gap:12px">
<div style="display:flex;align-items:center;justify-content:space-between"><h2 id="tr-h" class="h3">AT-401 lead · µg/L</h2><div class="seg"><span>8 h</span><span class="on">1 h</span><span>15 min</span></div></div>
{trend_svg()}
</section>'''

maincol = f'''<div style="flex:1;min-width:0;overflow:auto"><div class="body" style="max-width:820px;margin:0 auto">
{banner}{trendcard}
<section aria-labelledby="st-h" style="display:flex;flex-direction:column;gap:16px"><div style="display:flex;align-items:baseline;justify-content:space-between"><h2 id="st-h" class="h2">Recovery steps</h2><span class="qs">2 of 7 done</span></div>{steps}</section>
</div></div>'''

panel = f'''<aside class="panel" aria-label="Trip details"><div style="padding:16px;display:flex;flex-direction:column;gap:20px;overflow:auto">
<div class="divy">
<div class="prow"><span>Interlock</span><span>IL-01 · Lead high-high</span></div>
<div class="prow"><span>Trigger</span><span class="tab">AT-401 9.4 ≥ 8.0 µg/L</span></div>
<div class="prow"><span>Tripped at</span><span class="tab">22 Nov · 08:14:06</span></div>
<div class="prow"><span>Duration</span><span class="tab">32 min</span></div>
<div class="prow"><span>Fillers</span><span>9 stopped · F9 in maintenance</span></div>
<div class="prow"><span>Output lost</span><span class="tab">about 480 bags so far · 9,600 sachets</span></div>
<div class="prow"><span>Downtime</span><span><a href="Downtime.dc.html">MS-0412 · Quality hold</a></span></div>
<div class="prow"><span>Quality hold</span><span><a href="QualityHold.dc.html">QH-0031 · 256 bags, 14 sachets, T5</a></span></div>
</div>
<div style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">Quarantine</h3>
<div class="inset" style="display:flex;flex-direction:column;gap:10px">
<div style="display:flex;justify-content:space-between;font-size:13px"><span style="color:var(--ink-gray-7)">T5 level</span><span class="tab" style="color:var(--ink-gray-8)">2.3 of 5 m³</span></div><span class="bar"><i style="width:46%"></i></span>
<div style="display:flex;justify-content:space-between;font-size:13px"><span style="color:var(--ink-gray-7)">IX-501 resin used</span><span class="tab" style="color:var(--ink-gray-8)">12%</span></div><span class="bar"><i style="width:12%"></i></span>
<span class="qs">At the current inflow T5 is full in 1 h 10 min.</span></div></div>
<div style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">On this trip</h3>
<div style="display:flex;align-items:center;gap:8px"><span class="avs"><span class="av md">MA</span><span class="av md">GO</span><span class="av md">TB</span></span><span class="qs">Musa A., Grace O., Tunde B.</span></div></div>
<div style="display:flex;flex-direction:column;gap:10px"><h3 class="h3">Activity</h3><div class="tline">
<div class="ev"><span class="ic">{ic('flask')}</span><span><b>Grace O.</b> logged sample 1, 2.1 µg/L <span class="w">· 08:40</span></span></div>
<div class="ev"><span class="ic">{ic('check')}</span><span><b>Musa A.</b> marked T4 rinsed <span class="w">· 08:38</span></span></div>
<div class="ev"><span class="ic">{ic('msg')}</span><span><b>WhatsApp</b> to Tunde B. (Factory Manager), read <span class="w">· 08:15</span></span></div>
<div class="ev"><span class="ic">{ic('check')}</span><span><b>Musa A.</b> acknowledged the trip alarm <span class="w">· 08:15</span></span></div>
<div class="ev"><span class="ic" style="background:var(--surface-red-2);color:var(--ink-red-7)">{ic('octagon')}</span><span>PLC tripped IL-01 <span class="w">· 08:14</span></span></div>
</div></div>
</div></aside>'''

content = f'<div style="display:flex;flex:1;min-height:0">{maincol}{panel}</div>'
write('Trip.dc.html', page('TRIP-0007', shell('Trip.dc.html', head, content), {"$preview": {"width": 1440, "height": 900}}))
