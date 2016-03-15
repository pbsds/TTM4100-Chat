# -*- coding: utf-8 -*-
from threading import Thread
import json

class MessageReceiver(Thread):
	"""
	This is the message receiver class. The class inherits Thread, something that
	is necessary to make the MessageReceiver start a new thread, and it allows
	the chat client to both send and receive messages at the same time
	"""

	def __init__(self, connection, client):
		"""
		This method is executed when creating a new MessageReceiver object
		"""
		Thread.__init__(self)
		
		# Flag to run thread as a deamon
		self.daemon = True

		# TODO: Finish initialization of MessageReceiver
		
		self.connection = connection
		self.client = client
		#self.run() is called by the thread
		
		
	def run(self):
		# TODO: Make MessageReceiver receive and handle payloads
		
		
		while 1:
			#assume no fragmentation? yes, why not?
			payload = self.connection.recv(1024)
			self.client.receive_message(payload)
			
