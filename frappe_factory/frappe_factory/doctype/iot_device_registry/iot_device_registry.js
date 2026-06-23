frappe.ui.form.on("IoT Device Registry", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button("Ping Device", () => {
                frappe.show_alert({
                    message: __("Last seen: {0}", [frm.doc.last_seen || "never"]),
                    indicator: frm.doc.is_active ? "green" : "red",
                });
            });
        }
    },

    is_active(frm) {
        frm.set_df_property("thingsboard_device_id", "read_only", !frm.doc.is_active);
    },
});
