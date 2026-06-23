app_name = "frappe_factory"
app_title = "Frappe Factory"
app_publisher = "I-Varse Technologies NG"
app_description = "IoT integration app for Frappe v15 — factory telemetry, ThingsBoard integration, and plant floor design"
app_email = "dev@itechnologies.ng"
app_version = "4.1.0"
app_license = "mit"
required_apps = ["erpnext"]

# Add to Apps Screen
add_to_apps_screen = [
    {
        "name": "frappe_factory",
        "logo": "/assets/frappe_factory/frappe_factory.svg",
        "title": app_title,
        "route": "/app/frappe_factory",
        "has_permission": "frappe_factory.config.desktop.has_app_permission",
    }
]

# Includes in <head>
# ------------------
app_include_js = []
app_include_css = []

# Fixtures
# --------
fixtures = [
    {"dt": "Role", "filters": [["name", "in", [
        "Factory Manager", "Floor Supervisor",
        "Machine Operator", "Quality Inspector", "Storekeeper"
    ]]]},
    {"dt": "Custom DocPerm"},
]

# Document Events
# ---------------
doc_events = {
    "Attendance": {
        "on_submit": "frappe_factory.iot.webhooks.on_attendance_submit"
    },
    "Quality Inspection": {
        "on_submit": "frappe_factory.iot.webhooks.on_quality_submit"
    },
    "Work Order": {
        "on_update": "frappe_factory.iot.webhooks.on_work_order_update"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "hourly": [
        "frappe_factory.iot.webhooks.check_production_lag",
    ],
    "daily": [
        "frappe_factory.sync.api.cleanup_old_sync_logs",
        "frappe_factory.iot.webhooks.cleanup_old_telemetry",
    ],
}

# Testing
# -------
before_tests = "frappe_factory.tests.before_tests"

after_install = "frappe_factory.install.after_install"

# Permissions
# -----------
permission_query_conditions = {}
has_permission = {}

# User Data Protection
# --------------------
user_data_fields = []
