import os
import XMLHelper
import classUtility
from htmlHandler import *
from hashUtility import hashMethod

MSG='The Test Report is generated. Please go to test web page to view it.'
FIELDS=['Module','Total Test','Test Passed','No Return Data','Test Failed','Param Not in Return','Param Not in TestCase','Detail Results']
TITLE='Accelops Automation Test Report'
NAME='Test Report'
WELCOME='Welcome to Accelops Automation Test'
DESC='To view the most recent test results, please click the links to see the result:'
SUBTITLE='Test Running Time: %s Test Category: %s Test Target Build Version: %s'
DEFAULT_BORDER=1
REF='http://%s/testcase/%s/%s'
RESREF='http://%s/%s'
SUMREF='http://%s/testresult/%s/%s/report.html'
RESULT='../Results'
INDEX='../Public/index.html'
NO_RETURN='Testcases have No Return:'
PARAM_ERROR='Testcases have return but some parameters are not correct:'
MISS_RETURN='Testcases have return but some expected parameters are missing:'
IMPROVE_CASE='Testcases have return but some return parameters are not expected:'
CASE_FIELDS=['Test Case', 'Test Case Number', 'Event Type', 'Reporter', 'Test Suite']
ERROR_FIELDS=['Test Case', 'Test Case Number', 'Reporter', 'Event Type','Test Suite', 'Failed Attributes','Expect Value', 'Actual Value']
MISS_FIELDS=['Test Case', 'Test Case Number', 'Reporter', 'Event Type','Test Suite', 'Attributes Missing', 'Expect Value']
IMPROVE_FIELDS=['Test Case', 'Test Case Number', 'Reporter', 'Event Type','Test Suite', 'Attributes Need to Add', 'Actual Value']


class testReport:
    def __init__(self):
        self.totalRun=0
        self.totalPass=0
        self.totalFail=0
        self.totalNoReturn=0
        self.totalMiss=0
        self.totalImprove=0

    def generateReport(self, config, suiteResults):
        self.runTime=config['runTime']
        self.testTask=config['testTask']
        self.buildVersion=config['buildVersion']
        self.localhost=config['localhost']
        self.testFolder=config['testFolder']
        for suite in suiteResults:
            suite.runTime=self.runTime
            self.totalRun+=suite.totalRun
            self.totalPass+=suite.totalPass
            self.totalNoReturn+=suite.totalNoReturn
            self.totalFail+=suite.totalFail
            self.totalMiss+=suite.totalMiss
            self.totalImprove+=suite.totalImprove
        detailFileName=self.generateFile(suiteResults)
        self.generateHtml(suiteResults)
        self.generateSummary()

        return MSG

    def generateFile(self, testSuites):
        if not os.path.exists(str(self.testFolder)):
            os.makedirs(str(self.testFolder))
        for suite in testSuites:
            type=self._setType(suite)
            myXml=XMLHelper.classToXml(suite, type)
            fileName=self.testFolder+'/'+suite.name+'.xml'
            output=open(fileName, 'w')
            output.write(myXml)
            output.close()
            setattr(suite, 'detailFile', fileName)

    def generateHtml(self, testSuites):
        myHtml=HtmlDocument()
        myHtml.setHtmlTitle(TITLE)
        myHtml.append(Tag.H1(NAME))
        myHtml.append(Tag.HR())
        myHtml.append(Tag.B(SUBTITLE % (self.runTime, str(self.testTask), str(self.buildVersion))))
        table=Tag.TABLE(DEFAULT_BORDER)
        titleTR=Tag.TR()
        for field in FIELDS:
            titleTR.append(Tag.TD(Tag.B(field)))
        table.append(titleTR)
        totalTR=Tag.TR()
        totalTR.append(Tag.TD('Total'))
        totalTR.append(Tag.TD(str(self.totalRun)))
        totalTR.append(Tag.TD(str(self.totalPass)))
        totalTR.append(Tag.TD(str(self.totalNoReturn)))
        totalTR.append(Tag.TD(str(self.totalFail)))
        totalTR.append(Tag.TD(str(self.totalMiss)))
        totalTR.append(Tag.TD(str(self.totalImprove)))
        table.append(totalTR)

        for suite in testSuites:
            detailLink=suite.detailFile.replace(RESULT, 'testresult')
            moduleTR=Tag.TR()
            moduleTR.append(Tag.TD(Tag.A(suite.name, (REF %(self.localhost, str(self.testTask), str(suite.testFileName))))))
            moduleTR.append(Tag.TD(str(suite.totalRun)))
            moduleTR.append(Tag.TD(str(suite.totalPass)))
            moduleTR.append(Tag.TD(str(suite.totalNoReturn)))
            moduleTR.append(Tag.TD(str(suite.totalFail)))
            moduleTR.append(Tag.TD(str(suite.totalMiss)))
            moduleTR.append(Tag.TD(str(suite.totalImprove)))
            moduleTR.append(Tag.TD(Tag.A('Check Details', (RESREF %(self.localhost, detailLink)))))
            table.append(moduleTR)
        myHtml.append(table)
        if self.totalNoReturn:
            myHtml.append(Tag.HR())
            myHtml.append(Tag.H2(NO_RETURN))
            table=Tag.TABLE(DEFAULT_BORDER)
            titleTR=Tag.TR()
            for field in CASE_FIELDS:
                titleTR.append(Tag.TD(Tag.B(field)))
            table.append(titleTR)
            for suite in testSuites:
                for case in suite.caseTestResults:
                    if case.status=='No Return':
                        valueTR=Tag.TR()
                        valueTR.append(Tag.TD(case.testCaseName))
                        valueTR.append(Tag.TD(case.testCaseNum))
                        valueTR.append(Tag.TD(case.eventType))
                        valueTR.append(Tag.TD(case.reporter))
                        valueTR.append(Tag.TD(case.testSuite))
                        table.append(valueTR)
            myHtml.append(table)
        if self.totalFail:
            myHtml.append(Tag.HR())
            myHtml.append(Tag.H2(PARAM_ERROR))
            table=Tag.TABLE(DEFAULT_BORDER)
            titleTR=Tag.TR()
            for field in ERROR_FIELDS:
                titleTR.append(Tag.TD(Tag.B(field)))
            table.append(titleTR)
            for suite in testSuites:
                for case in suite.caseTestResults:
                    if case.status=='Fail':
                        valueTR=Tag.TR()
                        valueTR.append(Tag.TD(case.testCaseName))
                        valueTR.append(Tag.TD(case.testCaseNum))
                        valueTR.append(Tag.TD(case.reporter))
                        valueTR.append(Tag.TD(case.eventType))
                        valueTR.append(Tag.TD(case.testSuite))
                        myParam=hashMethod(case.failed)
                        valueTR.append(Tag.TD(myParam['name']))
                        valueTR.append(Tag.TD(myParam['expect']))
                        valueTR.append(Tag.TD(myParam['actual']))
                        table.append(valueTR)
            myHtml.append(table)
        if self.totalMiss:
            myHtml.append(Tag.HR())
            myHtml.append(Tag.H2(MISS_RETURN))
            table=Tag.TABLE(DEFAULT_BORDER)
            titleTR=Tag.TR()
            for field in MISS_FIELDS:
                titleTR.append(Tag.TD(Tag.B(field)))
            table.append(titleTR)
            for suite in testSuites:
                for case in suite.caseTestResults:
                    if case.status=='Miss':
                        valueTR=Tag.TR()
                        valueTR.append(Tag.TD(case.testCaseName))
                        valueTR.append(Tag.TD(case.testCaseNum))
                        valueTR.append(Tag.TD(case.reporter))
                        valueTR.append(Tag.TD(case.eventType))
                        valueTR.append(Tag.TD(case.testSuite))
                        myParam=hashMethod(case.missed)
                        valueTR.append(Tag.TD(myParam['name']))
                        valueTR.append(Tag.TD(myParam['expect']))
                        table.append(valueTR)
            myHtml.append(table)
        if self.totalImprove:
            myHtml.append(Tag.HR())
            myHtml.append(Tag.H2(IMPROVE_CASE))
            table=Tag.TABLE(DEFAULT_BORDER)
            titleTR=Tag.TR()
            for field in IMPROVE_FIELDS:
                titleTR.append(Tag.TD(Tag.B(field)))
            table.append(titleTR)
            for suite in testSuites:
                for case in suite.caseTestResults:
                    if case.status=='Improve':
                        valueTR=Tag.TR()
                        valueTR.append(Tag.TD(case.testCaseName))
                        valueTR.append(Tag.TD(case.testCaseNum))
                        valueTR.append(Tag.TD(case.reporter))
                        valueTR.append(Tag.TD(case.eventType))
                        valueTR.append(Tag.TD(case.testSuite))
                        myParam=hashMethod(case.improved)
                        valueTR.append(Tag.TD(myParam['name']))
                        valueTR.append(Tag.TD(myParam['actual']))
                        table.append(valueTR)
            myHtml.append(table)

        outFile=open(self.testFolder+'/report.html', 'w')
        myHtml.writeHtml(outFile)
        outFile.close()

    def generateSummary(self):
        itemList=os.listdir(RESULT)
        folderList=[]
        mapping={}
        for folder in itemList:
            if (os.path.isdir(RESULT+'/'+folder)):
                folderList.append(folder)
        for item in folderList:
            subFolder=os.listdir(RESULT+'/'+item)
            subFolder.sort()
            subFolder.reverse()
            mapping[item]=subFolder

        myHtml=HtmlDocument()
        myHtml.setHtmlTitle(TITLE)
        myHtml.append(Tag.H1(WELCOME))
        myHtml.append(Tag.P(DESC))
        myHtml.append(Tag.HR())

        for key in mapping.keys():
            myFolder=Tag.LI(key)
            myFolder.append(Tag.UL())
            mySubs=mapping[key]
            if len(mySubs)!=0:
                for item in mySubs:
                    myFolder.append(Tag.LI(Tag.A(item, (SUMREF %(self.localhost, key, item)))))
            myFolder.append(mySubs)
            myHtml.append(myFolder)

        outFile=open(INDEX, 'w')
        myHtml.writeHtml(outFile)
        outFile.close()

    def _setType(self, object):
        return classUtility.getType(object)+'s'




