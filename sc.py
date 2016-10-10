# File that stores superconcentrator implementations
import ptc

def butterfly(r, addend, parents):
    numvertices = r * 2 * 2**r
    increment = len(str(ptc.ptcsize(r+1)))

    # We do not add the sources to the superconcentrator graph, as they are added in ptc.py

    # We store the parents as: [Parent directly below vertex, parent below and to the side of vertex.]
    for vertex in range (2**r, numvertices):
        column = vertex % (2**r) + 1
        row = vertex / (2**r) + 1
        if row >= r + 1:
            shift = row - r
        else:
            shift = r - row + 2
            
        shift = 2 ** (shift - 1)
        # shift represents how far to the right or left the child is
        # of its parent.
        if (column-1) % (2*shift) < shift:
            # This occurs if the shift from child to parent is to the right.
            first_leading_zero = increment - len(str(addend + vertex - 2**r))
            second_leading_zero = increment - len(str(addend + vertex - 2**r + shift))
            parents.write("0" * first_leading_zero + str(addend + vertex - 2**r) + "0" * second_leading_zero + str(addend + vertex - 2**r + shift))
        else:
            # This occurs if the shift from child to parent is to the left.
            first_leading_zero = increment - len(str(addend + vertex - 2**r))
            second_leading_zero = increment - len(str(addend + vertex - 2**r - shift))
            parents.write("0" * first_leading_zero + str(addend + vertex - 2**r) + "0" * second_leading_zero + str(addend + vertex - 2**r - shift))
