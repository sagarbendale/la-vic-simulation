import Queue
from threading import Thread
from time import sleep
import json
from random import randint
import Pyro4

class RequestProcessor(Thread):

	def __init__(self, customer, speed):
		print 'thread init'
		Thread.__init__(self)
		self.forever = True
		self.customer = customer
		self.speed = speed

	def process_message(self, message):
		
		#print message
		respond_to = message['fromName']
		response_message = {}
		
		if message['messageType'] == "HELLO":
			response_message['messageType'] = "HELLO"
			response_message['message'] = "Hi! Thank you."

		elif message['messageType'] == "INTERACTION":
			response_message['messageType'] = "HELLO"
			response_message['message'] = "I am good, how are you?"

		elif message['messageType'] == 'ORDER_REQUEST':
			response_message['messageType'] = "ORDER_REQUEST"
			response_message['message'] = "I will take "
			response_message['order'] = {}
			response_message['order']['orderDetails'] = self.customer.getOrderDetails()

		elif message['messageType'] == 'PAYMENT_REQUEST': #will contain order
			response_message['messageType'] = "PAYMENT_REQUEST"
			response_message['message'] = "Thank you. Here is the cash."
			#print '###########going to save set_receipt'
			self.customer.set_receipt(message['order'])

		elif message['messageType'] == 'PAYMENT_MADE':
			response_message['messageType'] = "BBYE"
			response_message['message'] = "Thank you. Have a great day!"

		elif message['messageType'] == 'ORDER_PREPARED': #will contain order

			if self.customer.checkIfMyOrder(message['order']['tokenNumber']):
				#print str(message['fromName'])
				obj = Pyro4.Proxy(message['fromName'])
				#print  "[[[[[[[]]]]]]]]]]", obj
				#print 'taking order'
				res = obj.take_order()
				#print 'order taken^^^^^^^^^^', res
				self.customer.display._print_conversation("server", res['message'])
				obj._pyroRelease()
				self.customer.shutdown_customer()
				self.customer.display._print_info(self.customer.customer_name+ " received his order")
			return

		elif message['messageType'] == 'BBYE':
			return
		
		#sleep(int((randint(1,3)/self.speed)))
		#json_data = json.loads(response_message)
		#print "!!!!!!!!!>>>>>>>>>>>",response_message
		self.customer.speak(respond_to, response_message)
		

	def run(self):
		print 'worker thread running'
		while self.forever or self.customer.request_queue.qsize() > 0:
			try:
				message = self.customer.request_queue.get(timeout=2)
				self.process_message(message)
				self.customer.request_queue.task_done()
			except Queue.Empty, e:
				#sleep(int(2/self.speed))
				pass
			
	def shutdown(self):
		#print 'shutting down worker'
		self.forever = False
