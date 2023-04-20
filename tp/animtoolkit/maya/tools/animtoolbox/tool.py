from tp.core import tool


from tp.animtoolkit.maya.tools.animtoolbox import model, view, controller


class AnimToolboxTool(tool.DccTool):

	def setup_ui(self):
		super(AnimToolboxTool, self).setup_ui()

		_model = model.AnimToolboxModel()
		self._controller = controller.AnimToolboxController(_model)
		self.ui = view.AnimToolboxView(model=_model)
