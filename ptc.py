import sc # file for superconcentrators

def PTC(r, addend):
    if r == 1:
        return sc.gen(1, addend)
    else:
        parents = []

        # Adds Sources
        for i in range (2**(r)):
            parents.append([None, None])

        # Adds 1st SC copy
        sc1 = sc.gen(r-1, addend + len(parents))

        for i in range(2**(r-1)):
            sc1[i][0] = addend + i
            sc1[i][1] = addend + i+2**(r-1);

        parents.extend(sc1)

        # Adds 1st PTC copy
        ptc1 = PTC(r-1, addend + len(parents))

        for i in range(2**(r-1)):
            ptc1[i][0] = addend + len(parents) - 2**(r-1) + i

        parents.extend(ptc1)

        # Adds 2nd PTC copy
        ptc1 = PTC(r-1, addend + len(parents))

        for i in range(2**(r-1)):
            ptc1[i][0] = addend + len(parents) - 2**(r-1) + i

        parents.extend(ptc1)

        # Adds 2nd SC copy
        sc1 = sc.gen(r-1, addend + len(parents))

        for i in range(2**(r-1)):
            sc1[i][0] = addend + len(parents) - 2**(r-1) + i

        parents.extend(sc1)
        sofar = len(parents)

        # Adds Sinks
        for i in range (2**(r)):
            parents.append([None, None])

        for i in range(2**(r)):
            parents[i+sofar][0] = addend + sofar - 2**(r-1)+ (i % 2**(r-1))
            parents[i+sofar][1] = addend + i

        return parents
