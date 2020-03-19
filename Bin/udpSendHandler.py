from socket import *
import GenerateNetFlowData
import randomGen

SYSLOG_PORT=514
NETFLOW_PORT=2055

class udpSendHandler:
	def __init__(self, dataCollector):
		self.dataCollector=dataCollector

	def sendEvent(self, msg, type):
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
		self.sock.sendall(msg)

	def close(self):
		self.sock.close()



