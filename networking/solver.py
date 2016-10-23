import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import time, sys
import shelve
import hashlib
import random

def generateProof(ind, challenge):
    proof = []
    for i in range(30*24):
        proof.append(hashlib.sha512(str(ind)+'arbitrary').hexdigest())
    return proof

def genIP(i):
    return '10.0.' + str(i/256) + '.' + str(i%256)

class Solver:
    
    def __init__(self, ind, n, d, challenge=[16]):
        self.ind = ind
        self.con_r = False
        self.start_pro = False
        self.n = n
        self.d = d
        self.challenge = challenge
        self.solve()
        self.setup_neighbor()
        self.setup_server()
        self.setup_update()
        
    def solve(self):
        self.r = self.challenge[0]
        self.proof = generateProof(self.ind, self.challenge)
        self.public_key = hashlib.sha512(str(self.ind)).hexdigest()
        self.proof_signature = self.public_key

#        print "Solved"

    def setup_neighbor(self):
        self.neighbors = []
        self.IP = genIP(self.ind)
        
        ary = range(1, self.ind) + range(self.ind+1, self.n+1)
        random.shuffle(ary)

        for i in range(0, self.d):
            self.neighbors.append(genIP(ary[i]))
        
#        print "Neighbors:", self.neighbors

    def setup_server(self):
#        print self.IP
        SimpleXMLRPCServer.allow_reuse_address = True
        self.server = SimpleXMLRPCServer((self.IP, 8000),
                                         allow_none = True,
                                         logRequests = False)
        self.server.register_introspection_functions()
        self.server.register_function(self.send_proof, 'send_proof')
        self.server.register_function(self.consensus, 'consensus')
        self.server.register_function(self.start_propogate)
        st = threading.Thread(target=self.start_server)
        st.start()

#        print "Server started at " + self.IP + ":8000/"

    def consensus(self):
        self.con_r = True
    
    def start_propogate(self):
        self.start_pro = True

    def send_proof(self):
        return [self.proof, self.proof_signature]

    def start_server(self):
        while not self.con_r:
            self.server.handle_request()
#        print self.ind, "SERVED CLOSED"

    def setup_update(self):
        ut = threading.Thread(target=self.update_proof)
        ut.start()

#        print "Update started"

    def quality(self, proof):
        proof = "".join(proof)
        return hashlib.sha512(str(proof)).hexdigest()

    def update_proof(self):
        c = True
        while c:
            try:
                self.poll = xmlrpclib.ServerProxy("http://" + genIP(self.n+1) + ":8000/")
                self.poll.add(self.proof_signature)
                c = False
            except Exception:
                pass

        while not self.start_pro:
            time.sleep(0.5)

        while not self.con_r:
            for a in self.neighbors:
                if not self.con_r:
                    try:
#                        print self.IP, "connecting to " + a
                        proxy = xmlrpclib.ServerProxy("http://" + a + ":8000/")
                        proxy_proof = proxy.send_proof()
                        if self.quality(proxy_proof[0]) > self.quality(self.proof):
                            time.sleep(0.005) # accounts for verification
                            self.poll.addVote(proxy_proof[1], self.proof_signature)
#                            print proxy_proof[1]
                            self.proof = proxy_proof[0]
                            self.proof_signature = proxy_proof[1]
                    except Exception as err:
                        print err
                        print "Proof failed"
                        pass
                else:
                    break
                time.sleep(0.05)
