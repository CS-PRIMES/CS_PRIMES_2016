# File that stores superconcentrator implementations

# function that is used in PTC generation
def gen(r, addend):
    return butterfly(r, addend)

def butterfly(r, addend):
    numvertices = r * 2 * (2 ** r)

    parents = [[None, None]] * numvertices
    # None signifies the lack of a parent

    # First we input the parent directly below the vertice. Note that we do
    # not input anything for the sources because they do not have parents.
    for vertex in range (2**r, numvertices):
        parents[vertex][0] = addend + vertex - 2**r

        # Now we input the parent below and to the side of the vertice.
    for vertex in range (2**r, numvertices):
        column = vertex % (2**r) + 1
        row = vertex / (2**r) + 1
        if row >= r + 1:
            shift = row - r
        else:
            shift = r - row + 2
            shift = 2 ** (shift - 1)
            # shift represents how far to the right or left the parent is of
            # its child
        if (column-1) % (2*shift) < shift:
            # This occurs if the shift from child to parent is to the
            # right.
            parents[vertex][1] = addend + vertex - 2**r + shift
        else:
            # This occurs if the shift from child to parent is to the
            # left.
            parents[vertex][1] = addend + vertex - 2**r - shift

    return parents
