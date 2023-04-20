import maya.cmds as cmds

from tp.common.qt import api as qt
from tp.maya.cmds import optionvars


class OptionWidget(qt.QWidget):
	def __init__(self, label: str, parent: qt.QWidget = None):
		super().__init__(parent=parent)

		self._label_text = label
		self.ui()

	def ui(self):
		self.main_layout = qt.vertical_layout()
		self.setLayout(self.main_layout)

		self.scroll = qt.QScrollArea(parent=self)
		self.scroll.setVerticalScrollBarPolicy(qt.Qt.ScrollBarAsNeeded)
		self.scroll.setHorizontalScrollBarPolicy(qt.Qt.ScrollBarAsNeeded)
		self.scroll.setWidgetResizable(True)
		self.scroll_widget = qt.QWidget(parent=self)
		self.layout = qt.vertical_layout()
		self.scroll_widget.setLayout(self.layout)
		self.scroll.setWidget(self.scroll_widget)

		self.label = qt.label(self._label_text).h2()
		self.label.setAlignment(qt.Qt.AlignLeft | qt.Qt.AlignTop)
		self.layout.addWidget(self.label)

		self.main_layout.addWidget(self.scroll)


class FilePathOptionVarWidget(qt.QWidget):
	def __init__(self, option_var: str, default_value: str, parent: qt.QWidget = None):
		super().__init__(parent=parent)

		self._option_var = option_var
		self._path = optionvars.option_var(self._option_var, default_value)

		self.setLayout(qt.horizontal_layout())
		self._path_label = qt.label('Path:', parent=self)
		self._path_line_edit = qt.line_edit(text=self._path)
		self._directory_button = qt.button('Set folder', parent=self)
		self.layout().addWidget(self._path_label)
		self.layout().addWidget(self._path_line_edit)
		self.layout().addWidget(self._directory_button)

		self._directory_button.clicked.connect(self._on_directory_button_clicked)

	def _on_directory_button_clicked(self):

		folder_dialog = qt.QFileDialog(None, 'Pick Folder')
		folder_dialog.setDirectory(self._path)
		folder_dialog.setOption(qt.QFileDialog.DontUseNativeDialog, False)
		folder_dialog.setOption(qt.QFileDialog.ShowDirsOnly, True)
		selected_directory = folder_dialog.getExistingDirectory()
		if not selected_directory:
			return

		optionvars.set_option_var(self._option_var, selected_directory)
		self._path = selected_directory
		self._path_line_edit.setText(self._path)
