frappe.pages.plant_floor_designer = {
	page: null,
	init: function(wrapper) {
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: "Plant Floor Designer",
			single_column: true,
		});
		this.make(wrapper);
	},
	make: function(wrapper) {
		let $page = $(wrapper).find('.layout-main-section');
		$page.append(`
			<div id="plant-floor-canvas" style="width: 100%; height: 80vh; background: #f5f5f5;">
				<p style="padding: 20px;">Plant Floor Designer canvas placeholder.</p>
			</div>
		`);
	}
};
