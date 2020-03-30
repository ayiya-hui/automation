from runBase import baseTest
import Libs.CSVHandler as CSVHandler
import Libs.datFileHandler as datFileHandler
from ConfigConstants.TestConstant import event_query_params, approved_device_params, incident_debug_params, csv_key_attrs, incident_data_path, incident_data_keys, incident_query_params, incident_query_advance, incident_aggregate, incident_clear, incident_debug_query_special, incident_alter_params
from Libs.deviceHandler import deviceHandler
from Libs.restApiDataHandler import restApiDataHandler
from Libs.queryHandler import queryHandler
from Libs.sendEventHandler import sendEventHandler
from Models.ClassLocator import getClassObj
import time, sys
import Util.timeUtility as timeUtility
import Util.generalUtility as generalUtility
import Util.randomGen as randomGen
import Libs.expressionReader as expressionReader
import Libs.expressionEval as expressionEval
import Libs.rawUdpSendHandler as rawUdpSendHandler
import Libs.GenerateRawIPData as GenerateRawIPData
import Libs.GenerateNetFlowData as GenerateNetFlow
from Util.testUtility import xmlEscape
from ConfigConstants.groupConstants import group_name_key
from Libs.psqlHandler import psqlHandler

PORTS={'syslog':514, 'netflow':2055}

hardcore_reasons={'PH_RULE_STAT_HIGH_PROC_COUNT':'Known issue: need traffic info to geerate abnormal traffic',
                 'PH_RULE_STAT_HIGH_TRAFFIC_FROM_SRC_FIXED_PORT':'Known issue: need traffic info to generate abnormal traffic',
                 'PH_RULE_STAT_HIGH_TRAFFIC_TO_DEST_FIXED_PORT':'Known issue: need traffic info to generate abnormal traffic',
                 'PH_RULE_STAT_HIGH_TRAFFIC_SRC_DEST_FIXED_PORT':'Known issue: need traffic info to generate abnormal traffic',
                 'PH_RULE_NFS_DISK_SPACE_CRIT':'Known issue: need to create a Storage device type. So far no template availble',
                 'PH_RULE_NFS_DISK_SPACE_WARN':'Known issue: need ot create a Storage device type. So far no template availble',
                 'PH_RULE_ACCELOPS_COLLECTOR_DOWN':'Known issue for VA: VA has no collectors',
                 'PH_RULE_ACCELOPS_WORKER_DOWN':'Known issue for VA: VA has no workers',
                 }

correct_grammer_cases={'PH_RULE_ESX_DISKIO_CRIT':'(AVG(guestDiskRdLatency) >= 50 OR AVG(guestDiskWrLatency)) >= 50 AND COUNT(*) >= 2',
                       'PH_RULE_SERVER_INTF_ERR_WARN':'((AVG(inIntfPktErrPct) >= 1 AND AVG(inIntfPktErrPct) <= 5) OR (AVG(outIntfPktErrPct) >= 1 AND AVG(outIntfPktErrPct) <= 5)) AND COUNT(*) >= 2',
                       'PH_RULE_NET_INTF_ERR_CRIT':'(AVG(inIntfPktErrPct) > 5 OR AVG(outIntfPktErrPct) > 5) AND COUNT(*) >= 2',
                       'PH_RULE_SERVER_INTF_ERR_CRIT':'(AVG(inIntfPktErrPct) > 5 OR AVG(outIntfPktErrPct) > 5) AND COUNT(*) >= 2',}

perf_object_list=['sys_uptime_id','sys_cpu_id', 'sys_mem_id', 'sys_stat_id', 'sys_processes_id', 'sys_disk_id']

incident_sql_cmd="SELECT incident_id, last_seen_time FROM ph_incident WHERE incident_et='%s' AND orig_device_ip='%s' AND last_seen_time>%s;"

incident_query="SELECT * FROM ph_incident;"

incident_delete="DELETE FROM ph_incident;"

ip_in_privatenet=['PH_RULE_EXCESS_DENY_DEST']

class incidentTest(baseTest):
    def __init__(self, task, testConfig):
        baseTest.__init__(self, task, testConfig)
        self.appServer=testConfig.testServer.appServer
        self.user=testConfig.user
        self.password=testConfig.password
        self.queryHandler=queryHandler(self.appServer, user=self.user, password=self.password)
        self.deviceHandler=deviceHandler(self.appServer, user=self.user, password=self.password)
        self.restApiHandler=restApiDataHandler(self.appServer, user=self.user, password=self.password)
        self.psql=psqlHandler(self.appServer)
        if hasattr(testConfig, 'posix'):
            self.posix=True
        else:
            self.posix=False
        self.advance=testConfig.advance
        if testConfig.noSend==True:
            self.sendNoEvent=True
        else:
            self.sendNoEvent=False
        self.msgList=[]
        self.clearMsgList=[]

    def getGlobalData(self):
        self.deviceHandler.getAllDevices()
        self.deviceHandler.getApplicableDevices()
        map={}
        map['devices']=self.deviceHandler.devices
        map['applicableDevices']=self.deviceHandler.applicableDevices
        rawPerfObj=self.restApiHandler.getData('perfObject')
        perfMap={}
        for perfId in rawPerfObj:
            pType=rawPerfObj[perfId].type
            typeName=pType.name.lower()+'_id'
            if typeName in perf_object_list:
                perfMap[typeName]=perfId
        if perfMap:
            map['perfObj']=perfMap

        return map

    def getTestList(self, taskFiles):
        rawtestMap=self.restApiHandler.getData('rule')
        testMap={}
        for mapKey in rawtestMap.keys():
            if rawtestMap[mapKey].active=='true':
                if 'dataCreationType' in rawtestMap[mapKey].attribute.keys() and rawtestMap[mapKey].attribute['dataCreationType']=="SYSTEM" :
                    testMap[mapKey]=rawtestMap[mapKey]

        indexMap={}
        for key in testMap.keys():
            incidentType=testMap[key].incidentType.split('$')[-1]
            indexMap[incidentType]=testMap[key]
        finalMap={}
        if taskFiles.lower()=='all':
            finalMap=indexMap
        else:
            for index in taskFiles.split(','):
                if index in indexMap.keys():
                    finalMap[index]=indexMap[index]

        return finalMap

    def getCommonData(self, taskFiles):
        return CSVHandler.getDataFromFile('incidentData', self.path+'/incidentData.csv', None, None)

    def cleanDb(self):
        rawBefore=self.psql.execute(incident_query)
        if rawBefore:
            self.psql.execute(incident_delete, pick=False)
        rawAgain=self.psql.execute(incident_query)
        if not rawAgain:
            print 'Existing incidents are cleaned.'
        else:
            print 'Existing incidents are not cleaned.'

    def run(self, ruleType, testKey):
        fb_type=ruleType.filterOperators.type
        sleeper=0
        if fb_type=='FOLLOWED_BY':
            sleeper=5
        incidentType=ruleType.incidentType.split('$')[-1]
        ruleId=ruleType.attribute['id']
        if incidentType not in self.testConfig.commonData.keys():
            print 'Incidnet Name %s Incident Type %s is NOT implemented.' % (ruleType.name, incidentType)
            testRet=None
        else:
            testConf=self.testConfig.commonData[incidentType]
            if testConf.reptDevIpAddr=='$localhost':
                testConf.reptDevIpAddr=self.testConfig.localhost
            elif testConf.reptDevIpAddr=='$appServer':
                testConf.reptDevIpAddr=self.appServer
            allDevices=self.testConfig.globalData['devices']
            approvedDevices=self.testConfig.globalData['applicableDevices']
            perfObj=self.testConfig.globalData['perfObj']
            #create device if needed
            if not allDevices or (testConf.createDevice and not testConf.reptDevIpAddr in allDevices.keys()):
                if testConf.domainController:
                    print 'create domain controller %s' % testConf.reptDevIpAddr
                    self.deviceHandler.createDevice(testConf.reptDevIpAddr, testConf.deviceName, testConf.deviceType, perfObj, dataCollector=self.testConfig.testServer.dataCollector)
                else:
                    print 'create %s device %s' % (testConf.deviceType, testConf.reptDevIpAddr)
                    self.deviceHandler.createDevice(testConf.reptDevIpAddr, testConf.deviceName, testConf.deviceType, perfObj)
            else:
                print 'device %s is already exist.' % testConf.reptDevIpAddr
                #in case to make it domain controller
                if testConf.domainController:
                    print 'make domain controller %s' % testConf.reptDevIpAddr
                    self.deviceHandler.createDevice(testConf.reptDevIpAddr, testConf.deviceName, testConf.deviceType, perfObj, dataCollector=self.testConfig.testServer.dataCollector)

            #get raw data
            myData=datFileHandler.getData(self.path+'/'+incident_data_path+'/'+incidentType+'.dat', incident_data_keys)
            #send raw event to trigger incident
            if not myData.dataMap:
                print 'Fail to get test data. Exit.'
                exit()
            now,sendTime,utcnow,utcsendTime=timeUtility.getTimeNow()
            rept={}
            rept['$localhost']=self.testConfig.localhost
            rept['$dataCollector']=self.testConfig.testServer.dataCollector
            eventMsgs=myData.dataMap['default'].eventMsg
            if eventMsgs is None:
               print '%s: No eventMsg exist.' % incidentType
               exit()
            rawSend=False
            if self.posix and testConf.reptDevIpAddr!=self.testConfig.localhost:
                rawSend=True
            if rawSend:
                mySendEvent=rawUdpSendHandler.rawUdpSendHandler(self.testConfig.testServer.dataCollector, PORTS[testConf.method])
            else:
                mySendEvent=sendEventHandler(testConf.method, self.testConfig.testServer.dataCollector)
            sendSleep=0
            randomIPs=[]
            randomNums=[]
            ip=''
            num=''
            for i in range(int(testConf.count)):
                for line in eventMsgs:
                    msg=generalUtility.multiReplace(line, rept)
                    if '$reporter' in line:
                        msg=msg.replace('$reporter', testConf.reptDevIpAddr)
                    if '$randomIP' in line:
                        repeat=True
                        while repeat:
                            ip=randomGen.getRandomIPAddr()
                            if ip not in randomIPs:
                                if testConf.incidentType not in ip_in_privatenet:
                                    msg=msg.replace('$randomIP', ip)
                                    randomIPs.append(ip)
                                    repeat=False
                                else:
                                    if ip.split('.')[0] in ['10']:
                                        msg = msg.replace('$randomIP', ip)
                                        randomIPs.append(ip)
                                        repeat = False
                    if '$randomNum' in line:
                        num_repeat=True
                        while num_repeat:
                            num=randomGen.getRandomNum(1, 1000)
                            if num not in randomNums:
                                msg=msg.replace('$randomNum', num)
                                randomNums.append(num)
                                num_repeat=False
                    if '$group_' in line:
                        groupName=line.split('$group_')[-1].split('@')[0]
                        groupItem=self.restApiHandler.getData(group_name_key[groupName], module='namedValue')
                        value=''
                        if groupItem:
                            rawValue=groupItem[group_name_key[groupName]].namedValues[0]
                            if '-' in rawValue:
                                temp=rawValue.split('-')[0].split('.')
                                temp[-1]='100'
                                value='.'.join(temp)
                            else:
                                value=rawValue
                        msg=msg.replace('$group_'+groupName+'@', value)
                    temp_msg=''
                    if testConf.method=='netflow':
                        temp_msg=GenerateNetFlow.getNetFlowPacket(msg)
                    else:
                        temp_msg=msg.strip()
                    send_msg=''
                    if rawSend:
                        if testConf.method=='syslog':
                            temp_msg=temp_msg.encode('ascii', 'ignore')
                        send_msg=GenerateRawIPData.getRawIpPacket(temp_msg, testConf.reptDevIpAddr, self.testConfig.testServer.dataCollector, PORTS[testConf.method])
                    else:
                        send_msg=msg
                    time.sleep(sleeper)
                    if not self.sendNoEvent:
                        mySendEvent.sendoutEvent(send_msg, utf_8=False)

                    else:
                        print 'No event sent being configured.'
                    self.msgList.append(msg)
            #retrieve incident
            sendSleep = 120
            time.sleep(sendSleep)
            timeout=int(ruleType.triggerWindow)+180
            myParams={}
            myParams['constr']=incident_query_params['SingleEvtConstr'] % (testConf.reptDevIpAddr, incidentType)
            if self.sendNoEvent:
                print 'Query:,', myParams['constr']
            condition, oriRet, incidentId, failDetail, veriData, debugInfo=self.retriveIncident(incidentType, testConf, timeout, myParams)
            incident_id_sql=None
            if not condition: #check CMDB for incident
                rawResult=self.psql.execute(incident_sql_cmd % (incidentType, testConf.reptDevIpAddr, sendTime*1000))
                if rawResult:
                    incident_id_sql=rawResult[0][0]
                    condition=True
                    failDetail='Incident Id found in SQL but not from query.'
                else:
                    print 'no id in SQL'
            if not condition and not self.sendNoEvent:
                failDetail="need debug" #self.eventDebug(testConf.method, self.testConfig.testServer.appServer, testConf.reptDevIpAddr, ruleType, sendTime, utcsendTime, approvedDevices)
            testRet=getClassObj('TestSuiteResult', module='autoTest')
            testRet.name=testConf.name
            testRet.type=incidentType
            testRet.ruleId=ruleId
            testRet.queryString=myParams['constr']
            testRet.rawMsg=self.msgList
            testRet.testMethod=testConf.method
            testRet.reptDevIpAddr=testConf.reptDevIpAddr
            testRet.taskName='Incident'
            testRet.totalRun=1
            testRet.debugInfo=debugInfo
            setattr(testRet, 'total'+oriRet.status, 1)
            testRet.caseList.append(oriRet)
            if incidentId:
                print '%s: incident triggered with id: %s' % (incidentType, incidentId)
                testRet.info='incidentId: '+incidentId
            elif incident_id_sql:
                print '%s: incident triggered with id from sql: %s' % (incidentType, incident_id_sql)
                testRet.info='incidentId from SQL: '+incident_id_sql
                setattr(oriRet, 'reasons', failDetail)
            else:
                print '%s: no incident triggered' % incidentType
                testRet.info='incidentId: None'
                setattr(oriRet, 'reasons', failDetail)
            aggmsgList=[]
            if self.advance in ['aggregate', 'both']:
                if oriRet.status!='NoReturn' and incidentId and incidentId.strip():
                    #aggregate test
                    for i in range(int(testConf.count)):
                        for m in self.msgList:
                            mySendEvent.sendoutEvent(m, utf_8=False)
                    time.sleep(60)
                    aggParams={}
                    aggParams['constr']=incident_query_advance['SingleEvtConstr'] % (incidentId, '0')
                    condition, aggRet, inId, failDetail, aggVeriData, aggData=self.retriveIncident(incidentType, testConf, timeout, aggParams, agg=veriData)
                    if not condition:
                        failDetail=self.eventDebug(testConf.method, self.testConfig.testServer.appServer, testConf.reptDevIpAddr, ruleType, sendTime, utcsendTime, approvedDevices)
                    if failDetail:
                        setattr(aggRet, 'reasons', failDetail)
                    testRet.totalRun+=1
                    oldVal=getattr(testRet, 'total'+aggRet.status)
                    oldVal+=1
                    setattr(testRet, 'total'+aggRet.status, oldVal)
                    testRet.caseList.append(aggRet)
            if self.advance in ['clear', 'both']: #clear test
                if oriRet.status!='NoReturn' and hasattr(ruleType, 'clearCondition') and incidentId and incidentId.strip():
                    clearnow,clearsendTime,clearutcnow,clearutcsendTime=timeUtility.getTimeNow()
                    if ruleType.clearCondition.clearOption=='patternbased':
                        if not hasattr(myData.dataMap['default'], 'clearEventMsg'):
                            print '%s: need to add clearEventMsg' % incidentType
                        else:
                            raw_clear=getattr(myData.dataMap['default'], 'clearEventMsg')
                            time.sleep(600)
                            if raw_clear:
                                for line in raw_clear:
                                    clearmsg=generalUtility.multiReplace(line.strip(), rept)
                                    if '$reporter' in line:
                                        clearmsg=clearmsg.replace('$reporter', testConf.reptDevIpAddr)
                                    if '$randomIP' in line:
                                        ip=randomGen.getRandomIPAddr()
                                        clearmsg=clearmsg.replace('$randomIP', ip)
                                    if self.posix:
                                        send_clearmsg=GenerateRawIPData.getRawIpPacket(clearmsg.encode('ascii', 'ignore'), testConf.reptDevIpAddr, self.testConfig.testServer.dataCollector, PORTS[testConf.method])
                                    else:
                                        send_clearmsg=clearmsg
                                    self.clearMsgList.append(send_clearmsg)
                                if self.clearMsgList:
                                    for i in range(int(testConf.count)):
                                        for cl_msg in self.clearMsgList:
                                            mySendEvent.sendoutEvent(cl_msg, utf_8=False)
                                    time.sleep(120)
                    else:
                        time.sleep(float(int(ruleType.clearCondition.clearTimeWindow)+120))
                    clearParams={}
                    clearParams['constr']=incident_query_advance['SingleEvtConstr'] % (incidentId, '1')
                    condition, clearRet, incidentId, failDetail, clearVari, clearData=self.retriveIncident(incidentType, testConf, timeout, clearParams, clear=True)
                    if not condition:
                        failDetail="need debug" #self.eventDebug(testConf.method, self.testConfig.testServer.appServer, testConf.reptDevIpAddr, ruleType, clearsendTime, clearutcsendTime, approvedDevices, clearDebug=True)
                    if failDetail:
                        setattr(clearRet, 'reasons', failDetail)
                    print 'clear name: %s' % clearRet.name
                    testRet.totalRun+=1
                    oldVal=getattr(testRet, 'total'+clearRet.status)
                    oldVal+=1
                    setattr(testRet, 'total'+clearRet.status, oldVal)
                    testRet.caseList.append(clearRet)
            mySendEvent.close()

        return testRet

    def retriveIncident(self, incidentType, testConf, timeout, myParams, agg=False, clear=False):
        condition=False
        failDetail=''
        incidentId=''
        oriRet=''
        advanced=''
        aggValues=''
        veriData={}
        if agg:
            advanced='aggregate'
            aggValues=agg
        if clear:
            advanced='clear'
        if timeout>1800:
            print '%s: timeout %s is larger than 30 minutes. For test purpose, reduce to 30 minutes' % (incidentType, timeout)
            timeout=1800
        while not condition:
            if timeout>0:
                rawData, debugInfo=self.queryHandler.getQuery(myParams)
                if rawData:
                    #handle multiple reporting ip case
                    retData={}
                    for key in rawData.keys():
                        if ',' in key:
                            head, tail=key.split('@')
                            for item in tail.split(','):
                                retData[head+'@'+item]=rawData[key]
                        else:
                            retData[key]=rawData[key]
                    if agg:
                        for key in incident_clear.keys():
                            if key=='count':
                                veriData[key]=retData[incidentType+'@'+testConf.reptDevIpAddr][0].attributes['count']
                            if key=='incidentFirstSeen':
                                veriData[key]=retData[incidentType+'@'+testConf.reptDevIpAddr][0].attributes['incidentFirstSeen']
                            if key=='incidentLastSeen':
                                veriData[key]=retData[incidentType+'@'+testConf.reptDevIpAddr][0].attributes['incidentLastSeen']
                        if veriData['count']<agg['count']:
                            retData=''
                    else:
                        for key in incident_aggregate.keys():
                            if key=='count':
                                veriData[key]=str(int(retData[incidentType+'@'+testConf.reptDevIpAddr][0].attributes['count'])+1)
                            elif key=='incidentFirstSeen':
                                veriData[key]=retData[incidentType+'@'+testConf.reptDevIpAddr][0].attributes['incidentFirstSeen']
                oriRet, incidentId=self.verifyData(testConf, rawData, adv=advanced, advValue=aggValues)
                if oriRet.status=='NoReturn':
                    if incidentType in hardcore_reasons.keys():
                        failDetail=hardcore_reasons[incidentType]
                        condition=True
                        break
                    elif self.sendNoEvent:
                        condition=True
                        break
                    else:
                        time.sleep(60)
                        timeout=timeout-60
                else:
                    condition=True
                    break
            else:
                break

        return condition, oriRet, incidentId, failDetail, veriData, debugInfo

    def verifyData(self, testConf, retData, adv=False, advValue=False):
        dataKey=testConf.incidentType+'@'+testConf.reptDevIpAddr
        incidentId=''
        resObj=getClassObj('TestCaseResult', module='autoTest')
        if adv:
            resObj.name=testConf.name+'-'+adv+'('+testConf.incidentType+')'
        else:
            resObj.name=testConf.name+'('+testConf.incidentType+')'
        if retData:
            if dataKey in retData.keys():
                resObj.status='Pass'
                incidentId=retData[dataKey][0].attributes['incidentId']
                if adv and advValue:
                    for key in advValue.keys():
                        map={}
                        map['param']=key
                        map['actValue']=retData[dataKey][0].attributes[key]
                        map['expectValue']=advValue[key]
                        if advValue[key]!=retData[dataKey][0].attributes[key]:
                            resObj.status='Fail'
                            resObj.Fail.append(map)
                        else:
                            resObj.Pass.append(map)
            else:
                resObj.status='NoReturn'
        else:
            resObj.status='NoReturn'

        return resObj, incidentId

    def eventDebug(self, method, appServer, ip, ruleType, sendTime, utcsendTime, approved, clearDebug=False):
        """This function is to troubleshoot why an incident is not get triggered. It will go over SingleConstriant, GroupConstriant and GroupBy for clues and report the error."""
        reason=''
        groupCon=False
        groupConstr=False
        groupby=False
        groupbyConstr=False
        singleConstr=False
        my_debug=clearDebug
        if hasattr(ruleType, 'eventFilter') and ruleType.eventFilters[0].groupConstraint is not None:
            if ruleType in correct_grammer_cases.keys():
                groupCon=correct_grammer_cases[ruleType]
            else:
                groupCon=ruleType.eventFilters[0].groupConstraint
        if hasattr(ruleType, 'eventFilter') and ruleType.eventFilters[0].groupBy is not None:
            groupby=ruleType.eventFilters[0].groupBy
        if my_debug:
            if ruleType.clearCondition.clearOption=='patternbased':
                if hasattr(ruleType.clearCondition.clearEventFilters, 'singleConstraint') and ruleType.clearCondition.clearEventFilters.singleConstraint is not None:
                    singleConstr=expressionReader.expressionReader(ruleType.clearCondition.clearEventFilters.singleConstraint, appServer)
                if hasattr(ruleType.clearCondition.clearEventFilters, 'groupConstraint') and ruleType.clearCondition.clearEventFilters.groupConstraint is not None:
                    groupConstr=expressionReader.expressionReader(ruleType.clearCondition.clearEventFilters.groupConstraint, appServer, option='group')
                if hasattr(ruleType.clearCondition.clearEventFilters, 'groupBy') and ruleType.clearCondition.clearEventFilters.groupBy is not None:
                    groupbyConstr=ruleType.clearCondition.clearEventFilters.groupBy.split(',')
        else:
            if hasattr(ruleType, 'eventFilter') and ruleType.eventFilters[0].singleConstraint is not None:
                singleConstr=expressionReader.expressionReader(ruleType.eventFilters[0].singleConstraint, appServer)
            if groupCon:
                groupConstr=expressionReader.expressionReader(groupCon, appServer, option='group')
            if groupby:
                groupbyConstr=groupby.split(',')
        if method=='netflow':
            paramKey=event_query_params
        else:
            paramKey=incident_debug_params
        debugParams={}
        for key in paramKey.keys():
            debugParams[key]=paramKey[key]
        debugData={}
        msgList=[]
        if not my_debug:
            msgList=self.msgList
        else:
            msgList=self.clearMsgList
        if len(msgList):
            for msg in msgList[0]:
                msg=xmlEscape(msg)
                if ruleType.name in incident_debug_query_special.keys():
                    debugParams['constr']=incident_alter_params['SingleEvtConstr'] % incident_debug_query_special[ruleType.name]
                else:
                    debugParams['constr']=incident_debug_params['SingleEvtConstr'] % msg
                subData, my_debug=self.queryHandler.getQuery(debugParams)
                if subData:
                    for key in subData:
                        debugData[key]=subData[key]
        if debugData:
            key=debugData.keys()[0]
            finalMsgs=[]
            for msg in debugData[key]:
                rTime, zone=timeUtility.getUTimeFromString(msg.attributes['phRecvTime'])
                if zone=='UTC':
                    if rTime+600 >= utcsendTime:
                        finalMsgs.append(msg)
                else:
                    if rTime+600 >= sendTime:
                        finalMsgs.append(msg)
            if finalMsgs:
               check, reason=expressionEval.expressionEval(finalMsgs, singleConstr, groupConstr, groupbyConstr, approved)
            else:
                reason='no timely events in eventdb'
        else:
            reason='no event received in eventdb'

        return reason

    def getEventType(self):
        pass
