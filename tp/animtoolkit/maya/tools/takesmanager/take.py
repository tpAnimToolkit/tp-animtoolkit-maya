import maya.cmds as cmds

from tp.maya.cmds import contexts


def all_take_nodes():

	found_network_nodes = list()
	network_nodes = cmds.ls(type='network')
	for network_node in network_nodes:
		if not cmds.attributeQuery('isTake', node=network_node, exists=True):
			continue
		found_network_nodes.append(network_node)

	return [Take(network_node) for network_node in found_network_nodes]


def unique_take_name(name=None):

	name = name or 'Take_{}'.format(name, '1'.zfill(3))
	take_names = [take_node.name for take_node in all_take_nodes()]
	if not take_names:
		return name

	index = 1
	while name in take_names:
		name = '_'.join(name.split('_')[:-1]) + '_{}'.format(str(index).zfill(3))
		index += 1

	return name


def take_exits(take_name):

	take_names = [take_node.name for take_node in all_take_nodes()]
	return True if take_name in take_names else False



def create_new_take(name='Take_001'):

	new_take = Take()
	new_take.create(name=unique_take_name(name))

	return new_take


class Take(object):
	def __init__(self, node=None):
		super(Take, self).__init__()

		self._node = node

	@property
	def node(self):
		return self._node

	@property
	def name(self):
		return cmds.getAttr('{}.takeName'.format(self._node)) if self.exists() else 'Take_001'

	@name.setter
	def name(self, value):
		if not self.exists():
			return
		if take_exits(value):
			cmds.warning('Take with name "{}" already exists. Skipping take rename!'.format(value))
			return
		with contexts.unlock_attribute_context(self._node, 'takeName'):
			cmds.setAttr('{}.takeName'.format(self._node), value, type='string')

	@property
	def frame_range(self):
		if not self.exists():
			return [0, 0]

		return [cmds.getAttr('{}.startFrame'.format(self._node)), cmds.getAttr('{}.endFrame'.format(self._node))]

	@frame_range.setter
	def frame_range(self, value):
		if not self.exists():
			return
		with contexts.unlock_attribute_context(self._node, 'startFrame'):
			cmds.setAttr('{}.startFrame'.format(self._node), value[0])
		with contexts.unlock_attribute_context(self._node, 'endFrame'):
			cmds.setAttr('{}.endFrame'.format(self._node), value[1])

	def exists(self):
		return True if self._node and cmds.objExists(self._node) else False

	def create(self, name):
		if self._node:
			cmds.warning('Take is already created: {}'.format(self._node))
			return False

		self._node = cmds.createNode('network', name='take_#')
		cmds.addAttr(self._node, ln='isTake', at='bool', k=False)
		cmds.setAttr('{}.isTake'.format(self._node), True, l=True)
		cmds.addAttr(self._node, ln='takeName', dt="string")
		cmds.setAttr("{}.takeName".format(self._node), unique_take_name(name), k=False, l=True, type="string")

		return True
