# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver

class Client:
	
	def __init__(self, host, serverPort):
		self.host = host
		self.serverPort = serverPort
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((self.host,self.serverPort))
		self.jsonObject = None

	def disconnect(self):
		self.connection.close()
		
	def rawInput():
		request = raw_input("Request type: ");
		content = raw_input("Content: ");
		self.jsonObject = json.dumps({'request': request, 'content': content}, indent=4)

	def receiveMessage(self):
		messageReceiver = MessageReceiver(self.connection)
		messageReceiver.start()

	def send(self):
		self.connection.send(self.jsonObject)

if __name__ == '__main__':
	client = Client('localhost', 9998)
	client.receiveMessage()
	while True:
		client.rawInput()
		client.send()
		disconnection = raw_input("Want to disconnect? if so type c ");
		if disconnection == c:
			client.disconnect()
			break