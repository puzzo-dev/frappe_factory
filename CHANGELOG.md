# Changelog

All notable changes to this project will be documented in this file.

Versioning scheme:
- **MAJOR** (first number): new features
- **MINOR** (middle number): major fixes
- **PATCH** (last number): minor fixes, docs, chores, tests

## [4.1.0] - 2026-06-23

### Major Fix

- Fix broken `before_tests` hook
- Fix attendance hook field mismatch (`total_present` / `total_absent`)
- Fix quality hook workstation lookup
- Add missing `linked_work_order` field to IoT Device Registry
- Add ERPNext dependency declaration
- Fix `MANIFEST.in` package name
- Add telemetry timestamp validation and metric value parsing
- Replace broad `except Exception: pass` with structured logging
- Move edge-agent API keys from `frappe.conf` to database-stored `Factory Configuration`
- Add rate limiting to guest endpoints
- Implement `check_production_lag` scheduler
- Add database indexes to `Machine Telemetry Log`
- Add telemetry retention cleanup
- Add health check endpoint
- Add async telemetry ingestion option
- Expand unit test coverage

### Security

- Add audit log Doctype (`OpsEdge Audit Log`) and record all webhook/scheduler/sync actions
- Add IP allowlisting for guest webhook and sync API endpoints
- Create dedicated `factory-system@erp.local` system user for scheduler/doc-event operations
- Reduce `ignore_permissions=True` usage in doc-event hooks
- Convert raw SQL cleanup in sync API to Frappe ORM

### Performance

- Add optional bulk telemetry insert (`enable_bulk_telemetry`)
- Add optional telemetry deduplication (`enable_telemetry_dedup`)

### UI

- Implement basic Plant Floor Designer page with live widget telemetry

### Ops

- Export Role/Workspace fixtures
- Add client scripts for IoT Device Registry and Factory Configuration

## [4.0.0] - 2026-06-23

### Feature

- Plant Floor Designer module (Desk page, layout, and widget Doctypes)

## [3.0.0] - 2026-06-23

### Feature

- OpsEdge Sync module and edge-to-cloud sync API endpoints

## [2.0.0] - 2026-06-23

### Feature

- IoT module with ThingsBoard integration, telemetry ingestion, and alarm webhooks

## [1.0.0] - 2026-06-23

### Feature

- MVP release: Factory Configuration, IoT Device Registry, Machine Telemetry Log, Production Floor Event, and Shift Attendance Summary Doctypes
