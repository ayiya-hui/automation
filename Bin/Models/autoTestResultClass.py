class AutoTestResult:
    """This class is for automation test result."""
    def __init__(self):
        self.name=None
        self.batch=None
        self.testType=None
        self.totalRun=0
        self.totalPass=0
        self.totalNoReturn=0
        self.totalFail=0
        self.totalMissing=0
        self.totalExtra=0
	self.recipient=None
        self.runTime=None
        self.sendEmail=None
        self.runVersion=None
        self.testFolder=None
        self.localhost=None
        self.suiteList=[]

class TestSuiteResult:
    """This class is for automation test suite result."""
    def __init__(self):
        self.name=None
        self.type=None
        self.ruleId=None
        self.queryString=None
        self.rawMsg=None
        self.testMethod=None
        self.reptIpAddr=None
        self.taskName=None
        self.fileName=None
        self.testFileName=None
        self.totalRun=0
        self.totalPass=0
        self.totalNoReturn=0
        self.totalFail=0
        self.totalMissing=0
        self.totalExtra=0
        self.caseList=[]
        self.testRuleResultSummary=None
        self.testRuleDetail=None
        self.debugInfo=None

class TestCaseResult:
    """This class is for automation test case result."""
    def __init__(self):
        self.name=None
        self.status=None
        self.Pass=[]
        self.Fail=[]
        self.Missing=[]
        self.Extra=[]
