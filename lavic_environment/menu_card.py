import json
import Pyro4
import socket
import sys
Pyro4.config.REQUIRE_EXPOSE = True

class MenuCard(object):

    def __init__(self):
        self.menu_card =json.loads(open(str(sys.argv[1])).read())

    @Pyro4.expose
    def getmenucard(self):
        return self.menu_card

    @Pyro4.expose
    def getItem(self, lookup):
       for key, value in self.menu_card.items():
           for v in value:
                for innerKey,innerValue in v.items():
                    if lookup in innerKey:
                        return innerValue;

menuCard=MenuCard()
myIp = str(socket.gethostbyname(socket.gethostname()))
daemon=Pyro4.Daemon(myIp)
ns=Pyro4.locateNS()
uri=daemon.register(menuCard)
ns.register("lavic.menucard", uri)
print "Menu Card Serice started on : ",uri
daemon.requestLoop()