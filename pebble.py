#!/usr/bin/python -t

import shelve
import hashlib
import utils
import ptc

class PebbleGraph:
    pebble = shelve.open('pebble.txt')       # pebble contains whether or not the pebble is pebbled.
    B = []                                 # B contains the parents of the pebble.
    pebble_value = shelve.open('pebble_value.txt') # pebble_value stores the value of the hash associated with the pebble.

    def __init__(self, r):
        self.B = ptc.PTC(r,0) # line can be changed
        for i in range (len(self.B)):
            self.pebble[str(i)] = False # need to talk about this in meeting
            self.pebble_value[str(i)] = -1

    def close_files(self):
        self.d.close()
        self.pebble_value.close()
        
        
    def is_pebbled(self, v):
        return self.pebble[str(v)]

    def remove_pebble(self, v):
        if(self.is_pebbled(v)):
            print "Pebble removed from node "+str(v)
        self.pebble[str(v)] = False
        # John can you add code that will actually release the stored value of this vertex from memory to free up some space?

    def remove_pebbles(self, S):
        for v in S:
            self.remove_pebble(v)

    def reset(self):
        self.pebble = [False]*len(self.B)

    def add_pebble(self, v):
        if(self.is_source(v)):
            if(not self.is_pebbled(v)):
                self.pebble_value[str(v)] = utils.secure_hash(str(v))
                self.pebble[str(v)] = True                
                print "Pebble added to node "+str(v)
            return
        if(self.is_pebbled(self.B[v][0]) and self.is_pebbled(self.B[v][1])):
            if(not self.is_pebbled(v)):
                self.pebble_value[str(v)] = utils.secure_hash(str(self.pebble_value[str(self.B[v][0])]) + str(self.pebble_value[str(self.B[v][1])]))
                self.pebble[str(v)] = True
                print "Pebble added to node "+str(v)
            return
        print "Error: attempted to pebble node "+str(v)+" without pebbling both parents"

    def is_source(self, v):
        return (self.B[v][0] == -1 and self.B[v][1] == -1)

    def get_parents(self, v):
        return self.B[v]

    def size(self):
        return len(self.B)

    def pebble_list(self):
        return self.pebble

    def graph(self):
        return self.B
