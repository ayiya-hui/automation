import restApiDataHandler as restApi
import deviceHandler
import rawUdpSendHandler
import GenerateRawIPData
import GenerateNetFlowData
import sendEventHandler
import datFileHandler
import CSVHandler
from ConfigConstants.TestConstant import incident_query_advance, incident_data_keys, perf_object_list
from ConfigConstants.ruleTestTemplate import ruleTestEvents, ruleTestEvent
import Util.perfObjUtility as perfObj
import queryHandler
import appHandler
import ruleReader
import os, time, re
import sys
from string import Template
from Util.localhostIp import getLocalhostIp
from Util.randomGen import getRandomIPAddr, getRandomNum
import Util.generalUtility as generalUtility
#import dbHandler

PORTS={'syslog':514, 'netflow':2055}
group_key='Group@'
add_test_rule='test/rule'
get_test_rule='test/rule/result?id=%s'
csv_path='../TestData/Incident/incidentData.csv'
data_path='../TestData/Incident/IncidentMsgs/%s.dat'

eventsTemp=Template(ruleTestEvents)
eventTemp=Template(ruleTestEvent)

result_code='\<result code="(?P<number>[0-9])"\>'
result_exp=re.compile(result_code)

class incidentHandler:
    def __init__(self, appServer, restUser=False, restPassword=False):
        self.appServer=appServer
        self.user=restUser
        self.password=restPassword
        self.appHandler=appHandler.appHandler(self.appServer, user=self.user, password=self.password)
        self.restApiHandler=restApi.restApiDataHandler(self.appServer, user=self.user, password=self.password)
        self.deviceHandler=deviceHandler.deviceHandler(self.appServer, user=self.user, password=self.password)
        self.queryHandler=queryHandler.queryHandler(appServer)
        self.auto_params={}
        if os.name=='posix':
            self.posix=True
        else:
            self.posix=False

    def getAutoParams(self):
        if not self.auto_params:
            self.auto_params=CSVHandler.getDataFromFile('incidentData', csv_path, None, None)

        return self.auto_params

    def trigger(self, param, msgs):
        rept_ip=''
        if param.reptDevIpAddr=='$localhost':
            rept_ip=getLocalhostIp()
        elif param.reptDevIpAddr=='$appServer':
            rept_ip=self.appServer
        else:
            rept_ip=param.reptDevIpAddr
        if param.createDevice:
            self.createDevice(param.reptDevIpAddr, param.deviceName, param.deviceType, domain=param.domainController)
        rawSend=False
        if self.posix and param.reptDevIpAddr!='$localhost':
            rawSend=True
        if rawSend:
            mySendEvent=rawUdpSendHandler.rawUdpSendHandler(self.appServer, PORTS[param.method])
        else:
            mySendEvent=sendEventHandler.sendEventHandler(param.method, self.appServer)
        rept={}
        rept['$localhost']=getLocalhostIp()
        rept['$dataCollector']=self.appServer
        rept['$reporter']=rept_ip
        print rept_ip
        for i in range(int(param.count)):
            for line in msgs:
                msg=generalUtility.multiReplace(line, rept)
                if '$randomIP' in line:
                    ip=getRandomIPAddr()
                    msg=msg.replace('$randomIP', ip)
                if '$randomNum' in line:
                    num=getRandomNum(1, 100)
                    msg=msg.replace('$randomNum', num)
                if rawSend:
                    if param.method=='netflow':
                        temp_msg=GenerateNetFlowData.getNetFlowPacket(msg)
                    else:
                        temp_msg=msg.strip()
                    send_msg=GenerateRawIPData.getRawIpPacket(temp_msg, rept_ip, self.appServer, PORTS[param.method])
                else:
                    send_msg=msg
                print msg
                mySendEvent.sendoutEvent(send_msg)
                time.sleep(1)

    def createDevice(self, device_ip, device_name, device_type, domain=False):
        allDevices=self.deviceHandler.getAllDevices()
        rawPerfObj=self.restApiHandler.getData('perfObject')
        perfObj={}
        for perfId in rawPerfObj:
            pType=rawPerfObj[perfId].type
            typeName=pType.name.lower()+'_id'
            if typeName in perf_object_list:
                perfObj[typeName]=perfId
        if not allDevices or (device_ip not in allDevices.keys()):
            if domain:
                self.deviceHandler.createDevice(device_ip, device_name, device_type, perfObj, dataCollector=self.appServer)
            else:
                self.deviceHandler.createDevice(device_ip, device_name, device_type, perfObj)

    def send(self, event, name=False):
        if name:
            pass
        else:
            print 'Need to have incidentType name to decide how many counts of message to be sent.'

    def getByIncidentId(self, id, hour=False):
        params={}
        params['constr']=incident_query_advance['SingleEvtConstr'] % (id, '0')
        if hour:
            params['minute']=str(hour*60)
        else:
            params['minute']='240'
        self.queryHandler.getQuery(params)

        return self.queryHandler.appHandler.queryXml[0]

    def getRule(self, incident_type):
        allRule=self.getAllRules(inactive=True)
        myRule=''
        if not incident_type in allRule.keys():
            print 'incidntType %s NOT exist in system' % incident_type
            sys.exit()
        else:
            myRule=allRule[incident_type]

        return myRule

    def getTestRuleParameter(self, incident_type):
        param=''
        if not self.auto_params:
            self.getAutoParams()
        if self.auto_params:
            param=self.auto_params[incident_type]

        return param

    def testRule(self, id, count, data):
        events=[]
        for j in range(count):
            i=1
            for item in data['rawData']:
                eventMap={}
                eventMap['report_ip']=data['reportIp']
                eventMap['pause']=data['pause']
                eventMap['number']=str(i+j)
                ran_ip=''
                ran_msg=''
                if '$randomIP' in item:
                    ran_ip=item.replace('$randomIP', getRandomIPAddr())
                else:
                    ran_ip=item
                if '$randomNum' in item:
                    ran_msg=ran_ip.replace('$randomNum', getRandomNum(1, 10000))
                else:
                    ran_msg=ran_ip
                eventMap['raw_event']=ran_msg
                events.append(eventTemp.substitute(eventMap))
                i+=1
        eventsMap={}
        eventsMap['rule_id']=id
        eventsMap['events']=''.join(events)
        inXml=eventsTemp.substitute(eventsMap)
        msg=self.appHandler.putData(add_test_rule, inXml)
        number=''
        url_status=''
        while True:
            self.appHandler.getData(get_test_rule % id)
            if self.appHandler.xml:
                match=result_exp.search(self.appHandler.xml)
                if match:
                    groups=match.groupdict()
                    number=groups['number']
                if number=='3':
                    url_status='Pass'
                elif number=='4':
                    url_status='Failure'
                else:
                    url_status='Unfinish'
            if url_status=='Unfinish':
                time.sleep(60)
            else:
                break

        return url_status, self.appHandler.xml

    def getAllRules(self, inactive=False):
        rawtestMap=self.restApiHandler.getData('rule')
        testMap={}
        for mapKey in rawtestMap.keys():
            if 'dataCreationType' in rawtestMap[mapKey].attribute.keys() and rawtestMap[mapKey].attribute['dataCreationType']=="SYSTEM" :
                if rawtestMap[mapKey].active=='true':
                    testMap[mapKey]=rawtestMap[mapKey]
                elif inactive:
                    testMap[mapKey]=rawtestMap[mapKey]
        indexMap={}
        for key in testMap.keys():
            incidentType=testMap[key].incidentType.split('$')[-1]
            indexMap[incidentType]=testMap[key]
        finalMap={}
        for index in indexMap.keys():
            finalMap[index]=indexMap[index]

        return finalMap

    def getAllRulesNotExisted(self):
        pass

    def getAllSavedRuleInfo(self):
        pass

    def getRawData(self, incident_type):
        myData=datFileHandler.getData((data_path % incident_type), incident_data_keys)

        return myData

    def triggerIncident(self, dataCollector=False, data=False):
        if dataCollector:
            data_collector=dataCollector
        else:
            data_collector=self.appServer
        if data:
            self.msgMap={}
            if not data:
                myObj=self.db.findObj(self.incidentType)
                if myObj is None:
                    sys.exit()
            if not os.path.exists(data):
                print 'data file %s is NOT exist, exit.' % data
                sys.exit()
            else:
                myRead=open(data)
                myData=myRead.read()
                myRead.close()
                ipAddr, device_name=myData.strip().split(',')
                self.incidentRule.setDeviceInfo(ipAddr, device_name)
            for item in os.listdir(self.incidentType):
                myRead=open(self.incidentType+'/'+item)
                modi_item=item.replace('SLASH', '/')
                print modi_item
                self.msgMap[modi_item]=myRead.read().strip()
                myRead.close()
        if self.msgMap:
            order=self.incidentRule.setSendOrder()
            orderlist=order.keys()
            orderlist.sort()
            if self.incidentRule.createDevice:
                if not self.deviceHandler.isDeviceExist(self.incidentRule.ipAddr):
                    self.deviceHandler.createDevice(self.incidentRule.ipAddr, self.incidentRule.deviceName, self.incidentRule.deviceType, perfObj.getPerfObj(self.appServer), dataCollector=data_collector)
                    time.sleep(120)
                else:
                    print 'Device with ip %s is exist. Skip creating device.' % self.incidentRule.ipAddr
            mySendEvent=''
            if os.name=='posix':
                mySendEvent=rawUdpSendHandler.rawUdpSendHandler(data_collector, PORTS['syslog'])
            else:
                mySendEvent=sendEventHandler('syslog', data_collector)
            sendMsgs={}
            for key in order:
                msgInfo=order[key]
                check, eventType=self.checkType(msgInfo, self.msgMap)
                if check:
                    if os.name=='posix':
                        finalMsg=GenerateRawIPData.getRawIpPacket(self.msgMap[eventType], self.incidentRule.ipAddr, data_collector, PORTS['syslog'])
                    else:
                        finalMsg=self.msgMap[eventType]
                    sendMsgs[msgInfo.sendOrder]=finalMsg
                else:
                    print 'cannot pass the check. eventType %s does not have msg.' % msgInfo.eventType
            if sendMsgs:
                orders=sendMsgs.keys()
                orders.sort()
                for i in range(self.incidentRule.count):
                    for key in orders:
                        mySendEvent.sendoutEvent(sendMsgs[key])
                        time.sleep(self.incidentRule.insideInterval)
                    time.sleep(self.incidentRule.intervalSent)
            else:
                print 'No event message to be sent.'
                sys.exit()

    def getAutomatedRuleData(self, incident_type):
        pass

    def ruleReader(self, rule):
        myRule=ruleReader.readRule(rule)

        return myRule

    def singleCheck(self, eventType, msgs):
        check=False
        if eventType in msgs.keys():
            check=True

        return check, eventType

    def groupCheck(self, eventType, msgs):

        return self.finalCheck(eventType, msgs)

    def notgroupCheck(self, eventType, msgs):

        return self.finalCheck(eventType, msgs, opt=False)

    check_token={'single':singleCheck,
                 'group':groupCheck,
                 'notgroup':notgroupCheck,
                 }

    def checkType(self, eventInfo, msgs):

        return self.check_token[eventInfo.type](self, eventInfo.eventType, msgs)

    def getGroup(self, group):
        group_name=group.split(group_key)[-1].strip()
        contents=self.restApiHandler.getData(group_name, module='namedValue')

        return contents[group_name].namedValues

    def finalCheck(self, eventType, msgs, opt=True):
        check=False
        finalType=''
        eventTypes=eventType.split(',')
        allTypes=[]
        for event in eventTypes:
            if group_key in event:
                my_list=self.getGroup(event)
                for key in my_list:
                    if not key in allTypes:
                        allTypes.append(key)
            else:
                if not event in allTypes:
                    allTypes.append(event)
        if opt:
            for key in msgs.keys():
                if key in allTypes:
                    check=True
                    finalType=key
                    break
        else:
            for key in msgs.keys():
                if not key in allTypes:
                    check=True
                    finalType=key
                    break

        return check, finalType





