class applicationPackage:
    def __init__(self):
        self.name=''
        self.appGroupName=''
        self.pkgSignature=''
        self.processName=''
        self.processParam=''
        self.serviceString=''
        self.objectGroup=''
        self.priority=''

class eventAttributeType:
    def __init__(self):
        self.attribute={}
        self.attribute['attributeId']=''
        self.categories=''
        self.deprecated=''
        self.description=''
        self.displayName=''
        self.name=''
        self.usedByRbac=''
        self.valueType=''
        self.formatType=''

class customer:
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=''
        self.name=''
        self.fullName=''
        self.description=''
        self.adminUser=''
        self.adminPwd=''
        self.adminEmail=''
        self.svcUser=''
        self.svcPwd=''

class service:
    def __init__(self):
        self.name=''
        self.portList=''
        self.description=''

class monitorTemplate:
    def __init__(self):
        self.name=''
        self.sysDefined=''
        self.items=[]
        self.deviceTypes=[]

class monitorTemplateItem:
    def __init__(self):
        self.perObject=''
        self.template=''

class deviceType:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.accessProtocols=''
        self.bizSvcGroup=''
        self.type=''
        self.eventParsed=''
        self.model=''
        self.objectGroup=''
        self.priority=''
        self.services=''
        self.sysDefined=''
        self.vendor=''
        self.version=''

class eventParser:
    def __init__(self):
        self.attribute={}
        self.attribute['name']=''
        self.attribute['enabled']='true'
        self.attribute['sysDefined']='true'
        self.parserXml=''
        self.deviceType=''
        self.priority=''

class parser:
    def __init__(self):
        self.name=''
        self.priority=''

class eventType:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.description=''
        self.deviceType=''
        self.displayName=''
        self.name=''
        self.severity=''
        self.sysDefined=''
        self.systemType=''
        self.group=''

class group:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.attribute['type']=''
        self.attribute['name']=''
        self.displayName=''
        self.displayOrder=''
        self.parent=''

class rule:
    def __init__(self):
        self.attribute={}
        self.attribute['dataCreationType']=''
        self.attribute['dataChangeType']=''
        self.attribute['naturalId']=''
        self.attribute['entityVersion']=''
        self.attribute['xmlId']=''
        self.attribute['ownerId']=''
        self.attribute['lastModified']=''
        self.attribute['id']=''
        self.attribute['custId']=''
        self.attribute['creationTime']=''
        self.attribute['phIncidentCategory']=''
        self.activatedTime=''
        self.custInclusive=''
        self.description=''
        self.eventFilters=[]
        self.name=''
        self.triggerWindow=''
        self.advanced=''
        self.incidentAttrs=''
        self.incidentFireFreq=''
        self.incidentFired=''
        self.incidentType=''
        self.triggerEventAttrList=''
        self.group=''

class eventFilters:
    def __init__(self):
        self.attribute={}
        self.attribute['entityVersion']=''
        self.attribute['xmlId']=''
        self.attribute['ownerId']=''
        self.attribute['lastModified']=''
        self.attribute['id']=''
        self.attribute['custId']=''
        self.attribute['creationTime']=''
        self.groupBy=''
        self.groupConstraint=''
        self.index=''
        self.name=''
        self.singleConstraint=''

class malwareSite:
    def __init__(self):
        self.domainName=''

#have to handle both format from data-definition and rest API
class widget:
    def __init__(self):
        self.attribute={}
        self.attribute['group']=''
        self.attribute['naturalId']=''
        self.attribute['id']=''
        self.dataParam=''
        self.dataProvider=''
        self.dataProviderId=''
        self.dataProviderType=''
        self.description=''
        self.height=''
        self.name=''
        self.poxX=''
        self.poxY=''
        self.width=''
        self.name=''

#for data-definition only
class dataProvider:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.attribute['type']=''

class eventCode:
    def __init__(self):
        self.code=''
        self.description=''
        self.eventAttributeType=''

class deviceEventAttribute:
    def __init__(self):
        self.attrNameList=''
        self.deviceType=''
        self.eventType=''

class query:
    def __init__(self):
        self.attribute={}
        self.attribute['naturalId']=''
        self.attribute['entityVersion']=''
        self.attribute['xmlId']=''
        self.attribute['ownerId']=''
        self.attribute['lastModified']=''
        self.attribute['id']=''
        self.attribute['custId']=''
        self.attribute['creationTime']=''
        self.active=''
        self.custInclusive=''
        self.description=''
        self.eventFilters=[]
        self.name=''
        self.triggerWindow=''
        self.dataCreationType=''
        self.orderByClause=''
        self.inline=''
        self.internalUse=''
        self.relevantFilterAttr=''
        self.reportWindow=''
        self.reportWindowUnit=''
        self.selectClause=''
        self.timeRangeRelative=''
        self.group=''

class bizService:
    def __init__(self):
        self.attribute={}
        self.attribute['group']=''
        self.attribute['id']=''
        self.attribute['xmlId']=''
        self.name=''

class vulnerability:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.bugId=''
        self.cveCode=''
        self.vendorBugId=''
        self.description=''
        self.eventType=''
        self.affectedSoftwares=[]

class affectedSoftware:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.fixDate=''
        self.fixVersion=''
        self.osDeviceType=''
        self.osVersion=''
        self.vulnerability=''
        self.patches=''
        self.appModel=''
        self.appVendor=''
        self.appVersion=''







