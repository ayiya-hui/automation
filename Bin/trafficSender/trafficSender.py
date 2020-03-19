#!/usr/local/bin/python

from socket import *
import os, random, time, datetime

def trafficSender(dataCollector, ipbase, speed, num=False):
    if num:
        totalDevices=int(num)
    else:
        totalDevices=100

    #get rawData
    fileHandle=open('rawData', 'r')
    rawData=fileHandle.readlines()
    fileHandle.close()

    #get dataCollector
    if dataCollector=='localhost':
        collector=gethostbyname(gethostname())
    else:
        collector=dataCollector

    #setup udp client
    udpClient=socket(AF_INET, SOCK_DGRAM)
    udpClient.connect((collector, 514))

    while 1:
        stime=datetime.datetime.now()
        for j in range(int(speed)):
            ip=ipbase+"."+str(int(random.randrange(2, totalDevices)))
            if len(rawData)==1:
                ranMsg=0
            else:
                ranMsg=int(random.randrange(0, len(rawData)-1))
            msg=rawData[ranMsg]
            msg=msg.replace("$ip", ip)
            sendMsg=msg.encode()
            udpClient.sendall(sendMsg)
        time.sleep(1.0)

        ftime=datetime.datetime.now()
        dTime=ftime-stime
        print "%s events using %s" % (speed, dTime.seconds)
        if dTime.seconds==0:
            totalTime=1
        else:
            totalTime=dTime.seconds
        print "sending speed is %s per second." % (speed)




if __name__=='__main__':
    import sys
    if len(sys.argv) not in [4, 5]:
        usage="""Usage: trafficSender.py dataCollector Ipbase speed totalDevices
                Ipbase -- first three parts of IP address
                speed -- how many events per second. Support 100, 500, 1000 and 1500 now
                (optional)totalDevices -- total numbers of devices to simulated. Default is 100. """
        print usage
        exit()

    dataCollector=sys.argv[1]
    ipbase=sys.argv[2]
    speed=sys.argv[3]
    if len(sys.argv)==5:
        totalDevices=sys.argv[4]
    else:
        totalDevices=False

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

    trafficSender(dataCollector, ipbase, speed, num=totalDevices)
