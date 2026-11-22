from ff import *

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Devices and tags',None)),
  f'{btn("Import tags","upload","ghost")}<button type="button" class="btn solid">{ic("plus")}Add device</button>')

devs = [
  ('OpsEdge K1', 'Edge agent · v0.4.2', 'server', ('Online','green','g'), '2 s', False),
  ('PLC-1', 'Treatment and filling · Modbus TCP', 'cpu', ('Online','green','g'), '2 s', True),
  ('AT-401 analyser', 'Diagnostics · Modbus RTU', 'flask', ('Online','green','g'), '3 s', False),
  ('Filler PLCs F1 – F10', 'MQTT · Sparkplug B', 'radio', ('Online','green','g'), '1 s', False),
  ('Gen-1 controller', 'Generator · Modbus RTU', 'zap', ('Online','green','g'), '5 s', False),
  ('EM-1 energy meter', 'Incomer · Modbus TCP', 'gauge', ('No data 2 h','amber','a'), '2 h', False),
]
dl = ''
for n, d, i, (st, sc, dot), seen, act in devs:
    dl += f'''<div class="lr{" act" if act else ""}" style="grid-template-columns:28px minmax(0,1fr) auto;min-height:56px;margin:0"><span style="width:28px;height:28px;border-radius:8px;background:var(--surface-gray-2);display:grid;place-items:center;color:var(--ink-gray-6)">{ic(i)}</span><span class="c"><div class="t1">{n}</div><div class="m">{d}</div></span><span style="display:flex;flex-direction:column;align-items:flex-end;gap:4px"><span class="dot {dot}"></span><span class="qs tab" style="font-size:12px">{seen}</span></span></div>'''
devlist = f'''<div style="flex:0 0 19rem;width:19rem;border-right:1px solid var(--outline-gray-1);display:flex;flex-direction:column;min-height:0">
<div style="padding:12px;display:flex;gap:8px"><span class="in muted" style="flex:1">{ic("search")}<span class="grow">Search devices</span></span></div>
<div style="display:flex;flex-direction:column">{dl}</div>
<p class="qs" style="padding:12px;margin:0">6 devices · 132 tags · read by OpsEdge K1 and sent to the cloud every 2 s</p></div>'''

TC = 'grid-template-columns:minmax(0,1.3fr) 150px 64px 92px 72px 104px 72px 28px'
tags = [
  ('AT-401.LEAD', 'Lead at SP-1', 'IR 30001 · 4–20 mA', 'µg/L', '2 s', '0.05', '1.6', 'Good', 'IL-01'),
  ('AT-301.PH', 'pH after remineralization', 'HR 40103 · F32', '', '2 s', '0.02', '8.0', 'Good', 'IL-02'),
  ('AT-302.COND', 'Conductivity', 'HR 40105 · F32', 'µS/cm', '2 s', '1', '190', 'Good', 'IL-03'),
  ('AT-303.TURB', 'Turbidity', 'HR 40107 · F32', 'NTU', '2 s', '0.01', '0.21', 'Good', 'IL-04'),
  ('UV-301.INT', 'UV intensity', 'IR 30011 · U16 ÷10', '%', '5 s', '0.5', '96.0', 'Good', 'IL-05'),
  ('LT-401.LVL', 'T4 level', 'HR 40121 · F32', 'm³', '2 s', '0.01', '0.02', 'Good', ''),
  ('XV-301.ZS', 'Diverter position', 'DI 10017 · bool', '', '1 s', '—', 'T5', 'Good', ''),
  ('P-401.RUN', 'Fill pump running', 'Coil 00033 · bool', '', '1 s', '—', 'Off', 'Good', ''),
  ('P-401.HZ', 'Fill pump speed', 'HR 40141 · U16 ÷10', 'Hz', '2 s', '0.5', '0.0', 'Good', ''),
  ('IL-01.PERM', 'Filler run permissive', 'Coil 00001 · bool', '', '1 s', '—', '0', 'Good', ''),
  ('DP-102.DP', 'Carbon filter ΔP', 'HR 40109 · F32', 'bar', '5 s', '0.02', '1.3', 'Good', ''),
  ('KS-401.RST', 'Panel key switch', 'DI 10021 · bool', '', '1 s', '—', '0', 'Good', ''),
]
tr = ''
for t, d, addr, u, poll, db, val, q, il in tags:
    ilb = f' {bd(il,"o-gray","", "sm")}' if il else ''
    tr += f'''<div class="lr" style="{TC};min-height:52px"><span class="c"><div class="t1" style="display:flex;align-items:center;gap:6px"><span class="tab">{t}</span>{ilb}</div><div class="m">{d}</div></span><span class="tab qs" style="color:var(--ink-gray-7)">{addr}</span><span class="qs">{u or "—"}</span><span class="tab qs" style="color:var(--ink-gray-7)">{poll} · {('±'+db) if db!='—' else 'change'}</span><span class="r tab" style="display:flex;color:var(--ink-gray-9);font-weight:500">{val}</span><span style="display:flex;align-items:center;gap:6px;font-size:13px;color:var(--ink-gray-7)"><span class="dot g"></span>{q}</span><span style="display:flex;color:var(--ink-gray-4)" title="Read only">{ic("lock","i s35")}</span><span style="color:var(--ink-gray-4);display:flex">{ic("more","i s35")}</span></div>'''

detail = f'''<div style="flex:1;min-width:0;display:flex;flex-direction:column;overflow:auto">
<div style="padding:16px 20px 0;display:flex;align-items:flex-start;justify-content:space-between;gap:12px">
<div style="display:flex;gap:12px;align-items:center"><span style="width:40px;height:40px;border-radius:10px;background:var(--surface-gray-2);display:grid;place-items:center;color:var(--ink-gray-7)">{ic("cpu")}</span>
<div style="display:flex;flex-direction:column;gap:4px"><div style="display:flex;align-items:center;gap:8px"><h2 class="h2" style="font-size:18px">PLC-1</h2>{bd("Online","green","g")}</div><span class="qs">Treatment and filling PLC · Modbus TCP · 192.168.10.20:502 · unit 1</span></div></div>
<div style="display:flex;gap:8px">{btn("Test connection","refresh")}{btn("Add tag","plus")}{btn(icon="more",attrs="More")}</div></div>
<div class="tabs" style="margin-top:12px"><span class="t on">Tags <span class="bd gray">48</span></span><span class="t">Connection</span><span class="t">Health</span><span class="t">Changes</span></div>
<div class="body" style="gap:14px;padding-top:14px">
<div class="alert" style="background:var(--surface-gray-1);border-color:var(--outline-gray-1)"><span style="color:var(--ink-gray-6)">{ic("lock")}</span><div style="display:flex;flex-direction:column;gap:2px;font-size:13px;line-height:1.5;color:var(--ink-gray-7)"><span class="ttl" style="font-size:14px">Read only</span>Commands are off for Koyo 1. A tag can be written only when it is marked writable here, commands are on in Plant settings, and the edge agent allows writes.</div></div>
<div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><div style="display:flex;gap:8px"><span class="in muted" style="width:220px">{ic("search")}<span class="grow">Search 48 tags</span></span><span class="chip"><span class="k">Interlocked</span>Any</span><span class="chip"><span class="k">Quality</span>Any</span></div><span class="qs">Values live · 2 s</span></div>
<div class="list"><div class="lh" style="{TC}"><span>Tag</span><span>Address</span><span>Unit</span><span>Poll · deadband</span><span class="r" style="display:flex">Value</span><span>Quality</span><span>Write</span><span></span></div>{tr}</div>
<p class="qs" style="margin:0">F32 is a 32-bit float, word order high-low. Deadband is the smallest change that is stored; the interlock tags still stream every poll to the edge.</p>
</div></div>'''

write('Devices.dc.html', page('Devices and tags', shell('Devices.dc.html', head, f'<div style="display:flex;flex:1;min-height:0">{devlist}{detail}</div>'), {"$preview": {"width": 1440, "height": 900}}))
