import pebble, trees, pebbling_algos, utils
import shelve
import random # is this the right random number generator to use?

##### PRIMITIVE PROVER/VERIFIER SETUP #####
# Prover pebbles PTC graph, generates Merkle tree, and sends root to Verifier
# Verifier has Prover open n randomly chosen leaves of the MT, where n is
# 	defined in terms of r (currently it is set to n = 2*r)
# In each opening, Prover sends over an Opening object containing the leaf value
# 	and the sibling path.  Verifier then uses the Opening to recalculate the
# 	Merkle root, and compares it against the original one sent by Prover.
# If Prover passes all n test cases, then Verifier.verify() outputs True; other-
# 	wise, it outputs False.
#
# Note: in this version, Prover is completely honest (i.e. uses trivial_pebble)
# 	and stores the value of every PTC vertex using shelve), Verifier does not
# 	actually send over the sources, nor does he specifically check for the vali-
#	dity of some fixed number of sources.

filename = "merkle_tree.txt" # filename of the shelve storage file for Prover's MT

class Prover:
	def __init__(self, r, debug=False):
		self.debug = debug
		if self.debug:
			print "P: Starting up."
		self.r = r
		self.p = pebble.PebbleGraph(r)
		pebbling_algos.trivial_pebble(self.p, self.p.size()-1)

		# code to build MT
		#self.mt = trees.MerkleNode(self.p.list_values())
		self.mt = shelve.open(filename)
		self.mt["leaf_values"] = [""]*self.p.size()
		self.p.reset_seek()
		print self.p.size()
		for i in range(self.p.size()):
			self.mt["leaf_values"][i] = self.p.read_value_noseek()
		print len(self.mt["leaf_values"])
		self.mt["leaf_keys"] = trees.MT([0, self.p.size()], self.mt, "")

		if self.debug:
			print "P: Good to go, __init__ completed."

	def send_root(self):
		if self.debug:
			print "P: Sending over my Merkle root: "+self.mt[""][0] # "" is the key of the root, and [0] returns its value
		return self.mt[""][0]

	def open(self, i):
		leaf_value = utils.secure_hash(self.mt["leaf_values"][i])
		if self.debug:
			print "P: Opening that vertex, which has value "+leaf_value
		sibling_path = trees.mtopen(i, self.mt)
		if self.debug:
			print "P: The sibling path is: "
			print sibling_path
		return Opening(leaf_value, sibling_path)

	def close_files(self):
		if self.debug:
			print "P: Closing all my files.  Good night."
		self.p.close_files()
		self.mt.close()

class Verifier:
	# rroot is the received root from the prover -- verifier doesn't know for sure if the root is legitimate

	def __init__(self, r, debug=False):
		self.debug = debug
		if self.debug:
			print "V: Initializing."
		self.r = r
		self.n = 2*r # n is the number of vertices that the Verifier is going to open
		if self.debug:
			print "V: Initialization complete."

	def verify(self):
		if self.debug:
			print "V: Time to verify.  I will be checking "+str(self.n)+" randomly chosen vertices."
		self.receive_root()
		for x in range(self.n):
			i = self.choose_vertex()
			if self.debug:
				print "V: Verification trial #"+str(x+1)+" -- vertex index "+str(i)+"."
			result = self.verify_opening(self.prover.open(i))
			if self.debug:
				if result:
					print "V: Okay, you passed this one."
				else:
					print "V: ...which does NOT match your alleged root from earlier!"
			if not result:
				return False
		return True

	def set_prover(self, prover):
		self.prover = prover
		if self.debug:
			print "V: Prover set."

	def choose_vertex(self):
		return int(self.prover.p.size() * random.random())

	def receive_root(self):
		self.rroot = self.prover.send_root()
		if self.debug:
			print "V: Got your root."

	def verify_opening(self, opening): # returns True for pass, False for fail
		cur = opening.leaf_value
		if self.debug:
			print "V: Working my way up the Merkle tree..."
		for x in opening.sibling_path: # recall that x is a two-element array of the form [sibling_value, sibling_path]
			value = x[0]
			key = x[1]
			if key[-1] == 'R':
				cur = utils.secure_hash(cur+value)
			else:
				cur = utils.secure_hash(value+cur)
		if self.debug:
			print "V: Calculated root value is "+cur
		return cur == self.rroot

class Opening:
	def __init__(self, leaf_value, sibling_path):
		self.leaf_value = leaf_value
		self.sibling_path = sibling_path