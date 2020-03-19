from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp
from pyasn1.codec.ber import encoder
from pysnmp.proto import api

TRAP_PORT=162
DEFAULT_COMM='public'
V1='v1'
V2C='v2c'
ENTERPRISES='1.3.6.1.4.1.'
OID='oid'
TYPE='type'
VALUE='value'

class snmpHandler:
    def __init__(self, dataCollector):
        self.dataCollector=dataCollector

    def getOid(self):
        pass

    def sendTrap(self, version, enterprise, varList, community=False, destPort=False):
        if destPort:
            trapPort=destPort
        else:
            trapPort=TRAP_PORT
        if community:
            comm=community
        else:
            comm=DEFAULT_COMM
        if version==V1:
            verId=api.protoVersion1
        elif version==V2C:
            verId=api.protoVersion2c

        self.pMod=pMod=api.protoModules[verId]
        trapPdu=pMod.TrapPDU()
        pMod.apiTrapPDU.setDefaults(trapPdu)
        varBinds=self.__makeVarBinds(varList)

        if verId==api.protoVersion1:
            pMod.apiTrapPDU.setEnterprise(trapPdu, (pMod.ObjectIdentifier(ENTERPRISES+enterprise)))
            pMod.apiTrapPDU.setGenericTrap(trapPdu, 'coldStart')
            pMod.apiTrapPDU.setVarBinds(trapPdu, varBinds)
        trapMsg=pMod.Message()
        pMod.apiMessage.setDefaults(trapMsg)
        pMod.apiMessage.setCommunity(trapMsg, comm)
        pMod.apiMessage.setPDU(trapMsg, trapPdu)
        transportDispatcher=AsynsockDispatcher()
        transportDispatcher.registerTransport(udp.domainName, udp.UdpSocketTransport().openClientMode())
        transportDispatcher.sendMessage(encoder.encode(trapMsg), udp.domainName, (self.dataCollector, TRAP_PORT))
        transportDispatcher.runDispatcher()
        transportDispatcher.closeDispatcher()

    def __makeVarBinds(self, varList):
        varBinds=()
        for item in varList:
            tuple=()
            tuple+=self.pMod.ObjectIdentifier(ENTERPRISES+item[OID]),
            value=self.__typeReturn(item[VALUE], item[TYPE])
            tuple+=value,
            varBinds+=tuple,

        return varBinds

    def __typeReturn(self, value, type):
        if type=='macAddr':
            return self.pMod.OctetString(value)
        elif type=='string':
            return self.pMod.OctetString(value)
        elif type=='integer':
            return self.pMod.Integer(value)
        elif type=='ipAddr':
            return self.pMod.IpAddress(value)
        elif type=='counter':
            return self.pMod.Counter(value)
        elif type=='timeTicks':
            return self.pMod.TimeTicks(value)
        elif type=='Gauge':
            return self.pMod.Gauge(value)
        elif type=='networkAdd':
            return self.pMod.NetworkAddress(value)
        else:
            return self.pMod.Null(value)

if __name__=='__main__':
     myHandler=snmpHandler('192.168.20.118')
     enterprise='9.9.599.0.4'
     varList=[]
     varList.append({'oid':'9.9.599.1.3.1.1.1.0', 'type':'macAddr', 'value':'00 24 D7 36 A0 00'})
     varList.append({'oid':'9.9.513.1.1.1.1.5.0', 'type':'string', 'value':'AP-2'})
     varList.append({'oid':'9.9.599.1.3.1.1.8.0', 'type':'macAddr', 'value':'00 25 45 B7 66 70'})
     varList.append({'oid':'9.9.513.1.2.1.1.1.0', 'type':'integer', 'value':0})
     varList.append({'oid':'9.9.599.1.3.1.1.10.0', 'type':'ipAddr', 'value':'172.22.4.54'})
     varList.append({'oid':'9.9.599.1.2.1.0', 'type':'string', 'value':'IE\brouse'})
     varList.append({'oid':'9.9.599.1.2.2.0', 'type':'string', 'value':'IE'})
     myHandler.sendTrap(V2C, enterprise, varList, community='1n3t3ng')
     print 'Done'




