import frappe


def after_install():
    create_default_factory_configuration()
    create_workspace()


def create_default_factory_configuration():
    if not frappe.db.exists("Factory Configuration", "Factory Configuration"):
        doc = frappe.new_doc("Factory Configuration")
        doc.site_name = frappe.local.site
        doc.cloud_sync_interval_minutes = 60
        doc.machine_fault_timeout_minutes = 5
        doc.insert(ignore_permissions=True)
        frappe.db.commit()


def create_workspace():
    # Creates Frappe IOT workspace in Frappe desk
    pass
