from runBase import baseTest
import Libs.CSVHandler as CSVHandler
import Libs.datFileHandler as datFileHandler
from Libs.restApiDataHandler import restApiDataHandler
from Libs.deviceHandler import deviceHandler
from Libs.queryHandler import queryHandler
import Libs.GenerateRawIPData as GenerateRawIPData
import Libs.rawUdpSendHandler as rawUdpSendHandler
from ConfigConstants.TestConstant import logDiscover_data_path, logDiscover_params, logDiscover_data_key, incident_debug_params
import Util.testUtility as testUtility
import Models.ClassLocator as ClassLocator
import time
import Util.timeUtility as timeUtility
from Libs.sendEventHandler import sendEventHandler
from Util.testUtility import xmlEscape

SYSLOG_PORT=514

class logDiscoverTest(baseTest):
    def __init__(self, task, testConfig):
        baseTest.__init__(self, task, testConfig)
        self.deviceHandler=deviceHandler(testConfig.testServer.appServer)
        self.queryHandler=queryHandler(testConfig.testServer.appServer)
        if hasattr(testConfig, 'posix'):
            self.posix=True
            self.eventSender=rawUdpSendHandler.rawUdpSendHandler(testConfig.testServer.dataCollector, SYSLOG_PORT)
        else:
            self.posix=False
            self.eventSender=sendEventHandler('syslog', self.testConfig.testServer.dataCollector)

    def getCommonData(self, param):
        self.commons=CSVHandler.getDataFromFile('logDiscoverData', self.path+'/logDiscoverData.csv', None, None)

        return self.commons

    def getGlobalData(self):
        myRestApi=restApiDataHandler(self.testConfig.testServer.appServer)
        myDeviceTypes=myRestApi.getData('deviceType')
        keyedTypes=testUtility.rekeyKey('Attribute-id', myDeviceTypes)

        return keyedTypes

    def getTestList(self, taskFiles):
        if taskFiles.lower()=='all':
            map=self.commons
        else:
            map={}
            for key in taskFiles.split(','):
                map[key]=self.commons[key]

        return map

    def run(self, myType, testKey):
        import pdb
        pdb.set_trace()
        if myType.isApp:
            appDev=True
        else:
            appDev=False
        if not self.deviceHandler.isDeviceExist(myType.reptDevIpAddr, app=appDev):
            print 'Creating new deive %s' % myType.reptDevIpAddr
            myData=datFileHandler.getData(self.path+'/'+logDiscover_data_path+'/'+testKey+'.dat', logDiscover_data_key)
            if self.posix:
                rawPkt=GenerateRawIPData.getRawIpPacket(myData.dataMap['default'].eventMsg[0].strip(), myType.reptDevIpAddr, self.testConfig.testServer.dataCollector, SYSLOG_PORT)
                self.eventSender.sendoutEvent(rawPkt)
            else:
                self.eventSender.sendoutEvent(myData.dataMap['default'].eventMsg[0].strip())
            now,sendTime,unow,usendTime=timeUtility.getTimeNow()
            time.sleep(300)
        else:
            print 'Device already exist: %s' % myType.reptDevIpAddr
        exp_maps={}
        ret_maps={}
        for item in logDiscover_params:
            exp_maps[item]=getattr(myType, item)
            ret_maps[item]=None
        device=self.deviceHandler.getDeviceByIp(myType.reptDevIpAddr, isApp=appDev)
        resObj=ClassLocator.getClassObj('TestCaseResult', module='autoTest')
        resObj.name=testKey
        if device:
            ret_maps['reptDevIpAddr']=device.accessIp
            ret_maps['creationMethod']=device.creationMethod
            deviceTypeId=device.deviceType.split('@')[-1]
            if deviceTypeId in self.testConfig.globalData.keys():
                vendor, model, version=self.testConfig.globalData[deviceTypeId].split('@')
                ret_maps['vendor']=vendor
                ret_maps['model']=model
                ret_maps['version']=version
            status_list=[]
            for key in exp_maps.keys():
                map={}
                map['param']=key
                map['actValue']=ret_maps[key]
                map['expectValue']=exp_maps[key]
                if map['expectValue']!=map['actValue']:
                    status_list.append('Fail')
                    resObj.Fail.append(map)
                else:
                    status_list.append('Pass')
                    resObj.Pass.append(map)
            if 'Fail' in status_list:
                resObj.status='Fail'
            else:
                resObj.status='Pass'
        else:
            resObj.status='NoReturn'
            failDetail='Unknown'
            #failDetail=self.eventDebug(myType.reptDevIpAddr, myData.dataMap['default'].eventMsg[0].strip(), sendTime)
            setattr(resObj, 'reasons', failDetail)

        testRet=ClassLocator.getClassObj('TestSuiteResult', module='autoTest')
        testRet.name=testKey
        testRet.taskName='LogDiscover'
        testRet.totalRun=1
        setattr(testRet, 'total'+resObj.status, 1)
        testRet.caseList.append(resObj)

        return testRet

    def eventDebug(self, eventParam, msg, sendTime):
        reason=''
        debugParams={}
        msg=xmlEscape(msg)
        for key in incident_debug_params.keys():
            debugParams[key]=incident_debug_params[key]
        debugParams['constr']=incident_debug_params['SingleEvtConstr'] % msg
        debugData=self.queryHandler.getQuery(debugParams)
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
                    if mapValue!=debugData[finalParam][0].attributes[mapName]:
                        reason+='key %s is not same. Return %s' % (mapName+':'+mapValue, mapName+':'+debugData[finalParam][0].attributes[mapName])
                else:
                    reason+='data is presented, but somehow not show up in query.'
        else:
            reason+='No parsing event.'

        return reason


