from ff import *

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Alarm definitions',None)),
  f'{btn("Import","upload","ghost")}<button type="button" class="btn solid">{ic("plus")}New definition</button>')

C = 'grid-template-columns:minmax(0,1.5fr) 64px 120px 104px minmax(0,1fr) 72px 40px'
defs = [
  ('AT-401 Lead · high-high', 'IL-01 in the PLC · this definition only reports it', '1', 's-red', '≥ 8 µg/L', '0 s · —', 'Supervisor, Manager', 'Interlock', True),
  ('AT-401 Lead · high', 'Polishing', '2', 's-amber', '≥ 5 µg/L', '30 s · 0.3', 'Supervisor, Quality', '', True),
  ('SP-2 Verification · high', 'Grab sample entry', '2', 's-amber', '≥ 5 µg/L', 'on entry', 'Supervisor, Quality', '', True),
  ('AT-301 pH · out of band', 'Remineralization', '2', 's-amber', '< 7.8 or > 8.3', '60 s · 0.05', 'Supervisor', 'Interlock', True),
  ('AT-302 Conductivity · high', 'Polishing', '3', 'amber', '≥ 220 µS/cm', '60 s · 3', 'Supervisor', '', True),
  ('UV-301 Intensity · low', 'Disinfection', '1', 's-red', '< 70 %', '10 s · 1', 'Supervisor, Manager', 'Interlock', True),
  ('DP-102 Carbon ΔP · high', 'Pretreatment', '3', 'amber', '≥ 1.2 bar', '5 min · 0.05', 'Maintenance', '', True),
  ('LT-901 Diesel runway · low', 'Utilities', '3', 'amber', '< 48 h', '15 min · 1 h', 'Storekeeper', '', True),
  ('TT-F1…F10 Jaw temp · low', 'Filling · 10 tags', '3', 'amber', '< 130 °C', '20 s · 2', 'Supervisor', '', True),
  ('EM-1 Power factor · low', 'Utilities', '3', 'amber', '< 0.85', '10 min · 0.02', 'Maintenance', '', False),
]
rows = ''
for t, m, p, pc, lim, dd, who, il, en in defs:
    act = ' act' if t.startswith('AT-401 Lead · high ') or t == 'AT-401 Lead · high' else ''
    ilb = bd('Interlock','o-gray') if il else '<span class="qs">—</span>'
    rows += f'<div class="lr{act}" style="{C};min-height:56px"><span class="c"><div class="t1">{t}</div><div class="m">{m}</div></span><span><span class="bd {pc}" style="min-width:24px;justify-content:center">P{p}</span></span><span class="tab" style="color:var(--ink-gray-8)">{lim}</span><span class="tab qs" style="color:var(--ink-gray-7)">{dd}</span><span class="c qs" style="color:var(--ink-gray-7)">{who}</span><span>{ilb}</span><span><span class="sw{" on" if en else ""}"></span></span></div>'

lst = f'''<div class="body" style="gap:14px"><div style="display:flex;justify-content:space-between;align-items:center"><div style="display:flex;gap:8px"><span class="in muted" style="width:220px">{ic("search")}<span class="grow">Search definitions</span></span><span class="chip"><span class="k">Priority</span>All</span><span class="chip"><span class="k">Area</span>All</span></div><span class="qs">34 definitions · 6 mirror PLC interlocks</span></div>
<div class="list"><div class="lh" style="{C}"><span>Definition</span><span>Priority</span><span>Limit</span><span>Delay · deadband</span><span>Notify</span><span>Type</span><span>On</span></div>{rows}</div></div>'''

def radio(label, desc, on=False):
    return f'<label style="display:grid;grid-template-columns:16px minmax(0,1fr);gap:8px;align-items:start;padding:8px 10px;border-radius:8px;border:1px solid {"var(--ink-gray-9)" if on else "var(--outline-gray-2)"};cursor:pointer"><span class="rd{" on" if on else ""}" style="margin-top:1px"></span><span style="display:flex;flex-direction:column;gap:2px"><span style="font-size:14px;color:var(--ink-gray-8);font-weight:500">{label}</span><span class="qs" style="font-size:12px;line-height:1.4">{desc}</span></span></label>'

def chipx(t):
    return f'<span class="chip" style="height:22px;background:var(--surface-gray-3)">{t}{ic("x","i s35")}</span>'

dialog = f'''<label for="dlg" class="overlay" aria-label="Close"></label>
<div class="dialog" role="dialog" aria-labelledby="dlg-t" style="left:50%;top:40px;transform:translateX(-50%);width:640px">
<div style="padding:20px 24px 0;display:flex;justify-content:space-between;align-items:flex-start"><div style="display:flex;flex-direction:column;gap:4px"><h2 id="dlg-t" style="margin:0;font-size:20px;font-weight:600;color:var(--ink-gray-9)">AT-401 Lead · high</h2><span class="qs">ALD-0012 · Koyo 1 · changed 3 Nov by Tunde B.</span></div>{close_btn("dlg")}</div>
<div style="padding:20px 24px;display:flex;flex-direction:column;gap:22px;max-height:660px;overflow:auto">
<section style="display:flex;flex-direction:column;gap:12px"><h3 class="h3">When it raises</h3>
<div style="display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr) minmax(0,1fr);gap:12px">
{field('Tag', inp('<span class="tab">AT-401.LEAD</span> <span class="qs">· PLC-1</span>', right=ic("chev-d","i s35")), req=True)}
{field('Condition', sel('Goes above'), req=True)}
{field('Limit', inp('<span class="tab">5.0</span>', 'focus', right='<span class="qs">µg/L</span>'), req=True)}
</div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">
{field('Deadband', inp('<span class="tab">0.3</span>', right='<span class="qs">µg/L</span>'), hint='Clears below 4.7')}
{field('On delay', inp('<span class="tab">30</span>', right='<span class="qs">s</span>'))}
{field('Off delay', inp('<span class="tab">60</span>', right='<span class="qs">s</span>'))}
</div>
<div class="inset" style="display:flex;gap:8px;align-items:flex-start;font-size:13px;line-height:1.5;color:var(--ink-gray-7)"><span style="color:var(--ink-gray-6);display:flex;margin-top:1px">{ic("shield","i s35")}</span><span>The trip at 8 µg/L lives in the PLC as IL-01. Changing this alert does not change the trip.</span></div>
</section>
<section style="display:flex;flex-direction:column;gap:10px"><h3 class="h3">Priority</h3>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px">
{radio('Priority 1','Act now. Safety, product or a stopped line.')}
{radio('Priority 2','Act within 15 min or the line may stop.', True)}
{radio('Priority 3','Act this shift.')}
</div></section>
<section style="display:flex;flex-direction:column;gap:12px"><h3 class="h3">What the operator sees</h3>
{field('Likely cause', inp('Lead in raw water, or the remineralization chemicals carry lead.'))}
{field('If ignored', inp('Lead may reach 8 µg/L and the PLC stops filling.'))}
{field('Action', inp('Take a grab sample at SP-1 and check the borehole and dosing tanks.', 'ta'), req=True)}
</section>
<section style="display:flex;flex-direction:column;gap:12px"><h3 class="h3">Who is told</h3>
<div class="fl"><span class="lab">Roles</span><span class="in" style="height:auto;min-height:32px;flex-wrap:wrap;padding:4px 6px;gap:4px">{chipx("Floor Supervisor")}{chipx("Quality Inspector")}<span class="qs" style="padding:0 4px">Add role</span></span></div>
<div style="display:flex;flex-direction:column;gap:2px">
<label style="display:flex;align-items:center;justify-content:space-between;min-height:36px"><span style="display:flex;flex-direction:column"><span style="color:var(--ink-gray-8)">WhatsApp</span><span class="qs">Through frappe_whatsapp_openwa to the person on shift</span></span><span class="sw on"></span></label>
<label style="display:flex;align-items:center;justify-content:space-between;min-height:36px"><span style="display:flex;flex-direction:column"><span style="color:var(--ink-gray-8)">Escalate if not acknowledged</span><span class="qs">After 10 min to the Floor Supervisor, after 20 min to the Factory Manager. Reading a notification does not acknowledge.</span></span><span class="sw on"></span></label>
<label style="display:flex;align-items:center;justify-content:space-between;min-height:36px"><span style="display:flex;flex-direction:column"><span style="color:var(--ink-gray-8)">Allow shelving</span><span class="qs">Up to 8 h, with a reason</span></span><span class="sw"></span></label>
</div></section>
</div>
<div style="padding:12px 24px 20px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--outline-gray-1)"><span class="qs">Saving starts a new version and syncs to OpsEdge K1</span><div style="display:flex;gap:8px">{close_btn("dlg","Cancel")}<button type="button" class="btn solid">Save</button></div></div>
</div>'''

content = f'<div style="position:relative;flex:1;min-height:0">{lst}</div>'
body_html = f'<div style="position:relative">{shell("AlarmDefs.dc.html", head, content)}{closer("dlg")}<div class="ff ffov" style="position:absolute;inset:0;display:block;min-height:0;background:transparent">{dialog}</div></div>'
write('AlarmDefs.dc.html', page('Alarm definitions', body_html, {"$preview": {"width": 1440, "height": 900}}))
