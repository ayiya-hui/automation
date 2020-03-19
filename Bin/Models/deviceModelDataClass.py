import Util.randomGen as randomGen

class discoveryResult:
    def __init__(self):
        self.attribute={}
        self.attribute['tmpTd']=None
        self.attribute['custId']=None
        self.discoverAgent=1
        self.source='Discovery'
        self.status=100
        self.success=[]
        self.failure=None

class device:
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=None
        self.discoverMethod=None
        self.accessMethodIds=None
        self.discoverTime=randomGen.getRandomNum(1200, 2000)+'000000000'
        self.name=None
        self.accessIp=None
        self.vendor=None
        self.model=None
        self.version=None
        self.description=None
        self.sysUptime=randomGen.getRandomNum(7000, 9000)+'0000'
        self.interfaces=[]
        self.storages=[]
        self.buildNum=None
        self.osSerialNumber=None
        self.osEdition=None
        self.organization=None
        self.processors=[]
        self.assetCategory=None
        self.assetWeight=None
        self.location=None
        self.contact=None
        self.hwVendor=None
        self.hwModel=None
        self.hwSerialNum=None
        self.bios=BIOS()
        self.inventory=None
        self.patches=[]
        self.installedSoftware=[]
        self.runningSoftware=[]
        self.swServices=[]
        self.inventory=inventory()
        self.monitorTypes=None



class BIOS:
    def __init__(self):
        self.name=None
        self.vendor=None
        self.serialNumber=None
        self.version=None


class patch:
    def __init__(self):
        self.name=None
        self.description=None
        self.installedBy=None
        self.installedOn=None


class processor:
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=None
        self.name=None
        self.cpuUtil=None
        self.manufacturer=None
        self.version=None
        self.addrWidth=None
        self.dataWidth=None
        self.currClockSpeed=None
        self.maxClockSpeed=None
        self.l2CacheSize=None
        self.l2CacheSpeed=None

class storage:
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=None
        self.type=None
        self.description=None
        self.size=None
        self.used=None
        self.memUtil=None
        self.diskUtil=None



class networkInterface:
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=None
        self.type=None
        self.name=None
        self.description=None
        self.ipv4Addr=None
        self.ipv4Mask=None
        self.macAddr=randomGen.getRandomMac()
        self.speed=None
        self.snmpIndex=None
        self.adminStatus=None
        self.operStatus=None

class InstalledSoftware:
    def __init__(self, id):
        self.attribute={}
        self.attribute['custId']=None
        self.attribute['count']='80'

class application:
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=None
        self.name=None
        self.groupName=None
        self.processName=None
        self.path=None
        self.uptime=None
        self.status=None


class swService:
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=None
        self.name=None
        self.displayName=None
        self.descripition=None
        self.processId=None
        self.path=None
        self.state=None
        self.status=None
        self.startedFlag=None
        self.startMode=None

class component:
    def __init__(self):
        self.description=None
        self.model=None
        self.serial=None
        self.manufacturer=None
        self.swVer=None
        self.firmVer=None

class inventory:
    def __init__(self):
        self.description=None
        self.model=None
        self.manufacturer=None
        self.swVer=None
