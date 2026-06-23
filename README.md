# Frappe Factory

IoT-powered factory management for **Frappe v15**. Provides factory telemetry ingestion, ThingsBoard integration, plant floor design, and edge-to-cloud sync for the OpsEdge Workstation.

## Module Overview

- **IOT** (`frappe_factory/iot/`) — ThingsBoard REST client, webhook receivers, and production-lag checks.
- **Sync** (`frappe_factory/sync/`) — Endpoints consumed by the `opsedge-sync` service for edge-to-cloud data sync.
- **Plant Floor Designer** (`frappe_factory/page/plant_floor_designer/`) — Desk page for designing and viewing live factory floor layouts.

## Doctypes

| Doctype | Purpose |
|---|---|
| IoT Device Registry | Master device records linked to ThingsBoard |
| Machine Telemetry Log | High-volume sensor readings from ThingsBoard |
| Production Floor Event | Submittable audit log of floor events |
| Plant Floor Layout | Floor plan + machine widget placement |
| Plant Floor Widget | Child table of Plant Floor Layout |
| Shift Attendance Summary | Per-shift attendance summary |
| OpsEdge Sync Log | Sync transaction audit trail |
| Factory Configuration | Single-record site settings |

## Install

```bash
bench --site opscloud.local install-app frappe_factory
bench --site opscloud.local migrate
```

## Contact

I-Varse Technologies NG — dev@itechnologies.ng
