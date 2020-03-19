class incidentSuite:
    def __init__(self):
        self.name=None
        self.method=None
        self.testcases=[]

class incidentCase:
    def __init__(self):
        self.name=None
        self.eventType=None
        self.reporter=None
        self.repeatCount=None
        self.createDevice=None
        self.deviceType=None
        self.deviceName=None
        self.domainController=None
        self.events=[]
        self.parameters=None

class incidentEvent:
    def __init__(self):
        self.incidentMsg=None
