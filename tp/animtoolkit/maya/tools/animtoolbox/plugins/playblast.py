from tp.animtoolkit.maya.tools.animtoolbox import consts, abstract, widgets

PLUGIN_ID = 'playblast'


class PlayblastHotkeys(abstract.AbstractHotkeyFactory):

	ID = PLUGIN_ID

	def setup_hotkey_commands(self):

		self.set_category(consts.CATEGORIES.get('cameras'))

		self.add_command(
			name='incremental_playblast_avi', annotation='Incremental and Save Playblasts in AVI',
			command=['Playblast.make_playblast(ext="avi")'])


class PlayblastPlugin(abstract.AbstractToolPlugin):

	ID = PLUGIN_ID
	TOOL_NAME = 'Playblast'

	DEFAULT_DIRECTORY = 'c://playblasts//'

	def ui(self):
		super().ui()

		directory_widget = widgets.FilePathOptionVarWidget('animtoolbox_playblast_folder', self.DEFAULT_DIRECTORY)

		self.layout.addWidget(directory_widget)
		self.layout.addStretch()

		return self.option_widget

	def make_playblast(self, ext='mov'):
		print('Creating playblast ...', ext)
