from mininet.net import Mininet
from mininet.node import Host
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.link import TCLink
import shelve, random, threading, time, sys

class SingleSwitchTopo(Topo):
        "Single switch connected to n hosts."
        def build(self, n):
            switch = self.addSwitch('s1')
            for h in range(n):
                # Each host gets 50%/n of system CPU
                host = self.addHost('h%s' % (h + 1))
                # 10 Mbps
                self.addLink(host, switch, bw=100, delay='50ms')

def P2P(n, d):
    "Adds n hosts, each with d neighbors"

    topo = SingleSwitchTopo(n+1)
    net = Mininet(topo=topo, link=TCLink)

#    net = Mininet()
#    for i in range(1, n+2):
#        h = net.addHost('h' + str(i))
#      
#    for i in range(1, n+1):
#        net.addLink(net.hosts[n], net.hosts[i-1])
#        f = i
#        for k in range(1, (d/2)+1):
#            f += 1
#            if f == n + 1:
#                f = 1
#            net.addLink(net.hosts[i-1], net.hosts[f-1])
    
    net.start()
    start = time.time()
    
    counter_thread = threading.Thread(target=startCounter,args=(net.hosts[n], n, d, start))
    counter_thread.start()

    for ind in range(1, n+1):
        solver_thread = threading.Thread(target=startSolver,args=(net.hosts[ind-1], ind, n, d))
        solver_thread.start()
        time.sleep(0.2)

def startSolver(h, ind, n, d):
    print "Starting solver " + str(ind)
    h.cmd("python startSolver.py "+str(ind)+" "+str(n)+" "+str(d))

def startCounter(h, n, d, start):
    print "Starting counter"
    h.cmd("python startCounter.py "+str(n)+" "+str(d)+" "+str(start))

if __name__ == '__main__':
#    setLogLevel('debug')
    n = int(sys.argv[1])
    d = int(sys.argv[2])
    P2P(n, d)
