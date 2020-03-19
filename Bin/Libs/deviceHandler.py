import Util.generalUtility as generalUtility
import Util.hashToClassHelper as hashToClassHelper
import datetime, time
import sendEventHandler
import XmlHandler
from appHandler import appHandler
from restApiDataHandler import restApiDataHandler
from Models.ClassLocator import getClassObj
from ConfigConstants.TestConstant import create_device_param, create_device_domain_controller_msg, create_device_types, create_device_addon
from ConfigConstants.deviceTemplate import *
from string import Template
import randomGen

fix_interface='242.242.%s.%s'

device_types={'juniper-ssg':juniper_ssg_device_xml,
              'cisco_asa':cisco_asa_device_xml,
              'paloalto':paloalto_device_xml,
              'checkpoint':checkpoint_device_xml,
              'juniper':juniper_device_xml,
              }
#'sendmail':sendmail_device_xml,

class deviceHandler:
    """This class will handle all devices related utility in Accelops."""
    def __init__(self, appServer, user=False, password=False):
        self.appHandler=appHandler(appServer, user=user, password=password)
        self.restApiDataHandler=restApiDataHandler(appServer)

    def getAllDevices(self):
        """This method will get all devices."""
        self.devices=self.restApiDataHandler.getData('device')

        return self.devices

    def getAllApps(self):
        self.apps=self.restApiDataHandler.getData('application')

        return self.apps

    def getDeviceByIp(self, accessIp, isApp=False):
        """This method will get a device by IP address."""
        device=''
        if self.isDeviceExist(accessIp, app=isApp):
            if isApp:
                rawdevice=self.apps[accessIp]
                if type(rawdevice).__name__=='list':
                    device=rawdevice[0]
                else:
                    device=rawdevice
            else:
                device=self.devices[accessIp]
        else:
            print 'device %s not exist.' % accessIp

        return device

    def getApplicableDevices(self):
        """This method will get all applicabled devices."""
        params={}
        params['custId']='1'
        self.applicableDevices=self.restApiDataHandler.getData('applicableDevices', noKey=True, module='deviceInfo', arg=params)

    def isDeviceExist(self, accessIp, app=False):
        """This method will check if a device exist in CMDB."""
        data=''
        if app:
            data=self.getAllApps()
        else:
            data=self.getAllDevices()
        if data:
            if accessIp in data.keys():
                return True
            else:
                return False

    def createDevice(self, deviceIp, deviceName, deviceType, perfObj, dataCollector=False):
        """This method will create a device."""
        inXml=''
        if deviceType in device_types.keys():
            device_temp=Template(device_types[deviceType])
            device_map={}
            device_map['device_ip']=deviceIp
            device_map['device_name']=deviceName
            device_map['discover_time']=int(time.mktime(datetime.datetime.now().timetuple()))
            for param in sub_params[deviceType]:
                self.fillParam(device_map, param)

            inXml=device_temp.substitute(device_map)
        else:
            inXml=self.__createDeviceData(deviceIp, deviceName, deviceType, perfObj)
        if inXml:
            self.appHandler.putData(create_device_param, inXml)
        print 'dataCollector: %s' % dataCollector
        if dataCollector:
            myDict={}
            now=datetime.datetime.now()
            myDict['$time']=now.strftime("%b %d %H:%M:%S")
            myDict['$ip']=deviceIp
            myDict['$fullTime']=now.strftime("%a %b %d %H:%M:%S %Y")
            sendMsg=generalUtility.multiReplace(create_device_domain_controller_msg, myDict)
            mySendHandler=sendEventHandler.sendEventHandler('syslog', dataCollector)
            mySendHandler.sendoutEvent(sendMsg)
            time.sleep(60)

    def createRandomDevices(self, deviceType, number, perfObj):
        """This method will create a numbers of random generated devices."""
        inXml=self.__createRandomDevicesData(self, deviceType, number, perfObj)
        self.appHandler.putData(DISCOVERED, node.toxml())

    def __createDeviceData(self, deviceIp, deviceName, deviceType, perfObj, custId='1'):
        deviceData=[]
        map={}
        map['name']=deviceName
        map['type']=deviceType
        map['ip']=deviceIp
        map['custId']=custId
        deviceData.append(map)

        return self.__createDevice(deviceData, perfObj)

    def __createRandomDevicesData(self, deviceType, number, perfObj, custId='1'):
        deviceData=[]
        for i in range(0, number):
            map={}
            map['name']="autoDevice"+deviceType+str(i+1)
            map['type']=deviceType
            map['ip']=randomGen.getRandomIPAddr()
            map['custId']=custId
            deviceData.append(map)

        return self.__createDevice(deviceData, perfObj)

    def __createDevice(self, deviceData, perfObj):
        myDeviceList=[]
        for device in deviceData:
            if device['type'] in create_device_types:
                myDevice=self.__createDeviceType(device['type'], device['name'], device['ip'], device['custId'])
            else:
                print "Device Type %s is not supported now. Created a Linux type" % device['type']
                myDevice=self.__createDeviceType('linux', device['name'], device['ip'], device['custId'])
            myDeviceList.append(myDevice)

        myObj=getClassObj('discoveryResult', module='device')
        for key in myObj.attribute.keys():
            myObj.attribute[key]=device['custId']
        myObj.success=myDeviceList
        inXml=XmlHandler.XmlHandler().XmlObjToString(myObj)
        myMon=Template(monitors)
        myMonitors=myMon.substitute(perfObj)
        myTemp=Template(inXml)
        map={'monitors':myMonitors}
        outXml=myTemp.substitute(map)

        return outXml

    def __createDeviceType(self, type, deviceName, deviceIp, custId):
        oldMap=create_device_info[type]
        if type in create_device_addon:
            base, addon=create_device_addon[type].split('->')
            tmpMap=create_device_info[base]
            if addon=='base':
                for mapKey in oldMap.keys():
                    tmpMap[mapKey]=oldMap[mapKey]
            else:
                tmpMap[addon].append(oldMap)
            infoMap=tmpMap
        else:
            infoMap=oldMap
        myDevice=getClassObj('device', module='device')
        myDevice=hashToClassHelper.hashToClass(infoMap, myDevice, objModule='device')
        myDevice.name=deviceName
        myDevice.accessIp=deviceIp
        myDevice.interfaces[0].ipv4Addr=deviceIp
        if hasattr(myDevice, 'attribute'):
            myDevice.attribute['custId']=custId
        else:
            map={'custId':custId}
            setattr(myDevice, 'attribute', map)
        for key in ['processors', 'storages', 'interfaces', 'installedSoftware', 'runningSoftware', 'swServices']:
            if hasattr(myDevice, key):
                subobjs=getattr(myDevice, key)
                for sub in subobjs:
                    if key=='interfaces':
                        if not getattr(sub, 'ipv4Addr'):
                            setattr(sub, 'ipv4Addr', randomGen.getRandomIPAddr())
                    if hasattr(sub, 'attribute'):
                        sub.attribute['custId']=custId
                    else:
                        map={'custId':custId}
                        setattr(sub, 'attribute', map)

        return myDevice

    def device_net_ip(self, map):
        map['device_net_ip']=randomGen.getRandomIPAddr()

    def device_net_mac(self, map):
        map['device_net_mac']=randomGen.getRandomMac()

    def device_mac(self, map):
        map['device_mac']=randomGen.getRandomMac()

    def hw_sn(self, map):
        map['hw_sn']=randomGen.getRandomNum(1000000000000000, 5999999999999999)

    def up_time(self, map):
        map['up_time']=randomGen.getRandomNum(2722222, 3733333)

    param_fill_token={'device_net_ip':device_net_ip,
                      'device_net_mac':device_net_mac,
                      'device_mac':device_mac,
                      'hw_sn':hw_sn,
                      'up_time':up_time,
                      }

    def fillParam(self, map, param):
        return self.param_fill_token[param](self, map)











