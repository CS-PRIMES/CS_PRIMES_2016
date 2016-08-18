#!/usr/bin/python -t

import shelve
import utils
import linear_ptc

class PebbleGraph:
    
    def __init__(self, r, debug=False):
        self.B = shelve.open('B.txt')                                  # B contains the parents of the pebble.
        self.all_graphs = shelve.open('all_graphs.txt', writeback=True)                # all_graphs contains the parents of every single ptc graph up to size r.
        self.pebble_value = shelve.open('pebble_value.txt')            # pebble_value stores the value of the hash associated with the pebble.
        self.num_pebbles = 0                                           # num_pebbles is the number of pebbles currently on the graph.
        self.max_pebbles = 0                                           # max_pebbles it the maximum number of pebbles that have been on the graph since the last reset.
        self.graph_num = r
        self.size = linear_ptc.linear_ptcsize(self.graph_num)
        linear_ptc.linear_PTC(r, self.all_graphs)
        for i in range(self.size):
            self.B[str(i)] = self.all_graphs[str(self.graph_num)][i]
        for i in range(self.size):
            self.pebble_value[str(i)] = None
        self.debug = debug
        self.all_graphs.close()
        
    def close_files(self):
        self.pebble_value.close()
        self.B.close()

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

    def remove_pebbles(self, S):
        for v in S:
            self.remove_pebble(v)

    def reset(self):
        for i in range(self.size):
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
            else:
                prehash = ""
                error = 0
                for i in range(7):
                    if self.B[str(v)][i] != None:
                        if self.pebble_value[str(self.B[str(v)][i])] == None:
                            print "Error: Attempted to pebble node " + str(v) + "without pebbling parent " + str(i) + "."
                            error = 1
                        else:
                            prehash = prehash + str(self.pebble_value[str(self.B[str(v)][i])])
                if error == 0:
                    self.pebble_value[str(v)] = utils.secure_hash(str(v))
                    self.num_pebbles += 1
                    if self.num_pebbles > self.max_pebbles:
                        self.max_pebbles = self.num_pebbles
                    if (self.debug):
                        print "Pebble added to node " + str(v)
        else:
            print "Error: Attempted to pebble node " + str(v) + " but it has already been pebbled"

    def is_source(self, v):
        return (self.B[str(v)][0] is None and self.B[str(v)][1] is None and self.B[str(v)][2] and self.B[str(v)][3] is None and
                self.B[str(v)][4] is None and self.B[str(V)][5] is None and self.B[str(v)][6] is None)

    def get_parents(self, v):
        return self.B[str(v)]

    def print_graph(self):
        print "[",
        for i in range(self.size):
            print ("[" + str(self.B[str(i)][0]) + ", " + str(self.B[str(i)][1]) + "," + str(self.B[str(i)][2]) + "," + str(self.B[str(i)][3]) +
                   "," + str(self.B[str(i)][4]) + "," + str(self.B[str(i)][5]) + "," + str(self.B[str(i)][6]) + "]",)
        print "]"

    def start_debug(self):
        self.debug = True

    def stop_debug(self):
        self.debug = False

    def list_values(self):
        values = []
        for i in range(self.size):
            values.append(self.pebble_value[str(i)])
        return values

