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

PORTS={'syslog':514, 'netflow':2055}

hardcore_reasons={'PH_RULE_STAT_HIGH_PROC_COUNT':'Known issue: need traffic info to geerate abnormal traffic',
                 'PH_RULE_STAT_HIGH_TRAFFIC_FROM_SRC_FIXED_PORT':'Known issue: need traffic info to generate abnormal traffic',
                 'PH_RULE_STAT_HIGH_TRAFFIC_TO_DEST_FIXED_PORT':'Known issue: need traffic info to generate abnormal traffic',
                 'PH_RULE_STAT_HIGH_TRAFFIC_SRC_DEST_FIXED_PORT':'Known issue: need traffic info to generate abnormal traffic',
                 }

correct_grammer_cases={'PH_RULE_ESX_DISKIO_CRIT':'(AVG(guestDiskRdLatency) >= 50 OR AVG(guestDiskWrLatency)) >= 50 AND COUNT(*) >= 2',
                       'PH_RULE_SERVER_INTF_ERR_WARN':'((AVG(inIntfPktErrPct) >= 1 AND AVG(inIntfPktErrPct) <= 5) OR (AVG(outIntfPktErrPct) >= 1 AND AVG(outIntfPktErrPct) <= 5)) AND COUNT(*) >= 2',
                       'PH_RULE_NET_INTF_ERR_CRIT':'(AVG(inIntfPktErrPct) > 5 OR AVG(outIntfPktErrPct) > 5) AND COUNT(*) >= 2',
                       'PH_RULE_SERVER_INTF_ERR_CRIT':'(AVG(inIntfPktErrPct) > 5 OR AVG(outIntfPktErrPct) > 5) AND COUNT(*) >= 2',}

perf_object_list=['sys_uptime_id','sys_cpu_id', 'sys_mem_id', 'sys_stat_id', 'sys_processes_id', 'sys_disk_id']

class incidentTest(baseTest):
    def __init__(self, task, testConfig):
        baseTest.__init__(self, task, testConfig)
        self.appServer=testConfig.testServer.appServer
        self.user=testConfig.user
        self.password=testConfig.password
        self.queryHandler=queryHandler(self.appServer, user=self.user, password=self.password)
        self.deviceHandler=deviceHandler(self.appServer, user=self.user, password=self.password)
        self.restApiHandler=restApiDataHandler(self.appServer, user=self.user, password=self.password)
        if hasattr(testConfig, 'posix'):
            self.posix=True
        else:
            self.posix=False
        if testConfig.advance=='True':
            self.advance=True
        else:
            self.advance=False
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
                    self.deviceHandler.createDevice(testConf.reptDevIpAddr, testConf.deviceName, testConf.deviceType, perfObj, dataCollector=self.testConfig.testServer.dataCollector)
                else:
                    self.deviceHandler.createDevice(testConf.reptDevIpAddr, testConf.deviceName, testConf.deviceType, perfObj)
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
            for i in range(int(testConf.count)):
                for line in eventMsgs:
                    msg=generalUtility.multiReplace(line, rept)
                    if '$reporter' in line:
                        msg=msg.replace('$reporter', testConf.reptDevIpAddr)
                    if '$randomIP' in line:
                        ip=randomGen.getRandomIPAddr()
                        msg=msg.replace('$randomIP', ip)
                    if '$randomNum' in line:
                        num=randomGen.getRandomNum(1, 100)
                        msg=msg.replace('$randomNum', num)
                    temp_msg=''
                    if testConf.method=='netflow':
                        temp_msg=GenerateNetFlow.getNetFlowPacket(msg)
                    else:
                        temp_msg=msg.strip()
                    send_msg=''
                    if rawSend:
                        send_msg=GenerateRawIPData.getRawIpPacket(temp_msg, testConf.reptDevIpAddr, self.testConfig.testServer.dataCollector, PORTS[testConf.method])
                    else:
                        send_msg=msg
                    time.sleep(sleeper)
                    mySendEvent.sendoutEvent(send_msg)
                    self.msgList.append(msg)
            #retrieve incident
            time.sleep(60)
            timeout=int(ruleType.triggerWindow)+60
            if timeout>1800:
                timeout=1800
            myParams={}
            myParams['constr']=incident_query_params['SingleEvtConstr'] % (testConf.reptDevIpAddr, incidentType)
            condition, oriRet, incidentId, failDetail, veriData, debugInfo=self.retriveIncident(incidentType, testConf, timeout, myParams)
            if not condition:
                failDetail=self.eventDebug(testConf.method, self.testConfig.testServer.appServer, testConf.reptDevIpAddr, ruleType, sendTime, utcsendTime, approvedDevices)
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
            else:
                print '%s: no incident triggered' % incidentType
                testRet.info='incidentId: None'
                setattr(oriRet, 'reasons', failDetail)
            aggmsgList=[]
            if self.advance:
                if oriRet.status!='NoReturn' and incidentId and incidentId.strip():
                    #aggregate test
                    for i in range(int(testConf.count)):
                        for m in self.msgList:
                            mySendEvent.sendoutEvent(m)
                    time.sleep(60)
                    aggParams={}
                    aggParams['constr']=incident_query_advance['SingleEvtConstr'] % (incidentId, '0')
                    condition, aggRet, inId, failDetail, aggData=self.retriveIncident(incidentType, testConf, timeout, aggParams, agg=veriData)
                    if not condition:
                        failDetail=self.eventDebug(testConf.method, self.testConfig.testServer.appServer, testConf.reptDevIpAddr, ruleType, sendTime, utcsendTime, approvedDevices)
                    if failDetail:
                        setattr(aggRet, 'reasons', failDetail)
                    testRet.totalRun+=1
                    oldVal=getattr(testRet, 'total'+aggRet.status)
                    oldVal+=1
                    setattr(testRet, 'total'+aggRet.status, oldVal)
                    testRet.caseList.append(aggRet)
                    #clear test
                    if oriRet.status!='NoReturn' and hasattr(ruleType, 'clearCondition') and incidentId and incidentId.strip():
                        clearnow,clearsendTime,clearutcnow,clearutcsendTime=timeUtility.getTimeNow()
                        if ruleType.clearCondition.clearOption=='patternbased':
                            if not hasattr(myData.dataMap['default'], 'clearEventMsg'):
                                print '%s: need to add clearEventMsg' % incidentType
                            else:
                                raw_clear=getattr(myData.dataMap['default'], 'clearEventMsg')
                                if raw_clear:
                                    for line in raw_clear:
                                        clearmsg=generalUtility.multiReplace(line.strip(), rept)
                                        if '$randomIP' in line:
                                            ip=randomGen.getRandomIPAddr()
                                            clearmsg=clearmsg.replace('$randomIP', ip)
                                        self.clearMsgList.append(clearmsg)
                                        if self.posix:
                                            send_clearmsg=GenerateRawIPData.getRawIpPacket(clearmsg, testConf.reptDevIpAddr, self.testConfig.testServer.dataCollector, PORTS[testConf.method])
                                        else:
                                            send_clearmsg=clearmsg
                                    if self.clearMsgList:
                                        for i in range(int(testConf.count)):
                                            for cl_msg in self.clearMsgList:
                                                mySendEvent.sendoutEvent(cl_msg)
                                        time.sleep(120)
                        else:
                            time.sleep(float(int(ruleType.clearCondition.clearTimeWindow)+120))
                        clearParams={}
                        clearParams['constr']=incident_query_advance['SingleEvtConstr'] % (incidentId, '1')
                        condition, clearRet, incidentId, failDetail, clearData=self.retriveIncident(incidentType, testConf, timeout, clearParams, clear=aggData)
                        if not condition:
                            failDetail=self.eventDebug(testConf.method, self.testConfig.testServer.appServer, testConf.reptDevIpAddr, ruleType, clearsendTime, clearutcsendTime, approvedDevices, clearDebug=True)
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
            aggValues=clear
        while not condition:
            if timeout>0:
                retData, debugInfo=self.queryHandler.getQuery(myParams)
                if retData:
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
                oriRet, incidentId=self.verifyData(testConf, retData, adv=advanced, advValue=aggValues)
                if oriRet.status=='NoReturn':
                    if incidentType in hardcore_reasons.keys():
                        failDetail=hardcore_reasons[incidentType]
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
            for msg in msgList:
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
