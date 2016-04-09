import pebble
import utils

P = pebble.PebbleGraph(3) # change 3 to whatever r is supposed to be

# Depth-first pebble method as described in page 10 of the PTC paper.
# B: parent adjacency matrix; v: vertex to be pebbled.
# I'm not 100% sure what S is but it seems to be a set of all the vertices that call on v to be pebbled
def depth_first_pebble(P, v, S):
	if(is_source(v)):
		P.pebble(v)
	for u in P.get_parents(v):
		if(!pebbled(u)):
			depth_first_pebble(P, u, utils.union(S, P.get_parents(v)))
	P.pebble(v)
	P.remove_pebbles(utils.complement1(P.size(), S))