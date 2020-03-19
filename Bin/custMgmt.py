from XMLHelper import pickleToXML

class device:
    def __init__(self):
        self.accessIp=''
        self.creationMethond=''
        self.deviceType=''

class userConf(pickleToXML):
    def __init__(self):
        self.custId=''
        self.users=[]

    def fillInfo(self, custId, users):
        self.custId=custId
        self.users=users

class user(pickleToXML):
    def __init__(self):
        self.name=''
        self.naturalId=''
        self.fullName=''
        self.company=''
        self.jobTitle=''
        self.domain=''
        self.dn=''
        self.password=''
        self.privileged='false'
        self.primaryProfile=''
        self.orgs=[]
        self.orgRoleMappings={}
        self.active='true'
        self.contacts=[]
        self.description=''
        self.effectiveCustId=''

    def fillInfo(self,name, naturalId, fullName, company, jobTitle, domain, dn, password, privileged, RbacProfile, orgs, orgRoleMappings, active, contacts, description, effectiveCustId):
        self.name=name
        self.naturalId=naturalId
        self.fullName=fullName
        self.company=company
        self.jobTitle=jobTitle
        self.domain=domain
        self.dn=dn
        self.password=password
        self.privileged=privileged
        self.primaryProfile=RbacProfile
        self.orgs=orgs
        self.orgRoleMappings=orgRoleMappings
        self.active=active
        self.contacts=contacts
        self.description=description
        self.effectiveCustId=effectiveCustId

class contact(pickleToXML):
    def __init__(self):
        self.primary=''
        self.name=''
        self.address=''
        self.address2=''
        self.city=''
        self.state=''
        self.country=''
        self.zip=''
        self.homePhone=''
        self.workPhone=''
        self.mobilePhone=''
        self.email=''
        self.smsProvider=''
        self.smsNumber=''
        self.description=''

    def fillInfo(self,primary,name,address,address2,city,state,country,zip,homePhone,workPhone,mobilePhone,email,smsProvider,smsNumber,description):
        self.primary=primary
        self.name=name
        self.address=address
        self.address2=address2
        self.city=city
        self.state=state
        self.country=country
        self.zip=zip
        self.homePhone=homePhone
        self.workPhone=workPhone
        self.mobilePhone=mobilePhone
        self.email=email
        self.smsProvider=smsProvider
        self.smsNumber=smsNumber
        self.description=description

class RbacProfile(pickleToXML):
    def __init__(self):
        self.name=''
        self.description=''
        self.eventFilter=''
        self.config=''

    def fillInfo(self, name, description, eventFilter, config):
        self.name=name
        self.description=description
        self.eventFilter=eventFilter
        self.config=config

class eventFilter(pickledToXML):
    def __init__(self):
        self.name=''
        self.singleConstraint=''
        self.groupConstraint=''
        self.groupBy=''
        self.index=''
        self.singleConditions=[]
        self.groupConditions=[]

    def fillInfo(self, name, singleConstraint, groupConstraint, groupBy, index, singleConditions, groupConditions):
        self.name=name
        self.singleConstraint=singleConstraint
        self.groupConstraint=groupConstraint


