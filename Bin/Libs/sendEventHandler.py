from udpSendHandler import udpSendHandler
from snmpHandler import snmpHandler
from classUtility import getType

DEFAULT_COMM='public'
DEFAULT_VER='2c'

class sendEventHandler:
    """This class will handle Accelops sending events utility.
    It takes one of types (syslog, netflow, snamptrap) to send out events."""
    def __init__(self, type, dataCollector):
        self.type=type
        self.snmp=False
        if type=='snmptrap':
            self.eventHandler=snmpHandler(dataCollector)
            self.snmp=True
        elif type in ['syslog','netflow']:
            self.eventHandler=udpSendHandler(dataCollector)
        else:
            print 'sendEvent type %s is not supported. Default to syslog.' % type
            self.type='syslog'
            self.eventHandler=udpSendHandler(dataCollector)

    def sendoutEvent(self, rawData, count=False, community=None, version=None, utf_8=True):
        """This method will take raw data, with counts to send out data."""
        myCount=1
        myComm=DEFAULT_COMM
        myVer=DEFAULT_VER
        if count:
            myCount=int(count)
        if community:
            myComm=community
        if version:
            myVer=version
        for i in range(myCount):
            if getType(rawData)=='list':
                for msg in rawData:
                    if self.snmp:
                        self.eventHandler.sendEvent(msg, self.type, myComm, myVer, utf_8)
                    else:
                        self.eventHandler.sendEvent(msg, self.type, utf_8)
            else:
                if self.snmp:
                    self.eventHandler.sendEvent(rawData, self.type, myComm, myVer, utf_8)
                else:
                    self.eventHandler.sendEvent(rawData, self.type, utf_8)

    def close(self):
        self.eventHandler.close()






