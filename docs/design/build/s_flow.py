"""Process flow: Plant Asset → Feeds into, edited as a graph. Drives generated layouts, starved/blocked stops,
downstream alarm suppression and quality-hold tracing."""
from ff import *

W, H = 84, 36
N = {}
def node(key, x, y, tag, typ, sel=False, w=W, muted=False):
    N[key] = (x, y, w)
    st = 'stroke:var(--ink-blue-7);stroke-width:2' if sel else 'stroke:var(--ink-gray-6);stroke-width:1.25'
    fill = 'var(--surface-gray-1)' if muted else 'var(--surface-base)'
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{H}" rx="6" style="fill:{fill};{st}"/>'
            f'<text x="{x+w/2}" y="{y+15}" text-anchor="middle" font-size="11" font-weight="600" fill="var(--ink-gray-9)">{tag}</text>'
            f'<text x="{x+w/2}" y="{y+28}" text-anchor="middle" font-size="9" fill="var(--ink-gray-5)">{typ}</text></g>')
def pt(k, side):
    x, y, w = N[k]
    return {'r': (x+w, y+H/2), 'l': (x, y+H/2), 't': (x+w/2, y), 'b': (x+w/2, y+H)}[side]
def edge(a, sa, b, sb, ret=False, label=''):
    (x1, y1), (x2, y2) = pt(a, sa), pt(b, sb)
    if sa in 'rl' and sb in 'rl': d = f'M{x1} {y1} H{x2}' if y1 == y2 else f'M{x1} {y1} H{(x1+x2)/2} V{y2} H{x2}'
    elif sa in 'tb' and sb in 'tb': d = f'M{x1} {y1} V{y2}' if x1 == x2 else f'M{x1} {y1} V{(y1+y2)/2} H{x2} V{y2}'
    elif sa in 'tb': d = f'M{x1} {y1} V{y2} H{x2}'
    else: d = f'M{x1} {y1} H{x2} V{y2}'
    dash = ' stroke-dasharray="5 4"' if ret else ''
    lab = f'<text x="{(x1+x2)/2}" y="{min(y1,y2)-5}" text-anchor="middle" font-size="9" fill="var(--ink-gray-5)">{label}</text>' if label else ''
    return f'<path d="{d}" fill="none" stroke="var(--ink-gray-6)" stroke-width="1.25"{dash} marker-end="url(#arr)"/>{lab}'

X = [16 + i*104 for i in range(8)]
nodes = ''.join([
  node('bh', X[0], 40, 'Borehole', 'source'), node('t1', X[1], 40, 'T1', 'raw tank'), node('p101', X[2], 40, 'P-101', 'feed pump'),
  node('mmf', X[3], 40, 'MMF-101', 'media filter'), node('cf102', X[4], 40, 'CF-102', 'carbon filter'), node('cf201', X[5], 40, 'CF-201', '5 µm cartridge'),
  node('p201', X[6], 40, 'P-201', 'HP pump'), node('ro', X[7], 40, 'RO-201', 'RO array'),
  node('drain', 852, 120, 'Drain', 'sink', w=64, muted=True), node('dp1', X[6], 118, 'DP-1', 'antiscalant'), node('dp3', X[5], 118, 'DP-3A·B·C', 'remineral.'),
  node('t2', X[7], 200, 'T2', 'permeate'), node('p301', X[6], 200, 'P-301', 'transfer'), node('cf301', X[5], 200, 'CF-301', '1 µm cartridge'),
  node('uv', X[4], 200, 'UV-301', 'UV'), node('xv301', X[3], 200, 'XV-301', 'diverter'), node('t4', X[2], 200, 'T4', 'verify'),
  node('p401', X[1], 200, 'P-401', 'fill pump', sel=True), node('xv402', X[0], 200, 'XV-402', 'valve'),
  node('fill', X[0], 300, 'F1 – F10', '10 sachet fillers', w=188), node('t5', X[3], 300, 'T5', 'quarantine'),
  node('p501', X[4], 300, 'P-501', 'recycle pump'), node('ix', X[5], 300, 'IX-501', 'ion exchange'),
])
edges = ''.join([
  edge('bh','r','t1','l'), edge('t1','r','p101','l'), edge('p101','r','mmf','l'), edge('mmf','r','cf102','l'), edge('cf102','r','cf201','l'),
  edge('cf201','r','p201','l'), edge('p201','r','ro','l'), edge('dp1','t','p201','b'), edge('ro','r','drain','t', label=''),
  edge('ro','b','t2','t', label=''), edge('t2','l','p301','r'), edge('p301','l','cf301','r'), edge('dp3','b','cf301','t'),
  edge('cf301','l','uv','r'), edge('uv','l','xv301','r'), edge('xv301','l','t4','r'), edge('t4','l','p401','r'), edge('p401','l','xv402','r'),
  edge('xv402','b','fill','t'), edge('xv301','b','t5','t', label=''), edge('t5','r','p501','l'), edge('p501','r','ix','l'),
])
ixr = pt('ix', 'r'); t1t = pt('t1', 't')
ret = f'<path d="M{ixr[0]} {ixr[1]} H930 V12 H{t1t[0]} V{t1t[1]}" fill="none" stroke="var(--ink-gray-6)" stroke-width="1.25" stroke-dasharray="5 4" marker-end="url(#arr)"/><text x="925" y="190" text-anchor="end" font-size="9" fill="var(--ink-gray-5)">return to T1</text>'
inst = f'<g><circle cx="422" cy="218" r="9" fill="var(--surface-base)" stroke="var(--ink-gray-6)"/><text x="422" y="221" text-anchor="middle" font-size="7" font-weight="600" fill="var(--ink-gray-7)">AT</text><text x="422" y="244" text-anchor="middle" font-size="9" fill="var(--ink-gray-5)">AT-401 on line</text></g>'
labs = ''.join([f'<text x="856" y="52" text-anchor="middle" font-size="9" fill="var(--ink-gray-5)">concentrate</text>',
                f'<text x="790" y="140" text-anchor="start" font-size="9" fill="var(--ink-gray-5)">permeate</text>',
                f'<text x="378" y="284" text-anchor="start" font-size="9" fill="var(--ink-gray-5)">diverted on trip</text>'])
svg = (f'<svg viewBox="0 0 950 350" width="100%" role="img" aria-label="Process flow of Koyo 1 drawn from each asset\'s Feeds into links: borehole to T1, filters, RO, T2, remineralization, UV, diverter, T4 verify, fill pump and ten fillers; diverter to T5 quarantine, recycle pump and ion exchange back to T1." style="display:block">'
       f'<defs><marker id="arr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L8 4 L0 8 z" fill="var(--ink-gray-6)"/></marker></defs>{edges}{ret}{nodes}{inst}{labs}</svg>')

FC = 'grid-template-columns:110px minmax(0,1fr) 120px 80px'
links = [('Borehole', 'T1', 'Raw water', ''), ('T1', 'P-101', 'Raw water', ''), ('P-101', 'MMF-101', 'Raw water', ''), ('MMF-101', 'CF-102', 'Raw water', ''),
         ('RO-201', 'T2 · Drain', 'Permeate · concentrate', ''), ('XV-301', 'T4 · T5', 'Treated water', 'Diverter'), ('T4', 'P-401', 'Treated water', ''),
         ('P-401', 'XV-402', 'Treated water', ''), ('XV-402', 'F1 – F10', 'Treated water', ''), ('IX-501', 'T1', 'Recovered water', 'Return')]
lr = ''.join(f'<div class="lr" style="{FC};cursor:default;{"background:var(--surface-gray-2)" if a=="P-401" else ""}"><span class="t1">{a}</span><span style="display:flex;gap:4px;flex-wrap:wrap">{"".join(f"<span class=chip style=height:22px>{x}</span>" for x in b.split(" · "))}</span><span class="qs">{m}</span><span>{bd(r, "violet" if r=="Return" else "gray") if r else ""}</span></div>' for a, b, m, r in links)

head = header(crumb(('Plants', 'Plants.dc.html'), ('Koyo 1', 'Main.dc.html'), ('Process flow', None)),
              f'{btn("Import from P&ID","upload","ghost")}<a href="LayoutEditor.dc.html" class="btn solid">{ic("layout")}Generate layout</a>')
checks = f'''<div class="alert" style="background:var(--surface-green-2);border-color:var(--outline-green-3);align-items:center"><span style="color:var(--ink-green-7);display:flex">{ic("check")}</span>
<span style="font-size:14px;color:var(--ink-gray-8)">25 assets, 26 links. Every path ends at a filler, the drain or a return. 1 return loop (IX-501 → T1), marked as a return. Utilities such as G-1 are left out of the flow. Last edited by Kemi E., Machine Operator, 20 Nov.</span></div>'''
main = f'''<div style="flex:1;min-width:0;overflow:auto"><div class="body">{checks}
<section class="card" style="background:var(--surface-gray-1);padding:12px;display:flex;flex-direction:column;gap:8px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h3">Flow</h2><span class="qs">Drawn from each asset's Feeds into · arrows follow the product</span></div>{svg}</section>
<section style="display:flex;flex-direction:column;gap:10px"><div style="display:flex;justify-content:space-between;align-items:baseline"><h2 class="h2">Links</h2><span class="qs">10 of 26 shown</span></div>
<div class="list"><div class="lh" style="{FC}"><span>Asset</span><span>Feeds into</span><span>Carries</span><span></span></div>{lr}</div></section></div></div>'''
panel = f'''<aside class="panel"><div style="padding:16px;display:flex;flex-direction:column;gap:18px;overflow:auto">
<div style="display:flex;flex-direction:column;gap:2px"><span style="font-weight:600;color:var(--ink-gray-9)">P-401 · Fill pump</span><span class="qs">Plant Asset · Treatment and filling</span></div>
<div style="display:flex;gap:8px;align-items:flex-start;padding:10px 12px;border-radius:8px;background:var(--surface-gray-1);font-size:13px;line-height:1.45;color:var(--ink-gray-7)"><span style="display:flex;margin-top:1px;color:var(--ink-gray-6)">{ic("lock","i s35")}</span><span>Edited by the Factory Manager (as Floor Engineer) or a Machine Operator. Everyone else can read it.</span></div>
{field('Fed by', inp('<span class="chip" style="height:20px">T4 verify</span>', 'out'))}
{field('Feeds into', inp('<span class="chip" style="height:20px">XV-402</span>', 'focus', right=ic("plus","i s35")), hint='Pick one or more downstream assets in this plant.')}
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">{field('Carries', sel('Treated water', 'out'))}{field('Return link', sel('No', 'out'))}</div>
<div style="display:flex;flex-direction:column;gap:6px"><h3 class="h3">Downstream of P-401</h3><span class="qs" style="line-height:1.5">XV-402 and fillers F1 – F10: 11 assets.</span></div>
<div style="display:flex;flex-direction:column;gap:8px"><h3 class="h3">What uses this</h3><div class="divy" style="font-size:13px;line-height:1.45">
<div style="padding:8px 0"><b style="font-weight:500;color:var(--ink-gray-8)">Generated layout.</b> <span class="qs">Pipes and the order of symbols come from these links.</span></div>
<div style="padding:8px 0"><b style="font-weight:500;color:var(--ink-gray-8)">Starved and blocked stops.</b> <span class="qs">If P-401 stops, the fillers' stops are logged as starved, not as their own fault.</span></div>
<div style="padding:8px 0"><b style="font-weight:500;color:var(--ink-gray-8)">Alarm flood control.</b> <span class="qs">After an upstream trip, alarms on downstream assets are held for 60 s.</span></div>
<div style="padding:8px 0"><b style="font-weight:500;color:var(--ink-gray-8)">Quality hold tracing.</b> <span class="qs">A fault at AT-401 holds product from every filler downstream of XV-301.</span></div></div></div>
</div></aside>'''
write('AssetFlow.dc.html', page('Process flow', shell('AssetFlow.dc.html', head, f'<div style="display:flex;flex:1;min-height:0">{main}{panel}</div>'), {"$preview": {"width": 1440, "height": 900}}))
