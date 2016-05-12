#!/usr/bin/python -t

import shelve
import utils
import ptc

class PebbleGraph:
    B = []                                 # B contains the parents of the pebble.
    pebble_value = shelve.open('pebble_value.txt') # pebble_value stores the value of the hash associated with the pebble.

    def __init__(self, r):
        self.B = ptc.PTC(r,0) # line can be changed
        for i in range (len(self.B)):
            self.pebble_value[str(i)] = -1

    def close_file(self):
        self.pebble_value.close()
                
    def is_pebbled(self, v):
        if (self.pebble_value[str(v)] == -1):
            return False
        else:
            return True

    def remove_pebble(self, v):
        if (self.is_pebbled(v)):
            print "Pebble removed from node "+str(v)
        self.pebble_value[str(v)] = -1

    def remove_pebbles(self, S):
        for v in S:
            self.remove_pebble(v)

    def reset(self):
        for q in range (len(self.B)):
            self.pebble_value[str(q)] = -1
                         

    def add_pebble(self, v):
        if (self.is_source(v)):
            if (not self.is_pebbled(v)):
                self.pebble_value[str(v)] = v
                print "Pebble added to node " + str(v)
            return
        if (self.is_pebbled(self.B[v][0]) and (self.B[v][1] == -1)): #If v only has one parent.
            if (not self.is_pebbled(v)):
                self.pebble_value[str(v)] = str(utils.secure_hash(str(self.pebble_value[str(self.B[v][0])])))
                print "Pebble added to node " + str(v)
            return
        if (self.is_pebbled(self.B[v][0]) and (self.is_pebbled(self.B[v][1]))):
            if (not self.is_pebbled(v)):
                self.pebble_value[str(v)] = str(utils.secure_hash(str(self.pebble_value[str(self.B[v][0])]) + str(self.pebble_value[str(self.B[v][1])])))
                print "Pebble added to node " + str(v)
            return
        print "Error: attempted to pebble node " + str(v) + " without pebbling both parents"

    def is_source(self, v):
        return (self.B[v][0] == -1 and self.B[v][1] == -1)

    def get_parents(self, v):
        return self.B[v]

    def size(self):
        return len(self.B)

    def pebble_list(self):
        return self.pebble_value

    def graph(self):
        return self.B
