"""Industry symbol packs: rice milling, edible oil and poultry farm. 48x48 boxes, ISA-101 style:
grey at rest, dark grey body when running, red outline on fault. Moving parts carry
class="spin" / "shake" so the plant screen animates them when running."""
G6 = 'var(--ink-gray-6)'; G4 = 'var(--ink-gray-4)'; W = 'var(--surface-base)'; R = 'var(--ink-red-7)'

def _c(run, fault=False):
    body = G6 if run else W
    part = W if run else G4
    edge = R if fault else G6
    return body, part, edge

# ---------- shared / handling ----------
def bucket_elevator(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<rect x="18" y="2" width="12" height="44" rx="2" fill="{W}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M21 6 v36 M27 6 v36" stroke="{G4}" stroke-dasharray="3 3" class="{"flow" if run else ""}"/>'
            f'<path d="M30 6 h10 l-4 6" fill="none" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M8 40 h10" stroke="{e}" stroke-width="1.5"/><circle cx="24" cy="6" r="3" fill="{b}" stroke="{e}"/>')
def silo(fill=0.6, fault=False):
    h = 28 * fill
    e = R if fault else G6
    return (f'<path d="M12 4 h24 v28 l-12 12 l-12 -12 z" fill="{W}" stroke="{e}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<clipPath id="sc{int(fill*100)}"><path d="M12 4 h24 v28 l-12 12 l-12 -12 z"/></clipPath>'
            f'<rect x="12" y="{44-h-8:.1f}" width="24" height="{h+8:.1f}" fill="var(--surface-gray-4)" clip-path="url(#sc{int(fill*100)})"/>')
def conveyor(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<rect x="4" y="20" width="40" height="10" rx="5" fill="{W}" stroke="{e}" stroke-width="1.5"/>'
            f'<circle cx="9" cy="25" r="3" fill="{b}" stroke="{e}"/><circle cx="39" cy="25" r="3" fill="{b}" stroke="{e}"/>'
            f'<path d="M12 21 h24" stroke="{G4}" stroke-dasharray="3 3" class="{"flow" if run else ""}"/>')
def screw_conveyor(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<rect x="4" y="18" width="40" height="12" rx="2" fill="{W}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M8 18 l4 12 l4 -12 l4 12 l4 -12 l4 12 l4 -12 l4 12 l4 -12" fill="none" stroke="{G6 if run else G4}"/>')
def cyclone(run=True, fault=False):
    e = R if fault else G6
    return (f'<path d="M14 6 h20 v12 l-7 20 h-6 l-7 -20 z" fill="{W}" stroke="{e}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M34 10 h8" stroke="{e}" stroke-width="1.5"/><path d="M21 38 v6 h6 v-6" fill="none" stroke="{e}" stroke-width="1.5"/>')
def fan(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<circle cx="24" cy="24" r="14" fill="{b}" stroke="{e}" stroke-width="1.5"/>'
            f'<g class="{"spin" if run else ""}"><path d="M24 24 l0 -10 a6 6 0 0 1 6 6 z M24 24 l10 0 a6 6 0 0 1 -6 6 z M24 24 l0 10 a6 6 0 0 1 -6 -6 z M24 24 l-10 0 a6 6 0 0 1 6 -6 z" fill="{p}"/></g>')
def bagger(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<path d="M14 4 h20 l-6 10 h-8 z" fill="{W}" stroke="{e}" stroke-width="1.5"/>'
            f'<rect x="12" y="14" width="24" height="14" rx="2" fill="{b}" stroke="{e}" stroke-width="1.5"/>'
            f'<text x="24" y="24" text-anchor="middle" font-size="7" font-weight="600" fill="{p}">kg</text>'
            f'<path d="M17 30 h14 l2 14 h-18 z" fill="{W}" stroke="{e}" stroke-width="1.5"/>')
def dryer(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<rect x="12" y="4" width="24" height="40" rx="3" fill="{W}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M12 14 h24 M12 24 h24 M12 34 h24" stroke="{G4}"/><path d="M4 30 h8 M36 18 h8" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M6 27 l3 3 l-3 3" fill="none" stroke="{"var(--ink-red-6, #e5484d)" if run else G4}" stroke-width="1.5"/>')

# ---------- rice milling ----------
def pre_cleaner(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<g class="{"shake" if run else ""}"><path d="M6 14 L42 22 L42 30 L6 22 Z" fill="{b}" stroke="{e}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M10 19 l28 6" stroke="{p}" stroke-dasharray="2 2"/></g>'
            f'<path d="M10 24 v16 M38 32 v8" stroke="{e}" stroke-width="1.5"/><path d="M18 6 h12 l-3 6 h-6 z" fill="{W}" stroke="{e}" stroke-width="1.3"/>')
def destoner(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<g class="{"shake" if run else ""}"><path d="M6 30 L42 16 L42 22 L6 36 Z" fill="{b}" stroke="{e}" stroke-width="1.5" stroke-linejoin="round"/></g>'
            f'<path d="M12 36 v8 M36 24 v20" stroke="{e}" stroke-width="1.5"/><circle cx="40" cy="12" r="2.5" fill="{G4}"/><circle cx="35" cy="10" r="2" fill="{G4}"/>')
def husker(run=True, fault=False):
    b, p, e = _c(run, fault)
    sp = 'spin' if run else ''
    return (f'<rect x="8" y="12" width="32" height="26" rx="3" fill="{W}" stroke="{e}" stroke-width="1.5"/>'
            f'<g class="{sp}"><circle cx="19" cy="25" r="7" fill="{b}" stroke="{e}"/><path d="M19 19 v12" stroke="{p}"/></g>'
            f'<g class="{sp}"><circle cx="29" cy="25" r="7" fill="{b}" stroke="{e}"/><path d="M23 25 h12" stroke="{p}"/></g>'
            f'<path d="M20 4 h8 v8 h-8 z" fill="{W}" stroke="{e}" stroke-width="1.3"/><path d="M24 38 v6" stroke="{e}" stroke-width="1.5"/>')
def paddy_separator(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<g class="{"shake" if run else ""}"><rect x="6" y="14" width="36" height="20" rx="2" fill="{b}" stroke="{e}" stroke-width="1.5" transform="rotate(-8 24 24)"/>'
            f'<path d="M10 20 h28 M10 25 h28 M10 30 h28" stroke="{p}" transform="rotate(-8 24 24)"/></g>'
            f'<path d="M10 38 v6 M24 38 v6 M38 34 v10" stroke="{e}" stroke-width="1.5"/>')
def whitener(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<path d="M18 4 h12 l-2 6 h-8 z" fill="{W}" stroke="{e}" stroke-width="1.3"/>'
            f'<rect x="14" y="10" width="20" height="28" rx="4" fill="{b}" stroke="{e}" stroke-width="1.5"/>'
            f'<g class="{"spin" if run else ""}"><circle cx="24" cy="24" r="6" fill="none" stroke="{p}" stroke-width="1.5"/><path d="M24 18 v12 M18 24 h12" stroke="{p}"/></g>'
            f'<path d="M24 38 v6 M34 30 h8" stroke="{e}" stroke-width="1.5"/>')
def grader(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<g class="{"shake" if run else ""}"><rect x="6" y="10" width="36" height="24" rx="2" fill="{b}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M6 18 h36 M6 26 h36" stroke="{p}" stroke-dasharray="3 2"/></g>'
            f'<path d="M12 34 v10 M24 34 v10 M36 34 v10" stroke="{e}" stroke-width="1.5"/>')
def color_sorter(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<path d="M14 4 h20 l-4 8 h-12 z" fill="{W}" stroke="{e}" stroke-width="1.3"/>'
            f'<rect x="10" y="12" width="28" height="26" rx="3" fill="{b}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M16 25 q8 -8 16 0 q-8 8 -16 0z" fill="none" stroke="{p}" stroke-width="1.5"/><circle cx="24" cy="25" r="2.5" fill="{p}"/>'
            f'<path d="M18 38 v6 M32 38 l6 6" stroke="{e}" stroke-width="1.5"/>')

# ---------- edible oil ----------
def cooker(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<rect x="10" y="10" width="28" height="30" rx="4" fill="{b}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M24 4 v28" stroke="{e}" stroke-width="1.5"/><g class="{"spin" if run else ""}"><path d="M16 30 h16" stroke="{p}" stroke-width="2"/></g>'
            f'<path d="M14 18 h20 M14 22 h20" stroke="{p}" stroke-dasharray="2 2"/><path d="M38 34 h6" stroke="{e}" stroke-width="1.5"/>')
def expeller(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<path d="M6 6 h12 l-3 8 h-6 z" fill="{W}" stroke="{e}" stroke-width="1.3"/>'
            f'<rect x="4" y="14" width="40" height="14" rx="3" fill="{b}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M8 14 l3 14 l3 -14 l3 14 l3 -14 l3 14 l3 -14 l3 14 l3 -14 l3 14 l3 -14" fill="none" stroke="{p}" class="{"flow" if run else ""}"/>'
            f'<path d="M20 28 v8 M14 40 h12" stroke="{e}" stroke-width="1.5"/><path d="M44 21 h-0" stroke="{e}"/><path d="M40 28 l4 8" stroke="{e}" stroke-width="1.5"/>')
def filter_press(run=True, fault=False):
    b, p, e = _c(run, fault)
    plates = ''.join(f'<rect x="{10+i*5}" y="12" width="4" height="22" rx="1" fill="{b}" stroke="{e}"/>' for i in range(6))
    return (f'<rect x="4" y="10" width="4" height="26" fill="{G6}"/><rect x="40" y="10" width="4" height="26" fill="{G6}"/>{plates}'
            f'<path d="M4 38 h40" stroke="{e}" stroke-width="1.5"/><path d="M24 34 v10" stroke="{e}" stroke-width="1.5"/>')
def reactor(run=True, fault=False, tag=''):
    b, p, e = _c(run, fault)
    t = f'<text x="24" y="31" text-anchor="middle" font-size="7" font-weight="600" fill="{p}">{tag}</text>' if tag else ''
    return (f'<path d="M12 10 h24 v22 a12 8 0 0 1 -24 0 z" fill="{b}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M24 2 v16" stroke="{e}" stroke-width="1.5"/><g class="{"spin" if run else ""}"><path d="M17 18 h14" stroke="{p}" stroke-width="2"/></g>{t}'
            f'<path d="M24 40 v6" stroke="{e}" stroke-width="1.5"/>')
def column(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<rect x="16" y="2" width="16" height="42" rx="8" fill="{b}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M18 12 h12 M18 20 h12 M18 28 h12 M18 36 h12" stroke="{p}"/><path d="M32 8 h10" stroke="{e}" stroke-width="1.5"/>')
def heat_exchanger(run=True, fault=False):
    e = R if fault else G6
    return (f'<circle cx="24" cy="24" r="14" fill="{W}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M10 24 l6 -6 l6 12 l6 -12 l6 12 l4 -6" fill="none" stroke="{e}" stroke-width="1.5"/>')
def bottle_filler(run=True, fault=False):
    b, p, e = _c(run, fault)
    bottles = ''.join(f'<path d="M{8+i*12} 44 v-12 l2 -4 v-4 h4 v4 l2 4 v12 z" fill="{W}" stroke="{e}"/>' for i in range(3))
    return (f'<rect x="4" y="4" width="40" height="14" rx="2" fill="{b}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M12 18 v4 M24 18 v4 M36 18 v4" stroke="{e}" stroke-width="1.5"/>{bottles}')

RICE = [('Pre-cleaner', pre_cleaner), ('Destoner', destoner), ('Husker', husker), ('Paddy separator', paddy_separator),
        ('Whitener', whitener), ('Grader', grader), ('Color sorter', color_sorter), ('Dryer', dryer)]
OIL = [('Cooker', cooker), ('Expeller', expeller), ('Filter press', filter_press), ('Neutralizer', lambda r=True, f=False: reactor(r, f, '')),
       ('Deodorizer', column), ('Heat exchanger', heat_exchanger), ('Bottle filler', bottle_filler)]
GENERAL = [('Bucket elevator', bucket_elevator), ('Silo', lambda r=True, f=False: silo(0.6, f)), ('Belt conveyor', conveyor),
           ('Screw conveyor', screw_conveyor), ('Cyclone', cyclone), ('Fan', fan), ('Bagger', bagger)]

# ---------- poultry farm (layers) ----------
def poultry_house(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<path d="M4 22 L24 8 L44 22 V42 H4 Z" fill="{W}" stroke="{e}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M10 30 h28 M10 36 h28" stroke="{G4}" stroke-dasharray="2 2"/>'
            f'<circle cx="38" cy="18" r="0" /><rect x="8" y="24" width="6" height="4" fill="{b}" stroke="{e}"/>')
def feeder_line(run=True, fault=False):
    b, p, e = _c(run, fault)
    pans = ''.join(f'<path d="M{6+i*10} 30 q4 8 8 0" fill="{W}" stroke="{e}"/>' for i in range(4))
    return (f'<path d="M4 18 H44" stroke="{e}" stroke-width="1.5"/>{pans}'
            f'<path d="M10 18 v12 M20 18 v12 M30 18 v12 M40 18 v12" stroke="{G4}"/>'
            f'<path d="M6 16 h36" stroke="{G4}" stroke-dasharray="3 3" class="{"flow" if run else ""}"/>')
def drinker_line(run=True, fault=False):
    e = R if fault else G6
    drops = ''.join(f'<path d="M{10+i*10} 24 v5 M{10+i*10} 33 q-2 3 0 5 q2 -2 0 -5" fill="{"var(--surface-gray-4)"}" stroke="{e}"/>' for i in range(4))
    return f'<path d="M4 22 H44" stroke="{e}" stroke-width="2"/><rect x="2" y="14" width="8" height="10" rx="1" fill="{W}" stroke="{e}"/>{drops}'
def exhaust_fan(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<rect x="6" y="6" width="36" height="36" rx="3" fill="{W}" stroke="{e}" stroke-width="1.5"/><circle cx="24" cy="24" r="14" fill="none" stroke="{e}"/>'
            f'<g class="{"spin" if run else ""}"><path d="M24 24 L24 12 A6 6 0 0 1 30 18 Z M24 24 L36 24 A6 6 0 0 1 30 30 Z M24 24 L24 36 A6 6 0 0 1 18 30 Z M24 24 L12 24 A6 6 0 0 1 18 18 Z" fill="{b}" stroke="{e}"/></g>')
def cooling_pad(run=True, fault=False):
    e = R if fault else G6
    waves = ''.join(f'<path d="M{10+i*7} 8 q3 5 0 10 q-3 5 0 10 q3 5 0 10" fill="none" stroke="{G6 if run else G4}"/>' for i in range(5))
    return f'<rect x="6" y="6" width="36" height="36" rx="2" fill="{W}" stroke="{e}" stroke-width="1.5"/>{waves}'
def brooder(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<path d="M10 14 h28 l-6 12 h-16 z" fill="{b}" stroke="{e}" stroke-width="1.5" stroke-linejoin="round"/><path d="M24 4 v10" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M16 32 q2 4 0 8 M24 32 q2 4 0 8 M32 32 q2 4 0 8" fill="none" stroke="{G6 if run else G4}"/>')
def hammer_mill(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<path d="M14 4 h20 l-4 8 h-12 z" fill="{W}" stroke="{e}" stroke-width="1.5"/><circle cx="24" cy="26" r="13" fill="{W}" stroke="{e}" stroke-width="1.5"/>'
            f'<g class="{"spin" if run else ""}"><path d="M24 26 L24 15 M24 26 L33 31 M24 26 L15 31" stroke="{b if run else G4}" stroke-width="3" stroke-linecap="round"/></g><path d="M20 39 v6 h8 v-6" fill="none" stroke="{e}" stroke-width="1.5"/>')
def ribbon_mixer(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<path d="M6 16 h36 v14 a8 8 0 0 1 -8 8 h-20 a8 8 0 0 1 -8 -8 z" fill="{W}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M10 26 c4 -6 8 6 12 0 s8 6 12 0 s6 4 6 0" fill="none" stroke="{G6 if run else G4}" stroke-width="1.5"/><path d="M4 26 h4 M40 26 h4" stroke="{e}" stroke-width="1.5"/><rect x="18" y="8" width="12" height="8" fill="{b}" stroke="{e}"/>')
def egg_conveyor(run=True, fault=False):
    b, p, e = _c(run, fault)
    eggs = ''.join(f'<ellipse cx="{10+i*9}" cy="20" rx="3" ry="4" fill="{W}" stroke="{e}"/>' for i in range(4))
    return (f'<rect x="4" y="24" width="40" height="8" rx="4" fill="{W}" stroke="{e}" stroke-width="1.5"/>{eggs}'
            f'<circle cx="9" cy="28" r="2" fill="{b}"/><circle cx="39" cy="28" r="2" fill="{b}"/><path d="M12 28 h24" stroke="{G4}" stroke-dasharray="3 3" class="{"flow" if run else ""}"/>')
def egg_grader(run=True, fault=False):
    b, p, e = _c(run, fault)
    return (f'<rect x="4" y="10" width="40" height="22" rx="2" fill="{b}" stroke="{e}" stroke-width="1.5"/>'
            + ''.join(f'<ellipse cx="{12+i*8}" cy="21" rx="2.5" ry="3.5" fill="{W}" stroke="{e}"/>' for i in range(4)) +
            f'<path d="M10 32 v8 M24 32 v8 M38 32 v8" stroke="{e}" stroke-width="1.5"/><path d="M6 42 h36" stroke="{e}" stroke-width="1.5"/>')
def egg_packer(run=True, fault=False):
    b, p, e = _c(run, fault)
    cells = ''.join(f'<circle cx="{11+(i%5)*6.5:.1f}" cy="{20+(i//5)*7}" r="2.4" fill="{W if i < 7 or not run else b}" stroke="{e}"/>' for i in range(15))
    return f'<rect x="5" y="14" width="38" height="20" rx="2" fill="{W}" stroke="{e}" stroke-width="1.5"/>{cells}<path d="M5 38 h38" stroke="{e}" stroke-width="1.5"/>'
def cold_room(run=True, fault=False):
    e = R if fault else G6
    return (f'<rect x="6" y="6" width="36" height="36" rx="2" fill="{W}" stroke="{e}" stroke-width="1.5"/>'
            f'<path d="M24 14 v20 M15 19 l18 10 M33 19 l-18 10" stroke="{G6 if run else G4}" stroke-width="1.5" stroke-linecap="round"/>')

POULTRY = [('Layer house', poultry_house), ('Feeder line', feeder_line), ('Drinker line', drinker_line), ('Tunnel fan', exhaust_fan),
           ('Cooling pad', cooling_pad), ('Brooder', brooder), ('Hammer mill', hammer_mill), ('Ribbon mixer', ribbon_mixer),
           ('Egg conveyor', egg_conveyor), ('Egg grader', egg_grader), ('Egg packer', egg_packer), ('Cold room', cold_room)]
