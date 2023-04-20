from tp.core import tool

from tp.animtoolkit.maya.tools.takesmanager import view


class TakesManagerTool(tool.DccTool):

	def setup_ui(self):
		super().setup_ui()

		self.ui = view.TakesManagerView()
