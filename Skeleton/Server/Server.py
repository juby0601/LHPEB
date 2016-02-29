# -*- coding: utf-8 -*-
from threading import Thread, Lock
import SocketServer
from socket import *
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

connections = []



class ClientHandler(Thread):
	"""
	This is the ClientHandler class. Everytime a new client connects to the
	server, a new ClientHandler object will be created. This class represents
	only connected clients, and not the server itself. If you want to write
	logic for the server, you must write it outside this class
	"""
	def __init__(self, connection):
		super(ClientHandler, self).__init__()
		self.connection = connection
	
	def run(self):
		self.userName = ''
		self.help = 'login <username> - log in with the given username\nlogout - log out\nmsg <message> - send message\nnames - list users in chat\nhelp - view help text'
		while True:
			try:
				receivedString = self.connection.recv(4096)
			except:
				print 'Connection lost'
				userNames.pop(userNames.index(self.userName))
				connections.remove(self.connection)
				break
			# TODO: Add handling of received payload from client
			msgTimestamp = time.ctime()
			jsonParser = json.loads(receivedString)
			clientRequest = jsonParser['request']
			if clientRequest == 'login':
				if jsonParser['content'] in userNames:
					jsonSender = json.dumps({'timestamp': msgTimestamp, 'response': 'Error', 'content': 'Username already exists'}, indent=4)
					self.connection.send(jsonSender)
				else:
					validMessage = 1
					for c in jsonParser['content']:
						if ord(c) > 122 or ord(c) < 48:
							jsonSender = json.dumps({'timestamp': msgTimestamp, 'response': 'Error', 'content': 'Invalid username'}, indent=4)
							self.connection.send(jsonSender)
							validMessage = 0
							break
					if validMessage == 1:		
						jsonSender = json.dumps({'timestamp': msgTimestamp, 'sender':jsonParser['content'] ,'response': 'login', 'content': 'Succesfully logged in'}, indent=4)
						self.connection.send(jsonSender)
						userNames.append(jsonParser['content'])
						self.userName = jsonParser['content']

				history.append(jsonSender)
			elif clientRequest == 'logout':
				if self.userName in userNames:
					jsonSender = json.dumps({'timestamp': msgTimestamp,'response': 'logout', 'content': 'Succesfully logged out'}, indent=4)
					self.connection.send(jsonSender);
					history.append(jsonSender)
					userNames.pop(userNames.index(self.userName))
					self.connection.close()
					connections.remove(self.connection)
					break
			elif clientRequest == 'msg':
				if(self.userName not in userNames):
					jsonSender = json.dumps({'timestamp': msgTimestamp, 'response': 'Error', 'content': 'Not logged in'}, indent=4)
				else:
					#TODO: counter should obviously be an int, but the logic to find it might be hard
					jsonSender = json.dumps({'timestamp': msgTimestamp, 'sender':self.userName, 'response': 'Message', 'content': jsonParser['content']}, indent=4)
					for connection in connections:
						self.connection.send(jsonSender)
				history.append(jsonSender)
			elif clientRequest == 'names':
				if self.userName in userNames:
					allNames = "\n".join(userNames)
					jsonSender = json.dumps({'timestamp': msgTimestamp ,'response': 'names', 'content': allNames}, indent=4)
					self.connection.send(jsonSender)
					history.append(jsonSender)
			elif clientRequest == 'help':
				jsonSender = json.dumps({'timestamp': msgTimestamp ,'response': 'help', 'content': self.help}, indent=4)
				self.connection.send(jsonSender)
				history.append(jsonSender)
		print 'LOL'	

if __name__ == "__main__":
	"""
	This is the main method and is executed when you type "python Server.py"
	in your terminal.

	No alterations are necessary
	"""
	HOST, PORT = 'localhost', 9998
	print 'Server running...'
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',PORT))
	serverSocket.listen(100)
	while True:
		connection, addr = serverSocket.accept()
		connections.append(connection)
		ClientHandler(connection).start()
