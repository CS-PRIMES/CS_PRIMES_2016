#!/usr/bin/python -t

import shelve
import utils
import linear_ptc

class PebbleGraph:
    
    def __init__(self, r, pre_generated_graph=False, debug=False):
        self.all_graphs = shelve.open('all_linear_graphs.txt', writeback=True)                # all_graphs contains the parents of every single ptc graph up to size r.
        self.pebble_value = open('pebble_value.txt', 'r+')            # pebble_value stores the value of the hash associated with the pebble.
        self.num_pebbles = 0                                           # num_pebbles is the number of pebbles currently on the graph.
        self.max_pebbles = 0                                           # max_pebbles it the maximum number of pebbles that have been on the graph since the last reset.
        self.graph_num = r
        self.size = linear_ptc.linear_ptcsize(self.graph_num)
        if pre_generated_graph == False:
            linear_ptc.linear_PTC(r, self.all_graphs)
        self.pebble_value.seek(0)
        for i in range(self.size):
            self.pebble_value.write('None' + 60 * '*')
        self.pebble_value.seek(0)
        self.debug = debug
        
    def close_files(self):
        self.pebble_value.close()
        self.all_graphs.close()

    def is_pebbled(self, v):
        if v is None:
            return True
        self.pebble_value.seek(v * 64)
        if self.pebble_value.read(64) != 'None' + 60 * "*":
            return True
        else:
            return False
        
    def remove_pebble(self, v):
        if(self.is_pebbled(v) and v is not None):
            self.pebble_value.seek(64 * v)
            self.pebble_value.write('None' + 60 * '*')
            self.num_pebbles -= 1
            if (self.debug):
                print "Pebble removed from node "+str(v)

    def remove_pebbles(self, S):
        for v in S:
            self.remove_pebble(v)

    def reset(self):
        self.pebble_value.seek(0)
        for i in range(self.size):
            self.pebble_value.write('None' + 60 * '*')
        self.num_pebbles = 0
        self.max_pebbles = 0
        if (self.debug):
            print "All pebbles have been removed from the graph"

    def add_pebble(self, v):
        if self.debug:
            if v is None:
                return
            if not self.is_pebbled(v):
                if self.is_source(v):
                    self.pebble_value.seek(64 * v)
                    self.pebble_value.write(utils.secure_hash(str(v)))
                    self.num_pebbles += 1
                    if self.num_pebbles > self.max_pebbles:
                        self.max_pebbles = self.num_pebbles
                    if (self.debug):
                        print "Pebble added to node " + str(v)
                else:
                    prehash = ""
                    error = 0
                    for i in range(7):
                        if self.all_graphs[str(self.graph_num)][v][i] != None:
                            self.pebble_value.seek(64 * self.all_graphs[str(self.graph_num)][v][i])
                            if self.pebble_value.read(64) =='None' + 60 * '*':
                                print "Error: Attempted to pebble node " + str(v) + "without pebbling parent " + str(i) + "."
                                error = 1
                            else:
                                prehash = prehash + str(self.pebble_value[str(self.all_graphs[str(self.graph_num)][v][i])])
                    if error == 0:
                        self.pebble_value.seek(64 * v)
                        self.pebble_value.write(utils.secure_hash(str(v)))
                        self.num_pebbles += 1
                        if self.num_pebbles > self.max_pebbles:
                            self.max_pebbles = self.num_pebbles
                        if (self.debug):
                            print "Pebble added to node " + str(v)
            else:
                print "Error: Attempted to pebble node " + str(v) + " but it has already been pebbled"

        else: # This is not for testing, but to run linear_pebble_graph_trivial as fast as possible.
            if v is None:
                return
            if v < 64 * 2**self.graph_num:
                self.pebble_value.write(utils.secure_hash(str(v)))
            else:
                parents = self.all_graphs[str(self.graph_num)][v]
                prehash = ''
                for i in range(7):
                    if parents[i] != None:
                        self.pebble_value.seek(64 * parents[i])
                        prehash = prehash + self.pebble_value.read(64)
                self.pebble_value.seek(64 * v)
                self.pebble_value.write(utils.secure_hash(prehash))
                
                
                    
                
            

    def is_source(self, v):
        return (self.all_graphs[str(self.graph_num)][v][0] is None and
                self.all_graphs[str(self.graph_num)][v][1] is None and
                self.all_graphs[str(self.graph_num)][v][2] is None and
                self.all_graphs[str(self.graph_num)][v][3] is None and
                self.all_graphs[str(self.graph_num)][v][4] is None and
                self.all_graphs[str(self.graph_num)][v][5] is None and
                self.all_graphs[str(self.graph_num)][v][6] is None)

    def get_parents(self, v):
        return self.all_graphs[str(self.graph_num)][v]

    def print_graph(self):
        print "[",
        for i in range(self.size):
            print ("[" +
                   str(self.all_graphs[str(self.graph_num)][i][0]) +
                   ", " +
                   str(self.all_graphs[str(self.graph_num)][str(i)][1])
                   + "," +
                   str(self.all_graphs[str(self.graph_num)][str(i)][2])
                   + "," +
                   str(self.all_graphs[str(self.graph_num)][i][3]) +
                   "," +
                   str(self.all_graphs[str(self.graph_num)][i][4]) +
                   "," +
                   str(self.all_graphs[str(self.graph_num)][i][5]) +
                   "," +
                   str(self.all_graphs[str(self.graph_num)][i][6]) +
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
            values.append(self.pebble_value.read(64))
        return values

