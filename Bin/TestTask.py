import time

MULTI_TASK='deviceTest'
MODULE_EVENT='eventParsing'
VERIFY_OPTION={'none':0, 'case':1, 'module':2}

def runTest(config, testSuite):
    testSuite.key=''
    verify=VERIFY_OPTION['none']
    sendSnmp=False
    if testSuite.method=='snmptrap':
        sendSnmp=True

    if config['option']!='SendOnly':
        if config['testTask']==MODULE_EVENT:
            verify=VERIFY_OPTION['module']
        else:
            verify=VERIFY_OPTION['case']

    if config['testTask']==MULTI_TASK:
        setTask=False
    else:
        setTask=True

    for testcase in testSuite.testcases:
        if setTask:
            testcase.task=config['testTask']
        if testSuite.method:
            myMethod=testSuite.method
        else:
            myMethod=testcase.method
        testcase.setParam(config['appServer'], config['dataCollector'], myMethod)
        if testcase.task=='logDiscovery':
            result=testcase.runLogDiscovery()
        elif testcase.task=='snmpDiscovery':
            result=testcase.runSnmpDiscovery()
        elif testcase.task=='eventParsing':
            if sendSnmp:
                result=testcase.runEventParsing(testSuite.method, verify, communityName=testSuite.snmpCommunity, snmpVersion=testSuite.snmpVersion)
            else:
                result=testcase.runEventParsing(testSuite.method, verify)
        elif testcase.task=='incident':
            result=''
            if testcase.type=='aggregate':
                if testSuite.runStatus and testSuite.resultData:
                    result, resData=testcase.runAggregateIncident(config['option'], testSuite.method, testSuite.resultData)
                    testSuite.resultData=resData
                else:
                    print 'Incident is not triggered, skip aggregation test.'
                    result={}
                    result['status']='No Return'
            elif testcase.type=='clear':
                if testSuite.runStatus and testSuite.resultData:
                    result, resData=testcase.runClearIncident(config['option'], testSuite.method, testSuite.resultData)
                    testSuite.resultData=resData
                else:
                    print '%s %s: Incident is not triggered, skip clear test.' % (testSuite.name, testcase.name)
                    result={}
                    result['status']='No Return'
            else:
                result, resData=testcase.runIncident(config['option'], testSuite.method)
                testSuite.resultData=resData
                testSuite.runStatus=True

        if verify==VERIFY_OPTION['case']:
            testcase.fillInResult(testSuite.name, result)
            testSuite.fillInCaseResult(testcase.caseTestResult)

    if verify==VERIFY_OPTION['module']:
        if 'sleep' in config.keys() and config['sleep']!='0':
            time.sleep(float(int(config['sleep'])*60))
        else:
            time.sleep(120)
        testSuite.runModuleVerify(config['appServer'])

    if verify!=VERIFY_OPTION['none']:
        testSuite.fillInResultInfo()

    return testSuite.suiteTestResult

