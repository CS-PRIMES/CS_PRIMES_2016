import utils
import ptc

class PebbleGraph:
	pebble = []
	B = []
	def __init__(self, r):
		self.B = utils.tpl_to_adj(ptc.PTC(r,0))
		self.pebble = [False]*len(self.B)

	def pebbled(self, v):
		return self.pebble[v]

	def remove_pebble(self, v):
		self.pebble[v] = false

	def remove_pebbles(self, S):
		for v in S:
			self.remove_pebble(V)

	def reset(self):
		self.pebble = [False]*len(self.B)

	def add_pebble(self, v):
		if(self.is_source(v)):
			self.pebble[v] = True
			return
		if(self.pebbled(self.B[v][0]) and self.pebbled(self.B[v][1])):
			self.pebble[v] = True
			return
		return -1

	def is_source(self, v):
		return (self.B[v][0] == -1 and self.B[v][1] == -1)

	def get_parents(self, v):
		return self.B[v]

	def size(self):
		return len(self.B)