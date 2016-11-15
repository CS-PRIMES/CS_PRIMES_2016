import linear_ptc
import random

def superconcentrator(graph_num, extra, linear_parents, graph_increment):
    # graph_num must be an integer power of 2 greater than or equal to 128.
    
    graph_size = linear_sc_size(graph_num)
    
    # Now we build the linear superconcentrator graph from the bottom up using expander graphs.

    # The first half:
    i = graph_num
    current = 0
    # current is the location of the next expander graph we will add to the linear superconcentrator.
    while (i >= 128): # i is the size of the next expander graph we will add.
        expander_graph(i, current, linear_parents, extra, 1, graph_increment)
        current = current + 2 * i
        i = i / 2
        # This loop goes for i over all powers of 2 from graph_num to 128 (inclusive).

    # The second half:
    i = 256
    while (i <= graph_num):
        expander_graph(i, current, linear_parents, extra, 0, graph_increment)
        current = current + 2 * i
        i = i * 2
        # This loop goes over all powers of 2 from i = 256 to i = graph_num
        # Note: These four for loops are redundant. Only two are needed.
    
                       
def expander_graph(n, addend, expander_parents, extra, beginning, graph_increment):
    # n must be an integer power of 2 greater than or equal to 8.
    # for our purposes, we will always call n >= 128.

    if beginning == 1:
        # Add the parents of the left vertices
        if addend != 0: # If addend == 0 then the left vertices will be added in linear_ptc.py
            for i in range(n):
                leading_zero = graph_increment - len(str(extra + addend + n - 2*i))
                expander_parents.write("0" * leading_zero + str(extra + addend + n - 2*i) + "z" * 6 * graph_increment)
            
        # Add the parents of the right vertices
        for i in range(n):
            parents = random.sample(range(n), 6)
            zeroes = []
            for g in range(6):
                parents[g] += addend + extra
                zeroes.append(graph_increment - len(str(parents[g])))
            if n > 128 and n + addend <= i and i < addend + n*3/2:
                zeroes.append(graph_increment - len(str(addend + extra + i + n/2)))
                expander_parents.write("0" * zeroes[0] + str(parents[0]) + "0" * zeroes[1] + str(parents[1]) + "0" * zeroes[2] + str(parents[2]) +
                                       "0" * zeroes[3] + str(parents[3]) + "0" * zeroes[4] + str(parents[4]) + "0" * zeroes[5] + str(parents[5]) + "0" * zeroes[6] + str(addend + extra + i + n/2))
            else:
                expander_parents.write("0" * zeroes[0] + str(parents[0]) + "0" * zeroes[1] + str(parents[1]) + "0" * zeroes[2] + str(parents[2]) +
                                       "0" * zeroes[3] + str(parents[3]) + "0" * zeroes[4] + str(parents[4]) + "0" * zeroes[5] + str(parents[5]) + "z" * graph_increment)
    else:
        # Add the parents of the left vertices
        for i in range(n/2):
            first_leading_zero = graph_increment - len(str(addend + extra + i - n/2))
            second_leading_zero = graph_increment - len(str(addend + extra + i - n/2 - linear_sc_size(n/2)))
            expander_parents.write("0" * first_leading_zero + str(addend + extra + i - n/2) + "0" * second_leading_zero + str(addend + extra + i - n/2 - linear_sc_size(n/2)) + "z" * 5 * graph_increment)
        for i in range(n/2, n):
            first_leading_zero = graph_increment - len(str(extra + addend + i - n/2))
            second_leading_zero = graph_increment - len(str(extra + addend + i - n*3/2 - linear_sc_size(i/2)))
            expander_parents.write("0" * first_leading_zero + str(extra + addend + i - n/2) + "0" * second_leading_zero + str(extra + addend + i - n*3/2 - linear_sc_size(i/2)) + "z" * 5 * graph_increment)

        # Add the parents of the right vertices
        for i in range(n):
            parents = random.sample(range(n), 6)
            zeroes = []
            for g in range(6):
                parents[g] += addend + extra
                zeroes.append(graph_increment - len(str(parents[g])))
            expander_parents.write("0" * zeroes[0] + str(parents[0]) + "0" * zeroes[1] + str(parents[1]) + "0" * zeroes[2] + str(parents[2]) +
                                   "0" * zeroes[3] + str(parents[3]) + "0" * zeroes[4] + str(parents[4]) + "0" * zeroes[5] + str(parents[5]) + "z" * graph_increment)

            
def linear_sc_size(graph_num):
    return graph_num * 8 - 6 # graph_num is a power of 2.
