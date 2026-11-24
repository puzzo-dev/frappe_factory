import re, sys, os, json, glob
sys.path.insert(0, '/home/claude/ff-design/build')
from render_dc import render
from playwright.sync_api import sync_playwright
JS = r'''() => {
 const W = innerWidth, H = innerHeight;
 const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
   return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && r.top < H && r.left < W && r.bottom > 0 && r.right > 0; };
 const cv = document.createElement('canvas'); cv.width = cv.height = 1; const cx = cv.getContext('2d', {willReadFrequently: true});
 const rgba = c => { if (/rgba?\(0, 0, 0, 0\)|transparent/.test(c)) return null; cx.clearRect(0,0,1,1); cx.fillStyle = '#000'; cx.fillStyle = c; cx.fillRect(0,0,1,1); const d = cx.getImageData(0,0,1,1).data; return [d[0], d[1], d[2], d[3]/255]; };
 const lum = c => { const m = rgba(c); if (!m) return null; const [r,g,b,a] = m; if (a === 0) return null;
   const f = v => { v/=255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4) }; return [0.2126*f(r)+0.7152*f(g)+0.0722*f(b), a ?? 1]; };
 const bgOf = el => { while (el) { const c = getComputedStyle(el).backgroundColor; const l = lum(c); if (l && l[1] > .5) return l[0]; el = el.parentElement; } return 1; };
 const out = { small: [], lowc: [], trunc: [], offright: [], primary: [], emoji: [], lorem: [], smalltap: [] };
 const texts = [];
 const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
 while (walker.nextNode()) { const t = walker.currentNode; const s = t.textContent.trim(); if (!s) continue; const el = t.parentElement; if (!el || el.closest('svg')) continue; if (!vis(el)) continue; texts.push([el, s]); }
 const seen = new Set();
 for (const [el, s] of texts) {
   if (seen.has(el)) continue; seen.add(el);
   const cs = getComputedStyle(el); const fs = parseFloat(cs.fontSize);
   if (fs <= 12 && !/^[A-Z0-9 ·]+$/.test(s)) out.small.push(fs + 'px ' + s.slice(0, 40));
   const fg = lum(cs.color); if (fg) { const bg = bgOf(el); const L1 = Math.max(fg[0], bg), L2 = Math.min(fg[0], bg); const cr = (L1 + .05) / (L2 + .05);
     const big = fs >= 18 || (fs >= 14 && parseInt(cs.fontWeight) >= 700); if (cr < (big ? 3 : 4.5)) out.lowc.push(cr.toFixed(2) + ' ' + fs + 'px ' + s.slice(0, 40)); }
   if (/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u.test(s)) out.emoji.push(s.slice(0, 40));
   if (/lorem|ipsum|Item \d\b/i.test(s)) out.lorem.push(s.slice(0, 40));
 }
 for (const el of document.querySelectorAll('body *')) { if (!vis(el) || el.closest('svg')) continue; const cs = getComputedStyle(el);
   if (el.children.length === 0 && el.textContent.trim() && el.scrollWidth > el.clientWidth + 2 && cs.overflow !== 'visible') out.trunc.push(el.textContent.trim().slice(0, 40));
   const r = el.getBoundingClientRect(); if (r.right > W + 2 && cs.position !== 'fixed' && !el.closest('[style*="overflow"]')) out.offright.push(el.tagName + ' ' + (el.className||'') + ' ' + el.textContent.trim().slice(0, 30));
 }
 const ov = [...document.querySelectorAll('.dialog,.ffov,[role=dialog]')].filter(vis).length > 0;
 for (const el of document.querySelectorAll('.btn.solid, .kb.solid, button.solid, a.solid')) if (vis(el)) out.primary.push(el.textContent.trim().slice(0, 30));
 for (const el of document.querySelectorAll('.kb, .ktile, a.kb')) { if (!vis(el)) continue; const r = el.getBoundingClientRect(); if (r.height < 44) out.smalltap.push(Math.round(r.height) + 'px ' + el.textContent.trim().slice(0, 20)); }
 // fit: lowest visible content in main area
 let bottom = 0; for (const el of document.querySelectorAll('main *')) { if (!vis(el)) continue; const r = el.getBoundingClientRect(); if (el.children.length === 0 && r.bottom > bottom && r.bottom <= H + 1) bottom = r.bottom; }
 out.emptyBottom = Math.round((H - bottom) / H * 100); out.dialog = ov;
 return out;
}'''
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for f in sorted(glob.glob('/home/claude/ff-design/project/*.dc.html')):
        n = os.path.basename(f)[:-8]; s = open(f).read()
        w = int(re.search(r'"width": ?(\d+)', s).group(1)); h = int(re.search(r'"height": ?(\d+)', s).group(1))
        pg = b.new_page(viewport={'width': w, 'height': h})
        pg.set_content(re.sub(r'<link[^>]*fonts.googleapis[^>]*>', '', render(s)))
        pg.screenshot(path=f'/home/claude/ff-review/shots/{n}.png') if os.path.isdir('/home/claude/ff-review/shots') else None
        res[n] = pg.evaluate(JS); pg.close()
    b.close()
json.dump(res, open('/home/claude/ff-review/audit.json', 'w'), indent=1)
for n, r in res.items():
    print(f"{n:22} small={len(r['small']):3} lowc={len(r['lowc']):3} trunc={len(r['trunc']):2} off={len(r['offright']):2} primary={len(r['primary'])} emoji={len(r['emoji'])} tap<44={len(r['smalltap'])} emptyBottom={r['emptyBottom']}%")
