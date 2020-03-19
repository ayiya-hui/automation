from runBase import baseTest
import Libs.CSVHandler as CSVHandler
import Libs.datFileHandler as datFileHandler
from Libs.restApiDataHandler import restApiDataHandler
from ConfigConstants.TestConstant import incident_debug_params, event_data_keys, event_query_params, event_ignore_params, event_replace_symbol
import Util.generalUtility as generalUtility
import AutoTestUtil.custIdUtil as custIdUtil
from Libs.queryHandler import queryHandler
from Libs.sendEventHandler import sendEventHandler
from Models.ClassLocator import getClassObj
import time, os
import Util.timeUtility as timeUtility
from Util.testUtility import processList, xmlEscape
import pdb

ignore_space_params=['eventName','hwComponentName', 'winLogonType', 'vmwEventMsg', 'usrMsg', 'icmpCode', 'errReason', 'vulnCVEId', 'devEventTypeGrp']
msg_too_long=['CiscoIPS']
no_raw_send=['WinOSWmi_30','WinOSWmi_31', 'WinOSWmi_32']
ignore_param=set(['eventName',])
parser_holdon_module=['CiscoFWSM','IronportMail','CiscoPIX','IISViaSnare','MicrosoftIAS','WinOS']
parser_holdon_eventtype=['Cisco-IronPort-Mail-Bytes','Cisco-IronPort-Mail-Subject','Cisco-IronPort-Mail-PolicyMatch','Cisco-IronPort-Mail-Final-SpamNegative','Cisco-IronPort-Mail-Interim-SpamNegative','Cisco-IronPort-Mail-AVPositive-Dropped','Cisco-IronPort-Mail-AVNegative','FWSM-302014','PIX-302014','IIS-FTP-Login-Failure','Win-IAS-FailedAuth','Win-Security-592','Win-Security-593','Win-Security-576','Win-Security-560','Win-Security-578','Win-Security-567']


class eventParsingTest(baseTest):
    def __init__(self, task, testConfig):
        baseTest.__init__(self, task, testConfig)
        self.appServer=testConfig.testServer.appServer
        self.user=testConfig.user
        self.password=testConfig.password
	self.testType=testConfig.testType
        self.excludeModules=self.getExcludes(testConfig.testTask)
        self.queryHandler=queryHandler(self.appServer, user=self.user, password=self.password)
        if hasattr(testConfig, 'posix'):
            self.posix=True
        else:
            self.posix=False

    def getExcludes(self, tasks):
        excludes=[]
        for task in tasks:
            if task.exclude is not None:
                myExc=task.exclude.split(',')
                for item in myExc:
                    if item not in excludes:
                        excludes.append(item)

        return excludes

    def getGlobalData(self):
        myRestApi=restApiDataHandler(self.appServer, user=self.user, password=self.password)
        myCusts=myRestApi.getData('domain')

        return myCusts

    def getCommonData(self, taskFiles):
        indexModule={}
        if taskFiles.lower()=='all':
            folders=os.listdir(self.path)
            if '.svn' in folders:
                folders.remove('.svn')
        else:
            folders=taskFiles.split(',')
        for f in folders:
            rawData=CSVHandler.getDataFromFile('eventParsingData', self.path+'/'+f+'/Index', None, None, asCsv=False)
            for key in rawData.keys():
                if rawData[key].reptDevIpAddr=='$localhost':
                    rawData[key].reptDevIpAddr=self.testConfig.localhost
                if f not in indexModule.keys():
                    indexModule[f]={}
                    indexModule[f][key]=rawData[key]
                else:
                    indexModule[f][key]=rawData[key]
        self.commons=indexModule

        return self.commons

    def getTestList(self, taskFiles):
        if taskFiles.lower()=='all':
            map=self.commons
        else:
            map={}
            for key in taskFiles.split(','):
                map[key]=self.commons[key]
        if self.excludeModules:
            for item in self.excludeModules:
                if item in map.keys():
                    del map[item]

        return map

    def run(self, etype, module):
        params={}
        path=self.path+'/'+module
        mySendEvent=''
        for key in etype.keys():
            myVal=etype[key]
            if myVal.key:
                myKey=myVal.reptDevIpAddr+' ('+myVal.key+')'
            else:
                myKey=myVal.reptDevIpAddr
            fileName=myVal.eventType+'.dat'
            for rep in event_replace_symbol:
                if rep in fileName:
                    fileName=fileName.replace(rep, '$')
            myData=datFileHandler.getData(path+'/'+fileName, event_data_keys)
            if myVal.reptDevIpAddr==self.testConfig.localhost:
                mkey=myKey.replace(myVal.reptDevIpAddr, '$localhost')
                msg=getattr(myData.dataMap[mkey], 'eventMsg')
                myPars=getattr(myData.dataMap[mkey], 'params')
            else:
                msg=getattr(myData.dataMap[myKey], 'eventMsg')
                myPars=getattr(myData.dataMap[myKey], 'params')
            replaceDict={}
            replaceDict['$reporter']=myVal.reptDevIpAddr
            replaceDict['$localhost']=self.testConfig.localhost
            if '$localhost' in msg or '$reporter' in msg:
                msg=generalUtility.multiReplace(msg, replaceDict)
            if hasattr(self.testConfig, 'globalData'):
                custId=custIdUtil.getCustIdbyIp(self.testConfig.globalData, myVal.reptDevIpAddr, self.testConfig.testServer.dataCollector)
            else:
                custId='1'
            newPar={}
            for pkey in myPars.keys():
                if myPars[pkey]=='$localhost':
                    myPars[pkey]=self.testConfig.localhost
                if myPars[pkey]=='$reporter':
                    myPars[pkey]=myVal.reptDevIpAddr
                if myPars[pkey]=='$sender':
                    myPars[pkey]=custId
            params[myVal.eventType+'@'+myKey]={}
            params[myVal.eventType+'@'+myKey]['params']=myPars
            params[myVal.eventType+'@'+myKey]['msg']=msg
            ver=''
            comm=''
            if key not in no_raw_send and module not in msg_too_long and self.posix and 'snmptrap' not in myVal.method:
                import Libs.rawUdpSendHandler as rawUdpSendHandler
                import Libs.GenerateRawIPData as GenerateRawIPData
                rawmsg=GenerateRawIPData.getRawIpPacket(msg.encode('ascii', 'xmlcharrefreplace'), myVal.reptDevIpAddr, self.testConfig.testServer.dataCollector, 514)
                self.rawUdpSender=rawUdpSendHandler.rawUdpSendHandler(self.testConfig.testServer.dataCollector, 514)
                now,sendTime,unow,usendTime=timeUtility.getTimeNow()
                self.rawUdpSender.sendoutEvent(rawmsg)
            else:
                if 'snmptrap@' in myVal.method:
                    sendMethod,ver,comm=myVal.method.split('@')
                else:
                    sendMethod=myVal.method
                if not mySendEvent:
                    mySendEvent=sendEventHandler(sendMethod, self.testConfig.testServer.dataCollector)
                now,sendTime,unow,usendTime=timeUtility.getTimeNow()
                if ver and comm:
                    mySendEvent.sendoutEvent(msg, version=ver, community=comm, utf_8=True)
                else:
                    mySendEvent.sendoutEvent(msg, utf_8=True)
        #get query
        time.sleep(300)
        myParams={}
        if module in parser_holdon_module:
            time.sleep(360)
        for key in event_query_params.keys():
            myParams[key]=event_query_params[key]
        eventTypes=[]
        reporters=[]
        for myKey in params.keys():
            eventType, reporter=myKey.split(' (')[0].split('@')
            if eventType.strip() not in eventTypes:
                eventTypes.append(eventType.strip())
            if reporter.strip() not in reporters:
                reporters.append(reporter)
        finalEventTypes=[]
        if len(eventTypes)>500:
            num=generalUtility.splitByNum(len(eventTypes), 500)
            finalEventTypes.append(eventTypes[0:500])
            for i in range(num-1):
                s=(i+1)*500
                e=(i+2)*500
                subList=eventTypes[s:e]
                finalEventTypes.append(subList)
        else:
            finalEventTypes.append(eventTypes)
        reporterStr=','.join(reporters)
        retData={}
        for i in range(len(finalEventTypes)):
            eventtypeStr='","'.join(finalEventTypes[i])
            myParams['constr']=event_query_params['constr'] % (reporterStr, eventtypeStr)
            retSubData, debugInfo=self.queryHandler.getQuery(myParams)
            for key in retSubData.keys():
                newList=[]
                for item in retSubData[key]:
                    rTime,zone=timeUtility.getUTimeFromString(item.attributes['phRecvTime'])
                    if zone=='UTC':
                        if rTime+300 >= usendTime:
                            newList.append(item)
                    else:
                        if rTime+300 >= sendTime:
                            newList.append(item)
                if newList:
                    retData[key]=newList

        finalRet=self.verifyData(etype, params, retData, debugInfo, module, sendTime)
        if finalRet.totalMissing or finalRet.totalExtra:
            self.__updateCase(finalRet.caseList, path)
        return finalRet

    def verifyData(self, type, params, retData, debugInfo, module, sendTime):
        resObjList=[]
        for key in type.keys():
            if type[key].key:
                keyVal=type[key].eventType+'@'+type[key].reptDevIpAddr+' ('+type[key].key+')'
            else:
                keyVal=type[key].eventType+'@'+type[key].reptDevIpAddr
            expData=params[keyVal]
            resObj=getClassObj('TestCaseResult', module='autoTest')
            actData=''
            if keyVal in retData.keys():
                if keyVal:
                    actData=retData[keyVal][0]
            elif ' (' in keyVal:
                oriKey,map=keyVal.split(' (')
                mapKey,mapVal=map[:-1].split(':')
                if oriKey in retData.keys():
                    for item in retData[oriKey]:
                        if mapKey in item.attributes.keys():
                            if mapVal==item.attributes[mapKey]:
                                actData=item
                        elif not mapVal:
                            actData=item

            if actData:
                miss, extra, common=processList(expData['params'].keys(), actData.attributes.keys())
                for comkey in common:
                    map={}
                    map['param']=comkey
                    if actData.attributes[comkey]!=None:
                        map['actValue']=actData.attributes[comkey]
                        if 'Name' in comkey and 'HOST-' in actData.attributes[comkey]:
                            ignore_param.update([comkey])
                    else:
                        map['actValue']='None'
                    map['expectValue']=expData['params'][comkey]
                    if '\n' in map['actValue']:
                        map['actValue']=map['actValue'].replace('\n','')
                    if self.testType != 'Official' and map['param'] in ignore_param:
                        resObj.Pass.append(map)
                        continue
                    if map['expectValue']=='any' or map['expectValue'].strip()==map['actValue'].strip():
                        resObj.Pass.append(map)
                    else:
                        if map['param'] in ignore_space_params:
                            if map['expectValue'].replace(' ', '')==map['actValue'].replace(' ', ''):
                                resObj.Pass.append(map)
                            else:
                                resObj.Fail.append(map)
                        else:
                            resObj.Fail.append(map)
                if miss:
                    for misskey in miss:
                        map={}
                        map['param']=misskey
                        map['expectValue']=expData['params'][misskey]
                        map['actValue']='None'
                        resObj.Missing.append(map)
                if extra:
                    for exkey in extra:
                        if exkey not in event_ignore_params and actData.attributes[exkey]:
                            map={}
                            map['param']=exkey
                            map['expectValue']='None'
                            map['actValue']=actData.attributes[exkey]
                            resObj.Extra.append(map)
                if resObj.Fail:
                    resObj.status='Fail'
                else:
                    resObj.status='Pass'
            else:
                resObj.status='NoReturn'
                failDetail=self.eventDebug(keyVal, expData['msg'], sendTime)
                setattr(resObj, 'reasons', failDetail)
            if self.testConfig.localhost in keyVal:
                keyVal=keyVal.replace(self.testConfig.localhost, '$localhost')
            resObj.name=key+'('+keyVal+')'
            resObjList.append(resObj)
        suiteObj=getClassObj('TestSuiteResult', module='autoTest')
        suiteObj.name=module
        suiteObj.taskName='EventParsing'
        suiteObj.debugInfo=debugInfo
        for item in resObjList:
            suiteObj.totalRun+=1
            oldVal=getattr(suiteObj, 'total'+item.status)
            oldVal+=1
            setattr(suiteObj, 'total'+item.status, oldVal)
            suiteObj.caseList.append(item)

        return suiteObj

    def eventDebug(self, eventParam, msg, sendTime):
        reason=''
        debugParams={}
        for key in incident_debug_params.keys():
            debugParams[key]=incident_debug_params[key]
        debugParams['constr']=incident_debug_params['SingleEvtConstr'] % xmlEscape(msg).encode('utf-8')
        debugData, debugInfo=self.queryHandler.getQuery(debugParams)
        if ' (' in eventParam:
            finalParam, mapKey=eventParam.split(' (')
        else:
            finalParam=eventParam
            mapKey=''
        if debugData:
            if finalParam not in debugData.keys():
                reason+='eventParam %s not correct, returned data is %s' % (eventParam, ','.join(debugData.keys()))
            else:
                if mapKey:
                    maps=mapKey.split(':')
                    mapName=maps[0].strip()
                    mapValue=maps[1][0:-1].strip()
                    if mapName not in debugData[finalParam][0].attributes.keys():
                        reason+='key %s in not in attribute' % mapName
                    elif mapValue!=debugData[finalParam][0].attributes[mapName]:
                        reason+='key %s is not same. Return %s' % (mapName+':'+mapValue, mapName+':'+debugData[finalParam][0].attributes[mapName])
                else:
                    reason+='data is presented, but somehow not show up in query.'
        else:
            reason+='No parsing event.'

        return reason

    def __updateCase(self, caselist, path):
        for case in caselist:
            map={}
            first, second=case.name.split('@')
            filename=path+'/'+first.split(' (')[-1]+'.dat'
            index=second[:-1]
            if case.Missing or case.Extra:
                change=False
                myData=datFileHandler.getData(filename, event_data_keys)
                if case.Missing:
                    for item in case.Missing:
                        value=item['param']+'='+item['actValue']
                        if value in myData.dataMap[index].params:
                            myData.dataMap[index].params.remove(value)
                            change=True
                if case.Extra:
                    for item in case.Extra:
                        value=item['param']+'='+item['actValue']
                        if value not in myData.dataMap[index].params:
                            myData.dataMap[index].params.append(value.encode('utf-8'))
                            change=True
                if change:
                    datFileHandler.modifyDatFile(myData, type='eventParsing')
                    print '%s updated.' % filename
