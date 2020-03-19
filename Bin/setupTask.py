import createDevice
import ComHandler
import DynamicCaseBuilder
import processCSV
import GenerateNetFlowData
import classUtilities
import logging

DEFAULT_ADMIN="super/admin"
DEFAULT_PASSWORD="admin*1"

def runSetup(config, setupTask):
    className=classUtilities.getClassName(setupTask)
    if className=="createDevice":
        deviceCreate(config, setupTask.deviceList)
        return None
    elif className in ["sentEvent","sentIncident"]:
        testData=DynamicCaseBuilder.getData(setupTask, className)
        sendMap=prepareData(testData)
        dataSend(config, sendMap)
        return testData
    elif calssName=="readEventType":
        testData=processCSV.getData(setupTask.name)
        return testData

def deviceCreate(config, setupValue):
    myHandler=ComHandler.comHandler(config['appServer'], config['dataCollector'], DEFAULT_ADMIN, DEFAULT_PASSWORD)
    inXml=createDevice.createDeviceList(setupValue)
    queryString="discovered/discover?sync=true"
    myHandler.getEvent("PUT", urlString=queryString, xml=inXml)

def prepareData(testData):
    sendSyslogData=[]
    sendTrapData=[]
    sendNetflowData=[]
    for test in testData:
       map={}
       map['msg']=test['msg']
       if 'repeatCount' in test.keys():
           count=test.repeatCount
       else:
           count="1"
       map['count']=count

       if test['sentMethod']=="syslog":
           sendSyslogData.append(map)
       elif test['sentMethod']=="snmptrap":
           sendTrapData.append(map)
       elif test['sentMethod']=="netflow":
           sendNetflowData.append(map)

    sendMap={}
    sendMap['syslog']=sendSyslogData
    sendMap['snmptrap']=sendTrapData
    sendMap['netflow']=sendNetflowData

    return sendMap

def dataSend(config, sendMap):
    myHandler=ComHandler.comHandler(config['appServer'], config['dataCollector'], DEFAULT_ADMIN, DEFAULT_PASSWORD)
    for key in sendMap.keys():
        if key=="syslog":
            myHandler.udpClient()
            for data in sendMap['syslog']:
                for i in range(int(data['count'])):
                    myHandler.sendEvent(data['msg'].decode())
                    logging.debug(data['msg'])
            myHandler.udpClientClose()
        elif key=="netflow":
            myHandler.udpClient(port=2055)
            for data in sendMap['netflow']:
                realMsg=GenerateNetFlowData.getNetFlowPacket(msg)
                for i in range(int(data['count'])):
                    myHandler.sendEVent(realMsg)
                    logging.debug(realMsg)
            myHandler.udpClientClose()
        elif key=="snmptrap":
            for data in sendMap['snmptrap']:
                for i in range(int(data['count'])):
                    returnC=os.system(data['msg'])
                    logging.debug(data['msg'])

