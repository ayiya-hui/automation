import logging
import autoTestClass
import ComHandler
import createDevice
import createQuery
import parsingQueryResult
import time, os, datetime
import compareTestResult
import GenerateNetFlowData
import randomGen
import deviceHandler
import deviceDataClass

#Win-Security-672
DOMAIN_CONTROLLER_MSG='<13>$time $reporter MSWinEventLog    1    Security    9162    $fullTime    673    Security    SYSTEM    User    Success Audit    SJQAVWINADS    Account Logon        Service Ticket Request:     User Name: PARTHA_LAPTOP$@PROSPECT-HILLS.NET     User Domain: PROSPECT-HILLS.NET     Service Name: krbtgt     Service ID: %{S-1-5-21-3383442562-1768178646-255068551-502}     Ticket Options: 0x60810010     Ticket Encryption Type: 0x17     Client Address: 192.168.20.33     Failure Code: -     Logon GUID: {7bf641ec-0dcb-7718-cefa-3ba07f269654}     Transited Services: -        8604'
def runIncident(config, testSuite):
    option=config['option']
    myHandler=ComHandler.comHandler(config['dataCollector'], config['appServer'], config['user'], config['password'])
    if option!="CheckOnly":
        if testSuite.method=='snmptrap':
            for case in testSuite.testcases:
                for i in range(0, int(case.repeatCount)):
                    for j in range(0, len(case.events)):
                        logging.debug(case.events[j].incidentMsg)
                        returnC=os.system(case.events[j].incidentMsg)
        else:
            if testSuite.method=='netflow':
                    myHandler.udpClient(port=2055)
            else:
                    myHandler.udpClient()

            for case in testSuite.testcases:
                if case.createDevice.lower()=="true":
                    myDevHandler=deviceHandler.deviceHandler(config['appServer'], config['user'], config['password'])
                    myDev=deviceDataClass.device()
                    myType=deviceDataClass.deviceType()
                    deviceDataClass.createType(myType, case.deviceType)
                    myDev.deviceType=myType
                    myDev.accessIp=case.reporter
                    myDev.name=case.deviceName
                    myRet=myDevHandler.isDeviceExist(myDev)
                    if not myRet:
                        deviceData=[]
                        device=autoTestClass.device()
                        device.name=case.deviceName
                        device.type=case.deviceType
                        device.ip=case.reporter
                        device.custId=case.custId
                        deviceData.append(device)
                        inXml=createDevice.createDeviceList(deviceData)
                        queryString="discovered/discover?sync=true"
                        myHandler.setSecure()
                        myHandler.getEvent("PUT", urlString=queryString, xml=inXml)
                        time.sleep(120)
                        myRet=myDevHandler.isDeviceExist(myDev)

                        while not myRet:
                            time.sleep(60)

                    if case.domainController=="true":
                        now=datetime.datetime.now()
                        setMsg0=DOMAIN_CONTROLLER_MSG.replace('$time', now.strftime("%b %d %H:%M:%S"))
                        setMsg1=setMsg0.replace('$fullTime', now.strftime("%a %b %d %H:%M:%S %Y"))
                        setMsg2=setMsg1.replace('$reporter', case.reporter)
                        myHandler.sendEvent(setMsg2)
                        time.sleep(120)

                for i in range(0, int(case.repeatCount)):
                    for j in range(0, len(case.events)):
                        if testSuite.method=='netflow':
                            realMsg=GenerateNetFlowData.getNetFlowPacket(case.events[j].incidentMsg)
                        else:
                            if '$randomIP' in case.events[j].incidentMsg:
                                ipMsg=case.events[j].incidentMsg.replace("$randomIP",randomGen.getRandomIPAddr())
                            elif 'randomNum' in case.events[j].incidentMsg:
                                ipMsg=case.events[j].incidentMsg.replace("$randomNum",randomGen.getRandomNum(100,900))
                            else:
                                ipMsg=case.events[j].incidentMsg
                            realMsg=ipMsg.decode()
                        myHandler.sendEvent(realMsg)
                        logging.debug(realMsg)
                    if case.repeatInterval!='':
                        time.sleep(float(case.repeatInterval))

            myHandler.udpClientClose()

    finalResult=None
    if option!="SendOnly":
        if 'sleep' in config:
            sleepTime=float(config['sleep'])*60
        else:
            sleepTime=120.0

        time.sleep(sleepTime)
        keyMap=testSuite.getKeyMap()
        queryString='phEventCategory=1 AND (eventType IN ('+keyMap['eventType']+') AND incidentRptIp IN ('+keyMap['reporter']+'))'
        inXml=createQuery.CreateQueryXML(queryString)
        myHandler.getEvent("POST", xml=inXml)


        param=parsingQueryResult.XMLParsingQueryResult(myHandler.xml)
        finalResult=compareTestResult.runCompareResult(config, testSuite, param)

    return finalResult

