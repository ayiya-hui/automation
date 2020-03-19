from testClass import testSuite, testCase, EVENTPARSING
import queryHandler
import hashUtility

SKIP=['any']
IGNORE=['rawEventMsg', 'destName','hostName','srcName','ipProto']

class eventParsingSuite(testSuite):
    def __init__(self):
        testSuite.__init__(self)

    def runModuleVerify(self, appServer):
        ips=[]
        eventtypes=[]
        params={}
        for case in self.testcases:
            if case.reporter not in ips:
                ips.append(case.reporter)
            if case.eventType not in eventtypes:
                eventtypes.append(case.eventType)
            if case.key!='':
                keyName, keyValue=case.key.split(':')
                key=case.eventType+'_'+case.reporter+'#'+keyName+'#'+keyValue
            else:
                key=case.eventType+'_'+case.reporter
            params[key]=case.parameters
        ipString=','.join(ips)
        eventtypeString='","'.join(eventtypes)
        myQuery=queryHandler.queryHandler()
        singleConstr=EVENTPARSING % (eventtypeString, ipString)
        myQuery.getQuery(appServer, singleConstr)
        retParam={}
        for data in myQuery.data:
            if 'reptDevIpAddr' in data.keys() and 'eventType' in data.keys():
                key=data['eventType']+'_'+data['reptDevIpAddr']
            if key not in retParam.keys():
                retParam[key]=[]
                retParam[key].append(data)
            else:
                retParam[key].append(data)
        if not len(retParam):
            print 'No return in data'

        resultParam={}
        for key in params:
            passed=failed=missed=improved=[]
            map={}
            if '#' in key:
                subKey, subName, subValue=key.split('#')
                if subKey in retParam.keys():
                    exist=False
                    for data in retParam[subKey]:
                        if subName in data.keys() and subValue in data[subName]:
                            exist=True
                            myCompare=hashUtility.hashCompareHandler(params[key], data, skip=SKIP, ignore=IGNORE)
                            map['status'], map['passed'], map['failed'], map['missed'], map['improved']=myCompare.compareHash()
                    if not exist:
                        map['status']='No Return'
                else:
                    map['status']='No Return'
            else:
                if key in retParam.keys():
                    myCompare=hashUtility.hashCompareHandler(params[key], retParam[key][0], skip=SKIP, ignore=IGNORE)
                    map['status'], map['passed'], map['failed'], map['missed'], map['improved']=myCompare.compareHash()
                else:
                    map['status']='No Return'
            resultParam[key]=map

        for case in self.testcases:
            if case.key!='':
                keyName, keyValue=case.key.split(':')
                key=case.eventType+'_'+case.reporter+'#'+keyName+'#'+keyValue
            else:
                key=case.eventType+'_'+case.reporter
            case.fillInResult(self.name, resultParam[key], module=True)
            self.fillInCaseResult(case.caseTestResult)

class eventParsingCase(testCase):
    def __init__(self):
        testCase.__init__(self)







