from socket import *
import Util.randomGen as randomGen

class rawUdpSendHandler:
	"""This class will create UDP raw socket to send events."""
	def __init__(self, dataCollector, destPort):
		self.dataCollector=dataCollector
		self.destPort=destPort
		self.sock=socket(AF_INET, SOCK_RAW, IPPROTO_RAW)
		self.sock.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
		try:
			self.sock.connect((self.dataCollector, self.destPort))
		except error:
			print 'Cannot open socket to %s' % self.dataCollector
			exit()

	def sendoutEvent(self, packet, utf_8=False):
		"""This method will send a raw UDP packet."""
		for chunk in packet:
			self.sock.sendall(chunk)

	def close(self):
		"""This method will close the raw socket."""
		self.sock.close()



