from tp.core import dcc

from tp.animtoolkit.maya.tools.animtoolbox import api


class AnimToolboxController(object):
	def __init__(self, model):
		super(AnimToolboxController, self).__init__()

		self._model = model									# type: tp.animtoolkit.maya.tools.animtoolbox.model.AnimToolboxModel

	# =================================================================================================================
	# PROPERTIES
	# =================================================================================================================

	@property
	def model(self):
		return self._model

	# =================================================================================================================
	# BASE
	# =================================================================================================================

	@dcc.undo_decorator()
	def change_rotate_order(self):
		"""
		Changes the rotation of the current selected nodes with DCC.
		"""

		api.change_rotation_order(new_rotate_order=self.model.rotation_order)

	def select_animated_nodes(self):
		"""
		Selects current animated nodes based on selected mode.
		"""

		api.select_animated_nodes(mode=self.model.selection_mode)

	def set_key_channel_box(self):
		"""
		Sets key on all attributes taking into account selected channel box attributes.
		"""

		api.set_key_channel_box()

	def set_key(self):
		"""
		Sets key on all attributes without taking into account selected channel box attributes.
		"""

		api.set_key()

	def make_anim_hold(self):
		"""
		Keeps the animation
		"""

		api.hold_animation()

	def delete_key_current_time(self):
		"""
		Deletes keys at the current time or the selected timeline range.
		"""

		api.delete_key_current_time()

	def key_toggle_visibility(self):
		"""
		Keys and inverts the visibility of the selected nodes.
		"""

		api.key_toggle_visibility()

	def reset_attributes(self):
		"""
		Resets the selected node/s attributes to default values.
		"""

		api.reset_attributes()

	def toggle_control_curve_visibility(self):
		"""
		Toggles curve visibility in the current viewport.
		"""

		api.toggle_control_curve_visibility()
