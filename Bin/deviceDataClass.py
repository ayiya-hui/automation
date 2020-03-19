from pickClass import pickleClass

class device:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.accessIp=''
        self.creationMethod=''
        self.deviceType=''
        self.name=''

class deviceType:
    def __init__(self):
        self.model=''
        self.vendor=''
        self.version=''

class ipAccessMapping(pickleClass):
    def __init__(self):
        self.ipRange=''
        self.accessMethod=''

class discoveryIpRange(pickleClass):
    def __init__(self):
        self.name=''
        self.includeRange=''
        self.excludeRange=''
        self.noPing='True'



