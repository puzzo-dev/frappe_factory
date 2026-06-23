from __future__ import annotations

import frappe


def get_data():
    return [
        {
            "module_name": "Frappe IOT",
            "color": "grey",
            "icon": "octicon octicon-cpu",
            "type": "module",
            "label": "Frappe IOT",
        }
    ]


def has_app_permission():
    return True
