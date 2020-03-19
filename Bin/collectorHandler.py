from appHandler import appHandler
import timeUtility
import xml.dom.minidom as dom
import XMLHelper
from pickClass import pickleClass
from custHandler import custHandler
from configHandler import configHandler
from randomGen import getRandomDecimal, getRandomNum

REG='registration'
COL='eventCollector'
UPDATE='phoenixSystem'
REGISTER='register?requestId='
COLLECTOR_UPDATE='mgmt/collector/statusUpdate'
COLLECTOR_QUERY='config/eventCollector'
LIST='list'
EVENT_COLLECTOR='eventCollectors'
PWD='Prospect@Hi123'

class collectorHandler:
    def __init__(self, appServer):
        self.appServer=appServer
        self.appHandler=appHandler(appServer)
        myConfigHand=configHandler(appServer)
        self.version=myConfigHand.getVersion()
        self.collectors=[]
        self.customers=[]

    def getAllCollectors(self):
        self.appHandler.getData(COLLECTOR_QUERY)
        self.collectors=XMLHelper.unpickleXml(self.appHandler.xml, EVENT_COLLECTOR, type=LIST)

    def getAllCustomers(self):
        myCust=custHandler(self.appServer)
        self.customers=myCust.getCustomer()

    def getCustNamebyCollector(self, collectorName, customers):
        custName=''
        for cust in customers:
            if hasattr(cust, 'collectors'):
                for col in cust.collectors:
                    if col.name==collectorName:
                        custName=cust.name

        return custName

    def collectorRegister(self, custName, collector):
        myReg=registration()
        myReg.domainName=custName
        myReg.collectorName=collector.name
        myReg.collectorId=custName+'/admin'
        myReg.password='admin*1'
        myReg.appServer=self.appServer
        myReg.attribute['requestId']=collector.collectorId
        myReg.uniqueId=collector.collectorId
        self.appHandler.putData(REGISTER+myReg.attribute['requestId'], self.createXml(myReg, REG))

    def collectorUpdate(self, custName, collector):
        myStatusList=[]
        myStatus=collectorStatus()
        myStatus.version=self.version
        myStatus.buildDate=int(int(collector.attribute['creationTime'])/1000)
        myStatus.collectorId=collector.collectorId
        myStatus.custId=collector.attribute['custId']
        myStatus.status='up'
        myStatus.lastStatusTime=timeUtility.getUTimeNow()
        print myStatus.lastStatusTime
        myDiskIOs=[]
        myDiskIO=DiskIO()
        myDiskIO.attribute['name']='sda'
        myDiskIOs.append(myDiskIO)
        myCPUs=[]
        myCPU=CPU()
        myCPU.attribute['id']='0'
        myCPUs.append(myCPU)
        myCPU1=CPU()
        myCPU1.attribute['id']='1'
        myCPUs.append(myCPU1)
        myDisks=[]
        myDisk=Disk()
        myDisk.attribute['name']='/dev/sda3'
        myDisks.append(myDisk)
        myDisk1=Disk()
        myDisk1.attribute['name']='/dev/sda1'
        myDisks.append(myDisk1)
        myDisk2=Disk()
        myDisk2.attribute['name']='tmpfs'
        myDisks.append(myDisk2)
        mySwaps=[]
        mySwap=Swap()
        mySwaps.append(mySwap)
        myStatus.DiskIOs=myDiskIOs
        myStatus.CPUs=myCPUs
        myStatus.Disks=myDisks
        myStatus.Swaps=mySwaps
        myStatus.memUtil=str(getRandomDecimal(1, 100))
        myStatus.upTime=str(getRandomDecimal(100, 100000))
        myStatus.cpuUtil=str(getRandomDecimal(1, 100))
        myStatus.ipAddr=collector.ipAddr
        myStatus.collectorName=collector.name
        myStatus.healthStatus='normal'
        myStatusList.append(myStatus)
        myHand=appHandler(self.appServer, user=collector.collectorId, password=PWD)
        myHand.putData(COLLECTOR_UPDATE, self.createXml(myStatusList, UPDATE))

    def createXml(self, obj, eName):
        node=XMLHelper.pickle(root=obj, fabric=dom.Document(), elementName=eName)
        return node.toxml()

    def autoWork(self, type):
        if not len(self.collectors):
            self.getAllCollectors()
        if not len(self.customers):
            self.getAllCustomers()
        for collector in self.collectors:
            if 'AutoCollector' in collector.name:
                custName=self.getCustNamebyCollector(collector.name, self.customers)
                if type=='register':
                    self.collectorRegister(custName, collector)
                elif type=='update':
                    self.collectorUpdate(custName, collector)

class registration(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['requestId']=''
        self.collectorName=''
        self.domainName=''
        self.password=''
        self.collectorId=''
        self.uniqueId=''
        self.appServer=''

class collectorStatus(pickleClass):
    def __init__(self):
        self.custName=''
        self.collectorName=''
        self.ipAddr=''
        self.status=''
        self.healthStatus=''
        self.upTime=''
        self.cpuUtil=''
        self.memUtil=''
        self.lastStatusTime=''
        self.lastPerfData=''
        self.version=''
        self.upgradeVersion=''
        self.installStatus=''
        self.downloadStatus=''
        self.buildDate=''
        self.collectorId=''
        self.custId=''
        self.DiskIOs=[]
        self.CPUs=[]
        self.Disks=[]
        self.Swaps=[]

class DiskIO(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['name']=''
        self.attribute['rps']=getRandomDecimal(1, 10)
        self.attribute['wps']=getRandomDecimal(1, 10)
        self.attribute['rkbps']=getRandomDecimal(1, 100)
        self.attribute['wkbps']=getRandomDecimal(1, 200)
        self.attribute['latency']=getRandomDecimal(1, 10)
        self.attribute['appLatency']=getRandomDecimal(1, 10)
        self.attribute['util']=getRandomDecimal(1, 10)

class CPU(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.attribute['load']=getRandomNum(1, 10)

class Disk(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['name']=''
        self.attribute['used']=getRandomNum(1000000, 3000000)
        self.attribute['total']=getRandomNum(30000000, 90000000)

class Swap(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['size']=getRandomNum(5000000, 9000000)
        self.attribute['used']=getRandomNum(0, 5000000)

if __name__=='__main__':
    myHandler=collectorHandler('192.168.20.37:8181')
    #myHandler.autoWork('register')
    myHandler.autoWork('update')


    print 'Done'

