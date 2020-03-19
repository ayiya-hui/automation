import struct
import array
from socket import inet_aton

def __ntohs(pkt):
    return struct.pack('H', struct.unpack('!H', pkt)[0])

def __htons(pkt):
    return struct.pack('!H', struct.unpack('H', pkt)[0])

def iph2net(pkt):
    """This method handles IP from host order to network order."""
    return pkt[:2]+__htons(pkt[2:4])+__htons(pkt[4:6])+__htons(pkt[6:8])+pkt[8:]

def net2iph(pkt):
    """This method handles IP from network order to host order."""
    return pkt[:2]+__ntohs(pkt[2:4])+__ntohs(pkt[4:6])+__ntohs(pkt[6:8])+pkt[8:]

def udph2net(pkt):
    """This method handles UDP from host order to network order."""
    return __htons(pkt[:2])+__htons(pkt[2:4])+__htons(pkt[4:6])+pkt[6:]

def net2udph(pkt):
    """This method handles UDP from network order to host order."""
    return __ntohs(pkt[:2])+__ntohs(pkt[2:4])+__ntohs(pkt[4:6])+pkt[6:]

def parse_addr(addr):
    """This method transfer an IP address from x.x.x.x string format into a structure."""
    return inet_aton(addr)

def checksum(pkt):
    """This method calculate a checksum(for IP packet)."""
    if (len(pkt) & 1):
        pkt=pkt+'\0'
    words=array.array('h', pkt)
    sum=0
    for word in words:
        sum=sum+(word & 0xffff)
    hi=sum >> 16
    lo=sum & 0xffff
    sum=hi+lo
    sum=sum+(sum >> 16)
    last=(~sum) & 0xffff

    return last




