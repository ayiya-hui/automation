import logging
import ComHandler
import SshHandler
import ScpHandler
import makeTime
import eventExportCompare
import createQuery
import parsingQueryResult
import time

FILTER=['phCustId', 'reptDevIpAddr', 'hostName', 'phRecvTime', 'rawEventMsg']
FILENAME="exportedEvents.dat"

def runEventExport(config, testSuite):
    option=config['option']
    myHandler=ComHandler.comHandler(config['dataCollector'], config['appServer'], config['user'], config['password'])
    totalParam=[]
    accessIps=[]

    finalResult=None
    caseList=[]

    for case in testSuite.testcases:
        timeParam=makeTime.MakeTime(case.startTime, case.endTime)
        myPrompt=''
        if config['SshAdmin']=='root':
            myPrompt='#'
        else:
            myPrompt='$'
        mySSH=SshHandler.SshHandler(config['dataCollector'], config['SshAdmin'], config['SshPass'], prompt=myPrompt)
        cmdList=[]
        cmdList.append(makeCmd(case.option, config['destFolder'], timeParam, case.reporter, case.custName))
        value=mySSH.runCmd(cmdList)
        time.sleep(120)
        mySCP=ScpHandler.ScpHandler(config['dataCollector'], config['SshAdmin'], config['SshPass'])
        fileName=config['destFolder']+'/'+FILENAME
        mySCP.getFile(fileName)
        testParam=getFile(FILENAME)
        logging.debug("Script return %s", testParam)

        queryString='reptDevIpAddr='+case.reporter
        inXml=createQuery.CreateQueryXML(queryString, startTime=timeParam['startTime']['uTime'], endTime=timeParam['endTime']['uTime'])
        myHandler.getEvent("POST", xml=inXml)
        param=parsingQueryResult.XMLParsingQueryResult(myHandler.xml, filter=FILTER)
        logging.debug("REST API return %s", param)
        if len(param)!=testParam:
            print "phExportEvent script generates %d records." % len(testParam)
            print "REST API query returns %d records." % len(param)

        resultCase=eventExportCompare.verifyResult(config, case.name, "N/A", case.reporter, testParam, param)
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

    return resultTestSuite

def makeCmd(option, destFolder, timeParam, dev, org):
    if option=="relativeStart":
        time='--relstarttime "'+timeParam['duration']+'" --endtime "'+timeParam['endTime']['cTime']+'"'
    elif option=="relativeEnd":
        time='--starttime "'+timeParam['startTime']['cTime']+'" --relendtime "'+timeParam['duration']+'"'
    else:
        time='--starttime "'+timeParam['startTime']['cTime']+'" --relendtime "'+timeParam['endTime']['cTime']+'"'

    cmd='./phExportEvent --dest '+destFolder+' '+time+' --dev '+dev+' --org '+org

    return cmd

def getFile(fileName):
    param=[]
    fileHandler=open(fileName, 'r')
    lines=fileHandler.readlines()
    for line in lines:
        map={}
        if line!='':
           temp=line.split(",")
           for i in range(len(FILTER)):
               map[FILTER[i]]=temp[i]
               param.append(map)

    return param


