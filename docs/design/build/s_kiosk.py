"""Floor kiosk shell: a tablet fixed at the filling line. No sidebar by design (one task per screen,
signed in with the user's own Frappe login; access comes from the Kiosk Profile, like POS Profile); same frappe-ui tokens at the touch sizes (lg controls, 40-56px targets)."""
from ff import *
import symbols as S

W_, H_ = 1180, 820
KCSS = """
.kb{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:48px;padding:0 16px;border:0;border-radius:10px;font:500 16px Inter,sans-serif;cursor:pointer;background:var(--surface-gray-2);color:var(--ink-gray-8)}
.kb.solid{background:var(--surface-gray-10);color:var(--ink-base)}
a.kb{text-decoration:none}
.ff a.kb{color:var(--ink-gray-8)}
.ff a.kb.solid{color:var(--ink-base)}
.kb[disabled]{opacity:.5;cursor:not-allowed}
.kb svg.i{width:20px;height:20px;flex-basis:20px}
.key{height:64px;border-radius:12px;border:1px solid var(--outline-gray-2);background:var(--surface-base);font:500 24px Inter,sans-serif;color:var(--ink-gray-9);display:grid;place-items:center}
"""

def topbar(user=None, kiosk=('K1', 'Filling hall · F1 – F5', 'Koyo 1 · tablet T-02 · session KS-0221')):
    u = (f'<div style="display:flex;align-items:center;gap:10px"><span class="av md" style="width:36px;height:36px;flex:0 0 36px;font-size:13px">{user[0]}</span><span style="display:flex;flex-direction:column"><span style="font-size:15px;font-weight:500;color:var(--ink-gray-9)">{user[1]}</span><span class="qs">{user[2]}</span></span><a href="KioskLogin.dc.html" class="kb" style="height:48px;font-size:15px;margin-left:8px">{ic("arrow-r")}Log out</a></div>'
         if user else '<span class="qs" style="font-size:14px">Nobody logged in</span>')
    return f'''<header style="height:64px;flex:0 0 64px;display:flex;align-items:center;justify-content:space-between;padding:0 24px;border-bottom:1px solid var(--outline-gray-1)">
<div style="display:flex;align-items:center;gap:12px"><span class="logo" style="width:36px;height:36px;flex-basis:36px">{kiosk[0]}</span><span style="display:flex;flex-direction:column"><span style="font-size:16px;font-weight:600;color:var(--ink-gray-9)">{kiosk[1]}</span><span class="qs">{kiosk[2]}</span></span></div>
<div style="display:flex;align-items:center;gap:20px">{topbar_right()}{u}</div></header>'''

def topbar_right():
    return '<span class="tab" style="font-size:20px;font-weight:600;color:var(--ink-gray-9)">08:46</span><span class="bd gray" style="height:24px;font-size:13px"><span class="dot g"></span>Online</span>'

def kpage(name, body, overlay=''):
    ov = (closer('kd') + f'<div class="ff ffov" style="position:absolute;inset:0;display:block;min-height:0;background:transparent;font-size:16px"><label for="kd" class="overlay" aria-label="Close"></label>{overlay}</div>') if overlay else ''
    return page(name, f'<div style="position:relative;height:100vh"><div class="ff" style="flex-direction:column;font-size:16px">{body}</div>{ov}</div>', {"$preview": {"width": W_, "height": H_}}, helmet_extra=KCSS)

# ---------------- Sign in: the Frappe login. The Kiosk Profile assigned to the user opens next, as POS Profile does.
login = f'''{topbar()}
<div style="flex:1;display:grid;place-items:center;background:var(--surface-gray-1);min-height:0">
<div style="width:440px;background:var(--surface-base);border-radius:16px;box-shadow:var(--shadow-lg);padding:32px;display:flex;flex-direction:column;gap:18px">
<div style="display:flex;flex-direction:column;gap:6px;align-items:center;text-align:center"><span class="logo" style="width:44px;height:44px;flex-basis:44px;font-size:16px">FF</span><h1 style="margin:8px 0 0;font-size:24px;font-weight:600;color:var(--ink-gray-9)">Log in to Frappe Factory</h1><p class="ps" style="font-size:15px">Use your own Frappe login. The kiosk assigned to you opens next.</p></div>
<label class="fl"><span class="lab" style="font-size:15px">Email</span><span class="in lg focus" style="height:48px;font-size:16px"><span class="grow">kemi.e@koyo1.ng</span></span></label>
<label class="fl"><span class="lab" style="font-size:15px">Password</span><span class="in lg" style="height:48px;font-size:16px"><span class="grow">••••••••••</span>{ic("eye","i s35") if "eye" in IC else ""}</span></label>
<a href="KioskLine.dc.html" class="kb solid" style="width:100%">Log in</a>
<div style="display:flex;flex-direction:column;gap:8px;padding:12px 14px;border-radius:12px;background:var(--surface-gray-1);font-size:14px;line-height:1.5;color:var(--ink-gray-7)">
<div style="display:flex;gap:10px"><span style="color:var(--ink-gray-6);display:flex;margin-top:2px">{ic("info","i s35")}</span><span>This tablet runs the Filling hall T-02 kiosk. Only users assigned to that Kiosk Profile can open it. Everything you record is saved under your Frappe user and this shift.</span></div>
<div style="display:flex;gap:10px"><span style="color:var(--ink-gray-6);display:flex;margin-top:2px">{ic("clock","i s35")}</span><span>Logs out after 10 min without a tap.</span></div></div>
<span class="qs" style="font-size:13px;text-align:center">Not assigned? A Factory Manager adds you in App settings → Kiosks.</span>
</div></div>'''
write('KioskLogin.dc.html', kpage('Kiosk sign in', login))

# ---------------- Line view during the trip, with a stop that needs a reason
def ftile(n, rate, count, state):
    col = {'Stopped': ('var(--outline-red-3)', 'red', 'Stopped · trip'), 'Maint': ('var(--outline-gray-2)', 'violet', 'Maintenance')}[state]
    run = False
    return f'''<div style="display:flex;flex-direction:column;align-items:center;gap:8px;padding:16px 10px;border-radius:14px;border:1px solid {col[0]};background:var(--surface-base)">
<div style="display:flex;width:100%;justify-content:space-between;align-items:center"><span style="font-size:18px;font-weight:600;color:var(--ink-gray-9)">{n}</span>{bd(col[2], col[1])}</div>
<svg viewBox="0 0 48 48" width="72" height="72" aria-hidden="true">{S.filler(run)}</svg>
<div style="display:flex;width:100%;justify-content:space-between" class="tab"><span class="qs" style="font-size:14px">Sachets</span><span style="font-size:16px;font-weight:600;color:var(--ink-gray-9)">{count}</span></div>
<div style="display:flex;width:100%;justify-content:space-between" class="tab"><span class="qs" style="font-size:14px">Rate</span><span style="font-size:16px;color:var(--ink-gray-7)">{rate}</span></div></div>'''
tiles = ''.join([ftile('F1', '0 /h', '3,890', 'Stopped'), ftile('F2', '0 /h', '3,850', 'Stopped'), ftile('F3', '0 /h', '3,920', 'Stopped'), ftile('F4', '0 /h', '3,780', 'Stopped'), ftile('F5', '0 /h', '3,880', 'Stopped')])
reasons = ['Power dip', 'Generator changeover', 'Jaw jam', 'Film change or splice', 'Seal temperature low', 'Waiting for water', 'No film', 'Other']
rb = ''.join(f'<button type="button" class="kb" style="height:56px;justify-content:flex-start;{"background:var(--surface-gray-10);color:var(--ink-base)" if r=="Power dip" else ""}">{r}</button>' for r in reasons)
line = f'''{topbar(('KE', 'Kemi E.', 'Operator · F1 – F5'))}
<div style="flex:1;overflow:auto;padding:20px 24px 24px;display:flex;flex-direction:column;gap:18px">
<div style="display:flex;align-items:center;gap:14px;padding:14px 18px;border-radius:14px;background:var(--surface-red-2);border:1px solid var(--outline-red-3)"><span style="color:var(--ink-red-7);display:flex">{ic("octagon","i")}</span><div style="flex:1"><div style="font-size:17px;font-weight:600;color:var(--ink-gray-9)">Line stopped by the lead interlock at 08:14</div><div style="font-size:15px;color:var(--ink-gray-7)">Do not restart. The supervisor is running the recovery steps.</div></div><span class="tab" style="font-size:22px;font-weight:600;color:var(--ink-red-7)">32 min</span></div>
<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px">{tiles}</div>
<section style="display:flex;flex-direction:column;gap:12px;padding:18px;border-radius:14px;border:1px solid var(--outline-amber-3);background:var(--surface-base)">
<div style="display:flex;justify-content:space-between;align-items:baseline"><div><div style="font-size:18px;font-weight:600;color:var(--ink-gray-9)">Why did all fillers stop at 07:40?</div><div class="qs" style="font-size:14px">3 min · picked up by the PLC · 1 of 2 stops on your fillers without a reason</div></div><span class="qs" style="font-size:14px">Tap one</span></div>
<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px">{rb}</div>
<div style="display:flex;justify-content:flex-end;gap:10px"><button type="button" class="kb">Skip for now</button><button type="button" class="kb solid">Save reason</button></div></section>
<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">
<a href="KioskRejects.dc.html" class="kb" style="height:64px">{ic("x")}Log rejects</a><a href="KioskSample.dc.html" class="kb" style="height:64px">{ic("flask")}Record a sample</a><a href="KioskFault.dc.html" class="kb" style="height:64px">{ic("wrench")}Report a fault</a><button type="button" class="kb" style="height:64px">{ic("phone")}Call supervisor</button></div>
</div>'''
write('KioskLine.dc.html', kpage('Kiosk line', line))

# ---------------- Open kiosk session (like ERPNext POS Opening Entry)
opts = [('Filling hall T-02', 'Line view · Koyo 1 · F1 – F5 · this tablet', True, 'KioskLogin.dc.html'), ('Filling hall T-03', 'Line view · Koyo 1 · F6 – F10', False, 'KioskLogin.dc.html'),
        ('Maintenance T-05', 'Maintenance view · Koyo 1 · all equipment', False, 'KioskMaint.dc.html'), ('Quality lab T-06', 'Quality view · Koyo 1 · analysers and holds', False, 'KioskQA.dc.html')]
ol = ''.join(f'<a href="{h}" style="text-decoration:none;display:grid;grid-template-columns:20px minmax(0,1fr);gap:12px;padding:14px;border-radius:12px;border:1px solid {"var(--ink-gray-9)" if on else "var(--outline-gray-2)"};cursor:pointer"><span class="rd{" on" if on else ""}" style="width:20px;height:20px;flex-basis:20px;margin-top:1px"></span><span style="display:flex;flex-direction:column;gap:2px"><span style="font-size:16px;font-weight:500;color:var(--ink-gray-9)">{n}</span><span class="qs" style="font-size:14px">{m}</span></span></a>' for n, m, on, h in opts)
openk = f"""<div style="position:relative;flex:1;background:var(--surface-gray-1)">
<div style="position:absolute;inset:0;display:grid;place-items:center">
<div class="dialog" role="dialog" aria-labelledby="ok-t" style="position:relative;width:560px;display:flex;flex-direction:column">
<div style="padding:24px 28px 0;display:flex;flex-direction:column;gap:6px"><h1 id="ok-t" style="margin:0;font-size:22px;font-weight:600;color:var(--ink-gray-9)">Open kiosk</h1><p class="ps" style="font-size:15px">Musa A. · musa.a@koyo1.ng · Floor Supervisor. Logged in with his Frappe user. Only kiosks he is assigned to are listed.</p></div>
<div style="padding:20px 28px;display:flex;flex-direction:column;gap:18px">
<div style="display:flex;flex-direction:column;gap:8px"><span style="font-size:14px;color:var(--ink-gray-6)">Kiosk</span>{ol}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">{field('Shift', sel('Morning · 06:00 – 14:00', 'out'))}{field('Production run', sel('RUN-0412 · from WO-0412', 'out'), hint='From ERPNext. Hidden when ERPNext is not linked.')}</div>
<div style="display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:10px;background:var(--surface-green-2);font-size:14px"><span style="color:var(--ink-green-7);display:flex">{ic("check")}</span><span style="color:var(--ink-gray-8)">This tablet is registered as T-02 for Filling hall T-02.</span></div>
</div>
<div style="padding:16px 28px 24px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--outline-gray-1)"><span class="qs" style="font-size:13px;max-width:280px">Opens full screen. Leaving full screen needs a Floor Supervisor to log in. Closing writes every log-in to the shift.</span><span style="display:flex;gap:10px"><a href="Dashboard.dc.html" class="kb">Cancel</a><a href="KioskLogin.dc.html" class="kb solid">Open kiosk</a></span></div>
</div></div></div>"""
write('KioskOpen.dc.html', kpage('Open kiosk', openk))

# ---------------- Shared bits for the department views
def card(title, sub, inner, extra='', border='var(--outline-gray-2)'):
    return f'''<section style="display:flex;flex-direction:column;gap:12px;padding:16px 18px;border-radius:14px;border:1px solid {border};background:var(--surface-base);min-width:0">
<div style="display:flex;justify-content:space-between;align-items:baseline;gap:8px"><div><div style="font-size:17px;font-weight:600;color:var(--ink-gray-9)">{title}</div>{f'<div class="qs" style="font-size:13px">{sub}</div>' if sub else ''}</div>{extra}</div>{inner}</section>'''

def etile(sym, tag, name, state, val, note):
    tone = {'Running': ('gray', 'var(--outline-gray-2)'), 'Alarm': ('amber', 'var(--outline-amber-3)'), 'Low stock': ('amber', 'var(--outline-amber-3)'), 'Maintenance': ('violet', 'var(--outline-gray-2)'), 'Stopped': ('red', 'var(--outline-red-3)')}[state]
    return f'''<div style="display:grid;grid-template-columns:52px minmax(0,1fr);gap:10px;padding:12px;border-radius:12px;border:1px solid {tone[1]};background:var(--surface-base);align-items:center">
<svg viewBox="0 0 48 48" width="52" height="52" aria-hidden="true">{sym}</svg>
<div style="display:flex;flex-direction:column;gap:3px;min-width:0"><div style="display:flex;justify-content:space-between;align-items:center;gap:6px"><span style="font-size:15px;font-weight:600;color:var(--ink-gray-9)">{tag}</span>{bd(state, tone[0])}</div>
<span class="qs" style="font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{name}</span><span class="tab" style="font-size:14px;color:var(--ink-gray-8)">{val} <span class="qs" style="font-size:12px">{note}</span></span></div></div>'''

def actions(*bs):
    return f'<div style="display:grid;grid-template-columns:repeat({len(bs)},minmax(0,1fr));gap:12px">' + ''.join(bs) + '</div>'

# ---------------- Maintenance view
eq = ''.join([
  etile(S.pump(True), 'P-101', 'Borehole pump', 'Running', '10.9 m³/h', 'feed'),
  etile(S.mmf(), 'CF-102', 'Carbon filter', 'Alarm', 'ΔP 1.3 bar', 'backwash at 1.2'),
  etile(S.ro(), 'RO-201', 'Reverse osmosis', 'Running', '6.0 m³/h', 'permeate · 55%'),
  etile(S.uv(), 'UV-301', 'UV steriliser', 'Running', '96%', 'lamp 6,920 h'),
  etile(S.dosing(), 'DP-1', 'Antiscalant dosing', 'Low stock', '38 L', 'lasts 22 h'),
  etile(S.generator(), 'G-1', 'Generator 60 kVA', 'Running', '41 h', 'diesel left'),
  etile(S.filler(False), 'F9', 'Sachet filler', 'Maintenance', 'MNT-0088', '3 h 14 min'),
  etile(S.ix(), 'IX-501', 'Resin, quarantine loop', 'Running', 'T5 2.3 m³', 'resin 12%'),
])
def job(ref, title, meta, st, sc, btns):
    return f'''<div style="display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center;padding:12px 0;border-top:1px solid var(--outline-gray-1)">
<div style="display:flex;flex-direction:column;gap:3px;min-width:0"><div style="display:flex;gap:8px;align-items:center"><span class="tab qs" style="font-size:13px">{ref}</span>{bd(st, sc)}</div><span style="font-size:16px;font-weight:500;color:var(--ink-gray-9)">{title}</span><span class="qs" style="font-size:13px">{meta}</span></div>
<div style="display:flex;gap:8px">{btns}</div></div>'''
jobs = ''.join([
  job('MNT-0088', 'F9 · replace jaw heater, test 40 sachets', 'Planned · logged by Musa A. 05:32 · heater from MR-0195', 'In progress', 'blue', '<button type="button" class="kb" style="height:48px;font-size:15px">Add note</button><button type="button" class="kb solid" style="height:48px;font-size:15px">Finish and test</button>'),
  job('MNT-0090', 'CF-102 · backwash the carbon filter', 'From the shift handover · due 16:00 · ΔP above 1.2 bar since 07:52', 'Open', 'gray', '<button type="button" class="kb" style="height:48px;font-size:15px">Start job</button>'),
  job('MNT-0091', 'DP-1 · refill antiscalant from MR-0193', 'Due 15:00 · storekeeper is bringing 2 drums of 25 L', 'Waiting for parts', 'amber', '<button type="button" class="kb" style="height:44px;font-size:15px">Start job</button>'),
])
def kal(p, col, title, meta, btn_):
    return f'<div style="display:grid;grid-template-columns:24px minmax(0,1fr) auto;gap:10px;align-items:center;padding:10px 0;border-top:1px solid var(--outline-gray-1)"><span style="width:22px;height:22px;border-radius:6px;background:{col};color:{'#fff' if col == RED else 'oklch(0.21 0 0)'};font-size:12px;font-weight:600;display:grid;place-items:center">{p}</span><span style="display:flex;flex-direction:column;gap:2px;min-width:0"><span style="font-size:15px;font-weight:500;color:var(--ink-gray-9)">{title}</span><span class="qs" style="font-size:13px">{meta}</span></span>{btn_}</div>'
AMB, RED = 'oklch(0.723 0.152 71.82)', 'oklch(0.556 0.198 26.552)'
mal = ''.join([
  kal('3', AMB, 'DP-102 carbon filter ΔP high', '1.3 bar · since 07:52 · not acknowledged', '<button type="button" class="kb" style="height:48px;font-size:15px">Acknowledge</button>'),
  kal('3', AMB, 'Diesel runway under 48 h', '41 h left · acknowledged by Musa A.', ''),
  kal('3', AMB, 'F9 jaw temperature low', 'Shelved by Musa A. while MNT-0088 is open', bd('Shelved', 'gray')),
])
maint = f'''{topbar(('IK', 'Ibrahim K.', 'Maintenance Technician'), ('K1', 'Maintenance · Koyo 1', 'Koyo 1 · tablet T-05 · session KS-0224'))}
<div style="flex:1;overflow:auto;padding:18px 24px 24px;display:flex;flex-direction:column;gap:16px">
<div style="display:flex;align-items:center;gap:14px;padding:12px 16px;border-radius:14px;background:var(--surface-red-2);border:1px solid var(--outline-red-3)"><span style="color:var(--ink-red-7);display:flex">{ic("octagon","i")}</span><div style="flex:1"><div style="font-size:16px;font-weight:600;color:var(--ink-gray-9)">Filling stopped by the lead interlock at 08:14 · TRIP-0007</div><div style="font-size:14px;color:var(--ink-gray-7)">No maintenance step is open on this trip. Do not touch key KS-401: the Floor Supervisor resets it after QA release.</div></div><span class="tab" style="font-size:20px;font-weight:600;color:var(--ink-red-7)">32 min</span></div>
<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px">{eq}</div>
<div style="display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:14px">
{card('My jobs', '3 open · assigned to Ibrahim K.', jobs)}
{card('Equipment alarms', 'Only alarms on equipment this kiosk covers', mal)}
</div>
</div>
<div style="flex:0 0 auto;padding:12px 24px 16px;border-top:1px solid var(--outline-gray-1);display:flex;flex-direction:column;gap:8px;background:var(--surface-base)">{actions(f'<a href="KioskFault.dc.html" class="kb" style="height:60px">{ic("wrench")}Report a fault</a>', f'<a href="KioskSpare.dc.html" class="kb" style="height:60px">{ic("package")}Request a spare part</a>', f'<button type="button" class="kb" style="height:60px">{ic("phone")}Call supervisor</button>')}
</div>'''
write('KioskMaint.dc.html', kpage('Kiosk maintenance', maint))

# ---------------- Quality view
qa_tiles = ''.join([
  etile(S.analyser('AT'), 'AT-401', 'Lead after UV', 'Running', '2.0 µg/L', 'under 3 for 8 of 10 min'),
  etile(S.analyser('AT'), 'AT-302', 'Conductivity', 'Running', '186 µS/cm', 'band 150 – 220'),
  etile(S.analyser('AT'), 'AT-303', 'Turbidity', 'Running', '0.21 NTU', 'trip at 4'),
  etile(S.uv(), 'UV-301', 'UV intensity', 'Running', '96%', 'trip below 70'),
])
def lot(ref, qty, sub, test, tc, act):
    return f'<div style="display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:center;padding:11px 0;border-top:1px solid var(--outline-gray-1)"><span style="display:flex;flex-direction:column;gap:3px;min-width:0"><span style="display:flex;gap:8px;align-items:center"><span style="font-size:15px;font-weight:600;color:var(--ink-gray-9)">{ref}</span><span class="tab" style="font-size:15px;color:var(--ink-gray-8)">{qty}</span></span><span class="qs tab" style="font-size:13px">{sub}</span><span>{bd(test, tc)}</span></span>{act}</div>'
lots = ''.join([
  lot('L1', '100 bags', '2,000 sachets · 07:56 – 08:03', '2 of 3 pass · S-4 at the outside lab', 'gray', '<button type="button" class="kb" style="height:44px;font-size:15px" disabled>Decide</button>'),
  lot('L2', '156 bags + 14 sachets', '3,134 sachets · 08:03 – 08:14', 'S-3 failed · 6.8 µg/L', 'red', '<a href="KioskDecide.dc.html" class="kb" style="height:48px;font-size:15px">Decide</a>'),
  lot('L3', '2.3 m³ in T5', 'Not yet filled · template says reprocess', 'Reprocess via IX-501', 'gray', '<a href="KioskDecide.dc.html" class="kb" style="height:48px;font-size:15px">Decide</a>'),
])
def chk(name, rule, last, nxt, due=False):
    return f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 76px;gap:10px;align-items:center;padding:10px 0;border-top:1px solid var(--outline-gray-1)"><span style="display:flex;flex-direction:column;gap:2px;min-width:0"><span style="font-size:15px;font-weight:500;color:var(--ink-gray-9)">{name}</span><span class="qs" style="font-size:13px">{rule} · last {last}</span></span><span class="tab" style="text-align:right;font-size:15px;font-weight:600;color:{"var(--ink-amber-8)" if due else "var(--ink-gray-8)"}">{nxt}</span></div>'
checks = ''.join([
  chk('Lead at SP-1', 'Every 2 h · ASV meter · under 5 µg/L', '07:55 pass 2.2', 'Paused'),
  chk('Fill volume', '10 sachets per filler · 50 cl ± 2%', '07:30 pass', '09:30'),
  chk('Seal and leak', '10 sachets per filler · squeeze test', '06:30 pass', '10:30'),
  chk('Coliform plate', 'Daily · 2 sachets to the lab', 'yesterday pass', '11:00'),
])
qa = f'''{topbar(('GO', 'Grace O.', 'Quality Inspector'), ('K1', 'Quality lab · Koyo 1', 'Koyo 1 · tablet T-06 · session KS-0225'))}
<div style="flex:1;overflow:auto;padding:18px 24px 24px;display:flex;flex-direction:column;gap:16px">
<div style="display:flex;align-items:center;gap:14px;padding:12px 16px;border-radius:14px;background:var(--surface-red-2);border:1px solid var(--outline-red-3)"><span style="color:var(--ink-red-7);display:flex">{ic("flask","i")}</span><div style="flex:1"><div style="font-size:16px;font-weight:600;color:var(--ink-gray-9)">TRIP-0007 is waiting for you: sample 2 is due now</div><div style="font-size:14px;color:var(--ink-gray-7)">Sample 1 at 08:36 read 2.1 µg/L. Take sample 2 at SP-1, at least 10 min later. The line stays stopped until you release it.</div></div><a href="KioskSample.dc.html" class="kb solid" style="height:48px">Record sample 2</a></div>
<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px">{qa_tiles}</div>
<div style="display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:14px">
{card('QH-0031 · held product', '256 bags, 14 loose sachets and 2.3 m³ · opened by TRIP-0007', lots, '<a href="QualityHold.dc.html" style="font-size:14px">Open hold</a>', 'var(--outline-amber-3)')}
{card('Routine checks', 'From the plant quality plan · lead check paused during the trip', checks)}
</div>
</div>
<div style="flex:0 0 auto;padding:12px 24px 16px;border-top:1px solid var(--outline-gray-1);display:flex;flex-direction:column;gap:8px;background:var(--surface-base)">{actions(f'<a href="KioskSample.dc.html" class="kb" style="height:60px">{ic("flask")}Record a sample</a>', f'<button type="button" class="kb" style="height:60px" disabled>{ic("lock")}QA release · needs sample 2</button>', f'<button type="button" class="kb" style="height:60px">{ic("phone")}Call supervisor</button>')}
<span class="qs" style="font-size:13px;text-align:center">Every result and decision is saved under your Frappe user.</span>
</div>'''
write('KioskQA.dc.html', kpage('Kiosk quality', qa))

# ================= Kiosk action dialogs (each over its view; every save is under the logged-in Frappe user)
def kdialog(title, sub, body, foot_note, primary, w=760, back='#', h=None):
    hh = f'height:{h}px;' if h else ''
    return f'''<div class="dialog" role="dialog" aria-label="{title}" style="left:50%;top:50%;transform:translate(-50%,-50%);width:{w}px;{hh}display:flex;flex-direction:column">
<div style="padding:22px 26px 0;display:flex;justify-content:space-between;align-items:flex-start;gap:16px"><div style="display:flex;flex-direction:column;gap:4px"><h1 style="margin:0;font-size:22px;font-weight:600;color:var(--ink-gray-9)">{title}</h1><p class="ps" style="font-size:15px">{sub}</p></div><a href="{back}" class="kb" style="width:44px;height:44px;padding:0" aria-label="Close">{ic("x")}</a></div>
<div style="padding:18px 26px;display:flex;flex-direction:column;gap:18px;flex:1;min-height:0;overflow:auto">{body}</div>
<div style="padding:14px 26px 20px;display:flex;justify-content:space-between;align-items:center;gap:16px;border-top:1px solid var(--outline-gray-1)"><span class="qs" style="font-size:13px;max-width:420px;line-height:1.45">{foot_note}</span><div style="display:flex;gap:10px"><a href="{back}" class="kb">Cancel</a>{primary}</div></div></div>'''

def klabel(t, extra=''):
    return f'<div style="display:flex;justify-content:space-between;align-items:baseline"><span style="font-size:15px;font-weight:500;color:var(--ink-gray-8)">{t}</span><span class="qs" style="font-size:13px">{extra}</span></div>'
def chips(items, on, cols=3, h=52):
    return f'<div style="display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:10px">' + ''.join(
        f'<button type="button" class="kb" style="height:{h}px;justify-content:flex-start;{"background:var(--surface-gray-10);color:var(--ink-base)" if i in on else ""}{";opacity:.45" if i.startswith("~") else ""}">{i.lstrip("~")}</button>' for i in items) + '</div>'
def numpad(value, unit, note=''):
    keys = ''.join(f'<span class="key" style="height:52px;font-size:20px">{k}</span>' for k in '123456789') + f'<span class="key" style="height:52px;font-size:20px">.</span><span class="key" style="height:52px;font-size:20px">0</span><span class="key" style="height:52px;color:var(--ink-gray-6)">{ic("arrow-l")}</span>'
    return f'''<div style="display:flex;flex-direction:column;gap:10px"><div style="height:64px;border-radius:12px;border:2px solid var(--ink-gray-9);display:flex;align-items:center;justify-content:flex-end;gap:8px;padding:0 16px"><span class="tab" style="font-size:30px;font-weight:600;color:var(--ink-gray-9)">{value}</span><span style="font-size:16px;color:var(--ink-gray-6)">{unit}</span></div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px">{keys}</div>{f'<span class="qs" style="font-size:13px">{note}</span>' if note else ''}</div>'''
def pin_confirm(ini, name, email, role):
    return f'''<div style="display:flex;align-items:center;gap:14px;padding:12px 16px;border-radius:12px;background:var(--surface-gray-1)"><span class="av" style="width:40px;height:40px;flex:0 0 40px;font-size:14px">{ini}</span>
<div style="flex:1;display:flex;flex-direction:column;gap:2px"><span style="font-size:15px;font-weight:500;color:var(--ink-gray-9)">Saved as {name}</span><span class="qs tab" style="font-size:13px">{email} · {role} · logged in on this kiosk</span></div></div>'''

# ---- Record a sample (Quality view)
samp = f'''<div style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:22px">
<div style="display:flex;flex-direction:column;gap:16px">
<div style="display:flex;flex-direction:column;gap:8px">{klabel('For', 'from the open trip')}{chips(['TRIP-0007 · sample 2', 'QH-0031 · lot L1', 'Routine check'], ['TRIP-0007 · sample 2'], 3, 48)}</div>
<div style="display:flex;flex-direction:column;gap:8px">{klabel('Sample point')}{chips(['SP-1 · after UV', 'SP-2 · T4 outlet', 'Filler F1 – F10'], ['SP-1 · after UV'], 3, 48)}</div>
<div style="display:flex;flex-direction:column;gap:8px">{klabel('Test and method')}{chips(['Lead · ASV meter', 'Lead · ICP-MS lab', 'Conductivity'], ['Lead · ASV meter'], 3, 48)}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:14px">
<div style="padding:12px 14px;border-radius:12px;background:var(--surface-gray-1);display:flex;flex-direction:column;gap:2px"><span class="qs" style="font-size:13px">Taken at</span><span class="tab" style="font-size:16px;color:var(--ink-gray-9)">08:47 · 11 min after sample 1</span></div>
<a class="kb" style="height:auto;padding:12px 14px;justify-content:flex-start">{ic("upload")}Photo of the meter</a></div>
{pin_confirm('GO', 'Grace O.', 'grace.o@koyo1.ng', 'Quality Inspector')}
</div>
<div style="display:flex;flex-direction:column;gap:10px">{klabel('Result')}{numpad('1.8', 'µg/L', 'Pass for release: under 3 µg/L.')}<div style="display:flex;align-items:center;gap:8px;padding:10px 12px;border-radius:10px;background:var(--surface-green-2)"><span style="color:var(--ink-green-7);display:flex">{ic("check")}</span><span style="font-size:15px;color:var(--ink-gray-9)">Under 3 · passes</span></div></div>
</div>'''
write('KioskSample.dc.html', kpage('Kiosk · record a sample', qa, kdialog('Record sample 2', 'TRIP-0007 · lead trip at 08:14 · sample 1 read 2.1 µg/L at 08:36', samp,
  'Saves Quality Sample S-6 on the trip. With ERPNext it also posts Quality Inspection QI-0932 (In Process, against Job Card JC-0412). After 2 passing results QA release opens.', '<a href="KioskQA.dc.html" class="kb solid">Save sample</a>', 960, 'KioskQA.dc.html')))

# ---- Log rejects (Line view)
rj = f'''<div style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:22px">
<div style="display:flex;flex-direction:column;gap:16px">
<div style="display:flex;flex-direction:column;gap:8px">{klabel('Filler', 'your fillers on this kiosk')}{chips(['F1', 'F2', 'F3', 'F4', 'F5'], ['F3'], 5, 52)}</div>
<div style="display:flex;flex-direction:column;gap:8px">{klabel('Why rejected')}{chips(['Seal leak', 'Under-fill', 'Over-fill', 'Film misprint', 'No date code', 'Other'], ['Seal leak'], 3, 52)}</div>
<div style="display:flex;flex-direction:column;gap:6px;padding:12px 14px;border-radius:12px;background:var(--surface-gray-1);font-size:14px;line-height:1.5;color:var(--ink-gray-7)"><span><b style="font-weight:500;color:var(--ink-gray-9)">Counted in sachets.</b> 24 sachets is 1 bag and 4 sachets. Rejects are taken off good output for this run.</span><span>F3 so far this run: 46 sachets rejected, 3,920 good.</span></div>
{pin_confirm('KE', 'Kemi E.', 'kemi.e@koyo1.ng', 'Machine Operator')}
</div>
<div style="display:flex;flex-direction:column;gap:10px">{klabel('How many')}{numpad('24', 'sachets', 'Whole sachets only.')}</div></div>'''
write('KioskRejects.dc.html', kpage('Kiosk · log rejects', line, kdialog('Log rejects', 'Filling hall T-02 · RUN-0412 · found while clearing the line after the trip', rj,
  'Adds 24 sachets to F3 rejects on RUN-0412. With ERPNext the run total posts as process loss on the Manufacture entry when the run ends.', '<a href="KioskLine.dc.html" class="kb solid">Save rejects</a>', 960, 'KioskLine.dc.html')))

# ---- Report a fault (Maintenance view)
eqs = ['P-101 · pump', 'CF-102 · carbon filter', 'RO-201', 'UV-301', 'DP-1 · dosing', 'G-1 · generator', 'F9 · filler', 'IX-501 · resin']
flt = f'''<div style="display:flex;flex-direction:column;gap:16px">
<div style="display:flex;flex-direction:column;gap:8px">{klabel('Which equipment')}{chips(eqs, ['CF-102 · carbon filter'], 4, 48)}</div>
<div style="display:flex;flex-direction:column;gap:8px">{klabel('What is wrong')}{chips(['Leak', 'Noise or vibration', 'Overheating', 'Pressure out of range', "Won't start", 'Other'], ['Pressure out of range'], 3, 48)}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div style="display:flex;flex-direction:column;gap:8px">{klabel('Is it still running?')}{chips(['Still running', 'Stopped'], ['Still running'], 2, 48)}</div>
<div style="display:flex;flex-direction:column;gap:8px">{klabel('Note')}<span class="in" style="height:48px;font-size:15px"><span class="grow">ΔP 1.3 bar, backwash valve stiff</span></span></div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px"><a class="kb" style="height:48px;justify-content:flex-start">{ic("upload")}Add a photo</a><span class="qs" style="font-size:13px;line-height:1.45;align-self:center">Linked alarm: DP-102 carbon filter ΔP high, 07:52. It is acknowledged when you save.</span></div>
{pin_confirm('IK', 'Ibrahim K.', 'ibrahim.k@koyo1.ng', 'Maintenance Technician')}
</div>'''
write('KioskFault.dc.html', kpage('Kiosk · report a fault', maint, kdialog('Report a fault', 'Maintenance · Koyo 1 · creates a maintenance job you can start now', flt,
  'Creates job MNT-0092 in the maintenance queue. "Stopped" also opens a Machine Stop. With ERPNext the job is mirrored to a Maintenance Visit on the asset.', '<a href="KioskMaint.dc.html" class="kb solid">Report fault</a>', 900, 'KioskMaint.dc.html')))

# ---- Request a spare part (Maintenance view)
def part(code, name, qty, stock, ok):
    return f'''<div style="display:grid;grid-template-columns:minmax(0,1fr) 150px 120px 44px;gap:12px;align-items:center;padding:12px 0;border-top:1px solid var(--outline-gray-1)">
<span style="display:flex;flex-direction:column;gap:2px"><span style="font-size:16px;font-weight:500;color:var(--ink-gray-9)">{name}</span><span class="qs tab" style="font-size:13px">{code}</span></span>
<span style="display:flex;align-items:center;gap:6px"><span class="key" style="width:48px;height:48px;font-size:20px">−</span><span class="tab" style="width:36px;text-align:center;font-size:18px;font-weight:600">{qty}</span><span class="key" style="width:48px;height:48px;font-size:20px">+</span></span>
<span>{bd(stock, "green" if ok else "amber")}</span><span style="color:var(--ink-gray-6);display:flex">{ic("x")}</span></div>'''
spr = f'''<div style="display:flex;flex-direction:column;gap:16px">
<div style="display:flex;flex-direction:column;gap:8px">{klabel('For job')}{chips(['MNT-0088 · F9 jaw heater', 'MNT-0090 · CF-102 backwash', 'No job'], ['MNT-0088 · F9 jaw heater'], 3, 48)}</div>
<div>{klabel('Parts', 'from the Item list · stock at Koyo 1 store')}
{part('PART-JH-400', 'Jaw heater 220 V 400 W', 1, '0 in stock', False)}
{part('PART-PTFE-40', 'PTFE tape 40 mm, roll', 2, '14 in stock', True)}
<a class="kb" style="height:44px;margin-top:10px">{ic("plus")}Add a part</a></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div style="display:flex;flex-direction:column;gap:8px">{klabel('Needed by')}{chips(['Now', 'Today 10:00', 'Tomorrow'], ['Today 10:00'], 3, 48)}</div>
<div style="display:flex;flex-direction:column;gap:6px;padding:12px 14px;border-radius:12px;background:var(--surface-amber-2);font-size:14px;line-height:1.5;color:var(--ink-gray-8)"><span>The jaw heater is out of stock here. Main store Lagos has 3.</span></div></div>
{pin_confirm('IK', 'Ibrahim K.', 'ibrahim.k@koyo1.ng', 'Maintenance Technician')}
</div>'''
write('KioskSpare.dc.html', kpage('Kiosk · request a spare part', maint, kdialog('Request a spare part', 'Maintenance · Koyo 1 · the storekeeper is told on WhatsApp', spr,
  'With ERPNext: Material Request MR-0195 (Material Transfer, Main store Lagos → Koyo 1 store). Without ERPNext: a Spare Part Request in Frappe Factory.', '<a href="KioskMaint.dc.html" class="kb solid">Send request</a>', 900, 'KioskMaint.dc.html')))

# ---- Decide a held lot (Quality view)
def dopt(t, d, on=False, dis=False):
    st = 'border:2px solid var(--ink-gray-9);background:var(--surface-base)' if on else 'border:1px solid var(--outline-gray-2);background:var(--surface-base)'
    if dis: st += ';opacity:.5'
    return f'<label style="display:flex;gap:12px;align-items:flex-start;padding:14px;border-radius:12px;{st}"><span class="rd{" on" if on else ""}" style="width:20px;height:20px;flex-basis:20px;margin-top:2px"></span><span style="display:flex;flex-direction:column;gap:3px"><span style="font-size:16px;font-weight:500;color:var(--ink-gray-9)">{t}</span><span class="qs" style="font-size:13px;line-height:1.4">{d}</span></span></label>'
dec = f'''<div style="display:flex;flex-direction:column;gap:16px">
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;font-size:14px">
<div style="padding:12px 14px;border-radius:12px;background:var(--surface-gray-1)"><div class="qs" style="font-size:13px">Quantity</div><div class="tab" style="font-size:17px;font-weight:600;color:var(--ink-gray-9)">156 bags + 14 sachets</div><div class="qs tab" style="font-size:13px">3,134 sachets · 1,567 L</div></div>
<div style="padding:12px 14px;border-radius:12px;background:var(--surface-gray-1)"><div class="qs" style="font-size:13px">Filled</div><div class="tab" style="font-size:17px;font-weight:600;color:var(--ink-gray-9)">08:03 – 08:14</div><div class="qs" style="font-size:13px">after SP-1 passed the alert limit</div></div>
<div style="padding:12px 14px;border-radius:12px;background:var(--surface-red-2)"><div class="qs" style="font-size:13px">Tests</div><div class="tab" style="font-size:17px;font-weight:600;color:var(--ink-red-7)">S-3 · 6.8 µg/L</div><div class="qs" style="font-size:13px">fails: limit 5 µg/L</div></div></div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px">
{dopt('Release', 'Not offered: a sample failed.', dis=True)}
{dopt('Release with deviation', 'Not offered: a sample failed.', dis=True)}
{dopt('Rework', 'Not offered for sealed sachets.', dis=True)}
{dopt('Scrap', 'Cut and drain; film to recycling.', on=True)}</div>
<div style="display:flex;flex-direction:column;gap:8px">{klabel('Reason', 'shown on the hold and the trip report')}<span class="in" style="height:48px;font-size:15px"><span class="grow">Sample S-3 at 6.8 µg/L, above the 5 µg/L limit</span></span></div>
{pin_confirm('GO', 'Grace O.', 'grace.o@koyo1.ng', 'Quality Inspector')}
</div>'''
write('KioskDecide.dc.html', kpage('Kiosk · decide a held lot', qa, kdialog('Decide lot L2 · QH-0031', 'Held since the trip at 08:14 · store bay 3, pallet H-0332 and loose crate C-7', dec,
  'Scrap: with ERPNext a Material Issue moves 156 bags + 14 sachets of PW-50CL to the Scrap warehouse and the batch stays disabled. Every decision is signed.', '<a href="KioskQA.dc.html" class="kb solid">Save decision</a>', 900, 'KioskQA.dc.html')))
