import utils

class MerkleNode(object):

	# Constructor for MerkleNode object.
	# leaf_values: an array containing the values of the leaves of the tree
	# parent: self-explanatory
	# prehashed: whether the leaf values are hashed already or not
	# IMPORTANT: leaf_values may or may not be hashed, so when accessing the value of a leaf,
    #	it is always best to use mt.leaves[i].value instead of mt.leaf_values[i].
	def __init__(self, leaf_values, parent=None, prehashed=False):
		self.size = len(leaf_values)
		self.parent = parent
		self.leaf_values = leaf_values
		self.leaves = None
		self.on_right = None
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
			self.left.on_right = False
			self.right.on_right = True
			self.value = utils.secure_hash(self.left.value+self.right.value)
			self.leaves = self.left.leaves + self.right.leaves

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