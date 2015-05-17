import Pyro4
import Queue
import socket

Pyro4.config.REQUIRE_EXPOSE = True

queue = Queue.Queue()

class CustomerQueue(object):

    @Pyro4.expose
    def register(self, name):
        print name + " Joined the Customer Queue"
        queue.put(name)

    @Pyro4.expose
    def getNextCustomer(self):
        return queue.get()
    
    @Pyro4.expose
    def get_size(self):
        return queue.qsize()

custQueue=CustomerQueue()
myIp = str(socket.gethostbyname(socket.gethostname()))
daemon=Pyro4.Daemon(myIp)
ns=Pyro4.locateNS()
uri=daemon.register(custQueue)
ns.register("lavic.queue.customer", uri)
print "Customer Queue Started on : ", uri
daemon.requestLoop()
