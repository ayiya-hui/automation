from appHandler import appHandler
import XMLHelper
import deviceDataClass
import classToHash
from randomGen import getRandomIPAddr
import xml.dom.minidom as dom
from createDeviceHandler import createDeviceHandler
import sendEvent
import time, datetime
import generalUtility

APP='applications'
DEV='devices'
DEVTYPE='deviceTypes'
DEVICE_QUERY='config/device'
APP_QUERY='config/application'
DEVICETYPE_QUERY='config/deviceType'
APPLICABLE_DEV='deviceInfo/applicableDevices?custId=1'
APPLICABLE='applicableDevices'
LIST='list'
DISCOVERED='discovered/discover?sync=true'
APP_SNMP='AppSNMP'
IPACCESS_ADD='ipaccessmapping/add'
DEFAULT_SNMP_METHOD='SNMP_Public'
IPACCESS_WRAP='ipAccessMappings'
DISCOVER_RUN='discovery/run'
DISCOVERY_RANGES='discoveryIpRanges'
DOMAIN_CONTROLLER_MSG='<13>$time $ip MSWinEventLog    1    Security    9162    $fullTime   673    Security    SYSTEM    User    Success Audit    SJQAVWINADS    Account Logon        Service Ticket Request:     User Name: PARTHA_LAPTOP$@PROSPECT-HILLS.NET     User Domain: PROSPECT-HILLS.NET     Service Name: krbtgt     Service ID: %{S-1-5-21-3383442562-1768178646-255068551-502}     Ticket Options: 0x60810010     Ticket Encryption Type: 0x17     Client Address: 192.168.20.33     Failure Code: -     Logon GUID: {7bf641ec-0dcb-7718-cefa-3ba07f269654}     Transited Services: -        8604'

class deviceHandler:
    def __init__(self, appServer, user=False, password=False):
        self.appHandler=appHandler(appServer, user=user, password=password)
        self.createDeviceHandler=createDeviceHandler()

    def getDeviceType(self, id):
        self.appHandler.getData(DEVICETYPE_QUERY, arg=id)
        deviceType=XMLHelper.unpickleXml(self.appHandler.xml, DEVTYPE, type=LIST)
        myHash=classToHash.classToHash(deviceType[0])

        return myHash

    def getAllDevices(self, app=False):
        tagName=''
        if app:
            self.appHandler.getData(APP_QUERY)
            tagName=APP
        else:
            self.appHandler.getData(DEVICE_QUERY)
            tagName=DEV
        devices=XMLHelper.unpickleXml(self.appHandler.xml, tagName, type=LIST)
        deviceData={}
        for dev in devices:
            myHash=classToHash.classToHash(dev)
            if app==APP_SNMP:
                key=dev.accessIp+' '+dev.name
            else:
                key=dev.accessIp
            deviceData[key]=myHash

        return deviceData

    def getApplicableDevices(self):
        self.appHandler.getData(APPLICABLE_DEV)
        applicableDevs=XMLHelper.unpickleXml(self.appHandler.xml, APPLICABLE)

        return applicableDevs

    def isDeviceExist(self, accessIp, name=False, app=False):
        devices=self.getAllDevices(app)
        if name:
            myKey=accessIp+'_'+name
        else:
            myKey=accessIp
        self.devStat=deviceStatus()
        if myKey in devices.keys():
            dev=devices[myKey]
            devType=False
            if dev['deviceType']!='':
                devType=self.getDeviceType(dev['deviceType'].split('@')[-1])
            self.devStat.exist=True
            self.devStat.id=dev['attribute']['id']
            self.devStat.detail['accessIp']=dev['accessIp']
            self.devStat.detail['creationMethod']=dev['creationMethod']
            self.devStat.detail['name']=dev['name']
            if devType:
                self.devStat.detail['model']=devType['model']
                self.devStat.detail['vendor']=devType['vendor']
                self.devStat.detail['version']=devType['version']

        return self.devStat

    def createDevice(self, deviceIp, deviceName, deviceType, dataCollector=False):
        inXml=self.createDeviceHandler.createDevice(deviceIp, deviceName, deviceType)
        self.appHandler.putData(DISCOVERED, inXml)
        if dataCollector:
            myDict={}
            now=datetime.datetime.now()
            myDict['$time']=now.strftime("%b %d %H:%M:%S")
            myDict['$ip']=deviceIp
            myDict['$fullTime']=now.strftime("%a %b %d %H:%M:%S %Y")
            sendMsg=generalUtility.multiReplace(DOMAIN_CONTROLLER_MSG, myDict)
            print sendMsg
            time.sleep(60)
            mySendHandler=sendEvent.sendEventHandler('syslog', dataCollector)
            mySendHandler.sendoutEvent(sendMsg)
            time.sleep(60)

    def createRandomDevices(self, deviceType, number):
        inXml=self.createDeviceHandler.createRandomDevices(self, deviceType, number)
        self.appHandler.putData(DISCOVERED, node.toxml())

    def discoveryDevice(self, ip, type=False):
        ipAccessList=[]
        ipAccess=deviceDataClass.ipAccessMapping()
        ipAccess.ipRange=ip
        if type:
            ipAccessMethod=type
        else:
            ipAccessMethod=DEFAULT_SNMP_METHOD
        ipAccessList.append(ipAccess)
        node=XMLHelper.pickle(root=ipAccessList, fabric=dom.Document(), elementName=IPACCESS_WRAP)
        self.appHandler.putData(IPACCESS_ADD, node.toxml())
        discoveryRanges=[]
        discoveryRange=deviceDataClass.discoveryIpRange()
        discoveryRange.name='Discovery'+ip
        discoveryRange.includeRange=ip
        discoveryRanges.append(discoveryRange)
        node1=XMLHelper.pickle(root=discoveryRanges, fabric=dom.Document(), elementName=DISCOVERY_RANGES)
        self.appHandler.putData(DISCOVER_RUN, node1.toxml())


class deviceStatus:
    def __init__(self):
        self.exist=False
        self.id=''
        self.detail={}
