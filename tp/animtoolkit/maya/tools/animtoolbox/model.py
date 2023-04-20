from tp.common.plugin import factory
from tp.common.qt import api as qt

from tp.animtoolkit.maya.tools.animtoolbox import abstract


class AnimToolboxModel(qt.QObject):

	def __init__(self):

		super().__init__()

		self._plugins_manager = factory.PluginFactory(abstract.AbstractToolPlugin, plugin_id='ID')
		self._hotkeys_manager = factory.PluginFactory(abstract.AbstractHotkeyFactory, plugin_id='ID')
		self._plugins_manager.register_paths_from_env_var('TPDCC_ANIMTOOLBOX_PLUGIN_PATHS')
		self._hotkeys_manager.register_paths_from_env_var('TPDCC_ANIMTOOLBOX_PLUGIN_PATHS')

	@property
	def plugins_manager(self) -> factory.PluginFactory:
		return self._plugins_manager

	@property
	def hotkeys_manager(self) -> factory.PluginFactory:
		return self._hotkeys_manager
