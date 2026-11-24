"""Missing UI states from the 23 Nov review (review-ui-states method).
Each state is its base screen with the change that state makes: a notice, a changed badge, a dialog.
Run after every other builder, because it reads the boards they wrote."""
import re, json, sys
from ff import ic, btn, bd

P = '/home/claude/ff-design/project/'
OUT, FAIL = [], []

def load(n):
    return open(P + n).read()

def sub(h, a, b, count=1):
    if a not in h:
        FAIL.append(a[:90]); return h
    return h.replace(a, b, count) if count else h.replace(a, b)

def save(name, h, title, flow, desc):
    h = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', h, count=1)
    open(P + name, 'w').write(h)
    OUT.append((name, flow, desc))

def into_body(h, snip):
    """Insert at the top of the page body (shell pages) or the kiosk's scrolling content."""
    for key in ('<div class="body"', '<div style="flex:1;overflow:auto;padding:'):
        i = h.find(key)
        if i >= 0:
            j = h.index('>', i) + 1
            return h[:j] + snip + h[j:]
    FAIL.append('no body in page'); return h

def overlay(h, dialog, back, width=520, top=120):
    i = h.index('<div class="ff"'); j = h.index('>', i) + 1
    ov = (f'<div class="ff" style="position:absolute;inset:0;display:block;min-height:0;background:transparent;z-index:40">'
          f'<a href="{back}" class="overlay" aria-label="Close"></a>'
          f'<div class="dialog" role="dialog" style="left:50%;top:{top}px;transform:translateX(-50%);width:{width}px;display:flex;flex-direction:column">{dialog}</div></div>')
    return h[:j] + ov + h[j:]

TONE = {'red': ('var(--surface-red-2)', 'var(--outline-red-3)', 'var(--ink-red-7)'),
        'amber': ('var(--surface-amber-2)', 'var(--outline-amber-3)', 'var(--ink-amber-8)'),
        'blue': ('var(--surface-blue-2)', 'var(--outline-gray-2)', 'var(--ink-blue-8)'),
        'green': ('var(--surface-green-2)', 'var(--outline-gray-2)', 'var(--ink-green-7)'),
        'gray': ('var(--surface-gray-2)', 'var(--outline-gray-2)', 'var(--ink-gray-7)')}

def notice(tone, icon, title, body, actions='', big=False):
    bg, bc, ink = TONE[tone]
    fs = 'font-size:17px' if big else 'font-size:14px'
    act = f'<div style="display:flex;gap:8px;align-items:center;flex-shrink:0">{actions}</div>' if actions else ''
    return (f'<div role="status" style="display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:12px;background:{bg};border:1px solid {bc}">'
            f'<span style="display:flex;color:{ink}">{ic(icon)}</span><div style="flex:1;display:flex;flex-direction:column;gap:2px;min-width:0">'
            f'<span style="font-weight:600;color:var(--ink-gray-9);{fs}">{title}</span><span style="font-size:{"15px" if big else "13px"};line-height:1.5;color:var(--ink-gray-7)">{body}</span></div>{act}</div>')

def dhead(title, sub_, back):
    return (f'<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px;padding:20px 20px 0">'
            f'<div style="display:flex;flex-direction:column;gap:4px"><h2 style="margin:0;font-size:18px;font-weight:600;color:var(--ink-gray-9)">{title}</h2>'
            f'<p class="ps" style="font-size:14px">{sub_}</p></div><a href="{back}" class="btn ghost ico" aria-label="Close">{ic("x")}</a></div>')

def dfoot(note, *btns):
    return (f'<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 20px;border-top:1px solid var(--outline-gray-1);margin-top:16px">'
            f'<span class="qs" style="max-width:300px;line-height:1.45">{note}</span><span style="display:flex;gap:8px">{"".join(btns)}</span></div>')

def kv(rows):
    return '<div style="display:flex;flex-direction:column;padding:12px 20px 0">' + ''.join(
        f'<div style="display:grid;grid-template-columns:150px minmax(0,1fr);gap:8px;padding:8px 0;border-bottom:1px solid var(--outline-gray-1);font-size:14px"><span class="qs">{a}</span><span style="color:var(--ink-gray-8)">{b}</span></div>' for a, b in rows) + '</div>'

def a_btn(label, href, kind='', icon=None):
    return f'<a href="{href}" class="btn {kind}">{ic(icon) if icon else ""}{label}</a>'

def kbtn(label, href, solid=False, icon=None):
    return f'<a href="{href}" style="white-space:nowrap" class="kb{" solid" if solid else ""}">{ic(icon) if icon else ""}{label}</a>'

def skeleton_rows(n, cols):
    bar = lambda w: f'<span style="display:block;height:12px;width:{w}%;border-radius:6px;background:var(--surface-gray-2)"></span>'
    return ''.join(f'<div class="lr" style="{cols};min-height:52px;cursor:default">' + ''.join(f'<span>{bar(w)}</span>' for w in (70, 45, 55, 40, 30)[:cols.count("px") + cols.count("fr")]) + '</div>' for _ in range(n))

# ======================================================================= Kiosk session
def balanced(h, start, tag='div'):
    depth = 0
    for m in re.finditer(r'<(/?)' + tag + r'\b[^>]*>', h[start:]):
        depth += -1 if m.group(1) else 1
        if depth == 0: return start + m.end()
    return len(h)

L = load('KioskLogin.dc.html')
RIGHT = '<div style="border-left:1px solid var(--outline-gray-1);background:var(--surface-gray-1);padding:28px 32px'
def right_panel(h, inner):
    i = h.find(RIGHT)
    if i < 0: FAIL.append('kiosk right panel'); return h
    e = balanced(h, i)
    return h[:i] + RIGHT + ';display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;text-align:center">' + inner + '</div>' + h[e:]

h = right_panel(L, f"""<span class="av" style="width:64px;height:64px;flex:0 0 64px;font-size:20px">KE</span>
<div style="font-size:18px;font-weight:600;color:var(--ink-gray-9)">Kemi E.</div>
{notice('red', 'lock', 'Too many wrong PINs', 'Kemi E. is locked on every kiosk at Koyo 1 for 15 minutes, until 09:02. A Factory Manager can unlock her early in App settings → Kiosks.')}
<span class="kb solid" style="width:240px;opacity:.45;cursor:not-allowed">Sign in</span>""")
save('KioskLocked.dc.html', h, 'Kiosk · locked after wrong PINs', 'Kiosk session', 'Five wrong PINs lock that user on every kiosk at the plant for 15 min.')

h = right_panel(L, f"""<span class="av" style="width:64px;height:64px;flex:0 0 64px;font-size:20px">YB</span>
<div style="display:flex;flex-direction:column;gap:2px"><div style="font-size:18px;font-weight:600;color:var(--ink-gray-9)">Yusuf B.</div><div class="qs" style="font-size:14px">First sign-in on this kiosk · step 1 of 2</div></div>
<div style="display:flex;flex-direction:column;gap:12px;width:300px;text-align:left">
<label class="fl"><span class="lab">Frappe user</span><span class="in" style="height:48px;font-size:16px;color:var(--ink-gray-7)">yusuf.b@koyo1.ng</span></label>
<label class="fl"><span class="lab">Frappe password</span><span class="in focus" style="height:48px;font-size:16px">••••••••</span></label></div>
<span class="kb solid" style="width:300px">Next: choose your PIN</span>
<span class="qs" style="font-size:13px;line-height:1.5;max-width:300px">Checked by Frappe Factory, so this step needs the internet. Your login then lasts 7 days on this kiosk; each sign-in after that is your name and PIN.</span>
{kbtn('Pick another name', 'KioskLogin.dc.html')}""")
save('KioskFirstSignIn.dc.html', h, 'Kiosk · first sign-in: Frappe login, then choose a PIN', 'Kiosk session', 'A user signs in with their Frappe login once every 7 days on the kiosk; their PIN is asked every time.')

K = load('KioskLine.dc.html')
h = overlay(K, f'''<div style="padding:28px 28px 8px;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center">
<span style="width:64px;height:64px;border-radius:32px;background:var(--surface-gray-2);display:grid;place-items:center;font-size:24px;font-weight:600;color:var(--ink-gray-9)" class="tab">0:28</span>
<h2 style="margin:0;font-size:22px;font-weight:600;color:var(--ink-gray-9)">Still there, Kemi?</h2>
<p class="ps" style="font-size:16px;max-width:380px">No taps for 9 min 32 s. This kiosk logs you out in 28 seconds so nobody else saves under your name.</p></div>
<div style="display:flex;gap:10px;padding:16px 28px 24px">{kbtn("Log out now", "KioskLogin.dc.html")}<a href="KioskLine.dc.html" class="kb solid" style="flex:1">I'm here</a></div>''', 'KioskLine.dc.html', 460, 220)
save('KioskIdle.dc.html', h, 'Kiosk · idle warning', 'Kiosk session', 'After 9.5 min without a tap the kiosk warns, then logs out at 10 min.')

h = sub(K, '<span class="dot g"></span>Online</span>', '<span class="dot o"></span>Working locally</span>')
h = into_body(h, notice('amber', 'wifi-off', 'No internet since 08:43 · working locally', 'OpsKiosk keeps working on the plant network: live values and alarms come from OpsEdge, the siren works, and sign-in uses the PINs it already holds. 2 entries are waiting and go to Frappe Factory in order when the internet returns; ERPNext postings wait until then.', big=True))
save('KioskOffline.dc.html', h, 'Kiosk · local mode, no internet', 'Kiosk session', 'Internet down: OpsKiosk keeps working on the LAN with OpsEdge; entries queue for Frappe Factory.')

R = load('KioskRejects.dc.html')
h = sub(R, '<a href="KioskLine.dc.html" class="kb solid">Save rejects</a>', '<span class="kb solid" style="opacity:.6;cursor:progress">Saving… try 2 of 5</span>')
h = sub(h, 'Saved as Kemi E.', 'Not saved yet · Kemi E.')
h = sub(h, '<div class="kb', notice('amber', 'refresh', 'The server did not answer', 'Trying again every 10 s. Your 24 sachets stay on this screen until they are saved; you can leave the dialog and they will still be sent.') + '<div class="kb', 1) if False else h
i = h.find('How many');
h = h[:i] + h[i:]
h = sub(h, 'Whole sachets only.', 'Whole sachets only.</span>' + '<div style="margin-top:8px">' + notice('amber', 'refresh', 'The server did not answer', 'Trying again every 10 s. Nothing is lost: the 24 sachets stay here until they are saved.') + '</div><span>')
save('KioskSaveRetry.dc.html', h, 'Kiosk · save failed, retrying', 'Kiosk session', 'A save that fails keeps the entry and retries; the button shows the attempt.')

save_close = overlay(K, f'''{dhead("Close the Filling hall T-02 kiosk", "Musa A. · Floor Supervisor · ends session KS-0221 for the morning shift", "KioskLine.dc.html")}
{kv([("Log-ins", "Kemi E. 06:02 – now · Sani I. 06:10 – 06:40"), ("Stops given a reason", "6 of 7 · 1 still open (07:40, all fillers)"), ("Rejects logged", "212 sachets on F1 – F5"), ("Samples", "none from this kiosk")])}
<div style="padding:12px 20px 0">{notice("amber", "alert-t", "One stop has no reason", "07:40 · all fillers · 3 min. Give it a reason now or it goes to the handover as an open item.")}</div>
{dfoot("Closing writes every log-in and entry to the shift and logs Kemi E. out.", kbtn("Give the reason", "KioskLine.dc.html"), kbtn("Close kiosk", "KioskLogin.dc.html", True))}''', 'KioskLine.dc.html', 620, 110)
save('KioskClosing.dc.html', save_close, 'Kiosk · closing the session', 'Kiosk session', 'Closing the kiosk session: a supervisor reviews the shift totals and open items.')

# ======================================================================= Alarm lifecycle (plant Alarms page)
A = load('Alarms.dc.html')
def alarms_tab(h, which):
    h = h.replace('<span class="t on" role="tab" aria-selected="true">Active', '<span class="t" role="tab">Active', 1)
    return h.replace(f'<span class="t" role="tab">{which}', f'<span class="t on" role="tab" aria-selected="true">{which}', 1)

h = sub(A, '>Acknowledged</span>', '>Cleared · not acknowledged</span>', 1)
h = into_body(h, notice('amber', 'bell', 'AT-401 Lead trip has cleared but nobody has acknowledged it', 'The value went back under the limit at 08:41. It stays in this list, and keeps escalating, until someone acknowledges it.', btn('Acknowledge')))
save('AlarmsCleared.dc.html', h, 'Alarms · cleared, not acknowledged', 'Alarm lifecycle', 'A cleared alarm nobody acknowledged stays listed and keeps escalating.')

def alist(rows):
    C = 'grid-template-columns:28px 52px minmax(0,1.6fr) 120px minmax(0,1.3fr) 110px'
    head = '<div class="list"><div class="lh" style="' + C + '"><span></span><span>Priority</span><span>Alarm</span><span>Value</span><span>Who and why</span><span>When</span></div>'
    return head + ''.join(f'<div class="lr" style="{C};min-height:56px;cursor:default"><span></span><span>{bd("P" + p, "amber" if p != "1" else "red")}</span><span class="c"><div class="t1">{t}</div><div class="m">{m}</div></span><span class="tab">{v}</span><span class="c qs" style="white-space:normal;line-height:1.4">{w}</span><span class="tab qs">{when}</span></div>' for p, t, m, v, w, when in rows) + '</div>'

def no_panel(h):
    i = h.find('<aside class="panel"')
    if i < 0: return h
    return h[:i] + h[h.index('</aside>', i) + 8:]

def alarms_page(h, which, rows, note):
    h = no_panel(alarms_tab(h, which))
    i = h.index('<div class="list"'); j = h.index('</p>', i)
    j = h.index('>', j) + 1
    return h[:i] + alist(rows) + f'<p class="qs" style="margin:12px 0 0">{note}</p>' + h[j:]

h = alarms_page(A, 'Shelved', [('3', 'F9 jaw temperature low', 'TT-F9 · Filling', '118 °C', 'Musa A. · F9 is in maintenance under MNT-0088', 'until 14:00')],
                'A shelved alarm still records, but does not show or notify until the time runs out or the job closes. Every shelve needs a reason and an end time.')
save('AlarmsShelved.dc.html', h, 'Alarms · shelved', 'Alarm lifecycle', 'Shelved alarms with who shelved them, why, and until when.')

h = alarms_page(A, 'History', [('1', 'AT-401 Lead trip', 'Raised 14 Nov 11:02 · cleared 11:40', '8.6 µg/L', 'Acknowledged in 1 min by Musa A. · TRIP-0006', '14 Nov'),
                               ('2', 'DP-102 Carbon filter ΔP high', 'Raised 18 Nov 09:10 · cleared 10:05', '1.4 bar', 'Acknowledged in 6 min by Ibrahim K. · backwashed', '18 Nov'),
                               ('2', 'T4 failed verification', 'Raised 20 Nov 15:22 · cleared 15:50', '5.4 µg/L', 'Acknowledged in 22 min by Bola N. · escalated once', '20 Nov'),
                               ('3', 'Diesel runway under 48 h', 'Raised 21 Nov 06:00 · cleared 21 Nov 11:30', '44 h', 'Acknowledged by Musa A. · refuelled 1,000 L', '21 Nov'),
                               ('3', 'RO permeate flow low', 'Raised 21 Nov 13:05 · cleared 13:20', '4.6 m³/h', 'Acknowledged in 2 min by Sani I.', '21 Nov')],
                'Closed alarms from the last 30 days. Time to acknowledge is the column ISA-18.2 asks you to watch.')
save('AlarmsHistory.dc.html', h, 'Alarms · history', 'Alarm lifecycle', 'Closed alarms with how long they took to acknowledge.')

h = into_body(A, notice('red', 'siren', 'T4 failed verification escalated to Tunde B.', 'Not acknowledged 20 min after it was raised (its response time is 15 min). Musa A. was told at 08:41 on WhatsApp; Tunde B. (Factory Manager) at 08:46.', btn('Acknowledge')))
h = sub(h, '>Unacknowledged</span>', '>Escalated · Factory Manager</span>')
save('AlarmsEscalated.dc.html', h, 'Alarms · escalated', 'Alarm lifecycle', 'An unacknowledged alarm past its response time goes up a level.')

h = into_body(A, notice('red', 'alert-t', '23 alarms in 10 minutes · flood', 'After the 08:14 trip, 19 alarms on equipment downstream of AT-401 were held back because they follow from the trip (Process Flow). The 4 that need action are listed; the rest are under the trip.', a_btn('See the 19 held', 'Trip.dc.html', 'ghost')))
h = sub(h, 'Alarm rate: 1 in the last 10 min · target 1 or fewer', '<b style="color:var(--ink-red-7)">Alarm rate: 23 in the last 10 min · target 1 or fewer</b>')
save('AlarmsFlood.dc.html', h, 'Alarms · flood', 'Alarm lifecycle', 'A flood: downstream alarms are held under the trip so the four that matter stay visible.')

i = A.index('<div class="list"'); j = A.index('</p>', i); j = A.index('>', j) + 1
empty = f'''<div style="display:flex;flex-direction:column;align-items:center;gap:8px;padding:72px 0;text-align:center"><span style="width:44px;height:44px;border-radius:22px;background:var(--surface-green-2);color:var(--ink-green-7);display:grid;place-items:center">{ic("check")}</span>
<h2 class="h2">No active alarms at Koyo 1</h2><p class="ps" style="max-width:380px">The last one, DP-102 Carbon filter ΔP high, cleared at 10:05 and was acknowledged by Ibrahim K. Shelved: none.</p>{a_btn("Open history", "AlarmsHistory.dc.html", "ghost")}</div>'''
h = A[:i] + empty + A[j:]
h = h.replace('Active <span class="bd gray">4</span>', 'Active <span class="bd gray">0</span>', 1)
save('AlarmsNone.dc.html', h, 'Alarms · none active', 'Alarm lifecycle', 'The calm state: no active alarms, with the last one named.')

# ======================================================================= Plant monitoring
D = load('PlantD.dc.html')
h = sub(D, '<span class="dot o"></span>Offline since 05:34</span>', '<span class="dot o"></span>Waiting for first data</span>')
h = sub(h, 'No data for 3 h 12 min. Last heartbeat 05:34 over Starlink; the edge kept 4 G as backup but it shows no signal. The site supervisor was told on WhatsApp at 05:44.',
        'OpsEdge D1 was paired 2 min ago and has not sent anything yet. The first values usually arrive within a minute of the box finding its PLCs.')
h = sub(h, '<span class="bd gray ">Offline</span>', '<span class="bd blue ">Connecting</span>')
h = sub(h, 'No live data since 05:34', 'Waiting for the first message from OpsEdge D1')
h = sub(h, 'The edge box at Plant D stopped reporting. It keeps recording locally and sends the gap when the link returns. Values shown are the last received.',
        'Nothing to show yet. If this lasts more than 5 minutes, open the edge box page on the plant network and check Devices.')
save('PlantConnecting.dc.html', h, 'Plant D · first connection', 'Plant monitoring', 'A newly paired plant before its first message: nothing is shown as a value.')

M = load('OilMill.dc.html')
h = sub(M, 'Live · 2 s', 'Delayed · 1 min 40 s')
h = into_body(h, notice('amber', 'clock', 'Values are 1 min 40 s old', 'The Oil mill edge box is still connected but slow (uplink queue 1,200 messages). Values update when they arrive; alarms raised on the box still fire on time. Offline after 5 min.'))
save('PlantDelayed.dc.html', h, 'Oil mill · data delayed', 'Plant monitoring', 'Between live and offline: data 30 s to 5 min old, shown as delayed.')

R2 = load('RiceMill.dc.html')
i = R2.find('<div class="mimic');
if i < 0: i = R2.find('Layout</h2>') if 'Layout</h2>' in R2 else R2.find('>Layout<')
save_nl = R2
k = R2.find('<svg', R2.find('>Layout<'))
e = R2.find('</svg>', k) + 6
if k > 0:
    save_nl = R2[:k] + f'''<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;height:300px;text-align:center"><span style="color:var(--ink-gray-6);display:flex">{ic("layout")}</span><h3 class="h3">No layout yet</h3><p class="ps" style="max-width:360px">Rice mill has 16 machines and 61 tags but no Plant Floor Layout. Draw one from its Process Flow, or start blank.</p><span style="display:flex;gap:8px">{a_btn("Generate from flow", "LayoutRice.dc.html", "", "layout")}{a_btn("Start blank", "LayoutRice.dc.html", "ghost")}</span></div>''' + R2[e:]
save('PlantNoLayout.dc.html', save_nl, 'Rice mill · no layout yet', 'Plant monitoring', 'A plant with tags but no layout: live values elsewhere work, the layout area invites one.')

if False:
    print(len(OUT), 'states'); print('FAILED:', FAIL)


def alert(h, title, body, tone=None):
    """Rewrite the page's first alert box (title, text and optionally its colour)."""
    m = re.search(r'<span class="ttl">.*?</span>(\s*)<span style="font-size:13px;line-height:1.5;color:var\(--ink-gray-7\)">.*?</span>', h, re.S)
    if not m: FAIL.append('alert box: ' + title); return h
    h = h[:m.start()] + f'<span class="ttl">{title}</span>{m.group(1)}<span style="font-size:13px;line-height:1.5;color:var(--ink-gray-7)">{body}</span>' + h[m.end():]
    if tone:
        bg, bc, ink = TONE[tone]
        h = re.sub(r'border-color:var\(--outline-(red|amber)-3\);background:var\(--surface-(red|amber)-2\)', f'border-color:{bc};background:{bg}', h, count=1)
    return h

# ======================================================================= Trip recovery
T = load('Trip.dc.html')
h = sub(T, '<span class="bd s-red ">Tripped · 32 min</span>', '<span class="bd amber ">Awaiting QA release · 1 h 06 min</span>')
h = alert(h, 'Both lab results passed · waiting for QA release', 'Sample 1 read 2.1 µg/L at 08:36 and sample 2 read 1.8 µg/L at 08:47, both under 3. Grace O. (Quality Inspector) can now release the line. Filling stays stopped until she does and the key is reset.', 'amber')
h = sub(h, '<span class="qs">2 of 7 done</span>', '<span class="qs">3 of 7 done · step 4 waiting for Grace O.</span>')
save('TripAwaitingRelease.dc.html', h, 'TRIP-0007 · awaiting QA release', 'Trip recovery', 'Both samples passed; only the Quality Inspector can release the line.')

h = sub(T, '<span class="bd s-red ">Tripped · 32 min</span>', '<span class="bd amber ">Awaiting key reset · 1 h 12 min</span>')
h = alert(h, 'Released by Grace O. at 09:20 · reset the key at the panel', 'QA release is done. Musa A. must turn key KS-401 on the filler panel; the PLC then clears IL-01 and the fillers may start. Frappe Factory cannot reset the interlock.', 'amber')
h = sub(h, '<span class="qs">2 of 7 done</span>', '<span class="qs">5 of 7 done · waiting for the key reset</span>')
save('TripAwaitingReset.dc.html', h, 'TRIP-0007 · awaiting key reset', 'Trip recovery', 'QA released; the PLC interlock is reset only by the key at the panel.')

h = sub(T, '<span class="bd s-red ">Tripped · 32 min</span>', '<span class="bd green ">Restarted · 1 h 18 min stop</span>')
h = alert(h, 'Filling restarted at 09:32', 'IL-01 was reset by key at 09:31 and F1 – F8, F10 are filling. TRIP-0007 closes when QH-0031 is closed. Lost: 1 h 18 min and about 1,170 bags (23,400 sachets).', 'green')
h = sub(h, '<span class="qs">2 of 7 done</span>', '<span class="qs">6 of 7 done · close the hold to finish</span>')
save('TripRestarted.dc.html', h, 'TRIP-0007 · restarted', 'Trip recovery', 'Restarted after the key reset; the trip closes with its quality hold.')

h = sub(T, '<span class="bd s-red ">Tripped · 32 min</span>', '<span class="bd s-red ">Tripped · 58 min</span>')
h = alert(h, 'Sample 2 failed: 4.2 µg/L at 08:47', 'Above the 3 µg/L release limit, so the line stays stopped. Find the cause before sampling again: the template suggests checking the borehole and the remineralization dosing. Sampling starts over at sample 1.', 'red')
h = sub(h, '<span class="qs">2 of 7 done</span>', '<span class="qs">2 of 7 done · step 3 failed, starts over</span>')
save('TripSampleFailed.dc.html', h, 'TRIP-0007 · second sample failed', 'Trip recovery', 'A failed release sample sends recovery back to sampling.')

# ======================================================================= Quality hold
Q = load('QualityHold.dc.html')
h = sub(Q, '<span class="bd amber ">On hold</span>', '<span class="bd blue ">Ready to close</span>')
h = alert(h, 'Every lot has a decision', 'L1 released (3 of 3 pass), L2 scrapped, L3 reprocessed through IX-501. Close the hold to post the stock moves and finish TRIP-0007.', 'blue')
h = h.replace('<span class="grow">Choose</span>', '<span class="grow">Release</span>', 1)
save('HoldReadyClose.dc.html', h, 'QH-0031 · ready to close', 'Quality hold', 'Every lot decided: the hold can be closed and its stock moves posted.')

h = sub(Q, '<span class="bd amber ">On hold</span>', '<span class="bd gray ">Closed</span>')
h = alert(h, 'Closed by Grace O. at 10:05', 'Posted to ERPNext: L1 100 bags released to Finished Goods, L2 156 bags + 14 sachets to Scrap (Material Issue MI-0921), L3 2.3 m³ reprocessed. TRIP-0007 is closed.', 'gray')
save('HoldClosed.dc.html', h, 'QH-0031 · closed', 'Quality hold', 'A closed hold shows what was posted and closes its trip.')

h = sub(Q, '<span class="bd amber ">On hold</span>', '<span class="bd amber ">Waiting for the Factory Manager</span>')
h = alert(h, 'Release with deviation needs Tunde B.', 'Grace O. proposed releasing L1 with a deviation (S-4 lab result not back). A release with deviation needs a Factory Manager who is not the inspector. Tunde B. was told at 09:40.', 'amber')
save('HoldDeviation.dc.html', h, 'QH-0031 · deviation waiting for approval', 'Quality hold', 'A release with deviation waits for a second person, the Factory Manager.')

h = sub(Q, '<span class="bd amber ">On hold</span>', '<span class="bd red ">Posting failed</span>')
h = alert(h, 'ERPNext did not accept the scrap entry', 'Material Issue for L2 failed at 10:05: "Insufficient stock of PW-50CL in Koyo 1 · Stores". The hold stays open and nothing else was posted. Fix the stock in ERPNext, then retry.', 'red')
save('HoldPostFailed.dc.html', h, 'QH-0031 · ERPNext posting failed', 'Quality hold', 'If ERPNext refuses a stock move, the hold stays open and says why.')

# ======================================================================= Downtime reason
W = load('Downtime.dc.html')
nopop = lambda h: h.replace('open_pop: !s.closed_pop', 'open_pop: false')
h = nopop(sub(W, '<span class="grow">Pick a reason</span>', '<span class="grow">Power dip</span>'))
h = sub(h, '<span class="bd amber ">3 need a reason</span>', '<span class="bd amber ">2 need a reason</span>')
h = into_body(h, notice('green', 'check', 'Saved: 07:40 · all fillers · Power dip', 'Saved by Musa A. at 08:47. ERPNext Downtime Entry DT-0318 updated.'))
save('DowntimeSaved.dc.html', h, 'Downtime · reason saved', 'Downtime reason', 'After picking a reason: the row updates and a short confirmation shows.')

h = nopop(W.replace('<span class="grow">Pick a reason</span>', '<span class="grow">Power dip</span>'))
h = sub(h, '<span class="bd amber ">3 need a reason</span>', '<span class="bd green ">All have a reason</span>')
save('DowntimeAllGiven.dc.html', h, 'Downtime · nothing needs a reason', 'Downtime reason', 'Every stop today has a reason: the badge says so instead of disappearing.')

# ======================================================================= Production run
RU = load('Runs.dc.html')
h = overlay(RU, f"""{dhead('Start a run', 'Koyo 1 · Morning · 06:00 – 14:00', 'Runs.dc.html')}
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;padding:16px 20px 0">
<label class="fl"><span class="lab">Work order</span><span class="in out"><span class="grow">WO-0413 · Pure water · 50 cl sachet</span>{ic("chev-d","i s35")}</span></label>
<label class="fl"><span class="lab">Plan</span><span class="in out"><span class="grow tab">7,200 bags · 144,000 sachets</span></span></label>
<label class="fl"><span class="lab">Fillers</span><span class="in out"><span class="grow">F1 – F8, F10 · F9 in maintenance</span></span></label>
<label class="fl"><span class="lab">Supervisor</span><span class="in out"><span class="grow">Bola N.</span>{ic("chev-d","i s35")}</span></label></div>
<div style="padding:14px 20px 0">{notice('gray', 'info', 'Checks before start', 'Treated water T2 at 70 % · film 52 rolls · no open trip · QH-0031 must be closed first.')}</div>
{dfoot('Starts a Job Card in ERPNext and counts from the fillers from now.', a_btn('Cancel', 'Runs.dc.html', 'ghost'), '<span class="btn solid" style="opacity:.45;cursor:not-allowed">Start run</span>')}""", 'Runs.dc.html', 600, 100)
save('RunStart.dc.html', h, 'Runs · start a run', 'Production run', 'Start a run from a work order; it stays disabled while a hold blocks it.')

RD = load('RunDetail.dc.html')
h = overlay(RD, f"""{dhead('End RUN-0412?', 'Pure water · 50 cl sachet · WO-0412', 'RunDetail.dc.html')}
{kv([('Good output', '1,743 bags · 34,860 sachets'), ('Rejects', '500 sachets · 25 bags worth'), ('Held', '256 bags + 14 sachets in QH-0031, not counted as good'), ('Posts to ERPNext', 'Manufacture Stock Entry for 1,743 bags · Job Card JC-0412 closed')])}
{dfoot('You can still correct counts for 24 h after ending.', a_btn('Keep running', 'RunDetail.dc.html', 'ghost'), a_btn('End run', 'RunPostFailed.dc.html', 'solid'))}""", 'RunDetail.dc.html', 560, 120)
save('RunEndConfirm.dc.html', h, 'RUN-0412 · end run', 'Production run', 'Ending a run shows what will post to ERPNext before it does.')

h = sub(RD, '<span class="bd red ">Stopped by trip</span>', '<span class="bd red ">Ended · not posted</span>')
h = sub(h, '<button type="button" class="btn solid">End run</button>', '<button type="button" class="btn solid">Retry posting</button>')
h = into_body(h, notice('red', 'alert-t', 'ERPNext rejected the Manufacture entry', '"Job Card JC-0412 is already completed" at 14:02. The run ended and its counts are kept; nothing was posted. Reopen the Job Card in ERPNext, then retry.', a_btn('Open JC-0412', 'CompanyERPNext.dc.html', 'ghost', 'ext')))
save('RunPostFailed.dc.html', h, 'RUN-0412 · posting failed', 'Production run', 'Ended but not posted: counts are kept and the ERPNext error is shown.')

h = re.sub(r'<button type="button" class="btn ghost">(<svg.*?</svg>)?Work order</button>', '', RD, count=1, flags=re.S)
h = into_body(h, notice('gray', 'info', 'ERPNext is not linked', 'This run was started by hand. Counts, OEE and stops work the same; nothing posts to stock. Link ERPNext in App settings to start runs from work orders.'))
save('RunNoERPNext.dc.html', h, 'RUN-0412 · without ERPNext', 'Production run', 'The same run with ERPNext off: no work order, nothing posted.')

# ======================================================================= Shift handover
HO = load('Handover.dc.html')
h = sub(HO, '<span class="bd gray ">Draft</span><span class="qs">Saved 08:44</span><button type="button" class="btn solid">Submit handover</button>',
        '<span class="bd amber ">Waiting for Bola N.</span><span class="qs">Submitted 13:58</span>')
h = into_body(h, notice('amber', 'clock', 'Submitted by Musa A. at 13:58', 'Bola N. accepts it when she starts the afternoon shift. The morning shift closes when she does; the four items became ToDos.'))
save('HandoverSubmitted.dc.html', h, 'Handover · submitted', 'Shift handover', 'Submitted and waiting for the incoming supervisor to accept.')

h = sub(HO, '<span class="bd gray ">Draft</span><span class="qs">Saved 08:44</span><button type="button" class="btn solid">Submit handover</button>',
        '<span class="bd green ">Accepted 14:06</span><span class="qs">Morning shift closed</span>')
h = into_body(h, notice('green', 'check', 'Accepted by Bola N. at 14:06', 'She added: "T5 nearly full, starting the recycle pump." The morning shift is closed and the handover is read-only.'))
save('HandoverAccepted.dc.html', h, 'Handover · accepted', 'Shift handover', 'Accepted: the shift closes and the handover becomes read-only.')

h = into_body(HO, notice('red', 'lock', 'The morning shift cannot close yet', 'It is 14:12 and no handover has been submitted. Handover is required at Koyo 1, so the shift stays open and Bola N. cannot start the afternoon run.', '<button type="button" class="btn solid">Submit handover</button>'))
h = sub(h, '<button type="button" class="btn solid">Submit handover</button></div></header>', '<button type="button" class="btn">Submit handover</button></div></header>')
save('HandoverBlocked.dc.html', h, 'Handover · shift blocked', 'Shift handover', 'Without a submitted handover the shift cannot close.')



def cut(h, marker, tag='div'):
    i = h.find(marker)
    if i < 0: FAIL.append('cut: ' + marker[:60]); return h
    return h[:i] + h[balanced(h, i, tag):]

def on_canvas(h, snip, top=64):
    i = h.find('<div class="grid-bg"'); j = h.index('>', i) + 1
    return h[:j] + f'<div style="position:absolute;left:16px;right:16px;top:{top}px;z-index:5">{snip}</div>' + h[j:]

# ======================================================================= Layout editor
LE = load('LayoutEditor.dc.html')
def blank_canvas(h, inner):
    i = h.find('<div class="grid-bg"'); j = h.index('>', i) + 1
    k = h.find('<div style="position:absolute;left:', j)
    h = h[:k] + h[balanced(h, k):]
    k = h.find('<div aria-label="Minimap"', j)
    if k > 0: h = h[:k] + h[balanced(h, k):]
    return h[:j] + f'<div style="position:absolute;inset:0;display:grid;place-items:center">{inner}</div>' + h[j:]

h = blank_canvas(LE, f"""<div style="display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center;max-width:380px">
<span style="width:48px;height:48px;border-radius:12px;border:1px dashed var(--outline-gray-3);display:grid;place-items:center;color:var(--ink-gray-6)">{ic("layout")}</span>
<h2 class="h2">An empty layout</h2><p class="ps" style="font-size:14px">Drag symbols from the left, or draw it from Koyo 1's Process Flow: 25 assets are placed and piped for you, then you move them.</p>
<span style="display:flex;gap:8px">{a_btn("Draw from flow", "LayoutFromFlow.dc.html", "solid", "pipe")}{a_btn("Import SVG", "LayoutEditor.dc.html", "", "upload")}</span></div>""")
h = sub(h, '<span class="bd gray ">Draft · v13</span><span class="qs">Live: v12</span>', '<span class="bd gray ">Draft · v1</span><span class="qs">Not published</span>')
h = re.sub(r'<span style="color:var\(--ink-gray-8\)">2 problems</span><span class="qs">[^<]*</span>', '<span style="color:var(--ink-gray-8)">Nothing placed yet</span><span class="qs">0 symbols</span>', h, count=1)
h = sub(h, '<button type="button" class="btn solid">Publish</button>', '<span class="btn solid" style="opacity:.45;cursor:not-allowed">Publish</span>')
save('LayoutEmpty.dc.html', h, 'Layout editor · empty layout', 'Layout editor', 'A new layout: start from the Process Flow or by dragging symbols.')

h = on_canvas(LE, notice('blue', 'pipe', 'Drawn from Process Flow v4', '25 symbols placed and 26 pipes drawn in flow order. Positions are a first pass: move them to match the floor, then Publish. Utilities (G-1) are left out.', a_btn('Undo', 'LayoutEmpty.dc.html', 'ghost')))
save('LayoutFromFlow.dc.html', h, 'Layout editor · drawn from flow', 'Layout editor', 'Generated from the Process Flow; a notice says what was placed and what to check.')

h = cut(LE, '<div style="flex:0 0 15rem;width:15rem;border-right')
h = cut(h, '<aside', 'aside')
h = sub(h, '<span class="bd gray ">Draft · v13</span><span class="qs">Live: v12</span>', '<span class="bd blue ">Preview · draft v13</span>')
h = re.sub(r'<button type="button" class="btn ">(<svg.*?</svg>)?Preview</button>', '<a href="LayoutEditor.dc.html" class="btn">Exit preview</a>', h, count=1, flags=re.S)
save('LayoutPreview.dc.html', h, 'Layout editor · preview', 'Layout editor', 'Preview shows the draft as operators will see it, with live values, before publishing.')

h = overlay(LE, f"""{dhead('Publish v13?', 'Treatment and filling · Koyo 1 · replaces v12 on the plant screen and the kiosks', 'LayoutEditor.dc.html')}
{kv([('Added', 'XV-402 diverter · bound to PLC-1 ZS-402'), ('Moved', 'P-401 and T4, 40 px right'), ('Bindings', 'P-401 fault not bound yet'), ('Seen by', 'Plant screen, 3 kiosks, the Plant B copy is not affected')])}
<div style="padding:12px 20px 0">{notice('amber', 'alert-t', '1 problem left', 'P-401 fault has no tag, so a P-401 fault will not show on the layout. You can publish anyway.')}</div>
{dfoot('v12 stays in the history and can be restored.', a_btn('Back to editing', 'LayoutEditor.dc.html', 'ghost'), a_btn('Publish v13', 'LayoutPublished.dc.html', 'solid'))}""", 'LayoutEditor.dc.html', 580, 110)
save('LayoutPublishConfirm.dc.html', h, 'Layout editor · publish', 'Layout editor', 'Publishing shows what changed and any problems left.')

h = sub(LE, '<span class="bd gray ">Draft · v13</span><span class="qs">Live: v12</span>', '<span class="bd green ">Live · v13</span><span class="qs">Published 09:12</span>')
h = on_canvas(h, notice('green', 'check', 'v13 is live', 'Published by Tunde B. at 09:12. The plant screen and the three kiosks show it from now. v12 is in the history.'))
save('LayoutPublished.dc.html', h, 'Layout editor · published', 'Layout editor', 'Published: the version is live and the previous one is kept.')

h = overlay(LE, f"""{dhead('Someone else published first', 'Bola N. published v13 at 08:40. Your draft started from v12.', 'LayoutEditor.dc.html')}
{kv([('Her changes', 'Moved T5 and added a label on IX-501'), ('Your changes', 'Added XV-402, moved P-401 and T4'), ('Overlap', 'None: different symbols')])}
{dfoot('Nothing is lost either way.', a_btn('Keep mine as v14', 'LayoutPublishConfirm.dc.html', 'ghost'), a_btn('Merge onto v13', 'LayoutEditor.dc.html', 'solid'))}""", 'LayoutEditor.dc.html', 560, 120)
save('LayoutConflict.dc.html', h, 'Layout editor · published by someone else', 'Layout editor', 'Two people editing: the second publisher merges or saves a new version.')

# ======================================================================= Process flow
F = load('AssetFlow.dc.html')
h = overlay(F, f"""{dhead('Propose a change to the process flow', 'Kemi E. · Machine Operator · goes to Tunde B. for approval (Process Flow workflow)', 'AssetFlow.dc.html')}
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;padding:16px 20px 0">
<label class="fl"><span class="lab">Asset</span><span class="in out"><span class="grow">XV-402 · diverter</span>{ic("chev-d","i s35")}</span></label>
<label class="fl"><span class="lab">Feeds into</span><span class="in out"><span class="grow">F1 – F10, <b>F11</b></span></span></label></div>
<label class="fl" style="padding:14px 20px 0"><span class="lab">Why</span><span class="in out" style="height:64px;align-items:flex-start;padding-top:8px"><span class="grow" style="white-space:normal;line-height:1.45">New filler F11 arrives 1 Dec and takes treated water from XV-402 like the others.</span></span></label>
{dfoot('Until it is approved, v4 stays live and nothing changes on the floor.', a_btn('Cancel', 'AssetFlow.dc.html', 'ghost'), a_btn('Send for approval', 'AssetFlow.dc.html', 'solid'))}""", 'AssetFlow.dc.html', 600, 110)
save('FlowProposing.dc.html', h, 'Process flow · propose a change', 'Process flow', 'Roles below Factory Manager propose a change through the workflow.')

h = sub(F, '<span class="bd amber ">Pending approval</span><button type="button" class="btn ghost">Reject</button><button type="button" class="btn solid">Approve as v5</button>',
        '<span class="bd red ">Rejected</span>' + a_btn('Propose again', 'FlowProposing.dc.html', 'ghost'))
h = sub(h, 'Kemi E. proposed v5 · Pending approval', 'Kemi E. proposed v5 · Rejected by Tunde B. at 09:20')
h = sub(h, 'Machine Operator · through the Process Flow workflow · add F11 to what XV-402 feeds, for the filler arriving 1 Dec',
        '"F11 will be fed from its own line, not XV-402. See the drawing from the installer." v4 stays live.')
save('FlowRejected.dc.html', h, 'Process flow · proposal rejected', 'Process flow', 'A rejected proposal keeps the reason and leaves the live version unchanged.')

h = sub(F, '<button type="button" class="btn ghost">Reject</button><button type="button" class="btn solid">Approve as v5</button>', '')
h = re.sub(r'<a href="LayoutEditor.dc.html" class="btn">(<svg.*?</svg>)?Generate layout</a>', '', h, count=1, flags=re.S)
h = into_body(h, notice('gray', 'lock', 'You can view the process flow', 'Halima S. · Storekeeper. Koyo 1 has no Process Flow workflow for your role, so you cannot propose changes. A Factory Manager can add your role to the workflow.')) if '<div class="body"' in h else h
if 'You can view the process flow' not in h:
    k = h.find('<div class="alert"')
    h = h[:k] + '<div style="margin-bottom:12px">' + notice('gray', 'lock', 'You can view the process flow', 'Halima S. · Storekeeper. Koyo 1 has no Process Flow workflow for your role, so you cannot propose changes. A Factory Manager can add your role to the workflow.') + '</div>' + h[k:]
save('FlowReadOnly.dc.html', h, 'Process flow · read only', 'Process flow', 'With no workflow for their role, lower roles can only read the flow.')

h = re.sub(r'(<div class="alert" style="background:var\(--surface-)green-2(\);border-color:var\(--outline-)green-3', r'\1red-2\2red-3', F, count=1)
h = sub(h, '25 assets, 26 links. Every path ends at a filler, the drain or a return.', '<b>1 path ends nowhere.</b> MMF-101 feeds nothing since CF-102 was removed, so stops at P-101 cannot be traced to the fillers.')
h = sub(h, '<button type="button" class="btn solid">Approve as v5</button>', '<span class="btn solid" style="opacity:.45;cursor:not-allowed">Approve as v5</span>')
save('FlowDeadEnd.dc.html', h, 'Process flow · a path ends nowhere', 'Process flow', 'Validation blocks approval while any path ends without a filler, drain or return.')

# ======================================================================= Add plant
AP = load('AddPlant.dc.html')
def stepper(cur, done):
    names = ['Details', 'Industry', 'Edge box', 'Layout']
    out = []
    for n, name in enumerate(names, 1):
        if n in done:
            dot = f'<span style="width:22px;height:22px;border-radius:50%;background:var(--surface-gray-10);color:var(--ink-base);display:grid;place-items:center">{ic("check","i s35")}</span>'
            col, w = 'var(--ink-gray-9)', 400
        elif n == cur:
            dot = f'<span style="width:22px;height:22px;border-radius:50%;border:1.5px solid var(--ink-gray-9);display:grid;place-items:center;font-size:12px;font-weight:600">{n}</span>'
            col, w = 'var(--ink-gray-9)', 600
        else:
            dot = f'<span style="width:22px;height:22px;border-radius:50%;background:var(--surface-gray-2);color:var(--ink-gray-6);display:grid;place-items:center;font-size:12px">{n}</span>'
            col, w = 'var(--ink-gray-6)', 400
        out.append(f'<div style="display:flex;align-items:center;gap:8px">{dot}<span style="font-size:14px;font-weight:{w};color:{col}">{name}</span></div>')
    return '<div style="display:flex;align-items:center;gap:12px">' + '<span style="flex:0 0 32px;height:1px;background:var(--outline-gray-2)"></span>'.join(out) + '</div>'

def addplant(name, cur, done, title, sub_, content, back='Back', nxt='Continue', nxt_href='#', desc=''):
    i = AP.index('<div class="body" style="max-width:1040px'); j = AP.index('>', i) + 1; e = balanced(AP, i)
    foot = f'<div style="display:flex;justify-content:space-between;padding-top:16px;border-top:1px solid var(--outline-gray-1)"><button type="button" class="btn">{back}</button>{a_btn(nxt, nxt_href, "solid")}</div>'
    body = f'{stepper(cur, done)}<div style="display:flex;flex-direction:column;gap:4px"><h2 style="margin:0;font-size:20px;font-weight:600;color:var(--ink-gray-9)">{title}</h2><p class="ps">{sub_}</p></div>{content}{foot}'
    save(name, AP[:j] + body + AP[e - 6:], 'New plant · ' + title, 'Add plant', desc)

f2 = lambda l, v, req=False: f'<label class="fl"><span class="lab">{l}{" <span style=color:var(--ink-red-7)>*</span>" if req else ""}</span><span class="in out"><span class="grow">{v}</span></span></label>'
addplant('AddPlantDetails.dc.html', 1, [], 'Name the plant', 'One plant is one factory. Everything else in this wizard can be changed later in Plant settings.',
  '<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;max-width:760px">' + f2('Plant name', 'Abuja rice mill', True) + f2('Code', 'RM2', True) + f2('Address', 'Plot 7, Idu Industrial Area, Abuja') + f2('Time zone', 'Africa/Lagos · UTC+01:00') + f2('ERPNext warehouse', 'Abuja · Stores') + f2('Factory Manager', 'Tunde B.') + '</div>',
  'Cancel', 'Continue', 'AddPlant.dc.html', 'Step 1: the plant\'s name, code, place and warehouse.')

pair_card = f"""<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px">
<div class="card" style="display:flex;flex-direction:column;gap:12px"><h3 class="h3">Pair the edge box</h3>
<p class="ps" style="font-size:14px">On the box at the plant, run this, or type the code on its own page:</p>
<div class="inset tab" style="font-size:15px;padding:12px">opsedge pair RM2-4KD-9XT</div>
<span class="qs">The code works for 24 h. It carries the broker, client ID and credentials.</span></div>
<div class="card" style="display:flex;flex-direction:column;gap:12px"><h3 class="h3">Waiting for the box</h3>
<div style="display:flex;align-items:center;gap:10px"><span class="dot o"></span><span style="font-size:14px;color:var(--ink-gray-8)">Not paired yet</span></div>
<span class="qs" style="line-height:1.5">You can finish the wizard without the box. The plant shows as Never connected until it pairs, and its alarms start once data arrives.</span></div></div>"""
addplant('AddPlantEdge.dc.html', 3, [1, 2], 'Connect the edge box', 'Frappe Factory runs in the cloud; the box at the plant connects out to it.', pair_card, 'Back', 'Continue', 'AddPlantLayout.dc.html', 'Step 3: pair the plant\'s edge box with a code.')

lay = f"""<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px">
<div class="card" style="display:flex;flex-direction:column;gap:8px;border:2px solid var(--ink-gray-9)"><h3 class="h3">Use the rice milling starter layout</h3><p class="ps">A milling line with 16 symbols, bound to the template's tag names. Move them to match the floor.</p></div>
<div class="card" style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">Copy from Rice mill</h3><p class="ps">The Kano plant's layout v2. Tags are re-bound by name; anything missing is listed.</p></div>
<div class="card" style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">Start blank</h3><p class="ps">Draw it later from the Process Flow, or by hand.</p></div></div>"""
addplant('AddPlantLayout.dc.html', 4, [1, 2, 3], 'Pick a starting layout', 'The plant screen shows this layout with live values. You can edit it any time.', lay, 'Back', 'Create plant', 'AddPlantDone.dc.html', 'Step 4: the first layout, from the template, another plant or blank.')

done = f"""<div style="display:flex;flex-direction:column;align-items:center;gap:10px;padding:40px 0;text-align:center"><span style="width:48px;height:48px;border-radius:24px;background:var(--surface-green-2);color:var(--ink-green-7);display:grid;place-items:center">{ic("check")}</span>
<h2 class="h2" style="font-size:20px">Abuja rice mill is set up</h2><p class="ps" style="font-size:14px;max-width:460px">16 machines, 61 tags, 18 alarm definitions and 22 downtime reasons from the rice milling template. It shows as Never connected until its edge box pairs.</p>
<span style="display:flex;gap:8px">{a_btn("Open the plant", "PlantConnecting.dc.html", "solid")}{a_btn("Invite people", "SettingsPeople.dc.html")}</span></div>"""
i = AP.index('<div class="body" style="max-width:1040px'); j = AP.index('>', i) + 1; e = balanced(AP, i)
save('AddPlantDone.dc.html', AP[:j] + stepper(5, [1, 2, 3, 4]) + done + AP[e - 6:], 'New plant · done', 'Add plant', 'Finished: what was created and what happens next.')

# ======================================================================= Resources and power
RS = load('Resources.dc.html')
h = sub(RS, '<span class="bd amber ">On generator</span>', '<span class="bd green ">On grid</span>')
h = sub(h, '<span style="font-weight:600;color:var(--ink-gray-9)">Grid</span><span class="bd gray ">Off</span></div><span class="qs" style="font-size:13px;line-height:1.4">Off since 07:40 · 62% of today</span>',
        '<span style="font-weight:600;color:var(--ink-gray-9)">Grid</span><span class="bd green ">On</span></div><span class="qs" style="font-size:13px;line-height:1.4">Back since 10:12 · 400 V · 49.9 Hz</span>')
h = sub(h, 'Switched by itself at 07:40.', 'Back on grid by itself at 10:12 after 2 h 32 min on generator; GEN-1 cooled down and stopped at 10:17.')
h = sub(h, '<span class="bd amber ">Running</span>', '<span class="bd gray ">Stopped</span>')
h = sub(h, 'GEN-1 · 78 kW of 120 · diesel 41 h left', 'GEN-1 · stopped 10:17 · diesel 24 %')
save('ResourcesGrid.dc.html', h, 'Resources · back on grid', 'Resources and power', 'The grid is back: the switch is read from ATS-1 and the generator stops.')

h = sub(RS, '<span class="bd amber ">On generator</span>', '<span class="bd gray ">Not measured</span>')
h = sub(h, 'Switched by itself at 07:40. Read from the changeover switch ATS-1 (PLC-1 input DI 0.4) and confirmed by the generator controller.',
        'No tag at this plant has the power_source role, so Frappe Factory cannot tell grid from generator. Wire the ATS contact to a PLC input, or log changes by hand.')
h = sub(h, '<span class="bd gray ">Off</span>', '<span class="bd gray ">Unknown</span>')
h = sub(h, '<span class="bd amber ">Running</span>', '<span class="bd gray ">Unknown</span>')
h = sub(h, 'Off since 07:40 · 62% of today', 'No signal')
h = sub(h, 'GEN-1 · 78 kW of 120 · diesel 41 h left', 'GEN-1 · no controller link · diesel 41 h left')
h = h.replace('border:1px solid var(--ink-amber-8);cursor:pointer', 'border:1px solid var(--outline-gray-2);cursor:pointer', 1).replace('border:1px solid var(--ink-amber-7);cursor:pointer', 'border:1px solid var(--outline-gray-2);cursor:pointer', 1)
save('ResourcesNotMeasured.dc.html', h, 'Resources · power not measured', 'Resources and power', 'Without an ATS, controller or meter signal, the source is shown as not measured.')

h = into_body(RS, notice('red', 'fuel', 'Diesel under the reorder point: 22 %, 31 h left', 'DT-1 has 440 L at 13.7 L/h. Material Request MR-0201 for 1,500 L was raised at 06:10 and is waiting for approval.', a_btn('Open MR-0201', 'CompanyERPNext.dc.html', 'ghost', 'ext')))
h = sub(h, 'GEN-1 · 78 kW of 120 · diesel 41 h left', 'GEN-1 · 78 kW of 120 · <b style="color:var(--ink-red-7)">diesel 31 h left</b>')
save('ResourcesDieselLow.dc.html', h, 'Resources · diesel low', 'Resources and power', 'Diesel under its reorder point, with the request already raised.')


# ======================================================================= Plant settings · Connector
C = load('Settings.dc.html')
PANEL = '<div style="display:flex;flex-direction:column;gap:40px;padding-top:24px">'
def in_panel(h, snip):
    if PANEL not in h: FAIL.append('panel'); return h
    return h.replace(PANEL, PANEL + snip, 1)
UPL = '<span class="bd green "><span class="dot g"></span>Connected</span>'
h = in_panel(C, notice('red', 'alert-c', 'Test failed at 08:47', 'The site reached mqtt.koyo.ng, but OpsEdge K1 did not answer the test message within 10 s. The box may be off, or its plant LAN may be down. Its own page shows why.', a_btn('Open edge page', 'EdgeStatus.dc.html', 'ghost', 'ext')))
save('ConnTestFailed.dc.html', h, 'Connector · test failed', 'Connector', 'Test now fails: the message says which side did not answer.')

h = sub(C, UPL, '<span class="bd red "><span class="dot r"></span>Down 14 min</span>')
h = sub(h, 'OpsEdge K1 · v0.4.2 · connected 3 h 12 min · 0 messages waiting', 'OpsEdge K1 · last message 08:33 · the box is buffering, about 8,400 messages waiting')
h = in_panel(h, notice('amber', 'wifi-off', 'The uplink from Koyo 1 is down', 'Since 08:33. The box keeps reading and buffers up to 7 days; screens show values from 08:33. An offline alarm is raised after 5 min.'))
save('ConnUplinkDown.dc.html', h, 'Connector · uplink down', 'Connector', 'The uplink is down: the buffer fills on the box and screens say how old the data is.')

h = sub(C, '<span class="in out" style="width:140px"><span class="grow tab">K1-7QF-2M9</span></span>', '<span class="in out" style="width:140px;color:var(--ink-gray-5);text-decoration:line-through"><span class="grow tab">K1-7QF-2M9</span></span>')
h = in_panel(h, notice('amber', 'clock', 'The pairing code expired', 'K1-7QF-2M9 was made yesterday at 08:12 and was never used. Codes work for 24 h. Make a new one and run opsedge pair on the box.', '<button type="button" class="btn solid">New code</button>'))
save('ConnCodeExpired.dc.html', h, 'Connector · pairing code expired', 'Connector', 'An unused pairing code expires after 24 h; a new one is one click.')

h = sub(C, 'mqtts://mqtt.koyo.ng:8883', 'mqtts://mqtt2.koyo.ng:8883')
k = h.find('<div class="dialog"'); e = balanced(h, k)
bar = '<div style="position:absolute;left:0;right:0;bottom:0;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 20px;border-top:1px solid var(--outline-gray-1);background:var(--surface-base)"><span style="font-size:14px;color:var(--ink-gray-8)">Unsaved: broker address changed. The box reconnects to the new broker when you save.</span><span style="display:flex;gap:8px"><button type="button" class="btn ghost">Discard</button><button type="button" class="btn solid">Save</button></span></div>'
h = h[:e - 6] + bar + h[e - 6:]
save('ConnUnsaved.dc.html', h, 'Connector · unsaved changes', 'Connector', 'A changed field shows a save bar; closing asks before discarding.')

# ======================================================================= Edge box
ES = load('EdgeStatus.dc.html')
h = sub(ES, '<span class="v">Connected</span><span class="d">mqtt.koyo.ng · 3 h 12 min</span>', '<span class="v" style="color:var(--ink-red-7)">Down</span><span class="d">since 08:33 · retrying every 30 s</span>')
h = sub(h, '<span class="v">0</span><span class="d">messages waiting · holds 7 days</span>', '<span class="v">8,412</span><span class="d">messages waiting · 0.2 % of 7 days</span>')
h = into_body(h, notice('amber', 'wifi-off', 'Cannot reach mqtt.koyo.ng', 'DNS works, the broker port does not answer from the plant LAN. Readings and local alarms carry on; everything is buffered and sent in order when it connects.', '<button type="button" class="btn">Try GSM backup</button>'))
h = sub(h, 'Sending to mqtt.koyo.ng · 0 waiting', 'Retrying mqtt.koyo.ng · 8,412 waiting')
h = sub(h, 'Uplink connected', 'Uplink down')
save('EdgeUplinkDown.dc.html', h, 'Edge box · uplink down', 'Edge box', 'Uplink down on the box itself: the buffer grows, local work carries on.')

h = sub(ES, '<span style="color:var(--ink-gray-8)">08:46:12 WAT · synced to pool.ntp.org 4 min ago</span><span><span class="bd green ">OK</span>', '<span style="color:var(--ink-gray-8)">08:46:12 WAT · not synced for 3 days · may be 4 min off</span><span><span class="bd red ">Not synced</span>')
h = into_body(h, notice('red', 'clock', 'Uploads are paused until the clock is synced', 'Readings with a wrong time would put stops and trips in the wrong shift, so they wait on the box. Allow UDP 123 to pool.ntp.org, or set the plant router as the time server.', '<button type="button" class="btn">Set time server</button>'))
save('EdgeClockUnsynced.dc.html', h, 'Edge box · clock not synced', 'Edge box', 'With the clock unsynced the box keeps reading but holds uploads.')

EP = load('EdgePair.dc.html')
k = EP.find('<div class="body"'); j = EP.index('>', k) + 1; e = balanced(EP, k)
unp = f"""<div style="max-width:560px;margin:24px auto 0;display:flex;flex-direction:column;gap:16px"><div class="card" style="display:flex;flex-direction:column;gap:14px;padding:24px">
<h2 class="h2" style="font-size:18px">Pair this box with Frappe Factory</h2><p class="ps" style="font-size:14px">Get a code from Frappe Factory → Plant settings → Connector, then type it here. The box downloads its broker, client ID and credentials.</p>
<label class="fl"><span class="lab">Pairing code</span><span class="in focus" style="height:40px;font-size:16px"><span class="grow tab">RM2-</span></span></label>
<button type="button" class="btn solid" style="height:36px;justify-content:center">Pair</button>
<span class="qs">Network is up: eth0 192.168.20.14 by DHCP, internet reachable. Readings start once paired.</span></div></div>"""
h = EP[:j] + unp + EP[e - 6:]
h = sub(h, 'Uplink connected', 'Not paired')
save('EdgeUnpaired.dc.html', h, 'Edge box · first boot, not paired', 'Edge box', 'First boot: the only job is to enter the pairing code.')

EL = load('EdgeLogs.dc.html')
h = into_body(EL, notice('blue', 'refresh', 'Installing OpsEdge 0.4.3 · step 3 of 4', 'Buffer was empty, so the update started at 09:00. Agent restarted on 0.4.3 and is reading; uplink restarting now. If any service fails to start, the box goes back to 0.4.2 by itself.'))
save('EdgeUpdating.dc.html', h, 'Edge box · update installing', 'Edge box', 'An update in progress, with the automatic rollback stated.')

ED = load('EdgeDevices.dc.html')
h = re.sub(r'(<span class=c>DSE-7320 · generator</span>.*?)<span class="bd green "><span class="dot g"></span>Online</span>', r'\1<span class="bd red "><span class="dot r"></span>Offline · 12 min</span>', ED, count=1, flags=re.S)
h = into_body(h, notice('red', 'cpu', 'DSE-7320 generator controller stopped answering', 'Since 08:34 on /dev/ttyUSB0 (id 10): 24 timeouts in a row. EM-1 on the same port still answers, so check the controller end of the RS-485 cable. Its 9 tags show as Bad in Frappe Factory.'))
save('EdgeDeviceOffline.dc.html', h, 'Edge box · device offline', 'Edge box', 'One device stops answering: which port, since when, and what still works.')

SC = load('EdgeScan.dc.html')
k = SC.find('<div class="list">'); e = balanced(SC, k)
h = SC[:k] + f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px;padding:48px 0;text-align:center"><span style="color:var(--ink-gray-6);display:flex">{ic("search")}</span><h3 class="h3">Nothing new answered on 10.0.2.0/24</h3><p class="ps" style="max-width:420px">254 addresses tried on Modbus TCP 502 and OPC UA 4840. Check the device is on this network and its port, or scan the serial port instead.</p></div>' + SC[e:]
h = sub(h, 'Finished 08:40 · 254 addresses · 5 devices · reads only, never writes', 'Finished 08:52 · 254 addresses · 0 devices · reads only, never writes')
h = sub(h, 'eth1 · 10.0.1.0/24', 'eth1 · 10.0.2.0/24')
save('EdgeScanEmpty.dc.html', h, 'Edge box · scan found nothing', 'Edge box', 'A scan that finds nothing says what it tried and what to check.')

LG = load('EdgeLogin.dc.html')
h = sub(LG, '<a href="EdgeStatus.dc.html" class="btn solid" style="height:36px;justify-content:center;text-decoration:none">Log in</a>',
        notice('red', 'lock', 'Locked for 15 minutes', '5 wrong passwords for ibrahim.k. Try again at 09:02, or reset the password on the box with opsedge user passwd.') + '<span class="btn solid" style="height:36px;justify-content:center;opacity:.45">Log in</span>')
save('EdgeLocked.dc.html', h, 'Edge box · login locked', 'Edge box', 'Local logins lock after five wrong passwords, with the way to reset on the box.')

# ======================================================================= Devices and tags
DV = load('Devices.dc.html')
h = sub(DV, '<h2 class="h2" style="font-size:18px">PLC-1</h2><span class="bd green "><span class="dot g"></span>Online</span>', '<h2 class="h2" style="font-size:18px">PLC-1</h2><span class="bd red "><span class="dot r"></span>Offline · 6 min</span>')
h = into_body(h, notice('red', 'cpu', 'OpsEdge K1 cannot reach PLC-1', 'No reply from 192.168.10.20:502 since 08:40. Its 48 tags show their last values marked Bad; interlocks in the PLC are not affected. The edge page shows the error.', a_btn('Open edge page', 'EdgeDevices.dc.html', 'ghost', 'ext')))
h = re.sub(r'<span class="dot g"></span>Good', '<span class="dot r"></span>Bad', h)
k = h.find('<div class="t1">PLC-1</div>')
save('DevicesOffline.dc.html', h, 'Devices · PLC offline', 'Devices and tags', 'A device that stops answering marks its tags Bad and points to the edge page.')

h = re.sub(r'(AT-302\.COND.*?)<span class="dot g"></span>Good', r'\1<span class="dot r"></span><span style="color:var(--ink-red-7);font-weight:500">Bad · out of range</span>', DV, count=1, flags=re.S)
h = into_body(h, notice('amber', 'alert-t', 'AT-302.COND reads 0, outside 0.5 – 2,000 µS/cm', 'Marked Bad since 08:41, so its alarm definitions are paused and trends show a gap. Usually a loose 4–20 mA loop at the analyser.'))
save('DevicesBadTag.dc.html', h, 'Devices · bad quality tag', 'Devices and tags', 'A value outside the sensor range is marked Bad and pauses its alarms.')

h = into_body(DV, notice('blue', 'search', '2 devices found by OpsEdge K1', 'From the scan at 08:40: 10.0.1.12 (Modbus TCP, registers 40001–40120) and opc.tcp://10.0.1.40:4840 (Siemens S7-1200, 46 nodes). Add them and pick their tags here.', '<button type="button" class="btn">Review 2</button><button type="button" class="btn ghost">Dismiss</button>'))
save('DevicesSuggestions.dc.html', h, 'Devices · scan suggestions', 'Devices and tags', 'Devices the edge box found arrive as suggestions to review.')

rows = [('v41', '22 Nov · 07:58', 'Tunde B.', 'AT-401 alert 5.0 µg/L, deadband 0.3', 'Applied 07:58:30'), ('v40', '20 Nov · 16:10', 'Tunde B.', 'Added LT-901 diesel level (MQTT)', 'Applied 16:10:41'),
        ('v39', '18 Nov · 09:02', 'Ibrahim K.', 'DP-102 poll 5 s', 'Applied 09:03:02'), ('v38', '14 Nov · 12:20', 'Tunde B.', 'IL-01 trip mirror for AT-401', 'Applied 12:20:15')]
tbl = '<div style="padding:12px 20px 0"><div class="list"><div class="lh" style="grid-template-columns:56px 130px 100px minmax(0,1fr) 120px"><span>Version</span><span>Saved</span><span>By</span><span>Change</span><span>On the box</span></div>' + ''.join(f'<div class="lr" style="grid-template-columns:56px 130px 100px minmax(0,1fr) 120px;min-height:44px;cursor:default"><span class="tab">{a}</span><span class="tab qs">{b}</span><span>{c}</span><span class="c qs" style="color:var(--ink-gray-7)">{d}</span><span class="qs">{e}</span></div>' for a, b, c, d, e in rows) + '</div></div>'
h = overlay(DV, dhead('Config versions · OpsEdge K1', 'Every save to devices, tags or alarm definitions makes a version. The box applies each one whole.', 'Devices.dc.html') + tbl + dfoot('Restoring an old version makes it the newest one.', a_btn('Close', 'Devices.dc.html', 'ghost'), '<button type="button" class="btn">Restore v40</button>'), 'Devices.dc.html', 760, 110)
save('DevicesConfigHistory.dc.html', h, 'Devices · config versions', 'Devices and tags', 'The history of config versions sent to the box, with restore.')

# ======================================================================= Company lists
CA = load('CoAlarms.dc.html')
def co_list(h, inner):
    k = h.find('<div class="list">'); e = balanced(h, k)
    return h[:k] + inner + h[e:]
C6 = 'grid-template-columns:28px minmax(0,1.6fr) 120px 80px 160px 120px'
bar = lambda w: f'<span style="display:block;height:12px;width:{w}%;border-radius:6px;background:var(--surface-gray-2)"></span>'
sk = '<div class="list"><div class="lh" style="' + C6 + '"><span></span><span>Alarm</span><span>Plant</span><span>Since</span><span>State</span><span></span></div>' + ''.join(f'<div class="lr" style="{C6};min-height:52px;cursor:default"><span>{bar(80)}</span><span style="display:flex;flex-direction:column;gap:6px">{bar(60)}{bar(35)}</span><span>{bar(70)}</span><span>{bar(60)}</span><span>{bar(55)}</span><span></span></div>' for _ in range(7)) + '</div>'
h = co_list(CA, sk)
h = re.sub(r'(<div class="card kpi"><span class="k">[^<]*</span><span class="v"[^>]*>)[^<]*(</span><span class="d">)[^<]*', r'\1—\2Loading', h)
save('ListLoading.dc.html', h, 'Alarms · loading', 'Company lists', 'Loading: rows keep their shape so nothing jumps when data arrives.')

emp = lambda icon, title, body, act='': f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px;padding:72px 0;text-align:center"><span style="color:var(--ink-gray-6);display:flex">{ic(icon)}</span><h2 class="h2">{title}</h2><p class="ps" style="max-width:420px;font-size:14px">{body}</p>{act}</div>'
h = co_list(CA, emp('bell', 'No active alarms in any plant', '6 plants reporting. The last alarm, Diesel runway under 48 h at Koyo 1, was closed at 11:30.', a_btn('Open history', 'AlarmsHistory.dc.html', 'ghost')))
save('ListEmpty.dc.html', h, 'Alarms · empty', 'Company lists', 'Empty: says the plants are reporting, so empty means calm, not broken.')

h = co_list(CA, emp('search', 'No alarms match “XV-9”', 'Searched active alarms in all 6 plants. Try the tag number without the letter, or search History.', '<span style="display:flex;gap:8px"><button type="button" class="btn">Clear search</button>' + a_btn('Search history', 'AlarmsHistory.dc.html', 'ghost') + '</span>'))
h = h.replace('<span class="grow">Search alarms</span>', '<span class="grow" style="color:var(--ink-gray-9)">XV-9</span>', 1)
save('ListNoResults.dc.html', h, 'Alarms · no results', 'Company lists', 'No results for a search or filter, with a way out.')

h = co_list(CA, f'<div style="padding:24px 0">' + notice('red', 'alert-c', 'Could not load alarms', 'The server answered 502 at 08:47. Plants keep raising and sending alarms; this list will catch up. Trying again in 20 s.', '<button type="button" class="btn">Try again</button>') + '</div>')
save('ListFailed.dc.html', h, 'Alarms · failed to load', 'Company lists', 'A failed load says what failed and that alarms are still being raised.')

if __name__ == '__main__':
    print(len(OUT), 'states'); print('FAILED:', FAIL)
    json.dump(OUT, open('/home/claude/ff-design/build/states.json', 'w'))
