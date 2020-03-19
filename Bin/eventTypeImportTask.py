import logging
import autoTestClass
import setupTask
import verifyTask
import classUtilities
import resultCompareByCase
import autoTestResultClass
import time

def runConfigImport(config, testSuite):
    deviceTask=None
    otherTask=[]
    testData=[]
    caseList=[]
    for setup in testSuite.setupTasks:
        className=classUtilities.getClassName(setup)
        if className=="createDevice":
                deviceTask=setup
        else:
            otherTask.append(setup)

    if deviceTask:
        setupTask.runSetup(config,deviceTask)

    time.sleep(120)

    for task in otherTask:
        data=setupTask.runSetup(config, task)
        for item in data:
            testData.append(item)
    if 'sleep' in config.keys():
        time.sleep(float(60*(int(config['sleep']))))
    else:
        time.sleep(120)

    finalResult=None
    if config['option']!="SendOnly":
        for testcase in testSuite.testcases:
            rawData=verifyTask.runVerify(config, testcase.eventTypeImport)
            expectData=getExpectData(testcase.verifyTask.eventType, rawData['filter'], testData)
            testResult=resultCompareByCase.runCaseCompare(expectData, rawData['resultData'][-1])
            resultCase=autoTestResultClass.TestCaseResult(testcase.name, testResult['status'], testResult['passDetail'], testResult['failDetail'], testResult['missDetail'], testResult['improveDetail'])
            caseList.append(resultCase)

    totalPass=0
    totalFail=0
    totalMissing=0
    totalImprove=0

    for case in caseList:
        if case.status=='Pass':
            totalPass+=1
        elif case.status=='Fail':
            totalFail+=1
        elif case.status=='No Return':
            totalMissing+=1
        elif case.status=="Improve":
            totalImprove+=1

    finalResult=autoTestResultClass.TestSuiteResult(testSuite.name, testSuite.fileName, len(testSuite.testcases), totalPass, totalFail, totalMissing, totalImprove, caseList)

    return finalResult

def getExpectData(eventType, filter, testData):
    expectData={}
    for test in testData:
        if test['eventType']==eventType:
            for item in test['param'].keys():
                if item in filter or item=='eventName':
                    expectData[item]=test['param'][item]

    return expectData


