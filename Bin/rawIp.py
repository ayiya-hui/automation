import array
import struct
import inetUtil

next_offset=1480
fragment=1

class IPPacket:
    """This class will create a raw IP packet with spoofed source IP address."""
    def __init__(self, srcAddr, destAddr, protocol, data):
        self.version=4
        self.header_len=5
        self.tos=0
        self.len=20
        self.id=0
        self.mf=0
        self.offset=0
        self.ttl=62
        self.protocol=protocol
        self.chksum=0
        self.src_addr=srcAddr
        self.dest_addr=destAddr
        self.data=data

    def Assemble(self):
        """This method will pack an IP class object into a datastream. If data is chunk, then set fragment and offset"""
        finals=[]
        src=inetUtil.parse_addr(self.src_addr)
        dest=inetUtil.parse_addr(self.dest_addr)
        if len(self.data)>1:
            self.mf=1
        for i in range(len(self.data)):
            mylen=self.header_len+len(self.data[i])
            print self.data[i]
            if i>0:
                self.offset=next_offset
            if i==(len(self.data)-1):
                self.mf=0
            print 'packet: %i, fragment bit: %s, offset: %i' % (i, ((self.mf & 0x01) << 13), self.offset)
            header=struct.pack('ccHHHcc', chr((self.version & 0x0f) << 4 | (self.header_len & 0x0f)), chr(self.tos & 0xff), mylen, self.id, (self.mf & 0x01) << 13 | self.offset, chr(self.ttl & 0xff), chr(self.protocol & 0xff))

            pkt=header+'\000\000'+src+dest
            self.chksum=inetUtil.checksum(pkt)
            packet=header+struct.pack('H', self.chksum)+src+dest+self.data[i]
            final=inetUtil.iph2net(packet)
            print 'ip packet lenght: %i' % len(final)

            finals.append(final)

        return finals


