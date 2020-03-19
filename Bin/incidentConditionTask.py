import logging
import autoTestClass
import autoTestResultClass
import ComHandler
import createDevice
import createQuery
import parsingQueryResult
import time, os
import compareTestResult
import AdvIncidentCompare

PATTERN_REASON="clear conditions are met"
TIME_REASON="rule does not trigger for $n minutes"

def runPatternBased(config, testSuite):
    finalResult=runIncident(config, testSuite, "pattern")

    return finalResult

def runTimeBased(config, testSuite):
    finalResult=runIncident(config, testSuite, "time")

    return finalResult

def runIncident(config, testSuite, type):
    option=config['option']
    myHandler=ComHandler.comHandler(config['dataCollector'], config['appServer'], config['user'], config['password'])
    myHandler.udpClient()
    finalResult=[]
    caseList=[]
    for case in testSuite.testcases:
        inXml=''
        if case.createDevice.lower()=="true":
            inXml=createDevice.createDeviceList(case.deviceType, case.deviceName, case.reporter, 1, case.custId)
            queryString="discovered/discover?sync=true"
            myHandler.setSecure()
            myHandler.getEvent("PUT", urlString=queryString, xml=inXml)
            time.sleep(120)

        if option!="SendOnly":
            keyMap=testSuite.getKeyMap()
            queryString='phEventCategory=1 AND (eventType IN ('+keyMap['eventType']+') AND incidentRptIp IN ('+keyMap['reporter']+'))'
            inXml=createQuery.CreateQueryXML(queryString)
            logging.debug(inXml)

        mapping={}
        if testSuite.sendEvent=="true":
            for i in range(0, int(case.sendCount)):
                for j in range(0, int(case.repeatCount)):
                    for k in range(0, len(case.events)):
                        myHandler.sendEvent(case.events[k].incidentMsg)
                        logging.debug(case.events[k].incidentMsg.decode())
                        if case.repeatInterval!='':
                            time.sleep(float(case.repeatInterval))

                if option!="SendOnly":
                    if inXml!='':
                        time.sleep(float(case.sendInterval))
                        myHandler.getEvent("POST", xml=inXml)
                        myParam=parsingQueryResult.XMLParsingQueryResult(myHandler.xml)
                        if len(myParam)!=0:
                            if i==0:
                                mapping['New']=myParam[0]
                            else:
                                mapping['Update '+str(i)]=myParam[0]
                        else:
                            print "%s: No info in return parameter. Exit." % testSuite.name
                            exit()
                    else:
                        print "No Query XML. Exit."
                        exit()



        time.sleep(float(case.clearInterval))
        if type=="pattern":
            for i in range(0, int(case.clearCount)):
                myHandler.sendEvent(case.clearEvent)
                logging.debug(case.clearEvent)

        time.sleep(float(case.clearWait))
        myHandler.getEvent("POST", xml=inXml)
        clearParam=parsingQueryResult.XMLParsingQueryResult(myHandler.xml)
        if 'incidentClearedReason' in clearParam[0].keys():
            mapping['Clear']=clearParam[0]
        else:
            mapping['Clear']='No Clear Event'
        if type=="pattern":
            reason=PATTERN_REASON
        else:
            reason=TIME_REASON.replace("$n", case.clearInterval)
        resultCase=AdvIncidentCompare.verifyResult(config, case.name, case.eventType, case.reporter, case.sendCount, reason, mapping)
        caseList.append(resultCase)

    totalPass=0
    totalFail=0
    totalMissing=0
    for item in caseList:
        if item.status=='Pass':
            logging.debug("Total Pass: %s",totalPass)
            totalPass+=1
        elif item.status=='Fail':
            totalFail+=1
            logging.debug("Total Fail: %s",totalFail)
        elif item.status=='NoReturn':
            totalMissing+=1
            logging.debug("Total No Return: %s",totalMissing)

    resultTestSuite=autoTestResultClass.TestSuiteResult(testSuite.name, testSuite.fileName, len(testSuite.testcases), totalPass, totalFail, totalMissing, caseList)
    logging.debug('TestSuite Result:\n')
    logging.debug('TestSuiteResult name: %s total Run: %s pass: %s fail: %s', resultTestSuite.name, resultTestSuite.totalRun, resultTestSuite.totalPass, resultTestSuite.totalFail)

    myHandler.udpClientClose()

    return resultTestSuite

