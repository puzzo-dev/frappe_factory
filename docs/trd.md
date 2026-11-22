# Frappe Factory — TRD

Nov 22, 2026 · I-Varse Technologies NG

## Summary

This TRD sets the technical contracts the code agent builds against: services, message formats, the TimescaleDB schema, the Frappe API, commands, notifications, sync, security and deployment. It follows [architecture.md](architecture.md) and [prd.md](prd.md); story IDs (US-xxx) refer to the PRD.

**Decisions taken (22 Nov 2026)**

| Topic | Decision |
| --- | --- |
| Time-series database | TimescaleDB on PostgreSQL, on the OpsEdge box |
| Notifications | Frappe Notification (in-app, email, system) + WhatsApp through `frappe_whatsapp_openwa` |
| Pilot site | Koyo 10-head sachet water plant |
| PLC protocol | Not chosen yet. Driver layer supports Modbus TCP, Modbus RTU and OPC UA |
| Control | Release 1 is monitor-only. Command groundwork ships, disabled |
| Charts | frappe-ui charts (`frappe-ui/charts`, built on Apache ECharts 6; Apache 2.0). Raw ECharts only through their `echartOptions` hook or inside `ChartContainer` |
| IoT connector | Direct (default) and ThingsBoard, behind one interface |
| Frappe versions | v15 and v16 |
| Licence | Commercial licence owned by I-Varse Technologies |

## Components

Eight components. Five run on the OpsEdge box, one in OpsCloud, and two are the Frappe app and its frontend, which run in both places. The system diagram is in the Architecture doc.

| Component | Runs on | Language / packages | Job |
| --- | --- | --- | --- |
| OpsEdge Agent | Edge | Python 3.11, `asyncio`, `pymodbus`, `asyncua`, `paho-mqtt`, `psycopg` | Poll PLCs, scale and check values, write raw readings to TimescaleDB, publish state/alarm/status to MQTT, buffer in a local SQLite file when MQTT or the database is down, evaluate edge alarm rules |
| Mosquitto | Edge | Eclipse Mosquitto 2.x | Local MQTT broker. TLS and per-client username/password. Persistence on |
| Bridge | Edge | Python, `paho-mqtt`, `httpx` | Subscribe to state/alarm/status topics, post batches to Frappe every 1 s or 200 messages, retry with back-off, dedupe by message ID |
| TimescaleDB | Edge (optional in cloud) | PostgreSQL 16 + TimescaleDB | Raw readings, continuous aggregates, retention, compression |
| Frappe Factory app | Edge site and OpsCloud | Python, Frappe v15/v16, ERPNext | Domain DocTypes, alarm lifecycle, trips, runs, downtime, summaries, sync outbox, APIs, realtime |
| Frontend SPA | Served by Frappe | Vue 3, `frappe-ui`, frappe-ui charts (ECharts underneath), Vite | Control room, floor kiosk and manager shells at `/factory` |
| Sync service (`opsedge-sync`) | Edge | Python, `httpx` | Read the outbox in order, post to OpsCloud, pull masters |
| OpsCloud site | Cloud | Frappe + ERPNext + Frappe Factory | Head office, fleet view, finance, received documents |

**Driver layer in the agent.** `drivers/base.py` defines `Driver.read(tags) -> list[Reading]` and `Driver.write(tag, value)` (used only by commands, see below). Drivers: `modbus_tcp`, `modbus_rtu`, `opcua`, and `simulator` for tests and demos. The protocol for each device is a field on IoT Device Registry, so the pilot PLC choice is configuration, not code.

**Agent configuration.** The agent pulls its device and tag list from Frappe (`get_agent_config`) at start and every 5 minutes, and caches it, so it can start without Frappe.

## Messaging contract

All MQTT messages are JSON, UTF-8, with times in UTC as ISO 8601 with milliseconds. Every message has a `msg_id` (UUIDv7) so the bridge can drop duplicates.

| Topic | Publisher | QoS | Retained | Content |
| --- | --- | --- | --- | --- |
| `factory/{site}/{device}/telemetry` | Agent | 0 | No | Live values for the UI only. The database write is direct, not through MQTT |
| `factory/{site}/{device}/state` | Agent | 1 | Yes | `StateChange` |
| `factory/{site}/{device}/alarm` | Agent | 1 | No | `AlarmEvent` |
| `factory/{site}/{device}/status` | Agent | 1 | Yes | `DeviceStatus` (also the MQTT last-will message: offline) |
| `factory/{site}/{device}/cmd` | Bridge | 1 | No | `CommandRequest` — reserved, unused in release 1 |
| `factory/{site}/{device}/cmd/ack` | Agent | 1 | No | `CommandResult` — reserved, unused in release 1 |
| `factory/{site}/summary` | Bridge | 1 | Yes | `PlantStatus`: state, one-line note, output this shift, open alarms by priority, lowest runway. On change, at least every 15 s; the sync service forwards it to OpsCloud |

**Payloads**

```json
// StateChange
{"msg_id": "0193...", "device": "KOYO1-FILLER-01", "ts": "2026-11-22T08:14:03.120Z",
 "from": "running", "to": "stopped", "reason_code": "E_DOOR_OPEN"}

// AlarmEvent
{"msg_id": "0193...", "device": "KOYO1-LEAD-01", "ts": "...", "alarm": "LEAD_HH",
 "event": "raised", "severity": "critical", "tag": "lead_ppb", "value": 14.2,
 "limit": 10.0, "interlock": true}

// DeviceStatus
{"msg_id": "0193...", "device": "KOYO1-PLC-01", "ts": "...", "online": true,
 "firmware": "2.4.1", "buffer_backlog": 0}

// Telemetry (live UI only)
{"device": "KOYO1-TANK-RAW", "ts": "...", "values": {"level_pct": 62.4, "volume_l": 6240}}
```

`event` in AlarmEvent is `raised` or `cleared`. Acknowledge and shelve happen in Frappe and are not sent back to the agent. `reason_code` is optional and comes from the PLC when it provides one.

The ThingsBoard adapter maps ThingsBoard rule-chain webhooks to these same objects before the handlers see them.

## TimescaleDB schema

One narrow table for all readings, plus continuous aggregates. Tag IDs match the Frappe `Tag` name, so no join to MariaDB is needed.

```sql
CREATE TABLE reading (
  ts        TIMESTAMPTZ      NOT NULL,
  site      TEXT             NOT NULL,
  tag       TEXT             NOT NULL,   -- Frappe Tag name
  value     DOUBLE PRECISION,
  quality   SMALLINT         NOT NULL DEFAULT 0,  -- 0 good, 1 uncertain, 2 bad
  PRIMARY KEY (tag, ts)
);
SELECT create_hypertable('reading', 'ts', chunk_time_interval => INTERVAL '1 day');

ALTER TABLE reading SET (timescaledb.compress,
  timescaledb.compress_segmentby = 'tag', timescaledb.compress_orderby = 'ts DESC');
SELECT add_compression_policy('reading', INTERVAL '3 days');
SELECT add_retention_policy('reading', INTERVAL '90 days');   -- from Factory Configuration

CREATE MATERIALIZED VIEW reading_1m WITH (timescaledb.continuous) AS
SELECT time_bucket('1 minute', ts) AS bucket, tag,
       min(value), max(value), avg(value), last(value, ts) AS last, count(*) AS n
FROM reading GROUP BY bucket, tag;
SELECT add_continuous_aggregate_policy('reading_1m',
  start_offset => INTERVAL '1 hour', end_offset => INTERVAL '1 minute',
  schedule_interval => INTERVAL '1 minute');
SELECT add_retention_policy('reading_1m', INTERVAL '2 years');

-- reading_1h: same shape over reading_1m (hierarchical aggregate), kept forever
```

**Query rules** (`frappe_factory/timeseries/repository.py`)

| Range asked | Source | Bucket |
| --- | --- | --- |
| ≤ 6 hours | `reading` | raw, or 10 s if more than 2,000 points |
| ≤ 14 days | `reading_1m` | 1 min to 15 min |
| longer | `reading_1h` | 1 h to 1 day |

Every chart query returns at most 2,000 points per series. Counters (bag count, kWh, litres) use `last - first` per bucket, not `avg`.

**Connection.** Frappe connects with a read-only database user. Only the agent has write access. Credentials sit in Factory Configuration as Password fields.

## Frappe API surface

All methods are `@frappe.whitelist(methods=[...])` with type hints on every parameter. None allow guests, except the ThingsBoard webhooks.

| Method (module `frappe_factory.api.*`) | HTTP | Caller | Role | Purpose |
| --- | --- | --- | --- | --- |
| `ingest.events(batch: list[dict])` | POST | Bridge | Factory Integration | State, alarm and status messages. Idempotent on `msg_id` |
| `ingest.agent_config(site: str)` | GET | Agent | Factory Integration | Devices, tags, limits, alarm rules for the agent |
| `plant.get_snapshot(area: str)` | GET | SPA | any Factory role | Current value, quality and age of every tag in an area, plus asset states |
| `plant.get_series(tags: list[str], start: str, end: str, max_points: int = 2000)` | GET | SPA | any Factory role | Trend data from TimescaleDB |
| `alarms.acknowledge(alarm: str, comment: str \| None)` | POST | SPA | Operator and up | Acknowledge |
| `alarms.shelve(alarm: str, minutes: int, reason: str)` | POST | SPA | Supervisor and up | Shelve, max 480 min |
| `trips.complete_step(trip: str, step: str, value: str \| None)` | POST | SPA | per step | Recovery checklist |
| `trips.sign_off(trip: str)` | POST | SPA | Supervisor, Manager | Allow restart |
| `runs.start(work_order: str, line: str)` / `runs.close(run: str, rejects: list[dict])` | POST | SPA | Operator and up | Production runs |
| `downtime.set_reason(entry: str, reason: str)` | POST | SPA | Operator and up | Stop reason |
| `shift.close(summary: str, notes: str)` | POST | SPA | Supervisor | Submit shift summary |
| `sync.push(batch: list[dict])` / `sync.pull(since: str)` | POST / GET | Sync service | Factory Integration | Edge ↔ cloud |
| `hmi.get_symbols(since: str \| None)` | GET | SPA | any Factory role | Symbol library, cached per session |
| `health.status()` | GET | Monitoring | System Manager | Agent, broker, DB, sync backlog |
| `connectors.thingsboard.telemetry/alarm/device_connected` | POST | ThingsBoard | Guest + token + IP allowlist + rate limit | ThingsBoard adapter only |
| `plants.list()` | GET | SPA | any Factory role | Plants home cards: every plant the user may see, from Plant Status, problems first |
| `sync.status(status: dict)` | POST | Sync service | Factory Integration | Upserts the plant's one Plant Status row on OpsCloud and publishes it to the `factory:plants` room |
| `plant.watch(site: str)` | POST | SPA (OpsCloud) | any Factory role | Asks that plant's edge to relay live tag values while its screen is open. Renewed every 30 s; the relay stops 60 s after the last renewal |

**Realtime** (`frappe.publish_realtime`, room per site)

| Event | Payload | Rate limit |
| --- | --- | --- |
| `ff_tag` | `{tag, value, quality, ts}` | 1 per second per tag, last value wins |
| `ff_state` | `{asset, state, since}` | on change |
| `ff_alarm` | `{alarm, status, severity, asset}` | on change |
| `ff_trip` | `{trip, status}` | on change |

Live tag values reach the bridge over MQTT and are pushed to the SPA without being saved in MariaDB.

**Several plants in one app.** Each plant is a site-level Plant Area tied to one edge box, and access is per plant: a User Permission on that Plant Area plus a `permission_query_conditions` hook on every plant-scoped DocType. `Plant Status` (a regular DocType, one row per plant, overwritten, never a log) holds the latest PlantStatus message. No message for 60 s sets it to Offline and keeps the last figures with their time. The SPA subscribes to `factory:plants` on the Plants home and to `factory:<site>:*` only for the open plant. Opening a plant from OpsCloud starts `plant.watch`; the edge then relays that plant's telemetry through the sync channel at the plant's live interval (2 s by default) until the watch lapses.

## Command groundwork

Release 1 ships the full command path, switched off in three places. Turning it on later is configuration plus UI, not a redesign.

**The three switches** (all off by default)

1. `Factory Configuration.enable_commands` — site-wide.
2. `Tag.writable` — per tag; only writable tags accept commands. Never set on a tag that is part of a safety interlock (validation refuses it when `Tag.is_interlock` is set).
3. Agent config `allow_write: false` — the agent drops any command when this is off, even if Frappe sends one.

**What ships in release 1**

- DocType `Device Command` (submittable): tag, target value or action, reason, requested by, approved by, status, sent at, result, result at, error.
- Status flow: Draft → Requested → Approved → Sent → Done | Rejected by PLC | Timed out | Cancelled. A command times out after 10 s with no `cmd/ack`.
- `IoTConnector.send_command(device, command)` in the interface. Direct adapter: publishes `CommandRequest` to `cmd`. ThingsBoard adapter: calls ThingsBoard RPC. Both raise `CommandsDisabled` while switch 1 is off.
- Agent: `cmd` subscriber and handler registry with an allowlist of tags, value range check against Tag limits, and `Driver.write`. Returns `CommandResult`.
- Permissions: role `Factory Operator Command` (no users in R1). Two-person rule as a setting: requester and approver must be different users.
- Audit: every state change of a Device Command goes to `OpsEdge Audit Log`.
- Tests: the full path runs against the `simulator` driver in CI.

**Not in release 1:** command buttons in the SPA, setpoint screens, any recipe download.

## HMI symbol library

Every piece of equipment on a mimic is drawn from an `HMI Symbol` record. A symbol is drawn once and reused at every site, so a new customer's plant is assembled from the library, not drawn from scratch.

**Record.** `HMI Symbol` (regular DocType, named `{symbol_code}-v{version}`, for example `pump-centrifugal-v2`):

| Field | Type | Purpose |
| --- | --- | --- |
| `symbol_code` | Data, unique with version | Stable id, for example `pump-centrifugal` |
| `symbol_name` | Data | Label in the designer palette |
| `category` | Select | Pump, Tank, Valve, Filter, Membrane, Dosing, UV, Analyser, Filler, Conveyor, Motor, Generator, Meter, Pipe fitting, Other |
| `asset_types` | Small Text (list) | Plant Asset types it can draw; used for the default pick |
| `svg` | Code | The drawing, sanitized on save |
| `width`, `height` | Int | Default size in layout units |
| `ports` | Table: HMI Symbol Port | Pipe connection points: `port_id`, `x`, `y`, `direction` (In, Out, Both) |
| `bindings` | Table: HMI Symbol Binding | What can move: `property` (State, Level, Value, Alarm, Flow, Rotation), `element_id` (an `ff-*` id in the SVG), `effect` (Fill by state, Clip by level, Text, Show/hide, Animate), `required` |
| `version` | Int | Starts at 1 |
| `status` | Select | Draft, Published, Deprecated |
| `is_standard` | Check | Shipped by I-Varse (read-only at customer sites) or uploaded by the customer |
| `preview` | Attach Image | Palette thumbnail |

Links in: `Plant Floor Widget.symbol` → HMI Symbol (a pinned version), and `Plant Asset.default_symbol` → HMI Symbol (optional; otherwise picked by `asset_types`).

**Naming inside the SVG.** Elements that move carry ids starting with `ff-`: `ff-body` (state fill), `ff-level` (level clip), `ff-value` (text), `ff-alarm` (alarm marker anchor), `ff-flow` (animated path). Ports are declared in the record, not in the SVG. On save, the app checks that the `element_id` of every required binding exists.

**Versioning.** A Published symbol is never edited. A change makes a new version. Widgets keep the version they were drawn with until a manager updates the layout. Deprecated symbols still render but leave the palette.

**Distribution.** Standard symbols ship inside the app as fixtures (`frappe_factory/hmi/symbols/<code>/symbol.svg` + `symbol.json`), so a new edge site works offline. OpsCloud is the master for new and customer symbols: HMI Symbol is a cloud-owned master in the sync pull. The SPA loads symbols once per session through `hmi.get_symbols(since: str | None)` (GET, any Factory role) and caches them.

**Security.** An uploaded SVG is untrusted. On save the server parses it with `defusedxml` and keeps only an allowlist of SVG elements and attributes: no `script`, no `foreignObject`, no `on*` event attributes, no external `href` or `xlink:href`, no `style` with `url()` or `@import`, no embedded raster images. Maximum 200 KB. Only Factory Manager and System Manager can upload.

**Symbol packs.** Symbols ship as packs, one per industry, plus a general pack every plant gets. HMI Symbol gains a `pack` field. Release 1 ships five packs, about 49 symbols, ISA-101 style and drawn in-house:

| Pack | Symbols |
| --- | --- |
| General (every plant) | Tanks, silo, centrifugal pump, valves, diverter, bucket elevator, belt and screw conveyors, cyclone, fan, bagger, analyser, level and flow instruments, generator |
| Water and beverage | Sachet filler, media and cartridge filters, RO array, UV unit, ion exchange, dosing pump |
| Rice milling | Pre-cleaner, destoner, husker, paddy separator, whitener, grader, color sorter, dryer |
| Edible oil | Cooker, expeller, filter press, neutralizer and bleacher (agitated vessel), deodorizer, heat exchanger, bottle filler |
| Poultry farm | Layer house, feeder line, drinker line, tunnel fan, cooling pad, brooder, hammer mill, ribbon mixer, egg conveyor, egg grader, egg packer, cold room |

A machine with no symbol yet is placed as **Generic machine**: a labelled box that shows state colour and up to three values, swapped for a drawn symbol later. A company can also upload its own SVG; it is cleaned as below and shared by all that company's plants.

**Process Template** (approved 22 Nov 2026). One record per industry bundles a symbol pack, asset types, tag templates, alarm definitions, downtime reasons, KPIs and a starter layout. Adding a plant starts from a template, so a rice mill gets a working setup on day one. I-Varse ships Water and beverage, Rice milling, Edible oil, Poultry farm and Blank; a company can save any plant as its own template. Each template carries its units of count (for example sachet and bag of 20, or egg and tray of 30). A plant gets its own copy of the starter layout, edited in that plant's layout editor; editing the template's layout changes new plants only.

## Process flow (feeds into)

Approved 22 Nov 2026. Each Plant Asset lists the assets it feeds, which gives every plant a directed graph of how product moves. Each plant's flow is its own set of records, created and edited by the Factory Manager (acting as Floor Engineer) or a Maintenance Engineer; other roles can read it.

**Data.** Child table `Plant Asset Feed` on Plant Asset: `to_asset` (Link Plant Asset, same plant only), `medium` (Select: product, water, air, feed), `is_return` (Check), `from_port` and `to_port` (Data, optional, the symbol ports a pipe joins). Instruments on a line, such as AT-401, are not nodes: they carry `on_link` pointing at the link they measure. Utilities such as generators stay out of the flow.

**Rules.**

- A link may only point to an asset in the same plant.
- The graph must be acyclic once links marked `is_return` are removed. A return loop (IX-501 → T1) must be marked, or saving is refused.
- Every path should end at a sink: a filler, packer, drain or store. Dead ends are listed as warnings, not errors.
- A diverter (three-way valve) may have two outgoing links; its state tag decides which one is live.

**API.** `flow.graph(plant)` returns nodes and links; `flow.downstream(asset)` and `flow.upstream(asset)` walk it (cached per plant, cleared when a link changes); `layout.generate(plant, area)` turns the graph into a draft layout using a layered left-to-right layout (elkjs in the editor), placing each asset's symbol and drawing a pipe per link. The draft opens in the layout editor; nothing is published until a manager publishes it.

**What uses it.**

| Feature | How it uses the flow |
| --- | --- |
| Generated layouts | Symbol order and pipes come from the links; a hand-drawn layout can also be checked against the flow |
| Starved and blocked stops | When an asset stops, stops on downstream assets in the same minute are logged as Starved, and upstream ones as Blocked, not as their own fault |
| Alarm flood control | After an upstream trip, alarms on downstream assets are held for 60 s (configurable), then raised if still true |
| Quality hold tracing | A fault at a checkpoint holds product from every filler downstream of it; lots are split per sink |
| Bottleneck view | OEE per asset along the path shows which machine limits the line |

## ERPNext link and other ERPs

All ERP calls go through one adapter, so the rest of the app never knows where ERPNext lives. `frappe_factory/erp/base.py` defines `ErpAdapter` with `get_work_order`, `update_job_card`, `make_manufacture_entry`, `make_downtime_entry`, `set_workstation_status`, `make_quality_inspection`, `make_material_request` and `get_bin_qty`. Three implementations:

| Adapter | Used when | How |
| --- | --- | --- |
| `NullAdapter` | Standalone | Every call is a no-op; `is_linked()` is False, so screens hide what needs ERPNext |
| `LocalAdapter` | ERPNext on this site | `frappe.get_doc` and `frappe.new_doc` inside the same transaction as the Factory document |
| `RemoteAdapter` | ERPNext on another site | `frappe.frappeclient.FrappeClient` with the key and secret from ERPNext Settings; every call goes through the Sync Outbox, so a network drop queues instead of failing |

**Fields.** Base DocTypes carry no Link to an ERPNext DocType. Turning on the same-site link calls `create_custom_fields` for `erpnext_work_order`, `erpnext_workstation`, `erpnext_job_card` and so on; turning it off hides them. The remote adapter writes `erp_doctype` and `erp_ref` (Data). A `Machine Stop` maps its Downtime Reason to ERPNext's fixed `stop_reason` list (Excessive machine set up time, Unplanned machine maintenance, On-machine press checks, Machine operator errors, Machine malfunction, Electricity down, Other) through a mapping column on Downtime Reason, and keeps our reason in `remarks`.

**Other ERPs.** No adapter. Frappe Factory publishes a versioned set of whitelisted methods under `frappe_factory.api.v1` with an OpenAPI file in the repo, Integration users (role Factory Integration, read on plant data, write only on `plant.set_plan`) and standard Frappe `Webhook` records with HMAC-SHA256 secrets.

## Kiosk

The kiosk is a separate route, `/factory/kiosk`, a frappe-ui SPA in full-screen mode with no sidebar, like ERPNext's `/app/point-of-sale`.

1. A Floor Supervisor signs in with their Frappe user on the tablet and calls `kiosk.open_session(profile, shift_type, run=None)`. It checks the profile lists them, the role, and that the request's device token matches `Kiosk Profile.device_token`, then submits a `Kiosk Session`.
2. The tablet then works under a kiosk token bound to that session. `kiosk.switch_user(user, pin)` checks that the Frappe user is enabled, is on `Kiosk Profile User` and holds a role allowed for the profile's view, then that the PIN matches that user's hashed PIN (Password field on `Factory User Settings`). A PIN is never looked up on its own. It then sets the acting user for the next calls. Every write sets `owner` to the acting user, not the supervisor.
3. Each action method checks both the role and the profile's `allowed_actions`, and only for machines in `Kiosk Profile.machines`.
4. `kiosk.close_session()` needs a Floor Supervisor's Frappe user and PIN, totals the session and links it to the Shift Production Summary.

Five wrong PINs lock that user on every kiosk for 15 minutes. A user without a PIN cannot sign in; the PIN is set only from the user's own Frappe session after a password sign-in. `Kiosk Profile.view` (Select: Line, Maintenance, Quality) picks the screen and the allowed actions. Device tokens are random 32-byte values stored hashed, reset from Settings → Kiosks.

## Quality hold and QA release

`Interlock Definition.quality_related` (Check) and `Alarm Definition.places_quality_hold` (Check) decide when a hold opens. On a quality-related trip, the recovery checklist inserts two steps from the Quality Hold Template: the samples and `qa_release`. `trips.complete_step(trip, "qa_release")` checks the acting user's Quality Inspector role, re-checks their PIN, and that every required sample is in and passes; until then `trips.sign_off` refuses.

Opening a hold creates `Quality Hold` with `Hold Lot` rows. Lots come from the filler counters and the checkpoint readings: everything from the last passing check to the fault, split where the readings crossed the alert limit. Lot quantities are stored in the machine unit (sachets); the pack unit (bags) and the loose remainder come from the Process Template's conversion. Tanks named in the template are held whole. `quality.decide_lot(lot, decision, note)` takes Release, Release with deviation, Rework or Scrap; deviation also needs `quality.approve_deviation` by a Factory Manager. `quality.close_hold` needs a decision on every lot and the inspector's Frappe user and PIN.

With ERPNext: each `Quality Sample` creates a Quality Inspection (inspection type In Process, reference Job Card, status Accepted or Rejected); the hold sets the Batch `disabled` and opens a Non Conformance; Release clears the batch, Scrap posts a Material Issue to the scrap warehouse. Without ERPNext the samples and decisions stay in Frappe Factory.

## Notifications

All notifications use Frappe's own `Notification` DocType for in-app, email and system alerts. WhatsApp goes through `frappe_whatsapp` with the `frappe_whatsapp_openwa` dual gateway (OpenWA session or Meta Cloud API, with its outbound queue, retries and fallback). Frappe Factory adds no messaging code of its own.

**How it is wired**

- Frappe Factory ships `Notification` records as fixtures on `Alarm`, `Interlock Trip`, `Machine Stop`, `Resource Meter` and `Shift Production Summary`. Admins edit recipients and text in Desk.
- WhatsApp is a soft dependency. When `frappe_whatsapp` is installed, Frappe Factory also ships `WhatsApp Notification` records for the same events. The dual gateway routes them. When it is not installed, those fixtures are skipped.
- Recipients come from roles and from a per-area `Notification Group` field on Plant Area (for example the Koyo line supervisors).
- Meta Cloud API needs approved templates for business-initiated messages. The fixtures use templates; the OpenWA path can send the same text.

**Events and channels (defaults)**

| Event | In-app | Email | WhatsApp | Who |
| --- | --- | --- | --- | --- |
| Interlock trip raised | Yes | Yes | Yes | Supervisors of the area, Factory Manager, Quality Inspector |
| Critical alarm raised | Yes | No | Yes | Supervisors of the area |
| Critical alarm not acknowledged after 5 min | Yes | Yes | Yes | Factory Manager (escalation) |
| High / medium alarm | Yes | No | No | Area operators and supervisors |
| Tank below low level (fuel, water) | Yes | No | Yes | Storekeeper, Supervisor |
| Device offline > 10 min | Yes | Yes | No | Maintenance, System Manager |
| Shift summary submitted | Yes | Yes | No | Factory Manager |
| Sync backlog > 1 hour | Yes | Yes | No | System Manager |

**Escalation.** A scheduler job every minute raises `Alarm.escalation_level` when a critical alarm is still unacknowledged past its delay. A `Notification` on that field change sends the escalation. **One message per event:** repeats of a chattering alarm update the same Alarm and do not trigger new messages.

**Licence note.** `frappe_whatsapp_openwa` is declared AGPL-3.0 in its `hooks.py`. See Licensing.

## Sync protocol

Edge and cloud sync through an ordered outbox, with one owner per DocType. The direction table is in the Architecture doc.

**Outbox.** DocType `Sync Outbox` (log type, autoincrement): `seq`, `ref_doctype`, `ref_name`, `operation` (insert, update, submit, cancel), `modified`, `payload_hash`, `status` (pending, sent, acked, failed), `attempts`, `last_error`. A `doc_events` hook on every edge-owned DocType adds a row in the same transaction as the change.

**Push (edge → cloud)**

1. The sync service reads up to 100 pending rows in `seq` order.
2. It sends the current document JSON for each row to `sync.push`, with the site code and the highest `seq`.
3. OpsCloud applies the batch in one transaction. It skips rows whose `(site, seq)` it has already applied, so a resend is safe.
4. OpsCloud answers with the last applied `seq`. The edge marks those rows acked.
5. On error, back-off is 5 s, 30 s, 2 min, then every 10 min. A failed row blocks later rows of the same document only, not the whole queue.

**Pull (cloud → edge).** Every 5 minutes, the service calls `sync.pull(since)` with the last `modified` it saw per master DocType. Cloud-owned masters are inserted or updated on the edge with `ignore_permissions` under the Factory Integration user only.

**Links.** A document is sent only after the masters it links to exist in the cloud. Edge-created names carry the site code, so they never collide.

**Monitoring.** `OpsEdge Sync Log` records each batch. `health.status` reports backlog size and oldest pending age. The backlog alarm fires at 1 hour.

## Security

| Area | Control |
| --- | --- |
| Network | OpsEdge box on the factory LAN, firewall closed inbound from the internet. Outbound only to OpsCloud over HTTPS. Remote support over a VPN (WireGuard or Tailscale), never an open port |
| MQTT | TLS on the LAN, one username per client (agent, bridge), ACLs per topic. Anonymous access off |
| Frappe API | API key + secret per service user (`Factory Integration`). No guest methods on the Direct connector |
| ThingsBoard webhooks | Token in Factory Configuration (Password field), IP allowlist, rate limit — as in the current code |
| Database | TimescaleDB: agent user can write, Frappe user is read-only. MariaDB unchanged |
| Secrets | Password fields in Frappe; `.env` files on the box readable by root only. Nothing in git |
| Permissions | Role and Plant Area user permissions; `permission_query_conditions` and `has_permission` hooks return True/False; `get_query(..., ignore_permissions=False)` |
| System user | `factory-system` user gets only `Factory Integration`, not `System Manager` (change from current code) |
| Audit | Alarm actions, trip steps, sign-offs, commands, config changes, sync batches → `OpsEdge Audit Log` |
| Code checks | Semgrep with frappe/semgrep-rules on every PR; `deep-app-audit` at each phase end |

## Performance and capacity

Targets for one OpsEdge box. Each is checked with a load test in CI or at the pilot.

| Measure | Target |
| --- | --- |
| Tags per site | 500 at 1 s sampling (pilot needs far fewer) |
| PLC change to screen | ≤ 5 s at the 95th percentile on the LAN |
| Agent buffer | 7 days of readings when the database or broker is down |
| `get_snapshot` for one area | ≤ 300 ms |
| `get_series`, 24 h, 4 tags | ≤ 500 ms |
| `get_series`, 30 days, 4 tags | ≤ 1 s |
| `ingest.events` batch of 200 | ≤ 500 ms |
| Realtime clients | 20 SPA screens at the same time |
| Sync catch-up | A 24-hour backlog synced within 30 min once the link is back |
| Disk on the box | ≤ 50 GB for 90 days raw at 500 tags with compression (to be measured) |

**Recommended OpsEdge hardware (pilot):** x86 mini PC, 4 cores, 16 GB RAM, 512 GB SSD, UPS. The box runs Frappe, ERPNext, MariaDB, Redis, TimescaleDB, Mosquitto, the agent, the bridge and the sync service.

## Deployment

**OpsEdge box.** One `docker compose` project in `edge/deploy/`, based on `frappe_docker` (I-Varse fork):

| Service | Image | Restart | Volume |
| --- | --- | --- | --- |
| frappe (web, worker, scheduler, socketio) | custom image with ERPNext + Frappe Factory (+ frappe_whatsapp, frappe_whatsapp_openwa) | always | sites |
| mariadb, redis-cache, redis-queue | standard | always | db |
| timescaledb | `timescale/timescaledb` (TSL build, see Licensing) | always | tsdb |
| mosquitto | `eclipse-mosquitto:2` | always | mqtt config, data |
| opsedge-agent | built from `edge/opsedge_agent` | always | agent buffer |
| bridge | built from `edge/bridge` | always | — |
| opsedge-sync | built from the existing sync service | always | — |

Rules: every service restarts by itself after a power cut. The agent uses the host network only where a serial (RTU) port is needed. Backups: Frappe backup nightly to OpsCloud object storage when online; `pg_dump` of TimescaleDB rollups weekly.

**OpsCloud.** Standard Frappe Cloud-style multi-tenant bench, or own Kubernetes or Docker setup. Frappe Factory is installed with `install-app`. TimescaleDB in the cloud is optional (only for fleet trends from hourly rollups).

**Release.** Semantic versions as in the current repo (`scripts/bump_version.py`). Edge images are tagged with the same version. An edge box upgrades only when its sync backlog is empty.

## Testing

| Level | What | Tooling |
| --- | --- | --- |
| Unit (Python) | Scaling, limit checks, alarm state machine, outbox ordering, command validation | `pytest` for agent and bridge; `IntegrationTestCase` for Frappe code |
| Frappe integration | DocType controllers, APIs, permissions per role, hooks | `IntegrationTestCase` against a real MariaDB site, no mocks (frappe/skills rule). Current mock-based tests rewritten |
| Version matrix | Whole Frappe suite on v15 and v16 | GitHub Actions, two jobs, Pilot benches |
| End-to-end edge | Simulator driver → agent → MQTT → bridge → Frappe → SPA | docker compose in CI, scripted scenarios: stop, trip, low tank, link cut |
| Frontend | Components and screens, every UI state | Vitest; `review-ui-states` screenshots with Playwright |
| Load | 500 tags at 1 s for 24 h | Simulator + k6 or Locust for API calls |
| Pilot acceptance | PRD release criteria at Koyo | Checklist, signed by Factory Manager |

Each story ID in the PRD has at least one test named after it (for example `test_us_203_restart_blocked_without_signoff`).

## Licensing

Frappe Factory moves to a commercial licence owned by I-Varse Technologies. The repo today says MIT (`license.txt`, `hooks.py` `app_license = "mit"`, `pyproject.toml`). Those three change to a proprietary licence text, and new source files get an I-Varse copyright header.

Three dependencies need a decision from a lawyer before licences are sold. These are flags, not legal advice.

| Dependency | Licence | Why it matters | Suggested action |
| --- | --- | --- | --- |
| ERPNext | GPL-3.0 | Frappe Factory imports and extends ERPNext. Shipping it to customers on an OpsEdge box can count as distribution of a combined work | Legal opinion on whether Frappe Factory is a derivative work; keep ERPNext coupling through DocType links and documented hooks |
| `frappe_whatsapp_openwa` | AGPL-3.0 (declared in its `hooks.py`) | AGPL applies to network use too | It is I-Varse's own app: relicense it under the same commercial licence, if all its code is I-Varse's |
| TimescaleDB features used (compression, continuous aggregates, retention) | Timescale License (TSL) | Free to use inside a product; the main ban is offering TimescaleDB itself as a hosted database service | Use the TSL build (the Apache-only build lacks these features). Re-check the current TSL text (effective June 2025) |

Other dependencies are permissive and cause no conflict: Frappe and frappe-ui (MIT), Apache ECharts, which frappe-ui charts bring in (Apache 2.0), Mosquitto and paho-mqtt (EPL-2.0 / EDL-1.0), pymodbus (BSD), asyncua (LGPL-3.0, used as a library without changes). A licence scan (for example `pip-licenses` and `license-checker`) runs in CI and fails on a new copyleft dependency.
