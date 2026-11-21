# Frappe Factory — planning docs

Architecture and product plans for Frappe Factory, agreed on 22 Nov 2026. Read them in this order.

| Doc | What it holds |
| --- | --- |
| [decisions.md](decisions.md) | Every decision taken, with the reasons (ThingsBoard, data volume, SCADA, licensing) |
| [architecture.md](architecture.md) | Principles, system context, connector interface, data tiers, domain model, alarms, sync, frontend, roles, versions, build plan, screen list |
| [prd.md](prd.md) | Goals for the Koyo pilot, personas, scope, user stories with acceptance criteria, workflow diagrams, release criteria |
| [trd.md](trd.md) | Components, MQTT contract, TimescaleDB schema, Frappe API, command groundwork, notifications, sync protocol, security, performance, deployment, testing, licensing |
| [erd.md](erd.md) | Entity diagram and field reference for every DocType, plus TimescaleDB tables |
| [screens.md](screens.md) | The 16 screen designs in frappe-ui, one picture each, with their sources in [`design/`](design/) |
| [scada-hmi.md](scada-hmi.md) | Which SCADA we use (our own), alternatives considered, how equipment is drawn (ISA-101), and the symbol library for many customers |

Diagrams are in [`images/`](images/).

## Next step

Screens are designed ([screens.md](screens.md)). Next: review them, then the code agent starts phase 1 of the build plan in [architecture.md](architecture.md#build-plan). Still to draw: kiosk login and the tablet layouts.

## Rules for the code agent

The build follows the skills in [frappe/skills](https://github.com/frappe/skills): `frappe-app-dev` (Pilot, typed whitelists, permission rules, semgrep, `IntegrationTestCase` with no mocks), `frappe-code-review`, `deep-app-audit`, `ui-design`, `review-ui-states` and `ship-it`. See the workflow table in [architecture.md](architecture.md#versions-and-engineering-workflow).
