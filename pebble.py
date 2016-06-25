#!/usr/bin/python -t

import shelve
import utils
import ptc

class PebbleGraph:
    B = []                                 # B contains the parents of the pebble.
    pebble_value = []                      # pebble_value stores the value of the hash associated with the pebble.
    num_pebbles = 0                        # num_pebbles is the number of pebbles currently on the graph.
    max_pebbles = 0                        # max_pebbles it the maximum number of pebbles that have been on the graph since the last reset.

    def __init__(self, r):
        self.B = ptc.PTC(r,0) # line can be changed
        self.pebble_value = [None]*len(self.B)
        self.num_pebbles = 0
        self.max_pebbles = 0

    def is_pebbled(self, v):
        if (v is None or self.pebble_value[v] is not None):
            return True
        else:
            return False

    def remove_pebble(self, v):
        if(self.is_pebbled(v) and v is not None):
            self.pebble_value[v] = None
            self.num_pebbles -= 1
            print "Pebble removed from node "+str(v)
        # John can you add code that will actually release the stored value of this vertex from memory to free up some space?

    def remove_pebbles(self, S):
        for v in S:
            self.remove_pebble(v)

    def reset(self):
        self.pebble_value = [None]*len(self.B)
        self.num_pebbles = 0
        self.max_pebbles = 0
        print "All pebbles have been removed from the graph"

    def add_pebble(self, v):
        if v is None:
            return
        if not self.is_pebbled(v):
            if self.is_source(v):
                self.pebble_value[v] = utils.secure_hash(str(v))
                self.num_pebbles += 1
                if self.num_pebbles > self.max_pebbles:
                    self.max_pebbles = self.num_pebbles
                print "Pebble added to node " + str(v)
            elif self.is_pebbled(self.B[v][0]) and (self.B[v][1] is None):
                self.pebble_value[v] = utils.secure_hash(str(self.pebble_value[self.B[v][0]]))
                self.num_pebbles += 1
                if self.num_pebbles > self.max_pebbles:
                    self.max_pebbles = self.num_pebbles
                print "Pebble added to node " + str(v)
            elif self.is_pebbled(self.B[v][0]) and self.is_pebbled(self.B[v][1]):
                self.pebble_value[v] = utils.secure_hash(str(self.pebble_value[self.B[v][0]]) + str(self.pebble_value[self.B[v][1]]))
                self.num_pebbles += 1
                if self.num_pebbles > self.max_pebbles:
                    self.max_pebbles = self.num_pebbles
                print "Pebble added to node " + str(v)
            else:
                print "Error: attempted to pebble node " + str(v) + " without pebbling both parents"
        else:
            print "Attempted to pebble node " + str(v) + " but it has already been pebbled"

    def is_source(self, v):
        return (self.B[v][0] is None and self.B[v][1] is None)

    def get_parents(self, v):
        return self.B[v]

    def size(self):
        return len(self.B)

    def graph(self):
        return self.B
