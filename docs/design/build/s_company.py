"""Company settings (frappe-ui SettingsDialog) over the company Dashboard: ERPNext, API and webhooks, Kiosks."""
from ff import *

NAV = [
  ('Company', [('General', 'factory'), ('Users and roles', 'users')]),
  ('Floor', [('Kiosks', 'cpu'), ('Process templates', 'layers')]),
  ('Integrations', [('ERPNext', None), ('API and webhooks', 'link'), ('WhatsApp', 'msg'), ('ThingsBoard', 'radio')]),
]
HREF = {'General': 'CompanyGeneral.dc.html', 'Users and roles': 'CompanyUsers.dc.html', 'Kiosks': 'CompanyKiosks.dc.html', 'Process templates': 'CompanyTemplates.dc.html',
        'ERPNext': 'CompanyERPNext.dc.html', 'API and webhooks': 'CompanyAPI.dc.html', 'WhatsApp': 'CompanyWhatsApp.dc.html', 'ThingsBoard': 'CompanyTB.dc.html'}
def nav(active):
    o = ''
    for g, items in NAV:
        o += f'<div style="display:flex;align-items:center;height:28px;padding:0 8px;font-size:14px;color:var(--ink-gray-5);margin-top:8px">{g}</div><div style="display:flex;flex-direction:column;gap:2px">'
        for n, i in items:
            on = n == active
            st = 'background:var(--surface-elevation-3);box-shadow:var(--shadow-sm);color:var(--ink-gray-8)' if on else 'color:var(--ink-gray-7)'
            icon = ic(i) if i else '<span style="width:16px;height:16px;border:1.5px solid var(--ink-gray-6);border-radius:3px;display:grid;place-items:center;font-size:9px;font-weight:700;color:var(--ink-gray-6)">E</span>'
            o += f'<a href="{HREF[n]}" style="display:flex;align-items:center;gap:8px;height:28px;padding:0 8px;border-radius:8px;font-size:14px;text-decoration:none;{st}">{icon}{n}</a>'
        o += '</div>'
    return o

def row(title, desc, control):
    return f'<div style="display:flex;align-items:center;gap:32px;padding:14px 0"><div style="flex:1;min-width:0"><span style="display:block;font-size:14px;font-weight:500;color:var(--ink-gray-8)">{title}</span><span style="display:block;margin-top:4px;font-size:14px;line-height:20px;color:var(--ink-gray-6)">{desc}</span></div><div style="flex-shrink:0;display:flex;justify-content:flex-end">{control}</div></div>'
def section(title, rows):
    h = f'<h3 style="margin:0 0 2px;font-size:14px;font-weight:600;color:var(--ink-gray-8)">{title}</h3>' if title else ''
    return f'<section>{h}<div class="divy">{"".join(rows)}</div></section>'
def title(t, d, actions=''):
    return f'<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px"><div style="display:flex;flex-direction:column;gap:4px"><h2 style="margin:0;font-size:16px;font-weight:600;color:var(--ink-gray-8)">{t}</h2><p style="margin:0;font-size:14px;color:var(--ink-gray-6)">{d}</p></div><div style="display:flex;gap:8px;margin-right:40px">{actions}</div></div>'
SW_ON, SW_OFF = '<span class="sw on"></span>', '<span class="sw"></span>'

# ---------------- ERPNext
def erpnext():
    conn = f'''<div style="display:flex;flex-direction:column;gap:12px">
<div style="display:flex;align-items:center;gap:12px"><span style="width:40px;height:40px;border-radius:10px;background:oklch(0.55 0.16 252);color:#fff;display:grid;place-items:center;font-weight:700;font-size:18px">E</span><span style="flex:1;display:flex;flex-direction:column;gap:2px"><span style="font-weight:500;color:var(--ink-gray-8)">Enable ERPNext integration</span><span style="font-size:14px;color:var(--ink-gray-6)">Work orders, stock, quality and downtime flow between the two apps.</span></span>{SW_ON}</div>
<div style="display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:10px;background:var(--surface-green-2);font-size:14px"><span style="color:var(--ink-green-7);display:flex">{ic("check")}</span><span style="display:flex;flex-direction:column;gap:2px"><span style="font-weight:500;color:var(--ink-gray-8)">Connected to erp.ivarse.ng</span><span style="color:var(--ink-gray-6)">ERPNext 15.42 · company I-Varse Technologies · last sync 08:45 · 0 errors today</span></span></div></div>'''
    where = f'''<section style="display:flex;flex-direction:column;gap:10px"><h3 style="margin:0;font-size:14px;font-weight:600;color:var(--ink-gray-8)">Where ERPNext runs</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
<label style="display:grid;grid-template-columns:16px minmax(0,1fr);gap:10px;padding:12px;border-radius:10px;border:1px solid var(--outline-gray-2);opacity:.6"><span class="rd" style="margin-top:2px"></span><span style="display:flex;flex-direction:column;gap:3px"><span style="font-weight:500;color:var(--ink-gray-8)">On this site</span><span style="font-size:13px;color:var(--ink-gray-6)">ERPNext isn't installed here. Install it and this option turns on.</span></span></label>
<label style="display:grid;grid-template-columns:16px minmax(0,1fr);gap:10px;padding:12px;border-radius:10px;border:1px solid var(--ink-gray-9)"><span class="rd on" style="margin-top:2px"></span><span style="display:flex;flex-direction:column;gap:3px"><span style="font-weight:500;color:var(--ink-gray-8)">On another site</span><span style="font-size:13px;color:var(--ink-gray-6)">Talk to ERPNext through its REST API with an API key.</span></span></label></div>
<div style="display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr) minmax(0,1fr);gap:12px;align-items:end">
{field('Site URL', inp('https://erp.ivarse.ng', 'out'), req=True)}{field('API key', inp('7c1e…a4f2', 'out'), req=True)}{field('API secret', inp('••••••••••••', 'out'), req=True)}</div>
<div style="display:flex;align-items:center;gap:12px">{btn("Verify connection", "refresh")}<span class="qs">The key's user needs the Manufacturing User, Stock User and Quality Manager roles on ERPNext.</span></div>
<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px">{field('Company', sel('I-Varse Technologies', 'out'), req=True)}{field('Default warehouse for finished goods', sel('Finished Goods - IVT', 'out'))}</div></section>'''
    maps = section('What links', [
      row('Work orders drive production runs', 'A run starts from an ERPNext Work Order. Counts and times update its Job Card.', SW_ON),
      row('Post stock when a run ends', 'A Manufacture Stock Entry with the good quantity; rejects go in as scrap.', SW_ON),
      row('Send stops as Downtime Entry', 'Each closed machine stop becomes a Downtime Entry on its Workstation, with the operator and reason.', SW_ON),
      row('Machine state to Workstation status', 'Sets Production, Idle, Problem or Maintenance, so ERPNext\'s Plant Floor matches the machines.', SW_ON),
      row('Lab samples as Quality Inspection', 'Trip samples and shift checks create Quality Inspections against the batch.', SW_ON),
      row('Material requests from Resources', 'Request on a consumable creates a Material Request for the plant\'s store.', SW_ON),
      row('Employees and shifts from HRMS', 'Crew and attendance on the shift handover. Needs HRMS on the ERPNext site.', SW_OFF),
    ])
    return f'''{title('ERPNext', 'Link Frappe Factory to ERPNext. Without it, Frappe Factory runs on its own as a monitoring app.', btn("Disable") + '<button type="button" class="btn solid">Update</button>')}
<div class="tabs" style="padding:0;margin-top:16px"><span class="t on">General</span><span class="t">Item and machine mapping</span><span class="t">Logs</span></div>
<div style="display:flex;flex-direction:column;gap:32px;padding-top:20px">{conn}{where}{maps}</div>'''

# ---------------- API and webhooks
def api():
    hooks = [('Shift Summary', 'when closed', 'https://sap-bridge.ivarse.ng/hooks/shift', '200 · 06:02', 'green'),
             ('Machine Stop', 'when closed', 'https://sap-bridge.ivarse.ng/hooks/stop', '200 · 08:43', 'green'),
             ('Interlock Trip', 'when opened', 'https://sap-bridge.ivarse.ng/hooks/trip', '200 · 08:14', 'green'),
             ('Alarm', 'priority 1 raised', 'https://hooks.example-mes.com/ff', '502 · retrying', 'red')]
    C = 'grid-template-columns:130px 120px minmax(0,1fr) 110px 24px'
    hr = ''.join(f'<div class="lr" style="{C};margin:0"><span class="t1">{e}</span><span class="qs">{w}</span><span class="c tab qs" style="color:var(--ink-gray-7)">{u}</span><span>{bd(s, c)}</span><span style="color:var(--ink-gray-4);display:flex">{ic("more","i s35")}</span></div>' for e, w, u, s, c in hooks)
    return f'''{title('API and webhooks', 'For ERP and MES systems from other publishers. They read plant data through the API and get events pushed to them.', '<button type="button" class="btn solid">Add webhook</button>')}
<div style="display:flex;flex-direction:column;gap:32px;padding-top:24px">
{section('API', [
  row('REST API', 'Frappe\'s standard /api/resource and /api/method, plus the documented Frappe Factory methods.', f'<span class="in out" style="width:280px"><span class="grow tab">https://factory.ivarse.ng/api/v2</span>{ic("copy","i s35")}</span>'),
  row('API reference', 'OpenAPI 3 description of every method and DocType the integration may use.', f'<a href="https://github.com/puzzo-dev/frappe_factory/blob/docs/architecture-and-plans/docs/trd.md#frappe-api-surface" target="_blank" rel="noopener" class="btn">{ic("file")}Open reference</a>'),
  row('API keys', 'Frappe\'s own: each user makes keys on their User record. A key works as that user, with the same roles and plants.', f'<span class="qs">Managed in Frappe</span>'),
  row('Plan targets in', 'Other systems post the daily plan per plant and shift, so OEE and plan attainment work without ERPNext.', '<span class="in out tab" style="width:280px"><span class="grow">plant.set_plan(plant, date, shift, item, qty)</span></span>'),
])}
<section style="display:flex;flex-direction:column;gap:10px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h3 style="margin:0;font-size:14px;font-weight:600;color:var(--ink-gray-8)">Webhooks</h3><span class="qs">Frappe Webhook records · signed with HMAC-SHA256 · retried for 24 h</span></div>
<div class="list" style="margin:0"><div class="lh" style="{C};margin:0"><span>Document</span><span>When</span><span>URL</span><span>Last delivery</span><span></span></div>{hr}</div></section>
</div>'''

# ---------------- Kiosks
def kiosks():
    profs = [('Filling hall T-02', 'Line · Koyo 1 · F1 – F5', '5 users', True), ('Filling hall T-03', 'Line · Koyo 1 · F6 – F10', '4 users', False), ('Maintenance T-05', 'Maintenance · Koyo 1 · all equipment', '3 users', False), ('Quality lab T-06', 'Quality · Koyo 1 · analysers, holds', '2 users', False), ('Packing T-01', 'Line · Rice mill · bagger, color sorter', '4 users', False)]
    pl = ''.join(f'<div class="lr" style="grid-template-columns:minmax(0,1fr) auto;margin:0;min-height:56px;{"background:var(--surface-gray-2)" if on else ""}"><span class="c"><div class="t1">{n}</div><div class="m">{m}</div></span><span class="qs">{u}</span></div>' for n, m, u, on in profs)
    users = [('KE', 'Kemi E.', 'kemi.e@koyo1.ng', 'Machine Operator', True, True), ('SI', 'Sani I.', 'sani.i@koyo1.ng', 'Machine Operator', False, True), ('YB', 'Yusuf B.', 'yusuf.b@koyo1.ng', 'Machine Operator', False, False), ('GO', 'Grace O.', 'grace.o@koyo1.ng', 'Quality Inspector', False, True), ('MA', 'Musa A.', 'musa.a@koyo1.ng', 'Floor Supervisor', False, True)]
    UC = 'grid-template-columns:minmax(0,1fr) 116px 52px 96px 20px'
    ur = ''.join(f'<div class="lr" style="{UC};margin:0;cursor:default"><span style="display:flex;align-items:center;gap:8px;min-width:0"><span class="av">{a}</span><span class="c"><div class="t1">{n}</div><div class="m tab">{e}</div></span></span><span class="qs" style="color:var(--ink-gray-7)">{r}</span><span>{"<span class=cb.on></span>".replace("cb.on","\'cb on\'") if d else "<span class=cb></span>"}</span><span>{bd("Today","gray") if p else bd("Never","gray")}</span><span style="color:var(--ink-gray-4);display:flex">{ic("x","i s35")}</span></div>' for a, n, e, r, d, p in users)
    acts = [('Give stop reasons', 'Machine Operator', True), ('Log rejects', 'Machine Operator', True), ('Record samples', 'Quality Inspector', True), ('Start and end runs', 'Floor Supervisor · needs ERPNext', True), ('Close the kiosk session', 'Floor Supervisor', True)]
    ar = ''.join(f'<label style="display:flex;align-items:center;gap:10px;height:32px;font-size:14px"><span class="cb{" on" if on else ""}"></span><span style="color:var(--ink-gray-8)">{n}</span><span class="qs" style="margin-left:auto">{r}</span></label>' for n, r, on in acts)
    form = f'''<div style="display:flex;flex-direction:column;gap:20px">
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px">{field('Kiosk name', inp('Filling hall T-02', 'out'), req=True)}{field('Plant', sel('Koyo 1', 'out'), req=True)}{field('View', sel('Line · filling and packing', 'out'), req=True, hint='Line, Maintenance or Quality')}{field('Machines on screen', inp('<span class="chip" style="height:20px">F1</span> <span class="chip" style="height:20px">F2</span> <span class="chip" style="height:20px">F3</span> <span class="chip" style="height:20px">F4</span> <span class="chip" style="height:20px">F5</span>', 'out'))}</div>
<section style="display:flex;flex-direction:column;gap:8px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h3 style="margin:0;font-size:14px;font-weight:600;color:var(--ink-gray-8)">Assigned users</h3><span class="qs">Only these Frappe users can open this kiosk</span></div>
<div class="list" style="margin:0"><div class="lh" style="{UC};margin:0"><span>Frappe user</span><span>Role</span><span>Default</span><span>Last log-in</span><span></span></div>{ur}</div><div style="display:flex;justify-content:space-between;align-items:center">{btn("Add user","plus","ghost")}<span class="qs">Assigned like users on a POS Profile. They log in on the tablet with their own Frappe login; anyone not listed is refused.</span></div></section>
<section style="display:flex;flex-direction:column;gap:4px"><h3 style="margin:0 0 4px;font-size:14px;font-weight:600;color:var(--ink-gray-8)">What people can do here</h3>{ar}<span class="qs">Each action also needs the role shown. The kiosk never shows setup, other plants or Desk.</span></section>
{section('Device', [row('Locked to a tablet', 'T-02 · registered 3 Nov by Musa A. The kiosk opens only on this device.', f'{btn("Reset device")}'), row('Log out when idle', 'Logs the user out after no taps.', f'<span class="in out" style="width:110px"><span class="grow">10 min</span>{ic("chev-d","i s35")}</span>')])}
</div>'''
    return f'''{title('Kiosks', 'Full-screen station apps for tablets at the line, like ERPNext POS profiles: each kiosk is tied to a plant, its machines and the people assigned to it.', '<button type="button" class="btn solid">New kiosk</button>')}
<div style="display:grid;grid-template-columns:220px minmax(0,1fr);gap:24px;padding-top:24px"><div class="list" style="margin:0;align-self:start">{pl}</div>{form}</div>'''

def build(name, active, panel):
    import s_dashboard  # noqa: builds the dashboard; we only need its page body
    from s_dashboard import head as dh, body as db
    bg = shell('Dashboard.dc.html', dh, db, scope='company')
    dlg = f'''{closer("dlg")}<div class="ff ffov" style="position:absolute;inset:0;display:block;min-height:0;background:transparent"><label for="dlg" class="overlay" aria-label="Close"></label>
<div class="dialog" role="dialog" aria-label="App settings" style="left:50%;top:32px;transform:translateX(-50%);width:1100px;height:836px;display:flex">
<div style="width:220px;flex-shrink:0;background:var(--surface-sidebar);border-right:1px solid var(--outline-gray-1);padding:8px;display:flex;flex-direction:column">
<div style="display:flex;align-items:center;gap:8px;height:40px;padding:0 6px"><span class="logo" style="width:24px;height:24px;flex-basis:24px;font-size:11px">FF</span><span style="display:flex;flex-direction:column;line-height:1.15"><span style="font-weight:500;color:var(--ink-gray-8)">App settings</span><span class="qs" style="font-size:12px">Frappe Factory · all plants</span></span></div>{nav(active)}</div>
<div style="flex:1;min-width:0;display:flex;flex-direction:column;position:relative"><div style="position:absolute;right:16px;top:16px">{close_btn("dlg")}</div>
<div style="flex:1;overflow:auto;padding:40px 3.5rem 64px">{panel}</div></div></div></div>'''
    write(name, page('Settings', f'<div style="position:relative">{bg}{dlg}</div>', {"$preview": {"width": 1440, "height": 900}}))

build('CompanyERPNext.dc.html', 'ERPNext', erpnext())
build('CompanyAPI.dc.html', 'API and webhooks', api())
build('CompanyKiosks.dc.html', 'Kiosks', kiosks())
