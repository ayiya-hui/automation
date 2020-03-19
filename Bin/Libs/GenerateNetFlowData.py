from netFlowClass import *
import time, random
from Util.IPUtility import combineIP
import logging

NetFlowOption={'none':255,
               'srcIp':1,
               'srcPort':2,
               'dstIp':3,
               'dstPort':4,
               'dstIp-dstPort':5,
               'dstIp-srcPort':6,
               'srcIp-srcPort':7,
               'srcIp-dstPort':8}
NetProtocol={'icmp':1,
             'tcp':6,
             'udp':17}

def getNetFlowPacket(msg):
    """This method generates a netflow v5 packet."""
    mybuff=""
    myStack=msg.split(",")
    data={}
    for item in myStack:
        myVal=item.strip().split("=")
        data[myVal[0]]=myVal[1]

    #get option
    option=NetFlowOption[data['option']]

    #get protocol
    protocol=NetProtocol[data['protocol']]

    #prepare for ICMP, TCP and UDP
    srcPort=0
    dstPort=0
    tcpFlag=0
    packets=0
    bytes=0

    #fill in default packets and bytes if not in hash
    if 'packets' not in data.keys():
        packets=2000
    else:
        packets=int(data['packets'])

    if 'bytes' not in data.keys():
        bytes=10000
    else:
        bytes=int(data['bytes'])

    #handle icmp-type and code, and tcp flag
    if(protocol==NetProtocol['icmp']):
        typeCode=data['icmpTypeCode']
        dstPort=int(typeCode, 16)
    else:
        dstPort=int(data['dstPort'])
        srcPort=int(data['srcPort'])
        if(protocol==NetProtocol['tcp']):
            if 'tcpFlag' in data:
                tcpFlag=int(data['tcpFlag'])
            else:
                tcpFlag=0

    #get time now
    timeNow=time.time()
    timeInt=int(timeNow)
    nanoTime=int(1000*(timeNow-timeInt))

    #NetFlow version 5
    if(data['version']=="5"):
        myHeader=netflowV5Header(int(data['count']), timeInt, nanoTime)
        myRecord=""
        myRecordList=[]

        if(option==NetFlowOption['dstIp']):
            for i in range (0, int(data['count'])):
                newIp=combineIP(data['dstIp'], i)
                myRecord=netflowV5Record(data['srcIp'], newIp, data['nextHop'], srcPort, dstPort, tcpFlag, protocol, packets, bytes)
                logging.debug("Src Ip %s Dst Ip %s" % (data['srcIp'], newIp))
                myRecordList.append(myRecord)
        elif (option==NetFlowOption['dstPort']):
            for i in range (0, int(data['count'])):
                randomPort=random.randrange(1, 10000)+dstPort
                myRecord=netflowV5Record(data['srcIp'], data['dstIp'], data['nextHop'], srcPort, randomPort, tcpFlag, protocol, packets, bytes)
                logging.debug("Dst Ip %s DstPort %s" % (data['dstIp'], randomPort))
                myRecordList.append(myRecord)
        elif (option==NetFlowOption['dstIp-dstPort']):
            for i in range (0, int(data['count'])):
                randomPort=random.randrange(1, 10000)+dstPort
                newIp=combineIP(data['dstIp'], i)
                myRecord=netflowV5Record(data['srcIp'], newIp, data['nextHop'], srcPort, randomPort, tcpFlag, protocol, packets, bytes)
                logging.debug("Dst Ip %s DstPort %s",(newIp,randomPort))
                myRecordList.append(myRecord)
        elif (option==NetFlowOption['dstIp-srcPort']):
            for i in range (0, int(data['count'])):
                randomPort=random.randrange(1, 10000)+srcPort
                newIp=combineIP(data['dstIp'], i)
                myRecord=netflowV5Record(data['srcIp'], newIp, data['nextHop'], randomPort, dstPort, tcpFlag, protocol, packets, bytes)
                logging.debug("Dst Ip %s srcPort %s" % (newIp, randomPort))
                myRecordList.append(myRecord)
        elif (option==NetFlowOption['srcIp']):
            for i in range (0, int(data['count'])):
                newIp=combineIP(data['srcIp'], i)
                myRecord=netflowV5Record(newIp, data['dstIp'], data['nextHop'], srcPort, dstPort, tcpFlag, protocol, packets, bytes)
                logging.debug("Src Ip %s Dst Ip %s" % (newIp, data['dstIp']))
                myRecordList.append(myRecord)
        elif (option==NetFlowOption['srcPort']):
            for i in range(0, int(data['count'])):
                randomPort=random.randrange(1, 10000)+srcPort
                myRecord=netflowV5Record(data['srcIp'], data['dstIp'], data['nextHop'], randomPort, dstPort, tcpFlag, protocol, packets, bytes)
        elif (option==NetFlowOption['srcIp-srcPort']):
            for i in range(0, int(data['count'])):
                randomPort=random.randrange(1, 10000)+srcPort
                newIp=combineIP(data['srcIp'], i)
                myRecord=netflowV5Record(newIp, data['dstIp'], data['nextHop'], randomPort, dstPort, tcpFlag, protocol, packets, bytes)
        elif (option==NetFlowOption['srcIp-dstPort']):
            for i in range(0, int(data['count'])):
                randomPort=random.randrange(1, 10000)+srcPort
                newIp=combineIP(data['srcIp'], i)
                myRecord=netflowV5Record(newIp, data['dstIp'], data['nextHop'], srcPort, randomPort, tcpFlag, protocol, packets, bytes)
        else:
            #default
            for i in range (0, int(data['count'])):
                myRecord=netflowV5Record(data['srcIp'], data['dstIp'], data['nextHop'], srcPort, dstPort, tcpFlag, protocol, packets, bytes)
                logging.debug("Src Ip %s Dst Ip %s" % (data['srcIp'], data['dstIp']))
                myRecordList.append(myRecord)

        myPacket=netflowV5Packet(myHeader, myRecordList)
        mybuff=myPacket.Assemble()

    return  mybuff


