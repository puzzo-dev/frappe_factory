"""Small ISA-101 style symbol drawings shared by the layout editor and the symbol library.
Each returns SVG markup in a 48x48 box. Gray first; colour only for state."""
G6 = 'var(--ink-gray-6)'; G4 = 'var(--ink-gray-4)'; W = 'var(--surface-base)'

def tank_v(fill=0.6, st=G6):
    h = 34 * fill
    return f'<rect x="12" y="6" width="24" height="36" rx="5" fill="{W}" stroke="{st}" stroke-width="1.5"/><rect x="13" y="{41-h:.1f}" width="22" height="{h:.1f}" rx="3" fill="var(--surface-gray-4)"/>'
def tank_h():
    return f'<rect x="4" y="14" width="40" height="20" rx="10" fill="{W}" stroke="{G6}" stroke-width="1.5"/><rect x="6" y="24" width="36" height="8" rx="4" fill="var(--surface-gray-4)"/>'
def pump(run=True):
    f = G6 if run else W; i = W if run else G4
    return f'<circle cx="24" cy="24" r="13" fill="{f}" stroke="{G6}" stroke-width="1.5"/><path d="M24 11 H40" fill="none" stroke="{G6}" stroke-width="1.5"/><path d="M18 31 L24 17 L30 31 Z" fill="{i}"/><path d="M14 41 h20" stroke="{G6}" stroke-width="1.5"/>'
def dosing():
    return f'<rect x="12" y="14" width="24" height="22" rx="3" fill="{W}" stroke="{G6}" stroke-width="1.5"/><path d="M18 25 h12 M24 19 v12" stroke="{G6}" stroke-width="1.5"/><path d="M24 14 V6" stroke="{G6}" stroke-width="1.5"/>'
def valve(open_=True):
    f = W if open_ else G6
    return f'<path d="M8 16 L24 24 L8 32 Z M40 16 L24 24 L40 32 Z" fill="{f}" stroke="{G6}" stroke-width="1.5" stroke-linejoin="round"/><path d="M24 24 V12 M18 12 h12" stroke="{G6}" stroke-width="1.5"/>'
def valve3():
    return f'<path d="M6 18 L24 26 L6 34 Z M42 18 L24 26 L42 34 Z M16 44 L24 26 L32 44 Z" fill="{W}" stroke="{G6}" stroke-width="1.5" stroke-linejoin="round"/><path d="M24 26 V10 M18 10 h12" stroke="{G6}" stroke-width="1.5"/>'
def check():
    return f'<path d="M6 24 H42" stroke="{G6}" stroke-width="1.5"/><path d="M16 14 L32 24 L16 34 Z" fill="{W}" stroke="{G6}" stroke-width="1.5"/><path d="M32 14 V34" stroke="{G6}" stroke-width="1.5"/>'
def mmf():
    return f'<rect x="14" y="4" width="20" height="40" rx="10" fill="{W}" stroke="{G6}" stroke-width="1.5"/><path d="M15 22 h18 M15 28 h18 M15 34 h18" stroke="{G4}" stroke-dasharray="2 2"/>'
def cart():
    return f'<rect x="16" y="8" width="16" height="34" rx="3" fill="{W}" stroke="{G6}" stroke-width="1.5"/><path d="M20 12 v26 M24 12 v26 M28 12 v26" stroke="{G4}"/>'
def ro():
    return f'<rect x="4" y="12" width="40" height="10" rx="5" fill="{W}" stroke="{G6}" stroke-width="1.5"/><rect x="4" y="27" width="40" height="10" rx="5" fill="{W}" stroke="{G6}" stroke-width="1.5"/><path d="M8 17 h32 M8 32 h32" stroke="{G4}" stroke-dasharray="3 2"/>'
def uv():
    return f'<rect x="4" y="16" width="40" height="16" rx="8" fill="{W}" stroke="{G6}" stroke-width="1.5"/><path d="M10 24 h28" stroke="var(--ink-violet-6, {G6})" stroke-width="2.5" stroke-linecap="round"/>'
def ix():
    return f'<rect x="15" y="4" width="18" height="40" rx="9" fill="{W}" stroke="{G6}" stroke-width="1.5"/><g fill="{G4}"><circle cx="21" cy="18" r="1.4"/><circle cx="27" cy="22" r="1.4"/><circle cx="21" cy="26" r="1.4"/><circle cx="27" cy="30" r="1.4"/><circle cx="21" cy="34" r="1.4"/></g>'
def analyser(tag='AT'):
    return f'<circle cx="24" cy="24" r="15" fill="{W}" stroke="{G6}" stroke-width="1.5"/><path d="M9 24 h30" stroke="{G6}"/><text x="24" y="21" text-anchor="middle" font-size="9" font-weight="600" fill="var(--ink-gray-8)">{tag}</text><text x="24" y="33" text-anchor="middle" font-size="8" fill="var(--ink-gray-6)">401</text>'
def level():
    return f'<circle cx="24" cy="24" r="15" fill="{W}" stroke="{G6}" stroke-width="1.5"/><path d="M9 24 h30" stroke="{G6}"/><text x="24" y="21" text-anchor="middle" font-size="9" font-weight="600" fill="var(--ink-gray-8)">LT</text><text x="24" y="33" text-anchor="middle" font-size="8" fill="var(--ink-gray-6)">401</text>'
def flow():
    return f'<rect x="10" y="16" width="28" height="16" rx="3" fill="{W}" stroke="{G6}" stroke-width="1.5"/><path d="M4 24 h6 M38 24 h6" stroke="{G6}" stroke-width="1.5"/><text x="24" y="28" text-anchor="middle" font-size="9" font-weight="600" fill="var(--ink-gray-8)">FT</text>'
def filler(run=True):
    b = G6 if run else W; p = W if run else G4
    return f'<path d="M15 4 h18 l-4 7 h-10 z" fill="{W}" stroke="{G6}" stroke-width="1.3"/><rect x="11" y="11" width="26" height="32" rx="3" fill="{b}" stroke="{G6}" stroke-width="1.5"/><circle cx="24" cy="20" r="5" fill="none" stroke="{p}" stroke-width="1.5"/><path d="M19 30 h4 M25 30 h4" stroke="{p}" stroke-width="2"/><rect x="21" y="34" width="6" height="6" rx="1" fill="{p}"/>'
def generator():
    return f'<rect x="6" y="12" width="36" height="24" rx="3" fill="{W}" stroke="{G6}" stroke-width="1.5"/><circle cx="24" cy="24" r="7" fill="none" stroke="{G6}" stroke-width="1.5"/><path d="M21 24 q1.5 -3 3 0 t3 0" fill="none" stroke="{G6}" stroke-width="1.3"/>'

def box(inner, size=48, label=None):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" style="display:block">{inner}</svg>'

# ---- Power (utilities)
def grid_in():
    return f'<path d="M24 4 L14 22 H34 Z" fill="{W}" stroke="{G6}" stroke-width="1.5"/><path d="M18 22 L14 44 M30 22 L34 44 M16 32 H32 M24 22 V44" stroke="{G6}" stroke-width="1.3" fill="none"/>'
def meter():
    return f'<circle cx="24" cy="24" r="14" fill="{W}" stroke="{G6}" stroke-width="1.5"/><text x="24" y="28" text-anchor="middle" font-size="10" font-weight="600" fill="var(--ink-gray-8)">kWh</text>'
def breaker(closed=True):
    arm = 'M24 30 L24 18' if closed else 'M24 30 L33 19'
    return f'<path d="M24 4 V16 M24 32 V44" stroke="{G6}" stroke-width="1.5"/><circle cx="24" cy="17" r="2" fill="{G6}"/><circle cx="24" cy="31" r="2" fill="{G6}"/><path d="{arm}" stroke="{G6}" stroke-width="2"/>'
def ats(on_gen=True):
    arm = 'M24 30 L15 18' if on_gen else 'M24 30 L33 18'
    return f'<rect x="4" y="6" width="40" height="36" rx="4" fill="{W}" stroke="{G6}" stroke-width="1.5"/><circle cx="15" cy="16" r="2" fill="{G6}"/><circle cx="33" cy="16" r="2" fill="{G6}"/><circle cx="24" cy="31" r="2" fill="{G6}"/><path d="{arm}" stroke="var(--ink-amber-7)" stroke-width="2"/><text x="24" y="40" text-anchor="middle" font-size="7" fill="var(--ink-gray-6)">ATS</text>'
def db():
    return f'<rect x="10" y="6" width="28" height="36" rx="2" fill="{W}" stroke="{G6}" stroke-width="1.5"/><path d="M15 14 H33 M15 20 H33 M15 26 H33 M15 32 H33" stroke="{G4}" stroke-width="1.5"/>'
