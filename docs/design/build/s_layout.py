from ff import *
import symbols as S

def place(inner, x, y, s=1.0, label=None, sub=None, lx=None):
    lab = ''
    if label:
        cx = 24*s if lx is None else lx
        lab = f'<text x="{x+cx:.0f}" y="{y+48*s+14:.0f}" text-anchor="middle" font-size="11" font-weight="500" fill="var(--ink-gray-8)">{label}</text>'
        if sub: lab += f'<text x="{x+cx:.0f}" y="{y+48*s+27:.0f}" text-anchor="middle" font-size="10" fill="var(--ink-gray-5)">{sub}</text>'
    return f'<g transform="translate({x} {y}) scale({s})">{inner}</g>{lab}'

P = 'fill="none" stroke="var(--ink-gray-6)" stroke-width="1.5"'
def T(x, y, t, size=11, w=500, col='var(--ink-gray-8)', anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{w}" fill="{col}">{t}</text>'
FX = [120 + 72*i for i in range(9)]
pipes = f'''
<path d="M78 161 H96 V183 H121" {P}/>
<path d="M150 170 H246" {P}/>
<path d="M172 76 V170 M196 76 V170 M220 76 V170" {P}/>
<path d="M262 170 H305" {P}/>
<path d="M357 170 H446" {P}/>
<path d="M400 109 V170" fill="none" stroke="var(--ink-gray-5)" stroke-dasharray="3 3"/>
<path d="M482 170 H520 V64 H574 V88" {P}/>
<path d="M590 133 H620 V164 H651" {P}/>
<path d="M464 188 V210 H512 V226" {P}/>
<path d="M680 151 H760 V320 H{FX[0]+24}" {P}/>
{''.join(f'<path d="M{x+24} 320 V354" {P}/>' for x in FX)}
'''
syms = ''.join([
  place(S.tank_v(0.7), 20, 100, 1.6, 'T2', 'Permeate'),
  place(S.pump(True), 110, 159, 1.0, 'P-301'),
  place(S.dosing(), 148, 40, 1.0), place(S.dosing(), 172, 40, 1.0), place(S.dosing(), 196, 40, 1.0),
  T(196, 30, 'DP-3A · 3B · 3C', 11),
  place(S.cart(), 230, 145, 1.0, 'CF-301', '1 µm'),
  place(S.uv(), 300, 138.8, 1.3, 'UV-301'),
  place(S.analyser(), 376, 70, 1.0), T(430, 92, 'AT-401', 11, 500, anchor='start'), T(430, 105, 'Lead', 10, 400, 'var(--ink-gray-5)', 'start'),
  place(S.valve3(), 440, 144, 1.0), T(440, 206, 'XV-301', 11),
  place(S.tank_v(0.0), 540, 80, 1.4, 'T4', '2 m³'),
  place(S.pump(False), 640, 140, 1.0),
  place(S.tank_v(0.46), 488, 220, 1.0, 'T5', 'Quarantine'),
] + [place(S.filler(i != 8), FX[i], 350, 1.0, f'F{i+1}') for i in range(9)])

SEL = '''<g aria-label="Selected P-401">
<rect x="636" y="136" width="56" height="56" fill="none" stroke="var(--ink-blue-7)" stroke-width="1.25"/>
<g fill="var(--surface-base)" stroke="var(--ink-blue-7)" stroke-width="1.25">
<rect x="632.5" y="132.5" width="7" height="7"/><rect x="660.5" y="132.5" width="7" height="7"/><rect x="688.5" y="132.5" width="7" height="7"/>
<rect x="632.5" y="160.5" width="7" height="7"/><rect x="688.5" y="160.5" width="7" height="7"/>
<rect x="632.5" y="188.5" width="7" height="7"/><rect x="660.5" y="188.5" width="7" height="7"/><rect x="688.5" y="188.5" width="7" height="7"/></g>
<circle cx="651" cy="164" r="3.5" fill="var(--ink-blue-7)"/><circle cx="680" cy="151" r="3.5" fill="var(--ink-blue-7)"/>
<rect x="636" y="206" width="84" height="20" rx="4" fill="var(--ink-blue-7)"/><text x="678" y="220" text-anchor="middle" font-size="11" font-weight="500" fill="#fff">P-401 · pump</text>
</g>'''
warn = '''<g><circle cx="606" cy="118" r="8" fill="var(--surface-amber-2)" stroke="var(--ink-amber-7)"/><text x="606" y="122" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink-amber-7)">!</text></g>'''
canvas_svg = f'<svg viewBox="0 0 800 440" width="100%" role="img" aria-label="Layout editor canvas, polishing and filling area" style="display:block">{pipes}{syms}{warn}{SEL}</svg>'

# ---------- palette ----------
cats = [
  ('Tanks', [('Vertical tank', S.tank_v(0.6)), ('Horizontal tank', S.tank_h())]),
  ('Pumps', [('Centrifugal pump', S.pump(True)), ('Dosing pump', S.dosing())]),
  ('Valves', [('Two-way valve', S.valve()), ('Diverter, 3-way', S.valve3()), ('Check valve', S.check())]),
  ('Treatment', [('Media filter', S.mmf()), ('Cartridge filter', S.cart()), ('RO array', S.ro()), ('UV unit', S.uv()), ('Ion exchange', S.ix())]),
  ('Instruments', [('Analyser', S.analyser()), ('Level', S.level()), ('Flow meter', S.flow())]),
  ('Packaging', [('Sachet filler', S.filler(True))]),
]
pal = ''
for c, items in cats:
    pal += f'<div style="display:flex;justify-content:space-between;align-items:center;height:28px;padding:0 4px;margin-top:6px;font-size:13px;color:var(--ink-gray-5)"><span>{c}</span><span class="tab" style="font-size:12px">{len(items)}</span></div><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px">'
    for n, sv in items:
        pal += f'<div title="{n}" style="display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 2px 6px;border-radius:8px;border:1px solid var(--outline-gray-1);background:var(--surface-base);cursor:grab">{S.box(sv, 36)}<span style="font-size:11px;color:var(--ink-gray-6);text-align:center;line-height:1.2">{n}</span></div>'
    pal += '</div>'
palette = f'''<div style="flex:0 0 15rem;width:15rem;border-right:1px solid var(--outline-gray-1);display:flex;flex-direction:column;min-height:0;background:var(--surface-base)">
<div class="tabs" style="padding:0 12px"><span class="t on">Symbols</span><span class="t">Layers</span></div>
<div style="padding:12px 12px 8px"><span class="in muted">{ic("search")}<span class="grow">Search 46 symbols</span></span></div>
<div style="flex:1;overflow:auto;padding:0 12px 16px">{pal}</div>
<div style="border-top:1px solid var(--outline-gray-1);padding:10px 12px" class="qs">Drag a symbol onto the canvas. <a href="Symbols.dc.html">Open library</a></div></div>'''

# ---------- inspector ----------
def bind(state, tag, typ, ok=True, val=''):
    if ok:
        ctl = f'<span class="in" style="height:28px">{ic("link","i s35")}<span class="grow tab">{tag}</span><span class="qs tab">{val}</span></span>'
    else:
        ctl = f'<span class="in err" style="height:28px">{ic("link","i s35")}<span class="grow" style="color:var(--ink-gray-4)">Pick a tag</span>{ic("chev-d","i s35")}</span>'
    return f'<div class="fl"><span class="lab" style="display:flex;justify-content:space-between"><span>{state}</span><span class="qs" style="font-size:12px">{typ}</span></span>{ctl}{"" if ok else "<span class=errm>Required by this symbol</span>"}</div>'
inspector = f'''<aside class="panel" style="background:var(--surface-base);flex-basis:18rem;width:18rem">
<div style="padding:14px 16px;display:flex;gap:10px;align-items:center;border-bottom:1px solid var(--outline-gray-1)"><span style="width:36px;height:36px;border-radius:8px;border:1px solid var(--outline-gray-1);display:grid;place-items:center">{S.box(S.pump(True), 28)}</span><span style="display:flex;flex-direction:column;gap:2px;flex:1;min-width:0"><span style="font-weight:600;color:var(--ink-gray-9)">P-401</span><span class="qs">Centrifugal pump · v3</span></span>{btn(icon="more",kind="ghost",attrs="More")}</div>
<div class="tabs" style="padding:0 16px"><span class="t on">Bindings</span><span class="t">Look</span><span class="t">Position</span></div>
<div style="flex:1;overflow:auto;padding:16px;display:flex;flex-direction:column;gap:16px">
{field('Asset', sel('P-401 · Fill pump'), hint='The Plant Asset this symbol stands for.')}
{field('Label', inp('P-401'))}
<div style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h3 class="h3">States</h3><span class="qs">From the symbol's ports</span></div>
{bind('running', 'PLC-1 · P-401.RUN', 'bool', True, 'Off')}
{bind('speed', 'PLC-1 · P-401.HZ', 'number · Hz', True, '0.0')}
{bind('fault', '', 'bool', False)}
</div>
<div style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">On click</h3>
<div style="display:flex;flex-direction:column;gap:2px">
<label style="display:flex;align-items:center;gap:8px;height:28px;font-size:14px"><span class="rd on"></span>Open the faceplate</label>
<label style="display:flex;align-items:center;gap:8px;height:28px;font-size:14px"><span class="rd"></span>Open trends for its tags</label>
<label style="display:flex;align-items:center;gap:8px;height:28px;font-size:14px;color:var(--ink-gray-5)"><span class="rd" style="background:var(--surface-gray-1)"></span>Send a command <span class="bd gray sm">Commands off</span></label>
</div></div>
<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px">
{field('X', inp('<span class="tab">640</span>'))}{field('Y', inp('<span class="tab">140</span>'))}{field('Size', inp('<span class="tab">1.0×</span>'))}{field('Turn', inp('<span class="tab">0°</span>'))}
</div>
</div></aside>'''

topbar = f'''<header class="ph" style="padding:8px 16px">
<div style="display:flex;align-items:center;gap:8px;min-width:0"><div class="crumb" style="font-size:16px"><a href="Main.dc.html">Layouts</a><span class="sep">/</span><span class="cur">Treatment and filling</span></div>{bd("Draft · v13","gray")}<span class="qs">Live: v12</span></div>
<div style="display:flex;align-items:center;gap:6px">{btn(icon="undo",kind="ghost",attrs="Undo")}{btn(icon="redo",kind="ghost",attrs="Redo")}
<span style="width:1px;height:20px;background:var(--outline-gray-2);margin:0 4px"></span>
{btn(icon="zout",kind="ghost",attrs="Zoom out")}<span class="tab" style="font-size:13px;width:40px;text-align:center;color:var(--ink-gray-7)">100%</span>{btn(icon="zin",kind="ghost",attrs="Zoom in")}
<label style="display:inline-flex;align-items:center;gap:8px;font-size:13px;color:var(--ink-gray-7);margin-right:4px"><span class="sw"></span>Live values</label>
{btn("Preview","eye")}<button type="button" class="btn solid">Publish</button></div></header>'''

tools = f'''<div style="position:absolute;left:50%;top:16px;transform:translateX(-50%);display:flex;gap:2px;padding:4px;border-radius:12px;background:var(--surface-elevation-2);box-shadow:var(--shadow-2xl)">
<span class="btn ico" style="background:var(--surface-gray-3)" title="Select">{ic("pointer")}</span><span class="btn ico ghost" title="Pipe">{ic("pipe")}</span><span class="btn ico ghost" title="Text">{ic("type")}</span><span class="btn ico ghost" title="Move canvas">{ic("move")}</span></div>'''
issues = f'''<div style="position:absolute;left:16px;bottom:20px;display:flex;align-items:center;gap:8px;padding:6px 10px;border-radius:10px;background:var(--surface-elevation-2);box-shadow:var(--shadow-2xl);font-size:13px"><span style="color:var(--ink-amber-7);display:flex">{ic("alert-t","i s35")}</span><span style="color:var(--ink-gray-8)">2 problems</span><span class="qs">P-401 fault · XV-402 not placed</span><a href="#">Show</a></div>'''

canvas = f'<div class="grid-bg" style="flex:1;min-width:0;position:relative;background-color:var(--surface-gray-1);overflow:hidden"><div style="position:absolute;left:32px;right:32px;top:96px">{canvas_svg}</div>{tools}{issues}</div>'

html = f'<div class="ff">{sidebar("LayoutEditor.dc.html")}<div style="flex:1;min-width:0;display:flex;flex-direction:column">{topbar}<div style="display:flex;flex:1;min-height:0">{palette}{canvas}{inspector}</div></div></div>'
write('LayoutEditor.dc.html', page('Layout editor', html, {"$preview": {"width": 1440, "height": 900}}))
