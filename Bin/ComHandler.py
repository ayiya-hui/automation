from socket import *
import httplib2, ssl
import os, time
import callRest
import logging


class comHandler:
	def __init__(self, dataCollector, appServer, user, password):
		self.dataCollector=dataCollector
		self.appServer=appServer
		self.user=user
		self.password=password

	def udpClient(self, port=False):
		destPort=514
		if port:
			destPort=port
		self.sock=socket(AF_INET, SOCK_DGRAM)
		self.sock.connect((self.dataCollector, destPort))

	def sendEvent(self, msg):
		self.sock.sendall(msg)

	def udpClientClose(self):
		self.sock.close()

	def getEvent(self, method, urlString=False, xml=False):
		self.xml=callRest.SendQuery(self.appServer, self.user, self.password, method, inputString=urlString, inputXML=xml)
		for item in self.xml:
			logging.debug(item)

	def setSecure(self):
		self.appServer+=':443'
