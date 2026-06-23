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
