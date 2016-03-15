# -*- coding: utf-8 -*-
import SocketServer
import json
import time
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
from curses.ascii import isalnum

users = {}#[userName] = ClientHandler
history =[]

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        userName = None
        login = False
        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            recv_dict = json.loads(received_string) #Dette er en dictionary
            timestamp = time.strftime("%Y-%m/%d %H:%M:%S")
            sender = "server"
            response = "info"
            # TODO: Add handling of received payload from client
            if recv_dict['request'] == 'help':
                content  = """login <username> sends a request to login to the server. The content is a string      with the username.
logout sends a request to log out and disconnect from the server. The content is None.
msg <message> sends a message to the server that should be broadcasted to all connected clients. Thecontent is a string with the message.
names should send a request to list all the usernames currently connected to the server. """
               
            #send tilbake en liste over kommandoer
            elif login = True
                if recv_dict['request'] == 'logout':
                    content="Logout successful"
                    login = False #logg ut brukeren
                    del users[userName]
                    server_close()
                elif recv_dict['request'] == 'msg':
                    content = recv_dict['content']
                    sender = userName
                    resonse = "message"
                    for user in users.keys():
                        if user <> userName:
                            users[user].connection.send(json.dumps({'timestamp': timestamp, 'sender': sender, 'response': response, 'content': content}))
                    
                    history.append(content)
                    
                #send denne til alle brukerene med timestamp, sender, response, content
                elif recv_dict['request'] == 'names':
                    content = ", ".join(users.keys())
                #send tilbake en liste med brukere
                else #error
                    response = "error"
                    content = "Invalid request"
            else
                if recv_dict['request'] == 'login':
                    chkUserName = recv_dict['content']
                    if (isalnum(chkUserName) == True  and chkUserName not in users.keys():) #består av bokstarver A-Z, a-z og/eller tall 0-9
                        userName = chkUserName
                        login = True
                        users[userName] = self
                    #Send tilbake et json objekt med timestamp, sender, response (login successfull) og content
                    content = "Login successful"
                else #send en errormelding fordi man ikke er logga inn
                    response = "error"
                    content = "Invalid request or user name already taken."
            dict = {'timestamp': timestamp, 'sender': sender, 'response': response, 'content': content};
                    return json.dumps(dict)
            
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
