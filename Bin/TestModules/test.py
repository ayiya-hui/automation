from AutoTestUtil.testPrepare import getTestConfig
from ConfigConstants.TestConstant import supported_tasks, default_config_file_path
from TestModules.runPopulator import populatorTest
from TestModules.runDiscover import discoverTest
from TestModules.runEventParsing import eventParsingTest
from TestModules.runIncident import incidentTest
from TestModules.runRestApi import restApiTest
from TestModules.runLogDiscover import logDiscoverTest
from Core.testThreading import testThread
from Models.autoTestResultClass import AutoTestResult
import ConfigConstants.TestConstant as TestConstant
from Report.testReportHandler import testReport
from Util.testUtility import processList
import Util.classUtility as classUtility
from Libs.testRuleHandler import testRule
import Queue
import time
import re

default_threads_pool=100
default_thread_wait=0

tokenDict={'DbPopulator':populatorTest,
           'EventParsing':eventParsingTest,
           'Incident':incidentTest,
           'Discover':discoverTest,
           'RestApi':restApiTest,
           'LogDiscover':logDiscoverTest,}
test_rule_errors={'Syntax Error':'Rule Syntax Error',
                  'Filter Mismatch':'Event does not match Rule filter'}

test_rule_exps={}
for key in test_rule_errors.keys():
    test_rule_exps[key]=re.compile(test_rule_errors[key])

def autoTest(file):
    """starting point to run automation test."""
    testConfig=getTestConfig(file)
    if testConfig.threadPool is not None:
        thread_pool=testConfig.threadPool
    else:
        thread_pool=default_threads_pool
    thread_wait=0
    if testConfig.threadWaitTime is not None:
        thread_wait=int(testConfig.threadWaitTime)
    else:
        thread_wait=default_thread_wait
    threads=[]
    taskNames=[]
    queue=Queue.Queue()
    return_queue=Queue.Queue()
    for task in testConfig.testTask:
        taskNames.append(task.taskName)
        if not task.taskName in supported_tasks:
            print 'test task: %s is not supported at current time.' % task.taskName
            exit()
        testObj=tokenDict[task.taskName](task, testConfig)
        id=1
        commData=testObj.getCommonData(task.taskFiles)
        if commData:
            setattr(testConfig, 'commonData', commData)
        globalData=testObj.getGlobalData()
        if globalData:
            setattr(testConfig, 'globalData', globalData)
        tests=testObj.getTestList(task.taskFiles)

        if not tests:
            print 'no tests performed.'
            exit()
        miss, extra, common=processList(tests.keys(), commData.keys())
        miss_map={}
        if miss:
            print 'NOT implemented:\n'
            for item in miss:
                print 'Id: %s Name: %s\n' % (item, tests[item].name)
                miss_map[item]=tests[item].name

        for testKey in common:
            map={}
            map['name']=task.taskName
            map['task']=tests[testKey]
            map['key']=testKey
            map['obj']=tokenDict[task.taskName](task, testConfig)
            queue.put(map)

        if len(common)>thread_pool:
            thread_size=thread_pool
        else:
            thread_size=len(common)

        for i in range(thread_size):
            thread=testThread(queue, return_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
            if thread_wait:
                time.sleep(thread_wait)


    queue.join()
    fullResult=[]
    while not return_queue.empty():
        item=return_queue.get_nowait()
        if item:
            fullResult.append(item)


    print "Main Test Thread Exiting"
    if testConfig.ruleTest and testConfig.ruleTestSupport:
    #check testRule for incident testing
        if testConfig.testTask[0].taskName=='Incident':
            for item in fullResult:
                if item.caseList[0].status=='NoReturn' and item.testMethod=='syslog':
                    myMap={'ruleId':item.ruleId, 'rawMsg':item.rawMsg, 'reportIp':item.reptDevIpAddr}
                    status, msg=testRule(testConfig.testServer.appServer, ruleData=myMap)
                    reason=''
                    if status=="Pass":
                        item.caseList[0].status='Pass'
                    elif status=='Failure':
                        matched=''
                        for key in test_rule_exps.keys():
                            match=test_rule_exps[key].search(msg)
                            if match:
                                matched=key
                                break
                        reason='testRule triggers failure: %s' % matched
                    elif status=='Unfinish':
                        rasson='testRule triggers unfinished after timeout 10 minutes'
                    item.testRuleResultSummary=reason
                    item.testRuleResultDetail=msg

    autoRet=AutoTestResult()
    autoRet.name='-'.join(taskNames)
    if hasattr(testConfig, 'batch'):
        autoRet.batch=testConfig.batch
    else:
        autoRet.batch=''
    autoRet.testType=testConfig.testType
    autoRet.runTime=testConfig.runTime
    autoRet.runVersion=testConfig.buildVersion
    autoRet.localhost=testConfig.localhost
    autoRet.testFolder=TestConstant.default_result_path+testConfig.name
    if miss_map:
        setattr(autoRet, 'miss', miss_map)
    if classUtility.getType(testConfig.sendEmail)!='NoneType':
        autoRet.sendEmail=True
    for item in fullResult:
        for count in TestConstant.test_result_counters:
            value=getattr(autoRet, count)
            value+=getattr(item, count)
            setattr(autoRet, count, value)
        autoRet.suiteList.append(item)

    msg=testReport().generateReport(autoRet)

    return msg

if __name__=='__main__':
    import sys
    file=default_config_file_path+sys.argv[1]+'.xml'
    msg=autoTest(file)

    print 'Done'





