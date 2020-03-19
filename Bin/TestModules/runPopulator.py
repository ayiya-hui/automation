from runBase import baseTest
import Libs.passwordHandler as passwordHandler
import os, re
import Libs.CSVHandler as CSVHandler
from Models.ClassLocator import getClassObj
import Util.testUtility as testUtility
import ConfigConstants.TestConstant as testConstant
from Libs.restApiDataHandler import restApiDataHandler

import sys

from Libs.XmlHandler import XmlHandler
import Util.generalUtility as generalUtility
import Util.classUtility as classUtility
import Util.classTranslation as classTranslation
import Libs.cmdbHandler as cmdbHandler
import xml.dom.minidom as dom



class populatorTest(baseTest):
    def __init__(self, task, testConfig):
        baseTest.__init__(self, task, testConfig)
        self.restApiHandler=restApiDataHandler(self.testConfig.testServer.appServer)
        #self.path=testConstant.populator_normal_path

    def run(self, type, typeName):
        myPath, ori, ret=self.tokenDict[type.testType](self, type)
        retObj=self.verifyData(typeName, ori, ret)

        return retObj

    def getCommonData(self):
        indexData=CSVHandler.getDataFromFile('DbPopulatorData', self.path+'/DbPopulatorData.csv', None, None)
        self.commons=indexData

        return self.commons

    def getTestList(self, type):
        testMap={}
        if type!='all':
            if ',' in type:
                tasks=type.split(',')
            else:
                tasks=[type]
            for task in tasks:
                if task in self.commons.keys():
                    testMap[task]=self.commons[task]
                else:
                    print 'task: %s is not supported.' % task
        else:
            testMap=self.commons
        self.testMap=testMap
        return testMap

    def testGroupDefinition(self, type):
        for test in TestConstant.group_tasks.keys():
            print '\nGroup Defn Test Task: %s' % test
            file=self.path+test+'.csv'
            data=CSVHandler.getDatafromFile(file)
            if not hasattr(self, 'groups'):
                self.groups=self.configHandler.getData('group')
            retData=self.groups[TestConstant.group_tasks[test]]
            self.verifyData(data, retData, self.__getListKey('group'))

    def testGeneralDefinition(self, type=False):
        if type:
            tests=[type]
        else:
            tests=TestConstant.general_tasks.keys()
        for test in tests:
            print '\nTest %s' % test
            myPath=self.__getPath(type)+'.'+TestConstant.general_tasks[type]
            if TestConstant.general_tasks[type]=='xml':
                indexData=XmlHandler.getDatafromFile(myPath, type)
            elif TestConstant.general_tasks[type]=='csv':
                indexData=CSVHandler.getDatafromFile(myPath, type=type)
            retData=self.configHandler.getData(test)

            self.verifyData(indexData, retData, testUtility.getListKey(type))

    def testModule(self, type):
        print 'type: %s' % type.name
        myPath=self.__getPath(type.name)
        print 'path: %s' % myPath
        indexData={}
        if type.name in testConstant.populator_task_trans.keys():
                typeName=testConstant.populator_task_trans[type.name]
        else:
            typeName=type.name
        print 'type: %s' % typeName
        if type.fileType=='xml':
            indexData=self.__getXMLData(type.name, myPath)
        elif type.fileType=='csv':
            indexData=CSVHandler.getDatafromFolder(type.name, myPath)
        restType=self.__getRestTransTest(type.name)
        retData=self.restApiHandler.getData(restType)
        if type.name in testConstant.populator_special_handling:
            finalOri, finalRet=self.__specialHandling(type.name, indexData, retData)
        else:
            finalOri=indexData
            finalRet=retData

        return myPath, finalOri, finalRet

    tokenDict={'general':testGeneralDefinition,
               'module':testModule,
               'group':testGroupDefinition, }

    def __RuleSpecial(self, expData, actData):
        newData={}
        for key in expData.keys():
            newObj=classTranslation.classTranslation().doTranslate(expData[key])
            newData[newObj.attribute['naturalId']]=newObj
        newActData={}
        if not hasattr(self, 'groups'):
            self.groups=self.restApiHandler.getData('group')
        for key in actData.keys():
            actData[key].group=self.__setGroupName(actData[key].attribute['id'], None, self.groups)
            actData[key].incidentType=actData[key].incidentType.split('EventType$')[-1]
            newActData[actData[key].attribute['naturalId']]=actData[key]

        return newData, newActData

    def __ReportSpecial(self, expData, actData):
        newData={}
        for key in expData.keys():
            newObj=classTranslation.classTranslation().doTranslate(expData[key])
            groups=newObj.group.split(',')
            groups.sort()
            newObj.group=','.join(groups)
            newData[newObj.attribute['naturalId']]=newObj
        newActData={}
        if not hasattr(self, 'groups'):
            self.groups=self.restApiHandler.getData('group')
        for key in actData.keys():
            actData[key].group=self.__setGroupName(actData[key].attribute['id'], None, self.groups)
            newActData[actData[key].attribute['naturalId']]=actData[key]

        return newData, newActData

    def __RoleSpecial(self, expData, actData):
        newData={}
        for key in expData.keys():
            profileObj=expData[key].Config.profile
            impl=dom.getDOMImplementation()
            doc=impl.createDocument(None, None, None)
            myTitle=doc.toxml('UTF-8')
            myXml=XmlHandler().XmlObjToString(profileObj)
            setattr(expData[key], 'Config', myTitle+myXml)
            newObj=classTranslation.classTranslation().doTranslate(expData[key])
            newData[newObj.attribute['naturalId']]=newObj

        return newData, actData

    def __WidgetSpecial(self, expData, actData):
        newData={}
        for key in expData.keys():
            expData[key].attribute['naturalId']=expData[key].attribute['id']
            expData[key].dataProviderId=expData[key].dataProvider.attribute['id']
            expData[key].dataProviderType=expData[key].dataProvider.attribute['type']
            delattr(expData[key], 'dataProvider')
            newData[expData[key].attribute['naturalId']]=expData[key]
        newActData={}
        if not hasattr(self, 'groups'):
            self.groups=self.restApiHandler.getData('group')
        reportData=testUtility.rekeyKey('Attribute-id', self.restApiHandler.getData('report'))
        for key in actData.keys():
            actData[key].attribute['group']=self.__setGroupName(actData[key].attribute['id'], None, self.groups)
            actData[key].attribute['id']=actData[key].attribute['naturalId']
            if actData[key].dataProviderType=='Report':
                actData[key].dataProviderId=reportData[actData[key].dataProviderId]
            delattr(actData[key], 'dataProvider')
            newActData[actData[key].attribute['naturalId']]=actData[key]

        return newData, newActData

    def __EventAttrDescSpecial(self, expData, actData):
        newData={}
        for key in expData.keys():
            newObj=classTranslation.classTranslation().doTranslate(expData[key])
            newData[key]=newObj
        newActData={}
        for key in actData.keys():
            newKey=actData[key].eventAttributeType.split('$')[-1]
            actData[key].eventAttributeType=newKey
            finalKey=newKey+'-'+actData[key].code
            newActData[finalKey]=actData[key]

        return newData, newActData

    def __EventAttribByDeviceSpecial(self, expData, actData):
        newData={}
        for key in expData.keys():
            newObj=classTranslation.classTranslation().doTranslate(expData[key])
            newData[key]=newObj
        newActData={}
        deviceTypes=self.restApiHandler.getData('deviceType')
        rekeyTypes=testUtility.rekeyKey('Attribute-id', deviceTypes)
        for key in actData.keys():
            if hasattr(actData[key], 'eventType') and actData[key].eventType!=None:
                eventType=actData[key].eventType.split('$')[-1]
                actData[key].eventType=eventType
            else:
                eventType=''
            t=actData[key]
            if classUtility.getType(actData[key])=='list':
                dType=rekeyTypes[actData[key][0].deviceType.split('@')[-1]]
                Li=[]
                for sub in actData[key]:
                    Li.append(sub)
                newActData[dType+'-'+eventType]=Li
            else:
                dType=rekeyTypes[actData[key].deviceType.split('@')[-1]]
                actData[key].deviceType=dType
                newActData[dType+'-'+eventType]=actData[key]

        return newData, newActData

    def __EventTypeSpecial(self, expData, actData):

        print 'data-definition: %s, cmdb: %s' % (len(expData), len(actData))
        key1=expData.keys()
        key2=actData.keys()
        miss=[]
        for key in key1:
            if key not in key2:
                miss.append(key)
        extra=[]
        for key in key2:
            if key not in key1:
                extra.append(key)
        print 'data-definition miss: %s' % len(miss)
        for key in miss:
            print key

        print 'cmdb miss: %s' % len(extra)
        for key in extra:
            print key
        myF=open('result.txt', 'w')
        myF.write('Total missing: %s\n', len(miss))
        if miss:
            for item in miss:
                myF.write(item+'\n')

        sys.exit()
        deviceTypes=self.__getCMDBData('deviceType')
        newData={}
        newActData={}
        for data in expData:
            key=data.deviceType
            for item in data.keys():
                if key in deviceTypes.keys():
                    data[item].deviceType=deviceTypes[key]
                else:
                    print 'item %s has no deviceType' % item
                datas[item]=data[item]

        return newData, newActData

    specialDict={'rule':__RuleSpecial, 'report':__ReportSpecial, 'role':__RoleSpecial, 'widget':__WidgetSpecial, 'eventAttrDesc':__EventAttrDescSpecial, 'eventAttribByDevice':__EventAttribByDeviceSpecial, 'eventType':__EventTypeSpecial,}

    def __specialHandling(self, type, expData, actData):
        return self.specialDict[type](self, expData, actData)

    def __getXMLData(self, type, myPath):
        if type in testConstant.populator_type_switch.keys():
            indexKey=testUtility.getKey(testConstant.populator_type_switch[type])
        else:
            indexKey=testUtility.getKey(type)
        fileList=os.listdir(myPath)
        newFiles=[]
        for file in fileList:
            if '.xml' in file and file not in testConstant.populator_skip_files:
                newFiles.append(file)
        rawdata={}
        for file in newFiles:
            name=file.split('.')[0]
            myFile=open(myPath+'/'+file, 'r')
            text=''
            for line in myFile.readlines():
                text+=line.replace('\n', '')
            myFile.close()
            rawdata[name]=text
        finalData={}
        if type in testConstant.populator_path_change.keys():
            type=type.title()
        types=generalUtility.getPlural(type)
        myXmlHandler=XmlHandler()
        for subkey in rawdata.keys():
            myData=myXmlHandler.XmlStringToObj(rawdata[subkey], keyword=types)
            for data in myData:
                if 'Attribute-' in indexKey:
                    key=data.attribute[indexKey.split('-')[-1]]
                else:
                    key=getattr(data, indexKey)
                finalData[key]=data

        return finalData



    def __setDeviceType(self, deviceTypeId):
        if not hasattr(self, 'device_types'):
            self.device_types=self.configHandler.getData('deviceType')
        if deviceTypeId in self.device_types.keys():
            myDevType=self.device_types[deviceTypeId]
        else:
            myDevType=''

        return myDevType

    def __setGroupName(self, id, oldGroupName, groupData):
        groupName=[]
        if not hasattr(self, 'group_items'):
            myCMDB=cmdbHandler.cmdbHandler(self.testConfig.testServer.dbServer)
            self.group_items=myCMDB.getGroupItem()
        if id in self.group_items.keys():
            groupId=self.group_items[id].split(',')
            for key in groupData.keys():
                if groupData[key].attribute['id'] in groupId:
                    groupName.append(key)
        groupName.sort()
        return ','.join(groupName)



    def __indexEventParser(self, fileList, type, myPath):
        for file in fileList:
            if '.xml' not in file or file in SKIP_FILES:
                fileList.remove(file)
        data={}
        for file in fileList:
            name=file.split('.')[0]
            myFile=open(myPath+file, 'r')
            text=''
            for line in myFile.readlines():
                text+=line.replace('\n', '')
            myFile.close()
            data[name]=text
        indexData={}
        deviceTypes=self.__getCMDBData('deviceType')
        orderData=CSVHandler.getDatafromFile(myPath+'parserOrder.csv')
        pattern=re.compile(REGEX)
        for key in data.keys():
          if SPLIT['head'] in data[key]:
              valueHead=SPLIT['head']
          else:
              valueHead=SPLIT['althead']
          myHead=data[key].split(valueHead, 1)
          if len(myHead)==2:
              middle=myHead[1]
          else:
              print 'there is no such data pattern.'
          myTail=middle.split(SPLIT['tail'])
          myObj=locateClassInstance.getClassInstance(type)
          myObj.attribute['name']=key
          myObj.parserXml=valueHead+myTail[0]+SPLIT['tail']
          myWord=myHead[0].split('</deviceType')[0]
          ret=pattern.search(myWord)
          myType=ret.group('modelName')+'-'+ret.group('vendorName')
          if myType in deviceTypes.keys():
              myObj.deviceType=deviceTypes[myType]
          myObj.priority=orderData[key].priority
          indexData[key]=myObj

        return indexData

    def __getOriData(self, task, fileName):
        test, type=fileName.split('.')
        path=self.__getPath(task)
        file=path+fileName
        if type=='csv':
            data=CSVHandler.getDatafromFile(file)
        elif type=='xml':
            mydata=XMLHelper.unpickleFile(file, XML_TYPE[test], type='list')
            data={}
            for item in mydata:
                for attr in classUtility.getAttrList(item):
                    if attr in SPECIAL_LIST:
                        newValue=self.__specialFormat(item, attr)
                        setattr(item, attr, newValue)
                key=getattr(item, XML_DATAKEY[test])
                data[key]=item

        return data

    def __specialFormat(self, obj, attr):
        oldVal=getattr(obj, attr)
        newVal=oldVal
        if attr=='adminEmail':
            if oldVal=='not_set':
                newVal=''

        return newVal

    def __getCMDBData(self, test):
        if test=='Cust-Super':
            myCmdb=cmdbHandler.cmdbHandler(self.appServer)
            retData=myCmdb.getDomain(param='Super')
        else:
            if test in TestConstant.task_trans.keys():
                retData=self.configHandler.getData(TestConstant.task_trans[test])
            else:
                retData=self.configHandler.getData(test)

        return retData

    def __getPath(self, type):
        if type in testConstant.populator_special_path.keys():
            prePath=testConstant.populator_special_path[type]
        else:
            if type in testConstant.populator_path_change.keys():
                prePath=testConstant.populator_normal_path % testConstant.populator_path_change[type]
            else:
                prePath=testConstant.populator_normal_path % type

        return prePath

    def __getRestTransTest(self, test):
        newTest=test
        if test in testConstant.populator_rest_trans.keys():
            newTest=testConstant.populator_rest_trans[test]

        return newTest

    def __verifyEncrptPassword(self, plain, encrypt):
        passcode, salt, alg=encrypt.split('-')
        myPass=passwordHandler.passwordHandler(int(alg))
        newPass=myPass.getHashCode(salt, plain)
        if newPass==passcode:
            matched=True
        else:
            matched=False
            print 'admin password is not matched with encryption one. Plaintext %s, hexDigest %s, actual hexDigest %s' % (plain, newPass, passcode)

        return matched


    def verifyData(self, name, ori, ret):
        resObjList=[]
        if ret:
            miss, extraRaw, common=testUtility.processList(ori.keys(), ret.keys())
            extra=[]
            if name in testConstant.populator_comp_ignore.keys():
                for subKey in extraRaw:
                    if testConstant.populator_comp_ignore[name] not in subKey:
                        extra.append(subKey)
            else:
                extra=extraRaw
            for ikey in common:
                oriData=ori[ikey]
                retData=ret[ikey]
                attrList=classUtility.getAttrList(oriData)
                resObj=getClassObj('TestCaseResult', module='autoTest')
                resObj.name=ikey
                for item in attrList:
                    map={}
                    map['param']=item
                    map['expectValue']=getattr(oriData, item)
                    if hasattr(retData, item):
                        map['actValue']=getattr(retData, item)
                    else:
                        map['actValue']='Missing'
                    if '\n' in map['actValue']:
                            map['actValue']=map['actValue'].replace('\n','')
                    if map['expectValue'].strip().lower()==map['actValue'].strip().lower():
                        resObj.Pass.append(map)
                    else:
                        resObj.Fail.append(map)
                if resObj.Fail:
                    resObj.status='Fail'
                elif resObj.Missing:
                    resObj.status='Missing'
                elif resObj.Extra:
                    resObj.status='Extra'
                else:
                    resObj.status='Pass'
                resObjList.append(resObj)
            if miss:
                for misskey in miss:
                    resObj=getClassObj('TestCaseResult', module='autoTest')
                    resObj.name=misskey
                    resObj.status='NoReturn'
                    setattr(resObj, 'reasons', 'Fail to import')
                    resObjList.append(resObj)
            if extra:
                for extrakey in extra:
                    resObj=getClassObj('TestCaseResult', module='autoTest')
                    resObj.name=extrakey
                    resObj.status='Extra'
                    map={}
                    map['param']=extrakey
                    map['expectValue']='None'
                    map['actValue']=extrakey
                    resObj.Extra.append(map)
                    resObjList.append(resObj)
        suiteObj=getClassObj('TestSuiteResult', module='autoTest')
        suiteObj.name=name
        for item in resObjList:
            suiteObj.totalRun+=1
            oldVal=getattr(suiteObj, 'total'+item.status)
            oldVal+=1
            setattr(suiteObj, 'total'+item.status, oldVal)
            suiteObj.caseList.append(item)

        return suiteObj

if __name__=='__main__':
    import sys
    appServer=sys.argv[1]
    if len(sys.argv)==3:
        myPath=sys.argv[2]
    else:
        myPath=False
    appServer='192.168.20.116'
    dbServer='192.168.20.116'
    testPopulator=populatorTest(appServer, dbhost=dbServer, path=myPath)
    #test groups: DeviceGroupDefn, AppGroupDefn, ReportGroupDefn, RuleGroupDefn, ProtocolGroupDefn, NetworkGroupDefn, EventTypeGroupFinal, MetricGroupDefn, BizSrvcGroupDefn, DashboardGroupDefn}
    #testPopulator.testGroupDefn()
    #test generals: ApprovedDeviceVendorList, eventAttributeType, AppMapping, phIpSrvc4, eventType
    #for task in GENERAL_TASKS:
        #if task!='parserOrder':
            #testPopulator.testGeneralDefinition(type=task)
    testPopulator.testGeneralDefinition(type='vulnerability')
    #test modules: eventType, rule
    #for task in MODULE_TASKS.keys():
        #testPopulator.testModule('rule')
    #testPopulator.testModule('bizSrvc')

    print '\nTask finished.'

