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
    param=[]
    myHandler=ComHandler.comHandler(config['dataCollector'], config['appServer'], config['user'], config['password'])
    myHandler.udpClient()

    for case in testSuite.testcases:
        inXml=''
        if case.createDevice.lower()=="true":
            inXml=createDevice.createDeviceList(case.deviceType, case.deviceName, case.reporter, 1, "1")
            queryString="discovered/discover?sync=true"
            myHandler.setSecure()
            myHandler.getEvent(queryString, inXml, "PUT")
            time.sleep(120)

        if option!="SendOnly":
            keyMap=testSuite.getKeyMap()
            queryString='phEventCategory=1 AND (eventType IN ('+keyMap['eventType']+') AND incidentRptIp IN ('+keyMap['reporter']+'))'
            inXml=createQuery.CreateQueryXML(queryString)
            logging.debug(inXml)

        if testSuite.sendEvent=="true":
            for i in range(0, int(case.sentCount)):
                for j in range(0, int(case.repeatCount)):
                    for k in range(0, len(case.events)):
                        myHandler.sendEvent(case.events[k].incidentMsg)
                        logging.debug(case.events[k].incidentMsg.decode())
                    time.sleep(float(case.repeatInterval))
                    if option!="SendOnly":
                        if inXml!='':
                            myHandler.getEvent('', inXml, "POST")
                            myParam={}
                            myParam["Event "+str(i+1)]=parsingQueryResult.XMLParsingQueryResult(myHandler.xml, "nocheck")
                            param.append(myParam)
                        else:
                            print "No Query XML. Exit."
                            exit()

                    time.sleep(float(case.sentInterval))

        if testSuite.clearEvent=="true":
            time.sleep(float(case.clearInterval))
            myHandler.sendEvent(case.clearEvent)

        time.sleep(float(case.clearWait))
        myHandler.getEvent('', inXml, "POST")
        clearParam={}
        clearParam['Clear Event']=parsingQueryResult.XMLParsingQueryResult(myHandler.xml, "nocheck")
        param.append(clearParam)

    myHandler.udpClientClose()

    finalResult=compareTestResult.runCompareResult(config, testSuite, param)

    return finalResult

