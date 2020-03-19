from udpSendHandler import udpSendHandler
from snmpHandler import snmpHandler
from classUtility import getType

class demoSendEvent:
    def __init__(self, dataCollector):
        self.dataCollector=dataCollector
        self.self.sock=socket(AF_INET, SOCK_DGRAM)
        self.sock.connect((self.dataCollector, 514))

    def sendEvent(self, rawData):
        self.sock.sendall(msg)

if __name__=='__main__':
    import sys
    dataCollector=sys.argv[1]
    fileName=sys.argv[2]
    myFile=open(fileName, 'r')
    msgs=myFile.readlines()
    myFile.close()
    type=sys.argv[3]
    sendoutEvent(dataCollector, msgs, type)
    print 'Done'
