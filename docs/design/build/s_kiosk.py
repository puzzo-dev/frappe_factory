"""Floor kiosk shell: a tablet fixed at the filling line. No sidebar by design (one task per screen,
Frappe user + PIN sign-in); same frappe-ui tokens at the touch sizes (lg controls, 40-56px targets)."""
from ff import *
import symbols as S

W_, H_ = 1180, 820
KCSS = """
.kb{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:48px;padding:0 16px;border:0;border-radius:10px;font:500 16px Inter,sans-serif;cursor:pointer;background:var(--surface-gray-2);color:var(--ink-gray-8)}
.kb.solid{background:var(--surface-gray-10);color:var(--ink-base)}
.kb svg.i{width:20px;height:20px;flex-basis:20px}
.key{height:64px;border-radius:12px;border:1px solid var(--outline-gray-2);background:var(--surface-base);font:500 24px Inter,sans-serif;color:var(--ink-gray-9);display:grid;place-items:center}
"""

def topbar(user=None, kiosk=('K1', 'Filling hall · F1 – F5', 'Koyo 1 · tablet T-02 · session KS-0221')):
    u = (f'<div style="display:flex;align-items:center;gap:10px"><span class="av md" style="width:36px;height:36px;flex:0 0 36px;font-size:13px">{user[0]}</span><span style="display:flex;flex-direction:column"><span style="font-size:15px;font-weight:500;color:var(--ink-gray-9)">{user[1]}</span><span class="qs">{user[2]}</span></span><button type="button" class="kb" style="height:40px;font-size:14px;margin-left:8px">{ic("users")}Switch user</button></div>'
         if user else '<span class="qs" style="font-size:14px">Nobody signed in</span>')
    return f'''<header style="height:64px;flex:0 0 64px;display:flex;align-items:center;justify-content:space-between;padding:0 24px;border-bottom:1px solid var(--outline-gray-1)">
<div style="display:flex;align-items:center;gap:12px"><span class="logo" style="width:36px;height:36px;flex-basis:36px">{kiosk[0]}</span><span style="display:flex;flex-direction:column"><span style="font-size:16px;font-weight:600;color:var(--ink-gray-9)">{kiosk[1]}</span><span class="qs">{kiosk[2]}</span></span></div>
<div style="display:flex;align-items:center;gap:20px">{topbar_right()}{u}</div></header>'''

def topbar_right():
    return '<span class="tab" style="font-size:20px;font-weight:600;color:var(--ink-gray-9)">08:46</span><span class="bd gray" style="height:24px;font-size:13px"><span class="dot g"></span>Online</span>'

def kpage(name, body):
    return page(name, f'<div class="ff" style="flex-direction:column;font-size:16px">{body}</div>', {"$preview": {"width": W_, "height": H_}}, helmet_extra=KCSS)

# ---------------- Sign in: Frappe user + PIN
people = [('KE', 'Kemi E.', 'kemi.e@koyo1.ng', 'Machine Operator', True), ('SI', 'Sani I.', 'sani.i@koyo1.ng', 'Machine Operator', True), ('YB', 'Yusuf B.', 'yusuf.b@koyo1.ng', 'Machine Operator', False), ('GO', 'Grace O.', 'grace.o@koyo1.ng', 'Quality Inspector', True), ('MA', 'Musa A.', 'musa.a@koyo1.ng', 'Floor Supervisor', True)]
def ptile(i, a, n, e, r, pin):
    sel_ = i == 0
    return f'<button type="button" style="display:flex;flex-direction:column;align-items:center;gap:8px;padding:18px 8px;border-radius:14px;border:{"2px solid var(--ink-gray-9)" if sel_ else "1px solid var(--outline-gray-2)"};background:{"var(--surface-base)" if pin else "var(--surface-gray-1)"};cursor:{"pointer" if pin else "not-allowed"};font:inherit;{"" if pin else "opacity:.7"}"><span class="av" style="width:56px;height:56px;flex:0 0 56px;font-size:18px">{a}</span><span style="font-size:16px;font-weight:500;color:var(--ink-gray-9)">{n}</span><span class="qs tab" style="font-size:13px">{e}</span><span class="qs" style="font-size:13px">{r}</span>{"" if pin else bd("No PIN yet","amber")}</button>'
tiles = ''.join(ptile(i, *p) for i, p in enumerate(people))
keys = ''.join(f'<span class="key">{k}</span>' for k in '123456789') + f'<span class="key" style="font-size:15px;color:var(--ink-gray-6)">Clear</span><span class="key">0</span><span class="key" style="color:var(--ink-gray-6)">{ic("arrow-l")}</span>'
dots = ''.join(f'<span style="width:16px;height:16px;border-radius:50%;{"background:var(--ink-gray-9)" if i < 2 else "border:2px solid var(--outline-gray-3)"}"></span>' for i in range(6))
login = f'''{topbar()}
<div style="flex:1;display:grid;grid-template-columns:minmax(0,1fr) 400px;min-height:0">
<div style="padding:28px 32px;display:flex;flex-direction:column;gap:18px;overflow:auto"><div style="display:flex;flex-direction:column;gap:4px"><h1 style="margin:0;font-size:24px;font-weight:600;color:var(--ink-gray-9)">Who is working here?</h1><p class="ps" style="font-size:15px">Tap your Frappe user, then enter your PIN. Only the 5 users assigned to Filling hall T-02 are listed.</p></div>
<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px">{tiles}</div>
<div style="display:flex;flex-direction:column;gap:8px;padding:14px 16px;border-radius:12px;background:var(--surface-gray-1);font-size:14px;line-height:1.5;color:var(--ink-gray-7)">
<div style="display:flex;gap:10px"><span style="color:var(--ink-gray-6);display:flex;margin-top:2px">{ic("info","i s35")}</span><span>A PIN on its own signs no one in. It is checked against the Frappe user you tapped, so every stop reason, sample and approval is recorded against that user and this shift.</span></div>
<div style="display:flex;gap:10px"><span style="color:var(--ink-amber-7);display:flex;margin-top:2px">{ic("lock","i s35")}</span><span>Yusuf B. has no PIN yet. He sets one himself in Frappe under My settings → Kiosk PIN, after signing in with his Frappe password.</span></div></div>
<span class="qs" style="font-size:14px">Not listed? A Factory Manager adds your Frappe user to this kiosk in Settings → Kiosks.</span></div>
<div style="border-left:1px solid var(--outline-gray-1);background:var(--surface-gray-1);padding:28px 32px;display:flex;flex-direction:column;align-items:center;gap:18px">
<span class="av" style="width:64px;height:64px;flex:0 0 64px;font-size:20px">KE</span><div style="text-align:center;display:flex;flex-direction:column;gap:2px"><div style="font-size:18px;font-weight:600;color:var(--ink-gray-9)">Kemi E.</div><div class="qs tab" style="font-size:14px">kemi.e@koyo1.ng · Machine Operator</div><div style="font-size:14px;color:var(--ink-gray-7);margin-top:6px">Enter your 6-digit PIN</div></div>
<div style="display:flex;gap:12px">{dots}</div>
<div style="display:grid;grid-template-columns:repeat(3,72px);gap:12px">{keys}</div>
<span class="qs" style="font-size:13px;text-align:center;line-height:1.5">5 wrong PINs lock this user on every kiosk for 15 min. Signs out after 10 min without a tap.</span></div>
</div>'''
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
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">
<button type="button" class="kb" style="height:64px">{ic("x")}Log rejects</button><button type="button" class="kb" style="height:64px">{ic("flask")}Record a sample</button><button type="button" class="kb" style="height:64px">{ic("phone")}Call supervisor</button></div>
</div>'''
write('KioskLine.dc.html', kpage('Kiosk line', line))

# ---------------- Open kiosk session (like ERPNext POS Opening Entry)
opts = [('Filling hall T-02', 'Line view · Koyo 1 · F1 – F5 · this tablet', True), ('Filling hall T-03', 'Line view · Koyo 1 · F6 – F10', False)]
ol = ''.join(f'<label style="display:grid;grid-template-columns:20px minmax(0,1fr);gap:12px;padding:14px;border-radius:12px;border:1px solid {"var(--ink-gray-9)" if on else "var(--outline-gray-2)"};cursor:pointer"><span class="rd{" on" if on else ""}" style="width:20px;height:20px;flex-basis:20px;margin-top:1px"></span><span style="display:flex;flex-direction:column;gap:2px"><span style="font-size:16px;font-weight:500;color:var(--ink-gray-9)">{n}</span><span class="qs" style="font-size:14px">{m}</span></span></label>' for n, m, on in opts)
openk = f"""<div style="position:relative;flex:1;background:var(--surface-gray-1)">
<div style="position:absolute;inset:0;display:grid;place-items:center">
<div class="dialog" role="dialog" aria-labelledby="ok-t" style="position:relative;width:560px;display:flex;flex-direction:column">
<div style="padding:24px 28px 0;display:flex;flex-direction:column;gap:6px"><h1 id="ok-t" style="margin:0;font-size:22px;font-weight:600;color:var(--ink-gray-9)">Open kiosk</h1><p class="ps" style="font-size:15px">Musa A. · musa.a@koyo1.ng · Floor Supervisor. Signed in with his Frappe user and PIN. Only kiosks he is assigned to are listed.</p></div>
<div style="padding:20px 28px;display:flex;flex-direction:column;gap:18px">
<div style="display:flex;flex-direction:column;gap:8px"><span style="font-size:14px;color:var(--ink-gray-6)">Kiosk</span>{ol}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">{field('Shift', sel('Morning · 06:00 – 14:00', 'out'))}{field('Production run', sel('RUN-0412 · from WO-0412', 'out'), hint='From ERPNext. Hidden when ERPNext is not linked.')}</div>
<div style="display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:10px;background:var(--surface-green-2);font-size:14px"><span style="color:var(--ink-green-7);display:flex">{ic("check")}</span><span style="color:var(--ink-gray-8)">This tablet is registered as T-02 for Filling hall T-02.</span></div>
</div>
<div style="padding:16px 28px 24px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--outline-gray-1)"><span class="qs" style="font-size:13px;max-width:280px">Opens full screen. Leaving needs a supervisor's Frappe user and PIN. Closing writes every sign-in to the shift.</span><button type="button" class="kb solid">Open kiosk</button></div>
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
  job('MNT-0088', 'F9 · replace jaw heater, test 40 sachets', 'Planned · logged by Musa A. 05:32 · heater from MR-0195', 'In progress', 'blue', '<button type="button" class="kb" style="height:44px;font-size:15px">Add note</button><button type="button" class="kb solid" style="height:44px;font-size:15px">Finish and test</button>'),
  job('MNT-0090', 'CF-102 · backwash the carbon filter', 'From the shift handover · due 16:00 · ΔP above 1.2 bar since 07:52', 'Open', 'gray', '<button type="button" class="kb solid" style="height:44px;font-size:15px">Start job</button>'),
  job('MNT-0091', 'DP-1 · refill antiscalant from MR-0193', 'Due 15:00 · storekeeper is bringing 2 drums of 25 L', 'Waiting for parts', 'amber', '<button type="button" class="kb" style="height:44px;font-size:15px">Start job</button>'),
])
def kal(p, col, title, meta, btn_):
    return f'<div style="display:grid;grid-template-columns:24px minmax(0,1fr) auto;gap:10px;align-items:center;padding:10px 0;border-top:1px solid var(--outline-gray-1)"><span style="width:22px;height:22px;border-radius:6px;background:{col};color:#fff;font-size:12px;font-weight:600;display:grid;place-items:center">{p}</span><span style="display:flex;flex-direction:column;gap:2px;min-width:0"><span style="font-size:15px;font-weight:500;color:var(--ink-gray-9)">{title}</span><span class="qs" style="font-size:13px">{meta}</span></span>{btn_}</div>'
AMB, RED = 'oklch(0.723 0.152 71.82)', 'oklch(0.556 0.198 26.552)'
mal = ''.join([
  kal('3', AMB, 'DP-102 carbon filter ΔP high', '1.3 bar · since 07:52 · not acknowledged', '<button type="button" class="kb" style="height:40px;font-size:14px">Acknowledge</button>'),
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
{actions(f'<button type="button" class="kb" style="height:60px">{ic("wrench")}Report a fault</button>', f'<button type="button" class="kb" style="height:60px">{ic("package")}Request a spare part</button>', f'<button type="button" class="kb" style="height:60px">{ic("phone")}Call supervisor</button>')}
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
  lot('L2', '156 bags + 14 sachets', '3,134 sachets · 08:03 – 08:14', 'S-3 failed · 6.8 µg/L', 'red', '<button type="button" class="kb solid" style="height:44px;font-size:15px">Decide</button>'),
  lot('L3', '2.3 m³ in T5', 'Not yet filled · template says reprocess', 'Reprocess via IX-501', 'gray', '<button type="button" class="kb solid" style="height:44px;font-size:15px">Decide</button>'),
])
def chk(name, rule, last, nxt, due=False):
    return f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 76px;gap:10px;align-items:center;padding:10px 0;border-top:1px solid var(--outline-gray-1)"><span style="display:flex;flex-direction:column;gap:2px;min-width:0"><span style="font-size:15px;font-weight:500;color:var(--ink-gray-9)">{name}</span><span class="qs" style="font-size:13px">{rule} · last {last}</span></span><span class="tab" style="text-align:right;font-size:15px;font-weight:600;color:{"var(--ink-amber-7)" if due else "var(--ink-gray-8)"}">{nxt}</span></div>'
checks = ''.join([
  chk('Lead at SP-1', 'Every 2 h · ASV meter · under 5 µg/L', '07:55 pass 2.2', 'Paused'),
  chk('Fill volume', '10 sachets per filler · 50 cl ± 2%', '07:30 pass', '09:30'),
  chk('Seal and leak', '10 sachets per filler · squeeze test', '06:30 pass', '10:30'),
  chk('Coliform plate', 'Daily · 2 sachets to the lab', 'yesterday pass', '11:00'),
])
qa = f'''{topbar(('GO', 'Grace O.', 'Quality Inspector'), ('K1', 'Quality lab · Koyo 1', 'Koyo 1 · tablet T-06 · session KS-0225'))}
<div style="flex:1;overflow:auto;padding:18px 24px 24px;display:flex;flex-direction:column;gap:16px">
<div style="display:flex;align-items:center;gap:14px;padding:12px 16px;border-radius:14px;background:var(--surface-red-2);border:1px solid var(--outline-red-3)"><span style="color:var(--ink-red-7);display:flex">{ic("flask","i")}</span><div style="flex:1"><div style="font-size:16px;font-weight:600;color:var(--ink-gray-9)">TRIP-0007 is waiting for you: sample 2 is due now</div><div style="font-size:14px;color:var(--ink-gray-7)">Sample 1 at 08:36 read 2.1 µg/L. Take sample 2 at SP-1, at least 10 min later. The line stays stopped until you release it.</div></div><button type="button" class="kb solid" style="height:48px">Record sample 2</button></div>
<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px">{qa_tiles}</div>
<div style="display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:14px">
{card('QH-0031 · held product', '256 bags, 14 loose sachets and 2.3 m³ · opened by TRIP-0007', lots, '<a href="QualityHold.dc.html" style="font-size:14px">Open hold</a>', 'var(--outline-amber-3)')}
{card('Routine checks', 'From the plant quality plan · lead check paused during the trip', checks)}
</div>
{actions(f'<button type="button" class="kb" style="height:60px">{ic("flask")}Record a sample</button>', f'<button type="button" class="kb" style="height:60px" disabled>{ic("lock")}QA release · needs sample 2</button>', f'<button type="button" class="kb" style="height:60px">{ic("phone")}Call supervisor</button>')}
<span class="qs" style="font-size:13px;text-align:center">Every result and decision is signed with your Frappe user and confirmed with your PIN.</span>
</div>'''
write('KioskQA.dc.html', kpage('Kiosk quality', qa))
