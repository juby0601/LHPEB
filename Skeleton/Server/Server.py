# -*- coding: utf-8 -*-
from threading import Thread, Lock
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
		self.help = 'login <username> - log in with the given username\nlogout - log out\nmsg <message> - send message\nnames - list users in chat\nhelp - view help text'
		while True:
			recvDict = received_string.dumps(dict)
			receivedString = self.connection.recv(4096)
			# TODO: Add handling of received payload from client
			msgTimestamp = time.ctime()
			jsonParser = json.loads(receivedString)
			clientRequest = jsonParser['request']
			if clientRequest == 'login':
				if jsonParser['content'] in userNames:
					jsonSender = json.dumps({'timestamp': msgTimestamp, 'reponse': 'Error', 'content': 'Username already exists'}, indent=4)
					self.connection.send(jsonSender)
				else:
					validMessage = 1
					for c in jsonParser['content']:
						if ord(c) > 122 and ord(c) < 65:
							jsonSender = json.dumps({'timestamp': msgTimestamp, 'reponse': 'Error', 'content': 'Invalid username'}, indent=4)
							self.connection.send(jsonSender)
							validMessage = 0
							break
					if validMessage == 1:		
						jsonSender = json.dumps({'timestamp': msgTimestamp, 'Sender':jsonParser['content'] ,'reponse': 'login', 'content': 'Succesfully logged in'}, indent=4)
						self.connection.send(jsonSender)
						userNames.append(jsonParser['content'])

				history.append(jsonSender)
			elif clientRequest == 'logout':
				if self.userName in userNames:
					jsonSender = json.dumps({'timestamp': msgTimestamp,'reponse': 'logout', 'content': 'Succesfully logged out'}, indent=4)
					self.connection.send(jsonSender);
					history.append(jsonSender)
					userNames.pop(userNames.index(self.userName))
					self.connection.close()
					break
			elif clientRequest == 'msg':
				#TODO: If client not logged in, send back: "error: not logged in"

				#TODO: counter should obviously be an int, but the logic to find it might be hard
				counter = "Nr of active connections to clients" 
				jsonMessage = json.dump({'timestamp': msgTimestamp, 'content': jsonParser['content']})
				messageQueue.append([jsonParser, counter])
			elif clientRequest == 'names':
				if self.userName in userNames:
					allNames = "\n".join(userNames)
					jsonSender = json.dumps({'timestamp': msgTimestamp ,'reponse': 'names', 'content': allNames}, indent=4)
					self.connection.send(jsonSender)
					history.append[jsonSender]
			elif clientRequest == 'help':
				jsonSender = json.dumps({'timestamp': msgTimestamp ,'reponse': 'help', 'content': self.help}, indent=4)
				self.connection.send(jsonSender)
				history.append[jsonSender]
			

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
	print 'Server running...'
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
