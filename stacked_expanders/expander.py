# Stacked Expanders Class Code
# Author(s): CS PRIMES 2016

import random
import hashlib
import utils

class expanders:

    def __init__(self, n, k, pre_gen_graph=False, debug=False):
        # graph is partitioned into k sets of n vertices.
        # Note: n must be at least 16!
        # This is described in "Proof of Space from Stacked Bipartite Graphs"
        self.n = n  
        self.k = k
        self.size = n * k
        self.merkle_root = None
        self.hash_length = utils.hash_length()
        # parents stores the parents of V_2
        self.parents = open('expanders_parents.txt', 'r+')
        self.parents_increment = len(str(n-1)) # a parent will be a num from 0 to n-1
        if not pre_gen_graph:
            self.create_graph()
        # pebble_value stores the values associated with the vertices
        # in one of the k sets of n vertices.  Then a merkle_tree is
        # created in pebble_value from the hashes of these n vertices
        # to compute the merkle root, some C_m.
        self.pebble_value = open('expander_pebble_value.txt', 'r+')
        # Finally each C_1 through C_k is written into this file.
        # A merkle tree is created from these to find a single merkle root, C.
        self.merkle_tree = open('expander_merkle_tree.txt', 'r+')

    def close_files(self):
        self.parents.close()
        self.pebble_value.close()
        self.merkle_tree.close()
        
    def create_graph(self):
        self.parents.seek(0)
        for i in range(self.n):
            parents_of_vertex = random.sample(range(self.n), 16)
            for g in range(16):
                leading_zeroes = self.parents_increment - len(str(parents_of_vertex[g]))
                self.parents.write("0" * leading_zeroes + str(parents_of_vertex[g]))

    # yields merkle root (not like any of our other trivial_pebbles,
    # as the entire graph is never stored at once)
    def trivial_pebble(self):
        # pebbles sources
        self.pebble_value.seek(0)
        self.merkle_tree.seek(0)
        for i in range(self.n):
            self.pebble_value.write(utils.prehash_associated_with_source(i))
        self.merkle_tree.write(self.merkle_pebble_value(1))
        # pebbles rest of graph
        for i in range(self.k - 1):
            self.pebble_row(i%2) # when i is even, the data is in the first half of pebble_value.txt
            self.merkle_tree.write(self.merkle_pebble_value(i%2))
        self.merkle_root = self.merkle_merkle_roots()

    # fill is either 0 or 1, depending on whether the first half or
    # second half of pebble_value.txt is filled with the hashes of
    # the previous pebbls.
    def pebble_row(self, fill):
        self.parents.seek(0)
        for i in range(self.n):
            prehash = ''
            for i in range(16):
                self.pebble_value.seek(fill*self.n*self.hash_length + int(self.parents.read(self.parents_increment)))
                prehash += self.pebble_value.read(self.hash_length)
            self.pebble_value.seek(self.n * self.opp(fill) * self.hash_length + i * self.hash_length)
            self.pebble_value.write(utils.secure_hash(prehash))

    # fill is either 0 or 1, depending on whether the merkle tree will
    # be written in the first half or second half (using data from the
    # other half of pebble_value.txt)
    def merkle_pebble_value(self, fill):
        power_of_two = 1 # first we set it to smallest power of two greater than or equal to n
        while (power_of_two < self.n):
            power_of_two *= 2
        for i in range(power_of_two):
            if (2*i + 2 <= self.n):
                self.pebble_value.seek(2*i*self.hash_length + self.hash_length * self.opp(fill)*self.n)
                prehash = self.pebble_value.read(2 * self.hash_length)
                self.pebble_value.seek(i*self.hash_length + self.hash_length * fill * self.n)
                self.pebble_value.write(utils.secure_hash(prehash))
            elif (2*i + 1 == self.n):
                self.pebble_value.seek(2*i*self.hash_length + self.hash_length*self.opp(fill)*self.n)
                prehash = self.pebble_value.read(self.hash_length) + '\00' * self.hash_length
                self.pebble_value.seek(i*self.hash_length + self.hash_length * fill * self.n)
                self.pebble_value.write(utils.secure_hash(prehash))
            else:
                prehash = '\00' * 2 * self.hash_length
                self.pebble_value.seek(i*self.hash_length + self.hash_length * fill * self.n)
                self.pebble_value.write(utils.secure_hash(prehash))
        power_of_two /= 2
        while (power_of_two >= 1):
            for i in range(power_of_two):
                self.pebble_value.seek(2*i*self.hash_length + self.hash_length * fill * self.n)
                prehash = self.pebble_value.read(2 * self.hash_length)
                self.pebble_value.seek(i*self.hash_length + self.hash_length * fill * self.n)
                self.pebble_value.write(utils.secure_hash(prehash))
            power_of_two /= 2
        self.pebble_value.seek(self.n * fill * self.hash_length)
        return self.pebble_value.read(self.hash_length)

    def merkle_merkle_roots(self):
        power_of_two = 1 #intitially set to the smallest power of two greater than or equal to k.
        while (power_of_two < self.k):
            power_of_two *= 2
        power_of_two /= 2
        for i in range(power_of_two):
            if (2*i + 2 <= self.k):
                self.merkle_tree.seek(2*i*self.hash_length)
                prehash = self.merkle_tree.read(2*self.hash_length)
                self.merkle_tree.seek(i*self.hash_length)
                self.merkle_tree.write(utils.secure_hash(prehash))
            elif (2*i + 1 == self.k):
                self.merkle_tree.seek(2*i*self.hash_length)
                prehash = self.merkle_tree.read(self.hash_length) + '\00' * self.hash_length
                self.merkle_tree.seek(i*self.hash_length)
                self.merkle_tree.write(utils.secure_hash(prehash))
            else:
                prehash = '\00' * self.hash_length
                self.merkle_tree.seek(i*self.hash_length)
                self.merkle_tree.write(utils.secure_hash(prehash))
        power_of_two /= 2
        while (power_of_two >= 1):
            for i in range(power_of_two):
                self.merkle_tree.seek(2*i*self.hash_length)
                prehash = self.merkle_tree.read(2*self.hash_length)
                self.merkle_tree.seek(i*self.hash_length)
                self.merkle_tree.write(utils.secure_hash(prehash))
            power_of_two /= 2
        self.merkle_tree.seek(0)
        return self.merkle_tree.read(self.hash_length)

    # flips a bool that's 0 or 1
    def opp(self, num):
        if num == 0:
            return 1
        else:
            return 0
