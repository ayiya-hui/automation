from testClass import testSuite, testCase
import deviceDataClass
import classUtility
import time

EVENTS='events'
ERR_MSG='device already exist. Delete it from system'
PARSER='and restart phParser'
LOG='log'
SNMP='snmp'

class deviceTestSuite(testSuite):
    def __init__(self):
        testSuite.__init__(self)

class deviceTestCase(testCase):
    def __init__(self):
        testCase.__init__(self)

    def runLogDiscovery(self, port=False):
        return self.__runDiscovery(LOG, port=port)

    def runSnmpDiscovery(self):
        return self.__runDiscovery(SNMP)

    def __runDiscovery(self, type, port=False):
        if not self.isParamSet():
            self.setParam(self.appServer, self.dataCollector)
        preResult=self.__checkDevice()
        if preResult.exist:
            if type==LOG:
                msg=type+':'+ERR_MSG+' '+PARSER
            else:
                msg=type+':'+ERR_MSG
            print msg
        else:
            if type==LOG:
                self.msg=self.parseEvent
                self.eventHandler.sendoutEvent(self.parseEvent)
            if type==SNMP:
                 self.deviceHandler.discoveryDevice(self.reporter)
            time.sleep(120)
            myRet=self.__checkDevice()
            map={}
            if myRet.exist:
                myCompare=hashUtility.hashCompareHandler(self.parameters, myRet.details)
                map['status'], map['passed'], map['failed'], map['missed'], map['improved']=myCompare.compareHash()
            else:
                map['status']='No Return'

        return map

    def __checkDevice(self):
        myDevice=deviceDataClass.device()
        myType=deviceDataClass.deviceType()
        myType=classUtility.hashToClass(self.parameters, myType)
        myDevice=classUtility.hashToClass(self.parameters, myDevice)
        myDevice.deviceType=myType
        myDevStat=self.deviceHandler.isDeviceExist(myDevice, app=self.type)

        return myDevStat


