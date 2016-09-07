#!/usr/bin/python -t

import utils
import linear_ptc

class PebbleGraph:
    
    def __init__(self, r, pre_generated_graph=False, debug=False):
        self.hash_length = utils.hash_length()
        self.all_graphs = open("all_linear_graphs.txt", "r+")                # all_graphs contains the parents of every single ptc graph up to size r.
        self.pebble_value = open("linear_pebble_value.txt", "r+")            # pebble_value stores the value of the hash associated with the pebble.
        self.num_pebbles = 0                                           # num_pebbles is the number of pebbles currently on the graph.
        self.max_pebbles = 0                                           # max_pebbles it the maximum number of pebbles that have been on the graph since the last reset.
        self.graph_num = r
        self.size = linear_ptc.linear_ptcsize(self.graph_num)
        if pre_generated_graph == False:
            linear_ptc.linear_PTC(r, self.all_graphs)
        self.all_graphs_increment = len(str(linear_ptc.linear_ptcsize(self.graph_num))) # The number of bytes each parent in all_graphs takes.
        self.all_graphs_start = linear_ptc.all_graphs_start(self.graph_num) # The position where the rth graph is stored in all_graphs.
        self.all_graphs.seek(self.all_graphs_start + 7 * 2**(self.graph_num+6) * self.all_graphs_increment)
        self.pebble_value.seek(0)
        for i in range(self.size):
            self.pebble_value.write("\00" * self.hash_length)
        self.pebble_value.seek(0)
        self.debug = debug
        
    def close_files(self):
        self.pebble_value.close()
        self.all_graphs.close()

    def is_pebbled(self, v):
        if v is "\00" * self.all_graphs_increment:
            return True
        self.pebble_value.seek(v * self.hash_length)
        if self.pebble_value.read(self.hash_length) != "\00" * self.hash_length:
            return True
        else:
            return False
        
    def remove_pebble(self, v):
        if(self.is_pebbled(v) and v is not "\00" * self.all_graphs_increment):
            self.pebble_value.seek(self.hash_length * v)
            self.pebble_value.write("\00" * self.hash_length)
            self.num_pebbles -= 1
            if (self.debug):
                print "Pebble removed from node "+str(v)

    def remove_pebbles(self, S):
        for v in S:
            self.remove_pebble(v)

    def reset(self):
        self.pebble_value.seek(0)
        for i in range(self.size):
            self.pebble_value.write("\00" * self.hash_length)
        self.num_pebbles = 0
        self.max_pebbles = 0
        if (self.debug):
            print "All pebbles have been removed from the graph"

    def add_pebble(self, v):
        if self.debug:
            if v is "\00" * self.all_graphs_increment:
                return
            if not self.is_pebbled(v):
                if self.is_source(v):
                    self.pebble_value.seek(self.hash_length * v)
                    self.pebble_value.write(utils.secure_hash(str(v)))
                    self.num_pebbles += 1
                    if self.num_pebbles > self.max_pebbles:
                        self.max_pebbles = self.num_pebbles
                    if (self.debug):
                        print "Pebble added to node " + str(v)
                else:
                    self.all_graphs.seek(7 * v * self.all_graphs_increment)
                    parents = []
                    prehash = ""
                    error = 0
                    for i in range(7):
                        parents.append(all_graphs.read(self.all_graphs_increment))
                        if parents[i] != "\00" * self.all_graphs_increment:
                            self.pebble_value.seek(self.hash_length * parents[i])
                            parent_hash = self.pebble_value.read(hash_length)
                            if parent_hash =="\00" * self.hash_length:
                                print "Error: Attempted to pebble node " + str(v) + "without pebbling parent " + str(i) + "."
                                error = 1
                            else:
                                prehash = prehash + parent_hash
                    if error == 0:
                        self.pebble_value.seek(self.hash_length * v)
                        self.pebble_value.write(utils.secure_hash(str(v)))
                        self.num_pebbles += 1
                        if self.num_pebbles > self.max_pebbles:
                            self.max_pebbles = self.num_pebbles
                        if (self.debug):
                            print "Pebble added to node " + str(v)
            else:
                print "Error: Attempted to pebble node " + str(v) + " but it has already been pebbled"

        else: # This is not for testing, but to run linear_pebble_graph_trivial as fast as possible.
            if v is "\00" * self.all_graphs_increment:
                return
            if v < 64 * 2**self.graph_num:
                self.pebble_value.write(utils.secure_hash(str(v)))
            else:
                self.all_graphs.seek(self.all_graphs_start + self.all_graphs_increment * 7 * v)
                prehash = ""
                for i in range(7):
                    parent = self.all_graphs.read(self.all_graphs_increment)
                    if parent != "\00" * self.all_graphs_increment:
                        self.pebble_value.seek(self.hash_length * int(parent))
                        prehash = prehash + self.pebble_value.read(self.hash_length)
                self.pebble_value.seek(self.hash_length * v)
                self.pebble_value.write(utils.secure_hash(prehash))
                
                
                    
                
    def is_source(self, v):
        self.all_graphs.seek(self.all_graphs_start + 7 * v * self.all_graphs_increment)
        return self.all_graphs.read(self.all_graphs_increment * 7) == "\00" * self.all_graphs_increment * 7

    def get_parents(self, v):
        self.all_graphs.seek(self.all_graphs_start + self.all_graphs_increment * 7 * v)
        parents = []
        for i in range(7):
            parents.append(self.all_graphs.read(self.all_graphs_increment))
        return parents

    def print_graph(self):
        self.all_graphs.seek(self.all_graphs_start)
        print "[",
        for i in range(self.size):
            print ("[" +
                   self.all_graphs.read(self.all_graphs_increment) +
                   ", " +
                   self.all_graphs.read(self.all_graphs_increment) +
                   "," +
                   self.all_graphs.read(self.all_graphs_increment) +
                   "," +
                   self.all_graphs.read(self.all_graphs_increment) +
                   "," +
                   self.all_graphs.read(self.all_graphs_increment) +
                   "," +
                   self.all_graphs.read(self.all_graphs_increment) +
                   "," +
                   self.all_graphs.read(self.all_graphs_increment) +
                   "]",)
        print "]"

    def start_debug(self):
        self.debug = True

    def stop_debug(self):
        self.debug = False

    def list_values(self): # values does not use persistent storage, so it will fail for large graphs.
        values = []
        self.pebble_value.seek(0)
        for i in range(self.size):
            values.append(self.pebble_value.read(self.hash_length))
        return values

