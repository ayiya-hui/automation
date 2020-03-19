import testPrepare
import autoTestClass
import generalTest
import logging

LOG_FILE="../Log/autoTestLog.txt"

def runTest(configName):
    #set logging
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

    #get configuration for test
    config=testPrepare.getNewConfigure(configName)
    logging.debug(config)

    #get testcases
    testSuites=testPrepare.getTestCases(config)

    if len(testSuites.suites)==0:
        print "Empty TestSuite List, Exit."
        exit()
    else:
        #run test
        finalResult=generalTest.TestRun(config, testSuites)
        print finalResult

    #print finalResult


if __name__=='__main__':
    import sys
    runTest(sys.argv[1])
