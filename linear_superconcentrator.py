import shelve
import random

def superconcentrator(graph_num, extra, linear_parents):
    # graph_num must be an integer power of 2 greater than or equal to 128.
    
    graph_size = linear_sc_size(graph_num)
    for i in range(graph_size):
        linear_parents[str(i)] = [None, None, None, None, None, None, None]
        # The maximum number of parents any vertex should have in the linear superconcentrator is 7.

    # Now we build the linear superconcentrator graph from the bottom up using expander graphs.

    # The first half:
    i = graph_num
    current = 0
    # current is the location of the next expander graph we will add to the linear superconcentrator.
    while (i >= 128):
        expander_graph(i, current, linear_parents, extra)

        # This connects the left vertices in the expander graph to the vertices directly to the left.
        if current != 0:
            for n in range(current, current + i):
                linear_parents[str(n)] = [extra + n - 2*i, None, None, None, None, None, None]

        # This adds the extra edges connecting the right half of the expander graph to itself.  (1)
        if i > 128:
            for n in range(current + i, current + i + i/2):
                linear_parents[str(n)] = [linear_parents[str(n)][0], linear_parents[str(n)][1], linear_parents[str(n)][2], linear_parents[str(n)][3], linear_parents[str(n)][4], linear_parents[str(n)][5], extra + n + i/2]
            
        current = current + 2 * i
        i = i / 2
        # This loop goes for i over all powers of 2 from graph_num to 128 (inclusive).

    # The second half:
    i = 256
    while (i <= graph_num):
        expander_graph(i, current, linear_parents, extra)

        '''
        for n in range(current, current + i / 2):
            linear_parents[str(n)] = [extra + n - i/2, None, None, None, None, None, None]
            # This connects the top left vertices in the expander graph to the vertices directly to the left.
        for n in range(current + i/2, current + i):
            linear_parents[str(n)] = [extra + n - i/2, None, None, None, None, None, None]
            # This adds the edges connecting the left half of the expander graph to itself (2).
        for n in range(current, current + i / 2):
            linear_parents[str(n)] = [extra + n - i/2, extra + n - i/2 - linear_sc_size(i/2), None, None, None, None, None]
            # This adds the edges in the set (4).
        for n in range(current + i/2, current + i):
            linear_parents[str(n)] = [extra + n - i/2, extra + n - i*3/2 - linear_sc_size(i/2), None, None, None, None, None]
             # This adds the edges in the set (3).                         
        '''

        for n in range(current, current + i/2):
            linear_parents[str(n)] = [extra + n - i/2, extra + n - i/2 - linear_sc_size(i/2), None, None, None, None, None]
            # This connects the top left vertices in the expander graph to the vertices directly to the left.
            # It also adds the edges in the set (4).
        for n in range(current + i/2, current + i):
            linear_parents[str(n)] = [extra + n - i/2, extra + n - i*3/2 - linear_sc_size(i/2), None, None, None, None, None]
            # This adds the edges in the set (2).
            # It also adds the edges in the set (3).
        
        current = current + 2 * i
        i = i * 2
        # This loop goes over all powers of 2 from i = 256 to i = graph_num
        # Note: These four for loops are redundant. Only two are needed.
    
                       
def expander_graph(n, addend, expander_parents, extra):
    # n must be an integer power of 2 greater than or equal to 8.
    # for our purposes, we will always call n >= 128.

    # Add the parents of the left vertices
    for i in range(n):
        expander_parents[str(addend + i)] = [None, None, None, None, None, None, None]

    # Add the parents of the right vertices
    for i in range(n):
        parents = random.sample(range(n), 6)
        expander_parents[str(addend + i + n)] = [addend + extra + parents[0], addend + extra + parents[1], addend + extra + parents[2], addend + extra + parents[3], addend + extra + parents[4], addend + extra + parents[5], None]

    return expander_parents
        
            
def linear_sc_size(graph_num):
    return graph_num * 8 - 6 # graph_num is a power of 2.
