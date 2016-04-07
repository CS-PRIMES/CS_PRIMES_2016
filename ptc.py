import sc # file for superconcentrators

def PTC(r, addend):
    if r == 1:
        return sc.gen(1, addend)
    else:
        parent1 = []
        parent2 = []

        # Adds Sources
        for i in range (2**(r)):
            parent1.append(-1)
            parent2.append(-1)

        # Adds 1st SC copy
        sc1, sc2 = sc.gen(r-1, addend + len(parent1))
        
        for i in range(2**(r-1)):
            sc1[i] = addend + i
            sc2[i] = addend + i+2**(r-1);
        
        parent1.extend(sc1);
        parent2.extend(sc2);

        # Adds 1st PTC copy
        ptc1, ptc2 = PTC(r-1, addend + len(parent1))

        for i in range(2**(r-1)):
            ptc1[i] = addend + len(parent1) - 2**(r-1) + i

        parent1.extend(ptc1)
        parent2.extend(ptc2)

        # Adds 2nd PTC copy
        ptc1, ptc2 = PTC(r-1, addend + len(parent1))

        for i in range(2**(r-1)):
            ptc1[i] = addend + len(parent1) - 2**(r-1) + i

        parent1.extend(ptc1)
        parent2.extend(ptc2)
        
        # Adds 2nd SC copy
        sc1, sc2 = sc.gen(r-1, addend + len(parent1))

        for i in range(2**(r-1)):
            sc1[i] = addend + len(parent1) - 2**(r-1) + i

        parent1.extend(sc1);
        parent2.extend(sc2);

        # Adds Sinks
        for i in range(2**(r)):
            parent2.append(addend + len(parent1) - 2**(r-1)+ (i % 2**(r-1)))
        
        for i in range(2**(r)):
            parent1.append(addend + i)

        return parent1, parent2
