
from hashUtility import hashMethod
import Util.classUtility as classUtility
import ConfigConstants.detailResultTemplate as detailResultTemplate
import ConfigConstants.summaryResultTemplate as summaryResultTemplate
import os
from Libs.XmlHandler import XmlHandler
import ConfigConstants.TestConstant as TestConstant
import shutil
from string import Template
from datetime import datetime

SPECIAL_CHARS=[':', '/']
LINK='http://$localhostIp/testresult/$linkText/report.html'
MSG='Test runs at $dateTime, build version $buildVersion, total run $runTotal, pass $passTotal, no return $noReturnTotal, fail $failTotal, missing $missTotal, extra $extraTotal'
#MAIL='Test Name: $linkText-Sender:192.168.20.214\n http link:$link\n$report'
MAIL='<p>Test Name: $linkText-Tester:10.1.2.72</p><p>http link: $link</p> <p> $report </p>'
param_list_map={'NoReturn':['case.name', 'suite.name', 'suite.taskName', 'suite.testRuleResultSummary', 'case.reasons'],
                'Fail':['case.name', 'suite.name', 'suite.taskName']}
name_map={'EventParsing':{'module':'EventParsing Module', 'sys_module':'Parser'},
          'Incident':{'module':'IncidentId', 'sys_module':'Incident Name'}}

class testReport:
    """ This class handles test result report."""
    def generateReport(self, autoResult):
        """This method generate the reports."""
        if autoResult.testType=='Official':
            result_file=TestConstant.official_result_file
        else:
            result_file=TestConstant.unofficial_result_file
        msgMap={'dateTime':autoResult.runTime,
                'buildVersion':autoResult.runVersion,
                'runTotal':autoResult.totalRun,
                'passTotal':autoResult.totalPass,
                'noReturnTotal':autoResult.totalNoReturn,
                'failTotal':autoResult.totalFail,
                'missTotal':autoResult.totalMissing,
                'extraTotal':autoResult.totalExtra}
        msg=self.substitute(MSG, msgMap)
        linkText=autoResult.testFolder.split('../Results/')[-1]
        myFile=open(result_file, 'a')
        myFile.write(linkText+'@')
        myFile.write(msg+'\n')
        myFile.close()
        self.__generateFiles(autoResult)
        report=self.__generateHtml(autoResult)
        self.__generateSummary(autoResult)
        if classUtility.getType(autoResult.sendEmail)!='NoneType':
            linkMap={'localhostIp':autoResult.localhost, 'linkText':linkText}
            link=self.substitute(LINK, linkMap)
            mailMap={'linkText':linkText, 'report':report, 'link':link}
            mailContent=self.substitute(MAIL, mailMap)
            mail_name=''
            if autoResult.batch:
                mail_name=autoResult.name+'-'+autoResult.batch
            else:
                mail_name=autoResult.name
            self.__sendEmailout(mailContent, mail_name)

        return TestConstant.report_msg

    def __sendEmailout(self, data, name_test):
        import Libs.sendEmailHandler as sendEmailHandler
        mySmtp=sendEmailHandler.sendEmailHandler()
        mySmtp.sendEmail(data, name_test)

    def __generateFiles(self, autoResult):
        if not os.path.exists(str(autoResult.testFolder)):
            if ':' in autoResult.testFolder:
                autoResult.testFolder=autoResult.testFolder.replace(':', '-')
            os.makedirs(str(autoResult.testFolder))
        for suite in autoResult.suiteList:
            for spec in SPECIAL_CHARS:
                if spec in suite.name:
                    suite.name=suite.name.replace(spec, '-')
            if '"' in suite.name:
                suite.name=suite.name.replace('"','')
            fileName=autoResult.testFolder+'/'+suite.name+'.xml'
            XmlHandler().XmlObjToFile(suite, fileName)
            setattr(suite, 'detailFile', fileName)

    def __generateHtml(self, autoResult):
        main_table=[]
        cells=[]
        for item in TestConstant.test_result_counters:
            cellMap={'tableCell':str(getattr(autoResult, item))}
            cells.append(self.substitute(detailResultTemplate.table_cell, cellMap))
        totalRowMap={'totalRow':''.join(cells)}
        total_row=self.substitute(detailResultTemplate.total_row, totalRowMap)
        main_table.append(total_row)
        for suite in autoResult.suiteList:
            detailLink=suite.detailFile.replace(TestConstant.default_result_path, 'testresult/')
            cells=[]
            for item in [suite.name, suite.taskName]:
                itemMap={'tableCell':item.encode('utf-8')}
                cells.append(self.substitute(detailResultTemplate.table_cell, itemMap))
            for count in TestConstant.test_result_counters:
                cellMap={'tableCell':str(getattr(suite, count))}
                cells.append(self.substitute(detailResultTemplate.table_cell, cellMap))
            alinkMap={'localhostIp':str(autoResult.localhost), 'detail':detailLink}
            cells.append(self.substitute(detailResultTemplate.table_cell_alink, alinkMap))
            tableRowMap={'tableRow':''.join(cells)}
            table_row=self.substitute(detailResultTemplate.table_row, tableRowMap)
            main_table.append(table_row)
        option_table=[]
        if getattr(autoResult, 'totalNoReturn'):
            no_return_table=self.getTable('NoReturn', detailResultTemplate.no_return_table, autoResult.suiteList)
            option_table.append(no_return_table)
        if getattr(autoResult, 'totalFail'):
            fail_table=self.getTable('Fail',detailResultTemplate.fail_table,autoResult.suiteList)
            option_table.append(fail_table)
        if hasattr(autoResult, 'miss'):
            miss_map= getattr(autoResult, 'miss')
            for key in name_map[autoResult.name]:
                miss_map[key]=name_map[autoResult.name][key]
            miss_rows=[]
            if miss_map:
                for key in miss_map.keys():
                    cells=[]
                    idMap={'tableCell':key}
                    cells.append(self.substitute(detailResultTemplate.table_cell, idMap))
                    nameMap={'tableCell':miss_map[key]}
                    cells.append(self.substitute(detailResultTemplate.table_cell, nameMap))
                    rowMap={'tableRow':''.join(cells)}
                    table_row=self.substitute(detailResultTemplate.table_row, rowMap)
                    miss_rows.append(table_row)
                missMap={'notImplemented':''.join(miss_rows)}
                miss_table=self.substitute(detailResultTemplate.not_implemented, missMap)
                option_table.append(miss_table)
        htmlMap={'testType':autoResult.name.encode('utf-8'),
                 'runTime':str(autoResult.runTime),
                 'runVersion':str(autoResult.runVersion),
                 'mainTable':''.join(main_table),
                 'optionTable':''.join(option_table)}
        final_html=self.substitute(detailResultTemplate.report_html, htmlMap)
        outFile=open(autoResult.testFolder+'/report.html', 'w')
        outFile.write(final_html)
        outFile.close()
        shutil.copyfile('../Public/sorttable.js', autoResult.testFolder+'/sorttable.js')

        return final_html

    def getTable(self, case_status, template_text, suiteList):
        final_rows=[]
        for suite in suiteList:
            for case in suite.caseList:
                cells=[]
                if case.status==case_status:
                    for item in param_list_map[case_status]:
                        class_name, class_param=item.split('.')
                        value=''
                        if class_name=='case':
                            value=getattr(case, class_param)
                        elif class_name=='suite':
                            value=getattr(suite, class_param)
                        if value:
                            caseMap={'tableCell':value.encode('utf-8')}
                            cells.append(self.substitute(detailResultTemplate.table_cell, caseMap))
                    if case_status=='Fail':
                        fail=[]
                        for dat in case.Fail:
                            if dat['actValue'] is None:
                                dat['actValue']='None'
                            fail.append(str(dat['param']+': EXPECT '+dat['expectValue'].encode('ascii', 'ignore')+' ACTUAL '+dat['actValue'].encode('ascii', 'ignore')))
                        failMap={'tableCell':'; '.join(fail).encode('utf-8')}
                        cells.append(self.substitute(detailResultTemplate.table_cell, failMap))
                    rowMap={'tableRow':''.join(cells)}
                    table_row=self.substitute(detailResultTemplate.table_row, rowMap)
                    final_rows.append(table_row)
        finalMap={case_status:''.join(final_rows)}
        final_table=self.substitute(template_text, finalMap)

        return final_table

    def __generateSummary(self, autoResult):
        official=''
        if os.path.exists(TestConstant.official_result_file):
            official=self.__getSummary(autoResult, 'Official')
        unofficial=''
        if os.path.exists(TestConstant.unofficial_result_file):
            unofficial=self.__getSummary(autoResult, 'Unofficial')
        final=summaryResultTemplate.summary_html_base % (official+unofficial)
        outFile=open(TestConstant.report_index_html, 'w')
        outFile.write(final)
        outFile.close()

    def __getSummary(self, autoResult, option):
        if option=='Official':
            file_path=TestConstant.official_result_file
        elif option=='Unofficial':
            file_path=TestConstant.unofficial_result_file
        myFile=open(file_path)
        myData=myFile.readlines()
        myFile.close()
        myMap={}
        myIndex=[]
        for data in myData:
            link, msg=data.split('@', 1)
            h1,year,month,day,h2,h3=link.split('-')
            dIndex=datetime(int(year), int(month), int(day))
            myMsg={}
            myMsg[link]=msg
            if dIndex not in myIndex:
                myIndex.append(dIndex)
                myMap[dIndex]=[myMsg]
            else:
                myD=myMap[dIndex]
                myD.append(myMsg)
                myMap[dIndex]=myD
        myIndex.reverse()
        contents=''
        for key in myIndex:
            contents+=summaryResultTemplate.date % key.strftime('%Y-%B-%d')
            data=myMap[key]
            for item in data:
                for subkey in item:
                    contents+=summaryResultTemplate.content % (str(autoResult.localhost), subkey, subkey)
                    contents+=summaryResultTemplate.page % item[subkey]
        final=summaryResultTemplate.content_html % (option, contents)

        return final

    def substitute(self, templateText, tempMap):
        myTemplate=Template(templateText)

        return myTemplate.substitute(tempMap)










