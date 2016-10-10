import pebble
import utils
import ptc

# TRIVIAL PEBBLE METHOD, literally just pebble everything
# Relies on the property that if i is a parent of j, then i < j

# Pebbles up to and including vertex i.
def trivial_pebble(P, i):
    for i in range(i+1):
         P.add_pebble(i)

# Pebbles an entire linear ptc graph from sources to sinks. Never removes pebbles.
def linear_trivial_pebble(graph):
    position = 0
    while (position < graph.size):
        graph.all_graphs.seek(graph.all_graphs_start + 7 * position * graph.all_graphs_increment + 6 * graph.all_graphs_increment)
        last_parent = graph.all_graphs.read(graph.all_graphs_increment)
        if last_parent == "\00" * graph.all_graphs_increment:
            for i in range(position, position + 128):
                graph.add_pebble(i)
            position += 128
        # Only occurs if we are in the right vertices of an expander graph.
        else:
            i = position + 2 * (last_parent - position) - 1
            while (i >= position):
                graph.add_pebble(i)
                i = i - 1
            position += 2 * (last_parent - position)

    
# DEPTH-FIRST PEBBLE METHOD, as described in page 10 of the PTC paper.
# B: parent adjacency matrix; v: vertex to be pebbled.
# I'm not 100% sure what S is but it seems to be a set of all the vertices that call on v to be pebbled...
# NOTE: the last line of dfp is now commented out in order to make it essentially equivalent to the trivial pebble implementation

# Topmost call of DFP recursion
def depth_first_pebble(P, v):
    S = set([v])
    dfp(P, v, S)

# Pebbles vertex v
def dfp(P, v, S):
    if P.is_source(v):
        P.add_pebble(v)
        return
    for u in P.get_parents(v):
        if not P.is_pebbled(u):
            dfp(P, u, S | set(P.get_parents(v)))
    P.add_pebble(v)
    P.remove_pebbles(set(range(P.size)) - S)

# LEVEL PEBBLE METHOD, intuitively graph level by level
# v does nothing at this point
# Goes level by level, means super concentrator must be leveled
# Only pebbles sinks, as pebbling a specific vertex is very ugly

# Topmost call of Level recursion
def level_pebble(P, v):
    for i in range(2**P.graph_num):
        P.add_pebble(i)
    level_ptc(P, v, P.graph_num, 0)

# Pebbles PTC's Sinks
def level_ptc(P, v, r, addend):
    if r == 1:
        level_sc(P, v, 1, addend)
    else:
        ptc_size = ptc.ptcsize(r-1)
        sc_size  = ptc.scsize(r-1)

        # pebble sources of sc1
        for i in range(0, 2**(r-1)):
            P.add_pebble(addend + 2**r + i)

        # pebble sc1
        level_sc(P, v, r-1, addend + 2**r)

        # pebble sources of ptc1
        for i in range(0, 2**(r-1)):
            P.add_pebble(addend + 2**r + sc_size + i)
            P.remove_pebble(addend + 2**(r-1) + sc_size + i)

        # pebble ptc1
        level_ptc(P, v, r-1, addend + 2**r + sc_size)

        # pebble sources of ptc2
        for i in range(0, 2**(r-1)):
            P.add_pebble(addend + 2**r + sc_size + ptc_size + i)
            P.remove_pebble(addend + 2**(r-1) + sc_size + ptc_size + i)

        # pebble ptc2
        level_ptc(P, v, r-1, addend + 2**r + sc_size + ptc_size)

        # pebble sources of sc2
        for i in range(0, 2**(r-1)):
            P.add_pebble(addend + 2**r + sc_size + 2*ptc_size + i)
            P.remove_pebble(addend + 2**(r-1) + sc_size + 2*ptc_size + i)

        # pebble sc2
        level_sc(P, v, r-1, addend + 2**r + sc_size + 2*ptc_size)

        # pebble sinks of PTC
        for i in range(0, 2**r):
            P.add_pebble(addend + 2**r + 2*sc_size + 2*ptc_size + i)
            P.remove_pebble(addend + i)
            if i >= 2**(r-1):
                P.remove_pebble(addend + 2*sc_size + 2*ptc_size + i)

# Pebbles SC's Sinks
def level_sc(P, v, r, addend):
    level_butterfly(P, v, r, addend)

# Pebbles Butterfly's Sinks
def level_butterfly(P, v, r, addend):
    for level in range(1, 2*r):
        for i in range(2**r):
            P.add_pebble(addend + (level)*(2**r) + i)
        for i in range(2**r):
            P.remove_pebble(addend + (level-1)*(2**r) + i)
