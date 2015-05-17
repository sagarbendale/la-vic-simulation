from time import sleep
import Pyro4
from display import Display


class Chef():
    speed = None
    name = None
    pendingOrderQueue = None
    completedOrderQueue = None
    menuServer = None
    output = None
    def __init__(self, name, speed):
        self.output = Display()
        self.name = name
        self.speed = speed
        self.output._print_main_title("Chef "+str(name)+" is now on duty!")

    def start_work(self):
        self.check_queue()

    def prepare(self,order_details):
        order_details_size = len(order_details)-1
        while order_details_size >= 0:
            quantity = int(order_details[order_details_size]['quantity'])
            item_name = order_details[order_details_size]['itemName']
            self.output._print_info("Preparing "+str(item_name)+" Quantity: "+str(quantity))
            time_to_prepare = self.get_time_from_menu(item_name)
            time_to_prepare *= float(quantity)
            self.output._print_info("Time to prepare: "+str(time_to_prepare))
            sleep(time_to_prepare/self.speed)
            order_details_size -= 1

    def get_time_from_menu(self,item_name):
        self.menuServer = Pyro4.Proxy("PYRONAME:lavic.menucard")  # menu-card queue connect
        item_json = self.menuServer.getItem(item_name)
        self.menuServer._pyroRelease()                            # menu-card queue release
        time = float(item_json['prep_time'])
        return time

    def check_queue(self):
        self.output._print_network("Monitoring Pending Order Queue")
        while True:
            self.pendingOrderQueue = Pyro4.Proxy("PYRONAME:lavic.queue.pendingOrders")   # pending queue connect
            if self.pendingOrderQueue.getNumberOfOrders() > 0:
                next_order = self.pendingOrderQueue.getOrder()
                token_number = int(next_order['order']['tokenNumber'])
                print "Order " + str(token_number) + " is getting prepared"
                if next_order is not None:
                    if next_order['messageType'] == "ORDER_INCOMPLETE":
                        order_details = next_order['order']['orderDetails']
                        self.prepare(order_details)
                        next_order['messageType'] = "ORDER_COMPLETE"
                        self.output._print_success("Token Number:" + str(token_number) + " Ready to Serve")
                        self.completedOrderQueue = Pyro4.Proxy("PYRONAME:lavic.queue.readyOrders")  # completed queue connect
                        self.completedOrderQueue.add_order(next_order)
                        self.completedOrderQueue._pyroRelease()                          # completed queue release
                        self.output._print_network("Order sent to Server")
                        self.pendingOrderQueue._pyroRelease()                            # pending queue release
                else:
                    self.output._print_error("Null Data")
            else:
                sleep(1.0/self.speed)

chef = Chef("Bob", 2.0)
chef.start_work()