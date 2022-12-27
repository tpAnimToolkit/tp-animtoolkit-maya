from tp.common.qt import api as qt


class AnimToolboxModel(qt.QObject):

	rotationOrderChanged = qt.Signal(int)
	selectionModeChanged = qt.Signal(int)

	changeRotationOrderEvent = qt.Signal()
	selectAnimatedNodesEvent = qt.Signal()
	setKeyChannelBoxEvent = qt.Signal()
	setKeyEvent = qt.Signal()
	makeAnimHoldEvent = qt.Signal()
	deleteKeyCurrentTimeEvent = qt.Signal()
	keyToggleVisibilityEvent = qt.Signal()
	resetAttributesEvent = qt.Signal()
	toggleControlCurvesVisibilityEvent = qt.Signal()

	def __init__(self):
		super(AnimToolboxModel, self).__init__()

		self._rotation_order = 0
		self._selection_mode = 0

	# =================================================================================================================
	# PROPERTIES
	# =================================================================================================================

	@property
	def rotation_order(self):
		return self._rotation_order

	@rotation_order.setter
	def rotation_order(self, index):
		self._rotation_order = index
		self.rotationOrderChanged.emit(self._rotation_order)

	@property
	def selection_mode(self):
		return self._selection_mode

	@selection_mode.setter
	def selection_mode(self, value):
		self._selection_mode = value
		self.selectionModeChanged.emit(self._selection_mode)
