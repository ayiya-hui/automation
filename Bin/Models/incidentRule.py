device_types={'Network':'cisco',
              'WINDOWS_SERVER':'win',
              'Server':'win',
              'SERVER':'linux',
              'NETWORK_IPS':'cisco_ips',
              'FIREWALL':'juniper_ssg',
              'default':'linux'}
class rule:
    def __init__(self):
        self.incidentType=None
        self.ipAddr=None
        self.eventTypes=[]
        self.msgs=[]
        self.count=None
        self.createDevice=False
        self.deviceType=False
        self.deviceName=None
        self.intervalSent=30
        self.insideInterval=10
        self.count=1

    def setCreateDevice(self, group_type):
        self.createDevice=True
        if group_type in device_types:
            self.deviceType=device_types[group_type]
        else:
            print 'Device Type %s is NOT supported now. Use Linux as default.' % group_type
            self.deviceType=device_types['default']

    def setDeviceInfo(self, ipAddr, deviceName):
        self.ipAddr=ipAddr
        self.deviceName=deviceName

    def setSendOrder(self):
        map={}
        print 'events: ', self.eventTypes
        if self.eventTypes:
            for item in self.eventTypes:
                map[item.sendOrder]=item
        print 'Map: %s' % str(map)

        return map

class eventMsgType:
    def __init__(self):
        self.type=''
        self.eventType=''

    def setType(self, type, eventType, sendOrder):
        self.type=type
        self.eventType=eventType
        self.sendOrder=sendOrder

