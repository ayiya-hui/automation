import autoTestClass
import topEdgeDataClass
import roleDataClass
import deviceDataClass
import custDataClass
import deviceTestClass
import eventDataClass
import eventParsingTestClass
import incidentTestClass
import phoenixDataClass
import collectorDataClass
import perfTestClass
import userDataClass
import approvedDeviceDataClass
import entityValueDataClass
import devicePropertyDataClass
import notificationDataClass
import cmdbDataClass
import definitionDataClass

def getClassInstance(classType):
    myObj=''
    if classType=='Report':
        myObj=definitionDataClass.Report()
    elif classType=='CustomerScope':
        myObj=definitionDataClass.CustomerScope()
    elif classType=='Include':
        myObj=definitionDataClass.Include()
    elif classType=='PatternClause':
        myObj=definitionDataClass.PatternClause()
    elif classType=='SubPattern':
        myObj=definitionDataClass.SubPattern()
    elif classType=='SelectClause':
        myObj=definitionDataClass.SelectClause()
    elif classType=='OrderByClause':
        myObj=definitionDataClass.OrderByClause()
    elif classType=='ReportInterval':
        myObj=definitionDataClass.ReportInterval()
    elif classType=='Window':
        myObj=definitionDataClass.Window()
    elif classType=='Rule':
        myObj=definitionDataClass.Rule()
    elif classType=='rule':
        myObj=cmdbDataClass.rule()
    elif classType=='eventFilters':
        myObj=cmdbDataClass.eventFilters()
    elif classType=='IncidentDef':
        myObj=definitionDataClass.IncidentDef()
    elif classType=='Operator':
        myObj=definitionDataClass.Operator()
    elif classType=='TriggerEventDisplay':
        myObj=definitionDataClass.TriggerEventDisplay()
    elif classType=='ClearCondition':
        myObj=definitionDataClass.ClearCondition()
    elif classType=='ClearIncidentDef':
        myObj=definitionDataClass.ClearIncidentDef()
    elif classType=='event':
        myObj=eventDataClass.event()
    elif classType=='attribute':
        myObj=eventDataClass.attribute()
    elif classType=='deviceTestSuite':
        myObj=deviceTestClass.deviceTestSuite()
    elif classType=='deviceTestCase':
        myObj=deviceTestClass.deviceTestCase()
    elif classType=='testData':
        myObj=deviceTestClass.testData()
    elif classType=='eventParsingData':
        myObj=deviceTestClass.eventParsingData()
    elif classType=='incidentData':
        myObj=deviceTestClass.incidentData()
    elif classType=='logDiscoveryData':
        myObj=deviceTestClass.logDiscoveryData()
    elif classType=="device":
        myObj=deviceDataClass.device()
    elif classType=="application":
        myObj=deviceDataClass.device()
    elif classType=='ipAccessMapping':
        myObj=deviceDataClass.ipAccessMapping()
    elif classType=='domain':
        myObj=custDataClass.domain()
    elif classType=="logDiscoverySuite":
        myObj=autoTestClass.logDiscoverySuite()
    elif classType=="logDiscoveryCase":
        myObj=autoTestClass.logDiscoveryCase()
    elif classType=="RBACSuite":
        myObj=autoTestClass.RBACSuite()
    elif classType=="RBACCase":
        myObj=autoTestClass.RBACCase()
    elif classType=="eventExportSuite":
        myObj=autoTestClass.eventExportSuite()
    elif classType=="eventExportCase":
        myObj=autoTestClass.eventExportCase()
    elif classType=="eventParsingSuite":
        myObj=eventParsingTestClass.eventParsingSuite()
    elif classType=="eventParsingCase":
        myObj=eventParsingTestClass.eventParsingCase()
    elif classType=="eventTypeSuite":
        myObj=autoTestClass.eventTypeSuite()
    elif classType=="eventTypeCase":
        myObj=autoTestClass.eventTypeCase()
    elif classType=="incidentSuite":
        myObj=incidentTestClass.incidentSuite()
    elif classType=="incidentCase":
        myObj=incidentTestClass.incidentCase()
    elif classType=="incidentEvent":
        myObj=incidentTestClass.incidentEvent()
    elif classType=="reportSuite":
        myObj=autoTestClass.reportSuite()
    elif classType=="reportCase":
        myObj=autoTestClass.reportCase()
    elif classType=="linuxFileMonitorSuite":
        myObj=autoTestClass.linuxFileMonitorSuite()
    elif classType=="linuxFileMonitorCase":
        myObj=autoTestClass.linuxFileMonitorCase()
    elif classType=="linuxUser":
        myObj=autoTestClass.linuxUser()
    elif classType=="task":
        myObj=autoTestClass.task()
    elif classType=="setupTask":
        myObj=autoTestClass.setupTask()
    elif classType=="createDevice":
        myObj=autoTestClass.createDevice()
    elif classType=="readEventType":
        myObj=autoTestClass.readEventType()
    elif classType=="sentEvent":
        myObj=autoTestClass.sentEvent()
    elif classType=="event":
        myObj=autoTestClass.event()
    elif classType=="sentIncident":
        myObj=autoTestClass.sentIncident()
    elif classType=="incident":
        myObj=autoTestClass.incident()
    elif classType=="reportQuery":
        myObj=autoTestClass.reportQuery()
    elif classType=="eventTypeQuery":
        myObj=autoTestClass.eventTypeQuery()
    elif classType=="RbacProfile":
        myObj=autoTestClass.RbacProfile()
    elif classType=="eventFilter":
        myObj=autoTestClass.eventFilter()
    elif classType=='topoEdge':
        myObj=topEdgeDataClass.topoEdge()
    elif classType=='topoNode':
        myObj=topEdgeDataClass.topoNode()
    elif classType=='Role':
        myObj=roleDataClass.Role()
    elif classType=='Config':
        myObj=roleDataClass.Config()
    elif classType=='profile':
        myObj=roleDataClass.profile()
    elif classType=='groupNode':
        myObj=roleDataClass.groupNode()
    elif classType=='action':
        myObj=roleDataClass.action()
    elif classType=='eventCollector':
        myObj=collectorDataClass.eventCollector()
    elif classType=='phoenixSystem':
        myObj=phoenixDataClass.phoenixSystem()
    elif classType=='perfTestSuite':
        myObj=perfTestClass.perfTestSuite()
    elif classType=='perfTestCase':
        myObj=perfTestClass.perfTestCase()
    elif classType=='user':
        myObj=userDataClass.user()
    elif classType=='applicableDevices':
        myObj=approvedDeviceDataClass.applicableDevices()
    elif classType=='approvedDevice':
        myObj=approvedDeviceDataClass.approvedDevice()
    elif classType=='entityValue':
        myObj=entityValueDataClass.entityValue()
    elif classType=='deviceProperties':
        myObj=devicePropertyDataClass.deviceProperties()
    elif classType=='property':
        myObj=devicePropertyDataClass.property()
    elif classType=='notificationPolicy':
        myObj=notificationDataClass.notificationPolicy()
    elif classType=='notificationAction':
        myObj=notificationDataClass.notificationAction()
    elif classType=='notificationCondition':
        myObj=notificationDataClass.notificationCondition()
    elif classType=='eventAttributeType':
        myObj=cmdbDataClass.eventAttributeType()
    elif classType=='applicationPackage':
        myObj=cmdbDataClass.applicationPackage()
    elif classType=='customer':
        myObj=cmdbDataClass.customer()
    elif classType=='service':
        myObj=cmdbDataClass.service()
    elif classType=='deviceType':
        myObj=cmdbDataClass.deviceType()
    elif classType=='eventParser':
        myObj=cmdbDataClass.eventParser()
    elif classType=='parser':
        myObj=cmdbDataClass.parser()
    elif classType=='eventType':
        myObj=cmdbDataClass.eventType()
    elif classType=='group':
        myObj=cmdbDataClass.group()
    elif classType=='malwareSite':
        myObj=cmdbDataClass.malwareSite()
    elif classType=='widget':
        myObj=cmdbDataClass.widget()
    elif classType=='dataProvider':
        myObj=cmdbDataClass.dataProvider()
    elif classType=='eventCode':
        myObj=cmdbDataClass.eventCode()
    elif classType=='deviceEventAttribute':
        myObj=cmdbDataClass.deviceEventAttribute()
    elif classType=='query':
        myObj=cmdbDataClass.query()
    elif classType=='bizService':
        myObj=cmdbDataClass.bizService()
    elif classType=='vulnerability':
        myObj=cmdbDataClass.vulnerability()


    return myObj
