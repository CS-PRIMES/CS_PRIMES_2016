from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import info, setLogLevel
from mininet.cli import CLI
from time import sleep
import threading

N = 9 # total number of nodes; if this is to be changed,
# make sure to also change the N in host.py

def consensusTest():
        topo = SingleSwitchTopo(N)
        net = Mininet(topo)
        net.start()
#       net.startTerms()
        hosts = net.hosts
        print "Starting test..."
        for id in range(1,N+1):
                host_thread = threading.Thread(target=startHost,args=(id, hosts[id-1]))
                host_thread.start()
                sleep(0.03)
        CLI(net)

def startHost(id, h):
        print "Starting host "+str(id)
        h.cmd('python startHost.py '+str(id))

if __name__ == '__main__':
        consensusTest()
