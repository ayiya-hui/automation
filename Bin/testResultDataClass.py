from pickClass import pickleClass

class suiteTestResult(pickleClass):
    def __init__(self):
        self.name=''
        self.testFileName=''
        self.runTime=''
        self.totalRun=0
        self.totalPass=0
        self.totalFail=0
        self.totalNoReturn=0
        self.totalMiss=0
        self.totalImprove=0
        self.caseTestResults=[]

class caseTestResult(pickleClass):
    def __init__(self):
        self.testCaseName=''
        self.testCaseNum=''
        self.reporter=''
        self.eventType=''
        self.status=''
        self.passed=[]
        self.failed=[]
        self.missed=[]
        self.improved=[]

class param(pickleClass):
    def __init__(self):
        self.name=''
        self.expect=''
        self.actual=''
