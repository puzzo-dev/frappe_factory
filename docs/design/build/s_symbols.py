from ff import *
import symbols as S
import symbols_ind as I

head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Symbol library',None)),
  f'{btn("Import SVG","upload","ghost")}<button type="button" class="btn solid">{ic("plus")}New symbol</button>')

packs = [
  ('Rice milling', 'Built-in pack · 8', [(n, f()) for n, f in I.RICE], 'Husker'),
  ('Edible oil', 'Built-in pack · 7', [(n, f()) for n, f in I.OIL], None),
  ('General: handling and utilities', 'Built-in · in every plant · 15',
   [(n, f()) for n, f in I.GENERAL] + [('Vertical tank', S.tank_v(0.6)), ('Centrifugal pump', S.pump(True)), ('Two-way valve', S.valve()),
    ('Diverter, 3-way', S.valve3()), ('Analyser', S.analyser()), ('Level', S.level()), ('Flow meter', S.flow()), ('Generator', S.generator())], None),
  ('Water and beverage', 'Built-in pack · 7', [('Sachet filler', S.filler(True)), ('Media filter', S.mmf()), ('Cartridge filter', S.cart()), ('RO array', S.ro()), ('UV unit', S.uv()), ('Ion exchange', S.ix()), ('Dosing pump', S.dosing())], None),
]
def card(n, sv, on):
    bord = 'border:1px solid var(--ink-gray-9);box-shadow:var(--shadow-sm)' if on else 'border:1px solid var(--outline-gray-1)'
    return f'''<div style="display:flex;flex-direction:column;border-radius:12px;{bord};overflow:hidden;cursor:pointer;background:var(--surface-base)">
<div style="height:76px;display:grid;place-items:center;background:var(--surface-gray-1)">{S.box(sv, 48)}</div>
<div style="padding:8px 10px;font-size:13px;font-weight:500;color:var(--ink-gray-8);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{n}</div></div>'''
sections = ''
for title, meta, items, sel in packs:
    sections += f'''<section style="display:flex;flex-direction:column;gap:10px"><div style="display:flex;align-items:baseline;gap:8px"><h2 class="h3">{title}</h2><span class="qs">{meta}</span></div>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:10px">{"".join(card(n, sv, n == sel) for n, sv in items)}</div></section>'''

grid = f'''<div style="flex:1;min-width:0;overflow:auto"><div class="body" style="gap:22px">
<div style="display:flex;align-items:center;justify-content:space-between;gap:8px"><div style="display:flex;gap:8px;align-items:center"><span class="in muted" style="width:220px">{ic("search")}<span class="grow">Search 37 symbols</span></span>
<div class="seg"><span class="on">All</span><span>Built-in</span><span>Your company</span></div></div><span class="chip"><span class="k">Pack</span>All 4</span></div>
<div class="alert" style="background:var(--surface-gray-1);border-color:var(--outline-gray-1)"><span style="color:var(--ink-gray-6);display:flex">{ic("info")}</span><span style="font-size:13px;line-height:1.5;color:var(--ink-gray-7)">A plant uses the general symbols plus its industry pack. Anything missing: upload an SVG, or place a <b style="font-weight:500">Generic machine</b> (a labelled box with state colour and up to three values) and swap it for a drawn symbol later. Your company's symbols are shared by all its plants.</span></div>
{sections}
</div></div>'''

def big(state):
    run = state == 'Running'; fault = state == 'Fault'
    return f'<svg viewBox="0 0 48 48" width="150" height="150" aria-label="Husker, {state.lower()}">{I.husker(run, fault)}</svg>'

ports = [('in', 'Paddy in', 'top · 24, 4'), ('out', 'Brown rice and husk out', 'bottom · 24, 44')]
pl = ''.join(f'<div style="display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:8px;align-items:center;min-height:32px;font-size:13px"><span class="tab" style="color:var(--ink-gray-8)">{a}</span><span style="color:var(--ink-gray-7)">{b}</span><span class="qs tab">{c}</span></div>' for a,b,c in ports)
states = [('running', 'bool', 'Fills the body, turns both rollers'), ('current', 'number · A', 'Shown under the label'), ('roll_gap', 'number · mm', 'Shown on hover'), ('fault', 'bool', 'Red outline')]
sl = ''.join(f'<div style="display:flex;flex-direction:column;gap:2px;padding:8px 0"><span style="display:flex;justify-content:space-between;font-size:13px"><span class="tab" style="color:var(--ink-gray-8);font-weight:500">{a}</span><span class="qs">{b}</span></span><span class="qs">{c}</span></div>' for a,b,c in states)
panel = f'''<aside class="panel" style="flex-basis:24rem;width:24rem"><div style="padding:16px;display:flex;flex-direction:column;gap:20px;overflow:auto">
<div style="display:flex;justify-content:space-between;align-items:flex-start"><div style="display:flex;flex-direction:column;gap:4px"><h2 class="h2">Husker</h2><span class="qs">HMI-SYM-0112 · Rice milling pack · Built-in</span></div>{btn(icon="more",kind="ghost",attrs="More")}</div>
<div style="border-radius:12px;background:var(--surface-gray-1);display:flex;flex-direction:column;align-items:center;gap:12px;padding:16px">
{big('Running')}
<div class="seg"><span class="on">Running</span><span>Stopped</span><span>Fault</span></div></div>
<div style="display:flex;flex-direction:column;gap:6px"><h3 class="h3">States it reads</h3><div class="divy">{sl}</div></div>
<div style="display:flex;flex-direction:column;gap:6px"><h3 class="h3">Ports</h3><div class="divy">{pl}</div><span class="qs">Pipes and chutes snap to ports in the layout editor.</span></div>
<div class="divy">
<div class="prow"><span>Version</span><span>v1 · 20 Nov 2026</span></div>
<div class="prow"><span>Used in</span><span>Rice mill · 1 layout</span></div>
<div class="prow"><span>Elements</span><span class="tab">ff-body, ff-roll-a, ff-roll-b</span></div>
<div class="prow"><span>Asset types</span><span>Rubber roll huller</span></div>
</div>
<span class="qs">SVGs are cleaned on upload: scripts, event handlers and outside links are removed.</span>
</div>
<div style="display:flex;gap:8px;padding:12px 16px;border-top:1px solid var(--outline-gray-1)">{btn("Duplicate to edit","copy")}{btn("Download","download","ghost")}</div></aside>'''

write('Symbols.dc.html', page('Symbol library', shell('Symbols.dc.html', head, f'<div style="display:flex;flex:1;min-height:0">{grid}{panel}</div>'), {"$preview": {"width": 1440, "height": 900}}))
