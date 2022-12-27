import maya.mel as mel
import maya.cmds as cmds

from tp.core import log, dcc
from tp.maya import api

from tp.maya.cmds import attribute, animation, gui

logger = log.tpLogger


@dcc.undo_decorator()
def change_rotation_order(nodes=None, new_rotate_order=api.kRotateOrder_XYZ, bake_every_frame=False, timeline=True):
	"""
	Ses the rotation order for the given nodes.

	:param list(api.DagNode) or None nodes: list of nodes to change rotations order of. If None, all selected nodes
		will be taken into account.
	:param int new_rotate_order: rotation order number.
	:param bool bake_every_frame: whether all frames on the timeline or between the start and end frame keys for the
		nodes should be baked.
	:param bool timeline: whether the current active timeline should be used as a key filter.
	"""

	nodes = nodes or list(api.selected(filter_types=(api.kNodeTypes.kTransform,)))
	if not nodes:
		logger.warning('No objects selected. Please make a selection.')
		return

	frame_range = list(map(int, animation.selected_or_current_frame_range())) if timeline else None
	api.set_rotation_order_over_frames(
		nodes, rotation_order=new_rotate_order, bake_every_frame=bake_every_frame, frame_range=frame_range)


@dcc.undo_decorator()
def select_animated_nodes(mode=0):
	"""
	Selects animated nodes based on the given mode:
		- 0: select all animated nodes under the selected hierarchy.
		- 1: select all animated nodes in the scene.
		- 2: select all animated nodes in the selection.

	:param int mode: selection mode.
	"""

	if mode == 0:
		animation.animated_nodes(nodes_flag='hierarchy', select=True)
	elif mode == 1:
		animation.animated_nodes(nodes_flag='all', select=True)
	else:
		animation.animated_nodes(nodes_flag='selected', select=True)


@dcc.undo_decorator()
def set_key_channel_box():
	"""
	Sets key on all attributes taking into account selected channel box attributes.
	"""

	selected_attributes = mel.eval('selectedChannelBoxAttributes')
	if not selected_attributes:
		mel.eval('setKeyframe;')
	else:
		cmds.setKeyframe(breakdown=False, attribute=selected_attributes)


@dcc.undo_decorator()
def set_key():
	"""
	Sets key on all attributes without taking into account selected channel box attributes.
	"""

	mel.eval('setKeyframe;')


@dcc.undo_decorator()
def hold_animation():
	"""
	Makes an animation hold by copying the first selected key to the second one with flat tangents.
	"""

	animation.anim_hold()


@dcc.undo_decorator()
def delete_key_current_time():
	"""
	Deletes keys at the current time or the selected timeline range.
	"""

	mel.eval('timeSliderClearKey;')


@dcc.undo_decorator()
def key_toggle_visibility():
	"""
	Keys and inverts the visibility of the selected nodes.
	"""

	animation.toggle_and_key_visibility()


@dcc.undo_decorator()
def reset_attributes():
	"""
	Resets the selected node/s attributes to default values.
	"""

	attribute.reset_selected_nodes_attributes()


@dcc.undo_decorator()
def toggle_control_curve_visibility():
	"""
	Toggles curve visibility in the current viewport.
	"""

	current_panel = gui.panel_under_pointer_or_focus()
	if not current_panel:
		return
	visible_state = cmds.modelEditor(current_panel, query=True, nurbsCurves=True)
	cmds.modelEditor(current_panel, edit=True, nurbsCurves=not visible_state)
	visibility_str = 'VISIBLE' if visible_state else 'HIDDEN'
	logger.info('Control visibility set to {}'.format(visibility_str))
