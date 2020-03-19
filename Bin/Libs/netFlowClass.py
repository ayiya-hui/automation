import struct
"""try:
    import ctypes
    TYPE='CTYPES'
except ImportError:"""
TYPE='STRUCT'

class netflowV5Packet:
    """This class will create a Netflow V5 packet."""
    def __init__(self, v5header, v5Records):
        self.header=v5header
        self.records=v5Records

    def Assemble(self):
        """This method will pack a netflow v5 class object into a
        datastream by first with ctypes, or with struct if ctypes
        not present."""
        if TYPE=='CTYPES':
            packet=self.__assembleCtypes()
        else:
            packet=self.__assembleStruct()

        return packet

    def __assembleCtypes(self):
        th='H H L L L L B B H'
        tr=''
        values=[]
        values.append(self.header.version)
        values.append(self.header.count)
        values.append(self.header.sys_uptime)
        values.append(self.header.unix_secs)
        values.append(self.header.unix_nsecs)
        values.append(self.header.flow_sequence)
        values.append(self.header.engine_type)
        values.append(self.header.engine_id)
        values.append(self.header.sampling_interval)

        for re in self.records:
            tr=tr+'B B B B B B B B B B B B H H L L L L H H B B B B H H B B H'

            for i in re.srcaddr.split("."):
                values.append(int(i))

            for i in re.dstaddr.split("."):
                values.append(int(i))

            for i in re.nexthop.split("."):
                values.append(int(i))

            values.append(re.input)
            values.append(re.output)
            values.append(re.dPkts)
            values.append(re.dOctets)
            values.append(re.first)
            values.append(re.last)
            values.append(re.srcport)
            values.append(re.dstport)
            values.append(re.pad1)
            values.append(re.tcp_flags)
            values.append(re.prot)
            values.append(re.tos)
            values.append(re.src_as)
            values.append(re.dst_as)
            values.append(re.src_mask)
            values.append(re.dst_mask)
            values.append(re.pad2)

        s=struct.Struct('>'+th+tr)
        b=ctypes.create_string_buffer(s.size)
        s.pack_into(b, 0, *values)

        return b

    def __assembleStruct(self):
        header=struct.pack('>HHLLLLBBH', self.header.version, self.header.count, self.header.sys_uptime, self.header.unix_secs, self.header.unix_nsecs, self.header.flow_sequence, self.header.engine_type,
                        self.header.engine_id, self.header.sampling_interval)
        record=''
        for re in self.records:
            src=re.srcaddr.split(".")
            dst=re.dstaddr.split(".")
            hop=re.nexthop.split(".")
            src1=int(src[0])
            src2=int(src[1])
            src3=int(src[2])
            src4=int(src[3])
            dst1=int(dst[0])
            dst2=int(dst[1])
            dst3=int(dst[2])
            dst4=int(dst[3])
            record=record+struct.pack('>BBBBBBBBBBBBHHLLLLHHBBBBHHBBH', src1, src2, src3, src4, dst1, dst2, dst3, dst4, int(hop[0]), int(hop[1]), int(hop[2]), int(hop[3]), re.input, re.output,
                                re.dPkts, re.dOctets, re.first, re.last, re.srcport, re.dstport, re.pad1, re.tcp_flags, re.prot, re.tos, re.src_as, re.dst_as, re.src_mask, re.dst_mask, re.pad2)
        packet=header+record

        return packet



class netflowV5Header:
    """This class will create a netflow v5 header."""
    def __init__(self, count, unixS, unixNano):
        self.version=5                #NetFlow export format version number
        self.count=count                #Number of flows exported in this packet(1-30)
        self.sys_uptime=999999        #Current time in milliseconds since th eexport device booted
        self.unix_secs=unixS        #Current count of seconds since 0000 UTC 1970
        self.unix_nsecs=unixNano        #Residual nanoseconds since 0000 UTC 1970
        self.flow_sequence=111100        #Sequence counter of ttal flows seen
        self.engine_type=255            #Type of flow-switching engine
        self.engine_id=255            #Slot number of the flow-switching engine
        self.sampling_interval=65535        #First two bits hold the sampling mode, remaining 14 bits hold value of sampling interval

class netflowV5Record:
    """This class will create a netflow v5 record."""
    def __init__(self, srcIp, dstIp, nextHop, srcPort, dstPort, tcpFlags, protocol, Packets, Bytes):
        self.srcaddr=srcIp            #Source IP address
        self.dstaddr=dstIp            #Destination IP address
        self.nexthop=nextHop            #IP address of next hop router
        self.input=101                #SNMP index of input interface
        self.output=102                #SNMP index of output interface
        self.dPkts=Packets            #Packets in the flow
        self.dOctets=Bytes            #Total number of Layer 3 bytes in the packets of the flow
        self.first=5200                #SysUptime at start of flow
        self.last=5300                #SysUptime at the time the last packet of the flow was received
        self.srcport=srcPort            #TCP/UDP source port number or equivalent
        self.dstport=dstPort            #TCP/UDP destination port number of equivalent
        self.pad1=0                #Unused (zeors) bytes
        self.tcp_flags=tcpFlags            #Cumulative OR of TCP flags
        self.prot=protocol            #IP protocl type (for exampe, TCP=6; UDP=17)
        self.tos=1                    #IP type of service (ToS)
        self.src_as=1001                #Autonomous system number of the source, either origin or peer
        self.dst_as=1002                #Autonomous system number of the destination, either origin or peer
        self.src_mask=254            #Source address prefix mask bits
        self.dst_mask=254            #Destination address prefix mask bits
        self.pad2=0                #Unused (zero) bytes



