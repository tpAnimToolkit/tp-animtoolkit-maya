import maya.mel as mel
import maya.cmds as cmds

from tp.common.qt import api as qt
from tp.animtoolkit.maya.tools.takesmanager import widgets, layereditor


class TakesManagerView(qt.BaseWidget):

	def ui(self):
		super().ui()

		self.take_content_tab = qt.QTabWidget()

		# Anim Layers Content
		self.anim_layers_content_wgt = qt.QWidget()
		self.anim_layers_content_wgt.setLayout(qt.vertical_layout())
		self.take_content_tab.addTab(self.anim_layers_content_wgt, 'Anim Layers')
		self.anim_layers_editor = layereditor.TakesAnimLayersEditor(parent=self)
		self.anim_layers_content_wgt.layout().addWidget(self.anim_layers_editor)

		# Takes
		self.takes_group = qt.QGroupBox('Takes')
		self.takes_group.setLayout(qt.vertical_layout())
		self.takes_list = widgets.TakesListWidget(self)
		self.takes_group.layout().addWidget(self.takes_list)

		self.main_layout.addWidget(self.take_content_tab)
		self.main_layout.addWidget(self.takes_group)

	def setup_signals(self):
		super().setup_signals()
