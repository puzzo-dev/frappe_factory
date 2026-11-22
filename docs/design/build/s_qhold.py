"""Quality hold: QA decides what happens to product made around a fault. Opened by TRIP-0007."""
from ff import *

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Quality holds','HoldList.dc.html'),('QH-0031',None)),
  f'{bd("On hold","amber")}{btn("Report","file","ghost")}{btn(icon="more",kind="ghost",attrs="More")}')

banner = f'''<div class="alert amber" style="border-color:var(--outline-amber-3);background:var(--surface-amber-2)"><span class="ai">{ic('shield')}</span>
<div style="display:flex;flex-direction:column;gap:4px"><span class="ttl">256 bags, 14 loose sachets and 2.3 m³ of water are on hold</span>
<span style="font-size:13px;line-height:1.5;color:var(--ink-gray-7)">Everything made between the last passing check at 07:55 and the trip at 08:14: 5,134 sachets of 50 cl, 2,567 L. A bag is 20 sachets. Held stock cannot be dispatched or used until a Quality Inspector decides each lot.</span></div></div>'''

QS = {'L1': '2,000 sachets · 1,000 L', 'L2': '3,134 sachets · 1,567 L', 'L3': 'not yet filled'}
LC = 'grid-template-columns:minmax(0,1.4fr) 160px minmax(0,1fr) 120px 150px'
lots = [
  ('L1 · Sachets 07:56 – 08:03', 'F1–F8, F10 · SP-1 under 5 µg/L', '100 bags', 'Store bay 3 · pallet H-0331', ('Tests 2 of 3 pass', 'gray'), sel('Choose', 'out', ph=True)),
  ('L2 · Sachets 08:03 – 08:14', 'Filled after SP-1 passed the alert limit', '156 bags + 14 sachets', 'Store bay 3 · H-0332, loose crate C-7', ('1 sample at 6.8 µg/L', 'red'), sel('Scrap', 'out')),
  ('L3 · Water in T5', 'Diverted by XV-301 and XV-402', '2.3 m³', 'T5 quarantine', ('By template', 'gray'), sel('Reprocess via IX-501', 'out')),
]
lr = ''.join(f'''<div class="lr" style="{LC};min-height:60px;cursor:default"><span class="c"><div class="t1">{a}</div><div class="m">{b}</div></span><span class="c"><div class="tab" style="color:var(--ink-gray-8)">{q}</div><div class="m tab">{QS[a[:2]]}</div></span><span class="c qs" style="color:var(--ink-gray-7)">{w}</span><span>{bd(t, tc)}</span><span>{d}</span></div>''' for a, b, q, w, (t, tc), d in lots)
lots_html = f'''<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h2">Held lots</h2><span class="qs">Split by time from the filler counters and SP-1 readings</span></div>
<div class="list"><div class="lh" style="{LC}"><span>Lot</span><span>Quantity</span><span>Where</span><span>Tests</span><span>QA decision</span></div>{lr}</div>
<p class="qs" style="margin:0">Decisions: Release, Release with deviation (needs the Factory Manager too), Rework or reprocess, Scrap. Scrap posts a Material Issue to scrap in ERPNext.</p></section>'''

SC = 'grid-template-columns:72px 90px minmax(0,1fr) 110px 110px'
samples = [('S-1', 'F1 · 07:58', 'Lead, ASV meter', '2.4 µg/L', ('Pass', 'green'), 'L1'),
           ('S-2', 'F6 · 08:01', 'Lead, ASV meter', '3.1 µg/L', ('Pass', 'green'), 'L1'),
           ('S-3', 'F4 · 08:06', 'Lead, ASV meter', '6.8 µg/L', ('Fail', 'red'), 'L2'),
           ('S-4', 'F8 · 08:02', 'Lead, ICP-MS lab', 'Sent 08:40', ('Waiting', 'gray'), 'L1')]
sr = ''.join(f'<div class="lr" style="{SC};cursor:default"><span class="tab qs" style="color:var(--ink-gray-7)">{a}</span><span class="tab qs" style="color:var(--ink-gray-7)">{b}</span><span class="c">{c} · <span class="qs">{lot}</span></span><span class="tab" style="color:var(--ink-gray-9);font-weight:500">{d}</span><span>{bd(e, ec)}</span></div>' for a, b, c, d, (e, ec), lot in samples)
tests = f'''<section style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><div style="display:flex;gap:8px;align-items:baseline"><h2 class="h2">Tests</h2><span class="qs">From template QHT-003 · Lead trip, sachet water</span></div>{btn("Add sample","plus")}</div>
<div class="inset" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;font-size:13px">
<div><span class="qs">Test</span><div style="color:var(--ink-gray-8);margin-top:2px">Lead in finished sachets</div></div>
<div><span class="qs">Pass if</span><div class="tab" style="color:var(--ink-gray-8);margin-top:2px">Under 5 µg/L, every sample</div></div>
<div><span class="qs">How many</span><div style="color:var(--ink-gray-8);margin-top:2px">3 sachets per lot from different fillers, plus 1 to the outside lab</div></div></div>
<div class="list"><div class="lh" style="{SC}"><span>Sample</span><span>Taken</span><span>Test and lot</span><span>Result</span><span>Status</span></div>{sr}</div></section>'''

close = f'''<section class="card" style="display:flex;align-items:center;justify-content:space-between;gap:16px"><div style="display:flex;flex-direction:column;gap:4px"><span style="font-weight:500;color:var(--ink-gray-8)">Close the hold</span><span class="qs">Needs a decision on every lot, signed by a Quality Inspector: their Frappe user plus their PIN. Any release with deviation also needs Tunde B. as Factory Manager.</span></div><button type="button" class="btn solid" disabled>Close hold</button></section>'''

main = f'<div style="flex:1;min-width:0;overflow:auto"><div class="body" style="max-width:900px;margin:0 auto">{banner}{lots_html}{tests}{close}</div></div>'

panel = f'''<aside class="panel"><div style="padding:16px;display:flex;flex-direction:column;gap:20px;overflow:auto">
<div class="divy">
<div class="prow"><span>Opened by</span><span><a href="Trip.dc.html">TRIP-0007</a> · automatic</span></div>
<div class="prow"><span>Opened at</span><span class="tab">22 Nov · 08:14</span></div>
<div class="prow"><span>QA owner</span><span>Grace O. · Quality Inspector</span></div>
<div class="prow"><span>Approver</span><span>Tunde B. · Factory Manager</span></div>
<div class="prow"><span>Template</span><span>QHT-003</span></div>
</div>
<div style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">In ERPNext</h3><div class="divy" style="font-size:13px">
<div style="display:flex;justify-content:space-between;padding:7px 0"><span style="color:var(--ink-gray-7)">Batch PW-50CL-221126-M</span><span class="qs">disabled while held</span></div>
<div style="display:flex;justify-content:space-between;padding:7px 0"><span style="color:var(--ink-gray-7)">Quality Inspections</span><span class="qs">3 · In Process</span></div>
<div style="display:flex;justify-content:space-between;padding:7px 0"><span style="color:var(--ink-gray-7)">Non Conformance NC-0019</span><span class="qs">Open</span></div>
</div><span class="qs">Without ERPNext the samples and decisions stay in Frappe Factory as Quality Samples.</span></div>
<div style="display:flex;flex-direction:column;gap:10px"><h3 class="h3">Activity</h3><div class="tline">
<div class="ev"><span class="ic">{ic('flask')}</span><span><b>Grace O.</b> recorded S-3, 6.8 µg/L, fail <span class="w">· 08:44</span></span></div>
<div class="ev"><span class="ic">{ic('msg')}</span><span><b>WhatsApp</b> to Grace O. and Tunde B. <span class="w">· 08:14</span></span></div>
<div class="ev"><span class="ic" style="background:var(--surface-amber-2);color:var(--ink-amber-7)">{ic('shield')}</span><span>Hold opened by TRIP-0007 <span class="w">· 08:14</span></span></div>
</div></div>
</div></aside>'''

write('QualityHold.dc.html', page('QH-0031', shell('QualityHold.dc.html', head, f'<div style="display:flex;flex:1;min-height:0">{main}{panel}</div>'), {"$preview": {"width": 1440, "height": 900}}))
