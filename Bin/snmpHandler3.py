from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntforg, context
from pysnmp.proto.api import v2c

TRAP_PORT=162
DEFAULT_COMM='public'
V1='v1'
V2C='v2c'
V3='v3'
ENTERPRISES='1.3.6.1.4.1.'
OID='oid'
TYPE='type'
VALUE='value'
TEST_AGENT='test_agent'
TEST_USER='test_user'
AUTHKEY='authkey'
PRIVKEY='privkey'
AUTHPRIV='authPriv'
PARAM='MyParams'
NMS='MyNMS'

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
        snmpEngine = engine.SnmpEngine()
        # v1/2 setup
        config.addV1System(snmpEngine, TEST_AGENT, comm)
        # v3 setup
        config.addV3User(snmpEngine, TEST_USER, config.usmHMACMD5AuthProtocol, 'authKey1',config.usmDESPrivProtocol, 'privKey1')
        # Transport params
        config.addTargetParams(snmpEngine, PARAM, TEST_USER, AUTHPRIV)
        #config.addTargetParams(snmpEngine, 'myParams', 'test-agent', 'noAuthNoPriv', 0)
        # Transport addresses
        config.addTargetAddr(snmpEngine, NMS, config.snmpUDPDomain,(self.dataCollector, trapPort), PARAM, tagList='myManagementStations')
        # Notification targets
        config.addNotificationTarget(
        #    snmpEngine, 'myNotifyName', 'myParams', 'myManagementStations', 'trap'
            snmpEngine, 'myNotifyName', PARAM, 'myManagementStations', 'inform'
            )
        # Setup transport endpoint
        config.addSocketTransport(snmpEngine, udp.domainName, udp.UdpSocketTransport().openClientMode())
        # Agent-side VACM setup
        config.addContext(snmpEngine, '')
        config.addTrapUser(snmpEngine, 1, 'test-agent', 'noAuthNoPriv', (1,3,6)) # v1
        config.addTrapUser(snmpEngine, 2, 'test-agent', 'noAuthNoPriv', (1,3,6)) # v2c
        config.addTrapUser(snmpEngine, 3, 'test-user', 'authPriv', (1,3,6)) # v3

        # SNMP context
        snmpContext = context.SnmpContext(snmpEngine)

        def cbFun(sendRequestHandle, errorIndication, cbCtx):
            if errorIndication:
                print errorIndication

        ntforg.NotificationOriginator(snmpContext).sendNotification(
            snmpEngine, 'myNotifyName', ('SNMPv2-MIB', 'coldStart'),
            (((1,3,6,1,2,1,1,5), v2c.OctetString('Example Notificator')),), cbFun)

        snmpEngine.transportDispatcher.runDispatcher()


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




