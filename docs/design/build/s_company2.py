"""More company settings panels (General, Users and roles, Process templates, WhatsApp, ThingsBoard) and the user's own
My settings dialog with the kiosk PIN."""
from ff import *
from s_company import build, row, section, title, SW_ON, SW_OFF
import symbols as S
import symbols_ind as I

# ---------------- General
def general():
    return f'''{title('General', 'Company-wide defaults. Each plant can change its own shifts and time zone in Plant settings.')}
<div style="display:flex;flex-direction:column;gap:28px;padding-top:24px">
<div style="display:flex;align-items:center;gap:16px"><span class="logo" style="width:56px;height:56px;flex-basis:56px;font-size:18px;border-radius:12px">KI</span><div style="display:flex;flex-direction:column;gap:6px"><span style="font-weight:500;color:var(--ink-gray-8)">Company logo</span><div style="display:flex;gap:8px">{btn("Upload","upload")}{btn("Remove",kind="ghost")}</div></div></div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px">
{field('Company name', inp('Koyo Industries Ltd', 'out'), req=True)}
{field('ERPNext company', sel('Koyo Industries Ltd', 'out'), hint='Used for stock, work orders and quality records when ERPNext is linked.')}
{field('Default time zone', sel('Africa/Lagos · UTC+01:00', 'out'))}
{field('Date and number format', sel('22 Nov 2026 · 1,234.50', 'out'))}
</div>
{section('Units', [
  row('Measurement system', 'Metric. Pack units such as a bag of 20 sachets or a tray of 30 eggs come from each Process Template.', f'<span class="in out" style="width:150px"><span class="grow">Metric</span>{ic("chev-d","i s35")}</span>'),
  row('Show the machine unit next to pack units', 'For example 1,743 bags · 34,860 sachets. Keeps counts from being misread.', SW_ON),
])}
{section('Shifts', [
  row('Default shift pattern', 'Morning 06–14, Afternoon 14–22, Night 22–06. New plants start with this.', f'<span class="in out" style="width:150px"><span class="grow">3 × 8 h</span>{ic("chev-d","i s35")}</span>'),
  row('Shift handover is required', 'A shift cannot close until the outgoing supervisor signs the handover.', SW_ON),
])}
{section('Data', [
  row('Keep raw readings', 'Every reading at full rate in TimescaleDB, then 1-minute averages.', f'<span class="in out" style="width:150px"><span class="grow">90 days</span>{ic("chev-d","i s35")}</span>'),
  row('Keep summaries', 'Hourly and shift summaries, trips, holds and stops.', f'<span class="in out" style="width:150px"><span class="grow">7 years</span>{ic("chev-d","i s35")}</span>'),
])}
</div>'''

# ---------------- Users and roles
def users():
    roles = [('Factory Manager', 2), ('Floor Supervisor', 3), ('Quality Inspector', 2), ('Maintenance Engineer', 1), ('Maintenance Technician', 2), ('Machine Operator', 9), ('Factory Integration', 1)]
    rc = ''.join(f'<span class="chip" style="height:26px"><span class="k">{r}</span>{n}</span>' for r, n in roles)
    UC = 'grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) 96px 92px 20px'
    us = [('TB', 'Tunde B.', 'tunde.b@koyo.ng', 'Factory Manager, System Manager', 'All 6 plants', ('PIN set', 'green')),
          ('MA', 'Musa A.', 'musa.a@koyo1.ng', 'Floor Supervisor', 'Koyo 1', ('PIN set', 'green')),
          ('BN', 'Bola N.', 'bola.n@koyo1.ng', 'Floor Supervisor', 'Koyo 1', ('PIN set', 'green')),
          ('GO', 'Grace O.', 'grace.o@koyo1.ng', 'Quality Inspector', 'Koyo 1', ('PIN set', 'green')),
          ('ST', 'Segun T.', 'segun.t@koyo.ng', 'Maintenance Engineer', 'All 6 plants', ('PIN set', 'green')),
          ('IK', 'Ibrahim K.', 'ibrahim.k@koyo1.ng', 'Maintenance Technician', 'Koyo 1', ('PIN set', 'green')),
          ('KE', 'Kemi E.', 'kemi.e@koyo1.ng', 'Machine Operator', 'Koyo 1', ('PIN set', 'green')),
          ('YB', 'Yusuf B.', 'yusuf.b@koyo1.ng', 'Machine Operator', 'Koyo 1', ('No PIN yet', 'amber')),
          ('AF', 'Amaka F.', 'amaka.f@koyo.ng', 'Floor Supervisor, Quality Inspector', 'Poultry farm', ('PIN set', 'green')),
          ('ER', 'ERP sync', 'erp-sync@koyo.ng', 'Factory Integration', 'API key · read only', ('No kiosk', 'gray'))]
    ur = ''.join(f'<div class="lr" style="{UC};margin:0;cursor:default;min-height:48px"><span style="display:flex;align-items:center;gap:8px;min-width:0"><span class="av">{a}</span><span class="c"><div class="t1">{n}</div><div class="m tab">{e}</div></span></span><span class="c qs" style="color:var(--ink-gray-7)">{r}</span><span class="c qs">{p}</span><span>{bd(*b)}</span><span style="color:var(--ink-gray-4);display:flex">{ic("more","i s35")}</span></div>' for a, n, e, r, p, b in us)
    return f'''{title('Users and roles', 'Frappe users with Frappe Factory roles. Roles give permissions; plants and kiosk assignments limit where they apply.', btn("Invite user","plus") )}
<div style="display:flex;flex-direction:column;gap:20px;padding-top:20px">
<div style="display:flex;flex-wrap:wrap;gap:6px">{rc}</div>
<div style="display:flex;gap:8px;align-items:center"><span class="in muted" style="width:240px">{ic("search")}<span class="grow">Search users</span></span><span class="chip"><span class="k">Plant</span>All</span><span class="chip"><span class="k">Role</span>All</span></div>
<div class="list" style="margin:0"><div class="lh" style="{UC};margin:0"><span>User</span><span>Roles</span><span>Plants</span><span>Kiosk PIN</span><span></span></div>{ur}</div>
{section('Rules', [
  row('Restart and QA release need different people', 'The Quality Inspector who releases a line cannot also restart it as Floor Supervisor.', SW_ON),
  row('Release with deviation needs a Factory Manager', 'A second signature, from someone who is not the inspector.', SW_ON),
  row('Who edits process flows and layouts', 'Factory Manager, acting as Floor Engineer, and Maintenance Engineer. Everyone else can read them.', f'<span class="in out" style="width:180px"><span class="grow">2 roles</span>{ic("chev-d","i s35")}</span>'),
])}
</div>'''

# ---------------- Process templates
TEMPLATES = [
  ('Sachet and bottled water', 'v3 · I-Varse', 'Koyo 1, Plant B, Plant D', 'LayoutEditor.dc.html', [S.ro(), S.uv(), S.filler(True)], True),
  ('Rice milling', 'v2 · I-Varse', 'Rice mill', 'LayoutRice.dc.html', [I.husker(), I.whitener(), I.color_sorter()], False),
  ('Edible oil', 'v1 · I-Varse', 'Oil mill', 'LayoutOil.dc.html', [I.expeller(), I.column(), I.bottle_filler()], False),
  ('Poultry farm', 'v1 · I-Varse', 'Poultry farm', 'LayoutPoultry.dc.html', [I.poultry_house(), I.exhaust_fan(), I.egg_grader()], False),
  ('Start blank', 'v1 · I-Varse', '—', 'LayoutEditor.dc.html', [S.tank_v(0.5), I.conveyor(), I.fan()], False),
]
def templates():
    TC = 'grid-template-columns:minmax(0,1.3fr) 120px minmax(0,1fr) 110px'
    tl = ''.join(f'''<div class="lr" style="{TC};margin:0;min-height:56px;{"background:var(--surface-gray-2)" if on else ""}"><span style="display:flex;align-items:center;gap:10px;min-width:0"><span style="display:flex;gap:2px">{"".join(S.box(x, 22) for x in pics)}</span><span class="t1">{n}</span></span><span class="qs">{v}</span><span class="c qs">{u}</span><a href="{lay}" class="btn ghost" style="justify-self:end">{ic("pen")}Edit layout</a></div>''' for n, v, u, lay, pics, on in TEMPLATES)
    def sets(a, b, href=None, link='Edit'):
        l = f'<a href="{href}" style="font-size:13px">{link}</a>' if href else ''
        return f'<div style="display:grid;grid-template-columns:170px minmax(0,1fr) 80px;gap:12px;padding:10px 0;font-size:14px;line-height:1.45"><span style="color:var(--ink-gray-6)">{a}</span><span style="color:var(--ink-gray-8)">{b}</span><span style="text-align:right">{l}</span></div>'
    return f'''{title('Process templates', 'What a new plant starts with for its industry. Editing a template changes new plants only; each plant keeps its own copy.', f'{btn("Import")}<button type="button" class="btn solid">New template</button>')}
<div style="display:flex;flex-direction:column;gap:24px;padding-top:20px">
<div class="list" style="margin:0"><div class="lh" style="{TC};margin:0"><span>Template</span><span>Version</span><span>Used by</span><span></span></div>{tl}</div>
<section style="display:flex;flex-direction:column;gap:4px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h3 style="margin:0;font-size:14px;font-weight:600;color:var(--ink-gray-8)">Sachet and bottled water · sets up</h3>{btn("Duplicate","copy","ghost")}</div>
<div class="divy">
{sets('Units of count', 'Machine unit: sachet, 50 cl. Pack unit: bag of 20 sachets (10 L). Stock unit: bag. Rated filler speed 2,000 sachets an hour.')}
{sets('Starter layout', 'Treatment and filling: borehole, RO, UV, lead analyser, T4 verify, T5 quarantine, 10 fillers', 'LayoutEditor.dc.html', 'Edit layout')}
{sets('Symbol pack', 'Water and beverage, 7 symbols, plus the 15 general ones', 'Symbols.dc.html', 'Open')}
{sets('Alarm definitions', '21, with cause and action filled in', 'AlarmDefs.dc.html')}
{sets('Interlocks', '3 quality-related: lead high-high, turbidity high, UV intensity low')}
{sets('Quality hold templates', 'QHT-003 lead trip · QHT-004 turbidity trip', 'QHTemplate.dc.html', 'Edit')}
{sets('Downtime reasons', '18: film change or splice, jaw jam, seal temperature low, power dip and more', 'Downtime.dc.html', 'Open')}
{sets('Kiosk views', 'Line (filling and packing), Maintenance, Quality')}
{sets('KPIs', 'OEE, bags per hour, litres of treated water per bag, rejects %, diesel per 1,000 bags')}
</div></section></div>'''

# ---------------- WhatsApp
def whatsapp():
    RC = 'grid-template-columns:minmax(0,1.3fr) minmax(0,1.2fr) 90px'
    rules = [('Priority 1 alarm or interlock trip', 'Floor Supervisor, Quality Inspector, Factory Manager', SW_ON),
             ('Quality hold opened or decided', 'Quality Inspector, Factory Manager', SW_ON),
             ('Spare part request', 'Storekeeper', SW_ON),
             ('Runway under 24 h (water, diesel, feed, film)', 'Floor Supervisor, Storekeeper', SW_ON),
             ('Shift summary at shift end', 'Factory Manager', SW_ON),
             ('Priority 3 alarm', 'Nobody · in-app only', SW_OFF)]
    rr = ''.join(f'<div class="lr" style="{RC};margin:0;cursor:default;min-height:52px"><span class="t1" style="white-space:normal">{a}</span><span class="c qs" style="white-space:normal;color:var(--ink-gray-7)">{b}</span><span style="justify-self:end">{c}</span></div>' for a, b, c in rules)
    return f'''{title('WhatsApp', 'Messages through your frappe_whatsapp_openwa app. In-app and email notifications always go too.', btn("Send test message","msg"))}
<div style="display:flex;flex-direction:column;gap:24px;padding-top:20px">
<div class="alert" style="background:var(--surface-green-2);border-color:var(--outline-green-3)"><span style="color:var(--ink-green-7);display:flex">{ic("check")}</span><span style="font-size:14px;color:var(--ink-gray-8)">Connected as <b style="font-weight:500">+234 803 555 0142</b> · Koyo Industries · last message 08:14 (TRIP-0007)</span></div>
<section style="display:flex;flex-direction:column;gap:8px"><h3 style="margin:0;font-size:14px;font-weight:600;color:var(--ink-gray-8)">Who gets what</h3>
<div class="list" style="margin:0"><div class="lh" style="{RC};margin:0"><span>When</span><span>Who, by role at that plant</span><span></span></div>{rr}</div></section>
{section('Delivery', [
  row('Quiet hours', 'Hold non-urgent messages from 22:00 to 06:00. Priority 1 and trips always go.', f'<span class="in out" style="width:150px"><span class="grow">22:00 – 06:00</span>{ic("chev-d","i s35")}</span>'),
  row('Reply to acknowledge', 'People can reply ACK to acknowledge an alarm from WhatsApp; the reply is logged against their Frappe user.', SW_ON),
])}
</div>'''

# ---------------- ThingsBoard
def tb():
    PC = 'grid-template-columns:minmax(0,1fr) 150px 150px 100px'
    pl = [('Koyo 1', 'Edge box, direct', 'MQTT · 2 s', ('Live', 'green')), ('Plant B', 'ThingsBoard', 'Rule chain · 5 s', ('Live', 'green')),
          ('Plant D', 'Edge box, direct', 'MQTT · 2 s', ('Offline 3 h', 'gray')), ('Oil mill', 'Edge box, direct', 'MQTT · 2 s', ('Live', 'green')),
          ('Rice mill', 'Edge box, direct', 'MQTT · 2 s', ('Live', 'green')), ('Poultry farm', 'Edge box, direct', 'MQTT · 10 s', ('Live', 'green'))]
    pr = ''.join(f'<div class="lr" style="{PC};margin:0;cursor:default"><span class="t1">{a}</span><span class="qs" style="color:var(--ink-gray-7)">{b}</span><span class="qs tab">{c}</span><span>{bd(*d)}</span></div>' for a, b, c, d in pl)
    return f'''{title('ThingsBoard', 'Optional. A plant can send its data through an existing ThingsBoard instead of an edge box; the screens look the same either way.')}
<div style="display:flex;flex-direction:column;gap:24px;padding-top:20px">
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px">
{field('ThingsBoard URL', inp('https://tb.koyo.ng', 'out'), req=True)}
{field('Tenant', inp('Koyo Industries', 'out'))}
{field('Integration token', inp('••••••••••••••••', 'out'), hint='Stored encrypted. Read only: Frappe Factory never writes to ThingsBoard.')}
<div style="display:flex;align-items:flex-end;gap:8px">{btn("Verify connection","check")}<span class="qs" style="padding-bottom:6px">Verified 07:30 · 214 devices</span></div>
</div>
<section style="display:flex;flex-direction:column;gap:8px"><h3 style="margin:0;font-size:14px;font-weight:600;color:var(--ink-gray-8)">Where each plant's data comes from</h3>
<div class="list" style="margin:0"><div class="lh" style="{PC};margin:0"><span>Plant</span><span>Source</span><span>Path</span><span>Status</span></div>{pr}</div>
<span class="qs">Change a plant's source in its Plant settings → Connector.</span></section>
{section('Mapping', [row('Device profiles to symbols', 'ThingsBoard device profiles map to Frappe Factory asset types; telemetry keys map to tags.', f'<a href="Devices.dc.html" class="btn">Open mapping</a>')])}
</div>'''

build('CompanyGeneral.dc.html', 'General', general())
build('CompanyUsers.dc.html', 'Users and roles', users())
build('CompanyTemplates.dc.html', 'Process templates', templates())
build('CompanyWhatsApp.dc.html', 'WhatsApp', whatsapp())
build('CompanyTB.dc.html', 'ThingsBoard', tb())

# ---------------- My settings (the signed-in user's own dialog)
def my_nav(active):
    items = [('Profile', 'users'), ('Kiosk PIN', 'lock'), ('Notifications', 'bell'), ('Theme', 'moon')]
    o = '<div style="display:flex;flex-direction:column;gap:2px;margin-top:8px">'
    for n, i in items:
        st = 'background:var(--surface-elevation-3);box-shadow:var(--shadow-sm);color:var(--ink-gray-8)' if n == active else 'color:var(--ink-gray-7)'
        o += f'<span style="display:flex;align-items:center;gap:8px;height:28px;padding:0 8px;border-radius:8px;font-size:14px;{st}">{ic(i)}{n}</span>'
    return o + '</div>'
dots = lambda n, f: ''.join(f'<span style="width:12px;height:12px;border-radius:50%;{"background:var(--ink-gray-9)" if i < f else "border:2px solid var(--outline-gray-3)"}"></span>' for i in range(n))
pin_panel = f'''{title('Kiosk PIN', 'Your PIN signs you in on the kiosks you are assigned to, after you tap your name. It works only with your Frappe user: a PIN on its own signs no one in.')}
<div style="display:flex;flex-direction:column;gap:24px;padding-top:20px">
<div class="alert" style="background:var(--surface-green-2);border-color:var(--outline-green-3)"><span style="color:var(--ink-green-7);display:flex">{ic("check")}</span><span style="font-size:14px;color:var(--ink-gray-8)">PIN set on 3 Nov 2026. Last used 07:12 on Quality lab T-06.</span></div>
<section style="display:flex;flex-direction:column;gap:14px"><h3 style="margin:0;font-size:14px;font-weight:600;color:var(--ink-gray-8)">Change your PIN</h3>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px">
{field('Your Frappe password', inp('••••••••••', 'focus'), req=True, hint='Proves it is you before the PIN changes.')}
<label class="fl"><span class="lab">New PIN <span class="req">*</span></span><span class="in" style="gap:8px">{dots(6, 6)}</span><span class="hint">6 digits</span></label>
<label class="fl"><span class="lab">Confirm new PIN <span class="req">*</span></span><span class="in" style="gap:8px">{dots(6, 3)}</span></label></div>
<div class="qs" style="line-height:1.6">Not allowed: 6 of the same digit, a straight run such as 123456 or 654321, or your last 3 PINs. 5 wrong tries lock you on every kiosk for 15 minutes; a Factory Manager can unlock you.</div>
<div><button type="button" class="btn solid" disabled>Save PIN</button></div></section>
<section style="display:flex;flex-direction:column;gap:8px"><h3 style="margin:0;font-size:14px;font-weight:600;color:var(--ink-gray-8)">Kiosks you can sign in on</h3>
<div class="divy" style="font-size:14px">
<div style="display:flex;justify-content:space-between;padding:10px 0"><span style="color:var(--ink-gray-8)">Quality lab T-06 · Koyo 1</span><span class="qs">Quality view · for deviation approvals</span></div>
<div style="display:flex;justify-content:space-between;padding:10px 0"><span style="color:var(--ink-gray-8)">Filling hall T-02 · Koyo 1</span><span class="qs">Line view</span></div></div></section>
<section style="display:flex;flex-direction:column;gap:8px"><h3 style="margin:0;font-size:14px;font-weight:600;color:var(--ink-gray-8)">Recent kiosk sign-ins</h3>
<div class="divy tab" style="font-size:13px;color:var(--ink-gray-7)">
<div style="display:flex;justify-content:space-between;padding:8px 0"><span>22 Nov 07:12 · Quality lab T-06</span><span>Morning shift · session KS-0225</span></div>
<div style="display:flex;justify-content:space-between;padding:8px 0"><span>19 Nov 15:40 · Quality lab T-06</span><span>Afternoon shift · approved QH-0029 deviation</span></div></div></section>
</div>'''
import s_dashboard
from s_dashboard import head as dh, body as db
bg = shell('Dashboard.dc.html', dh, db, scope='company')
dlg = f'''<div class="ff" style="position:absolute;inset:0;display:block;min-height:0;background:transparent"><div class="overlay"></div>
<div class="dialog" role="dialog" aria-label="My settings" style="left:50%;top:48px;transform:translateX(-50%);width:960px;height:800px;display:flex">
<div style="width:220px;flex-shrink:0;background:var(--surface-sidebar);border-right:1px solid var(--outline-gray-1);padding:8px;display:flex;flex-direction:column">
<div style="display:flex;align-items:center;gap:8px;height:40px;padding:0 6px"><span class="av" style="width:24px;height:24px;flex:0 0 24px;font-size:10px">TB</span><span style="display:flex;flex-direction:column;line-height:1.15"><span style="font-weight:500;color:var(--ink-gray-8)">Tunde B.</span><span class="qs" style="font-size:12px">My settings</span></span></div>{my_nav('Kiosk PIN')}</div>
<div style="flex:1;min-width:0;display:flex;flex-direction:column;position:relative"><div style="position:absolute;right:16px;top:16px"><a href="Dashboard.dc.html" class="btn ghost ico" aria-label="Close">{ic("x")}</a></div>
<div style="flex:1;overflow:auto;padding:40px 3.5rem 64px">{pin_panel}</div></div></div></div>'''
write('MySettings.dc.html', page('My settings', f'<div style="position:relative">{bg}{dlg}</div>', {"$preview": {"width": 1440, "height": 900}}))
