# -*- coding: utf-8 -*-
import SocketServer
import json
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
port = "12000"
messageQueue = []	
history = []
userNames = []
counter = 0
self.lock = threading.Lock()

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    def handle(self):
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
		self.userName = ''
        # Loop that listens for messages from the client

        #Local

        while True:
            recvDict = received_string.dumps(dict)
			receivedString = self.connection.recv(4096)
            # TODO: Add handling of received payload from client
			msgTimestamp = time.ctime()
			jsonParser = json.loads(receivedString)
			clientRequest = jsonParser['request']
			if clientRequest == 'login':
				if jsonParser['content'] in userNames
					self.connection.send(json.dumps({'timestamp': msgTimestamp, 'reponse': 'Error', 'content': 'Username already exists'}, indent=4));
				else
					
			elif clientRequest == 'logout':
				
			elif clientRequest == 'msg':
				
			elif clientRequest == 'names':
				
			elif clientRequest == 'help':

            

            """
            Locic for queuing the message sending. Needs a global counter and
            a local threadspecific counter
            """
            #local 


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
