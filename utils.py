import hashlib

# Converts two-parent-list graph storage scheme to adjacency list
def tpl_to_adj(tpl): # METHOD CAN BE REMOVED
    # optional error-throwing mechanism in case the inputs are not of the same length; this really should need to be triggered in any case
    # if(len(parent1) != len(parent2)):
    # print("Error: input parent lists do not have same length")
    # return
    parent1 = tpl[0]
    parent2 = tpl[1]
    adj = []
    for i in range(len(parent1)):
        adj.append([parent1[i],parent2[i]])
    return adj

# Returns the union of two lists.  Designed for b to be a very small list.
def union(a, b):
    c = list(set(a) | set(b)) # c is the union of a and b.
    return c

# Returns all numbers in range(0,a) that are not in S
def complement1(a, S):
    b = []
    for i in range(a):
        if(i not in S):
            b.append(i)
    return b

def secure_hash(a):
    x = hashlib.sha224()
    x.update(a)
    return x.digest()
