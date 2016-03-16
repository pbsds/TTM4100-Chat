# -*- coding: utf-8 -*-
import SocketServer
import json
import time
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

users = {}#[userName] = ClientHandler
history =[]

class ClientHandler(SocketServer.BaseRequestHandler):
	"""
	This is the ClientHandler class. Everytime a new client connects to the
	server, a new ClientHandler object will be created. This class represents
	only connected clients, and not the server itself. If you want to write
	logic for the server, you must write it outside this class
	"""
	
	help_text = """login <username> sends a request to login to the server. The content is a string with the username.
logout sends a request to log out and disconnect from the server. The content is None.
msg <message> sends a message to the server that should be broadcasted to all connected clients. Thecontent is a string with the message.
names should send a request to list all the usernames currently connected to the server. """
	
	def handle(self):
		"""
		This method handles the connection between a client and the server.
		"""
		self.ip = self.client_address[0]
		self.port = self.client_address[1]
		self.connection = self.request
		
		userName = None
		login = False
		
		print self.ip, "connected."
		
		#Loop that listens for messages from the client
		while True:
			try:
				received_string = self.connection.recv(4096)
			except:
				print "Lost the connection to", userName or self.ip
				if userName:
					del users[userName]
				return
			recv_dict = json.loads(received_string) #Dette er en dictionary
			
			content = None
			timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
			sender = "server"
			response = "Info"
			
			if recv_dict['request'] == 'help':
				#send tilbake en liste over kommandoer
				content = self.help_text
				print userName if userName else self.ip, "requested help"
			elif login:
				if recv_dict['request'] == 'logout':
					print userName, "logged out"
					content="Logout successful"
					login = False #logg ut brukeren
					del users[userName]
					userName = None
					self.connection.close()
					break
				elif recv_dict['request'] == 'msg':
					content = recv_dict['content']
					print userName + ":", content
					sender = userName
					response = "Message"
					
					#sends to other users aswell:
					for user in users.keys():
						if user <> userName:
							try:
								users[user].connection.send(json.dumps({'timestamp': timestamp, 'sender': sender, 'response': response.lower(), 'content': content}))
								#send denne til alle brukerene med timestamp, sender, response, content
							except:
								pass
					
					#add message to history:
					history.append((timestamp, sender, content))#make it more threadsafe? nah
				elif recv_dict['request'] == 'names':
					content = ", ".join(users.keys())
					#send tilbake en liste med brukere
				else:#error
					response = "Error"
					content = "Invalid request"
			else:#not logged in:
				if recv_dict['request'] == 'login':
					chkUserName = recv_dict['content']
					if chkUserName.isalnum() and chkUserName not in users.keys():#består av bokstaver A-Z, a-z og/eller tall 0-9
						userName = chkUserName
						login = True
						users[userName] = self
						
						#Send tilbake et json objekt med timestamp, sender, response (login successfull) og content
						self.connection.send(json.dumps({'timestamp': timestamp, 'sender': sender, 'response': "Info".lower(), 'content': "Login successful"}))
						
						#send history:
						response = "History"
						content = []
						for date, sendie, message in history:
							content.append({'timestamp': date, 'sender': sendie, 'response': "Message", 'content': message})
						
						print userName, "logged in"
						
					else:#send en errormelding fordi man ikke er logget inn
						response = "Error"
						content = "Illegal request or username already taken."
						print self.ip, "failed logging in with the username", chkUserName
				else:#error
					response = "Error"
					content = "Invalid request (you're not logged in)"
			
			#send responce to user:
			dict = {'timestamp': timestamp, 'sender': sender, 'response': response.lower(), 'content': content};
			self.connection.send(json.dumps(dict))
		
		#cleanup:
		if userName:
			del users[userName]
		print self.ip, "disconnected."
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	"""
	This class is present so that each client connected will be ran as a own
	thread. In that way, all clients will be served by the server.

	No alterations are necessary
	"""
	allow_reuse_address = True

if __name__ == "__main__":
	"""
	This is the main method and is executed when you type "python Server.py"
	in your terminal.

	No alterations are necessary
	"""
	HOST, PORT = 'localhost', 9998
	print 'Server running...'

	# Set up and initiate the TCP server
	server = ThreadedTCPServer((HOST, PORT), ClientHandler)
	server.serve_forever()
