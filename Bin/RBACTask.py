import logging
import autoTestClass
import setupTask
import verifyTask

def runRBAC(config, testSuite):
    deviceTask=None
    otherTask=[]
    for setup in testSuite.setupTasks:
        if setup.setupName=="createDevice":
                deviceTask=setup
        else:
            otherTask.append(setup)

    if deviceTask:
        setupTask.runSetup(config,deviceTask)

    for task in otherTask:
        setupTask.runSetup(config, task)

    finalResult=None
    if config['option']!="SendOnly":
        for testcase in testSuite.testcases:
            verifyName=testcase.verifyName
            eventType=testcase.eventType
            reporter=testcase.reporter
            role=None
            for adminRole in testSuite.roles:
                if testcase.roleName==adminRole['userName']:
                    role=adminRole

            for task in testcase.verifyTasks:
                testResult=verifyTask.runVerify(config, verifyName, eventType, reporter, task, adminRole=role)
                finalResult.append(testResult)

    return finalResult

