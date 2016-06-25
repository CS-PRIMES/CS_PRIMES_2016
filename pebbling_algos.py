#!/usr/bin/python -t

import pebble
import utils

# Trivial pebbling algorithm: literally just pebble everything.  Relies on the property that if i is a parent of j, then i < j.

def trivial_pebble(P, i):
    for i in range(0, i):
         P.add_pebble(i)

# Depth-first pebble method as described in page 10 of the PTC paper.
# B: parent adjacency matrix; v: vertex to be pebbled.
# I'm not 100% sure what S is but it seems to be a set of all the vertices that call on v to be pebbled...
# NOTE: the last line of dfp is now commented out in order to make it essentially equivalent to the trivial pebble implementation

# Topmost call of dfp recursion
def depth_first_pebble(P, v):
    S = set([v])
    dfp(P, v, S)

def dfp(P, v, S):
    if P.is_source(v):
        P.add_pebble(v)
        return
    for u in P.get_parents(v):
        if not P.is_pebbled(u):
            dfp(P, u, S | set(P.get_parents(v)))
    P.add_pebble(v)
    P.remove_pebbles(set(range(P.size())) - S)
