class eventParser:
    def __init__(self):
        self.attribute={}
        self.attribute['sysDefined']=None
        self.attribute['name']=None
        self.attribute['enabled']=None
        self.deviceType=deviceType()
        self.parserXml=None

class deviceType:
    def __init__(self):
        self.attribute={}
        self.attribute['xmlId']=None
        self.accessProtocol=None
        self.type=None
        self.model=None
        self.objectGroup=None
        self.sysDefined=None
        self.vendor=None
