import Pyro4
import json
import random
import socket
from colorama import init, Fore, Back, Style
from threading import Thread
from time import sleep

Pyro4.config.REQUIRE_EXPOSE = True

bill = {}
handling_customer = False
uri = ""
counter = 0
myIP = ""


class Cashier(object):
    @Pyro4.expose
    def listen(self, from_person, from_name, msg):
        respond_t = Thread(target=respond, args=(from_person, from_name, msg))
        respond_t.start()
        return ""


def serve_customer():
    while True:
        customer_queue = Pyro4.Proxy("PYRONAME:lavic.queue.customer")
        customer_queue_size = 0
        while (customer_queue_size == 0):
            customer_queue_size = int(customer_queue.get_size())
            sleep(2)
        next_customer = Pyro4.Proxy("PYRONAME:" + customer_queue.getNextCustomer())
        customer_queue._pyroRelease()
        global handling_customer
        print next_customer
        if not (next_customer is None):
            print next_customer.listen("Cashier", uri, get_greet_msg())
            handling_customer = True
            while handling_customer:
                sleep(1)
        next_customer._pyroRelease()
        sleep(1)


def cashier_thread():
    cashier = Cashier()
    daemon = Pyro4.Daemon(myIp)
    global uri
    uri = daemon.register(cashier)
    print_main_title("Cashier on duty : "+ str(uri))
    daemon.requestLoop()


def getToken():
    global counter
    counter = counter + 1
    return str(random.randrange(0, 101, 2)) + str(counter) + str(random.randrange(0, 101, 2))


def calculate_bill(customer_order):
    global bill
    bill = {}
    order = {}
    order['tokenNumber'] = getToken()
    orderDetails = []
    cost = 0
    menu_card = Pyro4.Proxy("PYRONAME:lavic.menucard")
    for customer_order_item in customer_order['order']['orderDetails']:
        orderItem = {}
        orderItem['itemName'] = customer_order_item['itemName']
        orderItem['unitCost'] = menu_card.getItem(customer_order_item['itemName'])["price"]
        cost = cost + float(orderItem['unitCost'])
        orderItem['quantity'] = customer_order_item['quantity']
        orderDetails.append(orderItem)
    menu_card._pyroRelease()
    order['orderDetails'] = orderDetails
    order['cost'] = cost
    order['tax'] = 0.10
    order['total'] = cost * 0.10
    bill['order'] = order
    return bill


def respond(from_person, from_name, msg):
    parsed_msg = msg
    if parsed_msg['messageType'] == "HELLO":
        respond_to_hello(from_person, from_name, msg)
    elif parsed_msg['messageType'] == "INTERACTION":
        respond_to_interaction(from_person, from_name, msg)
    elif parsed_msg['messageType'] == 'BBYE':
        respond_to_bye(from_person, from_name, msg)
    elif parsed_msg['messageType'] == 'ORDER_REQUEST':
        respond_to_order_request(from_person, from_name, msg)
    elif parsed_msg['messageType'] == 'PAYMENT_REQUEST':
        respond_to_payment_request(from_person, from_name, msg)


def respond_to_hello(from_person, from_name, msg):
    print_success(from_person + " [" + from_name + "] : " + json.dumps(msg))
    customer = Pyro4.Proxy("PYRONAME:" + from_name)
    customer.listen("Cashier", uri, get_order_question_msg())
    customer._pyroRelease()


def respond_to_interaction(from_person, from_name, msg):
    print_success(from_person + " [" + from_name + "] : " + json.dumps(msg))
    customer = Pyro4.Proxy("PYRONAME:" + from_name)
    customer.listen("Cashier", uri, get_order_question_msg())
    customer._pyroRelease()


def respond_to_order_request(from_person, from_name, msg):
    print_info(from_person + " [" + from_name + "] : " + json.dumps(msg))
    customer = Pyro4.Proxy("PYRONAME:" + from_name)
    customer.listen("Cashier", uri, get_payment_request_msg(msg))
    customer._pyroRelease()


def respond_to_payment_request(from_person, from_name, msg):
    print_info(from_person + " [" + from_name + "] : " + json.dumps(msg))
    customer = Pyro4.Proxy("PYRONAME:" + from_name)
    customer.listen("Cashier", uri, get_payment_made_msg())
    customer._pyroRelease()


def respond_to_bye(from_person, from_name, msg):
    global handling_customer
    handling_customer = False
    pending_request_queue = Pyro4.Proxy("PYRONAME:lavic.queue.pendingOrders")
    pending_request_queue.addOrder(get_order_incomplete_msg())
    print_success(from_person + " [" + from_name + "] : " + json.dumps(msg))
    customer = Pyro4.Proxy("PYRONAME:" + from_name)
    customer.listen("Cashier", uri, get_bye_msg())
    customer._pyroRelease()


def get_greet_msg():
    msg = {}
    msg['messageType'] = "HELLO"
    msg['message'] = "Hello, Welcome to Lavic. :) "
    return msg


def get_order_question_msg():
    msg = {}
    msg['messageType'] = "ORDER_REQUEST"
    msg['message'] = "What would you like to have today ?"
    return msg


def get_order_incomplete_msg():
    msg = {}
    msg['messageType'] = "ORDER_INCOMPLETE"
    msg['message'] = ''
    msg['order'] = bill['order']
    return msg


def get_payment_request_msg(customer_order_msg):
    msg = {}
    msg['messageType'] = "PAYMENT_REQUEST"
    msg['message'] = 'Your total charges : '
    msg['order'] = calculate_bill(customer_order_msg)
    return msg


def get_payment_made_msg():
    msg = {}
    msg['messageType'] = "PAYMENT_MADE"
    msg['message'] = ' Payment Complete.'
    msg['order'] = bill['order']
    return msg


def get_bye_msg():
    msg = {}
    msg['messageType'] = "BBYE"
    msg['message'] = "Thank you. Visit Us Again"
    return msg



def print_success( message):
    print(Back.GREEN + Style.BRIGHT  +  Fore.BLACK + " SUCCESS " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def print_info( message):
    print(Back.BLUE + Style.BRIGHT  +  Fore.WHITE + " INFO " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def print_error( message):
    print( Back.RED + Style.BRIGHT  +  Fore.WHITE + " ERROR " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def print_network( message):
    print( Back.YELLOW + Style.BRIGHT  +  Fore.BLACK + " NETWORK " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def print_title(message):
    print(Fore.GREEN + Style.BRIGHT)
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("                 " + str(message))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def print_main_title(message):
    print(Fore.CYAN + Back.WHITE + Style.BRIGHT)
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
    print(Back.RESET)
    print( "                        " + str(message).upper()+ "                     ")
    print(Back.WHITE)
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def clear_screen():
    print("\033c")

if __name__ == "__main__":
    global myIp
    myIp = str(socket.gethostbyname(socket.gethostname()))
    cash_t = Thread(target=cashier_thread)
    serve_customer_t = Thread(target=serve_customer)
    serve_customer_t.start()
    cash_t.start()
    serve_customer_t.join()
    cash_t.join()
    print_title("Lavik is closed now")








