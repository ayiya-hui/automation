import os
import socket

IFCONFIG='ifconfig eth0:%s %s netmask 255.255.255.0 up'
ROUTEDEL='route del -net %s.0 netmask 255.255.255.0'
ROUTEADD='route add -net %s.0 gw %s netmask 255.255.255.0'
GATEWAY='/etc/sysconfig/network-scripts/ifcfg-eth0'

def configVIF(number):
    ip=socket.gethostbyname(socket.gethostname()).split('.')
    ipBase=ip[0:3]
    ipStart=ip[-1]
    for i in range(number):
        ipEnd=str(int(ipStart)+i+1)
        ipFinal='.'.join(ipBase)+'.'+ipEnd
        os.system(IFCONFIG % (str(i+1), ipFinal))



if __name__=='__main__':
    number=150
    configVIF(number)



