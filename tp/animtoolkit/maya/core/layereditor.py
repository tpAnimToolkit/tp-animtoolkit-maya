import math

import maya.mel as mel
import maya.cmds as cmds

from tp.maya.cmds import gui, decorators, contexts, animation


def modify_anim_layer_editor():
	"""
	Updates custom AnimToolbox layer editor UI.
	"""

	buttons_width = 22
	offset = -45

	ui_element = 'AnimLayerTabMoveUpButton'
	ui_type = cmds.objectTypeUI(ui_element)
	parent = mel.eval(ui_type + " -query -parent " + ui_element)
	qt_parent = gui.to_qt_object(parent)
	set_weight_button = gui.to_maya_object(qt_parent.layout().itemAt(2).widget())

	fast_merge_anim_layer_button = cmds.symbolButton(
		command=lambda *args: execute_fast_merge(), image='expandInfluenceList.png',
		annotation='Fast merge all layers excluding locked ones', width=buttons_width, parent=parent)
	fast_merge_single_item_from_layers_button = cmds.symbolButton(
		command=lambda *args: execute_fast_selected_merge(), image='alignVMin.png',
		annotation='Merge selected objects from animation layer excluding locked ones', width=buttons_width,
		parent=parent)
	layer_from_layer_range_button = cmds.symbolButton(
		command=lambda *args: create_add_anim_layer_from_objects_and_set_frame_range_from_multiply_anim_layers(),
		image='alignVMax.png', annotation='Creates anim layer with zero keyframes from bottom anim layer',
		width=buttons_width, parent=parent)
	layer_from_time_range_button = cmds.symbolButton(
		command=lambda *args: create_add_anim_layer_from_time_range(), image='flatTangent.png',
		annotation='Creates layer from time range', width=buttons_width, parent=parent)
	anim_layer_utils_button = cmds.symbolButton(
		command=lambda *args: show_anim_layer_utils(), image='layers.png',
		annotation='Anim Layer Utils', width=buttons_width, parent=parent)

	cmds.formLayout(
		parent, edit=True,
		attachForm=[(fast_merge_anim_layer_button, 'top', 1)],
		attachControl=[(fast_merge_anim_layer_button, 'right', offset, parent + '|' + set_weight_button)],
		attachNone=[(fast_merge_anim_layer_button, 'bottom'), (fast_merge_anim_layer_button, 'left')]
	)
	cmds.formLayout(
		parent, edit=True,
		attachForm=[(fast_merge_single_item_from_layers_button, 'top', 1)],
		attachControl=[(fast_merge_single_item_from_layers_button, 'right', offset, parent + '|' + fast_merge_anim_layer_button)],
		attachNone=[(fast_merge_single_item_from_layers_button, 'bottom'), (fast_merge_single_item_from_layers_button, 'left')]
	)
	cmds.formLayout(
		parent, edit=True,
		attachForm=[(layer_from_layer_range_button, 'top', 1)],
		attachControl=[(layer_from_layer_range_button, 'right', offset, parent + '|' + fast_merge_single_item_from_layers_button)],
		attachNone=[(layer_from_layer_range_button, 'bottom'), (layer_from_layer_range_button, 'left')]
	)
	cmds.formLayout(
		parent, edit=True,
		attachForm=[(layer_from_time_range_button, 'top', 1)],
		attachControl=[(layer_from_time_range_button, 'right', offset, parent + '|' + layer_from_layer_range_button)],
		attachNone=[(layer_from_time_range_button, 'bottom'), (layer_from_time_range_button, 'left')]
	)
	cmds.formLayout(
		parent, edit=True,
		attachForm=[(anim_layer_utils_button, 'top', 1)],
		attachControl=[(anim_layer_utils_button, 'right', 1, parent + '|' + ui_element)],
		attachNone=[(anim_layer_utils_button, 'bottom'), (anim_layer_utils_button, 'left')]
	)

	mel.eval('updateLayerEditor();')


@decorators.keep_selection_decorator
def execute_fast_merge():
	"""
	Fast merges all animation layers excluding locked ones.
	..note:: this operation is 5x - 20x times faster than standard Maya anim layers merge.
	"""

	with contexts.disable_viewport_context():
		layers = cmds.ls(type='animLayer')
		animation.select_objects_from_anim_layers(layers)
		have_locked = animation.extract_animation_based_on_anim_layer_selected_objects()
		if not have_locked:
			cmds.delete([anim_layer for anim_layer in layers if cmds.objExists(anim_layer)])


@decorators.keep_selection_decorator
def execute_fast_selected_merge():
	"""
	Merge selected objects from animation layers excluding locked ones (from start to end time of animation).
	"""

	with contexts.disable_viewport_context():
		animation.extract_animation_based_on_anim_layer_selected_objects()


def create_add_anim_layer_from_objects_and_set_frame_range_from_multiply_anim_layers(rotation_mode=1):
	"""
	Creates animation layer with zero keyframes from bottom.
	:return:
	"""

	selection = cmds.ls(sl=True)
	current_selected_anim_layers = animation.selected_anim_layers()
	frame_range = animation.anim_time_range_from_multiply_anim_layers(current_selected_anim_layers)
	if not current_selected_anim_layers:
		parent_layer = 'BaseAnimation'
	else:
		parent_layer = cmds.animLayer(current_selected_anim_layers[-1], query=True, parent=True)
	new_add_layer_name = animation.create_and_select_anim_layer(rotation_mode)
	cmds.animLayer(new_add_layer_name, edit=True, parent=parent_layer)
	if selection:
		cmds.setKeyframe(
			time=tuple([frame_range[0]]), breakdown=False, identity=True, inTangentType='linear',
			outTangentType='linear', dirtyDG=True, hierarchy='none', controlPoints=False, shape=False)
		cmds.setKeyframe(
			time=tuple([frame_range[1]]), breakdown=False, identity=True, inTangentType='linear',
			outTangentType='linear', dirtyDG=True, hierarchy='none', controlPoints=False, shape=False)

	return new_add_layer_name


def create_add_anim_layer_from_time_range(rotation_mode=1):
	"""
	Creates animation layer from time range.
	"""

	def _time_range_from_selected_keys_or_time_slider():

		playback_slider =  mel.eval('$tmpVar=$gPlayBackSlider')
		selected_time = cmds.timeControl(playback_slider, query=True, ra=True)
		curve = cmds.keyframe(query=True, name=True, sl=True)

		if selected_time[1] - selected_time[0] <= 1 and curve and curve[0]:
			num_frame = cmds.keyframe(query=True, sl=True)
			num_frame.sort()
			if not num_frame:
				selected_time = [0, 0]
			else:
				selected_time = [num_frame[0], num_frame[-1]]
			selected_time[1] = math.ceil(selected_time[1] + 1)

		return selected_time

	selection = cmds.ls(sl=True)
	frame_range = _time_range_from_selected_keys_or_time_slider()
	new_add_layer = animation.create_and_select_anim_layer(rotation_mode)
	if selection:
		cmds.setKeyframe(
			time=tuple([frame_range[0]]), breakdown=False, identity=True, inTangentType='linear',
			outTangentType='linear', dirtyDG=True, hierarchy='none', controlPoints=False, shape=False)
		cmds.setKeyframe(
			time=tuple([frame_range[1] - 1]), breakdown=False, identity=True, inTangentType='linear',
			outTangentType='linear', dirtyDG=True, hierarchy='none', controlPoints=False, shape=False)

	return new_add_layer


def show_anim_layer_utils():

	def _set_zero_key():
		cmds.setKeyframe(
			breakdown=False, identity=True, itt='plateau', ott='plateau', dd=True, hierarchy='none',
			controlPoints=False, shape=False)

	if cmds.window('animLayerUtils', query=True, ex=True):
		cmds.deleteUI('animLayerUtils')

	cmds.window('animLayerUtils', tb=True, mnb=False, mxb=False, mb=False, tlb=True, tbm=True)
	column_layout = cmds.columnLayout(adj=True)
	cmds.rowLayout(numberOfColumns=8)

	cmds.symbolButton(image='zeroKey.png', annotation='Zero Key Layer', command=lambda *args: _set_zero_key())

	cmds.showWindow('animLayerUtils')

