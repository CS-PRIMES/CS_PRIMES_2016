import shelve

# File that stores superconcentrator implementations

# function that is used in PTC generation
def gen(r, addend, parents):
    return butterfly(r, addend, parents)

def butterfly(r, addend, parents):
    numvertices = r * 2 * (2 ** r)

    for i in range(2**r):
        parents[str(i)] = [None, None]
    # None signifies the lack of a parent

    # First we input the parent directly below the vertice. Note that we do
    # not input anything for the sources because they do not have parents.


    # Now we input the parent below and to the side of the vertice.
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
            # This occurs if the shift from child to parent is to the
            # right.
            parents[str(vertex)] = [addend + vertex - 2**r, addend + vertex - 2**r + shift]
        else:
            # This occurs if the shift from child to parent is to the
            # left.
            parents[str(vertex)] = [addend + vertex - 2**r, addend + vertex - 2**r - shift]

    return parents


