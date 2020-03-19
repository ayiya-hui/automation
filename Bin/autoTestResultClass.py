from pickClass import pickleClass

class AutoTestResult(pickleClass):
    def __init__(self, totalRun, totalPass, totalNoReturn, totalFail, totalMissing, totalImprove, runTime, testTask, testVersion, testFolder, localhost, suiteList=[]):
        self.totalRun=totalRun
        self.totalPass=totalPass
        self.totalNoReturn=totalNoReturn
        self.totalFail=totalFail
        self.totalMissing=totalMissing
        self.totalImprove=totalImprove
        self.runTime=runTime
        self.testTask=testTask
        self.runVersion=testVersion
        self.testFolder=testFolder
        self.localhost=localhost
        self.suiteList=suiteList

class TestSuiteResult(pickleClass):
    def __init__(self, name, fileName, totalRun, totalPass, totalNoReturn, totalFail, totalMissing, totalImprove, caseList=[]):
        self.name=name
        self.fileName=fileName
        self.totalRun=totalRun
        self.totalPass=totalPass
        self.totalNoReturn=totalNoReturn
        self.totalFail=totalFail
        self.totalMissing=totalMissing
        self.totalImprove=totalImprove
        self.caseList=caseList

class TestCaseResult(pickleClass):
    def __init__(self, name, status, PassDetails=[], FailDetails=[], MissDetails=[], ImproveDetails=[], reporter=False, eventType=False, bugId=False):
        self.name=name
        self.status=status
        self.PassDetails=PassDetails
        self.FailDetails=FailDetails
        self.MissDetails=MissDetails
        self.ImproveDetails=ImproveDetails
        if reporter:
            self.reporter=reporter
        if eventType:
            self.eventType=eventType
        if bugId:
            self.bugId=bugId
