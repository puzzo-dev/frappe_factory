"""Refresh Main.dc.html (hand-written board) with the current shared sidebar and state wiring."""
import re, sys
from ff import sidebar, finalize
def skip_scif(s, i):
    # skip a balanced <sc-if>…</sc-if> starting at i
    depth = 0
    for m in re.finditer(r'<(/?)sc-if\b[^>]*>', s[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0: return i + m.end()
p = '../project/Main.dc.html'; s = open(p).read()
s = '\n'.join(l for l in s.split('\n') if '/*ff-wired*/' not in l).replace('ffBaseVals()', 'renderVals()', 1)
a = s.index('<nav class="side" aria-label="Plant">'); b = s.index('</nav>', a) + 6
while True:
    k = b
    while s[k:k+1] in ('\n', ' '): k += 1
    if s.startswith('<i data-ff-menu-default', k): k = s.index('</i>', k) + 4
    if s.startswith('<sc-if value="{{menuOpen}}"', k) or s.startswith('<sc-if value="{{is_plantsw__open}}"', k):
        b = skip_scif(s, k)
    else: break
s = s[:a] + sidebar('Main.dc.html', counts={'Alarms':'{{alarmCount}}','Interlock trips':'{{tripCount}}','Quality holds':'1','Downtime':'3'}) + s[b:]
open(p, 'w').write(finalize(s))
print('ok')
