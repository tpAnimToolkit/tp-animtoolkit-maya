class AnimToolboxController(object):
	def __init__(self, model):
		super().__init__()

		self._model = model									# type: tp.animtoolkit.maya.tools.animtoolbox.model.AnimToolboxModel