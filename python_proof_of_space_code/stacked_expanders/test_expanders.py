import datetime
import expander
import re
import sys
import time

def create_expander_graph(n):
    print "***************"
    print "Running create_expander_graph(" + str(n) + "), starting at ",
    print str(datetime.datetime.now()) + "."
    start_time = time.time()
    p = expander.expanders(n, 1)
    time_elapsed = time.time() - start_time
    print "Elapsed time: " + str(time_elapsed)
    print "Vertices for whom parents were generated per second: " + str(n/time_elapsed)
    print "***************"
    p.close_files()
    

def pebble_stacked_expander(n, k, pre_generated_graph=False):
    print "***************"
    print "Running pebble_stacked_expander(" + str(n) + ", " + str(k) + "), starting at ",
    print str(datetime.datetime.now()) + "."
    p = expander.expanders(n, k, pre_gen_graph=pre_generated_graph)
    start_time = time.time()
    p.trivial_pebble()
    print "Vertices in graph: " + str(p.size)
    print "Time to find final Merkle root: " + str(time.time() - start_time)
    print "Vertices pebbled per second: " + str(p.size/(time.time() - start_time))
    print "Final Merkle root: " + p.merkle_root
    print "***************"
    p.close_files
    
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
