import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import time, sys
import shelve
import hashlib

import random # remove later

def PebbleGraph(r):
    # time.sleep(size/1600000)
    time.sleep(1)
    return 1

def trivial_pebble(P, i):
    # time.sleep(size/32000)
    time.sleep(1)

def generateMT():
    # time.sleep(size / )
    time.sleep(1)
    return 1

def generateProof(ind, challenge):
    # time.sleep(size / )
    time.sleep(1)
    return hashlib.sha512(str(ind)+'arbitrary').hexdigest()

def genIP(i):
    return '10.0.' + str(i/256) + '.' + str(i%256)

class Solver:
    
    def __init__(self, ind, n, d, challenge=[15]):
        self.ind = ind
        self.con_r = False
        self.n = n
        self.d = d
        self.challenge = challenge
        self.solve()
        self.setup_neighbor()
        self.setup_server()
        self.setup_update()
        
    def solve(self):
        self.r = self.challenge[0]
        self.p = PebbleGraph(self.r)
        trivial_pebble(self.p, 0)

        self.mt = generateMT()
        self.proof = generateProof(self.ind, self.challenge)                 
        self.public_key = hashlib.sha512(str(self.ind)).hexdigest()
        self.proof_signature = self.public_key

        print "Solved"

    def setup_neighbor(self):
        f = self.ind
        b = self.ind
        self.neighbors = []
        self.IP = genIP(self.ind)
        for k in range(1, (self.d/2)+1):
            f += 1
            if f == self.n + 1:
                f = 1
            self.neighbors.append(genIP(f))
            b -= 1
            if b == 0:
                b = self.n
            self.neighbors.append(genIP(b))            
        
        print "Neighbors:", self.neighbors

    def setup_server(self):
        print self.IP
        SimpleXMLRPCServer.allow_reuse_address = True
        self.server = SimpleXMLRPCServer((self.IP, 8000),
                                         allow_none = True)
        self.server.register_introspection_functions()
        self.server.register_function(self.send_proof, 'send_proof')
        self.server.register_function(self.consensus, 'consensus')
        st = threading.Thread(target=self.start_server)
        st.start()

        print "Server started at " + self.IP + ":8000/"

    def consensus(self):
        self.con_r = True

    def send_proof(self):
        return [self.proof, self.proof_signature]

    def start_server(self):
        while not self.con_r:
            self.server.handle_request()
        print self.ind, "SERVED CLOSED"

    def setup_update(self):
        ut = threading.Thread(target=self.update_proof)
        ut.start()

        print "Update started"

    def quality(self, proof):
        return hashlib.sha512(str(proof)).hexdigest()

    def update_proof(self):
        poll = xmlrpclib.ServerProxy("http://" + genIP(self.n+1) + ":8000/")
        poll.addVote(self.public_key)
        while not self.con_r:
            for a in self.neighbors:
                try:
                    print self.IP, "connecting to " + a
                    proxy = xmlrpclib.ServerProxy("http://" + a + ":8000/")
                    proxy_proof = proxy.send_proof()
                    if self.quality(proxy_proof[0]) > self.quality(self.proof):
                        poll.addVote(proxy_proof[1])
                        print proxy_proof[1]
                        poll.remVote(self.proof_signature)
                        self.proof = proxy_proof[0]
                        self.proof_signature = proxy_proof[1]
                except Exception as err:
                    print err
                    print "Proof failed"
                    pass
