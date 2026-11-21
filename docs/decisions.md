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
- **Still pending:** `Process Template` and `Plant Asset.feeds_into`.

## Licensing flags (for legal review)

These are flags, not legal advice.

- ERPNext is GPL-3.0; whether Frappe Factory is a derivative work when shipped on an OpsEdge box needs a legal opinion.
- `frappe_whatsapp_openwa` declares AGPL-3.0 in its `hooks.py`; as I-Varse's own app it can be relicensed if all its code is I-Varse's.
- TimescaleDB features used (compression, continuous aggregates, retention) are under the Timescale License: fine inside a product, not as a hosted database service. Use the TSL build.
- The repo still says MIT in `license.txt`, `hooks.py` and `pyproject.toml`; these change when the build starts.
