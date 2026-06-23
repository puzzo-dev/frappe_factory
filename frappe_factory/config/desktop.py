from __future__ import annotations

import frappe


def get_data():
    return [
        {
            "module_name": "Frappe Factory",
            "color": "grey",
            "icon": "octicon octicon-cpu",
            "type": "module",
            "label": "Frappe Factory",
        }
    ]


def has_app_permission():
    return True
