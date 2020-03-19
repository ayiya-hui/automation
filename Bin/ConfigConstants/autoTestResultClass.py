class AutoTestResult:
    """This class is for automation test result."""
    def __init__(self):
        self.name=None
        self.testType=None
        self.totalRun=0
        self.totalPass=0
        self.totalNoReturn=0
        self.totalFail=0
        self.totalMissing=0
        self.totalExtra=0
        self.runTime=None
        self.sendEmail=None
        self.runVersion=None
        self.testFolder=None
        self.localhost=None
        self.suiteList=[]
        self.info='N/A'

class TestSuiteResult:
    """This class is for automation test suite result."""
    def __init__(self):
        self.name=None
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
        self.info=''

class TestCaseResult:
    """This class is for automation test case result."""
    def __init__(self):
        self.name=None
        self.status=None
        self.Pass=[]
        self.Fail=[]
        self.Missing=[]
        self.Extra=[]
