app_name = "frappe_iot"
app_title = "Frappe IOT"
app_publisher = "I-Varse Technologies NG"
app_description = "IoT integration app for Frappe v15 — factory telemetry, ThingsBoard integration, and plant floor design"
app_email = "dev@itechnologies.ng"
app_version = "1.0.0"
app_license = "mit"
required_apps = []

# Add to Apps Screen
add_to_apps_screen = [
    {
        "name": "frappe_iot",
        "logo": "/assets/frappe_iot/frappe_iot.svg",
        "title": app_title,
        "route": "/app/frappe_iot",
        "has_permission": "frappe_iot.config.desktop.has_app_permission",
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
        "on_submit": "frappe_iot.iot.webhooks.on_attendance_submit"
    },
    "Quality Inspection": {
        "on_submit": "frappe_iot.iot.webhooks.on_quality_submit"
    },
    "Work Order": {
        "on_update": "frappe_iot.iot.webhooks.on_work_order_update"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "hourly": [
        "frappe_iot.iot.webhooks.check_production_lag",
    ],
    "daily": [
        "frappe_iot.sync.api.cleanup_old_sync_logs",
    ],
}

# Testing
# -------
before_tests = "frappe_iot.tests.before_tests"

after_install = "frappe_iot.install.after_install"

# Permissions
# -----------
permission_query_conditions = {}
has_permission = {}

# User Data Protection
# --------------------
user_data_fields = []
