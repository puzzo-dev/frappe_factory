# Frappe Factory

![Version](https://img.shields.io/badge/version-4.1.0-blue)

IoT-powered factory management for **Frappe v15**. Provides factory telemetry ingestion, ThingsBoard integration, plant floor design, and edge-to-cloud sync for the OpsEdge Workstation.

Versioning: `MAJOR.MINOR.PATCH` — major for features, minor for major fixes, patch for minor fixes.

## Security & Performance

- Database-stored API keys and webhook tokens
- IP allowlisting for guest endpoints
- Rate limiting on guest endpoints
- Audit log (`OpsEdge Audit Log`) for all webhook/scheduler/sync actions
- Optional bulk telemetry insert and deduplication
- Dedicated system user for scheduler tasks

## Auto-versioning

Use [Conventional Commits](https://www.conventionalcommits.org/). Install the hooks:

```bash
cp scripts/prepare-commit-msg-hook.sh .git/hooks/prepare-commit-msg
chmod +x .git/hooks/prepare-commit-msg
cp scripts/commit-msg-hook.sh .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

Bump version:

```bash
python scripts/bump_version.py --strict
```

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
