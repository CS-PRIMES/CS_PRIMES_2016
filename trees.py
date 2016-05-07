import utils

class MerkleNode(object):
	def __init__(self, leaves, parent=None, prehashed=False):
		self.size = len(self.leaves)
		if(self.size == 1):
			if prehashed:
				self.value = data
			else:
				self.value = utils.secure_hash(data).digest()
			self.left = None
			self.right = None
			self.parent = self
		if(self.size > 1):
			self.left = MerkleNode(leaves[:self.size/2], self, prehashed)
			self.right = MerkleNode(leaves[self.size/2:], self, prehashed)
			self.value = utils.secure_hash(self.left.value.decode('hex')+self.right.value.decode('hex')).digest()

######################## IGNORE STUFF BELOW ########################

class MerkleTree(object):
	def __init__(self, leaves=[], prehashed=False):
		if prehashed:
			self.leaves = [Node(leaf.decode('hex'), prehashed=True) for leaf in leaves]
		else:
			self.leaves = [Node(leaf) for leaf in leaves]
		self.root = None

	def add(self, data, prehashed=False):
		if prehashed:
			self.leaves.append(Node(data.decode('hex'), prehashed=True))
		else:
			self.leaves.append(Node(data))

	def clear(self):
		self.root = None
		for leaf in self.leaves:
			leaf.left, leaf.right, leaf.parent, leaf.sibling, leaf.side = [None]*5

	def _build(self, leaves):
		

class Node(object):
	def __init__(self, data, prehashed=False):
		if prehashed:
			self.value = data
		else:
			self.value = utils.secure_hash(data).digest()
		self.left = None
		self.right = None
		self.parent = None
		self.sibling = None
		self.side = None

	def __repr__(self):
		return "Value: <"+str(self.value.encode('hex'))+">"