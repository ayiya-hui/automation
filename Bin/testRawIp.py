from Libs.rawUdpSendHandler import rawUdpSendHandler
import Libs.GenerateRawIPData as generateRawIp
import os, sys

def testRawIp(server, dataPort, filename):
    myUdp=rawUdpSendHandler(server, dataPort)
    if not os.path.exists(filename):
        print 'No such file %s. Exit' % filename
        sys.exit()
    myR=open(filename)
    msg=myR.read().strip()
    print 'udp data length: %i' % len(msg)
    myR.close()
    packets=generateRawIp.getRawIpPacket(msg, '1.1.1.1', server, dataPort)
    myUdp.sendoutEvent(packets)

if __name__=='__main__':
    server='192.168.20.218'
    dataPort=514
    filename='myRaw.txt'
    testRawIp(server, dataPort, filename)
    print 'task done'
