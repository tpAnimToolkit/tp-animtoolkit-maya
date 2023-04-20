import re
from functools import partial

from tp.common.qt import api as qt
from tp.common.qt.widgets import accordion

from tp.animtoolkit.maya.tools.animtoolbox import consts


class AnimToolboxView(qt.BaseWidget):
	def __init__(self, model, parent=None):

		self._model = model							# type: model.AnimToolboxModel

		super(AnimToolboxView, self).__init__(parent=parent)

	def get_main_layout(self):
		return qt.horizontal_layout(
			spacing=qt.consts.SPACING,
			margins=(
				qt.consts.WINDOW_SIDE_PADDING, qt.consts.WINDOW_BOTTOM_PADDING,
				qt.consts.WINDOW_SIDE_PADDING, qt.consts.WINDOW_BOTTOM_PADDING))

	def ui(self):
		super().ui()

		self._tool_type_scroll_area = qt.QScrollArea()
		self._tool_widget = qt.QListWidget(parent=self)
		self._tool_type_scroll_area.setWidget(self._tool_widget)
		self._tool_type_scroll_area.setWidgetResizable(True)
		self._tool_type_scroll_area.setFixedWidth(qt.dpi_scale(148))
		self._tool_type_scroll_area.setVerticalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)

		self._left_layout = qt.vertical_layout()
		self._tool_label = qt.label('Tools').h2()
		self._left_layout.addWidget(self._tool_label)
		self._left_layout.addWidget(self._tool_type_scroll_area)

		self._tool_options_stack = qt.sliding_opacity_stacked_widget(parent=self)
		self._tool_options_stack.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
		self._tool_hotkeys_stack = qt.sliding_opacity_stacked_widget(parent=self)
		self._tool_hotkeys_stack.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)

		self._tab_widget = qt.QTabWidget(parent=self)
		self._tab_widget.addTab(self._tool_options_stack, 'Tool Options')
		self._tab_widget.addTab(self._tool_hotkeys_stack, 'Tool Hotkeys')

		self.main_layout.addLayout(self._left_layout)
		self.main_layout.addWidget(self._tab_widget)

		for i, tool_class in enumerate(sorted(self._model.plugins_manager.plugins(), key=lambda x: x.ORDER)):
			new_tool = tool_class()
			tool_ui = new_tool.ui()
			hotkey_ui = new_tool.hotkey_ui()
			if not tool_ui:
				continue
			self._tool_widget.insertItem(i, re.sub("([a-z])([A-Z])", "\g<1> \g<2>", new_tool.TOOL_NAME))
			self._tool_options_stack.addWidget(tool_ui)
			self._tool_hotkeys_stack.addWidget(hotkey_ui)

	def setup_signals(self):
		super().setup_signals()

	# 	self._change_rotation_combo = qt.combobox_widget(
	# 		text='Change Rotation Order', items=consts.ROTATE_ORDERS, label_ratio=16, box_ratio=23,
	# 		tooltip=consts.CHANGE_ROTATE_ORDER_COMBO_TOOLTIP)
	# 	self._change_rotation_order_button = qt.button(
	# 		icon='key', min_width=qt.consts.BUTTON_WIDTH_ICON_MEDIUM, parent=self,
	# 		tooltip=consts.CHANGE_ROTATE_ORDER_COMBO_TOOLTIP)
	# 	change_rotation_layout = qt.horizontal_layout()
	# 	change_rotation_layout.addWidget(self._change_rotation_combo, 20)
	# 	change_rotation_layout.addWidget(self._change_rotation_order_button, 1)
	#
	# 	self._select_anim_nodes_combo = qt.combobox_widget(
	# 		text='Select Animated Nodes', items=consts.SELECT_OPTIONS, label_ratio=16, box_ratio=23,
	# 		tooltip=consts.SELECT_ANIMATED_NODES_TOOLTIP)
	# 	self._select_anim_nodes_button = qt.button(
	# 		icon='cursor', min_width=qt.consts.BUTTON_WIDTH_ICON_MEDIUM, parent=self,
	# 		tooltip=consts.SELECT_ANIMATED_NODES_TOOLTIP)
	# 	select_combo_layout = qt.horizontal_layout()
	# 	select_combo_layout.addWidget(self._select_anim_nodes_combo, 20)
	# 	select_combo_layout.addWidget(self._select_anim_nodes_button, 1)
	#
	# 	self._set_key_all_button = qt.button(
	# 		text='Set Key Channel Box', icon='key', tooltip=consts.SET_KEY_ALL_CHANNELS_TOOLTIP, parent=self)
	# 	self._set_key_button = qt.button(
	# 		text='Set Key All Channels', icon='key', tooltip=consts.SET_KEY_CHANNELS_TOOLTIP, parent=self)
	# 	self._anim_hold_button = qt.button(text='Hold Animation', tooltip=consts.ANIM_ON_HOLD_TOOLTIP, parent=self)
	# 	self._delete_current_frame_button = qt.button(
	# 		text='Delete Key Current Time', tooltip=consts.DELETE_CURRENT_FRAME_TOOLTIP, parent=self)
	# 	self._key_toggle_visibility_button = qt.button(
	# 		text='Key Visibility Toggle', tooltip=consts.TOGGLE_VIS_TOOLTIP, parent=self)
	# 	self._reset_attributes_button = qt.button(
	# 		text='Reset Attributes', tooltip=consts.RESET_ATTRS_TOOLTIP, parent=self)
	# 	self._toggle_control_curves_visibility_button = qt.button(
	# 		text='Control Curve Toggle', tooltip=consts.TOGGLE_CURVE_VISIBILITY_TOOLTIP, parent=self)
	#
	# 	accordion_widget = accordion.AccordionWidget(parent=self)
	# 	playback_widget = qt.QWidget(parent=self)
	# 	timeline_widget = qt.QWidget(parent=self)
	# 	accordion_widget.add_item('Playback', playback_widget, collapsed=False)
	# 	accordion_widget.add_item('Timeline', timeline_widget, collapsed=False)
	#
	# 	grid_top_layout = qt.grid_layout(spacing=2)
	# 	grid_top_layout.addWidget(self._set_key_all_button, 0, 0)
	# 	grid_top_layout.addWidget(self._set_key_button, 0, 1)
	# 	grid_top_layout.addWidget(self._anim_hold_button, 1, 0)
	# 	grid_top_layout.addWidget(self._delete_current_frame_button, 1, 1)
	# 	grid_top_layout.addWidget(self._key_toggle_visibility_button, 2, 0)
	# 	grid_top_layout.addWidget(self._reset_attributes_button, 2, 1)
	# 	grid_top_layout.addWidget(self._toggle_control_curves_visibility_button, 3, 0)
	#
	# 	self.main_layout.addLayout(change_rotation_layout)
	# 	self.main_layout.addLayout(select_combo_layout)
	# 	self.main_layout.addLayout(grid_top_layout)
	# 	self.main_layout.addWidget(accordion_widget)
	#
	# 	self._change_rotation_combo.set_current_index(self._model.rotation_order)
	# 	self._select_anim_nodes_combo.set_current_index(self._model.selection_mode)
	#
	# def setup_signals(self):
	# 	super(AnimToolboxView, self).setup_signals()
	#
	# 	self._model.rotationOrderChanged.connect(self._on_rotation_order_model_changed)
	# 	self._model.selectionModeChanged.connect(self._on_selection_mode_model_changed)
	#
	# 	self._change_rotation_combo.currentIndexChanged.connect(partial(setattr, self._model, 'rotation_order'))
	# 	self._change_rotation_order_button.clicked.connect(self._model.changeRotationOrderEvent.emit)
	# 	self._select_anim_nodes_combo.currentIndexChanged.connect(partial(setattr, self._model, 'selection_mode'))
	# 	self._select_anim_nodes_button.clicked.connect(self._model.selectAnimatedNodesEvent.emit)
	# 	self._set_key_all_button.clicked.connect(self._model.setKeyChannelBoxEvent.emit)
	# 	self._set_key_button.clicked.connect(self._model.setKeyEvent.emit)
	# 	self._anim_hold_button.clicked.connect(self._model.makeAnimHoldEvent.emit)
	# 	self._delete_current_frame_button.clicked.connect(self._model.deleteKeyCurrentTimeEvent.emit)
	# 	self._key_toggle_visibility_button.clicked.connect(self._model.keyToggleVisibilityEvent.emit)
	# 	self._reset_attributes_button.clicked.connect(self._model.resetAttributesEvent.emit)
	# 	self._toggle_control_curves_visibility_button.clicked.connect(self._model.toggleControlCurvesVisibilityEvent)
	#
	# def _on_rotation_order_model_changed(self, rotation_order_index):
	# 	"""
	# 	Internal callback function that is called each time rotation order index model value changes.
	#
	# 	:param int rotation_order_index: rotation order index.
	# 	"""
	#
	# 	with qt.block_signals(self._change_rotation_combo):
	# 		self._change_rotation_combo.set_current_index(rotation_order_index)
	#
	# def _on_selection_mode_model_changed(self, selection_mode_index):
	# 	"""
	# 	Internal callback function that is called each time selection mode index model value changes.
	#
	# 	:param int selection_mode_index: selection mode index.
	# 	"""
	#
	# 	with qt.block_signals(self._select_anim_nodes_combo):
	# 		self._select_anim_nodes_combo.set_current_index(selection_mode_index)
