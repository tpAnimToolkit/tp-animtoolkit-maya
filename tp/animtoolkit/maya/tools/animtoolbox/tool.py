from tp.core import tool


from tp.animtoolkit.maya.tools.animtoolbox import model, view, controller


class AnimToolboxTool(tool.DccTool):

	def setup_ui(self):
		super(AnimToolboxTool, self).setup_ui()

		_model = model.AnimToolboxModel()
		self._controller = controller.AnimToolboxController(_model)

		_model.changeRotationOrderEvent.connect(self._controller.change_rotate_order)
		_model.selectAnimatedNodesEvent.connect(self._controller.select_animated_nodes)
		_model.setKeyChannelBoxEvent.connect(self._controller.set_key_channel_box)
		_model.setKeyEvent.connect(self._controller.set_key)
		_model.makeAnimHoldEvent.connect(self._controller.make_anim_hold)
		_model.deleteKeyCurrentTimeEvent.connect(self._controller.delete_key_current_time)
		_model.keyToggleVisibilityEvent.connect(self._controller.key_toggle_visibility)
		_model.resetAttributesEvent.connect(self._controller.reset_attributes)
		_model.toggleControlCurvesVisibilityEvent.connect(self._controller.toggle_control_curve_visibility)

		self.ui = view.AnimToolboxView(model=_model)
