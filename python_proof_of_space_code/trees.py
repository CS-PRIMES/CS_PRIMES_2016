# This file is no longer used in our implementation of Proof of Space.

import utils

# shelf[key] = [value, leaf_range, isLeaf]
def MT(leaf_range, shelf, key, prehashed=False): # recursively generates merkle tree
	size = leaf_range[1]-leaf_range[0] # number of leaves under (and possibly including) the current node
	value = None
	if size == 1: # if it is a leaf
		if prehashed:
			value = shelf["leaf"+str(leaf_range[0])]
		else:
			value = utils.secure_hash(shelf["leaf"+str(leaf_range[0])])
		shelf[key] = [value, leaf_range, True]
		return [key]
	else:
		left_range = [leaf_range[0], leaf_range[0]+size/2]
		right_range = [leaf_range[0]+size/2, leaf_range[1]]
		left_keys = MT(left_range, shelf, key+'L', prehashed)
		right_keys = MT(right_range, shelf, key+'R', prehashed)
		value = utils.secure_hash(shelf[key+'L'][0]+shelf[key+'R'][0])
		shelf[key] = [value, leaf_range, False]
		return left_keys + right_keys

def mtopen(leaf_index, shelf): # returns sibling path of the chosen leaf
	leaf_key = shelf["leaf_keys"][leaf_index]
	cur_key = leaf_key
	path = []
	while cur_key != "":
		sibling_key = _sibling(cur_key)
		path.append([shelf[sibling_key][0], sibling_key]) # append the two-element array [sibling_value, sibling_key] to the path
		cur_key = cur_key[:-1]
	return path

def _sibling(key):
	if key == "":
		return None
	elif key[-1] == 'L':
		return key[:-1]+'R'
	else:
		return key[:-1]+'L'



#########################################
## OLD CODE BELOW, DOES NOT USE SHELVE ##
#########################################

class MerkleNode(object):

	# Constructor for MerkleNode object.
	# leaf_values: an array containing the values of the leaves of the tree
	# parent: self-explanatory
	# prehashed: whether the leaf values are hashed already or not
	# IMPORTANT: leaf_values may or may not be hashed, so when accessing the value of a leaf,
    #	it is always best to use mt.leaves[i].value instead of mt.leaf_values[i] for consistency.
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
			self.leaves = self.left.leaves + self.right.leaves # note leaves is an array

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
