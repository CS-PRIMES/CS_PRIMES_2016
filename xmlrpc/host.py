from time import sleep
import random
import threading

N = 9 # number of hosts; if this is to be changed,
# make sure to also chage the N in topo.py

n = 5 # number of neighbors per host

def generate_neighbors(id, n):
        ary = range(1,id)+range(id+1,N+1)
        for d in range(N-2,0,-1):
                e = random.randint(0,d)
                if e == d:
                        continue
                ary[d],ary[e] = ary[e],ary[d]
        return ary[:n]

class Host:

        def initial_proof(self):
                # right now this is very arbitrary, the only condition
                # is that it is unique to each host
                return hashlib.sha512(str(self.id)+'arbitrary').hexdigest()

        def serve_proof(self):
                return [self.proof, self.proof_signature]

        def update_proof(self):
                print "update proof"
                for id in self.neighbors:
                        try:
                                server = xmlrpclib.ServerProxy("http://10.0.0."+str(id)+":8000")
                                print "server connection made"
                                served_proof = server.serve_proof()
                                print "Got proof from "+str(id)
                                if self.quality(served_proof[0]) > self.quality(self.proof):
                                        self.proof = served_proof[0]
                                        self.proof_signature = served_proof[1]
                                        print "Proof updated to "+served_proof[0]+", from "+served_proof[1]
                        except Exception:
                                print "proof service failed"
                                pass
                        sleep(0.05)

        def test_server(self):
                return "Hello, client!"

        def quality(self, proof):
                return hashlib.sha512(proof).hexdigest()

        def start(self):
#               for a in range(200):
                while True:
                        self.update_proof()

        def __init__(self, id):
                print "Starting up host "+str(id)+"..."
                self.id = id
                self.server = SimpleXMLRPCServer(("10.0.0."+str(self.id),
                                8000), allow_none=True)
                self.server.register_introspection_functions()
                self.server.register_function(self.serve_proof, 'serve_proof')
                self.server.register_function(self.test_server, 'test_server')
                self.proof = self.initial_proof()
                self.neighbors = generate_neighbors(self.id, n)
                print "Neighbors:"
                print self.neighbors
                self.public_key = hashlib.sha512(str(self.id)).hexdigest()
                print "Proof: "+self.proof
                print "Public key: "+self.public_key
                self.proof_signature = self.public_key
                server_thread = threading.Thread(target=self.server.serve_forever)
                server_thread.start()
                print "Now serving"
                update_thread = threading.Thread(target=self.start)
                update_thread.start()
                print "Now updating"
