# Screen design sources

- `boards/` — the 62 screen boards (`*.dc.html`) and `canvas.json`, as published in [Frappe Factory — screens](https://claude.ai/artifact/8NiCgasgTHvjFr3z7civXz). `Main.dc.html` is hand-written (its sidebar and CSS come from `ff.py`); the rest are generated.
- `build/` — Python that generates the other boards. `ff.py` holds the shared frappe-ui shell and the CSS that mirrors frappe-ui 1.0 tokens and components (Button, Badge, TextInput, List, Tabs, Dialog, Switch); `symbols.py` holds the HMI symbol drawings; `s_*.py` builds one screen each.
- Regenerate: `cd build && python3 s_alarms.py` (writes into `../boards`). `shot.py` renders PNGs with Playwright for `docs/images/screens/`.

These are design references for the code agent, not app code. The real screens are Vue components built with frappe-ui; class names here (`.si`, `.lr`, `.bd`) map to `SidebarItem`, `ListRow`, `Badge`.
