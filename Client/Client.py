#/usr/bin/python2
# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import select, sys
from Queue import Queue

#The client handles user input and messge output asymetrically, which makes for a nices interface.

#reads a single character from stdin, if any
def GetChar():
	if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
		return sys.stdin.read(1)
	return ""


class Client:
	"""
	This is the chat client class
	"""
	terminal_width = 80#windows width
	
	def __init__(self, host, server_port):
		"""
		This method is run when creating a new Client object
		"""
		
		# Set up the socket connection to the server
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# Set up the incoming messages queue:
		self.queue = Queue()
		self.prompt = ["username: ", []]
		
		self.run()
	def run(self):
		# Initiate the connection to the server
		self.connection.connect((self.host, self.server_port))
		
		mode = 0#{0: push username, 1: send messages}
		
		self.print_message("Welome to our totally awesome chat client!")
		self.print_message("If you need help with using some commands, type /help")
		self.print_message("Connecting to %s:%s" % ())
		self.print_message("")
		self.print_message("Please select as userhandle to go by:")
		
		while 1:
			out = handle_input()
			if out:
				pass
			
			if not self.queue.empty():
				data = self.queue.get()
				message = MessageParser.parse(date)
				self.queue.task_done()
				
				if message[0] in ("Error", "Info"):
					if message[0] == "Info" and message[1] == "Login successful":
						mode = 1
						self.prompt[0] == "msg: "
						#self.refresh_prompt()#is handeled below instead
					self.print_message("%s: %s" % (message[0], message[1]))
				elif message[0] == "Message":
					#todo after message reciever is finished
					User = "<user>"
					msg = "<msg>"
					self.print_message("%s: %s" % (user, msg))
				elif message[0] == "History":
					pass
	#run() helpers:
	def handle_input(self, string):#call each iteration, handles user input, returns a string if enter is pressed:
		char = GetChar()
		
		if char:
			if char == "\n":
				ret = "".join(self.prompt[1])
				self.prompt[1] = []
				return ret
			else:
				self.prompt[1].append(char)
			self.refresh_prompt()
	def print_message(self, string):
		#clear
		sys.stdout.write("\r%s\r" % (" "*(self.terminal_width-1)))
		
		#print
		print string
		
		#recreate prompt:
		self.refresh_prompt(clear=False)
	def refresh_prompt(self, clear=True):
		#clear
		if clear:
			sys.stdout.write("\r%s\r" % (" "*(self.terminal_width-1)))
		
		#recreate prompt:
		sys.stdout.write(self.prompt[0] + ("".join(self.prompt[1]))[-terminal_width+1+len(self.prompt[0]):])
	#events:
	def disconnect(self):
		# TODO: Handle disconnection
		pass
		
	def receive_message(self, message):#works with threads
		self.queue.put(message, True, None)
	def send_payload(self, data):
		# TODO: Handle sending of a payload
		pass


if __name__ == '__main__':
	"""
	This is the main method and is executed when you type "python Client.py"
	in your terminal.

	No alterations are necessary
	"""
	client = Client('localhost', 9998)
