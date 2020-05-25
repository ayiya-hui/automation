from Libs.restApiDataHandler import restApiDataHandler
from Libs.caseDbHandler import caseDbHandler
from ConfigConstants.checkParseTemplate import html_content, table_body, table_row
from string import Template

ignores=['PHBoxParser', 'PHRuleIncidentParser', 'SyslogNGParser']
output='../Public/checkNewParsers.html'

def checkNewParsers(appServer):
    """Usage: checkNewParsers.py <appServer>
    appServer - AO server."""
    myRest=restApiDataHandler(appServer)
    myData=myRest.getData('parsers', module='device')
    if myData:
        myDb=caseDbHandler('EventParsing')
        exist_modules=[]
        new_modules=[]
        modules=myDb.getAllModules()
        for key in myData.keys():
            if  key not in ignores:
                if key.replace('Parser', '') not in modules:
                    print 'New parser %s' % key
                    new_modules.append(key)
                else:
                    exist_modules.append(key)
                    print 'Old parser %s' % key
        # myRowTemp=Template(table_row)
        # myTableTemp=Template(table_body)
        # myHtmlTemp=Template(html_content)
        # old_body=''
        # new_body=''
        # old_count=''
        # new_count=''
        # if exist_modules:
        #     myRows=[]
        #     for key in exist_modules:
        #         myMap={'module':key}
        #         print myMap
        #         myRows.append(myRowTemp.substitute(myMap))
        #     if myRows:
        #         oldMap={'tableBody':''.join(myRows)}
        #         old_body=myTableTemp.substitute(oldMap)
        #         old_count=len(myRows)
        # if new_modules:
        #     newRows=[]
        #     for key in new_modules:
        #         myMap={'module':key}
        #         newRows.append(myRowTemp.substitute(myMap))
        #     if newRows:
        #         newMap={'tableBody':''.join(newRows)}
        #         new_body=myTableTemp.substitute(newMap)
        #         new_count=len(newRows)
        # htmlMap={}
        # if old_body and old_count:
        #     htmlMap['old']=old_body
        #     htmlMap['old_count']=old_count
        # if new_body and new_count:
        #     htmlMap['new']=new_body
        #     htmlMap['new_count']=new_count
        # if htmlMap:
        #     final=myHtmlTemp.substitute((htmlMap))
        #     myW=open(output, 'w')
        #     myW.write(final)
        #     myW.close()

if __name__=='__main__':
    import sys
    if len(sys.argv)!=2:
        print checkNewParsers.__doc__
        sys.exit()
    checkNewParsers(sys.argv[1])
    print 'Task is done.'
