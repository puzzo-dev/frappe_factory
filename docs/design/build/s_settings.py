from ff import *
from s_plantbg import plant_bg

NAV = [
  ('Plant', [('General','factory'),('Shifts','clock'),('Downtime reasons','clipboard')]),
  ('Data', [('Connector','radio'),('Data retention','server')]),
  ('Alerts', [('Notifications','bell'),('WhatsApp','msg')]),
  ('Control', [('Commands','zap')]),
  ('Access', [('People and roles','users')]),
]
def nav(active):
    o = ''
    for g, items in NAV:
        o += f'<div style="display:flex;align-items:center;height:28px;padding:0 8px;font-size:14px;color:var(--ink-gray-5);margin-top:8px">{g}</div><div style="display:flex;flex-direction:column;gap:2px">'
        for n, i in items:
            on = n == active
            st = 'background:var(--surface-elevation-3);box-shadow:var(--shadow-sm);color:var(--ink-gray-8)' if on else 'color:var(--ink-gray-7)'
            h = {'Connector': 'Settings.dc.html', 'Commands': 'SettingsCommands.dc.html', 'Downtime reasons': 'Downtime.dc.html', 'People and roles': 'CompanyUsers.dc.html', 'WhatsApp': 'CompanyWhatsApp.dc.html'}.get(n)
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
<div style="display:flex;flex-direction:column;gap:44px;padding-top:24px">
<section style="display:flex;flex-direction:column;gap:8px">
{option('Frappe Factory edge', 'OpsEdge reads the PLCs and publishes to the plant MQTT broker. Data, alarms and trips stay on site if the internet drops, then sync.', True)}
{option('ThingsBoard', 'Use an existing ThingsBoard server. Frappe Factory pulls telemetry and alarms through the ThingsBoard API. Community Edition is free; the source-available licence limits some uses.', False)}
</section>
{section('Edge', [
  row('Edge agent', 'OpsEdge K1 · v0.4.2 · online · last message 1 s ago', bd('Online','green','g')),
  row('MQTT broker', 'Mosquitto on the edge box. Topics factory/koyo-1/…', f'<span class="in out" style="width:260px"><span class="grow tab">mqtts://edge.koyo1.local:8883</span></span>'),
  row('Live update interval', 'How often open screens refresh. Interlocked tags are always sent on change.', f'<span class="in out" style="width:120px">{"<span class=grow>2 s</span>"}{ic("chev-d","i s35")}</span>'),
  row('Cloud sync', 'Outbox to OpsCloud. 0 messages waiting.', '<span class="qs">Last sync 08:45:58</span>'),
])}
{section('Time-series data', [
  row('Database', 'TimescaleDB 2.17 on the plant site. Hypertable ff_tag_value.', bd('Healthy','green')),
  row('Keep raw values', 'Every reading at full speed. Used by Trends up to 30 days.', f'<span class="in out" style="width:120px"><span class="grow">30 days</span>{ic("chev-d","i s35")}</span>'),
  row('Keep 1-minute averages', 'Continuous aggregate. Used for reports and longer trends.', f'<span class="in out" style="width:120px"><span class="grow">2 years</span>{ic("chev-d","i s35")}</span>'),
  row('Compress after', 'Older chunks are compressed, about 10× smaller.', f'<span class="in out" style="width:120px"><span class="grow">7 days</span>{ic("chev-d","i s35")}</span>'),
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
<div class="dialog" role="dialog" aria-label="Koyo 1 plant settings" style="left:auto;right:12px;top:12px;bottom:12px;width:1000px;height:auto;display:flex;flex-direction:column">
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
