from Libs.incidentHandler import incidentHandler
from Util.localhostIp import getLocalhostIp
from ConfigConstants.ruleTestTemplate import html_content, table_body, test_table_row, other_table_row
from string import Template
import re

test_rule_errors={'Syntax Error':'Rule Syntax Error',
                  'Filter Mismatch':'Event does not match Rule filter',
                  'Summary Dropped':'RuleMaster dropped Rule state summary from RuleWorker'}

test_rule_exps={}
for key in test_rule_errors.keys():
    test_rule_exps[key]=re.compile(test_rule_errors[key])

output='../Public/ruleTest.html'

def testRule(appServer, rule_id):
    """Usage: testRule.py appServer, ruleId"""
    myHandler=incidentHandler(appServer)
    myRules={}
    autoParams=myHandler.getAutoParams()
    if rule_id.lower()=='all':
        myRules=myHandler.getAllRules()
    else:
        for item in rule_id.split(','):
            myRules[item]=myHandler.getRule(item)
    test_result={}
    netflow_rules={}
    not_implemented_rules={}
    if len(myRules):
        for rule_key in myRules.keys():
            if rule_key not in autoParams.keys():
                not_implemented_rules[rule_key]=myRules[rule_key].name
            elif autoParams[rule_key].method=='netflow':
                netflow_rules[rule_key]=myRules[rule_key].name
            else:
                print 'Testing rule %s' % rule_key
                sys_rule_id=myRules[rule_key].attribute['id']
                pause=0
                fb_type=myRules[rule_key].filterOperators.type
                if fb_type=='FOLLOWED_BY':
                    pause=5
                myParam=autoParams[rule_key]
                reportIp=''
                if myParam:
                    reportIp=myParam.reptDevIpAddr
                    if reportIp=='$localhost':
                        reportIp=getLocalhostIp()
                    if reportIp=='$appServer':
                        reportIp=appServer
                    if myParam.createDevice:
                        myHandler.createDevice(myParam.reptDevIpAddr, myParam.deviceName, myParam.deviceType, domain=myParam.domainController)
                    myData=myHandler.getRawData(rule_key)
                if myData:
                    dataList=[]
                    for item in myData.dataMap['default'].eventMsg:
                        if '$reporter' in item:
                            item=item.replace('$reporter', reportIp)
                        if '$localhost' in item:
                            item=item.replace('$localhost', getLocalhostIp())
                        if '$appServer' in item:
                            item=item.replace('$appServer', appServer)
                        dataList.append(item)
                    dataMap={}
                    dataMap['pause']=pause
                    dataMap['reportIp']=reportIp
                    dataMap['rawData']=dataList
                    status, msg=myHandler.testRule(sys_rule_id, int(myParam.count), dataMap)
                    reason=''
                    if status=='Failure':
                        matched=''
                        for key in test_rule_exps.keys():
                            match=test_rule_exps[key].search(msg)
                            print key, match
                            if match:
                                matched=key
                                break
                        reason=matched
                    elif status=='Unfinish':
                        rasson='timeout (10 minutes)'
                    elif status=='Success':
                        reason='pass'
                map={}
                map['name']=myRules[rule_key].name
                map['status']=status
                map['reason']=reason
                test_result[rule_key]=map
                print '%s %s %s' % (rule_key, status, reason)
    writeHtml(test_result, netflow_rules, not_implemented_rules)


def writeHtml(result_map, netflow_map, nosupport_map):
    myTestRowTemp=Template(test_table_row)
    myOtherRowTemp=Template(other_table_row)
    myTableTemp=Template(table_body)
    myHtmlTemp=Template(html_content)
    test_body=''
    netflow_body=''
    nosupport_body=''
    test_count=0
    netflow_count=0
    nosupport_count=0
    if result_map:
        testRows=[]
        for key in result_map.keys():
            myMap={}
            myMap['id']=key
            myMap['name']=result_map[key]['name']
            myMap['result']=result_map[key]['status']
            myMap['reason']=result_map[key]['reason']
            testRows.append(myTestRowTemp.substitute(myMap))
        if testRows:
            testMap={'tableBody':''.join(testRows)}
            test_body=myTableTemp.substitute(testMap)
            test_count=len(testRows)
    if netflow_map:
        netflowRows=[]
        for key in netflow_map.keys():
            myMap={}
            myMap['id']=key
            myMap['name']=netflow_map[key]
            netflowRows.append(myOtherRowTemp.substitute(myMap))
        if netflowRows:
            netflowMap={'tableBody':''.join(netflowRows)}
            netflow_body=myTableTemp.substitute(netflowMap)
            netflow_count=len(netflowRows)
    if nosupport_map:
        nosupportRows=[]
        for key in nosupport_map.keys():
            myMap={}
            myMap['id']=key
            myMap['name']=nosupport_map[key]
            nosupportRows.append(myOtherRowTemp.substitute(myMap))
        if nosupportRows:
            nosupportMap={'tableBody':''.join(nosupportRows)}
            nosupport_body=myTableTemp.substitute(nosupportMap)
            nosupport_count=len(nosupportRows)
    htmlMap={}
    htmlMap['test']=test_body
    htmlMap['test_count']=test_count
    htmlMap['netflow']=netflow_body
    htmlMap['netflow_count']=netflow_count
    htmlMap['nosupport']=nosupport_body
    htmlMap['nosupport_count']=nosupport_count
    if htmlMap:
        final=myHtmlTemp.substitute((htmlMap))
        myW=open(output, 'w')
        myW.write(final)
        myW.close()

if __name__=='__main__':
    import sys
    if len(sys.argv)!=3:
        print testRule.__doc__
        sys.exit()
    appServer=sys.argv[1]
    ruleId=sys.argv[2]
    testRule(appServer, ruleId)
