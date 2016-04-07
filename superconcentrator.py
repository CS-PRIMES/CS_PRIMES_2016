graph_number = 2
vertices = graph_number * 2 * (2 ** graph_number)

parent1 = []
parent2 = []

for i in range (vertices):
    parent1.append(-1)
    parent2.append(-1)
    # -1 signifies the lack of a parent

# First we input the parent directly below the vertice. Note that we do
# not input anything for the sources because they do not have parents.
for vertice in range (2 ** graph_number, vertices):
    parent1[vertice] = vertice - 2 ** graph_number

# Now we input the parent below and to the side of the vertice.
for vertice in range (2 ** graph_number, vertices):
    column = vertice % (2 ** graph_number) + 1
    row = vertice / (2 ** graph_number) + 1
    if row >= graph_number + 1:
        shift = row - graph_number
    else:
        shift = graph_number - row + 2
    shift = 2 ** (shift - 1)
    # shift represents how far to the right or left the parent is of
    # its child
    if (column-1) % (2*shift) < shift:
        # This occurs if the shift from child to parent is to the
        # right.
        parent2[vertice] = vertice - 2 ** graph_number + shift
    else:
        # This occurs if the shift from child to parent is to the
        # left.
        parent2[vertice] = vertice - 2 ** graph_number - shift

print parent1
print parent2
