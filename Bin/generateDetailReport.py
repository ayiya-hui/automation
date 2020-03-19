import autoTestResultClass
from xml.dom.minidom import Document
import XMLHelper

def generateDetailXML(testResult):
    #create detail file
    doc=Document()
    myResult=doc.createElement("TestResult")
    myResult.setAttribute("categoryName", testResult.testTask)
    myResult.setAttribute("runTime", testResult.runTime)
    myResult.setAttribute("totalRun", str(testResult.totalRun))
    myResult.setAttribute("noReturn", str(testResult.totalNoReturn))
    myResult.setAttribute("pass", str(testResult.totalPass))
    myResult.setAttribute("fail", str(testResult.totalFail))
    myResult.setAttribute("miss", str(testResult.totalMissing))
    myResult.setAttribute("improve", str(testResult.totalImprove))
    doc.appendChild(myResult)

    for suite in testResult.suiteList:
        suiteResult=doc.createElement("TestSuite")
        suiteResult.setAttribute("suiteName", suite.name)
        suiteResult.setAttribute("totalRun", str(suite.totalRun))
        suiteResult.setAttribute("pass", str(suite.totalPass))
        suiteResult.setAttribute("noReturn", str(suite.totalNoReturn))
        suiteResult.setAttribute("fail", str(suite.totalFail))
        suiteResult.setAttribute("miss", str(suite.totalMissing))
        suiteResult.setAttribute("improve", str(suite.totalImprove))
        myResult.appendChild(suiteResult)

        for case in suite.caseList:
            caseResult=doc.createElement("TestCase")
            caseResult.setAttribute("caseName", case.name)
            caseResult.setAttribute("status", case.status)
            if 'reporter' in dir(case):
                caseResult.setAttribute("reporter", case.reporter)
            if 'eventType' in dir(case):
                caseResult.setAttribute("eventType", case.eventType)
            if 'bugId' in dir(case):
                caseResult.setAttribute("bugId", case.bugId)
            suiteResult.appendChild(caseResult)

            passParam=doc.createElement("Passed")
            caseResult.appendChild(passParam)
            for passed in case.PassDetails:
                param1=doc.createElement("param")
                param1.setAttribute("name", passed['param'])
                param1.setAttribute("expect", passed['expect'])
                param1.setAttribute("actual", passed['actual'])
                passParam.appendChild(param1)

            failParam=doc.createElement("Failed")
            caseResult.appendChild(failParam)
            for failed in case.FailDetails:
                param2=doc.createElement("param")
                param2.setAttribute("name", failed['param'])
                param2.setAttribute("expect", failed['expect'])
                param2.setAttribute("actual", failed['actual'])
                failParam.appendChild(param2)

            missParam=doc.createElement("Missed")
            caseResult.appendChild(missParam)
            for missed in case.MissDetails:
                param3=doc.createElement("param")
                param3.setAttribute("name", missed['param'])
                param3.setAttribute("expect", missed['expect'])
                param3.setAttribute("actual", missed['actual'])
                missParam.appendChild(param3)

            improveParam=doc.createElement("Improve")
            caseResult.appendChild(improveParam)
            for improve in case.ImproveDetails:
                param4=doc.createElement("param")
                param4.setAttribute("name", improve['param'])
                param4.setAttribute("expect", improve['expect'])
                param4.setAttribute("actual", improve['actual'])
                improveParam.appendChild(param4)

    #Output XML files
    outDetail=testResult.testFolder+"/Detail.xml"
    outputFile=open (outDetail, 'w')
    doc.writexml(outputFile)
    outputFile.close()

    return 1


