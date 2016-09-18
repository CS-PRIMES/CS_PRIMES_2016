import counter
import sys
import re
import datetime

if __name__ == '__main__':
    n = int(sys.argv[1])
    d = int(sys.argv[2])
    start = float(sys.argv[3])

    filename = re.sub(r':', '.', str(datetime.datetime.now()))

#    sys.stdout = open("./con_test/(n="+str(n)+", d="+str(d)+") "+filename+".txt", "w")
#    sys.stderr = sys.stdout

    print "Starting test at " + str(datetime.datetime.now()) + "."

    c = counter.Counter(n, start)
