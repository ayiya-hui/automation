from Libs.udpSendHandler import udpSendHandler
from Libs.snmpHandler import snmpHandler
from Util.classUtility import getType
import time

DEFAULT_COMM='public'
DEFAULT_VER='2c'

class sendEventHandler:
    def __init__(self, type, dataCollector):
        self.type=type
        self.snmp=False
        if type=='snmptrap':
            self.eventHandler=snmpHandler(dataCollector)
            self.snmp=True
        elif type in ['syslog','netflow']:
            self.eventHandler=udpSendHandler(dataCollector)

    def sendoutEvent(self, rawData, delay=0, count=False, community=None, version=None):
        myContinue=False
        myDelay=0
        myCount=1
        myComm=DEFAULT_COMM
        myVer=DEFAULT_VER
        if delay:
            myDelay=delay
        if count:
            if count=='continue':
                myContinue=True
            else:
                myCount=int(count)
        if community:
            myComm=community
        if version:
            myVer=version
        keepSend=True
        while keepSend:
            for i in range(myCount):
                if getType(rawData)=='list':
                    for raw in rawData:
                        msg=raw.strip()
                        if self.snmp:
                            self.eventHandler.sendEvent(msg, self.type, myComm, myVer)
                        else:
                            print msg
                            self.eventHandler.sendEvent(msg, self.type)
                        time.sleep(myDelay)
                else:
                    f_msg=rawData.strip()
                    if self.snmp:
                        self.eventHandler.sendEvent(f_msg, self.type, myComm, myVer)
                    else:
                        self.eventHandler.sendEvent(f_msg, self.type)
            if not myContinue:
                keepSend=False
        self.eventHandler.close()

if __name__=='__main__':
#    print "Usage: python sendEvent.py 10.1.2.111 1.txt syslog"
    import sys, optparse, codecs
    usage="usage: %prog dataCollector dataFile option [syslog|netflow|snmptrap] [Options]"
    parser=optparse.OptionParser(usage=usage)
    parser.add_option("-i", "--interval", dest="interval", metavar="INVERVAL", help="seding messages with inverval")
    parser.add_option("-n", "--number", dest="count", metavar="COUNT", help="sending multiple messages for incidents")
    parser.add_option("-c", "--community", dest="community", metavar="SNMP Community", help="SNMP community name, default as public")
    parser.add_option("-v", "--version", dest="version", metavar="SNMP Version", help="SNMP version in 1, 2c, 3. default as 2c")
    (opts, args)=parser.parse_args()
    dataCollector=args[0]
    filePath=args[1]
    lines=codecs.open(filePath, encoding='utf-8')
    msg=[]
    for line in lines:
        msg.append(line.strip())
    option=args[2]
    interval=0
    count=''
    ver=''
    comm=''
    if opts.interval:
        interval=int(opts.interval)
    if opts.count:
        count=opts.count
    if opts.version:
        ver=opts.version
    if opts.community:
        comm=opts.community
    myEvent=sendEventHandler(option, dataCollector)
    myEvent.sendoutEvent(msg, delay=interval, count=count, version=ver, community=comm)

    print 'Done'





