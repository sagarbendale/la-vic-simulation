from Queue import Queue
import socket
import Pyro4

Pyro4.config.REQUIRE_EXPOSE = True

pendingQueue = Queue();
class PendingQueue:

    @Pyro4.expose
    def addOrder(self, order):
        pendingQueue.put(order)
        print "-------------------------"
        print order
        print "-------------------------"

    @Pyro4.expose
    def getOrder(self):
        if(pendingQueue.not_empty):
            return pendingQueue.get()
        else:
            return 0

    @Pyro4.expose
    def getNumberOfOrders(self):
        return pendingQueue.qsize()

orderQueue=PendingQueue()
myIp = str(socket.gethostbyname(socket.gethostname()))
daemon = Pyro4.Daemon(myIp)
ns = Pyro4.locateNS()
uri = daemon.register(orderQueue)
ns.register("lavic.queue.pendingOrders", uri)
print "Pedning Order Queue Started on : ", uri
daemon.requestLoop()