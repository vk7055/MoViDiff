"""

	This program implements QoS Differentiation between
	different services. It intercepts the network packets
	and uses svm_decision method of svm.py module to determine
	the service to which the packet belongs. Here we are
	using a dummy svm module that determines the belongings
	of the packets using random numbers. Packets of different 
	services are queued separately using the Producer Thread. 
	The Consumer Thread dequeues the packets from the
	queues depending upon the ratio of the service defined
	by user in the file set_ratio.txt.

"""


from netfilterqueue import NetfilterQueue
from svm import svm_decision
from ratio_parse_file import get_ratio_list_of_services
import threading
import time
import Queue


def pass_to_consumer_thread(pkt):
	"""
		pass_to_consumer_thread is the global name bound to 
		nfqueue. For every intercepted packet, this method
		gets called with packet itself as the argument.
	"""
	p.differentiate_and_enqueue(pkt)
	return


def get_maximum_sleep_time(ratio_list_of_services):
	"""
		This method computes the maximum time for which the
		Consumer thread can sleep before scanning the next
		packet for every service. It returns the list
		max_sleep_time which contains maximum sleep time for
		every service.
	"""
	max_sleep_time = []
	ratio_sum = 0
	
	i = 0
	while i < len(ratio_list_of_services):
		max_sleep_time.append(0)
		if ratio_list_of_services[i] != -1 and ratio_list_of_services[i] != 0:
			ratio_sum += ratio_list_of_services[i]
		i += 1

	i = 0
	while  i < len(ratio_list_of_services):
		if ratio_list_of_services[i] != -1 and ratio_list_of_services[i] != 0:
			fractional_ratio = ratio_list_of_services[i] / ratio_sum
			if fractional_ratio >= 0.9 and fractional_ratio <= 1:
				max_sleep_time[i] = 20
			elif fractional_ratio >= 0.75 and fractional_ratio < 0.9:
				max_sleep_time[i] = 15
			elif fractional_ratio >= 0.5 and fractional_ratio < 0.75:
				max_sleep_time[i] = 10
			elif fractional_ratio >= 0.2 and fractional_ratio < 0.5:
				max_sleep_time[i] = 5
			elif fractional_ratio >= 0 and fractional_ratio < 0.2:
				max_sleep_time[i] = 3
		i += 1

	return max_sleep_time


class ProducerThread(threading.Thread):
	"""
		Producer Thread is responsible for creating and running 
		nfqueue. It also differentiates between Skype and You 
		Tube and enqueues the packets in separate queues.
	"""

	def __init__(self, lock, target=None, name=None):
		super(ProducerThread,self).__init__()
		self.target = target
		self.name = name
		self.lock = lock
	
	def differentiate_and_enqueue(self, pkt):
		"""
			differentiate_and_enqueue method accepts network packet as 
			an argument and calls svm_decision method to determine the 
			service to which the packet belongs. If the ratio associated
			with the service is -1 (No Scheduling), the packet is accepted.
			If the ratio associated with the service is 0 (Blocking), the
			packet is dropped. Otherwise, the packet is enueued to the
			service queue depending upon the service to which it belongs. 
			Locks are acquired and released for using shared resources 
			which are in shared memory.
		"""
		q_type = svm_decision(pkt)
		self.lock.acquire()
		if ratio_list_of_services[q_type] == -1:
			pkt.accept()
		elif ratio_list_of_services[q_type] == 0:
			pkt.drop()
		else:
			print "	Putting in 	" + str(q_type)
			list_of_queues_of_services[q_type].put(pkt)
		self.lock.release()

	def run(self):
		"""
			run is the location where the producer thread p starts its
			execution. It creates an nfqueue and binds it to the global
			name pass_to_consumer_thread and queue number 5. It calls
			nfqueue.run() method which causes every intercepted 
			network packet to be passed one by one to the global 
			pass_to_consumer_thread() method
		"""
		nfqueue = NetfilterQueue()
		nfqueue.bind(5, pass_to_consumer_thread)
		try:
		    while True:
		        nfqueue.run()
		except KeyboardInterrupt:
		    print
		return


class ConsumerThread(threading.Thread):
	"""
		Consumer Thread is responsible for scheduling the 
		dequeueing and thus acceptance of the packets.
	"""

	def __init__(self, lock, target=None, name=None):
		super(ConsumerThread,self).__init__()
		self.target = target
		self.name = name
		self.lock = lock

	def run(self):
		"""
			run is the location where the consumer thread starts its 
			execution. Locks are acquired and released for using 
			shared resources which are in shared memory.
		"""
		
		maximum_sleep_time = get_maximum_sleep_time(ratio_list_of_services)
		
		while True:
		    self.lock.acquire()
		    i = 0
		    while i < len(ratio_list_of_services):
		    	if ratio_list_of_services[i] == -1 or ratio_list_of_services[i] == 0:
		    		print "			0-1	" + str(i)
		    	else:
		    		j = 0
		    		while j < ratio_list_of_services[i]:
		    			j += 1
		    			count_time = 0
		    			while list_of_queues_of_services[i].empty() and count_time < maximum_sleep_time[i]:
		    				count_time += 1
		    				self.lock.release()
		    				time.sleep(0.001)
		    				self.lock.acquire()
		    			if (not list_of_queues_of_services[i].empty()):
		    				print "								Getting from	" + str(i)
		    				extract_pkt = list_of_queues_of_services[i].get()
		    				extract_pkt.accept()
		    	i += 1

		    self.lock.release()
		return




"""
	Get ratio for all the services as a list
"""

ratio_list_of_services = get_ratio_list_of_services()

"""
	Create queues for every service
"""
list_of_queues_of_services = []

i = 0
while i < len(ratio_list_of_services):
	list_of_queues_of_services.append(Queue.Queue())
	i += 1

"""
	Create lock enabled threads
		p 	-	Producer Thread
		c 	- 	Consumer Thread
"""
lock = threading.Lock()
p = ProducerThread(lock, name='producer')
c = ConsumerThread(lock, name='consumer')

"""
	Start the Producer Thread
"""
p.start()

"""
	Wait for some time, say 1 second for some packets to get enqueued
"""
time.sleep(1)

"""
	Start the Cosumer Thread
"""
c.start()