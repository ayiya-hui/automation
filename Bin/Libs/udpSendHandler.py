from socket import *
import GenerateNetFlowData
import Util.randomGen as randomGen

SYSLOG_PORT=514
NETFLOW_PORT=2055

class udpSendHandler:
	"""This class will open a UDP socket with either Syslog(port 514) or Netflow(port 2055) and send a message."""
	def __init__(self, dataCollector):
		self.dataCollector=dataCollector

	def sendEvent(self, msg, type, utf8=True):
		"""This method will take a message and a type (Syslog or Netflow) to send out the packets.
		Message can contain '$randomNum' or '$randomIP' that will be replace by random generated
		numbers or IP addresses."""
		self.sock=socket(AF_INET, SOCK_DGRAM)
		if type=='syslog':
			port=SYSLOG_PORT
			if '$randomNum' in msg:
				msg=msg.replace('$randomNum', randomGen.getRandomNum(100,900))
			if '$randomIP' in msg:
				msg=msg.replace('$randomIP', randomGen.getRandomIPAddr())
		elif type=='netflow':
			port=NETFLOW_PORT
			msg=GenerateNetFlowData.getNetFlowPacket(msg)
		try:
			self.sock.connect((self.dataCollector, port))
		except error:
			print 'Cannot open socket to %s' % self.dataCollector
			exit()
		if utf8:
			msg=msg.encode('utf-8')
		self.sock.sendall(msg)

	def close(self):
		"""This method will close the socket."""
		if self.sock:
			self.sock.close()



