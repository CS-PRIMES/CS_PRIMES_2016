#!/usr/bin/python -t

import shelve
import utils
import ptc

class PebbleGraph:
    def __init__(self, r, debug=False):
        self.B = shelve.open('B.txt')                                  # B contains the parents of the pebble.
        self.all_graphs = shelve.open('all_graphs.txt', writeback=True)                # all_graphs contains the parents of every single ptc graph up to size r.
        self.pebble_value = shelve.open('pebble_value.txt')            # pebble_value stores the value of the hash associated with the pebble.
        self.num_pebbles = 0                                           # num_pebbles is the number of pebbles currently on the graph.
        self.max_pebbles = 0                                           # max_pebbles it the maximum number of pebbles that have been on the graph since the last reset.
        self.graph_num = r
        ptc.PTC(r, self.all_graphs) # line can be changed
        for i in range(self.size()):
            self.B[str(i)] = self.all_graphs[str(self.graph_num)][i]
        for i in range(self.size()):
            self.pebble_value[str(i)] = None
        self.debug = debug

    def close_files(self):
        self.pebble_value.close()
        self.B.close()
        self.all_graphs.close()

    def is_pebbled(self, v):
        if (v is None or self.pebble_value[str(v)] is not None):
            return True
        else:
            return False

    def remove_pebble(self, v):
        if(self.is_pebbled(v) and v is not None):
            self.pebble_value[str(v)] = None
            self.num_pebbles -= 1
            if (self.debug):
                print "Pebble removed from node "+str(v)
        # John can you add code that will actually release the stored value of this vertex from memory to free up some space?

    def remove_pebbles(self, S):
        for v in S:
            self.remove_pebble(v)

    def reset(self):
        for i in range(self.size()):
            self.pebble_value[str(i)] = None
        self.num_pebbles = 0
        self.max_pebbles = 0
        if (self.debug):
            print "All pebbles have been removed from the graph"

    def add_pebble(self, v):
        if v is None:
            return
        if not self.is_pebbled(v):
            if self.is_source(v):
                self.pebble_value[str(v)] = utils.secure_hash(str(v))
                self.num_pebbles += 1
                if self.num_pebbles > self.max_pebbles:
                    self.max_pebbles = self.num_pebbles
                if (self.debug):
                    print "Pebble added to node " + str(v)
            elif self.is_pebbled(self.B[str(v)][0]) and (self.B[str(v)][1] is None):
                self.pebble_value[str(v)] = utils.secure_hash(str(self.pebble_value[str(self.B[str(v)][0])]))
                self.num_pebbles += 1
                if self.num_pebbles > self.max_pebbles:
                    self.max_pebbles = self.num_pebbles
                if (self.debug):
                    print "Pebble added to node " + str(v)
            elif self.is_pebbled(self.B[str(v)][0]) and self.is_pebbled(self.B[str(v)][1]):
                self.pebble_value[str(v)] = utils.secure_hash(str(self.pebble_value[str(self.B[str(v)][0])]) + str(self.pebble_value[str(self.B[str(v)][1])]))
                self.num_pebbles += 1
                if self.num_pebbles > self.max_pebbles:
                    self.max_pebbles = self.num_pebbles
                if (self.debug):
                    print "Pebble added to node " + str(v)
            else:
                print "Error: attempted to pebble node " + str(v) + " without pebbling both parents"
        else:
            print "Attempted to pebble node " + str(v) + " but it has already been pebbled"

    def is_source(self, v):
        return (self.B[str(v)][0] is None and self.B[str(v)][1] is None)

    def get_parents(self, v):
        return self.B[str(v)]

    def size(self):
        return ptc.ptcsize(self.graph_num)

    def print_graph(self):
        print "[",
        for i in range(self.size()):
            print "[" + str(self.B[str(i)][0]) + ", " + str(self.B[str(i)][1]) + "]",
        print "]"

    def start_debug(self):
        self.debug = True

    def stop_debug(self):
        self.debug = False

    def list_values(self):
        values = []
        for i in range(self.size()):
            values.append(self.pebble_value[str(i)])
        return values