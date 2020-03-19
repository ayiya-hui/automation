import array
import struct
import inetUtil

next_offset=185

class IPPacket:
    """This class will create a raw IP packet with spoofed source IP address."""
    def __init__(self, srcAddr, destAddr, protocol, udp_packet, udp_fragment):
        self.version=4
        self.header_len=5
        self.tos=0
        self.len=20
        self.id=2400
        self.offset=0
        self.ttl=62
        self.protocol=protocol
        self.chksum=0
        self.src_addr=srcAddr
        self.dest_addr=destAddr
        self.udp_packet=udp_packet
        self.udp_fragment=udp_fragment
        if udp_fragment:
            self.more_fragment=1
        else:
            self.more_fragment=0

    def Assemble(self):
        """This method will pack an IP class object into a datastream. If data is chunk, then set fragment and offset"""
        finals=[]
        src=inetUtil.parse_addr(self.src_addr)
        dest=inetUtil.parse_addr(self.dest_addr)
        #assmeble main packet
        mylen=self.header_len+len(self.udp_packet)
        header=struct.pack('ccHHHcc', chr((self.version & 0x0f) << 4 | (self.header_len & 0x0f)), chr(self.tos & 0xff), mylen, self.id, (self.more_fragment & 0x01) << 13 | self.offset, chr(self.ttl & 0xff), chr(self.protocol & 0xff))
        pkt=header+'\000\000'+src+dest
        self.chksum=inetUtil.checksum(pkt)
        packet=header+struct.pack('H', self.chksum)+src+dest+self.udp_packet
        final=inetUtil.iph2net(packet)
        finals.append(final)
        #assmeble fragments
        if self.udp_fragment:
            if len(self.udp_fragment)==1:
                mylen=self.header_len+len(self.udp_fragment[0])
                header=struct.pack('ccHHHcc', chr((self.version & 0x0f) << 4 | (self.header_len & 0x0f)), chr(self.tos & 0xff), mylen, self.id, (0 & 0x01) << 13 | next_offset, chr(self.ttl & 0xff), chr(self.protocol & 0xff))
                pkt=header+'\000\000'+src+dest
                self.chksum=inetUtil.checksum(pkt)
                packet=header+struct.pack('H', self.chksum)+src+dest+self.udp_fragment[0]
                final=inetUtil.iph2net(packet)
                finals.append(final.encode('utf-8'))
            else:
                for i in range(len(self.udp_fragment)-1):
                    mylen=self.header_len+len(self.udp_fragment[i])
                    header=struct.pack('ccHHHcc', chr((self.version & 0x0f) << 4 | (self.header_len & 0x0f)), chr(self.tos & 0xff), mylen, self.id, (1 & 0x01) << 13 | 0, chr(self.ttl & 0xff), chr(self.protocol & 0xff))
                    pkt=header+'\000\000'+src+dest
                    self.chksum=inetUtil.checksum(pkt)
                    packet=header+struct.pack('H', self.chksum)+src+dest+self.udp_fragment[i]
                    final=inetUtil.iph2net(packet)
                    finals.append(final)
                mylen=self.header_len+len(self.udp_fragment[-1])
                header=struct.pack('ccHHHcc', chr((self.version & 0x0f) << 4 | (self.header_len & 0x0f)), chr(self.tos & 0xff), mylen, self.id, (0 & 0x01) << 13 | (i*next_offset), chr(self.ttl & 0xff), chr(self.protocol & 0xff))
                pkt=header+'\000\000'+src+dest
                self.chksum=inetUtil.checksum(pkt)
                packet=header+struct.pack('H', self.chksum)+src+dest+self.udp_fragment[0]
                final=inetUtil.iph2net(packet)
                print 'IP', type(final).__name__
                finals.append(final.encode('utf-8'))

        return finals


