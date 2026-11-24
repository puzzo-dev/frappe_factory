from ff import *
import symbols as S

def place(inner, x, y, s=1.0, label=None, sub=None, lx=None):
    lab = ''
    if label:
        cx = 24*s if lx is None else lx
        lab = f'<text x="{x+cx:.0f}" y="{y+48*s+14:.0f}" text-anchor="middle" font-size="12" font-weight="500" fill="var(--ink-gray-8)">{label}</text>'
        if sub: lab += f'<text x="{x+cx:.0f}" y="{y+48*s+27:.0f}" text-anchor="middle" font-size="10" fill="var(--ink-gray-6)">{sub}</text>'
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
<rect x="636" y="206" width="84" height="20" rx="4" fill="var(--ink-blue-7)"/><text x="678" y="220" text-anchor="middle" font-size="12" font-weight="500" fill="#fff">P-401 · pump</text>
</g>'''
warn = '''<g><circle cx="606" cy="118" r="8" fill="var(--surface-amber-2)" stroke="var(--ink-amber-7)"/><text x="606" y="122" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink-amber-7)">!</text></g>'''
canvas_svg = f'<svg viewBox="0 0 800 440" width="100%" role="img" aria-label="Layout editor canvas, polishing and filling area" style="display:block">{pipes}{syms}{warn}{SEL}</svg>'

def bind(state, tag, typ, ok=True, val=''):
    if ok:
        ctl = f'<span class="in" style="height:28px">{ic("link","i s35")}<span class="grow tab">{tag}</span><span class="qs tab">{val}</span></span>'
    else:
        ctl = f'<span class="in err" style="height:28px">{ic("link","i s35")}<span class="grow" style="color:var(--ink-gray-4)">Pick a tag</span>{ic("chev-d","i s35")}</span>'
    return f'<div class="fl"><span class="lab" style="display:flex;justify-content:space-between"><span>{state}</span><span class="qs" style="font-size:12px">{typ}</span></span>{ctl}{"" if ok else "<span class=errm>Required by this symbol</span>"}</div>'
cats = [
  ('Tanks', [('Vertical tank', S.tank_v(0.6)), ('Horizontal tank', S.tank_h())]),
  ('Pumps', [('Centrifugal pump', S.pump(True)), ('Dosing pump', S.dosing())]),
  ('Valves', [('Two-way valve', S.valve()), ('Diverter, 3-way', S.valve3()), ('Check valve', S.check())]),
  ('Treatment', [('Media filter', S.mmf()), ('Cartridge filter', S.cart()), ('RO array', S.ro()), ('UV unit', S.uv()), ('Ion exchange', S.ix())]),
  ('Instruments', [('Analyser', S.analyser()), ('Level', S.level()), ('Flow meter', S.flow())]),
  ('Packaging', [('Sachet filler', S.filler(True))]),
]

LAYERS = [('live', 'Live values', 'activity', 'Values and states drawn over symbols'), ('labels', 'Labels', 'type', 'Tag names and captions'),
          ('inst', 'Instruments', 'gauge', 'Analysers, level and flow'), ('equip', 'Equipment', 'shapes', 'Tanks, pumps, valves, machines'),
          ('pipes', 'Pipes', 'pipe', 'Drawn from Process flow'), ('bg', 'Background', 'layout', 'Areas, walls and the floor image')]
def layers_panel(sel_tag, sel_type):
    eye_on = '<svg class="i s35" viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
    eye_off = '<svg class="i s35" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 3l18 18M10.6 5.1A10 10 0 0 1 12 5c6.5 0 10 7 10 7a17 17 0 0 1-3 3.9M6.6 6.6A17 17 0 0 0 2 12s3.5 7 10 7a9.7 9.7 0 0 0 5.4-1.6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
    rows = ''
    for k, n, i, d in LAYERS:
        child = ''
        if k == 'equip':
            child = (f'<sc-if value="{{{{is_layer__equip}}}}" hint-placeholder-val="{{{{ true }}}}"><div style="display:flex;flex-direction:column;gap:1px;padding:2px 0 4px 30px">'
                     f'<span class="lyo on" style="display:flex;align-items:center;gap:6px;height:28px;padding:0 8px;border-radius:6px;font-size:13px;background:var(--surface-blue-2);color:var(--ink-blue-7);white-space:nowrap">{sel_tag}<span class="qs" style="margin-left:auto;font-size:12px;overflow:hidden;text-overflow:ellipsis">{sel_type.split(" · ")[0]}</span></span>'
                     f'<span class="qs" style="height:24px;padding:0 8px;font-size:12px;display:flex;align-items:center">and the other symbols in this layer</span></div></sc-if>')
        rows += (f'<div style="display:flex;flex-direction:column"><div class="lyr {{{{cls_layer__{k}}}}}" style="display:flex;align-items:center;gap:8px;min-height:40px;padding:4px 8px;border-radius:8px;cursor:pointer">'
                 f'<span onClick="{{{{set_layer__{k}}}}}" style="display:flex;align-items:center;gap:8px;flex:1;min-width:0">{ic(i) if i in IC else ic("layers")}<span style="display:flex;flex-direction:column;line-height:1.2;min-width:0"><span style="font-size:14px;color:var(--ink-gray-8)">{n}</span><span class="qs" style="font-size:12px">{d}</span></span></span>'
                 f'<button type="button" class="btn ghost ico" aria-label="Show or hide {n}" onClick="{{{{toggle_vis{k}}}}}" style="width:28px;height:28px"><sc-if value="{{{{is_vis{k}__open}}}}" hint-placeholder-val="{{{{ true }}}}">{eye_on}</sc-if><sc-if value="{{{{is_vis{k}__closed}}}}" hint-placeholder-val="{{{{ false }}}}"><span style="color:var(--ink-gray-4);display:flex">{eye_off}</span></sc-if></button>'
                 f'{sdef("vis"+k, "open")}</div>{child}</div>')
    return (f'{sdef("layer","equip")}<div style="flex:1;overflow:auto;padding:12px 8px 16px;display:flex;flex-direction:column;gap:2px">{rows}</div>'
            '<div style="border-top:1px solid var(--outline-gray-1);padding:10px 12px" class="qs">Top of the list draws on top. Hidden layers stay in the layout; they are only hidden while you edit.</div>')

KOYO_LAYOUTS = [('Treatment and filling', 'LayoutEditor.dc.html', 'Process · 21 symbols'), ('Utilities · power', 'LayoutUtilities.dc.html', 'Grid, ATS, generator · 9 symbols')]
import re as _re
CW, CH, ZOOM = 688, 852, 1.25   # canvas area at 1440 × 900, and the zoom the editor opens at
def zoomed(svg):
    """Open the drawing at 125 % around the selected symbol, with a minimap of the whole layout."""
    vb = [float(v) for v in _re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups()]
    m = _re.search(r'aria-label="Selected[^"]*">\s*<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', svg)
    cx, cy = (float(m.group(1)) + float(m.group(3)) / 2, float(m.group(2)) + float(m.group(4)) / 2) if m else (vb[0] / 2, vb[1] / 2)
    w, h = vb[0] * ZOOM, vb[1] * ZOOM
    left = min(0, max(CW - w, CW / 2 - cx * ZOOM)) if w > CW else (CW - w) / 2
    top = min(0, max(CH - h, CH * 0.45 - cy * ZOOM)) if h > CH else (CH - h) / 2
    big = svg.replace('width="100%"', f'width="{w:.0f}" height="{h:.0f}"', 1)
    mw = 200; mh = mw * vb[1] / vb[0]; k = mw / vb[0]
    vx, vy = max(0, -left / ZOOM) * k, max(0, -top / ZOOM) * k
    vw, vh = min(vb[0], CW / ZOOM) * k, min(vb[1], CH / ZOOM) * k
    mini = _re.sub(r'role="img" aria-label="[^"]*"', 'aria-hidden="true"', svg.replace('width="100%"', f'width="{mw}" height="{mh:.0f}"', 1), count=1)
    return (f'<div style="position:absolute;left:{left:.0f}px;top:{top:.0f}px;width:{w:.0f}px;height:{h:.0f}px">{big}</div>'
            f'<div aria-label="Minimap" style="position:absolute;right:16px;bottom:16px;width:{mw}px;height:{mh:.0f}px;background:var(--surface-base);border:1px solid var(--outline-gray-2);border-radius:8px;box-shadow:var(--shadow-sm);overflow:hidden">'
            f'<div style="opacity:.7">{mini}</div><div style="position:absolute;left:{vx:.0f}px;top:{vy:.0f}px;width:{vw:.0f}px;height:{vh:.0f}px;border:1.5px solid var(--ink-blue-8);border-radius:3px;background:oklch(0.62 0.19 252 / 0.06)"></div></div>')

def editor(fname, cats, canvas_svg, sel_icon, sel_tag, sel_type, asset, binds, layout_name, plant_name, plant_href, ver, live, nsym, issues_txt, side_kw, top=96, pos=('640','140'), feeds='', flow_href='AssetFlow.dc.html', layouts=None):
    # ---------- palette ----------
    pal = ''
    for c, items in cats:
        pal += f'<div style="display:flex;justify-content:space-between;align-items:center;height:28px;padding:0 4px;margin-top:6px;font-size:13px;color:var(--ink-gray-6)"><span>{c}</span><span class="tab" style="font-size:12px">{len(items)}</span></div><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px">'
        for n, sv in items:
            pal += f'<div title="{n}" style="display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 2px 6px;border-radius:8px;border:1px solid var(--outline-gray-1);background:var(--surface-base);cursor:grab">{S.box(sv, 36)}<span style="font-size:12px;color:var(--ink-gray-6);text-align:center;line-height:1.2">{n}</span></div>'
        pal += '</div>'
    palette = f'''<div style="flex:0 0 15rem;width:15rem;border-right:1px solid var(--outline-gray-1);display:flex;flex-direction:column;min-height:0;background:var(--surface-base)">
    <div class="tabs" role="tablist" style="padding:0 12px">{sdef("lt","sym")}{stab("lt","sym","Symbols")}{stab("lt","lay","Layers")}</div>
    <sc-if value="{{{{is_lt__sym}}}}" hint-placeholder-val="{{{{ true }}}}">
    <div style="padding:12px 12px 8px"><span class="in muted">{ic("search")}<span class="grow">Search {nsym} symbols</span></span></div>
    <div style="flex:1;overflow:auto;padding:0 12px 16px">{pal}</div>
    <div style="border-top:1px solid var(--outline-gray-1);padding:10px 12px" class="qs">Drag a symbol onto the canvas. <a href="Symbols.dc.html">Open library</a></div></sc-if>
    <sc-if value="{{{{is_lt__lay}}}}" hint-placeholder-val="{{{{ false }}}}">{layers_panel(sel_tag, sel_type)}</sc-if></div>'''

    # ---------- inspector ----------
    inspector = f'''<aside class="panel" style="background:var(--surface-base);flex-basis:18rem;width:18rem">
    <div style="padding:14px 16px;display:flex;gap:10px;align-items:center;border-bottom:1px solid var(--outline-gray-1)"><span style="width:36px;height:36px;border-radius:8px;border:1px solid var(--outline-gray-1);display:grid;place-items:center">{S.box(sel_icon, 28)}</span><span style="display:flex;flex-direction:column;gap:2px;flex:1;min-width:0"><span style="font-weight:600;color:var(--ink-gray-9)">{sel_tag}</span><span class="qs">{sel_type}</span></span>{btn(icon="more",kind="ghost",attrs="More")}</div>
    <div class="tabs" role="tablist" style="padding:0 16px">{sdef("it","bind")}{stab("it","bind","Bindings")}{stab("it","look","Look")}{stab("it","pos","Position")}</div>
    <sc-if value="{{{{is_it__bind}}}}" hint-placeholder-val="{{{{ true }}}}"><div style="flex:1;overflow:auto;padding:16px;display:flex;flex-direction:column;gap:16px">
    {field('Asset', sel(asset), hint='The Plant Asset this symbol stands for.')}
    {field('Label', inp(sel_tag))}
    {field('Feeds into', inp(feeds), hint='From Plant Asset → Feeds into. Pipes are drawn from it.') if feeds else ''}
    <div style="display:flex;flex-direction:column;gap:12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h3 class="h3">States</h3><span class="qs">From the symbol's ports</span></div>
    {''.join(bind(*b) for b in binds)}
    </div>
    <div style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">On click</h3>
    <div style="display:flex;flex-direction:column;gap:2px">
    <label style="display:flex;align-items:center;gap:8px;height:28px;font-size:14px"><span class="rd on"></span>Open the faceplate</label>
    <label style="display:flex;align-items:center;gap:8px;height:28px;font-size:14px"><span class="rd"></span>Open trends for its tags</label>
    <label style="display:flex;align-items:center;gap:8px;height:28px;font-size:14px;color:var(--ink-gray-6)"><span class="rd" style="background:var(--surface-gray-1)"></span>Send a command <span class="bd gray sm">Commands off</span></label>
    </div></div>
    </div></sc-if>
    <sc-if value="{{{{is_it__look}}}}" hint-placeholder-val="{{{{ false }}}}"><div style="flex:1;overflow:auto;padding:16px;display:flex;flex-direction:column;gap:16px">
    {field('Style', sel('From the symbol library'), hint='Colours follow the plant theme; states change them live.')}
    {field('Label position', sel('Below'))}
    <label style="display:flex;align-items:center;justify-content:space-between;height:32px;font-size:14px">Show the label<span class="sw on"></span></label>
    <label style="display:flex;align-items:center;justify-content:space-between;height:32px;font-size:14px">Show live value under the symbol<span class="sw on"></span></label>
    <label style="display:flex;align-items:center;justify-content:space-between;height:32px;font-size:14px">Flash on alarm<span class="sw on"></span></label>
    </div></sc-if>
    <sc-if value="{{{{is_it__pos}}}}" hint-placeholder-val="{{{{ false }}}}"><div style="flex:1;overflow:auto;padding:16px;display:flex;flex-direction:column;gap:16px">
    <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px">
    {field('X', inp(f'<span class="tab">{pos[0]}</span>'))}{field('Y', inp(f'<span class="tab">{pos[1]}</span>'))}{field('Size', inp('<span class="tab">1.0×</span>'))}{field('Turn', inp('<span class="tab">0°</span>'))}
    </div>
    {field('Layer', sel('Equipment'))}
    <label style="display:flex;align-items:center;justify-content:space-between;height:32px;font-size:14px">Lock position<span class="sw"></span></label>
    <span class="qs">Snaps to an 8 px grid. Hold Shift to move freely.</span>
    </div></sc-if>
    </aside>'''

    if layouts:
        opts = ''.join(f'<a class="mi{" on" if n == layout_name else ""}" href="{h}" style="font-size:14px;text-decoration:none"><span>{n}</span><span class="qs" style="margin-left:auto;font-size:12px">{d}</span></a>' for n, h, d in layouts)
        layout_title = (f'<button type="button" onClick="{{{{toggle_lsw}}}}" class="cur" style="all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:4px;font-weight:600;color:var(--ink-gray-9)">{layout_name}{ic("chev-d","i s35")}</button>'
                        f'<sc-if value="{{{{is_lsw__open}}}}" hint-placeholder-val="{{{{ false }}}}"><div class="menu-scrim" onClick="{{{{toggle_lsw}}}}" aria-hidden="true"></div><div class="pop appmenu" role="menu" style="left:420px;top:44px;width:300px"><div style="padding:4px 8px 6px;font-size:12px;color:var(--ink-gray-6)">Layouts in {plant_name}</div>{opts}</div></sc-if>')
    else:
        layout_title = f'<span class="cur">{layout_name}</span>'
    topbar = f'''<header class="ph" style="padding:8px 16px">
    <div style="display:flex;align-items:center;gap:8px;min-width:0"><div class="crumb" style="font-size:16px"><a href="{plant_href}">{plant_name}</a><span class="sep">/</span><a href="{plant_href}">Layouts</a><span class="sep">/</span>{layout_title}</div>{bd(ver,"gray")}<span class="qs">{live}</span></div>
    <div style="display:flex;align-items:center;gap:6px">{btn(icon="undo",kind="ghost",attrs="Undo")}{btn(icon="redo",kind="ghost",attrs="Redo")}
    <span style="width:1px;height:20px;background:var(--outline-gray-2);margin:0 4px"></span>
    {btn(icon="zout",kind="ghost",attrs="Zoom out")}<span class="tab" style="font-size:13px;width:40px;text-align:center;color:var(--ink-gray-7)">125%</span>{btn(icon="zin",kind="ghost",attrs="Zoom in")}{btn("Fit",kind="ghost")}
    <label style="display:inline-flex;align-items:center;gap:8px;font-size:13px;color:var(--ink-gray-7);margin-right:4px"><span class="sw"></span>Live values</label>
    <a href="{flow_href}" class="btn">{ic("pipe")}From flow</a>{btn("Preview","eye")}<button type="button" class="btn solid">Publish</button></div></header>'''

    tools = f'''<div style="position:absolute;left:50%;top:16px;transform:translateX(-50%);display:flex;gap:2px;padding:4px;border-radius:12px;background:var(--surface-elevation-2);box-shadow:var(--shadow-2xl)">
    <span class="btn ico" style="background:var(--surface-gray-3)" title="Select">{ic("pointer")}</span><span class="btn ico ghost" title="Pipe">{ic("pipe")}</span><span class="btn ico ghost" title="Text">{ic("type")}</span><span class="btn ico ghost" title="Move canvas">{ic("move")}</span></div>'''
    issues = f'''<div style="position:absolute;left:16px;bottom:20px;display:flex;align-items:center;gap:8px;padding:6px 10px;border-radius:10px;background:var(--surface-elevation-2);box-shadow:var(--shadow-2xl);font-size:13px">{issues_txt}<button type="button" style="border:0;background:none;padding:0;font:inherit;color:var(--ink-blue-7);cursor:pointer">Show</button></div>'''

    canvas = f'<div class="grid-bg" style="flex:1;min-width:0;position:relative;background-color:var(--surface-gray-1);overflow:hidden">{zoomed(canvas_svg)}{tools}{issues}</div>'

    html = f'<div class="ff">{sidebar(fname, **side_kw)}<div style="flex:1;min-width:0;display:flex;flex-direction:column">{topbar}<div style="display:flex;flex:1;min-height:0">{palette}{canvas}{inspector}</div></div></div>'
    write(fname, page('Layout editor · ' + layout_name, html, {"$preview": {"width": 1440, "height": 900}}))


editor('LayoutEditor.dc.html', cats, canvas_svg, S.pump(True), 'P-401', 'Centrifugal pump · v3', 'P-401 · Fill pump',
       [('running', 'PLC-1 · P-401.RUN', 'bool', True, 'Off'), ('speed', 'PLC-1 · P-401.HZ', 'number · Hz', True, '0.0'), ('fault', '', 'bool', False)],
       'Treatment and filling', 'Koyo 1', 'Main.dc.html', 'Draft · v13', 'Live: v12', 46,
       '<span style="color:var(--ink-amber-8);display:flex">' + ic("alert-t","i s35") + '</span><span style="color:var(--ink-gray-8)">2 problems</span><span class="qs">P-401 fault · XV-402 not placed</span>', {}, layouts=KOYO_LAYOUTS, feeds='<span class="chip" style="height:20px">XV-402</span> <span class="chip" style="height:20px">F1 – F10</span>')
