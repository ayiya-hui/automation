import dbDataHandler
import os
from xml.dom.minidom import parse
import XMLHelper
import classToHash

SIMPLE=['str','bool','dict','unicode']
KEYS=['displayName', 'id']

def getData(db, scope, id=False):
    myClass=dbDataHandler.dbDataHandler(db)
    myData={}
    if scope=='rule':
        if id:
            myData['rule']=myClass.getRuleData(naturalId=id)
        else:
            myData['rule']=myClass.getRuleData()
    if scope=='report':
        if id:
            myData['report']=myClass.getReportData(naturalId=id)
        else:
            myData['report']=myClass.getReportData()
    if scope=='role':
        if id:
            myData['role']=myClass.getRoleData(naturalId=id)
        else:
            myData['role']=myClass.getRoleData()
    if scope=='eventtype':
        if id:
            myData['eventtype']=myClass.getEventtypeData(naturalId=id)
        else:
            myData['eventtype']=myClass.getEventtypeData()
    if scope=='all':
        if id:
            myData['rule']=myClass.getRuleData(naturalId=id)
            myData['report']=myClass.getReportData(naturalId=id)
            myData['role']=myClass.getRoleData(naturalId=id)
            myData['eventtype']=myClass.getEventtypeData(naturalId=id)
        else:
            myData['rule']=myClass.getRuleData()
            myData['report']=myClass.getReportData()
            myData['role']=myClass.getRoleData()
            myData['eventtype']=myClass.getEventtypeData()

    return myData

def getXML(fileName=False, path=False, report=False):
    myData={}
    if path:
        myPath=path
    else:
        myPath=XML_PATH

    xmlFileList=[]
    if fileName:
        xmlFileList.append(fileName)
    else:
        xmlFileList=os.listdir(myPath)

    for xml in xmlFileList:
        if '.xml' in xml:
            doc=parse(myPath+'/'+xml)
            if report:
                rules=XMLHelper.unpickle(XMLHelper._getElementChilds(doc.childNodes[0]), type='list', report=True)
            else:
                rules=XMLHelper.unpickle(XMLHelper._getElementChilds(doc.childNodes[0]), type='list')
            for rule in rules:
                if hasattr(rule, 'active'):
                    if rule.active=='':
                        rule.active='true'
                if 'group' in rule.attribute.keys():
                    groupNames=rule.attribute['group'].split(',')
                    groupNames.sort()
                    rule.attribute['group']=','.join(groupNames)
                myHash=classToHash.classToHash(rule)
                myData[rule.attribute['id']]=myHash

    return myData

def compare(name, value1, value2, old, new):
    type=XMLHelper.getType(old)
    if type=='dict':
        for subName in old.keys():
            if subName in new.keys():
                if old[subName]!='' and new[subName]!='':
                    compare(subName, value1, value2, old[subName], new[subName])
    elif type=='list':
        for item in old:
            for key in new:
                for myKey in KEYS:
                    if myKey in item['attribute'].keys():
                        if item['attribute'][myKey]==key['attribute'][myKey]:
                            compare(name, value1, value2, item, key)

    else:
        if old!=new:
            print '\n%s:' % name
            print '%s: %s' % (value1, old)
            print '%s: %s' % (value2, new)

def output(oldData, newData, type, method):
    value1=''
    value2=''
    if method=='update':
        value1='OLD'
        value2='NEW'
    elif method=='install':
        if type=='eventtype':
            value1='CSV'
        else:
            value1='XML'
        value2='DB'

    bad=[]
    badId=[]
    newAdd=[]
    oldmiss=[]
    print 'BEFORE %s: total %ss %s' % (method, type, str(len(oldData)))
    print 'AFTER %s: total %ss %s' % (method, type, str(len(newData)))
    for id in oldData.keys():
        if id in newData.keys():
            correct='True'
            myoldData=oldData[id]
            mynewData=newData[id]
            if type=='eventtype':
                myId=myoldData['eventType']
            else:
                myId=myoldData['attribute']['id']
                myName=myoldData['Name']
            if myoldData!=mynewData:
                print '\nid: %s name: %s: Not Match' % (myId, id)

                for name in myoldData.keys():
                    compare(name, value1, value2, myoldData[name], mynewData[name])
                if type!='eventtype':
                    bad.append(myName)
                badId.append(myId)
        else:
            oldmiss.append(id)

    for id in newData.keys():
        if id not in oldData.keys():
            newAdd.append(id)

    if len(bad):
        print('\n%ss are changed %s:\n' % (type, len(bad)))
        for item in bad:
            print item


    if len(badId):
        print("\n%ss changed with natural IDs: %s\n" % (type, len(badId)))
        for item in badId:
            print(item)

    if len(oldmiss):
        print('\nOld %ss not showing up in new version: %s\n' % (type, len(oldmiss)))
        for item in oldmiss:
            print(item)
    else:
        print('\nNo old %s removed.' % type)

    if len(newAdd):
        print('\nNew %ss add in new version: %s\n' % (type, len(newAdd)))
        for item in newAdd:
            print(item)
    else:
        print('\nNo new %s added.' % type)




