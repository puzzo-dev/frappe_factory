import re, sys, os
from render_dc import render
from playwright.sync_api import sync_playwright
os.makedirs('/home/claude/ff-design/shots', exist_ok=True)
names = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    for n in names:
        s = open(f'/home/claude/ff-design/project/{n}').read()
        w = int(re.search(r'"width": ?(\d+)', s).group(1)); h = int(re.search(r'"height": ?(\d+)', s).group(1))
        html = re.sub(r'<link[^>]*fonts.googleapis[^>]*>', '', render(s))
        pg = b.new_page(viewport={'width': w, 'height': h})
        pg.set_content(html)
        out = f'/home/claude/ff-design/shots/{n.replace(".dc.html","")}.png'
        pg.screenshot(path=out)
        print(out, pg.evaluate('document.documentElement.scrollHeight'))
    b.close()
