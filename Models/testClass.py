import deviceHandler
from sendEvent import sendEventHandler
import queryHandler
import deviceDataClass
import eventDataClass
import classUtility
from testResultDataClass import *
import classToHash
import XMLHelper
from pickClass import pickleClass
import hashUtility
import time
import logging

EVENTS='events'
ERR_MSG='device already exist. Delete it from system'
PARSER='and restart phParser'
SKIP=['any']
EVENTPARSING='eventType IN ("%s") AND reptDevIpAddr IN (%s)'
INCIDENT='phEventCategory=1 AND (eventType IN ("%s") AND incidentRptIp IN ("%s") AND incidentStatus = 0)'
AGGREGATE='phEventCategory=1 AND incidentId= %s'

class testSuite(pickleClass):
    def __init__(self):
        self.name=''
        self.fileName=''
        self.testPlanName=''
        self.method=''
        self.snmpVersion=''
        self.snmpCommunity=''
        self.testcases=[]
        self.suiteTestResult=suiteTestResult()

    def fillInCaseResult(self, testCaseResult):
        self.suiteTestResult.caseTestResults.append(testCaseResult)

    def fillInResultInfo(self):
        self.suiteTestResult.name=self.name
        self.suiteTestResult.testFileName=self.fileName
        self.suiteTestResult.totalRun=len(self.testcases)
        for testResult in self.suiteTestResult.caseTestResults:
            if testResult.status=='Pass':
                self.suiteTestResult.totalPass+=1
            elif testResult.status=='Fail':
                self.suiteTestResult.totalFail+=1
            elif testResult.status=='No Return':
                self.suiteTestResult.totalNoReturn+=1
            elif testResult.status=='Improve':
                self.suiteTestResult.totalImprove+=1
            elif testResult.status=='Miss':
                self.suiteTestResult.totalMiss+=1

class testCase(pickleClass):
    def __init__(self):
        self.name=''
        self.task=''
        self.reporter=''
        self.eventType=''
        self.createDevice=''
        self.domainController=''
        self.deviceType=''
        self.deviceName=''
        self.type=''
        self.method=''
        self.key=''
        self.testCaseNumber=''
        self.parseEvent=''
        self.events=[]
        self.parameters=''
        self.caseTestResult=''

    def setParam(self, appServer, dataCollector, method):
        self.appServer=appServer
        self.dataCollector=dataCollector
        self.deviceHandler=deviceHandler.deviceHandler(self.appServer)
        self.setVerify()
        self.queryHandler=queryHandler.queryHandler()
        self.snmp=False
        if not method:
            method='syslog'
        if method=='snmptrap':
            self.snmp=True
        self.eventHandler=sendEventHandler(method, self.dataCollector)


    def isParamSet(self):
        if self.appServer and self.dataCollector:
            return True
        else:
            return False

    def setVerify(self):
        params=self.parameters.split(',')
        paramHash={}
        for par in params:
            try:
                hashKey, hashValue=par.split('=', 1)
                paramHash[hashKey]=hashValue.replace('$Comma', ',')
            except ValueError:
                print self.name+':'+par+' error'
        self.parameters=paramHash

    def fillInResult(self, suiteName, result, module=False):
        self.caseTestResult=caseTestResult()
        self.caseTestResult.testCaseName=self.name
        if self.testCaseNumber=='':
            self.caseTestResult.testCaseNum=self.name
        else:
            self.caseTestResult.testCaseNum=self.testCaseNumber
        self.caseTestResult.testSuite=suiteName
        self.caseTestResult.reporter=self.reporter
        self.caseTestResult.eventType=self.eventType
        logging.debug('result %s', result)
        self.caseTestResult.status=result['status']
        if result['status']!='No Return':
            self.caseTestResult.passed=result['passed']
            self.caseTestResult.failed=result['failed']
            self.caseTestResult.missed=result['missed']
            self.caseTestResult.improved=result['improved']

    def runEventParsing(self, method, verify, communityName=False, snmpVersion=False):
        myRet={}
        if self.isParamSet():
            self.__createDevice()
            if self.snmp:
                if communityName and snmpVersion:
                    self.eventHandler.sendoutEvent(self.parseEvent, community=communityName, version=snmpVersion)
                elif communityName:
                    self.eventHandler.sendoutEvent(self.parseEvent, community=communityName)
                elif snmpVersion:
                    self.eventHandler.sendoutEvent(self.parseEvent, version=snmpVersion)
                else:
                    self.eventHandler.sendoutEvent(self.parseEvent)
            else:
                self.eventHandler.sendoutEvent(self.parseEvent)
            if verify==1:
                time.sleep(60)
                singleConstr=EVENTPARSING % (self.eventType, self.reporter)
                self.queryHandler.getQuery(self.appServer, singleConstr, filter=True)
                myRet=self.__compareResult()
        return myRet

    def runIncident(self, option, method, aggregate=False):
        myRet={}
        if self.isParamSet():
            self.__createDevice()
            rawData=[event.incidentMsg for event in self.events]
            self.eventHandler.sendoutEvent(rawData, count=self.repeatCount)
            if option!='SendOnly':
                time.sleep(10*60)
                myRet=self.queryIncident(advance=aggregate)
        myData={}
        if hasattr(self, 'resultData') and self.resultData:
            myData=self.resultData

        return myRet, myData

    def queryIncident(self, advance=False):
        if advance:
            singleConstr=AGGREGATE % (advance)
        else:
            singleConstr=INCIDENT % (self.eventType, self.reporter)
        self.queryHandler.getQuery(self.appServer, singleConstr)
        myRet=self.__compareResult(skip=SKIP)
        if len(myRet):
            if 'improved' in myRet.keys():
                myRet['improved']=[]
            if myRet['status']=='Improve':
                myRet['status']='Pass'

            return myRet
        else:
            print 'No data return'
            exit(1)

    def __compareResult(self, skip=False):
        map={}

        if len(self.queryHandler.data):
            self.resultData=self.queryHandler.data[0]

            if not self.resultData:
                print 'No data returned'
                self.resultData=''
            logging.debug('Result Data: %s', self.resultData)
            myCompare=hashUtility.hashCompareHandler(self.parameters, self.resultData, skip=skip)
            map['status'], map['passed'], map['failed'], map['missed'], map['improved']=myCompare.compareHash()
        else:
            map['status']='No Return'

        return map

    def __createDevice(self):
        if self.createDevice.lower()=='true':
            devStat=self.deviceHandler.isDeviceExist(self.reporter)
            if not devStat.exist:
                if self.domainController:
                    self.deviceHandler.createDevice(self.reporter, self.deviceName, self.deviceType, dataCollector=self.dataCollector)
                else:
                    self.deviceHandler.createDevice(self.reporter, self.deviceName, self.deviceType)

class incidentEvent(pickleClass):
    def __init__(self):
        self.incidentMsg=''
