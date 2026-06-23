frappe.ui.form.on("Factory Configuration", {
    refresh(frm) {
        frm.add_custom_button("Test Webhook Token", () => {
            frappe.call({
                method: "frappe_factory.iot.webhooks.health_check",
                args: {},
                headers: {
                    "X-OpsEdge-Token": frm.doc.opsedge_webhook_token,
                },
                callback(r) {
                    if (r.message && r.message.status === "ok") {
                        frappe.show_alert({ message: __("Webhook token is valid"), indicator: "green" });
                    } else {
                        frappe.show_alert({ message: __("Webhook test failed"), indicator: "red" });
                    }
                },
                error() {
                    frappe.show_alert({ message: __("Webhook test failed"), indicator: "red" });
                },
            });
        });
    },
});
