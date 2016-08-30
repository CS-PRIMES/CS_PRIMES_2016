#!/usr/bin/python -t

import shelve
import utils
import ptc
import datetime

class PebbleGraph:
    
    def __init__(self, r, pre_generated_graph=0, debug=False):
        # set pre_generated_graph to be True if the file all_graphs already contains all the neccessary parents on your computer.
        self.all_graphs = shelve.open('all_graphs.txt', writeback=True)
        self.pebble_value = open('pebble_value.txt', 'r+')
        self.num_pebbles = 0                                           # num_pebbles is the number of pebbles currently on the graph.
        self.max_pebbles = 0                                           # max_pebbles it the maximum number of pebbles that have been on the graph since the last reset.
        self.graph_num = r
        if pre_generated_graph == 0:
            ptc.PTC(r, self.all_graphs)
        self.pebble_value.seek(0)
        for i in range(self.size()):
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
        if self.pebble_value.read(64) != 'None' + 60 * '*':
            return True
        else:
            return False

    def remove_pebble(self, v):
        if(self.is_pebbled(v) and v is not None):
            self.pebble_value.seek(v * 64)
            self.pebble_value.write('None' + 60 * '*')
            self.num_pebbles -= 1
            if (self.debug):
                print "Pebble removed from node "+str(v)

    def remove_pebbles(self, S):
        for v in S:
            self.remove_pebble(v)

    def reset(self):
        self.pebble_value.seek(0)
        for i in range(self.size()):
            self.pebble_value.write ('None' + 60 * '*')
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
                    self.pebble_value.seek(v * 64)
                    self.pebble_value.write(utils.secure_hash(str(v)))
                    self.num_pebbles += 1
                    if self.num_pebbles > self.max_pebbles:
                        self.max_pebbles = self.num_pebbles
                    if (self.debug):
                        print "Pebble added to node " + str(v)
                elif self.is_pebbled(self.all_graphs[str(self.graph_num)][v][0]) and (self.all_graphs[str(self.graph_num)][v][1] is None):
                    self.pebble_value.seek(64 * self.all_graphs[str(self.graph_num)][v][0])
                    pre_hash = self.pebble_value.read(64)
                    self.pebble_value.seek(64 * v)
                    self.pebble_value.write(utils.secure_hash(pre_hash))
                    self.num_pebbles += 1
                    if self.num_pebbles > self.max_pebbles:
                        self.max_pebbles = self.num_pebbles
                    if (self.debug):
                        print "Pebble added to node " + str(v)
                elif self.is_pebbled(self.all_graphs[str(self.graph_num)][v][0]) and self.is_pebbled(self.all_graphs[str(self.graph_num)][v][1]):
                    self.pebble_value.seek(64 * self.all_graphs[str(self.graph_num)][v][0])
                    first_prehash = self.pebble_value.read(64)
                    self.pebble_value.seek(64 * self.all_graphs[str(self.graph_num)][v][1])
                    second_prehash = self.pebble_value.read(64)
                    self.pebble_value.seek(64 * v)
                    self.pebble_value.write(utils.secure_hash(first_prehash + second_prehash))
                    self.num_pebbles += 1
                    if self.num_pebbles > self.max_pebbles:
                        self.max_pebbles = self.num_pebbles
                    if (self.debug):
                        print "Pebble added to node " + str(v)
                else:
                    print "Error: attempted to pebble node " + str(v) + " without pebbling both parents"
            else:
                print "Attempted to pebble node " + str(v) + " but it has already been pebbled"

        else: # This is meant to run faster and to execute trivial_pebble_graph(). It won't detect errors in the code.
            if v < 2**self.graph_num: # is a source
                self.pebble_value.write(utils.secure_hash(str(v))) # There is no seek before.
                # There is no code for setting self.max_pebbles, because this is not for testing code.
            elif self.all_graphs[str(self.graph_num)][v][1] == None: # has only one parent
                self.pebble_value.seek(64 * self.all_graphs[str(self.graph_num)][v][0])
                pre_hash = self.pebble_value.read(64)
                self.pebble_value.seek(64 * v)
                self.pebble_value.write(utils.secure_hash(pre_hash))
            else: # has two parents
                self.pebble_value.seek(64 * self.all_graphs[str(self.graph_num)][v][0])
                prehash = self.pebble_value.read(64)
                self.pebble_value.seek(64 * self.all_graphs[str(self.graph_num)][v][1])
                second_prehash = self.pebble_value.read(64)
                self.pebble_value.seek(64 * v)
                self.pebble_value.write(utils.secure_hash(prehash + second_prehash))
            
            
    def is_source(self, v):
        return (self.all_graphs[str(self.graph_num)][v][0] == None and self.all_graphs[str(self.graph_num)][v][1] == None)

    def get_parents(self, v):
        return self.all_graphs[str(self.graph_num)][v]

    def size(self):
        return ptc.ptcsize(self.graph_num)

    def print_graph(self):
        print "[",
        for i in range(self.size()):
            print "[" + str(self.all_graphs[str(self.graph_num)][i][0]) + ", " + str(self.all_graphs[str(self.graph_num)][i][1]) + "]",
        print "]"

    def start_debug(self):
        self.debug = True

    def stop_debug(self):
        self.debug = False

    def list_values(self): # I noticed that since values does not use persistent storage, this will fail for large graphs.
        values = []
        self.pebble_value.seek(0)
        for i in range(self.size()):
            values.append(self.pebble_value.read(64))
        return values


    def write_value(value, index):
        # value should be exactly 64 bytes. value will be written to the place where the hash associated with the indexth pebble is.
        self.pebble_value.seek(64 * index)
        self.pebble_value.write(value)

    def read_value(value, index): # value will be equal to what is read from the file.
        self.pebble_value.seek(64 * index)
        value = self.pebble_value.read(64)
