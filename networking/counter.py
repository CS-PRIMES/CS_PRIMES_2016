from SimpleXMLRPCServer import SimpleXMLRPCServer
from collections import defaultdict
import threading, sys, xmlrpclib, time

def genIP(i):
    return '10.0.' + str(i/256) + '.' + str(i%256)

class Counter:

    def __init__(self, n, start):
        self.n = n
        self.start = start
        self.percent = 5
        self.stop_server = False
        self.votes = {}
        self.votes = defaultdict(lambda:0, self.votes)
        self.setup_server()
        self.setup_update()
        self.notify_solvers()
        
    def setup_server(self):
        self.server = SimpleXMLRPCServer((genIP(self.n+1), 8000),
                                         allow_none = True)
        self.server.register_function(self.addVote, 'addVote')
        self.server.register_function(self.add, 'add')

    def kill_server(self):
        self.stop_server = True

    def addVote(self, pk1, pk2):
        print "Reached addVote:", pk1
        self.votes[pk1] += 1
        print self.votes[pk1]
        while self.votes[pk1] >= (self.percent * self.n)/100:
            print self.percent, "% consensus reached in", time.time() - self.start, "seconds"
            self.percent += 5
        if self.votes[pk1] >= (9 * self.n)/10: # can change
            self.kill_server()
            print "Consensus took:", time.time() - self.start, "seconds"
        self.votes[pk2] -= 1

    def add(self, pk1):
        print "Reached add", pk1
        self.votes[pk1] += 1

    def setup_update(self):
        while not self.stop_server:
            self.server.handle_request()

    def notify_solvers(self):
        for i in range(1, self.n+1):
            proxy = xmlrpclib.ServerProxy("http://" + genIP(i) + ":8000/")
            proxy.consensus()
