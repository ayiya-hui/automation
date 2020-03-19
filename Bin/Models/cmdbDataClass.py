class applicationPackage:
    """This class is for applicationPacket in CMDB."""
    def __init__(self):
        self.name=None
        self.appGroupName=None
        self.pkgSignature=None
        self.processName=None
        self.processParam=None
        self.serviceString=None
        self.objectGroup=None
        self.priority=None

class application:
    """This class is for application in CMDB."""
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.accessIp=None
        self.appPackage=None
        self.creationMethod=None
        self.device=None
        self.deviceType=None
        self.name=None
        self.updateMethod=None
        self.version=None

class eventAttributeType:
    """This class is for eventAttributeType in CMDB."""
    def __init__(self):
        self.attribute={}
        self.attribute['attributeId']=None
        self.categories=None
        self.deprecated=None
        self.description=None
        self.displayName=None
        self.name=None
        self.usedByRbac=None
        self.valueType=None
        self.formatType=None

class customer:
    """This class is for customer in CMDB."""
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=None
        self.name=None
        self.fullName=None
        self.description=None
        self.adminUser=None
        self.adminPwd=None
        self.adminEmail=None
        self.svcUser=None
        self.svcPwd=None

class service:
    """This class is for service in CMDB."""
    def __init__(self):
        self.name=None
        self.portList=None
        self.description=None

class monitorTemplate:
    """This class is for monitorTemplate in CMDB."""
    def __init__(self):
        self.name=None
        self.sysDefined=None
        self.items=[]
        self.deviceTypes=[]

class monitorTemplateItem:
    """This class is for monitorTemplateItem in CMDB."""
    def __init__(self):
        self.perObject=None
        self.template=None

class deviceType:
    """This class is for deviceType in CMDB."""
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.accessProtocols=None
        self.bizSvcGroup=None
        self.model=None
        self.services=None
        self.sysDefined=None
        self.vendor=None
        self.version=None
        self.category=None

class eventParser:
    """This class is for eventParser in CMDB."""
    def __init__(self):
        self.attribute={}
        self.attribute['name']=None
        self.attribute['enabled']='true'
        self.attribute['sysDefined']='true'
        self.parserXml=None
        self.deviceType=None
        self.priority=None

class parser:
    """This class is for parser in CMDB."""
    def __init__(self):
        self.name=None
        self.priority=None

class eventType:
    """This class is for eventType in CMDB."""
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.description=None
        self.deviceType=None
        self.displayName=None
        self.name=None
        self.severity=None
        self.sysDefined=None
        self.systemType=None
        self.group=None

class group:
    """This class is for group in CMDB."""
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.attribute['type']=None
        self.attribute['name']=None
        self.displayName=None
        self.displayOrder=None
        self.collectorId=None
        self.description=None
        self.parent=None

class rule:
    """This class is for rule in CMDB."""
    def __init__(self):
        self.attribute={}
        self.attribute['dataCreationType']=None
        self.attribute['dataChangeType']=None
        self.attribute['naturalId']=None
        self.attribute['entityVersion']=None
        self.attribute['xmlId']=None
        self.attribute['ownerId']=None
        self.attribute['lastModified']=None
        self.attribute['id']=None
        self.attribute['custId']=None
        self.attribute['creationTime']=None
        self.attribute['phIncidentCategory']=None
        self.activatedTime=None
        self.active=None
        self.custInclusive=None
        self.description=None
        self.eventFilters=[]
        self.name=None
        self.triggerWindow=None
        self.advanced=None
        self.incidentAttrs=None
        self.incidentFireFreq=None
        self.incidentFired=None
        self.incidentType=None
        self.triggerEventAttrList=None
        self.group=None
        self.filterOperators=filterOperators()
        self.globalConstraint=None
        self.rawFOString=None
        self.phEventCategory=None
        self.fireInternalIncident=None
        self.category=None

class eventFilters:
    """This class is for eventFilters in CMDB."""
    def __init__(self):
        self.attribute={}
        self.attribute['entityVersion']=None
        self.attribute['xmlId']=None
        self.attribute['ownerId']=None
        self.attribute['lastModified']=None
        self.attribute['id']=None
        self.attribute['custId']=None
        self.attribute['creationTime']=None
        self.groupBy=None
        self.groupConstraint=None
        self.index=None
        self.name=None
        self.singleConstraint=None

class filterOperators:
    """This class is for filterOperators in CMDB."""
    def __init__(self):
        self.rank=None
        self.type=None

class clearCondition:
    """This class is for clearCondition in CMDB."""
    def __init__(self):
        self.attribute={}
        self.attribute['ruleNaturalId']=None
        self.clearOption=None
        self.clearTimeWindow=None
        self.clearEventFilters=None

class eventFilter:
    """This class if or event filter inside clearCondtion."""
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.groupBy=None
        self.singleConstraint=None
        self.groupConstraint=None
        self.name=None

class malwareSite:
    """This class is for malwareSite in CMDB."""
    def __init__(self):
        self.domainName=None

#have to handle both format from data-definition and rest API
class widget:
    """This class is for widget in CMDB."""
    def __init__(self):
        self.attribute={}
        self.attribute['group']=None
        self.attribute['naturalId']=None
        self.attribute['id']=None
        self.dataParam=None
        self.dataProvider=dataProvider()
        self.dataProviderId=None
        self.dataProviderType=None
        self.description=None
        self.height=None
        self.name=None
        self.posX=None
        self.posY=None
        self.width=None
        self.name=None

#for data-definition only
class dataProvider:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.attribute['type']=None

class eventCode:
    def __init__(self):
        self.code=None
        self.description=None
        self.eventAttributeType=None

class deviceEventAttribute:
    def __init__(self):
        self.attrNameList=None
        self.deviceType=None
        self.eventType=None

class query:
    def __init__(self):
        self.attribute={}
        self.attribute['naturalId']=None
        self.attribute['entityVersion']=None
        self.attribute['xmlId']=None
        self.attribute['ownerId']=None
        self.attribute['lastModified']=None
        self.attribute['id']=None
        self.attribute['custId']=None
        self.attribute['creationTime']=None
        self.active=None
        self.custInclusive=None
        self.description=None
        self.eventFilters=[]
        self.name=None
        self.triggerWindow=None
        self.dataCreationType=None
        self.orderByClause=None
        self.inline=None
        self.internalUse=None
        self.relevantFilterAttr=None
        self.reportWindow=None
        self.reportWindowUnit=None
        self.selectClause=None
        self.timeRangeRelative=None
        self.group=None

class bizService:
    def __init__(self):
        self.attribute={}
        self.attribute['group']=None
        self.attribute['id']=None
        self.attribute['xmlId']=None
        self.name=None

class vulnerability:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.bugId=None
        self.cveCode=None
        self.vendorBugId=None
        self.description=None
        self.eventType=None
        self.affectedSoftwares=[]

class affectedSoftware:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.fixDate=None
        self.fixVersion=None
        self.osDeviceType=None
        self.osVersion=None
        self.vulnerability=None
        self.patches=None
        self.appModel=None
        self.appVendor=None
        self.appVersion=None

class rbacProfile:
    def __init__(self):
        self.attribute={}
        self.attribute['naturalId']=None
        self.config=None
        self.description=None
        self.eventFilter=eventFilter()
        self.name=None

class device:
    def __init__(self):
        self.organization=organization()
        self.accessIp=None
        self.approved=None
        self.contact=None
        self.creationMethod=None
        self.description=None
        self.deviceType=None
        self.discoverMethod=None
        self.discoverTime=None
        self.hwModel=None
        self.hwSerialNum=None
        self.location=None
        self.name=None
        self.systemUptime=None
        self.updateMethod=None

class organization:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.attribute['name']=None


class MaintSchedule:
    def __init__(self):
        self.name=None
        self.description=None
        self.devices=[]
        self.groups=[]
        self.fireIncident=None
        self.schedule=schedule()

class schedule:
    def __init__(self):
        self.startHour=None
        self.startMin=None
        self.duration=None
        self.timeZhone=None
        self.startDate=None
        self.endDate=None
        self.endDateOpen=None
        self.daysOfWeek=None
        self.daysOfMonth=None
        self.monthsOfYear=None

class accessConfigs:
    def __init__(self):
        self.ipAccessMethods=[]
        self.ipAccessMappings=[]

class accessMethod:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.accessProtocol=None
        self.baseDN=None
        self.description=None
        self.name=None
        self.port=None
        self.pullInterval=None
        self.credential=credential()
        self.deviceType=deviceType()

class credential:
    def __init__(self):
        self.password=None
        self.principal=None
        self.suPassword=None

class ipAccessMapping:
    def __init__(self):
        self.accessMethodId=None
        self.ipRange=None

class taskResults:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.item=[]

class item:
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=None
        self.attribute['id']=None
        self.ip=None
        self.status=None
        self.discoverTime=None
        self.name=None
        self.vendor=None
        self.model=None
        self.version=None
        self.description=None
        self.accessMethods=None
        self.interfaceCount=None
        self.runningSoftwareCount=None

class event:
    def __init__(self):
        self.attributes=[]
        self.eventType=None
        self.id=None
        self.index=None
        self.receiveTime=None

class attribute:
    def __init__(self):
        self.name=None
        self.value=None

class applicableDevices:
    def __init__(self):
        self.approvedDevicesOnly=None
        self.approvedDevices=[]

class approvedDevice:
    def __init__(self):
        self.hostName=None
        self.accessIp=None

class domain:
    def __init__(self):
        self.domainId=None
        self.name=None
        self.initialized=None
        self.includeRange=None
        self.excludeRange=None
        self.collectors=[]

class eventCollector:
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=None
        self.attribute['lastModified']=None
        self.attribute['creationTime']=None
        self.name=None
        self.description=None
        self.agentId=None
        self.collectorId=None
        self.version=None
        self.deviceType=None
        self.naturalId=None
        self.status=None
        self.startTime=None
        self.endTime=None
        self.eps=None
        self.registered=None
        self.ipAddr=None

class entityValue:
    def __init__(self):
        self.attribute={}
        self.attribute['valueType']=None
        self.attribute['naturalId']=None
        self.attribute['name']=None
        self.attribute['id']=None
        self.attribute['entityType']=None
        self.attribute['custId']=None
        self.namedValues=[]

class phoenixSystem:
    """This class is for phoenixSystem with partial data from CMDB."""
    def __init__(self):
        self.version=None
        self.buildDate=None

class user:
    """This class is for user in CMDB"""
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=None
        self.active=None
        self.description=None
        self.fullName=None
        self.loalAuthen=None
        self.name=None
        self.privileged=None

class perfObject:
    """This class is for perfObject in CMDB"""
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.attribute['custId']=None
        self.desc=None
        self.frequency=None
        self.method=None
        self.naturalId=None
        self.sysDefined=None
        self.type=type()
class type:
    """This class is for type in CMDB"""
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.category=None
        self.displayName=None
        self.name=None

class parser:
    """This class is for REST API call /device/parsers"""
    def __init__(self):
        self.attribute={}
        self.attribute['name']=None
        self.attribute['enabled']=None
        self.attribute['priority']=None
        self.attribute['sysDefined']=None

