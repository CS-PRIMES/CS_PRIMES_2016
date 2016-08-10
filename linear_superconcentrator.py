import shelve
import random

def superconcentrator(graph_num, extra, linear_parents):
    # graph_num must be an integer power of 2.
    
    graph_size = linear_sc_size(graph_num)
    for i in range(graph_size):
        linear_parents[str(i)] = [None, None, None, None, None, None, None]
        # The maximum number of parents any vertex should have in the linear superconcentrator is 7.

    # Now we build the linear superconcentrator graph from the bottom up using expander graphs.

    # The first half:
    i = graph_num
    current = 0
    # current is the location of the next expander graph we will add to the linear superconcentrator.
    while (i >= 1):
        expander_graph(i, current, linear_parents, extra)
        
        if current != 0:
            for n in range(current, current + i):
                linear_parents[str(n)] = [linear_parents[str(n)][0], linear_parents[str(n)][1], linear_parents[str(n)][2], linear_parents[str(n)][3], linear_parents[str(n)][4], linear_parents[str(n)][5], extra + n-2*i]
                # This connects the left vertices in the expander graph to the vertices directly to the left.
        for n in range(current + i, current + i + i/2):
            linear_parents[str(n)] = [linear_parents[str(n)][0], linear_parents[str(n)][1], linear_parents[str(n)][2], linear_parents[str(n)][3], linear_parents[str(n)][4], linear_parents[str(n)][5], extra + n + i/2]
            # This adds the extra edges connecting the right half of the expander graph to itself.  (1)
            
        current = current + 2 * i
        i = i / 2
        # This loop goes for i over all powers of 2 from graph_num to 1 (inclusive).

    # The second half:
    i = 2
    while (i <= graph_num):
        expander_graph(i, current, linear_parents, extra)

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
        current = current + 2 * i
        i = i * 2
        # This loop goes over all powers of 2 from i = 2 to i = graph_num
        # Note: These four for loops are redundant. Only two are needed.
    
                       
def expander_graph(n, addend, expander_parents, extra):
    # n must be an integer power of 2.
    
    if (n == 1):
        expander_parents[str(addend + 0)] = [None, None, None, None, None, None, None]
        expander_parents[str(addend + 1)] = [addend + extra + 0, None, None, None, None, None, None]
        return expander_parents
    
    for i in range(n):
        expander_parents[str(addend + i)] = [None, None, None, None, None, None, None]
        expander_parents[str(addend + i + n)] = [None, None, None, None, None, None, None] # The vertices in R may have up to 7 parents.
        
    for i in range(n):
        if (n == 2):
            expander_parents[str(addend + i + n)] = [addend + extra + 0, addend + extra + 1, None, None, None, None, None]
        elif (n == 4):
            expander_parents[str(addend + i + n)] = [addend + extra + 0, addend + extra + 1, addend + extra + 2, addend + extra + 3, None, None, None]
        else:
            parents = random.sample(range(n), 6)
            expander_parents[str(addend + i + n)] = [addend + extra + parents[0], addend + extra + parents[1], addend + extra + parents[2], addend + extra + parents[3], addend + extra + parents[4], addend + extra + parents[5], None]

    return expander_parents
        
            
def linear_sc_size(graph_num):
    return graph_num * 8 - 6 #graph_num is a power of 2.
