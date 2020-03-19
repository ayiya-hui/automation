import autoTestResultClass

def generateReportHTML(testResult):
    #generate report HTML file
    testTask=testResult.testTask
    outReport=testResult.testFolder+"/report.html"
    outFile=open(outReport,'w')
    outFile.write("<HTML>\n")
    outFile.write("<Title>Accelops Automation Test Report</Title>\n")
    outFile.write("<BODY>\n")
    outFile.write("<H1>Test Report</H1>\n")
    outFile.write("<HR>\n")
    outFile.write("<B>Test Running Time: %s</B>\n" % testResult.runTime)
    outFile.write("<B>Test Category: %s</B>\n" % testResult.testTask)
    outFile.write("<B>Test Target Build Version: %s</B>\n" % testResult.runVersion)
    outFile.write("<Table border=1>\n")
    outFile.write("<TR>\n")
    outFile.write("    <TD><B>Module</B></TD>\n")
    outFile.write("    <TD><B>Total Test</B></TD>\n")
    outFile.write("    <TD><B>Test Passed</B></TD>\n")
    outFile.write("    <TD><B>No Return Data</B></TD>\n")
    outFile.write("    <TD><B>Test Failed</B></TD>\n")
    outFile.write("    <TD><B>Param Not in Return</B></TD>\n")
    outFile.write("    <TD><B>Param Not in TestCase</B></TD>\n")
    outFile.write("    <TD><B>Detail Results</B></TD>\n")
    outFile.write("</TR>\n")

    outFile.write("<TR>\n")
    outFile.write("<TD>Total</TD>\n")
    outFile.write("<TD>%s</TD>\n" % str(testResult.totalRun))
    outFile.write("<TD>%s</TD>\n" % str(testResult.totalPass))
    outFile.write("<TD>%s</TD>\n" % str(testResult.totalNoReturn))
    outFile.write("<TD>%s</TD>\n" % str(testResult.totalFail))
    outFile.write("<TD>%s</TD>\n" % str(testResult.totalMissing))
    outFile.write("<TD>%s</TD>\n" % str(testResult.totalImprove))
    outFile.write("</TR>\n")

    linkString=testResult.testFolder.replace("../Results", "/testresult")
    detailLink="http://"+testResult.localhost+linkString+"/Detail.xml"
    for i in testResult.suiteList:
        link="http://"+testResult.localhost+"/testcase/"+testResult.testTask+"/"+i.fileName

        outFile.write("<TR>\n")
        outFile.write("<TD><A HREF=%s>%s</TD>\n" % (link, i.name))
        outFile.write("<TD>%s</TD>\n" % str(i.totalRun))
        outFile.write("<TD>%s</TD>\n" % str(i.totalPass))
        outFile.write("<TD>%s</TD>\n" % str(i.totalNoReturn))
        outFile.write("<TD>%s</TD>\n" % str(i.totalFail))
        outFile.write("<TD>%s</TD>\n" % str(i.totalMissing))
        outFile.write("<TD>%s</TD>\n" % str(i.totalImprove))
        outFile.write("<TD><A HREF=%s>Check Details</TD>\n" % detailLink)

    outFile.write("</Table>\n")
    outFile.write("<HR>\n")

    #list failed testcase details
    failedCase=[]
    showBugLink=False
    showReporter=False
    showEventType=False

    for suite in testResult.suiteList:
        for case in suite.caseList:
            mapping={}
            params=[]
            expects=[]
            actuals=[]
            if case.status!="Pass":
                mapping['caseName']=case.name
                mapping['testSuite']=suite.name
                mapping['testSuiteFile']=suite.fileName
                if case.status=="NoReturn":
                    mapping['attributes']="All"
                    mapping['expect']="All"
                    mapping['actual']="No Return Data"
                else:
                    if case.status=="Fail":
                        for error in case.FailDetails:
                            params.append(error['param'])
                            expects.append(error['expect'])
                            actuals.append(error['actual'])
                    elif case.status=="Miss":
                        for error in case.MissDetails:
                            params.append(error['param'])
                            expects.append(error['expect'])
                            actuals.append(error['actual'])
                    else:
                         for error in case.ImproveDetails:
                            params.append(error['param'])
                            expects.append(error['expect'])
                            actuals.append(error['actual'])

                    mapping['attributes']=','.join(params)
                    mapping['expect']=','.join(expects)
                    mapping['actual']=','.join(actuals)

                if 'reporter' in dir(case):
                    mapping['reporter']=case.reporter
                    showReporter=True
                if 'eventType' in dir(case):
                    mapping['eventType']=case.eventType
                    showEventType=True
                if 'bugId' in dir(case):
                    mapping['bugId']=case.bugId
                    showBugLink=True

            if mapping!={}:
                failedCase.append(mapping)

    if (len(failedCase)==0):
        outFile.write("This test run has no failed testcase.\n")
    else:
        if showBugLink:
            outFile.write("Enable to use the Bug Id link below, you need to <A HREF=\"http://sj-dev-s-rh-vmw-01/bugzilla-3.0.4\">log in.")
        outFile.write("<Table border=1>\n")
        outFile.write("<TR>\n")
        outFile.write("    <TD><B>Test Case</B></TD>\n")
        if showReporter:
            outFile.write("    <TD><B>Reporter</B></TD>\n")
        outFile.write("   <TD><B>Test Suite</B></TD>\n")
        if showEventType:
            outFile.write("   <TD><B>Event Type</B></TD>\n")
        outFile.write("    <TD><B>Failed Attribute</B></TD>\n")
        outFile.write("    <TD><B>Expect Value</B></TD>\n")
        outFile.write("    <TD><B>Actual Value</B></TD>\n")
        if showBugLink:
            outFile.write("   <TD><B>Bug ID</B></TD>\n")
        outFile.write("</TR>\n")

        for i in failedCase:
            errorLink="http://"+testResult.localhost+"/testcase/"+testResult.testTask+"/"+i['testSuiteFile']

            outFile.write("<TR>\n")
            outFile.write("<TD><A HREF=%s>%s</TD>\n" % (errorLink, i['caseName']))
            if showReporter:
                outFile.write("<TD>%s</TD>\n" % i['reporter'])
            outFile.write("<TD>%s</TD>\n" % i['testSuite'])
            if showEventType:
                outFile.write("<TD>%s</TD>\n" % i['eventType'])
            outFile.write("<TD>%s</TD>\n" % i['attributes'])
            outFile.write("<TD>%s</TD>\n" % i['expect'])
            outFile.write("<TD>%s</TD>\n" % i['actual'])
            if showBugLink:
                bugLink="http://sj-dev-s-rh-vmw-01/bugzilla-3.0.4/show_bug.cgi?id="
                outFile.write("<TD><A HREF=%s>%s</TD>\n" % (bugLink+i['buId'], i['buId']))
            outFile.write("</TR>\n")

        outFile.write("</Table>\n")
        outFile.write("<HR>\n")

    outFile.write("</BODY>\n")
    outFile.write("</HTML>\n")
    outFile.close()

    return 1
