from socket import *
import os, random, time, datetime

def demoTrafficSender():
    #get rawData
    fileList=os.listdir('/root/demo/perf')
    allData=[]
    for file in fileList:
        fileHandle=open('rawData', 'r')
        rawData=fileHandle.readlines()
        fileHandle.close()
        allData.append(rawData)

    #get dataCollector
    collector=gethostbyname(gethostname())

    #setup udp client
    udpClient=socket(AF_INET, SOCK_DGRAM)
    udpClient.connect((collector, 514))

    while 1:
        for line in allData:
            udpClient.sendall(line.encode())

if __name__=='__main__':
    # do double-fork magic
    try:
        pid=os.fork()
        if pid>0:
            sys.exit(0)    #exit first parent
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    #decouple from parent enviornment
    os.setsid()
    os.umask(0)

    #second fork
    try:
        pid=os.fork()
        if pid>0:    #exit out second parent, print out eventual PID
            print "Daemon PID %d" % pid
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    trafficSender(dataCollector, ipbase, speed, totalDevices)






