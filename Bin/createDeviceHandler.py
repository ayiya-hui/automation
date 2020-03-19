import XMLHelper
import DeviceModels
import xml.dom.minidom as dom
import randomGen
import DeviceModels
import CreateCisco
import CreateFortinet
import CreateEsx
import CreateLinux
import CreateWindows
import CreateJuniper

class createDeviceHandler:
    def __init__(self):
        pass

    def createDevice(self, deviceIp, deviceName, deviceType, custId='1'):
        deviceData=[]
        map={}
        map['name']=deviceName
        map['type']=deviceType
        map['ip']=deviceIp
        map['custId']=custId
        deviceData.append(map)

        return self.__createDevice(deviceData)

    def createRandomDevices(self, deviceType, number, custId='1'):
        deviceData=[]
        for i in range(0, number):
            map={}
            map['name']="autoDevice"+deviceType+str(i+1)
            map['type']=deviceType
            map['ip']=randomGen.getRandomIPAddr()
            map['custId']=custId
            deviceData.append(map)

        return self.__createDevice(deviceData)

    def __createDevice(self, deviceData):
        myDeviceList=[]
        for device in deviceData:
            myDevice=self.__createDeviceType(device['type'], device['name'], device['ip'], device['custId'])
            myDeviceList.append(myDevice)

        myObj=DeviceModels.discoveryResult("1", "1", myDeviceList)
        node=XMLHelper.pickle(root=myObj, fabric=dom.Document(), elementName='discoveryResult')

        return node.toxml()

    def __createDeviceType(self, type, deviceName, deviceIp, custId):
        if type=="win":
            myDevice=CreateWindows.CreateWindowsDevice(deviceName, deviceIp, custId)
        elif type=="symantec":
            myDevice=CreateWindows.CreateSymantecDevice(deviceName, deviceIp, custId)
        elif type=="aaa":
            myDevice=CreateWindows.CreateAAADevice(deviceName, deviceIp, custId)
        elif type=="cisco":
            myDevice=CreateCisco.CreateCiscoDevice(deviceName, deviceIp, custId)
        elif type=="ciscoIPS":
            myDevice=CreateCisco.CreateCiscoIPSDevice(deviceName, deviceIp, custId)
        elif type=="esx":
            myDevice=CreateEsx.CreateEsxDevice(deviceName, deviceIp, custId)
        elif type=="linux":
            myDevice=CreateLinux.CreateLinuxDevice(deviceName, deviceIp, custId)
        elif type=="bindDns":
            myDevice=CreateLinux.CreateBindDNSDevice(deviceName, deviceIp, custId)
        elif type=='snortIPS':
            myDevice=CreateLinux.CreateSnortDevice(deviceName, deviceIp, custId)
        elif type=="fortinet":
            myDevice=CreateFortinet.CreateFortinetDevice(deviceName, deviceIp, custId)
        elif type=="JuniperSecureAccess":
            myDevice=CreateJuniper.CreateSecureAccessDevice(deviceName, deviceIp, custId)
        else:
            print "Device Type %s is not supported now. Created a Linux type" % type
            myDevice=CreateLinux.CreateLinuxDevice(deviceName, deviceIp, custId)

        return myDevice


