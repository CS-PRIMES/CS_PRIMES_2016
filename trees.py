import utils

class MerkleNode(object):
	def __init__(self, leaf_values, parent=None, sibling=None, prehashed=False):
		self.size = len(leaf_values)
		self.parent = parent
		self.sibling = sibling
		self.leaf_values = leaf_values
		self.leaves = None
		if self.size == 1:
			if prehashed:
				self.value = leaf_values[0]
			else:
				self.value = utils.secure_hash(leaf_values[0])
			self.left = None
			self.right = None
			self.leaves = [self]
		if self.size > 1:
			self.left = MerkleNode(leaf_values[:self.size/2], self, prehashed)
			self.right = MerkleNode(leaf_values[self.size/2:], self, prehashed)
			self.left.sibling = self.right
			self.right.sibling = self.left
			self.value = utils.secure_hash(self.left.value+self.right.value)
			self.leaves = self.left.leaves + self.right.leaves

	def list_leaf_values(self):
		if self.size > 1:
			return self.left.list_leaf_values()+", "+self.right.list_leaf_values()
		else:
			return str(self.value)

	def root(self):
		return self.value

	def open(self, i): # opens the ith leaf (i.e. the ith vertex of the ptc graph)
		leaf = self.leaves[i]
		cur = leaf
		path = []
		while cur != self:
			path.append(cur)
			cur = cur.parent
		return path