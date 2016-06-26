import pebble
import pebbling_algos
import datetime
import sys
import re

# HOW TO USE THIS TEST FILE:
# 1. Make sure there is a folder called test_logs in this directory.  That is where the logs will be saved.
# 2. In command line or the Python shell (whichever you use), run the start() function
# 3. Run whichever tests you would like by calling the corresponding functions
# 4. Run the end() function
# 5. You will now see a new file in the test_logs folder.  Its name will be the timestamp of when you started the test.
#    You can rename this file for ease of future access if you wish.

# TEST FUNCTIONS (Feel free to add more)

def pebble_all_dfp(r):
	print("***************")
	print("Running pebble_all_dfp("+str(r)+"), starting at "+str(datetime.datetime.now())+".")
	p = pebble.PebbleGraph(r)
	for i in range(p.size()):
		print("Pebbling vertex "+str(i))
		pebbling_algos.depth_first_pebble(p, i)
		if(p.is_pebbled(i)):
			print("Vertex "+str(i)+" successfully pebbled, using "+str(p.max_pebbles)+" pebble(s) in total.")
                else:
                        print "Vertex " + str(i) + "was not successfully pebbled."
		p.reset()
	print("pebble_all_dfp("+str(r)+") completed at "+str(datetime.datetime.now())+".")
	print("***************")
        p.close_files()

def pebble_all_trivial(r):
	print("***************")
	print("Running pebble_all_trivial("+str(r)+").")
	p = pebble.PebbleGraph(r)
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
        p.close_files

def pebble_sinks_dfp(r):
	print("***************")
	print("Running pebble_sinks_dfp("+str(r)+"), starting at "+str(datetime.datetime.now())+".")
	p = pebble.PebbleGraph(r)
	for i in range(p.size()-2**r, p.size()): # just the sinks
		print("Pebbling vertex "+str(i))
		pebbling_algos.depth_first_pebble(p, i)
		if(p.is_pebbled(i)):
			print("Vertex "+str(i)+" successfully pebbled, using "+str(p.max_pebbles)+" pebble(s) in total.")
                else:
                        print "Vertex " + str(I) + " was not successfully pebbled."
		p.reset()
	print("pebble_sinks_dfp("+str(r)+") completed at "+str(datetime.datetime.now())+".")
	print("***************")
        p.close_files()

def pebble_sinks_trivial(r):
	print("***************")
	print("Running pebble_sinks_trivial("+str(r)+"), starting at "+str(datetime.datetime.now())+".")
	p = pebble.PebbleGraph(r)
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
        p.close_files

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
