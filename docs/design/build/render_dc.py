"""Crude local renderer for .dc.html boards: runs renderVals in node, expands sc-for / sc-if, fills holes."""
import re, json, subprocess, sys

def vals_for(src, props=None):
    script = re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>', src, re.S).group(1)
    dprops = json.loads(re.search(r"data-props='(.*?)'", src, re.S).group(1))
    p = {k: v.get('default') for k, v in dprops.items() if isinstance(v, dict) and 'default' in v}
    if props: p.update(props)
    js = "class DCLogic{constructor(){this.props=%s}}\n%s\nconsole.log(JSON.stringify(new Component().renderVals()))" % (json.dumps(p), script)
    out = subprocess.run(['node', '-e', js], capture_output=True, text=True)
    if out.returncode: raise SystemExit(out.stderr)
    return json.loads(out.stdout)

def get(ctx, path):
    cur = ctx
    for part in path.strip().split('.'):
        if isinstance(cur, dict): cur = cur.get(part)
        else: return ''
    return cur

def fill(html, ctx):
    # sc-for (innermost first, non-nested assumed)
    def rep_for(m):
        lst = get(ctx, m.group(1)); var = m.group(2); body = m.group(3)
        return ''.join(fill(body, dict(ctx, **{var: it})) for it in (lst or []))
    while '<sc-for' in html:
        html2 = re.sub(r'<sc-for list="\{\{([^}]+)\}\}" as="(\w+)"[^>]*>((?:(?!<sc-for).)*?)</sc-for>', rep_for, html, flags=re.S)
        if html2 == html: break
        html = html2
    def rep_if(m):
        return fill(m.group(2), ctx) if get(ctx, m.group(1)) else ''
    html = re.sub(r'<sc-if value="\{\{([^}]+)\}\}"[^>]*>(.*?)</sc-if>', rep_if, html, flags=re.S)
    html = re.sub(r'\{\{([^}]+)\}\}', lambda m: str(get(ctx, m.group(1)) if get(ctx, m.group(1)) is not None else ''), html)
    return html

def render(src, props=None):
    ctx = vals_for(src, props)
    helm = re.search(r'<helmet>(.*?)</helmet>', src, re.S).group(1)
    body = re.search(r'</helmet>(.*?)</x-dc>', src, re.S).group(1)
    return f'<!doctype html><html><head><meta charset="utf-8">{helm}</head><body>{fill(body, ctx)}</body></html>'
