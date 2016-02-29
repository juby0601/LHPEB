# -*- coding: utf-8 -*-
from threading import Thread
import json

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, connection):
        self.connection = connection

    def run(self):
        while True:
			try:	
				data = self.connection.recv(4096)
			except:
				print 'Connection lost'
				break
			jsonObject = json.loads(data)
			print jsonObject['timestamp']
			print jsonObject['sender']
			print jsonObject['response']
			print jsonObject['content']
