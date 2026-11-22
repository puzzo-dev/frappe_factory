# Frappe Factory — ERD

Nov 22, 2026 · I-Varse Technologies NG

## Entity relationship diagram

Tag is the hub: devices produce tags, and alarms, meters and commands are defined on them. Production and downtime hang off ERPNext Work Orders.

![ERD: 28 Frappe Factory DocTypes, 8 ERPNext DocTypes](images/erd.png)

The diagram shows the main chain; HMI Symbol and its two child tables are in the reference below (Plant Floor Widget and Plant Asset link to it).

Arrows point from a DocType to the one it links to (many-to-one). The arrows drawn are the main chain; every → line inside a box is a Link field to the named DocType, and ← in the ERPNext row shows which Frappe Factory DocType links to it.

## Entity reference

Key fields only; standard Frappe fields (`name`, `owner`, `creation`, `modified`, `docstatus`) are left out. → means a Link field. Naming series on edge-created documents start with the site code.

**Plant model**

| DocType | Kind | Key fields | Links to |
| --- | --- | --- | --- |
| Plant Area | Tree | `area_name`, `area_type` (Site, Area, Line, Cell), `site_code`, `notify_group` | → Plant Area (parent) |
| Plant Asset | Regular | `asset_name`, `asset_type` (Pump, Tank, Filter, Filler, Generator, Meter, PLC, Other), `current_state`, `state_since` | → Plant Area, → Workstation, → Asset (ERPNext, optional), → HMI Symbol (`default_symbol`, optional) |
| IoT Device Registry | Regular | `device_name`, `connector` (Direct, ThingsBoard), `protocol` (Modbus TCP, Modbus RTU, OPC UA, Simulator), `address`, `external_id`, `credentials` (Password), `online`, `last_seen`, `firmware` | → Plant Asset |
| Tag | Regular | `tag_key`, `label`, `unit`, `scale`, `offset`, `register_or_node`, `data_type`, `sample_ms`, `lo_lo`, `lo`, `hi`, `hi_hi`, `role` (Level, Flow, Pressure, Quality, Energy, Counter, State), `is_counter`, `is_interlock`, `writable` | → IoT Device Registry, → Plant Asset |

**Configuration**

| DocType | Kind | Key fields | Links to |
| --- | --- | --- | --- |
| Plant Floor Layout | Regular | `layout_name`, `background`, `width`, `height`, `is_published`, `published_at`, `widgets` (table) | → Plant Area |
| Plant Floor Widget | Child | `widget_type` (Asset, Value, Pipe, Label, Tank), `x`, `y`, `w`, `h`, `rotation`, `path` (for pipes), `tags` (JSON list), `symbol` | → Plant Asset, → HMI Symbol (pinned version) |
| HMI Symbol | Regular (named `{symbol_code}-v{version}`) | `symbol_code`, `symbol_name`, `category` (Pump, Tank, Valve, Filter, Membrane, Dosing, UV, Analyser, Filler, Conveyor, Motor, Generator, Meter, Pipe fitting, Other), `asset_types`, `svg` (sanitized), `width`, `height`, `ports` (table), `bindings` (table), `version`, `status` (Draft, Published, Deprecated), `is_standard`, `preview` | — |
| HMI Symbol Port | Child | `port_id`, `x`, `y`, `direction` (In, Out, Both) | → HMI Symbol (parent) |
| HMI Symbol Binding | Child | `property` (State, Level, Value, Alarm, Flow, Rotation), `element_id` (an `ff-*` id in the SVG), `effect` (Fill by state, Clip by level, Text, Show/hide, Animate), `required` | → HMI Symbol (parent) |
| Resource Meter | Regular | `meter_name`, `kind` (Diesel, Water, Chemical, Power), `capacity`, `unit`, `low_level` | → Tag, → Plant Asset, → Item (optional) |
| Alarm Definition | Regular | `alarm_code`, `condition` (HH, H, L, LL, State, Rate), `limit`, `severity` (Critical, High, Medium, Low), `on_delay_s`, `off_delay_s`, `deadband`, `is_interlock`, `recovery_steps` (table), `escalate_after_min` | → Tag |
| Downtime Reason | Tree | `reason_name`, `planned` (Check), `category` | → Downtime Reason (parent) |

**Operations and alarms**

| DocType | Kind | Key fields | Links to |
| --- | --- | --- | --- |
| Production Run | Submittable | `start`, `end`, `good_qty`, `reject_qty`, `rejects` (table: qty, reason), `status` | → Work Order, → Plant Area (line), → Batch (optional) |
| Factory Event | Log | `ts`, `event_type` (State, Status), `from_state`, `to_state`, `reason_code`, `msg_id` (unique) | → Plant Asset, → IoT Device Registry |
| Machine Stop (was Downtime Entry; renamed because ERPNext already has a Downtime Entry DocType) | Submittable | `start`, `end`, `duration_min`, `planned`, `comment`, `events` (table) | → Production Run, → Downtime Reason, → Plant Asset |
| Alarm | Regular | `status` (Raised, Acknowledged, Cleared, Shelved, Closed), `raised_at`, `acked_at`, `acked_by`, `cleared_at`, `shelved_until`, `shelve_reason`, `peak_value`, `repeat_count`, `escalation_level` | → Alarm Definition, → Plant Asset |
| Interlock Trip | Submittable | `tripped_at`, `readings_snapshot` (JSON), `steps` (table: step, done_by, done_at, value), `lab_value`, `signed_off_by`, `signed_off_at`, `restarted_at` | → Alarm, → Production Run, → Machine Stop, → Quality Inspection |
| Device Command | Submittable | `value`, `action`, `reason`, `status`, `requested_by`, `approved_by`, `sent_at`, `result`, `result_at` | → Tag, → IoT Device Registry |
| Refill Entry | Submittable | `qty`, `supplier`, `level_before`, `level_after`, `delivery_note` | → Resource Meter, → Stock Entry (optional) |

**Summaries and platform**

| DocType | Kind | Key fields | Links to |
| --- | --- | --- | --- |
| Shift Production Summary | Submittable | `shift_date`, `good_qty`, `reject_qty`, `uptime_min`, `downtime_min`, `oee`, `water_l`, `diesel_l`, `kwh`, `alarms`, `trips`, `notes` | → Plant Area, → Shift Type |
| Daily Plant Summary | Regular | `date`, same totals as shift, per site | → Plant Area (site) |
| Plant Status | Regular, one row per plant, overwritten | `state` (Running, Alert, Tripped, Offline), `note`, `good_qty_shift`, `open_alarms_p1/p2/p3`, `lowest_runway`, `last_seen`; feeds the Plants home cards | → Plant Area (site) |
| Resource Reading | Log | `ts`, `level`, `volume` (hourly from rollups) | → Resource Meter |
| Sync Outbox | Log | `seq`, `ref_doctype`, `ref_name` (Dynamic Link), `operation`, `status`, `attempts`, `last_error` | → DocType |
| Machine Telemetry | Virtual | reads TimescaleDB: `ts`, `tag`, `value`, `quality` | → Tag |
| Factory Configuration | Single | site, connector, TimescaleDB connection, retention days, `enable_commands`, sync URL and keys | — |
| OpsEdge Audit Log, OpsEdge Sync Log | Log | as today | — |

**Kiosk and ERP link**

| DocType | Kind | Key fields | Links to |
| --- | --- | --- | --- |
| Kiosk Profile | Regular | `kiosk_name`, `machines` (Table MultiSelect of Plant Asset), `allowed_actions`, `device_token`, `idle_minutes`, `disabled` | → Plant Area (site) |
| Kiosk Profile User | Child of Kiosk Profile | `user`, `is_default` | → User |
| Kiosk Session | Submittable, like POS Opening and Closing Entry | `opened_by`, `opened_at`, `closed_by`, `closed_at`, `status` | → Kiosk Profile, → Shift Type, → Production Run (only with ERPNext) |
| ERPNext Settings | Single | `enabled`, `mode` (Same site, Another site), `site_url`, `api_key`, `api_secret` (Password), `company`, `fg_warehouse`, one Check per link (work orders, stock, downtime, workstation status, quality, material requests, HRMS) | — |

Links to ERPNext DocTypes are never in these base DocTypes, because a Link to Work Order fails on a site without ERPNext. On a same-site link, turning the integration on adds Custom Fields such as `erpnext_work_order`; on another site, the ERPNext name is kept in a Data field `erp_ref` with `erp_doctype`.

**Templates and process flow** (Process Template and feeds into approved 22 Nov 2026)

| DocType | Kind | Key fields | Links to |
| --- | --- | --- | --- |
| Process Template | Regular | `template_name`, `industry`, `version`, `machine_unit`, `pack_unit`, `pack_size`, `stock_uom`, `rated_speed`, `symbol_pack`, `layout` (JSON), `assets` (JSON), `kiosk_views` | → HMI Symbol (via layout), → Quality Hold Template, → Alarm Definition (copied into the plant) |
| Plant (new field) | — | `process_template`, `template_version` | → Process Template |
| Process Flow | Regular, one live version per plant (approved 22 Nov 2026) | `plant`, `version`, `workflow_state`, `links` (table) | → Plant |
| Process Flow Link | Child of Process Flow | `from_asset`, `to_asset`, `medium`, `is_return`, `from_port`, `to_port`, `instrument` | → Plant Asset (same plant) |

**Quality**

| DocType | Kind | Key fields | Links to |
| --- | --- | --- | --- |
| Quality Hold | Submittable | `status` (On hold, Decided, Closed), `opened_by_doctype` and `opened_by` (Dynamic Link: Interlock Trip, Alarm or a person), `qa_owner`, `approver`, `closed_at` | → Quality Hold Template, → Plant Area, → Batch (only with ERPNext) |
| Hold Lot | Child of Quality Hold | `lot_label`, `from_time`, `to_time`, `machines`, `quantity`, `uom`, `location`, `decision` (Release, Release with deviation, Rework, Scrap), `decided_by`, `note` | — |
| Quality Sample | Regular | `taken_at`, `sample_point`, `machine`, `test`, `method`, `result`, `unit`, `passed`, `attachment` | → Quality Hold or → Interlock Trip, → Quality Inspection (only with ERPNext) |
| Quality Hold Template | Regular | `fault`, `tests` (table: test, limit, samples per lot, method), `release_rule`, `default_decisions` (table: lot kind, decision) | → Process Template, → Item |

Interlock Definition gains `quality_related` and Alarm Definition gains `places_quality_hold`. With ERPNext, a hold also opens a Non Conformance for the corrective action.

## Data outside MariaDB

TimescaleDB holds the readings. It has no foreign keys to MariaDB; the Frappe `Tag` name is the shared key.

| Table / view | Key | Columns | Kept |
| --- | --- | --- | --- |
| `reading` (hypertable) | `(tag, ts)` | `site`, `value`, `quality` | 90 days, compressed after 3 days |
| `reading_1m` (continuous aggregate) | `(tag, bucket)` | `min`, `max`, `avg`, `last`, `n` | 2 years |
| `reading_1h` (continuous aggregate on `reading_1m`) | `(tag, bucket)` | same | forever |

The agent's local buffer is a SQLite file with the same columns as `reading`, emptied in order when TimescaleDB is reachable.
