import logging

class Config:
	def __init__(self):
		self.dataCollector=''
		self.appServer=''
		self.user=''
		self.password=''
		self.testModule=''
		self.testTask=''
		self.testSuites=''
		self.excludeSuites=''
		self.option=''
		self.sleep=''
		self.version=''

class TestCategory:
	def __init__(self):
		self.suites=''

class TestSuite:
    def __init__(self):
        self.name=''
        self.method=''
        self.setupTasks=[]
        self.testcases=[]
        self.fileName=''

class configImportSuite(TestSuite):
	def __init__(self):
		TestSuite.__init__(self)

class RBACSuite(TestSuite):
	def __init__(self):
		TestSuite.__init__(self)

class adminRole:
	def __init__(self):
		self.userName=''
		self.org=''
		self.password=''
		self.scope=''

class setupTask:
	def __init__(self):
		self.setupName=''
		self.setupValue=[]

class verifyTask:
	def __init__(self):
		self.type=''

class eventTypeQuery:
	def __init__(self):
		self.name=''

class reportQuery:
	def __init__(self):
		self.id=''
		self.eventType=''
		self.key=''

class rbacEventQuery:
	def __init__(self):
		self.name=''
		self.condition=''

class readEventType:
	def __init__(self):
		self.name=''

class createDevice:
	def __init__(self):
		self.deviceList=[]

class device:
	def __init__(self):
		self.name=''
		self.type=''
		self.ip=''
		self.custId=''

class sentEvent:
	def __init__(self):
		self.eventList=[]

class event:
	def __init__(self):
		self.eventType=''
		self.reporter=''

class sentIncident:
	def __init__(self):
		self.incidentList=[]

class incident:
	def __init__(self):
		self.incidentType=''
		self.reporter=''

class eventExportSuite(TestSuite):
	def __init__(self):
		TestSuite.__init__(self)

class eventParsingSuite(TestSuite):
	def __init__(self):
		TestSuite.__init__(self)

	def getKeyMap(self):
		eventKey=[]
		reporterKey=[]
		for case in self.testcases:
			event=case.eventType.strip()
			if event not in eventKey:
				eventKey.append(event)
			reporter=case.reporter
			if reporter not in reporterKey:
				reporterKey.append(reporter)
		eventStr='","'.join(eventKey)
		reporterStr=','.join(reporterKey)
		keyMap={}
		keyMap['eventType']='"'+eventStr+'"'
		keyMap['reporter']=reporterStr

		return keyMap
class eventTypeSuite(TestSuite):
	def __init__(self):
		TestSuite.__init__(self)
class logDiscoverySuite(TestSuite):
    def __init__(self):
        TestSuite.__init__(self)

class incidentSuite(TestSuite):
	def __init__(self):
		TestSuite.__init__(self)

	def getKeyMap(self):
		eventKey=[]
		reporterKey=[]
		for case in self.testcases:
			event=case.eventType.strip()
			if event not in eventKey:
				eventKey.append(event)
			reporter=case.reporter
			if reporter not in reporterKey:
				reporterKey.append(reporter)
		eventStr='","'.join(eventKey)
		reporterStr='","'.join(reporterKey)
		keyMap={}
		keyMap['eventType']='"'+eventStr+'"'
		keyMap['reporter']='"'+reporterStr+'"'

		return keyMap

class incidentTimeBasedSuite(incidentSuite):
	def __init__(self):
		incidentSuite.__init__(self)
		self.sendEvent=''

class incidentPatternBasedSuite(incidentTimeBasedSuite):
	def __init__(self):
		incidentTimeBasedSuite.__init__(self)

class linuxFileMonitorSuite(TestSuite):
	def __init__(self):
		TestSuite.__init__(self)
		self.linuxHost=''
		self.linuxUsers=[]
		self.monPath=''
		self.monConfig=''

class linuxUser:
	def __init__(self):
		self.name=''
		self.password=''

class reportSuite(TestSuite):
	def __init__(self):
		TestSuite.__init__(self)

class TestCase:
	def __init__(self):
		self.name=''
		self.reporter=''

class configImportCase(TestCase):
	def __init__(self):
		TestCase.__init__(self)

class RBACCase(TestCase):
	def __init__(self):
		TestCase.__init__(self)
		self.verifyName=''
		self.eventType=''
		self.desc=''
		self.roleName=''
		self.verifyTasks=[]

class eventExportCase(TestCase):
	def __init__(self):
		TestCase.__init__(self)
		self.deviceName=''
		self.timeZone=''
		self.option=''
		self.startTime=''
		self.endTime=''
		self.custName=''

class eventParsingCase(TestCase):
	def __init__(self):
		TestCase.__init__(self)
		self.eventType=''
		self.parseEvent=''
		self.key=''
		self.parameters=''

class eventTypeCase(TestCase):
	def __init__(self):
		TestCase.__init__(self)
		self.verifyTasks=[]

class logDiscoveryCase(TestCase):
    def __init__(self):
        TestCase.__init__(self)
        self.discoverEvent=''
        self.parameters=''

class incidentCase(TestCase):
	def __init__(self):
		TestCase.__init__(self)
		self.eventType=''
		self.createDevice=''
		self.deviceType=''
		self.deviceName=''
		self.custId=''
		self.repeatCount=''
		self.repeatInterval=''
		self.domainController=''
		self.events=[]
		self.parameters=''

class incidentEvent:
	def __init__(self):
		self.incidentMsg=''

class incidentTimeBasedCase(incidentCase):
	def __init__(self):
		incidentCase.__init__(self)
		self.sendCount=''
		self.sendInterval=''
		self.clearInterval=''
		self.clearWait=''

class incidentPatternBasedCase(incidentTimeBasedCase):
	def __init__(self):
		incidentTimeBasedCase.__init__(self)
		self.clearEvent=''
		self.clearCount=''

class reportCase(TestCase):
	def __init__(self):
		TestCase.__init__(self)
		self.verifyTasks=[]

class linuxFileMonitorCase(TestCase):
	def __init__(self):
		TestCase.__init__(self)
		self.resultOption=''
		self.parameters=''
		self.tasks=[]

class task:
	def __init__(self):
		self.taskName=''
		self.taskType=''
		self.targetPath=''
		self.target=''
		self.recurse=''
		self.excuteUser=''

class RbacProfile:
	def __init__(self):
		self.name=''
		self.description=''
		self.config=''
		self.eventFilter=''

class eventFilter:
	def __init__(self):
		self.name=''
		self.singleConstraint=''
		self.groupConstraint=''
		self.groupBy=''
		self.index=''
		self.singleConditions=[]
		self.groupConditions=[]

class domain:
	def __init__(self):
		self.name=''
		self.domainId=''
		self.companyName=''
		self.description=''
		self.primaryContactUser=''
		self.secondaryContactUser=''
		self.initialized=True
		self.lastDataDistributedTime=''
		self.timeZoneOffset=''
		self.logoURL=''
		self.encKey=''
		self.disabled=False
		self.custKey=''
		self.includeRange=''
		self.excludeRange=''
		self.address=''
		self.phone=''
		self.collectors=[]






