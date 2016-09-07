# This program creates a ptc graph using linear superconcentrators.

import linear_superconcentrator # file for superconcentrators

# Notes:
# 1. all_parents is the file in which the ptc graphs are stored.
#     Remember, each key holds a two dimensional array.
# 2. The first PTC graph (for r = 1) is an expander graph of total size 256.
#     This first linear superconcentrator is also an expander graph of total size 256.

def linear_PTC(r, all_parents):
    all_parents.seek(0)

    graph_increment = len(str(linear_ptcsize(1)))
    all_parents.write("\00" * 7 * graph_increment * 128)
    linear_superconcentrator.superconcentrator(128, 0, all_parents, graph_increment)

    for graph_num in range (2, r+1):
        graph_start = all_graphs_start(graph_num)
        graph_increment = len(str(linear_ptcsize(graph_num)))
        previous_graph_start = all_graphs_start(graph_num-1)
        previous_graph_increment = len(str(linear_ptcsize(graph_num-1)))
        sc_size = linear_sc_size(graph_num-1) # The size of the superconcentrator we will be using to create this ptc graph.
        ptc_size = linear_ptcsize(graph_num-1) # The size of the previous ptc graph.
            
        # Adds Sources
        all_parents.write("\00" * 7 * graph_increment * 2**(graph_num+6))
                
        # Adds 1st SC copy
        for i in range(2**(graph_num+5)):
            first_leading_zero = graph_increment - len(str(i))
            second_leading_zero = graph_increment - len(str(i + 2**(graph_num+5)))
            all_parents.write("0" * first_leading_zero + str(i) + "0" * second_leading_zero + str(i + 2**(graph_num+5)) + "\00" * 5 * graph_increment)
            
        linear_superconcentrator.superconcentrator(2**(graph_num+5), 2**(graph_num+6), all_parents, graph_increment)

        # Adds 1st PTC copy
        for i in range(2**(graph_num+5)):
            leading_zero = graph_increment - len(str(2**(graph_num+6) + sc_size - 2**(graph_num+5) + i))
            all_parents.write("0" * leading_zero + str(2**(graph_num+6) + sc_size - 2**(graph_num+5) + i) + "\00" * graph_increment * 6)

        for i in range(2**(graph_num+5), ptc_size):
            all_parents.seek(previous_graph_start + i * 7 * previous_graph_increment)
            parents = []
            for g in range(7):
                parents.append(all_parents.read(previous_graph_increment))
            all_parents.seek(graph_start + (2**(graph_num+6) + sc_size + i) * 7 * graph_increment)
            for g in range(7):
                if parents[g] == "\00" * previous_graph_increment:
                    all_parents.write("\00" * graph_increment)
                else:
                    leading_zero = graph_increment - len(str(int(parents[g])))
                    all_parents.write("0" * leading_zero + str(int(parents[g])))
            
        # Adds 2nd PTC copy
        for i in range(2**(graph_num+5)):
            leading_zero = graph_increment - len(str(2**(graph_num+6) + sc_size + ptc_size - 2**(graph_num+5) + i))
            all_parents.write("0" * leading_zero + str(2**(graph_num+6) + sc_size + ptc_size - 2**(graph_num+5) + i) + "\00" * graph_increment * 6)

        for i in range(2**(graph_num+5),  ptc_size):
            all_parents.seek(previous_graph_start + i * 7 * previous_graph_increment)
            parents = []
            for g in range(7):
                parents.append(all_parents.read(previous_graph_increment))
            all_parents.seek(graph_start + (2**(graph_num+6) + sc_size + ptc_size + i) * 7 * graph_increment)
            for g in range(7):
                if parents[g] == "\00" * previous_graph_increment:
                    all_parents.write("\00" * graph_increment)
                else:
                    leading_zero = graph_increment - len(str(int(parents[g])))
                    all_parents.write("0" * leading_zero + str(int(parents[g])))
                    
        # Adds 2nd SC copy
        for i in range(2**(graph_num+5)):
            leading_zero = graph_increment - len(str(2**(graph_num+6) + sc_size + ptc_size + ptc_size + i - 2**(graph_num+5)))
            all_parents.write("0" * leading_zero + str(2**(graph_num+6) + sc_size + ptc_size + ptc_size + i - 2**(graph_num+5)) + "\00" * 6 * graph_increment)

        linear_superconcentrator.superconcentrator(2**(graph_num+5), 2**(graph_num+6) + sc_size + ptc_size + ptc_size, all_parents, graph_increment)
        
        # Adds Sinks
        sofar = 2**(graph_num+6) + 2 * sc_size + 2 * ptc_size
        for i in range(2**(graph_num+6)):
            first_leading_zero = graph_increment - len(str(sofar - 2**(graph_num+5) + (i % 2**(graph_num+5))))
            second_leading_zero = graph_increment - len(str(i))
            all_parents.write("0" * first_leading_zero + str(sofar - 2**(graph_num+5) + (i % 2**(graph_num+5))) + "0" * second_leading_zero + str(i) + "\00" * 5 * graph_increment)
            
def linear_ptcsize(r):
    # This returns the size of the rth ptc graph with linear superconcentrators.
    # The first of these ptc graphs is of size 256.
    if r == 1:
        return 256
    else:
        return 2 * (2**(r+6)) + 2 * linear_sc_size(r-1) + 2 * linear_ptcsize(r-1)
    
def linear_sc_size(r):
    # This function takes any positive integer r and returns the size of the rth linear superconcenetrator.
    # The first linear superconcentrator is of size 256.
    return (2**(r-1) * 8 - 6) * 128

def all_graphs_start(r):
    start = 0
    for i in range(1, r):
        start += linear_ptcsize(i) * 7 * len(str(linear_ptcsize(i)))
    return start
