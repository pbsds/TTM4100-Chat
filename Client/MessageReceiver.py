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
		#i assume all json start with { and end with }
		buffer = ""
		self.connection.connect((self.client.host[0], self.client.host[1]))
		
		
		while 1:
			#assumes fragmentation:
			buffer += self.connection.recv(1024)
			
			#check if buffer contains a finished json:
			message = None
			deep = 0
			for e, i in enumerate(buffer):
				if i == "{":
					deep += 1
				elif i == "}":
					deep -= 1
					if deep == 0:
						message = buffer[:e+1]
						buffer = buffer[e+1:]
						break
					if deep < 0:
						print "invalid json"
						sys.exit(1)
			if message:
				self.client.receive_message(message)
			
