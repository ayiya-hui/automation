import randomGen
import DeviceModels
import CreateCisco
import CreateFortinet
import CreateEsx
import CreateLinux
import CreateWindows
import CreateJuniper

def CreateDevice(type, deviceName, deviceIp, custId):
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
