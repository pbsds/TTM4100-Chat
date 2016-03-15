# -*- coding: utf-8 -*-
import SocketServer
import json
"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
from curses.ascii import isalnum

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
        
        login = False
        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            recv_dict = json.loads(received_string) #Dette er en dictionary
            
            # TODO: Add handling of received payload from client
            if recv_dict['request'] == 'help':
            #send tilbake en liste over kommandoer
            elif login = True
                if recv_dict['request'] == 'logout':
                    #send logout successfull eller noe
                    login = False #logg ut brukeren
                    #server_close();
                if recv_dict['request'] == 'msg':
                    message = recv_dict['content']
                #send denne til alle brukerene med timestamp, sender, response, content
                    if recv_dict['request'] == 'names':
                #send tilbake en liste med brukere
            else
                if recv_dict['request'] == 'login':
                    chkUserName = recv_dict['content']
                    if isalnum(chkUserName) = True #består av bokstarver A-Z, a-z og/eller tall 0-9
                        userName = chkUserName
                        login = True
                    #Send tilbake et json objekt med timestamp, sender, response (login successfull) og content
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
