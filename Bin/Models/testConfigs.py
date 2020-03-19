class testConfig:
    def __init__(self):
        self.name=None
        self.testType=None
        self.batch=None
        self.sendEmail=None
        self.localhost=None
        self.buildVersion=None
        self.runTime=None
        self.testServer=testServer()
        self.credential=credential()
        self.rootCredential=rootCredential()
        self.testTask=[]
        self.threadPool=None
        self.threadWaitTime=None
        self.NotCheckTimer=False
        self.advance=None
        self.ruleTest=None
        self.noSend=None
        self.recipient=None

class testServer:
    def __init__(self):
        self.allInOne=None
        self.dataCollector=None
        self.appServer=None
        self.dbServer=None

class credential:
    def __init__(self):
        self.user=None
        self.password=None

class rootCredential:
    def __init__(self):
        self.password=None

class testTask:
    def __init__(self):
        self.taskName=None
        self.taskFiles=None
        self.exclude=None
        self.taskOption=None
        self.waitTime=None

class incidentData:
    def __init__(self):
        self.incidentType=None
        self.name=None
        self.reptDevIpAddr=None
        self.createDevice=None
        self.deviceName=None
        self.deviceType=None
        self.domainController=None
        self.count=None
        self.method=None

class eventParsingData:
    def __init__(self):
        self.eventType=None
        self.name=None
        self.module=None
        self.reptDevIpAddr=None
        self.key=None
        self.method=None

class DbPopulatorData:
    def __init__(self):
        self.name=None
        self.testType=None
        self.fileType=None

class logDiscoverData:
    def __init__(self):
        self.name=None
        self.reptDevIpAddr=None
        self.model=None
        self.vendor=None
        self.model=None
        self.version='ANY'
        self.creationMethod='LOG'
        self.isApp=None

class testData:
    """This class is for testData."""
    def __init__(self):
        self.path=None
        self.dataMap={}

class testDataItem:
    """This class ia for testDataItem."""
    def __init__(self):
        self.eventMsg=None
        self.clearEventMsg=None
        self.params=None







