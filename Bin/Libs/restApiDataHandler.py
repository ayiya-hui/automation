from XmlHandler import XmlHandler
from appHandler import appHandler
import Util.testUtility as testUtility
import Util.generalUtility as generalUtility
import Util.classUtility as classUtility
import ConfigConstants.TestConstant as TestConstant
import types

class restApiDataHandler:
    """This class will handle Accelops REST API mechnism.
    It will start an appServer class instance to get XML data, then return an indexed
    object."""
    def __init__(self, appServer, user=False, password=False):
        self.appServer=appServer
        self.appHandler=appHandler(appServer, user=user, password=password)
        self.xmlHandler=XmlHandler()

    def getData(self, datatype, index=True, pickle=True, noKey=False, module='config', arg={}):
        """This method will call GET to return a dictinary of indexed objects."""
        data=''
        if pickle:
            data=self.__getData(datatype, module, noKey=noKey, args=arg)
        else:
            data=self.__getData(datatype, module, pickle=False, args=arg)
        if data:
            if module=='namedValue':
                datatype='entityValue'
            if type(data)==types.ListType:
                if pickle and index:
                    indexData={}
                    if datatype in TestConstant.obj_name_trans.keys():
                        fiType=TestConstant.obj_name_trans[datatype]
                    else:
                        fiType=datatype
                    keyItem=testUtility.getKey(fiType)
                    for item in data:
                        if item is not None:
                            if 'Attribute-' in keyItem:
                                key=item.attribute[keyItem.split('-')[-1]]
                            elif classUtility.getType(keyItem)=='list':
                                values=[]
                                for subKey in keyItem:
                                    subVal=getattr(item, subKey)
                                    if subVal==None:
                                        subVal=''
                                    values.append(subVal)
                                key='@'.join(values)
                            else:
                                key=getattr(item, keyItem)
                            if key not in indexData.keys():
                                indexData[key]=item
                            else:
                                oldData=indexData[key]
                                Li=[]
                                if classUtility.getType(oldData)=='list':
                                    Li=oldData
                                    Li.append(item)
                                else:
                                    Li.append(oldData)
                                    Li.append(item)
                                indexData[key]=Li
                    if datatype in TestConstant.rest_special_handling:
                        finalData=self.__specialHandling(datatype, indexData)
                        return finalData
                    else:
                        return indexData
                else:
                    return data

            else:
                return data
        else:
            return data



    def __indexVulnerability(self, data):
        indexData={}
        affectSwData=self.getData('affectedSoftware')
        deviceTypeData=self.getData('deviceType')
        idIndexDevType=testUtility.rekeyKey('Attribute-id', deviceTypeData)
        for key in data.keys():
            asList=[]
            for sw in affectSwData.keys():
                vi=affectSwData[sw].vulnerability.split('@')[-1]
                if vi==data[key].attribute['id']:
                    di=affectSwData[sw].osDeviceType.split('@')[-1]
                    if di and di in idIndexDevType.keys():
                        affectSwData[sw].osDeviceType=idIndexDevType[di]
                    asList.append(affectSwData[sw])
            data[key].affectedSoftwares=asList
            indexData[key]=data[key]
        return indexData

    def __indexRule(self, data):
        indexData={}
        clearConditions=self.getData('clearCondition')
        if clearConditions is not None:
            for key in data.keys():
                if data[key].attribute['naturalId'] in clearConditions.keys():
                    setattr(data[key], 'clearCondition', clearConditions[data[key].attribute['naturalId']])
                indexData[key]=data[key]
        else:
            indexData=data

        return indexData

    def __indexDomain(self, data):
        indexData={}
        collectors=self.getData('eventCollector')
        if collectors:
            for subkey in data:
                if data[subkey].initialized=='true':
                    if hasattr(data[subkey], 'collectors'):
                        data[subkey].collectors=[]
                        for morekey in collectors:
                            if data[subkey].domainId==collectors[morekey].attribute['custId']:
                                 data[subkey].collectors.append(collectors[morekey])
                    indexData[data[subkey].name]=data[subkey]
        else:
            indexData=data
        for key in indexData.keys():
            if key in ['Super', 'service', 'system']:
                del indexData[key]

        return indexData

    def __indexClearCondition(self, data):
        indexData={}
        clearEventFilters=self.getData('eventFilter')
        for key in data.keys():
            mydata=data[key]
            if type(mydata.clearEventFilters)!=types.NoneType:
                filterId=mydata.clearEventFilters.split('@')[-1].strip()
                if filterId in clearEventFilters.keys():
                    setattr(mydata, 'clearEventFilters', clearEventFilters[filterId])
            indexData[key]=mydata

        return indexData

    tokenDict={'vulnerability':__indexVulnerability, 'rule':__indexRule, 'domain':__indexDomain,
               'clearCondition':__indexClearCondition,
              }

    def __specialHandling(self, datatype, data):
        if datatype in self.tokenDict.keys():
            return self.tokenDict[datatype](self, data)
        else:
            print '%s: this type is not supported.' % datatype
            return {}

    def __indexDeviceEventAttribute(self, data):
        indexData={}
        deviceTypes=self.getData('deviceType')
        for item in data:
            deviceId=item.deviceType.split('@')[-1]
            for key in deviceTypes.keys():
                if deviceId==deviceTypes[key].attribute['id']:
                    item.deviceType=deviceTypes[key]
            item.eventType=item.eventType.split('$')[-1]
            indexData[item.eventType]=item

        return indexData

    def __indexEventCode(self, data):
        indexData={}
        keys=CSVHandler.getKeys('eventCode')
        for item in data:
            values=[]
            for key in keys:
                myVal=getattr(item, key)
                if 'EventAttributeType$' in myVal:
                    values.append(myVal.split('$')[-1])
                else:
                    values.append(myVal)
            value='-'.join(values)
            indexData[value]=item

        return indexData


    def __indexEventParser(self, data):
        indexData={}
        parsers=self.__getData('parsers', module='device')
        indexParser={}
        for par in parsers:
            indexParser[par.name]=par
        for item in data:
            item.priority=indexParser[item.attribute['name']].priority
            indexData[item.attribute['name']]=item

        return indexData

    def __indexGroup(self, data):
        indexData={}
        for item in data:
            if item.attribute['type'] in indexData.keys():
                map=indexData[item.attribute['type']]
            else:
                map={}
            if item.parent:
                item.parent=item.parent.split('$')[-1]
            map[item.attribute['name']]=item
            indexData[item.attribute['type']]=map

        return indexData

    def __indexNotification(self, data):
        actions=self.__getData('notificationAction')
        conditions=self.__getData('notificationCondition')
        indexData={}
        indexData['All']=[]
        for item in data:
            item.actions=[]
            for action in actions:
                if action.policy.split('@')[-1]==item.attribute['id']:
                    item.actions.append(action)
            item.conditions=[]
            for condition in conditions:
                if condition.policy.split('@')[-1]==item.attribute['id']:
                    item.conditions.append(condition)
                    item.attribute['naturalId']=condition.name
            if not len(item.attribute):
                indexData['All'].append(item)
            else:
                indexData[item.attribute['naturalId']]=item


        return indexData

    def __getData(self, name, module, noKey=False, pickle=True, args={}):
        if module=='namedValue':
            myParam=module+'/group?name='+name
            pickname='entityValue'
        else:
            myParam=module+'/'+name
            pickname=name
        if args:
            argStr=''
            argList=[]
            for key in args.keys():
                argList.append(key+'='+args[key])
                argStr='?'+'&'.join(argList)
            myParam+=argStr
        self.appHandler.getData(myParam)
        data=''
        if self.appHandler.xml:
            if pickle:
                if pickname in TestConstant.obj_name_trans.keys():
                    keyWord=TestConstant.obj_name_trans[pickname]
                else:
                    keyWord=pickname
                if keyWord in TestConstant.obj_xml_wrap.keys():
                    pickKey=TestConstant.obj_xml_wrap[keyWord]
                else:
                    if noKey:
                        pickKey=None
                    else:
                        pickKey=generalUtility.getPlural(keyWord)
                data=self.xmlHandler.XmlStringToObj(self.appHandler.xml, keyword=pickKey)
            else:
                data=self.appHandler.xml

        return data

