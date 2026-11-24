"""OpsEdge local UI: served by the edge box on the plant network (https://opsedge-k1.local).
For setting up and checking the box only. Tags, alarms and layouts are edited in Frappe Factory, never here."""
from ff import *

NAV = [('EdgeStatus.dc.html', 'gauge', 'Status'), ('EdgePair.dc.html', 'link', 'Pairing and network'), ('EdgeDevices.dc.html', 'cpu', 'Devices'),
       ('EdgeTags.dc.html', 'activity' if 'activity' in IC else 'chart', 'Live tags'), ('EdgeScan.dc.html', 'search', 'Scan'), ('EdgeLogs.dc.html', 'file', 'Logs and update')]

def side(active):
    items = ''.join(f'<a class="si{" on" if h == active else ""}" href="{h}"{" aria-current=page" if h == active else ""}>{ic(i)}<span class="lbl">{l}</span></a>' for h, i, l in NAV)
    return f'''<nav class="side" aria-label="OpsEdge">
<div style="display:flex;align-items:center;gap:8px;height:40px;margin:4px 0 6px;padding:0 6px"><span class="logo" aria-hidden="true" style="background:var(--surface-gray-10)">K1</span>
<span style="display:flex;flex-direction:column;min-width:0;flex:1"><span style="font-weight:500;color:var(--ink-gray-9);line-height:1.1">OpsEdge K1</span><span style="font-size:13px;color:var(--ink-gray-7);margin-top:3px;line-height:1.1">Koyo 1 · edge box</span></span></div>
<div class="sgrp" style="margin-top:8px">{items}</div>
<div class="side-foot" style="flex-direction:column;align-items:flex-start;gap:6px"><span><span class="dot g"></span> Uplink connected</span><span style="display:flex;gap:6px;align-items:center;white-space:nowrap">Ibrahim K. · <a href="EdgeLogin.dc.html">Log out</a></span></div></nav>'''

def head(title, sub, acts=''):
    return f'<header class="ph"><div style="display:flex;flex-direction:column;gap:2px"><div class="crumb"><span class="cur">{title}</span></div></div><div class="acts"><span class="qs" style="margin-right:4px">{sub}</span>{acts}</div></header>'

NOTE = f'<div class="inset" style="display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.5;color:var(--ink-gray-7)"><span style="display:flex;color:var(--ink-gray-6);margin-top:2px">{ic("info","i s35")}</span><span>This page is on the edge box and works without the internet. Tags, alarm definitions and layouts are changed in Frappe Factory and arrive here as a new config version.</span></div>'

def epage(fname, title, sub, body, acts=''):
    html = f'<div class="ff">{side(fname)}<main class="main">{head(title, sub, acts)}<div class="body" style="overflow:auto">{body}</div></main></div>'
    write(fname, page('OpsEdge · ' + title, html, {"$preview": {"width": 1440, "height": 900}}))

def kv(rows):
    return '<div style="display:flex;flex-direction:column">' + ''.join(f'<div style="display:grid;grid-template-columns:180px minmax(0,1fr) auto;gap:12px;align-items:center;min-height:40px;border-bottom:1px solid var(--outline-gray-1);font-size:14px"><span class="qs">{a}</span><span style="color:var(--ink-gray-8)">{b}</span><span>{c}</span></div>' for a, b, c in rows) + '</div>'
def card(title, inner, right=''):
    return f'<section class="card" style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h3">{title}</h2>{right}</div>{inner}</section>'
def tbl(cols, heads, rows):
    return f'<div class="list"><div class="lh" style="{cols}">{"".join(f"<span>{h}</span>" for h in heads)}</div>' + ''.join(f'<div class="lr" style="{cols};min-height:48px;cursor:default">{"".join(f"<span class=c>{c}</span>" for c in r)}</div>' for r in rows) + '</div>'

# ---------------- Login (local technician account; works offline)
login = f'''<div class="ff" style="display:grid;place-items:center;background:var(--surface-gray-1)">
<div style="width:400px;background:var(--surface-base);border-radius:16px;box-shadow:var(--shadow-lg);padding:32px;display:flex;flex-direction:column;gap:18px">
<div style="display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center"><span class="logo" style="width:44px;height:44px;flex-basis:44px;font-size:15px;background:var(--surface-gray-10)">K1</span>
<h1 style="margin:8px 0 0;font-size:22px;font-weight:600;color:var(--ink-gray-9)">OpsEdge K1</h1><p class="ps">Koyo 1 edge box · opsedge-k1.local</p></div>
{field('Username', inp('ibrahim.k', 'focus'))}{field('Password', inp('••••••••••'))}
<a href="EdgeStatus.dc.html" class="btn solid" style="height:36px;justify-content:center;text-decoration:none">Log in</a>
<span class="qs" style="text-align:center;line-height:1.5">Local technician accounts only, so this works without the internet. Created with <span class="tab">opsedge user add</span> on the box.</span>
</div></div>'''
write('EdgeLogin.dc.html', page('OpsEdge · Log in', login, {"$preview": {"width": 1440, "height": 900}}))

# ---------------- Status
kp = lambda k, v, d, col='': f'<div class="card kpi"><span class="k">{k}</span><span class="v"{f" style=color:{col}" if col else ""}>{v}</span><span class="d">{d}</span></div>'
status = f'''<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">
{kp('Uplink', 'Connected', 'mqtt.koyo.ng · 3 h 12 min')}{kp('Buffer', '0', 'messages waiting · holds 7 days')}{kp('Devices', '6 of 6', 'online · 132 tags')}{kp('Config', 'v41', 'from Frappe Factory · 22 Nov 07:58')}
</div>
<div style="display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:12px">
{card('Services', kv([("opsedge-agent", "Reading 6 devices · 1,204 values a minute", bd("Running","green","g")), ("opsedge-uplink", "Sending to mqtt.koyo.ng · 0 waiting", bd("Running","green","g")), ("mosquitto", "Local broker · 3 clients", bd("Running","green","g")), ("timescaledb", "Raw readings · 41 GB of 400 GB", bd("Running","green","g")), ("local alarms", "4 active · siren silenced 08:15 · stack light red", bd("Running","green","g")),  ("web", "This page", bd("Running","green","g"))]), btn("Restart all", "refresh"))}
{card('Box', kv([("Clock", "08:46:12 WAT · synced to pool.ntp.org 4 min ago", bd("OK","green")), ("Disk", "41% used", ""), ("Memory", "6.1 of 16 GB", ""), ("CPU", "18%", ""), ("Power", "UPS online · 92% · on generator mains", ""), ("Version", "OpsEdge 0.4.2 · up to date", "")]))}
</div>
{card('Last hour', f'<div class="inset" style="display:flex;flex-direction:column;gap:6px"><span class="qs">Values sent per minute</span>{spark([1180,1204,1199,1210,1204,1202,1190,1205,1204,1201,1204,1203], 1100, 60, "var(--ink-gray-8)", 1100, 1250)}</div>')}
{NOTE}'''
epage('EdgeStatus.dc.html', 'Status', 'Paired with frappe.koyo.ng · Koyo 1', status, btn('Test uplink', 'refresh'))

# ---------------- Pairing and network
pair = f'''<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px">
{card('Pairing', kv([("Site", "frappe.koyo.ng", bd("Paired","green","g")), ("Plant", "Koyo 1 · K1", ""), ("Broker", "mqtts://mqtt.koyo.ng:8883", ""), ("Client ID", '<span class="tab">opsedge-koyo-1</span>', ""), ("Paired", "3 Nov 2026 by Tunde B.", ""), ("Certificate", "Renews by itself · expires 3 Feb 2027", "")]) + f'<div style="display:flex;gap:8px;padding-top:4px">{btn("Pair again")}{btn("Unpair", kind="ghost")}</div><span class="qs" style="line-height:1.5">To pair, get a code from Frappe Factory → Plant settings → Connector and enter it here, or run <span class="tab">opsedge pair &lt;code&gt;</span>. The broker, client ID and credentials come with the code.</span>')}
{card('Network', kv([("Plant LAN", "eth0 · 192.168.10.20 · static", bd("Up","green")), ("PLC network", "eth1 · 10.0.1.20 · static", bd("Up","green")), ("Internet", "eth0 via 192.168.10.1 · 38 ms to broker", bd("Up","green")), ("Backup link", "GSM modem · MTN · used if the LAN is down", bd("Standby","gray")), ("Proxy", "None", ""), ("Name", "opsedge-k1.local", "")]) + f'<div style="display:flex;gap:8px;padding-top:4px">{btn("Edit network","pen")}</div>')}
</div>
{card('Uplink sessions · last 7 days', tbl('grid-template-columns:160px 160px 120px minmax(0,1fr)', ['Connected', 'Until', 'Length', 'Why it ended'], [
  ('22 Nov · 05:16', 'now', '3 h 30 min', '—'), ('22 Nov · 05:12', '22 Nov · 05:16', '4 min', 'Broker unreachable · ISP outage · 288 messages buffered, all sent'),
  ('19 Nov · 02:00', '22 Nov · 05:12', '3 days 3 h', 'Certificate renewed, reconnected'), ('17 Nov · 14:31', '19 Nov · 02:00', '1 day 11 h', 'Box rebooted for update 0.4.2'),
  ('16 Nov · 09:02', '17 Nov · 14:31', '1 day 5 h', 'Plant LAN switch replaced · 22 min on GSM backup')]))}
{NOTE}'''
epage('EdgePair.dc.html', 'Pairing and network', 'How this box reaches the plant and the cloud', pair)

# ---------------- Devices
DC = 'grid-template-columns:minmax(0,1.3fr) minmax(0,1fr) 92px 92px 92px 110px'
devs = [('PLC-1 · Delta DVP-12SE', 'Modbus TCP · 10.0.1.10:502 · unit 1', '84', '12 ms', '1 s', bd('Online','green','g')),
        ('PLC-2 · Delta DVP-12SE', 'Modbus TCP · 10.0.1.11:502 · unit 1', '30', '14 ms', '1 s', bd('Online','green','g')),
        ('DSE-7320 · generator', 'Modbus RTU · /dev/ttyUSB0 · 9600 · id 10', '9', '61 ms', '5 s', bd('Online','green','g')),
        ('EM-1 · grid meter', 'Modbus RTU · /dev/ttyUSB0 · 9600 · id 2', '6', '48 ms', '5 s', bd('Online','green','g')),
        ('LT-901 · diesel level', 'MQTT · wireless sensor · factory/koyo-1/lt901', '1', '—', '60 s', bd('Online','green','g')),
        ('Lead analyser AT-401', 'Modbus TCP · 10.0.1.30:502 · unit 3', '2', '22 ms', '1 s', bd('Online','green','g'))]
devices = f'''{tbl(DC, ['Device', 'Connection', 'Tags', 'Response', 'Polled every', 'State'], devs)}
<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px">
{card('PLC-1 · last 10 minutes', kv([("Reads", "600 of 600 OK", ""), ("Errors", "0 timeouts · 0 bad replies", ""), ("Slowest", "31 ms at 08:41", ""), ("Writes", "Off · commands are off for this plant", bd("Off","gray"))]))}
{card('Where devices come from', '<p class="ps" style="line-height:1.6;margin:0">Devices and tags are set up in Frappe Factory → Devices and tags and arrive here with each config version (now v41). This page shows whether the box can reach them. Use Scan to find new devices and send them to Frappe Factory.</p>' + f'<div><a class="btn" href="EdgeScan.dc.html">{ic("search")}Scan for devices</a></div>')}
</div>'''
epage('EdgeDevices.dc.html', 'Devices', '6 devices · config v41', devices, btn('Reload config', 'refresh'))

# ---------------- Live tags (read-only)
TC = 'grid-template-columns:minmax(0,1fr) minmax(0,1.2fr) 120px 88px 96px'
tags = [('AT-401.LEAD', 'PLC-1 · 40021 · ÷10', '<b style="color:var(--ink-red-7)">9.4 µg/L</b>', bd('Good','green'), '08:46:11'),
        ('AT-301.PH', 'PLC-1 · 40017 · ÷100', '8.00', bd('Good','green'), '08:46:11'), ('LT-201.LEVEL', 'PLC-1 · 40031 · 4–20 mA', '70 %', bd('Good','green'), '08:46:11'),
        ('FT-201.FLOW', 'PLC-1 · 40041 · ÷10', '6.0 m³/h', bd('Good','green'), '08:46:11'), ('P-401.RUN', 'PLC-1 · coil 12', 'Off', bd('Good','green'), '08:46:11'),
        ('ATS-1.GEN', 'PLC-1 · input DI 0.4', 'On', bd('Good','green'), '08:46:11'), ('GEN-1.LOAD', 'DSE-7320 · 1024', '78 kW', bd('Good','green'), '08:46:08'),
        ('LT-901.LEVEL', 'MQTT · lt901/level', '28 %', bd('Good','green'), '08:45:40'), ('UV-301.INT', 'PLC-2 · 40011', '96 %', bd('Good','green'), '08:46:11'),
        ('F9.COUNT', 'PLC-2 · 40109', '—', bd('Stale','amber'), '08:12:03')]
tagsb = f'''<div style="display:flex;gap:8px;align-items:center"><span class="in muted" style="width:260px">{ic("search")}<span class="grow">Search tags</span></span><span class="chip"><span class="k">Device</span>All</span><span class="chip"><span class="k">Quality</span>All</span><span class="qs" style="margin-left:auto">Read-only · refreshes every second</span></div>
{tbl(TC, ['Tag', 'Source', 'Value', 'Quality', 'Read at'], tags)}
<p class="qs" style="margin:0">Stale means no new value for 3 polls; F9 is stopped for maintenance. To change a tag's address or scaling, edit it in Frappe Factory.</p>'''
epage('EdgeTags.dc.html', 'Live tags', '132 tags · 1 stale', tagsb)

# ---------------- Scan
SC = 'grid-template-columns:28px minmax(0,1fr) minmax(0,1fr) 140px'
found = [('<span class="cb on"></span>', '10.0.1.12 · unit 1', 'Modbus TCP · replied to 40001–40120', bd('New','blue')),
         ('<span class="cb"></span>', '10.0.1.10 · unit 1', 'Modbus TCP · PLC-1', bd('Known','gray')),
         ('<span class="cb"></span>', '10.0.1.11 · unit 1', 'Modbus TCP · PLC-2', bd('Known','gray')),
         ('<span class="cb on"></span>', 'opc.tcp://10.0.1.40:4840', 'OPC UA · Siemens S7-1200 · 46 nodes', bd('New','blue')),
         ('<span class="cb"></span>', '/dev/ttyUSB0 · id 2, 10', 'Modbus RTU · EM-1, DSE-7320', bd('Known','gray'))]
scan = f'''<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">
{field('Network', sel('eth1 · 10.0.1.0/24'))}{field('Protocols', inp('<span class="chip" style="height:20px">Modbus TCP</span> <span class="chip" style="height:20px">OPC UA</span> <span class="chip" style="height:20px">Modbus RTU</span>'))}{field('Serial port', sel('/dev/ttyUSB0 · 9600 8N1'))}
</div>
<div style="display:flex;gap:8px;align-items:center">{btn("Scan again","refresh")}<span class="qs">Finished 08:40 · 254 addresses · 5 devices · reads only, never writes</span></div>
{tbl(SC, ['', 'Address', 'What answered', ''], found)}
{card('10.0.1.12 · unit 1 · first registers', tbl('grid-template-columns:120px 120px 120px minmax(0,1fr)', ['Register', 'Raw', 'As float', 'Looks like'], [
  ('40001', '17204', '—', 'Counter, rising'), ('40003–40004', '0x4148 0x0000', '12.5', 'Flow, m³/h'), ('40005–40006', '0x4120 0x0000', '10.0', 'Pressure, bar'),
  ('40011', '1', '—', 'Run bit'), ('40021', '742', '74.2 with ÷10', 'Level, %')]) + '<span class="qs">Read once to help you name tags in Frappe Factory. Guesses only; nothing is saved here.</span>')}
<div style="display:flex;justify-content:space-between;align-items:center"><span class="qs">2 selected. They appear in Frappe Factory → Devices and tags as suggestions, where tags are picked and named.</span><button type="button" class="btn solid">{ic("upload")}Send to Frappe Factory</button></div>'''
epage('EdgeScan.dc.html', 'Scan', 'Find devices on the plant networks', scan)

# ---------------- Logs and update
LC = 'grid-template-columns:96px 120px minmax(0,1fr)'
logs = [('08:46:11', bd('Info','gray'), 'uplink · batch 4,211 sent · 1,204 values'), ('08:41:02', bd('Warning','amber'), 'agent · PLC-2 · F9.COUNT stale for 3 polls'),
        ('08:14:00', bd('Info','gray'), 'local alarms · AT-401 lead trip · stack light on'), ('07:58:30', bd('Info','gray'), 'config · v41 applied · 132 tags · 18 alarm definitions'),
        ('07:40:08', bd('Info','gray'), 'agent · power source changed grid → generator · ATS-1 · 8 s gap'), ('06:02:15', bd('Info','gray'), 'agent · power source changed generator → grid · ATS-1 · 6 s gap'),
        ('05:32:10', bd('Info','gray'), 'agent · F9 put in maintenance · MNT-0088 · polling slowed to 10 s'), ('05:16:02', bd('Info','gray'), 'uplink · reconnected · 288 buffered messages sent in order'),
        ('05:12:44', bd('Error','red'), 'uplink · broker unreachable 4 min · messages buffered'), ('03:00:00', bd('Info','gray'), 'timescaledb · compression job · 7-day-old chunks · 4.1 GB → 0.4 GB'),
        ('02:14:51', bd('Warning','amber'), 'agent · DSE-7320 · 3 timeouts in a row, then OK'), ('00:00:05', bd('Info','gray'), 'clock · chrony in sync · offset 3 ms')]
logsb = f'''<div style="display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:12px;align-items:start">
{card('Recent events', '<div style="display:flex;gap:8px"><span class="chip"><span class="k">Service</span>All</span><span class="chip"><span class="k">Level</span>All</span></div>' + tbl(LC, ['Time', 'Level', 'Event'], logs), btn('Download logs','download','ghost'))}
<div style="display:flex;flex-direction:column;gap:12px">
{card('Update', kv([("Installed", "OpsEdge 0.4.2", ""), ("Available", "0.4.3 · signed by I-Varse", bd("New","blue")), ("Rule", "Installs only when the buffer is empty", "")]) + f'<div style="display:flex;gap:8px">{btn("Install 0.4.3", kind="solid")}{btn("Release notes", kind="ghost")}</div><span class="qs">Keeps 0.4.2 and rolls back by itself if a service does not start.</span>')}
{card('Services', f'<div style="display:flex;gap:8px;flex-wrap:wrap">{btn("Restart agent","refresh")}{btn("Restart uplink","refresh")}{btn("Reboot box", kind="ghost")}</div><span class="qs">Restarting the agent pauses readings for about 5 s. PLC interlocks are not affected.</span>')}
</div></div>'''
epage('EdgeLogs.dc.html', 'Logs and update', 'Last 24 h', logsb)
