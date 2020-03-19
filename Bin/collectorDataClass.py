from pickClass import pickleClass
from appHandler import appHandler
import XMLHelper
import xml.dom.minidom as dom
from randomGen import getRandomDecimal, getRandomNum

REG='registration'
COL='eventCollector'
UPDATE='phoenixSystem'
REGISTER='register?requestId='
COLLECTOR_UPDATE='mgmt/collector/infoUpdate'

class eventCollector(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=''
        self.attribute['lastModified']=''
        self.attribute['creationTime']=''
        self.name=''
        self.description=''
        self.agentId=''
        self.collectorId=''
        self.version=''
        self.deviceType=''
        self.naturalId=''
        self.status=''
        self.startTime=''
        self.endTime=''
        self.eps=''
        self.registered=''
        self.ipAddr=''







class deviceType(pickleClass):
    def __init__(self):
        self.vendor=''
        self.model=''
        self.version=''
        self.assetCategory=''
        self.assetWeight=''
        self.category=''
        self.services=''
        self.description=''
        self.objectGroup=''
        self.bizSvcGroup=''
        self.accessProtocols=''
        self.eventParsed=''
        self.priority=''
        self.sysDefined=''







if __name__=='__main__':
    myCol=eventCollector()
    myCol.name='autoCollector'
    myCol.agentId='10000'
    myCol.collectorId='10000'
    myCol.eps=2000
    myCol.naturalId='96649175928'
    myCol.registered='true'
    myCol.status='true'
    myCol.collectorRegister('192.168.20.116')
    print 'done'
