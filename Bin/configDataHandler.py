import XMLHelper
import appHandler
import xml.dom.minidom as dom
import generalUtility
import classUtility
import TestConstant
import testUtility

class configDataHandler:
    def __init__(self, appServer):
        self.appServer=appServer
        self.appHandler=appHandler.appHandler(appServer)

    def getData(self, type, index=True, pickle=True):
        if pickle:
            data=self.__getData(type)
        else:
            data=self.__getData(type, pickle=False)
        if pickle and index:
            indexData={}
            keyItem=testUtility.getKey(type)
            for item in data:
                if 'Attribute-' in keyItem:
                    key=item.attribute[keyItem.split('-')[-1]]
                elif classUtility.getType(keyItem)=='list':
                    values=[]
                    for subKey in keyItem:
                        values.append(getattr(item, subKey))
                    key='-'.join(values)
                else:
                    key=getattr(item, keyItem)
                indexData[key]=item
            if type in TestConstant.special_handling:
                finalData=self.__specialHandling(type, indexData)
            else:
                finalData=indexData
        else:
            finalData=data

        return finalData



    def _indexVulnerability(self, data):
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

    tokenDict={'vulnerability':_indexVulnerability, }

    def __specialHandling(self, type, data):
        if type in self.tokenDict.keys():
            return self.tokenDict[type](self, data)
        else:
            print '%s: this type is not supported.' % type
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



    def __indexDomain(self, data):
        finalDomains=[]
        collectors=self.getData('collector')
        if len(collectors):
            for domain in data:
                if domain.initialized=='true':
                    if hasattr(domain, 'collectors'):
                        domain.collectors=[]
                        for collector in collectors:
                            if domain.domainId==collector.attribute['custId']:
                                 domain.collectors.append(collector)
                    finalDomains.append(domain)
        else:
            finalDomains=data
        self.customers=finalDomains

        return finalDomains

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

    def __getData(self, name, module='config', pickle=True):
        myParam=module+'/'+name
        self.appHandler.getData(myParam)
        if pickle:
            if name in TestConstant.obj_name_trans.keys():
                keyWord=TestConstant.obj_name_trans[name]
            else:
                keyWord=name
            if keyWord in TestConstant.obj_xml_wrap.keys():
                pickKey=TestConstant.obj_xml_wrap[keyWord]
            else:
                pickKey=generalUtility.getPlural(keyWord)

            data=XMLHelper.unpickleXml(self.appHandler.xml, pickKey, objType='list')
        else:
            data=self.appHandler.xml

        return data


if __name__=='__main__':
    appServer='192.168.20.116'
    myConfig=configDataHandler(appServer)
    data=myConfig.getData('vulnerability')

    print len(data)
