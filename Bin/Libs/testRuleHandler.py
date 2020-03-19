from incidentHandler import incidentHandler
from Util.localhostIp import getLocalhostIp

def testRule(appServer, ruleId=False, ruleData=False):
    """Usage: testRule.py appServer [ruleId=ruleId, ruleData=ruleData]"""
    myHandler=incidentHandler(appServer)
    sys_rule_id=''
    pause=0
    if ruleData:
        sys_rule_id=ruleData['ruleId']
    elif ruleId:
        myRule=myHandler.getRule(ruleId)
        if myRule:
            sys_rule_id=myRule.attribute['id']
            fb_type=myRule.filterOperators.type
            if fb_type=='FOLLOWED_BY':
                pause=5
    dataMap={}
    dataMap['pause']=pause
    count=0
    if ruleData:
        dataMap['reportIp']=ruleData['reportIp']
        dataMap['rawData']=ruleData['rawMsg']
    else:
        myParam=myHandler.getTestRuleParameter(ruleId)
        count=int(myParam.count)
        reportIp=''
        if myParam:
            reportIp=myParam.reptDevIpAddr
            if reportIp=='$localhost':
                reportIp=getLocalhostIp()
            if reportIp=='$appServer':
                reportIp=appServer
        myData=myHandler.getRawData(rule_id)
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
            dataMap['pause']=0
            dataMap['reportIp']=reportIp
            dataMap['rawData']=dataList
    status=''
    msg=''
    if dataMap and sys_rule_id:
        status, msg=myHandler.testRule(sys_rule_id, count, dataMap)

    return status, msg

if __name__=='__main__':
    import sys
    if len(sys.argv)!=3:
        print testRule.__doc__
        sys.exit()
    appServer=sys.argv[1]
    ruleId=sys.argv[2]
    testRule(appServer, ruleId=ruleId)
