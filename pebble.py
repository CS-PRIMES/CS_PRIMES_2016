import utils
import ptc

class PebbleGraph:
	pebble = []
	B = []
	def __init__(self, r):
		self.B = utils.tpl_to_adj(ptc.PTC(r,0))
		self.pebble = [False]*len(self.B)

	def is_pebbled(self, v):
		return self.pebble[v]

	def remove_pebble(self, v):
		if(self.is_pebbled(v)):
			print "Pebble removed from node "+str(v)
		self.pebble[v] = False

	def remove_pebbles(self, S):
		for v in S:
			self.remove_pebble(v)

	def reset(self):
		self.pebble = [False]*len(self.B)

	def add_pebble(self, v):
		if(self.is_source(v)):
			if(not self.is_pebbled(v)):
				print "Pebble added to node "+str(v)
			self.pebble[v] = True
			return
		if(self.is_pebbled(self.B[v][0]) and self.is_pebbled(self.B[v][1])):
			if(not self.is_pebbled(v)):
				print "Pebble added to node "+str(v)
			self.pebble[v] = True
			return
		print "Error: attempted to pebble node "+str(v)+" without pebbling both parents"

	def is_source(self, v):
		return (self.B[v][0] == -1 and self.B[v][1] == -1)

	def get_parents(self, v):
		return self.B[v]

	def size(self):
		return len(self.B)

	def pebble_list(self):
		return self.pebble

	def graph(self):
		return self.B