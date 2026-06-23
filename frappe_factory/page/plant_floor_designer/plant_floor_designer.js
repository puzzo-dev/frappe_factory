frappe.pages.plant_floor_designer = {
	page: null,
	current_layout: null,

	init: function(wrapper) {
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: "Plant Floor Designer",
			single_column: true,
		});
		this.make(wrapper);
		this.load_layouts();
		this.bind_events();
	},

	make: function(wrapper) {
		$(wrapper).find('.layout-main-section').append($('.plant-floor-designer-container').detach());
	},

	bind_events: function() {
		const me = this;
		$('#layout-selector').on('change', function() {
			me.render_layout($(this).val());
		});
		$('#refresh-floor').on('click', function() {
			me.render_layout(me.current_layout);
		});
	},

	load_layouts: function() {
		const me = this;
		frappe.call({
			method: 'frappe.client.get_list',
			args: {
				doctype: 'Plant Floor Layout',
				fields: ['name', 'layout_name'],
				limit_page_length: 100,
			},
			callback: function(r) {
				const $sel = $('#layout-selector').empty();
				$sel.append('<option value="">Select a layout...</option>');
				(r.message || []).forEach(function(layout) {
					$sel.append(`<option value="${layout.name}">${layout.layout_name || layout.name}</option>`);
				});
				if (r.message && r.message.length === 1) {
					$sel.val(r.message[0].name).trigger('change');
				}
			},
		});
	},

	render_layout: function(name) {
		if (!name) return;
		this.current_layout = name;
		const me = this;
		frappe.call({
			method: 'frappe.client.get',
			args: {
				doctype: 'Plant Floor Layout',
				name: name,
			},
			callback: function(r) {
				me.draw(r.message);
			},
		});
	},

	draw: function(layout) {
		const $canvas = $('#plant-floor-canvas').empty();
		const width = Math.max(layout.width || 800, 400);
		const height = Math.max(layout.height || 600, 300);
		const $stage = $(`
			<div class="plant-floor-stage" style="
				position: relative;
				width: ${width}px;
				height: ${height}px;
				background: #f8f9fa;
				border: 1px solid #d1d8dd;
				margin: 10px 0;
			"></div>
		`);
		$canvas.append($stage);

		const widgets = (layout.widgets || []);
		if (!widgets.length) {
			$stage.append('<p class="text-muted" style="padding: 20px;">No widgets on this layout.</p>');
		}

		widgets.forEach(function(w) {
			const $widget = $(`
				<div class="plant-floor-widget" style="
					position: absolute;
					left: ${w.pos_x || 0}px;
					top: ${w.pos_y || 0}px;
					width: ${w.width || 120}px;
					height: ${w.height || 80}px;
					background: #fff;
					border: 2px solid #d1d8dd;
					border-radius: 6px;
					padding: 8px;
					box-shadow: 0 1px 3px rgba(0,0,0,0.1);
				">
					<strong>${w.label || w.machine_name || 'Machine'}</strong>
					<div class="widget-status indicator-pill gray">Loading...</div>
					<div class="widget-telemetry text-muted small"></div>
				</div>
			`);
			$stage.append($widget);
			if (w.thingsboard_device_id) {
				me.load_widget_status($widget, w.thingsboard_device_id);
			}
		});
		$('#plant-floor-status').text(`Layout: ${layout.layout_name || layout.name} (${widgets.length} widgets)`);
	},

	load_widget_status: function($widget, tb_device_id) {
		const me = this;
		frappe.call({
			method: 'frappe.client.get_list',
			args: {
				doctype: 'Machine Telemetry Log',
				filters: { thingsboard_device_id: tb_device_id },
				fields: ['metric_key', 'metric_value', 'recorded_at'],
				order_by: 'recorded_at desc',
				limit_page_length: 5,
			},
			callback: function(r) {
				const logs = r.message || [];
				let status = 'Idle';
				let telemetry = [];
				logs.forEach(function(log) {
					if (log.metric_key === 'machine_state') status = log.metric_value || status;
					else telemetry.push(`${log.metric_key}: ${log.metric_value}`);
				});
				const color = status === 'Running' ? 'green' : status === 'Fault' ? 'red' : 'gray';
				$widget.find('.widget-status')
					.removeClass('gray red green')
					.addClass(color)
					.text(status);
				$widget.find('.widget-telemetry').text(telemetry.join(' | '));
			},
		});
	},
};
