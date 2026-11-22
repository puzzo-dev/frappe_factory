from ff import *

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Shift handover','#'),('Morning to afternoon',None)),
  f'{bd("Draft","gray")}<span class="qs">Saved 08:44</span><button type="button" class="btn solid">Submit handover</button>')

def fig(k, v, d, ink=''):
    st = f'color:{ink}' if ink else ''
    return f'<div class="kpi"><span class="k">{k}</span><span class="v" style="font-size:18px;{st}">{v}</span><span class="d">{d}</span></div>'

summary = f'''<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h2">This shift so far</h2><span class="qs">Filled in from the plant · updates until you submit · as of 08:46</span></div>
<div class="card" style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px">
{fig('Good output','1,743 bags','34,860 sachets · 70% of plan to now')}
{fig('Downtime','42 min','32 min still running','var(--ink-red-7)')}
{fig('Alarms','5','1 not acknowledged')}
{fig('Rejects','1.4%','500 sachets')}
</div>
<div class="list" style="margin:0">
<a href="Trip.dc.html" class="lr" style="grid-template-columns:20px minmax(0,1fr) auto;color:inherit;margin:0 -12px;min-height:56px"><span style="color:var(--ink-red-7);display:flex">{ic("octagon")}</span><span class="c"><div class="t1">TRIP-0007 is still open</div><div class="m">Lead interlock at 08:14 · recovery 2 of 6 steps done</div></span>{bd("Tripped","s-red")}</a>
<a href="Downtime.dc.html" class="lr" style="grid-template-columns:20px minmax(0,1fr) auto;color:inherit;margin:0 -12px;min-height:56px"><span style="color:var(--ink-amber-7);display:flex">{ic("clock")}</span><span class="c"><div class="t1">3 stops have no reason</div><div class="m">07:40 all fillers · 05:32 F7 · 01:18 F3 (night shift)</div></span>{bd("Needs a reason","amber")}</a>
<a href="Resources.dc.html" class="lr" style="grid-template-columns:20px minmax(0,1fr) auto;color:inherit;margin:0 -12px;min-height:56px"><span style="color:var(--ink-amber-7);display:flex">{ic("droplet")}</span><span class="c"><div class="t1">Antiscalant 22 h · diesel 41 h</div><div class="m">Both under their reorder point · MR-0193 raised for antiscalant</div></span>{bd("Low","amber")}</a>
</div></section>'''

def item(text, who, init, due, done=False):
    return f'''<div style="display:grid;grid-template-columns:16px minmax(0,1fr) 140px 108px 24px;align-items:center;gap:10px;min-height:44px;border-bottom:1px solid var(--outline-gray-1)"><span class="cb{" on" if done else ""}"></span><span style="color:var(--ink-gray-8);{"text-decoration:line-through;color:var(--ink-gray-5)" if done else ""}">{text}</span><span style="display:flex;align-items:center;gap:6px;font-size:13px;color:var(--ink-gray-7)"><span class="av">{init}</span>{who}</span><span class="qs tab">{due}</span><span style="color:var(--ink-gray-4);display:flex">{ic("more","i s35")}</span></div>'''
nextshift = f'''<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h2">For the next shift</h2><span class="qs">Each item becomes a ToDo for the person named</span></div>
<div style="display:flex;flex-direction:column">
{item('Finish TRIP-0007: second sample, cause, key reset', 'Bola N.', 'BN', 'Before restart')}
{item('Backwash carbon filter, ΔP at 1.3 bar', 'Ibrahim K.', 'IK', 'Today 16:00')}
{item('Collect antiscalant from store (MR-0193)', 'Storekeeper', 'ST', 'Today 15:00')}
{item('Put F9 back after jaw heater swap, run 40 test sachets', 'Ibrahim K.', 'IK', 'Today 10:00')}
</div>
<div><button type="button" class="btn ghost">{ic("plus")}Add item</button></div></section>'''

notes = f'''<section style="display:flex;flex-direction:column;gap:12px"><h2 class="h2">Notes</h2>
{field('Safety and quality', f'<span class="in ta focus" style="min-height:96px"><span style="white-space:normal;line-height:1.55">Lead spike started after the grid dropped at 07:40 and the borehole pump restarted. Suspect sediment from T1. T4 batch from 07:55–08:14 is in T5; do not release it.<span style="display:inline-block;width:1px;height:16px;background:var(--ink-gray-9);vertical-align:-3px;margin-left:1px"></span></span></span>', hint='Shown first to the incoming supervisor.')}
{field('Anything else', inp('Optional', 'ta', ph=True))}
</section>'''

def chk(label, meta, state):
    if state == 'done':
        b = f'<span class="cb on"></span>'; m = f'<span class="qs tab">{meta}</span>'
    elif state == 'due':
        b = '<span class="cb"></span>'; m = f'<span class="qs tab">{meta}</span>'
    else:
        b = f'<span class="cb" style="border-color:var(--outline-red-3)"></span>'; m = f'<span class="tab" style="font-size:13px;color:var(--ink-red-7)">{meta}</span>'
    return f'<div style="display:grid;grid-template-columns:16px minmax(0,1fr) auto;align-items:center;gap:10px;min-height:40px;border-bottom:1px solid var(--outline-gray-1)">{b}<span style="color:var(--ink-gray-8)">{label}</span>{m}</div>'
checks = f'''<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h2">Shift checks</h2><span class="qs">2 of 4 done · all required to submit</span></div>
<div>
{chk('Lead grab sample every 2 hours', '06:30 · 08:30 · Grace O.', 'done')}
{chk('Filler seal and date-code check', '07:05 · Kemi E.', 'done')}
{chk('Diesel dip reading logged', 'Not done', 'todo')}
{chk('Filling hall cleaned', 'Due by 14:00', 'due')}
</div></section>'''

signoff = f'''<section class="card" style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div style="display:flex;gap:10px;align-items:center"><span class="av md">MA</span><span style="display:flex;flex-direction:column;gap:2px"><span style="color:var(--ink-gray-8);font-weight:500">Musa A. · outgoing</span><span class="qs">Signs when you submit</span></span></div>
<div style="display:flex;gap:10px;align-items:center"><span class="av md" style="background:var(--surface-gray-2);color:var(--ink-gray-5)">BN</span><span style="display:flex;flex-direction:column;gap:2px"><span style="color:var(--ink-gray-8);font-weight:500">Bola N. · incoming</span><span class="qs">Accepts after reading, from the app or WhatsApp</span></span></div>
</section>'''

main = f'<div style="flex:1;min-width:0;overflow:auto"><div class="body" style="max-width:820px;margin:0 auto;gap:28px">{summary}{nextshift}{notes}{checks}{signoff}</div></div>'

crew = [('KE','Kemi E.','Operator · F1–F5','06:02'),('SI','Sani I.','Operator · F6–F10','05:58'),('GO','Grace O.','Quality Inspector','06:00'),('IK','Ibrahim K.','Maintenance','06:10'),('AO','Ade O.','Treatment','06:01'),('ST','Funmi T.','Storekeeper','07:30'),('YB','Yusuf B.','Operator · relief','Absent')]
cl = ''.join(f'<div style="display:flex;align-items:center;gap:8px;min-height:36px;font-size:13px"><span class="av">{a}</span><span style="flex:1;display:flex;flex-direction:column"><span style="color:var(--ink-gray-8)">{n}</span><span class="qs" style="font-size:12px">{r}</span></span><span class="tab" style="{"color:var(--ink-red-7)" if t=="Absent" else "color:var(--ink-gray-5)"}">{t}</span></div>' for a,n,r,t in crew)
panel = f'''<aside class="panel"><div style="padding:16px;display:flex;flex-direction:column;gap:20px;overflow:auto">
<div class="divy">
<div class="prow"><span>Shift</span><span>Morning · 06:00 – 14:00</span></div>
<div class="prow"><span>Date</span><span>Sun 22 Nov 2026</span></div>
<div class="prow"><span>Outgoing</span><span>Musa A.</span></div>
<div class="prow"><span>Incoming</span><span>Bola N. · Afternoon</span></div>
<div class="prow"><span>Runs</span><span><a href="RunDetail.dc.html">RUN-0412</a></span></div>
</div>
<div style="display:flex;flex-direction:column;gap:6px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h3 class="h3">Crew</h3><span class="qs">6 of 7 clocked in</span></div>{cl}<span class="qs">From Shift Attendance Summary · biometric clock</span></div>
<div style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">Last handover</h3>
<a href="#" class="inset" style="display:flex;flex-direction:column;gap:4px;color:inherit"><span style="font-size:13px;color:var(--ink-gray-8);font-weight:500">Night to morning · Ibrahim K.</span><span class="ps">F9 jaw heater failing, swapped at 05:32. Two short stops on F3 and F7 not coded.</span><span class="qs">Accepted by Musa A. · 06:04</span></a></div>
</div></aside>'''

write('Handover.dc.html', page('Shift handover', shell('Handover.dc.html', head, f'<div style="display:flex;flex:1;min-height:0">{main}{panel}</div>'), {"$preview": {"width": 1440, "height": 900}}))
