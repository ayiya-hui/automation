from pickClass import pickleClass
import XMLHelper
from appHandler import appHandler

class customer(pickleClass):
    def __init__(self):
        self.custId=''
        self.name=''
        self.fullName=''
        self.description=''
        self.adminUser=''
        self.adminPwd=''
        self.adminEmail=''
        self.eventCollectorId=''
        self.svcUser=''
        self.svcPwd=''
        self.includeRange=''
        self.excludeRange=''
        self.address=''
        self.phone=''
        self.custResource=''
        self.collectors=[]

class custResource(pickleClass):
    def __init__(self):
        self.targetCustId=''
        self.diskQuote=''
        self.eps=''
        self.configItem=''
        self.startTime=''
        self.endTime=''
        self.duration=''
        self.registered=''

class domain:
    def __init__(self):
        self.domainId=''
        self.name=''
        self.initialized=''
        self.includeRange=''
        self.excludeRange=''
        self.collectors=[]

