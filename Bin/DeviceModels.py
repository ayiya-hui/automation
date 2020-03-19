from pickClass import pickleClass

class discoveryResult(pickleClass):
    def __init__(self, tId, id, success=[]):
        self.attribute={}
        self.attribute['tmpTd']=''
        self.attribute['custId']=''
        self.discoverAgent=1
        self.source="Discovery"
        self.status=100
        self.success=success
        self.failure=""

class device(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=''
        self.discoverMethod=''
        self.accessMethodIds=''
        self.discoverTime=''
        self.name=''
        self.accessIp=''
        self.vendor=''
        self.model=''
        self.version=''
        self.description=''
        self.sysUptime=''
        self.interfaces=''
        self.storages=''
        self.buildNum=''
        self.osSerialNumber=''
        self.osEdition=''
        self.organization=''
        self.processors=''
        self.assetCategory=''
        self.assetWeight=''
        self.location=''
        self.contact=''
        self.hwVendor=''
        self.hwModel=''
        self.hwSerialNum=''
        self.bios=''
        self.inventory=''
        self.patches=''
        self.installedSoftware=''
        self.runningSoftware=''
        self.swServices=''



class BIOS(pickleClass):
    def __init__(self):
        self.name=''
        self.vendor=''
        self.serialNumber=''
        self.version=''


class patch(pickleClass):
    def __init__(self):
        self.name=''
        self.description=''
        self.installedBy=''
        self.installedOn=''


class processor(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=''
        self.name=''
        self.cpuUtil=''
        self.manufacturer=''
        self.version=''
        self.addrWidth=''
        self.dataWidth=''
        self.currClockSpeed=''
        self.maxClockSpeed=''
        self.l2CacheSize=''
        self.l2CacheSpeed=''

class storage(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=''
        self.type=''
        self.description=''
        self.size=''
        self.used=''
        self.memUtil=''
        self.diskUtil=''



class networkInterface(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=''
        self.type=''
        self.name=''
        self.description=''
        self.ipv4Addr=''
        self.ipv4Mask=''
        self.macAddr=''
        self.speed=''
        self.snmpIndex=''
        self.adminStatus=''
        self.operStatus=''

class InstalledSoftware(pickleClass):
    def __init__(self, id):
        self.attribute={}
        self.attribute['custId']=''
        self.attribute['count']='80'

class application(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=''
        self.name=''
        self.groupName=''
        self.processName=''
        self.path=''
        self.uptime=''
        self.status=''


class swService(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=''
        self.name=''
        self.displayName=''
        self.descripition=''
        self.processId=''
        self.path=''
        self.state=''
        self.status=''
        self.startedFlag=''
        self.startMode=''

class component(pickleClass):
    def __init__(self):
        self.description=''
        self.model=''
        self.serial=''
        self.manufacturer=''
        self.swVer=''
        self.firmVer=''
