# Frappe IOT

IoT integration app for Frappe v15. Provides factory telemetry ingestion, ThingsBoard integration, plant floor design, and edge-to-cloud sync for the OpsEdge Workstation.

## Module Overview

- **IOT** (`frappe_iot/iot/`) — ThingsBoard REST client, webhook receivers, and production-lag checks.
- **Sync** (`frappe_iot/sync/`) — Endpoints consumed by the `opsedge-sync` service for edge-to-cloud data sync.
- **Plant Floor Designer** (`frappe_iot/page/plant_floor_designer/`) — Desk page for designing and viewing live factory floor layouts.

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
bench --site opscloud.local install-app frappe_iot
bench --site opscloud.local migrate
```

## Contact

I-Varse Technologies NG — dev@itechnologies.ng
