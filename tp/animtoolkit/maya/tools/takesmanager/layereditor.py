import maya.mel as mel
import maya.cmds as cmds

from tp.common.qt import api as qt
from tp.maya.cmds import gui
from tp.maya.cmds.animation import animlayers


class TakesAnimLayersEditor(qt.BaseWidget):
	def __init__(self, parent=None):
		super().__init__(parent=parent)

		self.update_anim_layer_editor()

	def ui(self):
		super().ui()

		window_name = self.__class__.__name__
		if cmds.window(f'{window_name}Window', exists=True):
			cmds.deleteUI(window_name)
		window = cmds.window(window_name)
		cmds.showWindow(window)
		window_qt = gui.to_qt_object(window)

		tab_layout = cmds.tabLayout(f'{window_name}Layout', scrollable=False, tabsVisible=True, parent=window)
		cmds.setParent(tab_layout)

		# MenuBar
		cmds.menuBarLayout(f'{window_name}MenuBar')
		edit_menu_for_anim_layers = cmds.menu(label=mel.eval('uiRes("m_layerEditor.kAnimLayers");'), allowOptionBoxes=True)
		edit_menu_for_options_anim_layers = cmds.menu(label=mel.eval('uiRes("m_layerEditor.kOptionsAnimLayers");'), allowOptionBoxes=True)
		show_menu_for_anim_layers = cmds.menu(label=mel.eval('uiRes("m_layerEditor.kAnimLayersShowMenu");'), allowOptionBoxes=True)
		help_menu_for_anim_layers = cmds.menu(label=mel.eval('uiRes("m_layerEditor.kAnimLayersHelpMenu");'), allowOptionBoxes=True)

		# Main UI
		width = 22
		anim_layer_form_layout = cmds.formLayout()

		zero_key_anim_layer_button = cmds.symbolButton(image='zeroKey.png', annotation=mel.eval('uiRes("m_layerEditor.kZeroKeyAnimLayer");'))
		zero_weight_anim_layer_button = cmds.symbolButton(image='keyZeroWeight.png', annotation=mel.eval('uiRes("m_layerEditor.kZeroWeightAnimLayer");'))
		full_weight_anim_layer_button = cmds.symbolButton(image='keyFullWeight.png', annotation=mel.eval('uiRes("m_layerEditor.kFullWeightAnimLayer");'))
		selected_anim_layer_button = cmds.symbolButton(image='newLayerSelected.png', annotation=mel.eval('uiRes("m_layerEditor.kCreateAnimLayer");'))
		empty_anim_layer_button = cmds.symbolButton(image='newLayerEmpty.png', annotation=mel.eval('uiRes("m_layerEditor.kCreateEmptyAnimLayer");'))

		move_selection_down_button = cmds.symbolButton(f'{window_name}MoveDownButton', image='moveLayerDown.png', annotation=mel.eval('uiRes("m_layerEditor.kMoveSelectionDownButton2");'))
		move_selection_up_button = cmds.symbolButton(f'{window_name}MoveUpButton', image='moveLayerUp.png', annotation=mel.eval('uiRes("m_layerEditor.kMoveSelectionUpButton2");'))
		anim_layer_weight_text = cmds.text(f'{window_name}WeightText', label=mel.eval('uiRes("m_layerEditor.kWeightAnimLayer");'))
		anim_layer_weight_field = cmds.floatField(f'{window_name}WeightField', width=33, precision=2, value=1.0)
		anim_layer_weight_slider = cmds.floatSlider(f'{window_name}WeightSlider', step=0.1, maxValue=1.0, minValue=0.0, value=1.0)
		anim_layer_weight_button = cmds.button(f'{window_name}WeightButton', label=mel.eval('uiRes("m_layerEditor.kKeyAnimLayers");'))

		buttons_on_right = cmds.optionVar(query='takeAnimLayerButtonsOnRight') if cmds.optionVar(exists='takeAnimLayerButtonsOnRight') else False
		reverse_layer_stack = cmds.optionVar(query='takeAnimLayerReverseLayerStack') if cmds.optionVar(exists='takeAnimLayerReverseLayerStack') else True
		self._anim_layer_editor = cmds.treeView(f'{window_name}AnimLayerEditor', numberOfButtons=4, attachButtonRight=buttons_on_right, reverseTreeOrder=reverse_layer_stack)

		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(zero_key_anim_layer_button, 'top', 1), (zero_key_anim_layer_button, 'left', 2)],
			attachNone=[(zero_key_anim_layer_button, 'bottom'), (zero_key_anim_layer_button, 'right')]
		)
		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(zero_weight_anim_layer_button, 'top', 1)],
			attachControl=[(zero_weight_anim_layer_button, 'left', 1, zero_key_anim_layer_button)],
			attachNone=[(zero_weight_anim_layer_button, 'bottom'), (zero_weight_anim_layer_button, 'right')]
		)
		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(full_weight_anim_layer_button, 'top', 1)],
			attachControl=[(full_weight_anim_layer_button, 'left', 1, zero_weight_anim_layer_button)],
			attachNone=[(full_weight_anim_layer_button, 'bottom'), (full_weight_anim_layer_button, 'right')]
		)
		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(selected_anim_layer_button, 'top', 1), (selected_anim_layer_button, 'right', 2)],
			attachNone=[(selected_anim_layer_button, 'bottom'), (selected_anim_layer_button, 'left')]
		)
		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(empty_anim_layer_button, 'top', 1)],
			attachControl=[(empty_anim_layer_button, 'right', 1, selected_anim_layer_button)],
			attachNone=[(empty_anim_layer_button, 'bottom'), (empty_anim_layer_button, 'left')]
		)
		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(move_selection_down_button, 'top', 1)],
			attachControl=[(move_selection_down_button, 'right', 4, empty_anim_layer_button)],
			attachNone=[(move_selection_down_button, 'bottom'), (move_selection_down_button, 'left')]
		)
		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(move_selection_up_button, 'top', 1)],
			attachControl=[(move_selection_up_button, 'right', 1, move_selection_down_button)],
			attachNone=[(move_selection_up_button, 'bottom'), (move_selection_up_button, 'left')]
		)
		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(anim_layer_weight_text, 'left', 2), (anim_layer_weight_text, 'bottom', 2)],
			attachNone=[(anim_layer_weight_text, 'right'), (anim_layer_weight_text, 'top')]
		)
		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(anim_layer_weight_field, 'bottom', 2)],
			attachControl=[(anim_layer_weight_field, 'left', 2, anim_layer_weight_text)],
			attachNone=[(anim_layer_weight_field, 'right'), (anim_layer_weight_field, 'top')]
		)
		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(anim_layer_weight_button, 'right', 2), (anim_layer_weight_button, 'bottom', 2)],
			attachNone=[(anim_layer_weight_button, 'left'), (anim_layer_weight_button, 'top')]
		)
		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(anim_layer_weight_slider, 'bottom', 2)],
			attachControl=[(anim_layer_weight_slider, 'left', 2, anim_layer_weight_field), (anim_layer_weight_slider, 'right', 2, anim_layer_weight_button)],
			attachNone=[(anim_layer_weight_slider, 'top')]
		)
		cmds.formLayout(
			anim_layer_form_layout, edit=True,
			attachForm=[(self._anim_layer_editor, 'left', 2), (self._anim_layer_editor, 'right', 4)],
			attachControl=[(self._anim_layer_editor, 'top', 2, selected_anim_layer_button), (self._anim_layer_editor, 'bottom', 2, anim_layer_weight_field)],
		)

		layer_available = animlayers.anim_layers_available()
		cmds.symbolButton(empty_anim_layer_button, edit=True, enable=layer_available, command=lambda *args: cmds.EmptyAnimLayer())

		cmds.scriptJob(compressUndo=True, parent=tab_layout, event=['SelectionChanged', self.update_anim_layer_editor])

		self.main_layout.addWidget(window_qt)

	def update_anim_layer_editor(self):

		selected = cmds.ls(selection=True, objectsOnly=True)
		layer_array = animlayers.all_anim_layers_ordered()
		best_layers = animlayers.best_anim_layers()
		affected_layers = animlayers.affected_anim_layers()

		cmds.treeView(self._anim_layer_editor, edit=True, removeAll=True)

		for anim_layer in layer_array:
			is_base_layer = False
			parent_layer = cmds.animLayer(anim_layer, query=True, parent=True)
			if parent_layer:
				grand_parent_layer = cmds.animLayer(parent_layer, query=True, parent=True)
				if not grand_parent_layer:
					parent_layer = None
			else:
				is_base_layer = True

			cmds.treeView(self._anim_layer_editor, edit=True, addItem=[anim_layer, parent_layer])

			show_namespace = cmds.optionVar(query='takeAnimLayerShowNamespace') if cmds.optionVar(exists='takeAnimLayerShowNamespace') else True
			name = animlayers.anim_layer_display_label(anim_layer, show_namespace=show_namespace)
			cmds.treeView(self._anim_layer_editor, edit=True, displayLabel=[anim_layer, name])

			cmds.treeView(self._anim_layer_editor, edit=True, image=(anim_layer, 1, 'Mute_OFF.png'))
			cmds.treeView(self._anim_layer_editor, edit=True, image=(anim_layer, 2, 'Solo_OFF.png'))
			cmds.treeView(self._anim_layer_editor, edit=True, image=(anim_layer, 3, 'Lock_OFF.png'))

			if is_base_layer:
				cmds.treeView(self._anim_layer_editor, edit=True, enableButton=(anim_layer, 3, False))

			buttons_on_right = cmds.optionVar(query='takeAnimLayerButtonsOnRight') if cmds.optionVar(exists='takeAnimLayerButtonsOnRight') else False
			reverse_layer_stack = cmds.optionVar(query='takeAnimLayerReverseLayerStack') if cmds.optionVar(exists='takeAnimLayerReverseLayerStack') else True
			cmds.treeView(self._anim_layer_editor, edit=True, attachButtonRight=buttons_on_right, reverseTreeOrder=reverse_layer_stack)

			self.update_editor_feedback_anim_layer(anim_layer, best_layers, affected_layers)

	def update_editor_feedback_anim_layer(self, anim_layer, best_layers, affected_layers):

		root_layer = cmds.animLayer(query=True, root=True)
		out_mute = f'{anim_layer}.outMute'
		parent_mute = f'{anim_layer}.parentMute'
		solo = f'{anim_layer}.solo'
		sibling_solo = f'{anim_layer}.siblingSolo'
		selected = f'{anim_layer}.selected'
		collapse = f'{anim_layer}.collapse'
		override = f'{anim_layer}.override'
		ghost = f'{anim_layer}.ghost'

		if not cmds.treeView(self._anim_layer_editor, query=True, itemExists=anim_layer):
			return

		out_mute_value = cmds.getAttr(out_mute) if root_layer != anim_layer else 0
		parent_mute_value = cmds.getAttr(parent_mute)
		solo_value = cmds.getAttr(solo)
		sibling_solo_value = cmds.getAttr(sibling_solo)
		selected_value = cmds.getAttr(selected)
		collapse_value = cmds.getAttr(collapse)
		override_value = cmds.getAttr(override)
		ghost_value = cmds.getAttr(ghost)
		sibling_solo_value_cumulative = sibling_solo_value if not solo_value and out_mute else False

		# Ensure the invisible buttons are truely transparent even in selection mode
		cmds.treeView(self._anim_layer_editor, edit=True, buttonErase=[anim_layer, False])

