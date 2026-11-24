from ff import *
from s_plantbg import plant_bg

NAV = [
  ('Plant', [('General','factory'),('Shifts','clock'),('Downtime reasons','clipboard')]),
  ('Data', [('Connector','radio'),('Data retention','server')]),
  ('Alerts', [('Notifications','bell'),('WhatsApp','msg')]),
  ('Control', [('Commands','zap')]),
  ('Access', [('People and roles','users')]),
]
PANEL_FILE = {'General': 'SettingsGeneral.dc.html', 'Shifts': 'SettingsShifts.dc.html', 'Downtime reasons': 'SettingsReasons.dc.html', 'Connector': 'Settings.dc.html',
              'Data retention': 'SettingsRetention.dc.html', 'Notifications': 'SettingsNotify.dc.html', 'WhatsApp': 'SettingsWhatsApp.dc.html', 'Commands': 'SettingsCommands.dc.html', 'People and roles': 'SettingsPeople.dc.html'}
def nav(active):
    o = ''
    for g, items in NAV:
        o += f'<div style="display:flex;align-items:center;height:28px;padding:0 8px;font-size:14px;color:var(--ink-gray-6);margin-top:8px">{g}</div><div style="display:flex;flex-direction:column;gap:2px">'
        for n, i in items:
            on = n == active
            st = 'background:var(--surface-elevation-3);box-shadow:var(--shadow-sm);color:var(--ink-gray-8)' if on else 'color:var(--ink-gray-7)'
            h = PANEL_FILE[n]
            tag = f'a href="{h}"' if h else 'span'
            o += f'<{tag} style="display:flex;align-items:center;gap:8px;height:28px;padding:0 8px;border-radius:8px;font-size:14px;text-decoration:none;{st}">{ic(i)}{n}</{tag.split()[0]}>'
        o += '</div>'
    return o

def row(title, desc, control, top=False):
    al = 'flex-start' if top else 'center'
    return f'<div style="display:flex;align-items:{al};gap:32px;padding:14px 0"><div style="flex:1;min-width:0"><span style="display:block;font-size:14px;font-weight:500;color:var(--ink-gray-8)">{title}</span><span style="display:block;margin-top:4px;font-size:14px;line-height:20px;color:var(--ink-gray-6)">{desc}</span></div><div style="flex-shrink:0;display:flex;justify-content:flex-end">{control}</div></div>'

def section(title, rows):
    h = f'<h3 style="margin:0 0 2px;font-size:14px;font-weight:600;color:var(--ink-gray-8)">{title}</h3>' if title else ''
    return f'<section>{h}<div class="divy">{"".join(rows)}</div></section>'

def option(title, desc, on):
    return f'<label style="display:grid;grid-template-columns:16px minmax(0,1fr);gap:10px;padding:12px;border-radius:10px;border:1px solid {"var(--ink-gray-9)" if on else "var(--outline-gray-2)"};cursor:pointer"><span class="rd{" on" if on else ""}" style="margin-top:2px"></span><span style="display:flex;flex-direction:column;gap:4px"><span style="font-weight:500;color:var(--ink-gray-8)">{title}</span><span style="font-size:13px;line-height:1.5;color:var(--ink-gray-6)">{desc}</span></span></label>'

def connector_panel():
    return f'''<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px"><div style="display:flex;flex-direction:column;gap:4px"><h2 style="margin:0;font-size:16px;font-weight:600;color:var(--ink-gray-8)">Connector</h2><p style="margin:0;font-size:14px;color:var(--ink-gray-6)">How Koyo 1's live data reaches Frappe Factory.</p></div>{btn("Test now","refresh")}</div>
<div style="display:flex;flex-direction:column;gap:40px;padding-top:24px">
<section style="display:flex;flex-direction:column;gap:8px">
{option('Edge box · Frappe Factory in the cloud', 'The edge box reads the PLCs, sounds the siren and sends everything to this site through its uplink. OpsKiosk at the plant keeps the kiosks working on the LAN when the internet drops.', True)}
{option('Edge box with its own Frappe site', 'A full Frappe Factory site also runs on the edge box and syncs to this one, so office screens at the plant keep working when the internet drops. For plants with poor internet.', False)}
{option('ThingsBoard', 'Use an existing ThingsBoard server instead of an edge box. Frappe Factory pulls telemetry and alarms through the ThingsBoard API.', False)}
</section>
{section('Uplink · edge box to this site', [
  row('Broker', 'The MQTT broker this site listens on. The edge box connects out to it, so the plant needs no open ports.', f'<span class="in out" style="width:280px"><span class="grow tab">mqtts://mqtt.koyo.ng:8883</span></span>'),
  row('Client ID', 'One per plant. Topics are factory/koyo-1/…', '<span class="in out" style="width:280px"><span class="grow tab">opsedge-koyo-1</span></span>'),
  row('Credentials', 'Username and password for this plant only, limited to its own topics. Shown once.', f'<span style="display:flex;gap:8px;align-items:center"><span class="qs tab">opsedge-koyo-1 · ••••••</span>{btn("Reset")}</span>'),
  row('Pair the edge box', 'Run opsedge pair with this code on the edge box. It downloads the broker, client ID and credentials above.', f'<span style="display:flex;gap:8px;align-items:center"><span class="in out" style="width:140px"><span class="grow tab">K1-7QF-2M9</span></span>{btn("New code")}</span>'),
  row('Uplink status', 'OpsEdge K1 · v0.4.2 · connected 3 h 12 min · 0 messages waiting', bd('Connected','green','g')),
  row('Edge box page', 'https://opsedge-k1.local · reachable on the plant network only', f'<a class="btn" href="EdgeStatus.dc.html">{ic("ext")}Open</a>'),
])}
{section('On the edge box', [
  row('Local broker', 'Mosquitto on OpsEdge K1 for the agent and the uplink. Set up by the edge installer; nothing to configure.', bd('Running','green','g')),
  row('Buffer', 'Readings kept on the box while the uplink is down, then sent in order.', f'<span class="in out" style="width:120px"><span class="grow">7 days</span>{ic("chev-d","i s35")}</span>'),
  row('Live update interval', 'How often open screens refresh. Interlocked tags are always sent on change.', f'<span class="in out" style="width:120px"><span class="grow">2 s</span>{ic("chev-d","i s35")}</span>'),
])}
</div>'''

def commands_panel():
    sw = lambda label, desc, state, extra='': f'''<div style="display:grid;grid-template-columns:28px minmax(0,1fr) auto;gap:12px;align-items:center;padding:14px 0"><span style="width:28px;height:28px;border-radius:50%;display:grid;place-items:center;background:{"var(--surface-green-2)" if state else "var(--surface-gray-2)"};color:{"var(--ink-green-7)" if state else "var(--ink-gray-5)"}">{ic("check","i s35") if state else ic("x","i s35")}</span><span><span style="display:block;font-weight:500;color:var(--ink-gray-8)">{label}</span><span style="display:block;margin-top:4px;font-size:14px;line-height:20px;color:var(--ink-gray-6)">{desc}</span></span>{extra}</div>'''
    return f'''<div style="display:flex;flex-direction:column;gap:4px"><h2 style="margin:0;font-size:16px;font-weight:600;color:var(--ink-gray-8)">Commands</h2><p style="margin:0;font-size:14px;color:var(--ink-gray-6)">Send setpoints and start or stop signals from Frappe Factory to the plant.</p></div>
<div style="display:flex;flex-direction:column;gap:44px;padding-top:24px">
<div class="alert" style="background:var(--surface-gray-1);border-color:var(--outline-gray-1)"><span style="color:var(--ink-gray-6);display:flex">{ic("lock")}</span><div style="display:flex;flex-direction:column;gap:4px;font-size:14px;line-height:1.5;color:var(--ink-gray-7)"><span class="ttl">Koyo 1 is monitor only</span>A command goes through only when all three switches below are on. Safety interlocks stay in the PLC whatever you set here; Frappe Factory can never bypass or reset them.</div></div>
<section><h3 style="margin:0 0 2px;font-size:14px;font-weight:600;color:var(--ink-gray-8)">Three switches</h3><div class="divy">
{sw('1 · Commands for this plant', 'Turned on here by a Factory Manager. Every command is logged with who, when and the value.', False, '<span class="sw"></span>')}
{sw('2 · The tag is writable', 'Set per tag in Devices and tags. 0 of 132 tags are writable.', False, '<a href="Devices.dc.html" style="font-size:13px">Open tags</a>')}
{sw('3 · The edge allows writes', 'allow_write in the OpsEdge K1 config file on the plant PC. Only someone at the plant can change it.', False, '<span class="qs tab">allow_write = false</span>')}
</div></section>
{section('When commands are on', [
  row('Confirm every command', 'Show the current value, the new value and the tag before sending.', '<span class="sw on dis"></span>'),
  row('Second person for setpoints', 'A Floor Supervisor approves setpoint changes made by an operator.', '<span class="sw dis"></span>'),
  row('Wait for acknowledgement', 'The edge reports success only after the PLC reads back the new value. Times out after 5 s.', '<span class="sw on dis"></span>'),
])}
</div>'''

def build(name, active, panel):
    bg = plant_bg()
    dlg = f'''{closer("dlg")}<div class="ff ffov" style="position:absolute;inset:0;display:block;min-height:0;background:transparent"><label for="dlg" class="overlay" aria-label="Close"></label>
<div class="dialog" role="dialog" aria-label="Koyo 1 plant settings" style="left:50%;top:40px;transform:translateX(-50%);width:1040px;max-height:820px;display:flex;flex-direction:column">
<div style="display:flex;align-items:center;gap:10px;height:56px;padding:0 16px 0 20px;border-bottom:1px solid var(--outline-gray-1);flex-shrink:0"><span style="width:28px;height:28px;border-radius:7px;background:var(--surface-gray-3);color:var(--ink-gray-8);display:grid;place-items:center;font-size:12px;font-weight:600">K1</span><span style="display:flex;flex-direction:column;line-height:1.15"><span style="font-weight:600;color:var(--ink-gray-9);font-size:16px">Plant settings · Koyo 1</span><span class="qs" style="font-size:12px">This plant only. App-wide settings are in the app menu.</span></span><span style="margin-left:auto">{close_btn("dlg")}</span></div>
<div style="flex:1;min-height:0;display:flex">
<div style="width:220px;flex-shrink:0;background:var(--surface-sidebar);border-right:1px solid var(--outline-gray-1);padding:8px;display:flex;flex-direction:column">
<div style="height:4px"></div>{nav(active)}</div>
<div style="flex:1;min-width:0;display:flex;flex-direction:column;position:relative">
<div style="flex:1;overflow:auto;padding:32px 4rem 64px">{panel}</div></div>
</div></div></div>'''
    write(name, page('Plant settings', f'<div style="position:relative">{bg}{dlg}</div>', {"$preview": {"width": 1440, "height": 900}}))

build('Settings.dc.html', 'Connector', connector_panel())
build('SettingsCommands.dc.html', 'Commands', commands_panel())

def ptitle(t, d, act=''):
    return f'<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px"><div style="display:flex;flex-direction:column;gap:4px"><h2 style="margin:0;font-size:16px;font-weight:600;color:var(--ink-gray-8)">{t}</h2><p style="margin:0;font-size:14px;color:var(--ink-gray-6)">{d}</p></div>{act}</div>'
def dd(v, w=140):
    return f'<span class="in out" style="width:{w}px"><span class="grow">{v}</span>{ic("chev-d","i s35")}</span>'
SWON, SWOFF = '<span class="sw on"></span>', '<span class="sw"></span>'
def wrap(*parts):
    return '<div style="display:flex;flex-direction:column;gap:36px;padding-top:24px">' + ''.join(parts) + '</div>'
def simple_list(cols, heads, rows):
    return f'<div class="list" style="margin:0"><div class="lh" style="{cols};margin:0">{"".join(f"<span>{h}</span>" for h in heads)}</div>' + ''.join(f'<div class="lr" style="{cols};margin:0;cursor:default;min-height:44px">{"".join(f"<span class=c>{c}</span>" for c in r)}</div>' for r in rows) + '</div>'

def general_panel():
    return ptitle('General', 'Koyo 1 only. Company-wide defaults are in App settings.') + wrap(
      '<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px">' + field('Plant name', inp('Koyo 1', 'out'), req=True) + field('Code', inp('K1', 'out'), req=True) +
      field('Industry', sel('Sachet water', 'out'), hint='Set from the Process Template when the plant was added.') + field('ERPNext warehouse', sel('Koyo 1 · Stores', 'out')) +
      field('Time zone', sel('Africa/Lagos · UTC+01:00', 'out')) + field('Address', inp('Plot 14, Ogere Industrial Layout', 'out')) + '</div>',
      section('Units', [row('Pack unit', 'A bag is 20 sachets of 50 cl. Machine rates stay in sachets.', dd('Bag · 20 sachets', 180)),
                        row('Show the machine unit too', 'For example 1,743 bags · 34,860 sachets.', SWON)]),
      section('Status', [row('Plant is active', 'Turning it off hides the plant from lists and stops alarms. History is kept.', SWON)]))

def shifts_panel():
    C = 'grid-template-columns:minmax(0,1fr) 110px 110px 150px'
    return ptitle('Shifts', 'Shift Types for Koyo 1. Runs, downtime and handovers are counted per shift.', btn('Add shift', 'plus')) + wrap(
      simple_list(C, ['Shift', 'Starts', 'Ends', 'Supervisor'], [('Morning', '06:00', '14:00', 'Musa A.'), ('Afternoon', '14:00', '22:00', 'Bola N.'), ('Night', '22:00', '06:00', 'Musa A. · rota')]),
      section('Handover', [row('Handover is required', 'A shift cannot close until the outgoing supervisor signs the handover.', SWON),
                           row('Overlap', 'Time both supervisors are on the floor.', dd('15 min', 110)),
                           row('Weekly rota', 'Supervisors rotate every Monday at 06:00.', SWON)]))

def reasons_panel():
    C = 'grid-template-columns:minmax(0,1fr) 120px 200px 72px'
    rs = [('Trip · interlock', 'Unplanned', 'Machine malfunction', 'Auto'), ('Film change or splice', 'Planned', 'Other', 'Kiosk'), ('Seal jaw fault', 'Unplanned', 'Machine malfunction', 'Kiosk'),
          ('Power dip', 'Unplanned', 'Electricity down', 'Auto'), ('No water in T4', 'Unplanned', 'Other', 'Auto'), ('Cleaning', 'Planned', 'Other', 'Kiosk'), ('Operator break', 'Planned', 'Machine operator errors', 'Kiosk')]
    return ptitle('Downtime reasons', 'The buttons operators see on the kiosk when a filler stops, in this order.', btn('Add reason', 'plus')) + wrap(
      simple_list(C, ['Reason', 'Type', 'ERPNext stop reason', 'Set by'], rs),
      section('Rules', [row('Ask for a reason after', 'Stops shorter than this are counted but not asked about.', dd('2 min', 110)),
                        row('Auto reasons win', 'Trips and power dips set the reason themselves; operators can add a note.', SWON)]))

def retention_panel():
    return ptitle('Data retention', 'How long Koyo 1 keeps its readings on the edge box and in the cloud.') + wrap(
      section('On the edge box · TimescaleDB', [row('Raw readings', 'Every value at full speed. Trends use them up to this age.', dd('7 days', 120)),
                                                   row('1-minute averages', 'Reports and long trends.', dd('2 years', 120)),
                                                   row('Compress after', 'Older chunks shrink about 10×.', dd('7 days', 120))]),
      section('Records', [row('Alarms and trips', 'Kept with their audit trail.', dd('Forever', 120)), row('Kiosk sessions', 'Log-ins, stop reasons, samples.', dd('5 years', 120))]),
      '<div class="qs">Using 38 GB of 200 GB on the plant PC. Cloud keeps 1-minute averages only.</div>')

def notify_panel():
    C = 'grid-template-columns:minmax(0,1fr) minmax(0,1.3fr) 64px 84px 64px'
    Y = ic('check', 'i s35')
    rt = [('Priority 1 alarms', 'Floor Supervisor on shift, Factory Manager', Y, Y, Y), ('Priority 2 alarms', 'Floor Supervisor on shift', Y, Y, ''),
          ('Priority 3 alarms', 'Floor Supervisor on shift', Y, '', ''), ('Quality holds', 'Quality Inspector, Floor Supervisor', Y, Y, ''),
          ('Maintenance requests', 'Maintenance Technician', Y, Y, ''), ('Stock below reorder', 'Storekeeper', Y, '', Y)]
    return ptitle('Notifications', 'Who at Koyo 1 is told about what. Alarms stay on the Alarms page until acknowledged; these only deliver them.') + wrap(
      simple_list(C, ['Event', 'Sent to', 'Bell', 'WhatsApp', 'Email'], rt),
      section('Escalation', [row('Unacknowledged alarms escalate', 'To the Floor Supervisor, then the Factory Manager, using each Alarm definition\'s response time.', SWON),
                             row('Quiet hours', 'Priority 3 waits until the shift starts. Priority 1 and 2 always go out.', SWOFF)]))

def whatsapp_panel():
    return ptitle('WhatsApp', 'Koyo 1 numbers and groups. The WhatsApp account itself is set up in App settings.') + wrap(
      section('Send to', [row('Koyo 1 floor group', 'Priority 1 and 2 alarms, trips and quality holds.', '<span class="qs tab">+234 803 ··· 4410</span>'),
                          row('Maintenance group', 'Faults and spare part requests from the kiosks.', '<span class="qs tab">+234 805 ··· 1182</span>'),
                          row('Supervisor on shift', 'Picked from the shift rota at send time.', SWON)]),
      section('Replies', [row('Acknowledge by reply', 'Replying ACK to an alarm message acknowledges it as that person, if their number is on their Frappe user.', SWON)]))

def people_panel():
    C = 'grid-template-columns:minmax(0,1fr) minmax(0,1fr) 120px'
    us = [('Musa A.', 'Floor Supervisor', 'T-02, T-03'), ('Bola N.', 'Floor Supervisor', 'T-02, T-03'), ('Grace O.', 'Quality Inspector', 'T-06, T-02'),
          ('Ibrahim K.', 'Maintenance Technician', 'T-05'), ('Kemi E.', 'Machine Operator', 'T-02'), ('Yusuf B.', 'Machine Operator', 'T-03'), ('Halima S.', 'Storekeeper', '—')]
    return ptitle('People and roles', 'Frappe users with access to Koyo 1, through a User Permission on this plant. Roles are set on the user.', btn('Add person', 'plus')) + wrap(
      simple_list(C, ['User', 'Role', 'Kiosks'], us),
      '<div class="qs" style="line-height:1.5">Tunde B. (Factory Manager) sees every plant and is not listed. Roles, invites and kiosk profiles for all plants are in App settings.</div>')

for f, n, p in [('SettingsGeneral.dc.html', 'General', general_panel), ('SettingsShifts.dc.html', 'Shifts', shifts_panel), ('SettingsReasons.dc.html', 'Downtime reasons', reasons_panel),
                ('SettingsRetention.dc.html', 'Data retention', retention_panel), ('SettingsNotify.dc.html', 'Notifications', notify_panel), ('SettingsWhatsApp.dc.html', 'WhatsApp', whatsapp_panel),
                ('SettingsPeople.dc.html', 'People and roles', people_panel)]:
    build(f, n, p())
