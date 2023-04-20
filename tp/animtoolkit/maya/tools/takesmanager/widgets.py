import importlib

from tp.common.qt import api as qt
from tp.animtoolkit.maya.tools.takesmanager import take


class TakesListWidget(qt.QListWidget):
	def __init__(self, parent=None):
		super(TakesListWidget, self).__init__(parent)

		self.setContextMenuPolicy(qt.Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self._on_custom_context_menu_requested)

	def _on_custom_context_menu_requested(self, pos):
		menu = qt.QMenu()
		new_take_action = qt.QAction('New Take')
		new_take_action.triggered.connect(self._on_create_new_take_action_triggered)
		menu.addAction(new_take_action)
		menu.exec_(self.mapToGlobal(pos))

	def _on_create_new_take_action_triggered(self):
		new_take = take.create_new_take()
		new_take_widget = TakeWidget(take=new_take)
		new_take_item = qt.QListWidgetItem()
		self.addItem(new_take_item)
		self.setItemWidget(new_take_item, new_take_widget)


class TakeWidget(qt.QWidget):

	class TakeLabel(qt.QLabel):

		doubleClicked = qt.Signal()

		def mouseDoubleClickEvent(self, event):
			if not isinstance(event, qt.QMouseEvent):
				return
			self.doubleClicked.emit()

	def __init__(self, take, parent=None):
		super(TakeWidget, self).__init__(parent)

		self._take = take

		self.setContextMenuPolicy(qt.Qt.CustomContextMenu)

		self.create_widgets()
		self.create_layout()
		self.create_connections()

	def create_widgets(self):
		self.take_label = TakeWidget.TakeLabel(self._take.name)

	def create_layout(self):
		self.main_layout = qt.vertical_layout()
		self.main_layout.setContentsMargins(2, 2, 2, 2)
		self.main_layout.setSpacing(2)
		self.setLayout(self.main_layout)

		self.main_layout.addWidget(self.take_label)
		self.main_layout.addStretch()

	def create_connections(self):
		self.customContextMenuRequested.connect(self._on_custom_context_menu_requested)

	def _on_custom_context_menu_requested(self, pos):
		menu = qt.QMenu()
		rename_take_action = qt.QAction('Rename')
		rename_take_action.triggered.connect(self._on_rename_take_action_triggered)
		set_color_take_action = qt.QAction('Set Color')
		set_color_take_action.triggered.connect(self._on_set_color_take_action_triggered)
		menu.addAction(rename_take_action)
		menu.addAction(set_color_take_action)
		menu.exec_(self.mapToGlobal(pos))

	def _on_rename_take_action_triggered(self):

		take_name = self._take.name
		new_name, valid = qt.QInputDialog.getText(
			None,
			'Rename {}'.format(take_name),
			'New name for {}'.format(take_name),
			qt.QLineEdit.Normal,
			take_name
		)
		if not valid or not new_name or new_name == take_name:
			return

		self._take.name = new_name
		self.take_label.setText(self._take.name)

	def _on_set_color_take_action_triggered(self):
		pass
