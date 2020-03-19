from socket import *
import os, random, time, datetime

def trafficSender(dataCollector, ipbase, speed, totalDevices):
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

    #define speed
    if speed=='100':
        sleep=100.0
    elif speed=='500':
        sleep=20.0
    elif speed=='1000':
        sleep=10.0
    elif speed=='1500':
        sleep=5.0
    else:
        print "This speed is not support. Default to 100 EPS."
        speed=100.0

    while 1:
        stime=datetime.datetime.now()
        for i in range(300):
            for j in range(10):
                ip=ipbase+"."+str(int(random.randrange(2, int(totalDevices))))
                if len(rawData)==1:
                    ranMsg=0
                else:
                    ranMsg=int(random.randrange(0, len(rawData)-1))
                msg=rawData[ranMsg]
                msg=msg.replace("$ip", ip)
                sendMsg=msg.encode()
                udpClient.sendall(sendMsg)
            time.sleep(float(sleep)/1000)

        ftime=datetime.datetime.now()
        dTime=ftime-stime
        print "3000 events using %s" % dTime.seconds
        if dTime.seconds==0:
            totalTime=1
        else:
            totalTime=dTime.seconds
        print "sending speed is %s per second." % (3000/totalTime)




if __name__=='__main__':
    import sys
    dataCollector=sys.argv[1]
    ipbase=sys.argv[2]
    speed=sys.argv[3]
    totalDevices=sys.argv[4]

    if len(sys.argv) not in [4, 5]:
        usage="""Usage: trafficSender.py dataCollector Ipbase speed totalDevices
                Ipbase -- first three parts of IP address
                speed -- how many events per second. Support 100 and 500 now
                (optional)totalDevices -- total numbers of devices to simulated. """
        print usage
        exit()
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






