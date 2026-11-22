from ff import *

def plant_bg():
    """A quiet stand-in for the page behind a dialog: shell + header + empty body."""
    head = header(crumb(('Plants','Plants.dc.html'),('Koyo 1','Main.dc.html'),('Treatment and filling',None)),
                  f'<span class="bd gray"><span class="dot g"></span>Live · 2 s</span>{btn("Edit layout","pen")}')
    body = '<div class="body"><div style="height:120px;border-radius:12px;background:var(--surface-gray-1)"></div><div style="height:520px;border-radius:12px;border:1px solid var(--outline-gray-1)"></div></div>'
    return shell('Settings.dc.html', head, body)
