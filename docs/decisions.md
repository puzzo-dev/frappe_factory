# Frappe Factory — Decision record

Decisions taken during architecture planning, 22 Nov 2026, with the reasons. Newest decisions are at the bottom of each section.

## D1 · Scope and product shape

- **Decision:** Frappe Factory becomes a full factory operations app (MES layer) on top of ERPNext, not only an IoT bridge.
- **Frontend:** Vue 3 + frappe-ui single-page app at `/factory` (control room, floor kiosk, manager shells). Desk stays for admins.
- **Frappe versions:** v15 and v16 both supported from one branch. Cost: about 10–15% extra effort per feature; reviewed after phase 3.

## D2 · IoT layer: own thin layer, ThingsBoard optional

- **Decision:** Build our own thin IoT layer from existing open-source parts (OpsEdge Agent, Mosquitto, TimescaleDB, pymodbus, asyncua). Keep ThingsBoard behind a connector interface so a site can use ThingsBoard or direct Frappe ingestion.
- **Why not ThingsBoard as the core:**
  - ThingsBoard 4.4 (released 29 Sept 2026) moved to BSL 1.1. Free commercial use is limited to 100 devices on one server with ThingsBoard branding visible; white-labeling and more devices need a paid licence per customer organization. Older Apache 2.0 releases (≤ 4.3) get security updates only until 20 July 2027.
  - Java runtime needs at least 4 GB RAM for ThingsBoard + PostgreSQL, on the same edge box as Frappe, MariaDB and Redis.
  - Two sources of truth for devices, alarms and users.
- **Why not "everything from scratch":** we never write a broker, protocol drivers or a time-series engine. We write the glue, domain logic, alarm lifecycle and screens. Hard parts we own: store-and-forward with ordered backfill, device credentials, time sync, alarm deduplication, acknowledge and shelving.
- **Clarification (user):** "from scratch" meant owning the IoT layer built from existing packages, not writing every component. The user architects, designs and guides; the code agent writes the code.

## D3 · Safety interlocks stay outside software

- **Decision:** The lead trip (and any safety trip) is a hardwired or PLC interlock. Frappe Factory observes, records, alarms and runs the recovery workflow (re-purify the slug, re-test, sign-off). It never sits in the trip path and never sends a reset to a safety circuit.

## D4 · Handling the volume of operational data

- **Decision:** Raw telemetry never goes into MariaDB. Five tiers: raw readings and rollups in TimescaleDB; summaries, events and business documents in Frappe.
- **How Desk still shows raw data:** a Virtual DocType (`Machine Telemetry`) reads TimescaleDB. Verified present in Frappe v15.
- **Log tables in Frappe:** registered with `default_log_clearing_doctypes` and Frappe's Log Settings (verified in v15), autoincrement naming, tracking off, composite indexes, bulk inserts.
- **Not used:** MariaDB partitioning (conflicts with Frappe's `name` primary key).
- **Example scale:** 60 tags at 1 s = ~5.2M raw rows/day (TimescaleDB), ~86k 1-minute rollups/day, tens to hundreds of Frappe rows/day.

## D5 · Choices made on 22 Nov 2026

| Topic | Decision |
| --- | --- |
| Time-series database | TimescaleDB |
| Notifications | Frappe Notification (in-app, email) + WhatsApp via `frappe_whatsapp_openwa` |
| Pilot site | Koyo 10-head sachet water plant |
| PLC / protocol | Not chosen yet; driver layer supports Modbus TCP, Modbus RTU, OPC UA |
| Control | Monitor-only in release 1; command groundwork built and disabled behind three switches |
| Charts | frappe-ui charts, which run on Apache ECharts 6 (Frappe Charts only for Desk dashboard charts) |
| Licence | Commercial licence owned by I-Varse Technologies |

## D6 · SCADA and HMI

- **Decision:** No off-the-shelf SCADA. Frappe Factory is the SCADA: agent (data acquisition), MQTT (transport), TimescaleDB (historian), alarm engine, SVG mimic (HMI), command groundwork (supervisory control, off in R1). Details in [scada-hmi.md](scada-hmi.md).
- **Considered:** FUXA (MIT, but a second system beside Frappe), Ignition/AVEVA (per-site licences), ThingsBoard (licence change). A customer's existing SCADA is supported as a data source through the connector interface.
- **HMI style:** ISA-101 high-performance HMI.

## D7 · Symbol library for many customers

- **Proposal:** One shared symbol library (about 40 ISA-101 symbols drawn in-house), auto-generated mimics from the plant model, industry templates, a designer, and custom SVG upload with a naming convention. Library mastered on OpsCloud and pulled by edge sites.
- **Approved (22 Nov 2026):** the `HMI Symbol` record type (with Port and Binding child tables), linked from Plant Floor Widget (`symbol`, pinned version) and Plant Asset (`default_symbol`). Versioned, sanitized on upload, shipped as fixtures, mastered on OpsCloud. Spec in [trd.md](trd.md#hmi-symbol-library).
- **Approved 22 Nov 2026:** `Process Template`.
- **Approved 22 Nov 2026:** process flow (feeds into), stored as one `Process Flow` per plant with `Process Flow Link` rows.

## Licensing flags (for legal review)

These are flags, not legal advice.

- ERPNext is GPL-3.0; whether Frappe Factory is a derivative work when shipped on an OpsEdge box needs a legal opinion.
- `frappe_whatsapp_openwa` declares AGPL-3.0 in its `hooks.py`; as I-Varse's own app it can be relicensed if all its code is I-Varse's.
- TimescaleDB features used (compression, continuous aggregates, retention) are under the Timescale License: fine inside a product, not as a hosted database service. Use the TSL build.
- The repo still says MIT in `license.txt`, `hooks.py` and `pyproject.toml`; these change when the build starts.

## 22 Nov 2026 · standalone, ERPNext and kiosk

| Decision | Choice | Why |
| --- | --- | --- |
| Standalone | Frappe Factory runs on plain Frappe and does everything ThingsBoard does. Production runs, OEE against work orders, stock and quality need ERPNext | Manufacturing needs items, BOMs, stock and costing; rebuilding them would duplicate ERPNext and drift |
| ERPNext link | Same site or another site (URL, API key and secret), like Frappe CRM and Helpdesk; each link is its own switch | Companies that already run ERPNext elsewhere can still connect |
| Other ERPs | Frappe REST API with keys the Factory Manager creates, plus Frappe Webhooks; no built-in adapters | Keeps the product neutral; their middleware does the mapping |
| Name clash | Our Downtime Entry is renamed Machine Stop | ERPNext already has Downtime Entry and Plant Floor; DocType names are unique per site |
| Kiosk | Full-screen station app like ERPNext POS: Kiosk Profile with assigned users, Kiosk Session opened by a Floor Supervisor, sign-in with the user's own Frappe login (no kiosk PIN), Line, Maintenance and Quality views, registered tablet | Role alone would let any operator use any kiosk; assignment ties people to a station |
| Process Template | Approved as a DocType. One per industry: units of count, symbol pack, asset types, tag templates, alarm and interlock definitions, quality hold templates, downtime reasons, kiosk views, KPIs and a starter layout. I-Varse ships water, rice milling, edible oil, poultry farm and blank. A new plant copies it; the plant's layout is then edited on its own | Every industry starts with a working setup on day one, and template changes never alter running plants |
| API access | No integration role and no key management in the app. API keys are Frappe's own, per user; a key carries its user's roles and plant permissions (a Floor Supervisor's key sees their floor, a manager's sees all plants). Keeping keys safe is each user's job, as with their password | Frappe's users and roles already do this; a second mechanism would only duplicate it |
| Maintenance Technician | Uses the Maintenance kiosk view: equipment status, own jobs, equipment alarms, fault reports, spare-part requests | Responds to faults from the floor without a desk |
| Editing flows and layouts | The Factory Manager edits directly. Every lower role changes a Process Flow or Plant Floor Layout only through a Frappe Workflow that names their role; with none set they can only read | Changes to how the plant is drawn and wired are approved by the person accountable for the plant |
| Process flow | Approved: one Process Flow per plant lists which asset feeds which (Process Flow Link). Edited as in the row above; the Koyo 1 board is the pattern. Drives generated layouts, starved and blocked stops, downstream alarm hold-off and quality hold tracing | One source of truth for how product moves, instead of re-describing it in every feature |
| QA release | A Quality Inspector releases the line after any quality fault, on human test results; a Quality Hold holds product made since the last passing check until QA decides each lot | A sensor back in range is not proof: the sensor may be the fault |
| Alarms and notifications | Alarm Definitions are the conditions, set per plant (plant = factory). An Alarm is shared plant state with its own Alarms page per plant and across plants: priority order, acknowledge, shelve, audit trail, shown on kiosks. A Notification only delivers it (Frappe bell, WhatsApp, email) and links back; reading one never acknowledges the alarm. Unacknowledged past its response time, it escalates to the Floor Supervisor, then the Factory Manager | Considered putting alarms inside Notifications and rejected it: read is personal while acknowledged is shared, routine messages bury priority 1 alarms, and an alarm must not depend on one person seeing it (ISA-18.2 / IEC 62682) |
| Kiosk sign-in | The user's own Frappe login on the tablet; the Kiosk Profile's assigned users decide who may open it, as with POS Profile. No kiosk PIN and no My settings screen | Frappe already handles login, password policy, lockout and 2FA; a second secret adds setup and nothing Frappe can't enforce |
| App menu | Sidebar head dropdown on every screen: profile, notifications, theme, app switcher, Open kiosk, App settings, help, log out. Plant settings open only from the plant's sidebar | Keeps app-wide and per-plant settings apart |
| Power source | Detected from an ATS position input, the generator controller or incomer meters, in that order; never inferred. Shown on Resources and the plant page, with its own Utilities · power layout and the diesel day tank | Grid and generator time drive diesel cost and power-dip downtime, so they must come from a signal, not memory |
| Settings popups | App settings (all plants) opens centred from the app menu; Plant settings opens centred from the plant sidebar with the plant in its header; every option in either opens inside that popup | One pattern for both; the header says which scope you are changing |
