import solver
import sys
import time

if __name__ == '__main__':
    hostID = int(sys.argv[1])
    n = int(sys.argv[2])
    d = int(sys.argv[3])

    sys.stdout = open("./solver/h" + str(hostID) + ".txt", "w")
    sys.stderr = sys.stdout

    s = solver.Solver(hostID, n, d, [15, 0, 1, 2, 3])
    
    print "Host h" + str(hostID) + " now running."
