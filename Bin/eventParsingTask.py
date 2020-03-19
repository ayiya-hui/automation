import logging
import autoTestClass
import ComHandler
import createQuery
import parsingQueryResult
import time, os
import compareTestResult
import randomGen
import GenerateNetFlowData

def runEventParsing(config, testSuite):
    option=config['option']

    if option!="CheckOnly":
        if testSuite.method=='snmptrap':
            for case in testSuite.testcases:
               logging.debug(case.parseEvent)
               returnC=os.system(case.parseEvent)
        else:
            if testSuite.method=='netflow':
                myHandler.udpClient(port=2055)
            else:
                myHandler.udpClient()

            for case in testSuite.testcases:
                if testSuite.method=='netflow':
                    realMsg=GenerateNetFlowData.getNetFlowPacket(case.parseEvent)
                else:
                    realMsg=case.parseEvent.decode()
                myHandler.sendEvent(realMsg)
                logging.debug(realMsg)
            myHandler.udpClientClose()

    finalResult=None
    if option!="SendOnly":
        if 'sleep' in config:
            sleepTime=float(config['sleep'])*60
        else:
            sleepTime=120.0

        time.sleep(sleepTime)
        keyMap=testSuite.getKeyMap()
        queryString='eventType IN ('+keyMap['eventType']+') AND reptDevIpAddr IN ('+keyMap['reporter']+')'
        inXml=createQuery.CreateQueryXML(queryString)
        myHandler.getEvent("POST", xml=inXml)
        param=parsingQueryResult.XMLParsingQueryResult(myHandler.xml, check=True)
        finalResult=compareTestResult.runCompareResult(config, testSuite, param)

    return finalResult



