#!/usr/bin/python -t

import pebble
import utils

# Topmost call of dfp recursion
def depth_first_pebble(P, v):
    S = []
    S.append(v)
    dfp(P, v, S)

# Depth-first pebble method as described in page 10 of the PTC paper.
# B: parent adjacency matrix; v: vertex to be pebbled.
# I'm not 100% sure what S is but it seems to be a set of all the vertices that call on v to be pebbled
def dfp(P, v, S):
    if(P.is_source(v)):
        P.add_pebble(v)
        return
    for u in P.get_parents(v):
        if (u != -1): # I added this because if u = -1 then P doesn't have two parents.
            if(not P.is_pebbled(u)):
                dfp(P, u, utils.union(S, P.get_parents(v)))
    P.add_pebble(v)
    P.remove_pebbles(utils.complement1(P.size(), S))

def trivial_pebble(graph):
    for i in range (len(graph.B)):
        graph.add_pebble(i)
