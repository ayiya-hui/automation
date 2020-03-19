import Util.testUtility as testUtility
import Util.classUtility as classUtility
import Util.generalUtility as generalUtility
from Models.autoTestResultClass import TestCaseResult, TestSuiteResult
import ConfigConstants.TestConstant as TestConstant

class dataCompareHandler:
    """"This class will handle compare data."""
    def compare(self, name, testFile, expData, actData):
        """This method will compare expect data dictionary with actual data dictionary."""
        suiteObj=TestSuiteResult()
        suiteObj.testFileName=testFile
        suiteObj.name=name
        missKey, extraKey, commKey=testUtility.processDictKeys(expData, actData)
        if missKey:
            for key in missKey:
                caseObj=TestCaseResult()
                caseObj.name=key
                caseObj.status='NoReturn'
                suiteObj.caseList.append(caseObj)

        for key in commKey:
            type=classUtility.getType(expData[key])
            mapList=self.__compareObject(key, type, expData[key], actData[key])
            caseObj=TestCaseResult()
            caseObj.name=key
            failed=False
            for item in mapList:
                oldList=getattr(caseObj, item['status'])
                oldList.append(item)
                setattr(caseObj, item['status'], oldList)
                caseObj.status=self.__setCaseStatus(caseObj)
            suiteObj.caseList.append(caseObj)
        for case in suiteObj.caseList:
            suiteObj.totalRun+=1
            value=getattr(suiteObj, 'total'+case.status)+1
            setattr(suiteObj, 'total'+case.status, value)

        return suiteObj

    def __compareClass(self, name, expClass, actClass):
        params=[]
        missKey, extraKey, commKey=testUtility.processClassAttrs(expClass, actClass)
        if missKey:
            for key in missKey:
                map=self.__setResultMap(paramName=name+'.'+key, expValue=getattr(expClass, key))
                params.append(map)
        if extraKey:
            for key in extraKey:
                if key not in TestConstant.compare_skip_extras:
                    map=self.__setResultMap(paramName=name+'.'+key, actValue=getattr(actClass.key))
                    params.append(map)
        for key in commKey:
            subobj=getattr(expClass, key)
            type=classUtility.getType(subobj)
            params.extend(self.__compareObject(key, type, subobj, getattr(actClass, key)))

        return params

    def __compareList(self, name, expList, actList):
        index=None
        if not name in TestConstant.compare_list_keys:
            name='default'
        index=TestConstant.compare_list_keys[name]
        if index:
            indexExp=classUtility.addIndex(index, expList)
            indexAct=classUtility.addIndex(index, actList)
            params=self.__compareDict(index, indexExp, indexAct)

            return params

    def __compareDict(self, name, expDict, actDict):
        params=[]
        missKey, extraKey, commKey=testUtility.processDictKeys(expDict, actDict)
        if missKey:
            for key in missKey:
                map=self.__setResultMap(paramName=name+'.'+key, expValue=expDict[key])
                params.append(map)
        if extraKey :
            for key in extraKey:
                if key not in TestConstant.compare_skip_extras:
                    map=self.__setResultMap(paramName=name+'.'+key, actValue=actDict[key])
                    params.append(map)
        for key in commKey:
            value=expDict[key]
            type=classUtility.getType(value)
            params.extend(self.__compareObject(key, type, value, actDict[key]))

        return params

    def __compareValue(self, name, expVal, actVal):
        params=[]
        params.append(self.__setResultMap(paramName=name, expValue=expVal, actValue=actVal))
        return params

    compToken={'str':__compareValue, 'unicode':__compareValue, 'dict':__compareDict, 'list':__compareList, 'default':__compareClass}

    def __compareObject(self, name, type, expObj, actObj):
        if type not in self.compToken.keys():
            type='default'

        return self.compToken[type](self, name, expObj, actObj)

    def __setResultMap(self, paramName=None, expValue=None, actValue=None):
        status=None
        if expValue=='':
            expValue='None'
        if actValue==None:
            actValue='None'
        token={'param':paramName, 'expectValue':expValue, 'actValue':actValue}
        if not expValue:
            status='Extra'
        if not actValue:
            status='Missing'
        if expValue and actValue:
            if generalUtility.multiReplace(expValue.strip(), TestConstant.compare_replace)==generalUtility.multiReplace(actValue.strip(), TestConstant.compare_replace):
                status='Pass'
            else:
                status='Fail'
                print 'Not match for %s:\n' % paramName
                print generalUtility.multiReplace(expValue.strip(), TestConstant.compare_replace)
                print generalUtility.multiReplace(actValue.strip(), TestConstant.compare_replace)
                print '\n'
        map={}
        for key in token.keys():
            map[key]=token[key]
        map['status']=status

        return map

    def __setCaseStatus(self, caseObj):
        final=''
        for key in ['Fail', 'Missing', 'Extra']:
            if getattr(caseObj, key):
                value='1'
            else:
                value='0'
            final+=value

        return self.statusDict[int(final)]

    statusDict={0:'Pass', 1:'Extra', 10:'Missing', 11:'Missing', 100:'Fail', 101:'Fail', 110:'Fail', 111:'Fail'}




