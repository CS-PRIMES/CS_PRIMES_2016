import sc # file for superconcentrators

def PTC(r, all_parents):
    all_parents.seek(0)
    all_parents.write("\00\00\00\00" + "0110") # Corresponds to [[None, None], [None, None], [0, 1], [1, 0]]
    
    for graph_num in range (2, r+1):
        graph_start = all_graphs_start(graph_num)
        graph_increment = len(str(ptcsize(graph_num)))
        previous_graph_start = all_graphs_start(graph_num-1)
        previous_graph_increment = len(str(ptcsize(graph_num-1)))
        sc_size = 2 * (graph_num-1) * 2**(graph_num-1)
        ptc_size = ptcsize(graph_num-1)

        # Adds Sources
        all_parents.write("\00\00" * graph_increment * 2**graph_num)
                
        # Adds 1st SC copy
        for i in range(2**(graph_num-1)):
            first_leading_zero = graph_increment - len(str(i))
            second_leading_zero = graph_increment - len(str(i + 2**(graph_num - 1)))
            all_parents.write("0" * first_leading_zero + str(i) + "0" * second_leading_zero + str(i + 2**(graph_num-1)))

        sc.butterfly(graph_num-1, 2**graph_num, all_parents)
            
            
        # Adds 1st PTC copy
        for i in range(2**(graph_num-1)):
            leading_zeroes = graph_increment - len(str(2**graph_num + sc_size - 2**(graph_num-1) + i))
            all_parents.write("0" * leading_zeroes + str(2**graph_num + sc_size - 2**(graph_num-1) + i) + "\00" * graph_increment)

        for i in range(2**(graph_num-1), ptc_size):
            all_parents.seek(previous_graph_start + 2 * previous_graph_increment * i)
            parents = []
            parents.append(all_parents.read(previous_graph_increment))
            parents.append(all_parents.read(previous_graph_increment))
            all_parents.seek(graph_start + (2**graph_num + sc_size + i) * graph_increment * 2)
            first_leading_zero = graph_increment - len(str(int(parents[0]) + 2**graph_num + sc_size))
            if parents[1] == "\00" * previous_graph_increment:
                all_parents.write("0" * first_leading_zero + str(int(parents[0]) + 2**graph_num + sc_size) + "\00" * graph_increment)
            else:
                second_leading_zero = graph_increment - len(str(int(parents[1]) + 2**graph_num + sc_size))
                all_parents.write("0" * first_leading_zero + str(int(parents[0]) + 2**graph_num + sc_size) + "0" * second_leading_zero + str(int(parents[1]) + 2**graph_num + sc_size))
            
        # Adds 2nd PTC copy
        for i in range(2**(graph_num-1)):
            leading_zeroes = graph_increment - len(str(2**graph_num + sc_size + ptc_size - 2**(graph_num-1) + i))
            all_parents.write("0" * leading_zeroes + str(2**graph_num + sc_size  + ptc_size - 2**(graph_num-1) + i) + "\00" * graph_increment)
            
        for i in range(2**(graph_num-1), ptc_size):
            all_parents.seek(previous_graph_start + 2 * previous_graph_increment * i)
            parents = []
            parents.append(all_parents.read(previous_graph_increment))
            parents.append(all_parents.read(previous_graph_increment))
            all_parents.seek(graph_start + (2**graph_num + sc_size + ptc_size + i) * graph_increment * 2)
            first_leading_zero = graph_increment - len(str(int(parents[0]) + 2**graph_num + sc_size + ptc_size))
            if parents[1] == "\00" * previous_graph_increment:
                all_parents.write("0" * first_leading_zero + str(int(parents[0]) + 2**graph_num + sc_size + ptc_size) + "\00" * graph_increment)
            else:
                second_leading_zero = graph_increment - len(str(int(parents[1]) + 2**graph_num + sc_size + ptc_size))
                all_parents.write("0" * first_leading_zero + str(int(parents[0]) + 2**graph_num + sc_size + ptc_size) + "0" * second_leading_zero + str(int(parents[1]) + 2**graph_num + sc_size + ptc_size))

        # Adds 2nd SC copy
        for i in range(2**(graph_num-1)):
            first_leading_zero = graph_increment - len(str(2**graph_num + sc_size + ptc_size + ptc_size + i - 2**(graph_num-1)))
            all_parents.write("0" * first_leading_zero + str(2**graph_num + sc_size + ptc_size + ptc_size + i - 2**(graph_num-1)) + "\00" * graph_increment)

        sc.butterfly(graph_num-1, 2**graph_num + sc_size + ptc_size + ptc_size, all_parents)
        
        # Adds Sinks
        sofar = 2**graph_num + 2 * sc_size + 2 * ptc_size
        for i in range(2**(graph_num)):
            first_leading_zero = graph_increment - len(str(sofar - 2**(graph_num-1) + (i % 2**(graph_num-1))))
            second_leading_zero = graph_increment - len(str(i))
            all_parents.write("0" * first_leading_zero + str(sofar - 2**(graph_num-1) + (i % 2**(graph_num-1))) + "0" * second_leading_zero + str(i))
            

def ptcsize(r):
    if r == 1:
        return 4
    else:
        return 2 * (2**r)  + 2 * (2 * (r-1) * 2**(r-1)) + 2 * ptcsize(r-1)

def scsize(r):
    return 2 * (r) * 2**(r)

def all_graphs_start(r):
    start = 0
    for i in range(1, r):
        start += ptcsize(i) * 2 * len(str(ptcsize(i)))
    return start
