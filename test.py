import pebble, pebbling_algos, trees, primitive_pv, linear_pebble, ptc, shelve, linear_ptc
import datetime
import sys
import re
import time

# HOW TO USE THIS TEST FILE:
# 1. Make sure there is a folder called test_logs in this directory.  That is where the logs will be saved.
# 2. In command line or the Python shell (whichever you use), run the start() function
# 3. Run whichever tests you would like by calling the corresponding functions
# 4. Run the end() function
# 5. You will now see a new file in the test_logs folder.  Its name will be the timestamp of when you started the test.
#    You can rename this file for ease of future access if you wish.

# TEST FUNCTIONS (Feel free to add more)

def create_linear_graphs(n): # creates all linear PTC graphs up to n.
    print "***************"
    print "Running create_linear_graphs(" + str(n) + ", starting at " + str(datetime.datetime.now()) + "."
    all_linear_graphs = shelve.open('all_linear_graphs.txt', writeback=True)
    linear_ptc.linear_PTC(n, all_linear_graphs)
    print "create_linear_graphs(" + str(n) + "), completed at " + str(datetime.datetime.now()) + "."
    print "***************"
    all_linear_graphs.close()
        
def create_butterfly_graphs(n): # creates all butterfly PTC graphs up to n.
    print "***************"
    print "Running create_butterfly_graphs(" + str(n) + "), starting at " + str(datetime.datetime.now()) + "."
    all_graphs = shelve.open('all_graphs.txt', writeback=True)
    ptc.PTC(n, all_graphs)
    print "create_butterfly_graphs(" + str(n) + ") completed at " + str(datetime.datetime.now()) + "."
    print "***************"
    all_graphs.close()

def primitive_pv_test(r):
    print "***************"
    print "Running pv_test("+str(r)+"), starting at "+str(datetime.datetime.now())+"."
    
    print "Initializing prover..."
    P = primitive_pv.Prover(r, debug=True)
    print "Prover initialization complete."
    print "Initializing verifier..."
    V = primitive_pv.Verifier(r, debug=True)
    V.set_prover(P)
    print "Verifier initialization complete."
    print "Commencing verification protocol."
    result = V.verify()
    if result:
        print "Honest prover verified successfully."
    else:
        print "Verification failed; prover will be denied."

    print "pv_test("+str(r)+") completed at "+str(datetime.datetime.now())+"."
    print "***************"
    P.close_files()

def merkle_test(r):
    print "***************"
    print "Running merkle_test("+str(r)+"), starting at "+str(datetime.datetime.now())+"."

    p = pebble.PebbleGraph(r, debug=True)
    pebbling_algos.trivial_pebble(p, p.size()-1)
    print "Building Merkle tree..."
    mt = trees.MerkleNode(p.list_values())
    print "Merkle tree setup complete.  Root: "+mt.root()

    print "merkle_test("+str(r)+") completed at "+str(datetime.datetime.now())+"."
    print "***************"
    p.close_files()

def pebble_all_dfp(r):
    print("***************")
    print("Running pebble_all_dfp("+str(r)+"), starting at "+str(datetime.datetime.now())+".")

    p = pebble.PebbleGraph(r, debug=True)
    for i in range(p.size()):
        print("Pebbling vertex "+str(i))
        pebbling_algos.depth_first_pebble(p, i)
        if(p.is_pebbled(i)):
            print("Vertex "+str(i)+" successfully pebbled, using "+str(p.max_pebbles)+" pebble(s) in total.")
        else:
            print "Vertex " + str(i) + " was not successfully pebbled."
        p.reset()

    print("pebble_all_dfp("+str(r)+") completed at "+str(datetime.datetime.now())+".")
    print("***************")
    p.close_files()

def pebble_all_trivial(r):
    print("***************")
    print("Running pebble_all_trivial("+str(r)+").")

    p = pebble.PebbleGraph(r, debug=True)
    for i in range(p.size()):
        print("Pebbling vertex "+str(i))
        pebbling_algos.trivial_pebble(p, i)
        if(p.is_pebbled(i)):
            print("Vertex "+str(i)+" successfully pebbled, using "+str(p.max_pebbles)+" pebble(s) in total.")
        else:
            print "Vertex " + str(i) + " was not successfully pebbled."
        p.reset()

    print("pebble_all_trivial("+str(r)+") completed at "+str(datetime.datetime.now())+".")
    print("***************")
    p.close_files()

def pebble_sinks_dfp(r):
    print("***************")
    print("Running pebble_sinks_dfp("+str(r)+"), starting at "+str(datetime.datetime.now())+".")

    p = pebble.PebbleGraph(r, debug=True)
    for i in range(p.size()-2**r, p.size()): # just the sinks
        print("Pebbling vertex "+str(i))
        pebbling_algos.depth_first_pebble(p, i)
        if(p.is_pebbled(i)):
            print("Vertex "+str(i)+" successfully pebbled, using "+str(p.max_pebbles)+" pebble(s) in total.")
        else:
            print "Vertex " + str(i) + " was not successfully pebbled."
        p.reset()

    print("pebble_sinks_dfp("+str(r)+") completed at "+str(datetime.datetime.now())+".")
    print("***************")
    p.close_files()

def pebble_sinks_trivial(r):
    print("***************")
    print("Running pebble_sinks_trivial("+str(r)+"), starting at "+str(datetime.datetime.now())+".")

    p = pebble.PebbleGraph(r, debug=True)
    for i in range(p.size()-2**r, p.size()): # just the sinks
        print("Pebbling vertex "+str(i))
        pebbling_algos.trivial_pebble(p, i)
        if(p.is_pebbled(i)):
            print("Vertex "+str(i)+" successfully pebbled, using "+str(p.max_pebbles)+" pebble(s) in total.")
        else:
            print "Vertex " + str(i) + " was not successfully pebbled."
        p.reset()

    print("pebble_sinks_trivial("+str(r)+") completed at "+str(datetime.datetime.now())+".")
    print("***************")
    p.close_files()

def pebble_sinks_level(r):
    print ("***************")
    print ("Running pebble_sinks_level("+str(r)+"), starting at "+str(datetime.datetime.now())+".")

    p = pebble.PebbleGraph(r, debug=True)
    pebbling_algos.level_pebble(p, 0)
    print ("The max amount of pebbles used was: " + str(p.max_pebbles) + ".")

    print ("pebble_sinks_level("+str(r)+") completed at "+str(datetime.datetime.now())+".")
    print ("***************")
    p.close_files()

# This function uses trivial_pebble to pebble the entire graph and all of its vertices.
def pebble_graph_trivial(r, pre_gen_graph=False, debug_flag=False):
    print "***************"
    print "Running pebble_graph_trivial(" + str(r) + ", pre_gen_graph=" + str(pre_gen_graph) + "), starting at " + str(datetime.datetime.now()) + "."
    start_generate = time.time()
    p = pebble.PebbleGraph(r, pre_generated_graph=pre_gen_graph, debug=debug_flag)
    end_generate = time.time()
    start_pebble = time.time()
    pebbling_algos.trivial_pebble(p, p.size() - 1)
    if p.is_pebbled(p.size() - 1):
        print "The final vertex in PTC(" + str(r) + ") was successfully pebbled."
    else:
        print "ERROR: The final vertex in PTC(" + str(r) + ") was not successfully pebbled."
    print "Vertices in graph: " + str(p.size())
    print "Seconds elapsed to generate graph: " + str(end_generate - start_generate)
    print "Vertices generated per second: " + str(p.size() / (end_generate - start_generate))
    print "Seconds elapsed to pebble graph: " + str(time.time() - start_pebble)
    print "Vertices pebbled per second: " + str(p.size() / (time.time() - start_pebble))
    print "Total seconds elapsed: " + str(time.time() - start_generate)
    print "Vertices generated and pebbled per second: " + str(p.size() / (time.time() - start_generate))
    print "pebble_graph_trivial(" + str(r) + ", pre_gen_graph=" + str(pre_gen_graph) + ") completed at " + str(datetime.datetime.now()) + "."
    print "***************"
    p.close_files()

# This function uses linear_trivial_pebble to pebble an entire linear ptc graph and all of its vertices.
def linear_pebble_graph_trivial(r, pre_gen_graph=False, debug_flag=False):
    print "***************"
    print "Running linear_pebble_graph_trivial(" + str(r) + "), starting at " + str(datetime.datetime.now()) + "."
    start_generate = time.time()
    p = linear_pebble.PebbleGraph(r, pre_generated_graph=pre_gen_graph, debug=debug_flag)
    end_generate = time.time()
    start_pebble = time.time()
    pebbling_algos.linear_trivial_pebble(p)
    if p.is_pebbled(p.size - 1):
        print "The final vertex in the linear PTC(" + str(r) + ") was successfully pebbled."
    else:
        print "ERROR: The final vertex in the linear PTC(" + str(r) + ") was not successfully pebbled."
    print "Vertices in graph: " + str(p.size)
    print "Seconds elapsed to generate graph: " + str(end_generate - start_generate)
    print "Vertices generated per second: " + str(p.size / (end_generate - start_generate))
    print "Seconds elapsed to pebble graph: " + str(time.time() - start_pebble)
    print "Vertices pebbled per second: " + str(p.size / (time.time() - start_pebble))
    print "Total seconds elapsed: " + str(time.time() - start_generate)
    print "Vertices generated and pebbled per second: " + str(p.size / (time.time() - start_generate))
    print "pebble_graph_trivial(" + str(r) + ") completed at " + str(datetime.datetime.now()) + "."
    print "***************"
    p.close_files()
    
# START/END FUNCTIONS

def start():
    filename = re.sub(r':', '.', str(datetime.datetime.now()))
    sys.stdout = open("./test_logs/"+filename+".txt", 'w')
    sys.stderr = sys.stdout
    print("Starting test at "+str(datetime.datetime.now())+".")

def end():
    print("Test completed at "+str(datetime.datetime.now())+".")
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
