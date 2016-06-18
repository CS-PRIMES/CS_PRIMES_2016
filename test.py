import pebble
import pebbling_algos
import datetime
import sys
import re

# Make sure there is a folder called test_logs in this directory.  That is where the logs will be saved.

# Feel free to add more test functions

def pebble_all(r):
	print("b")
	p = pebble.PebbleGraph(r)
	print("a")
	for i in range(p.size()):
		print("Pebbling vertex "+str(i))
		pebbling_algos.depth_first_pebble(p, i)
		p.reset()

# Just don't touch these functions:

def start():
	filename = re.sub(r':', '.', str(datetime.datetime.now()))
	sys.stdout = open("./test_logs/"+filename+".txt", 'w')
	sys.stderr = sys.stdout
	print("Starting test at "+str(datetime.datetime.now()))

def end():
	print("Test completed at "+str(datetime.datetime.now()))
	sys.stdout.close()
	sys.stdout = sys.__stdout__
	sys.stderr = sys.__stderr__