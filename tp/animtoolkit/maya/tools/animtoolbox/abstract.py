from __future__ import annotations

import re
import abc

from tp.animtoolkit.maya.tools.animtoolbox import widgets

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class AbstractToolPlugin(ABC):

	_INSTANCE = None
	ORDER = 0
	TOOL_NAME = 'baseTool'

	def __new__(cls):
		if AbstractToolPlugin._INSTANCE is None:
			AbstractToolPlugin._INSTANCE = object.__new__(cls)

		AbstractToolPlugin._INSTANCE.val = cls.TOOL_NAME
		return AbstractToolPlugin._INSTANCE

	@abc.abstractmethod
	def ui(self):
		tool_ui_name = re.sub("([a-z])([A-Z])", "\g<1> \g<2>", self.TOOL_NAME)
		self.option_widget = widgets.OptionWidget(label=tool_ui_name)
		self.layout = self.option_widget.layout

		return self.option_widget

	def hotkey_ui(self):
		tool_ui_name = re.sub("([a-z])([A-Z])", "\g<1> \g<2>", self.TOOL_NAME)
		self.hotkey_widget = widgets.OptionWidget(label=tool_ui_name)
		self.layout = self.hotkey_widget.layout

		return self.hotkey_widget


class AbstractHotkeyFactory(ABC):

	CATEGORY = 'tpAnimToolbox'
	COMMANDS_LIST = list()

	class AnimToolboxHotkey(object):
		def __init__(
				self, name: str = '', annotation: str = '', category: str = 'tpAnimToolbox', ctx: str = '',
				language: str = 'python', command: list[str] = None, help_str: str = ''):
			super().__init__()

			self._name = name
			self._annotation = annotation
			self._ctx = ctx
			self._category = category
			self._language = language
			self._command = ''
			self._hotkey_name = self._name + 'NameCommand'

	@abc.abstractmethod
	def setup_hotkey_commands(self):
		pass

	def add_command(
			self, name: str = '', annotation: str = '', category: str = 'tpAnimToolbox', ctx: str = '',
			language: str = 'python', command: list[str] = None, help_str: str = ''):
		self.COMMANDS_LIST.append(
			AbstractHotkeyFactory.AnimToolboxHotkey(
				name=name, annotation=annotation, category=category or self.CATEGORY, ctx=ctx, language=language,
				command=command, help_str=help_str))

	def set_category(self, category: str):
		self.CATEGORY = category
