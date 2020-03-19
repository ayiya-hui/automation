import Libs.GenerateRawIPData as GenerateRawIPData
import Libs.rawUdpSendHandler as rawUdpSendHandler
import os

SYSLOG_PORT=514

def sendRawPacket(srcAddr, destAddr, file):
    """This program will send a raw UDP packet with a fake source IP address
    inside the IP packet. Due to WinSock2 restriction, this function will not
    work in Windows system.
    sendRawPacket.py fake_src_ip dataCollector dataFile
    """
    myFile=open(file)
    myData=myFile.readlines()
    myFile.close()
    myUdp=rawUdpSendHandler.rawUdpSendHandler(destAddr, SYSLOG_PORT)
    for data in myData:
        myPacket=GenerateRawIPData.getRawIpPacket(data.strip(), srcAddr, destAddr, SYSLOG_PORT)
        myUdp.sendEvent(myPacket)

    myUdp.close()

if __name__=='__main__':
    import sys
    """if os.name=='nt':
        print sendRawPacket.__doc__
        print 'Not support on Windows system'
        sys.exit()"""
    if len(sys.argv)!=4:
        print sendRawPacket.__doc__
        sys.exit()
    srcAddr=sys.argv[1]
    destAddr=sys.argv[2]
    file=sys.argv[3]
    if not os.path.exists(file):
        print sendRawPacket.__doc__
        print 'data file is not exist.'
        sys.exit()

    sendRawPacket(srcAddr, destAddr, file)


