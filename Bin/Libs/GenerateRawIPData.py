import rawUdp
import rawIp
from Util.randomGen import getRandomPort

udp_protocol=17

def getRawIpPacket(msg, srcIp, destIp, destPort, frag=False):
    """This method generates a raw IP packet."""
    myUdp=rawUdp.UDPPacket(getRandomPort(), destPort, msg)
    udpPacket, fragments=myUdp.Assemble(frag)
    myIP=rawIp.IPPacket(srcIp, destIp, udp_protocol, udpPacket, fragments)
    ipPackets=myIP.Assemble()

    return ipPackets

