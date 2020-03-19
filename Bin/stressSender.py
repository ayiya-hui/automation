from socket import *
import random

def stressSender(dataCollector, totalRun):
    udpClient=socket(AF_INET, SOCK_DGRAM)
    udpClient.connect((dataCollector, 514))
    msg="<166>Sep 30 18:02:54 "+dataCollector+" Hostd: [2010-09-30 18:02:54.945 1B885DC0 verbose 'vm:/vmfs/volumes/116bf7c8-d061117a/saas01-app-02/saas01-app-02.vmx'] Actual VM overhead: 418635776 bytes"
    print msg

    for j in range(totalRun):
        udpClient.sendall(msg.encode())
        print "continue..."

if __name__=='__main__':
    import sys
    stressSender(sys.argv[1], int(sys.argv[2]))
