import shelve
import sc # file for superconcentrators

def PTC(r, addend):
    if r == 1:
        return sc.gen(1, addend)
    else:
        all_parents = shelve.open('all_parents.txt')
        sc_size = scsize(r-1)
        ptc_size = ptcsize(r-1)

        # Adds Sources
        for i in range (2**(r)):
            all_parents[str(i)] = [None, None]

        # Adds 1st SC copy
        sc1 = sc.gen(r-1, addend + 2**r)

        for i in range(2**(r-1)):
            sc1[str(i)] = [addend + i, addend + i+2**(r-1)]

        n = 0
        for i in range(2**r, 2**r + sc_size):
            all_parents[str(i)] = [sc1[str(n)][0], sc1[str(n)][1]]
            n = n + 1
            
        # Adds 1st PTC copy
        ptc1 = PTC(r-1, addend + 2**r + sc_size)

        for i in range(2**(r-1)):
            ptc1[str(i)] = [addend + 2**r + sc_size - 2**(r-1) + i, None]

        n = 0
        for i in range(2**r + sc_size, 2**r + sc_size + ptc_size):
            all_parents[str(i)] = [ptc1[str(n)][0], ptc1[str(n)][1]]
            n = n + 1
            
        # Adds 2nd PTC copy
        ptc2 = PTC(r-1, addend + 2**r + sc_size + ptc_size)

        for i in range(2**(r-1)):
            ptc2[str(i)] = [addend + 2**r + sc_size + ptc_size - 2**(r-1) + i, None]

        n = 0
        for i in range(2**r + sc_size + ptc_size, 2**r + sc_size + ptc_size + ptc_size):
            all_parents[str(i)] = [ptc2[str(n)][0], ptc2[str(n)][1]]
            n = n + 1
            
        # Adds 2nd SC copy
        sc2 = sc.gen(r-1, addend + 2**r + sc_size + ptc_size + ptc_size)

        for i in range(2**(r-1)):
            sc2[str(i)] = [addend + 2**r + sc_size + ptc_size + ptc_size - 2**(r-1) + i, None]

        n = 0
        for i in range(2**r + sc_size + ptc_size + ptc_size, 2**r + sc_size + ptc_size + ptc_size + sc_size):
            all_parents[str(i)] = [sc2[str(n)][0], sc2[str(n)][1]]
            n = n + 1

        sofar = 2**r + 2 * sc_size + 2 * ptc_size

        # Adds Sinks
        for i in range (2**(r)):
            all_parents[str(sofar+i)] = [None, None]

        for i in range(2**(r)):
            all_parents[str(i+sofar)] = [addend + sofar - 2**(r-1) + (i % 2**(r-1)), addend + i]

        return all_parents

def ptcsize(r):
    if r == 1:
        return 4
    else:
        return 2 * (2**r)  + 2 * (2 * (r-1) * 2**(r-1)) + 2 * ptcsize(r-1)

def scsize(r):
    return 2 * (r) * 2**(r)
