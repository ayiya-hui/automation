import logging
import autoTestClass
import ComHandler
import createDevice
import createQuery
import parsingQueryResult
import time, os
import compareTestResult

def runIncident(config, testSuite):
    option=config['option']
    myHandler=ComHandler.comHandler(config['dataCollector'], config['appServer'], config['user'], config['password'])
    if option!="CheckOnly":
        myHandler.udpClient()
        for case in testSuite.testcases:
            if case.createDevice.lower()=="true":
                inXml=createDevice.createDeviceList(case.deviceType, case.deviceName, case.reporter, 1, case.custId)
                queryString="discovered/discover?sync=true"
                myHandler.setSecure()
                myHandler.getEvent("PUT", urlString=queryString, xml=inXml)
                time.sleep(120)

            for i in range(0, int(case.repeatCount)):
                for j in range(0, len(case.events)):
                    myHandler.sendEvent(case.events[j].incidentMsg)
                    logging.debug(case.events[j].incidentMsg.decode())
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

