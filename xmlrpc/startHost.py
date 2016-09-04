import sys
import host
from time import sleep

if __name__ == '__main__':
        id = int(sys.argv[1])
        sys.stdout = open("./tmp/h"+str(id)+"/h"+str(id)+".txt", "w")
        sys.stderr = sys.stdout
        print str(id)
        h = host.Host(id)
        print "Host h"+str(id)+" now running."
        sleep(15)
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
