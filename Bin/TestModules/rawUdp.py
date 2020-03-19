import struct
import array
import inetUtil
import string

udp_protocol=17
maximum_data_length=1472

class UDPPacket:
    """This class will create a raw UDP packet."""
    def __init__(self, srcPort, destPort, data):
        self.src_port=srcPort
        self.dest_port=destPort
        self.len=0
        self.chksum=0
        self.data=data

    def Assemble(self, fragment=False):
        """This method will pack a UDP class object into a datastream. If the data is too long and cannot send in one piece(over 1472), then it will make IP fragmentation"""
        data=''
        fragments=[]
        if fragment:
            count=len(self.data)/maximum_data_length
            data=self.data[:maximum_data_length]
            print 'udp main packet data length: %i' % len(data)
            if count==1:
                fragments.append(self.data[maximum_data_length:])
            else:
                for i in range(count-1):
                    fragments.append(self.data[(i+1)*maximum_data_length:(i+2)*maximum_data_length])
                fragments.append(self.data[(count)*maximum_data_length:])
        else:
            data=self.data
        self.len=8+len(data)
        udp_pkt=struct.pack('HHHH', self.src_port, self.dest_port, self.len, self.chksum)+data
        if (len(udp_pkt) & 1):
            udp_pkt=udp_pkt+'\0'
        final_pkt=inetUtil.udph2net(udp_pkt)
        if fragments:
            i=1
            for fra in fragments:
                print 'udp fragment %i length: %i' % (i, len(fra))
                i+=1

        return final_pkt, fragments

