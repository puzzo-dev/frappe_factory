import frappe


def after_install():
    create_roles()
    create_system_user()
    create_default_factory_configuration()
    create_workspace()


def create_roles():
    """Create custom roles for Frappe Factory."""
    roles = ["Factory Manager", "Floor Supervisor", "Machine Operator", "Quality Inspector", "Storekeeper"]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({"doctype": "Role", "role_name": role, "desk_access": 1}).insert(ignore_permissions=True)
    frappe.db.commit()


def create_system_user():
    """Create a dedicated system user for scheduler tasks."""
    user_id = "factory-system@erp.local"
    if frappe.db.exists("User", user_id):
        return
    user = frappe.get_doc({
        "doctype": "User",
        "email": user_id,
        "first_name": "Factory",
        "last_name": "System",
        "enabled": 1,
        "user_type": "System User",
        "roles": [{"role": "System Manager"}, {"role": "Factory Manager"}],
    })
    user.insert(ignore_permissions=True)
    frappe.db.commit()


def create_default_factory_configuration():
    if not frappe.db.exists("Factory Configuration", "Factory Configuration"):
        doc = frappe.new_doc("Factory Configuration")
        doc.site_name = frappe.local.site
        doc.cloud_sync_interval_minutes = 60
        doc.machine_fault_timeout_minutes = 5
        doc.insert(ignore_permissions=True)
        frappe.db.commit()


def create_workspace():
    """Create Frappe Factory workspace in Frappe desk if it does not exist."""
    if frappe.db.exists("Workspace", "Frappe Factory"):
        return

    workspace = frappe.get_doc({
        "doctype": "Workspace",
        "name": "Frappe Factory",
        "label": "Frappe Factory",
        "title": "Frappe Factory",
        "sequence_id": 20,
        "is_standard": 0,
        "public": 1,
        "icon": "cpu",
        "charts": [],
        "shortcuts": [
            {"type": "DocType", "doc_type": "IoT Device Registry", "label": "IoT Devices"},
            {"type": "DocType", "doc_type": "Plant Floor Layout", "label": "Plant Floor Layouts"},
            {"type": "DocType", "doc_type": "Production Floor Event", "label": "Floor Events"},
            {"type": "DocType", "doc_type": "Factory Configuration", "label": "Factory Configuration"},
        ],
    })
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
