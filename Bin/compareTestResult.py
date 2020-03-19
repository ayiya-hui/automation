import autoTestResultClass
import bugHandler
import logging


def runCompareResult(config, testSuite, actualParam):
    totalPass=0
    totalNoReturn=0
    totalFail=0
    totalMissing=0
    totalImprove=0
    caseList=[]
    testTask=config['testTask']
    for case in testSuite.testcases:
        PassDetails=[]
        FailDetails=[]
        MissDetails=[]
        ImproveDetails=[]
        for actual in actualParam:
            condition=checkCondition(testTask, case, actual)
            if condition=="true":
                params=case.parameters.split(",")
                for param in params:
                    mapping={}
                    temp=param.split("=", 1)
                    mapping['param']=temp[0]
                    if len(temp)==2:
                        if '$Comma' in temp[1]:
                            expect=temp[1].replace("$Comma", ",")
                        else:
                            expect=temp[1]
                        mapping['expect']=expect
                        if temp[0] in actual.keys():
                            mapping['actual']=actual[temp[0]]
                        else:
                            print "TestSuite %s TestCase %s: parameter %s is not in actual return." %(testSuite.name, case.name, temp[0])
                            mapping['actual']='missing'
                        logging.debug(mapping)
                        mapCheck=checkMap(testTask, mapping)
                        if mapCheck=="Pass":
                            PassDetails.append(mapping)
                        elif mapCheck=="Fail":
                            FailDetails.append(mapping)
                        elif mapCheck=="Miss":
                            MissDetails.append(mapping)

                for key in actual.keys():
                     if (key+'=') not in case.parameters and key not in ["hostName","srcName","destName","rawEventMsg", "bizService"]:
                         mapping={}
                         mapping['param']=key
                         mapping['expect']="Need to Add"
                         mapping['actual']=actual[key]
                         ImproveDetails.append(mapping)

        status="NoReturn"
        if len(PassDetails)!=0 and len(FailDetails)==0 and len(MissDetails)==0 and len(ImproveDetails)==0:
            status="Pass"
        elif len(FailDetails)!=0:
            status="Fail"
        elif len(MissDetails)!=0:
            status="Miss"
        elif len(ImproveDetails)!=0:
            status="Improve"

        bugId=False
        #get bug ID if it is required
        if config['option']=="SendCheckBug":
            if 'bugZillaId' in config and 'bugZilliaPass' in config:
                bugId=bugHandler.AddBugInfo(case.name, FailDetails, config['bugZillaId'], config['bugZillaPass'])
        if testTask in ['logDiscovery', 'linuxFileMonitor']:
            eventType=False
        else:
            eventType=case.eventType

        resultCase=autoTestResultClass.TestCaseResult(case.name, status, PassDetails, FailDetails, MissDetails, ImproveDetails, eventType=eventType, reporter=case.reporter, bugId=bugId)
        caseList.append(resultCase)
        if status=='Pass':
            logging.debug("Total Pass: %s",totalPass)
            totalPass+=1
        elif status=="NoReturn":
            totalNoReturn+=1
            logging.debug("Total No Return: %s",totalNoReturn)
        elif status=='Fail':
            totalFail+=1
            logging.debug("Total Fail: %s",totalFail)
        elif status=='Miss':
            totalMissing+=1
            logging.debug("Total No Return: %s",totalMissing)
        elif status=='Improve':
            totalImprove+=1
            logging.debug("Total Need to Improve: %s",totalImprove)

    resultTestSuite=autoTestResultClass.TestSuiteResult(testSuite.name, testSuite.fileName, len(testSuite.testcases), totalPass, totalNoReturn, totalFail, totalMissing, totalImprove, caseList)
    logging.debug('TestSuite Result:\n')
    logging.debug('TestSuiteResult name: %s total Run: %s pass: %s no return: %s, fail: %s', resultTestSuite.name, resultTestSuite.totalRun, resultTestSuite.totalPass, resultTestSuite.totalNoReturn, resultTestSuite.totalFail)

    return resultTestSuite




def checkCondition(testTask, case, actual):
    condition="false"
    if testTask=="logDiscovery":
        if case.reporter==actual['accessIp']:
            condition="true"
    elif testTask=="eventParsing":
        if case.eventType.strip()==actual['eventType'].strip() and case.reporter.strip()==actual['reptDevIpAddr'].strip():
                if case.key=='':
                    condition="true"
                else:
                    logging.debug('case key: %s', case.key)
                    diffKey=case.key.split(":")
                    if diffKey[1]=="" and diffKey[0] not in actual.keys():
                        condition="true"
                    if diffKey[1]!="" and diffKey[0] in actual.keys() and actual[diffKey[0]]==diffKey[1]:
                        condition="true"
    elif testTask=="incident":
        if case.eventType.strip()==actual['eventType'].strip() and case.reporter.strip()==actual['incidentRptIp'].strip() and actual['incidentStatus']=="0":
            condition="true"
    elif testTask=='linuxFileMonitor':
        if case.name.strip()==actual['caseName'].strip():
            condition="true"

    return condition


def checkMap(testTask, mapping):
    check='Fail'
    if testTask=="logDiscovery":
        if mapping['expect']==mapping['actual']:
            check="Pass"
    elif testTask in ["eventParsing","linuxFileMonitor"]:
        if mapping['expect'].replace(" ","")==mapping['actual'].replace(" ", "") or (mapping['expect']=="any" and mapping['actual']!="missing"):
            check="Pass"
    elif testTask=="incident":
        if mapping['param']=="count":
            if mapping['expect']==mapping['actual']:
                check="Pass"
            else:
                if mapping['actual']>mapping['expect']:
                    check="Pass"
        elif mapping['param']=="incidentDetail" and 'incidentCount:' in mapping['expect']:
            check="Pass"
        else:
            if mapping['expect'].replace(" ","")==mapping['actual'].replace(" ", "") or (mapping['expect']=="any" and mapping['actual']!="missing"):
                check="Pass"

    if check!="Pass" and mapping['actual']=="missing":
        check="Miss"

    return check



