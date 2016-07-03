import shelve
import sc # file for superconcentrators

def PTC(r, all_parents):
    all_parents[str(1)] = [[None, None], [None, None], [0, 1], [1, 0]]
    
    for graph_size in range (2, r+1):
        sc_size = 2 * (graph_size-1) * 2**(graph_size-1)
        ptc_size = ptcsize(graph_size-1)
        all_parents[str(graph_size)] = []
        for i in range(ptcsize(graph_size)):
            all_parents[str(graph_size)].append([None, None])
            
        # Adds Sources
        for i in range (2**(graph_size)):
            all_parents[str(graph_size)][i] = [None, None]
                
        # Adds 1st SC copy
        sc1 = shelve.open('sc1.txt')
        sc1 = sc.gen(graph_size-1, 2**graph_size, sc1)
            
        for i in range(2**(graph_size-1)):
            sc1[str(i)] = [i, i + 2**(graph_size-1)]
            
        n = 0
        for i in range(2**graph_size, 2**graph_size + sc_size):
            all_parents[str(graph_size)][i] = [sc1[str(n)][0], sc1[str(n)][1]]
            n = n + 1

        sc1.close()
            
        # Adds 1st PTC copy
        n = 0
        for i in range(2**graph_size + sc_size, 2**graph_size + sc_size + 2**(graph_size-1)):
            all_parents[str(graph_size)][i] = [2**graph_size + sc_size - 2**(graph_size-1) + n, None]
            n = n + 1

        for i in range(2**graph_size + sc_size + 2**(graph_size-1), 2**graph_size + sc_size + ptc_size):
            if all_parents[str(graph_size-1)][n][1] == None:
                all_parents[str(graph_size)][i] = [all_parents[str(graph_size-1)][n][0] + 2**graph_size + sc_size, None]
            else:
                all_parents[str(graph_size)][i] = [all_parents[str(graph_size-1)][n][0] + 2**graph_size + sc_size, all_parents[str(graph_size-1)][n][1] + 2**graph_size + sc_size]
            n = n + 1
            
        # Adds 2nd PTC copy
        n = 0
        for i in range(2**graph_size + sc_size + ptc_size, 2**graph_size + sc_size + ptc_size + 2**(graph_size-1)):
            all_parents[str(graph_size)][i] = [2**graph_size + sc_size + ptc_size - 2**(graph_size-1) + n, None]
            n = n + 1

        for i in range(2**graph_size + sc_size + ptc_size + 2**(graph_size-1), 2**graph_size + sc_size + ptc_size + ptc_size):
            if all_parents[str(graph_size-1)][n][1] == None:
                all_parents[str(graph_size)][i] = [all_parents[str(graph_size-1)][n][0] + 2**graph_size + sc_size + ptc_size, None]
            else:
                all_parents[str(graph_size)][i] = [all_parents[str(graph_size-1)][n][0] + 2**graph_size + sc_size + ptc_size, all_parents[str(graph_size-1)][n][1] + 2**graph_size + sc_size + ptc_size]
            n = n + 1
                    
        # Adds 2nd SC copy
        sc2 = shelve.open('sc2.txt')
        sc2 = sc.gen(graph_size-1, 2**graph_size + sc_size + ptc_size + ptc_size, sc2)
        
        for i in range(2**(graph_size-1)):
            sc2[str(i)] = [2**graph_size + sc_size + ptc_size + ptc_size + i - 2**(graph_size-1), None]

        n = 0
        for i in range(2**graph_size + sc_size + ptc_size + ptc_size, 2**graph_size + sc_size + ptc_size + ptc_size + sc_size):
            all_parents[str(graph_size)][i] = [sc2[str(n)][0], sc2[str(n)][1]]
            n = n + 1

        sc2.close()
        
        sofar = 2**graph_size + 2 * sc_size + 2 * ptc_size
        
        # Adds Sinks
        for i in range (2**(graph_size)):
            all_parents[str(graph_size)][sofar+i] = [None, None]

        for i in range(2**(graph_size)):
            all_parents[str(graph_size)][i+sofar] = [sofar - 2**(graph_size-1) + (i % 2**(graph_size-1)), i]
            

def ptcsize(r):
    if r == 1:
        return 4
    else:
        return 2 * (2**r)  + 2 * (2 * (r-1) * 2**(r-1)) + 2 * ptcsize(r-1)
