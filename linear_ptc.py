# This program creates a ptc graph using linear superconcentrators.

import shelve
import linear_superconcentrator # file for superconcentrators

def linear_PTC(r, all_parents):
    all_parents[str(1)] = [[None, None, None, None, None, None, None], [0, None, None, None, None, None, None]]
    
    for graph_size in range (2, r+1):
        sc_size = linear_sc_size(graph_size-1) # The size of the superconcentrator we will be using to create this ptc graph.
        ptc_size = linear_ptcsize(graph_size-1) # The size of the previous ptc graph.
        all_parents[str(graph_size)] = []
        for i in range(linear_ptcsize(graph_size)):
            all_parents[str(graph_size)].append([None, None, None, None, None, None, None])
            
        # Adds Sources
        for i in range(2**(graph_size-1)):
            all_parents[str(graph_size)][i] = [None, None, None, None, None, None, None]
                
        # Adds 1st SC copy
        sc1 = shelve.open('sc1.txt')
        linear_superconcentrator.superconcentrator(2**(graph_size-2), 2**(graph_size-1), sc1)

        for i in range(2**(graph_size-2)):
            sc1[str(i)] = [i, i + 2**(graph_size-2), None, None, None, None, None]

        n = 0
        for i in range(2**(graph_size-1), 2**(graph_size-1) + sc_size):
            all_parents[str(graph_size)][i] = [sc1[str(n)][0], sc1[str(n)][1], sc1[str(n)][2], sc1[str(n)][3], sc1[str(n)][4], sc1[str(n)][5], sc1[str(n)][6]]
            n = n + 1

        sc1.close()
            
        # Adds 1st PTC copy
        n = 0
        for i in range(2**(graph_size-1) + sc_size, 2**(graph_size-1) + sc_size + 2**(graph_size-2)):
            all_parents[str(graph_size)][i] = [2**(graph_size-1) + sc_size - 2**(graph_size-2) + n, None, None, None, None, None, None]
            n = n + 1

        for i in range(2**(graph_size-1) + sc_size + 2**(graph_size-2), 2**(graph_size-1) + sc_size + ptc_size):
            vertex = [None, None, None, None, None, None, None]
            for g in range(7):
                if all_parents[str(graph_size-1)][n][g] != None:
                    vertex[g] = all_parents[str(graph_size-1)][n][g] + 2**(graph_size-1) + sc_size
            all_parents[str(graph_size)][i] = vertex
            n = n + 1
            
        # Adds 2nd PTC copy
        n = 0
        for i in range(2**(graph_size-1) + sc_size + ptc_size, 2**(graph_size-1) + sc_size + ptc_size + 2**(graph_size-2)):
            all_parents[str(graph_size)][i] = [2**(graph_size-1) + sc_size + ptc_size - 2**(graph_size-2) + n, None, None, None, None, None, None]
            n = n + 1

        for i in range(2**(graph_size-1) + sc_size + ptc_size + 2**(graph_size-2), 2**(graph_size-1) + sc_size + ptc_size + ptc_size):
            vertex = [None, None, None, None, None, None, None]
            for g in range(7):
                if all_parents[str(graph_size-1)][n][g] != None:
                    vertex[g] = all_parents[str(graph_size-1)][n][g] + 2**(graph_size-1) + sc_size + ptc_size
            all_parents[str(graph_size)][i] = vertex
            n = n + 1
                    
        # Adds 2nd SC copy
        sc2 = shelve.open('sc2.txt')
        linear_superconcentrator.superconcentrator(2**(graph_size-2), 2**(graph_size-1) + sc_size + ptc_size + ptc_size, sc2)
        
        for i in range(2**(graph_size-2)):
            sc2[str(i)] = [2**(graph_size-1) + sc_size + ptc_size + ptc_size + i - 2**(graph_size-2), None, None, None, None, None, None]

        n = 0
        for i in range(2**(graph_size-1) + sc_size + ptc_size + ptc_size, 2**(graph_size-1) + sc_size + ptc_size + ptc_size + sc_size):
            all_parents[str(graph_size)][i] = [sc2[str(n)][0], sc2[str(n)][1], sc2[str(n)][2], sc2[str(n)][3], sc2[str(n)][4], sc2[str(n)][5], sc2[str(n)][6]]
            n = n + 1

        sc2.close()
        
        sofar = 2**(graph_size-1) + 2 * sc_size + 2 * ptc_size
        
        # Adds Sinks
        for i in range(2**(graph_size-1)):
            all_parents[str(graph_size)][i+sofar] = [sofar - 2**(graph_size-2) + (i % 2**(graph_size-2)), i, None, None, None, None, None]
            

def linear_ptcsize(r):
    # This returns the size of the rth ptc graph with linear superconcentrators.
    # The first of these ptc graphs is of size 2.
    if r == 1:
        return 2
    else:
        return 2 * (2**(r-1)) + 2 * linear_sc_size(r-1) + 2 * linear_ptcsize(r-1)
    
def linear_sc_size(r):
    # This function takes any positive integer r and returns the size of the rth linear superconcenetrator.
    # The first linear superconcentrator is of size 2.
    return 2**(r-1) * 8 - 6
