#!/usr/bin/python -t

import utils
import ptc

class PebbleGraph:

    def __init__(self, r, pre_generated_graph=False, debug=False):
        # set pre_generated_graph to be True if the file all_graphs already contains all the neccessary parents on your computer.
        self.hash_length = utils.hash_length()
        self.all_graphs = open('all_graphs.txt', 'r+')
        self.pebble_value = open('pebble_value.txt', 'r+')
        self.num_pebbles = 0                                           # num_pebbles is the number of pebbles currently on the graph.
        self.max_pebbles = 0                                           # max_pebbles it the maximum number of pebbles that have been on the graph since the last reset.
        self.graph_num = r
        if not pre_generated_graph:
            all_graphs.seek(0)
            ptc.PTC(r, self.all_graphs)
        self.all_graphs_increment = len(str(ptc.ptcsize(self.graph_num))) # The number of bytes each parent in all_graphs takes
        self.all_graphs_start = ptc.all_graphs_start(self.graph_num) # The position where the rth graph is stored in all_graphs.
        self.all_graphs.seek(self.all_graphs_start + 2 * 2**self.graph_num * self.all_graphs_increment)
        self.pebble_value.seek(0)
        self.pebble_value.write("\00"*self.hash_length * self.size())
        self.pebble_value.seek(0)
        self.debug = debug

    def close_files(self):
        self.pebble_value.close()
        self.all_graphs.close()

    def is_pebbled(self, v):
        if v is '\00' * self.all_graphs_increment:
            return True
        self.pebble_value.seek(v * self.hash_length)
        if self.pebble_value.read(self.hash_length) != "\00"*self.hash_length:
            return True
        else:
            return False

    def remove_pebble(self, v):
        if(self.is_pebbled(v) and v is not '\00' * self.all_graphs_increment):
            self.pebble_value.seek(v * self.hash_length)
            self.pebble_value.write("\00"*self.hash_length)
            self.num_pebbles -= 1
            if (self.debug):
                print "Pebble removed from node "+str(v)

    def remove_pebbles(self, S):
        for v in S:
            self.remove_pebble(v)

    def reset(self):
        self.pebble_value.seek(0)
        for i in range(self.size()):
            self.pebble_value.write("\00"*self.hash_length)
        self.num_pebbles = 0
        self.max_pebbles = 0
        if (self.debug):
            print "All pebbles have been removed from the graph"

    def add_pebble(self, v):
        if self.debug:
            if v is '\00' * self.all_graphs_increment:
                return
            parents = []
            all_graphs.seek(self.all_graphs_start + 2 * self.all_graphs_increment * v)
            parents.append(all_graphs.read(all_graphs_increment))
            parents.append(all_graphs.read(all_graphs_increment))
            if not self.is_pebbled(v):
                if self.is_source(v):
                    self.pebble_value.seek(v * self.hash_length)
                    self.pebble_value.write(utils.secure_hash(utils.prehash_associated_with_source(v)))
                    self.num_pebbles += 1
                    if self.num_pebbles > self.max_pebbles:
                        self.max_pebbles = self.num_pebbles
                    if (self.debug):
                        print "Pebble added to node " + str(v)
                elif self.is_pebbled(int(parents[0])) and (parents[1]) is '\00' * self.all_graphs_increment:
                    self.pebble_value.seek(self.hash_length * int(parents[0]))
                    pre_hash = self.pebble_value.read(self.hash_length)
                    self.pebble_value.seek(self.hash_length * v)
                    self.pebble_value.write(utils.secure_hash(pre_hash))
                    self.num_pebbles += 1
                    if self.num_pebbles > self.max_pebbles:
                        self.max_pebbles = self.num_pebbles
                    if (self.debug):
                        print "Pebble added to node " + str(v)
                elif self.is_pebbled(int(parents[0])) and self.is_pebbled(int(parents[1])):
                    self.pebble_value.seek(self.hash_length * int(parents[0]))
                    first_prehash = self.pebble_value.read(self.hash_length)
                    self.pebble_value.seek(self.hash_length * int(parents[1]))
                    second_prehash = self.pebble_value.read(self.hash_length)
                    self.pebble_value.seek(self.hash_length * v)
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
                self.pebble_value.write(utils.secure_hash(utils.prehash_associated_with_source(v))) # There is no seek before.
                return
                # There is no code for setting self.max_pebbles, because this is not for testing code.
            parents = [self.all_graphs.read(self.all_graphs_increment), self.all_graphs.read(self.all_graphs_increment)]
            if parents[1] == '\00' * self.all_graphs_increment: # has only one parent
                self.pebble_value.seek(self.hash_length * int(parents[0]))
                prehash = self.pebble_value.read(self.hash_length)
                self.pebble_value.seek(self.hash_length * v)
                self.pebble_value.write(utils.secure_hash(prehash))
            else: # has two parents
                self.pebble_value.seek(self.hash_length * int(parents[0]))
                prehash = self.pebble_value.read(self.hash_length)
                self.pebble_value.seek(self.hash_length * int(parents[1]))
                second_prehash = self.pebble_value.read(self.hash_length)
                self.pebble_value.seek(self.hash_length * v)
                self.pebble_value.write(utils.secure_hash(prehash + second_prehash))

    def is_source(self, v):
        self.all_graphs.seek(self.all_graphs_start + self.all_graphs_increment * v * 2)
        return (self.all_graphs.read(2 * all_graphs_increment) == '\00' * 2 * all_graphs_increment)

    def get_parents(self, v):
        self.all_graphs.seek(self.all_graphs_start + self.all_graphs_increment * v  * 2)
        parents = [self.all_graphs.read(all_graphs_increment), self.all_graphs.read(all_graphs_increment)]
        return parents

    def size(self):
        return ptc.ptcsize(self.graph_num)

    def print_graph(self):
        self.all_graphs.seek(self.all_graphs_start)
        print "[",
        for i in range(self.size()):
            print "[" + self.all_graphs.read(self.all_graphs_increment) + ", " + self.all_graphs.read(self.all_graphs_increment) + "]",
        print "]"

    def start_debug(self):
        self.debug = True

    def stop_debug(self):
        self.debug = False

    def list_values(self): # I noticed that since values does not use persistent storage, this will fail for large graphs.
        values = []
        self.pebble_value.seek(0)
        for i in range(self.size()):
            values.append(self.pebble_value.read(self.hash_length))
        return values


    def write_value(self, value, index):
        # value should be exactly self.hash_length bytes. value will be written to the place where the hash associated with the indexth pebble is.
        self.pebble_value.seek(self.hash_length * index)
        self.pebble_value.write(value)

    def read_value(self, index): # value will be equal to what is read from the file.
        self.pebble_value.seek(self.hash_length * index)
        return self.pebble_value.read(self.hash_length)

    def read_value_noseek(self):
        return self.pebble_value.read(self.hash_length)

    def reset_seek(self):
        self.pebble_value.seek(0)

