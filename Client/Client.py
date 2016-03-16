#/usr/bin/python2
# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import sys, json
from Queue import Queue
from GetChar import GetCharFiltered as GetChar

#The client handles user input and message output asyncronously, which makes for a nices interface.

class Client():
	"""
	This is the chat client class
	"""
	terminal_width = 80#windows width, maybe implement a check for unix terminals? nah!
	
	help_text="""== Using the client: ==
If the prompt says "Username: ", you've yet to log in.
Type your wanted username and wait for the server to verify.
The prompt with then change to "msg: ", which means you can start
chatting away.

== Commands: ==
The client supports a few commands:
/help: displays this help text
/logout or /exit: logs out from the server and disconnects
/names or /who: Queries the server for a list of who is present on the server.
/shelp: Queries the server for its help text.
"""
	
	def __init__(self, host, server_port):
		"""
		This method is run when creating a new Client object
		"""
		self.host = (host, server_port)
		
		# Set up the socket connection to the server
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# Set up the incoming messages queue:
		self.queue = Queue()
		self.prompt = ["username: ", []]
		
		#ech, spis meg
		self.MessageParser = MessageParser()
		self.MessageReceiver = MessageReceiver(self.connection, self)
		
		self.run()
	def run(self):
		# Initiate the connection to the server
		self.MessageReceiver.start()
		
		mode = 0#{0: push username, 1: send messages}
		
		self.print_message("Welome to our totally awesome chat client!")
		self.print_message("If you need help with using the client, type /help")
		self.print_message("If you need help with using the server, type /shelp")
		self.print_message("Connecting to %s:%s..." % self.host)
		self.print_message("")
		
		self.prompt[0] = "Username: "
		self.print_message("Please select a username to go by:")
		
		
		while 1:
			out = self.handle_input()
			if out:
				if out[0] == "/":#commands:
					command = out[1:].split(" ")[0]
					if command  == "help":
						self.print_message(self.help_text)
					elif command == "logout" and mode==1:
						self.send_logout()
						self.disconnect()
					elif command == "exit":
						self.send_logout()
					elif command == "names" and mode==1:
						self.send_names()
					elif command == "who" and mode==1:
						self.send_names()
					elif command == "shelp":
						self.send_help()
					else:
						self.print_message("Unknown command \"/%s\"" % command)
						
				elif mode == 0:#username
					self.send_login(out)
					self.print_message("logging in as %s..." % out)
				else:#message
					self.send_msg(out)
					pass#server should echo the message
				
					
			if not self.queue.empty():
				data = self.queue.get()
				response, timestamp, sender, content = self.MessageParser.parse(data)
				self.queue.task_done()#neccesary? nah...
				
				if response.lower() in ("error", "info"):
					if response.lower() == "info" and "success" in content.lower():
						mode = 1
						self.prompt[0] = "msg: "
						#self.refresh_prompt()#is handeled in the print below instead
					self.print_message("%s: %s" % (response, content))
				elif response.lower() == "message":
					self.print_message("%s: %s" % (sender, content))
				elif response.lower() == "history":
					for i in content:
						if i["response"].lower() == "message":
							self.print_message("%s: %s" % (i["sender"], i["content"]))
						
	#run() helpers:
	def handle_input(self):#call each iteration, handles user input, returns a string if enter is pressed:
		char = GetChar()
		
		if char:
			if char == "\n":
				ret = "".join(self.prompt[1])
				self.prompt[1] = []
				self.refresh_prompt()
				return ret
			elif char == "\b":
				if self.prompt[1]:
					self.prompt[1].pop(-1)
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
		sys.stdout.write(self.prompt[0] + ("".join(self.prompt[1]))[-self.terminal_width+1+len(self.prompt[0]):])
	def send_login(self, username):
		out = {"request":"login"}
		out["content"] = username
		self.send_payload(json.dumps(out))
	def send_msg(self, message):
		out = {"request":"msg"}
		out["content"] = message
		self.send_payload(json.dumps(out))
	def send_logout(self):#todo: also handle disconnecting
		out = {"request":"logout"}
		out["content"] = None
		self.send_payload(json.dumps(out))
	def send_names(self):#ask for a list of users
		out = {"request":"names"}
		out["content"] = None
		self.send_payload(json.dumps(out))
	def send_help(self):#ask server for help
		out = {"request":"help"}
		out["content"] = None
		self.send_payload(json.dumps(out))
	#events:
	def disconnect(self):
		self.connection.close()
		sys.exit(0)
	def receive_message(self, message):#works with threads
		self.queue.put(message, True, None)#2threadingsafe4u
	def send_payload(self, data):
		self.connection.send(data)#2ez4u
		


if __name__ == '__main__':
	"""
	This is the main method and is executed when you type "python Client.py"
	in your terminal.

	No alterations are necessary
	"""
	client = Client('localhost', 9998)
