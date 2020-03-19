import os, os.path
import XMLHelper
import generateDetailReport
import generateHTMLReport

def generateReports(testResult):

    #create test run folder
    if not os.path.exists(testResult.testFolder):
        os.makedirs(testResult.testFolder)



    return 1

    result2=generateHTMLReport.generateReportHTML(testResult)

    if result1 and result2:
        result=1
    else:
        result=0

    return result

