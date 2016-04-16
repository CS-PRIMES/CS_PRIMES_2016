# Converts two-parent-list graph storage scheme to adjacency list
def tpl_to_adj(tpl):
	# optional error-throwing mechanism in case the inputs are not of the same length; this really should need to be triggered in any case
	# if(len(parent1) != len(parent2)):
	# 	print("Error: input parent lists do not have same length")
	# 	return
	parent1 = tpl[0]
	parent2 = tpl[1]
	adj = []
	for i in range(len(parent1)):
		adj.append([parent1[i],parent2[i]])
	return adj

# Returns the union of two lists.  Designed for b to be a very small list.
def union(a, b):
	c = a
	for e in b:
		if(e not in c):
			c.append(e)
	return c

# Returns all numbers in range(0,a) that are not in S
def complement1(a, S):
	b = []
	for i in range(a):
		if(i not in S):
			b.append(i)
	return b