import os
import pgdb
import time, datetime
import socket
from xml.dom.minidom import parse, parseString


KEYS=['displayName', 'id']
SIMPLE=['int','float','str','bool','dict','unicode']
SPECIAL={'PatternClause':['SubPattern','Operator']}
PREFIX='psql -h 192.168.20.118 -U phoenix phoenixdb -c "'
RULE='Select id, natural_id, active, name, description, cust_inclusive, trigger_window, raw_fo_str, global_constr, trigger_event_attr, indent_type_id, incident_attr from ph_drq_rule'
RULE_FILTER_ID='Select event_filter_id from ph_drq_rule2event_filter where rule_id = '
FILTER='Select name, single_constr, group_constr, group_by from ph_drq_filter where id = '
CLEAR='Select id, clear_option, clear_time_window, clear_incident_name, clear_incident_attrs, clear_constraints, clear_global_constraints, clear_filter_operator from ph_drq_clear_condition where rule_id ='
CLEAR_FILTER_ID='Select event_filter_id from ph_drq_clear_condition2event_filter where clear_condition_id = '
EVENT='Select name, severity from ph_event_type where id ='
GROUP_ITEM='Select group_id from ph_group_item where item_id = '
GROUP='Select natural_id from ph_group where id = '
UPDATE_ID='Update ph_drq_rule Set natural_id=$VALUE Where natural_id ='
DEFAULT_PORT=5432
DEFAULT_USER='phoenix'
DEFAULT_PASSWORD='J23lMBSo5DQ!'
DEFAULT_DATABASE='phoenixdb'
XML_PATH='/opt/phoenix/data-definition/rules'

def getTime():
    now=datetime.datetime.now()
    uTime=str(int(time.mktime(now.timetuple())))

    return uTime

def classToHash(obj):
    myData={}
    nameList=[name for name in dir(obj) if not name.startswith("__")]
    for name in nameList:
        subobj=getattr(obj, name)
        myType=getType(subobj)
        if myType in SIMPLE:
            myData[name]=subobj
        elif myType=='NoneType':
            myData[name]=''
        elif myType=='list':
            subData=[]
            subData=_listToHash(subobj)
            myData[name]=subData
        else:
            subData={}
            subData=classToHash(subobj)
            myData[name]=subData

    return myData

def _listToHash(list):
    listData=[]
    for obj in list:
        myData=classToHash(obj)
        listData.append(myData)

    return listData

class dbUtility:
    def __init__(self, host):
        self.host=host+':'+str(DEFAULT_PORT)
        self.user='phoenix'
        self.password='J23lMBSo5DQ!'
        self.database='phoenixdb'

    def connect(self):
        try:
            self.conn=pgdb.connect(dsn=None, user=self.user, password=self.password, host=self.host, database=self.database)
        except:
            print "Exception encountered connecting database."

    def close(self):
        self.conn.close()

    def execute(self, cmd):
        myCur=self.conn.cursor()
        myVal=myCur.execute(cmd)
        row=''
        if myVal!=None:
            row=myCur.fetchall()
        myCur.close()

        return row

class dbDataHandler:
    def __init__(self, dbServer):
        self.db=dbUtility(dbServer)
        self.db.connect()

    def close(self):
        self.db.close()

    def updateRule(self, naturalId, newId):
        cmd=UPDATE_ID.replace('$VALUE', newId)+naturalId
        self.db.execute(cmd)

    def getRuleData(self):
        myRules={}
        data=self.db.execute(RULE)
        for item in data:
            id=item[0]
            naturalId=item[1]
            myRule=rule()
            myRule.attribute['id']=naturalId
            myRule.attribute['group']=self.__getGroupName(id)
            myRule.active=str(item[2]).lower()
            myRule.Name=item[3]
            myRule.Description=item[4]
            eventId=item[10]
            incident_attr=item[11].strip()

            myCustScope=CustomerScope()
            myCustScope.attribute['groupByEachCustomer']=str(item[5]).lower()
            myInclude=Include()
            myInclude.attribute['all']=str(item[5]).lower()
            myCustScope.Include=myInclude
            myRule.CustomerScope=myCustScope
            myIncidentDef=self.__getIncidentDef(eventId)
            myIncidentDef.ArgList=incident_attr
            if myIncidentDef!='':
                myRule.IncidentDef=myIncidentDef
            type=getType(item[8])
            if type!='NoneType':
                globalConstr=item[8].strip()
            else:
                globalConstr=''
            myPattern=self.__getRulePattern(str(item[6]), RULE_FILTER_ID, id, item[7], globalConstr)
            myRule.PatternClause=myPattern
            myTrigger=TriggerEventDisplay()
            myTrigger.AttrList=item[9].strip()
            myRule.TriggerEventDisplay=myTrigger
            myClear=self.__getClear(id)
            if myClear!='':
                myRule.ClearCondition=myClear
            myHash=classToHash(myRule)
            myRules[naturalId]=myHash

        return myRules

    def __getGroupName(self, id):
        groupNameList=[]
        groupId=self.__getGroupId(id)
        for item in groupId:
            cmd=GROUP+str(item)
            data=self.db.execute(cmd)
            if len(data)!=0:
                groupNameList.append(data[0][0])
        groupNameList.sort()
        groupName=','.join(groupNameList)
        return groupName

    def __getGroupId(self, id):
        groupList=[]
        cmd=GROUP_ITEM+str(id)
        data=self.db.execute(cmd)
        if len(data)!=0:
            for item in data:
                groupList.append(item[0])

        return groupList

    def __getIncidentDef(self, id):
        cmd=EVENT+str(id)
        data=self.db.execute(cmd)
        myIncidentDef=IncidentDef()
        if len(data)!=0:
            myIncidentDef.attribute['eventType']=data[0][0]
            myIncidentDef.attribute['severity']=str(data[0][1])

        return myIncidentDef

    def __getRulePattern(self, window, filterId, id, oper, constr):
        myPattern=PatternClause()
        myPattern.attribute['window']=window
        myPattern.SubPattern=self.__getFilter(self.__getFilterIds(filterId, id))
        if oper!='' and oper!=None:
            myOperList=[]
            operList=oper.split(",")
            for oper in operList:
                myOper=Operator()
                myList=oper.split(':')
                myOper.attribute['type']=myList[0]
                myOper.attribute['rank']=myList[1]
                myOperList.append(myOper)
            myPattern.Operator=myOperList

        if constr!='':
            myPattern.GlobalConstr=constr

        return myPattern

    def __getClear(self, id):
        cmd=CLEAR+str(id)
        data=self.db.execute(cmd)
        myClear=''
        if len(data)!=0:
            myClear=ClearCondition()
            item=data[0]
            clearId=item[0]
            myClear.attribute['method']="Auto"
            myClear.attribute['type']=item[1]
            if myClear.attribute['type']=='timebased':
                myClear.QuietPeriod=str(item[2])
            elif myClear.attribute['type']=='patternbased':
                myClearDef=ClearIncidentDef()
                myClearDef.attribute['name']=item[3]
                if item[4]!=None:
                    myClearDef.ArgList=item[4].strip()
                myPattern=self.__getRulePattern(str(item[2]), CLEAR_FILTER_ID, clearId, item[7], item[6])
                myClear.ClearIncidentDef=myClearDef
                if item[5]!=None:
                    myClear.ClearConstr=item[5]
                myClear.PatternClause=myPattern

        return myClear

    def __getFilterIds(self, filter, id):
        filterIds=[]
        cmd=filter+str(id)
        data=self.db.execute(cmd)
        if len(data)!=0:
            for item in data:
                filterIds.append(item[0])

        return filterIds

    def __getFilter(self, ids):
        filters=[]
        for id in ids:
            cmd=FILTER+str(id)
            data=self.db.execute(cmd)
            if len(data)!=0:
                for item in data:
                    myClearSub=SubPattern()
                    myClearSub.attribute['displayName']=item[0]
                    myClearSub.attribute['name']=item[0]
                    if item[1]!=None:
                        myClearSub.SingleEvtConstr=item[1].strip()
                    if item[2]!=None:
                        myClearSub.GroupEvtConstr=item[2].strip()
                    if item[3]!=None:
                        myClearSub.GroupByAttr=item[3].strip()
                    filters.append(myClearSub)

        return filters

def getData(db):
    myClass=dbDataHandler(db)
    myData={}
    myData['rule']=myClass.getRuleData()

    return myData

def getXML():
    myData={}
    xmlFileList=os.listdir(XML_PATH)

    for xml in xmlFileList:
        if '.xml' in xml:
            doc=parse(XML_PATH+'/'+xml)
            rules=unpickle(_getElementChilds(doc.childNodes[0]), type='list')
            for rule in rules:
                if hasattr(rule, 'active'):
                    if rule.active=='':
                        rule.active='true'
                if 'group' in rule.attribute.keys():
                    groupNames=rule.attribute['group'].split(',')
                    groupNames.sort()
                    rule.attribute['group']=','.join(groupNames)
                myHash=classToHash(rule)
                myData[rule.attribute['id']]=myHash

    return myData

def compare(name, old, new):
    type=getType(old)
    if type=='dict':
        for subName in old.keys():
            if subName in new.keys():
                if old[subName]!='' and new[subName]!='':
                    compare(subName, old[subName], new[subName])
    elif type=='list':
        for item in old:
            for key in new:
                for myKey in KEYS:
                    if myKey in item['attribute'].keys():
                        if item['attribute'][myKey]==key['attribute'][myKey]:
                            compare(name, item, key)

    else:
        if old.replace(" ", "")!=new.replace(" ", ""):
            print '\n%s:' % name
            print 'XML: %s' % old
            print 'DB: %s' % new

def output(oldData, newData, db, update=False):
    bad={}
    newAdd={}
    oldmiss={}
    print 'XML: total rules %s' % str(len(oldData))
    print 'DB: total rules %s' % str(len(newData))
    for id in oldData.keys():
        if id in newData.keys():
            myoldData=oldData[id]
            mynewData=newData[id]
            name=myoldData['Name']
            if str(myoldData).replace(" ", "")!=str(mynewData).replace(" ", ""):
                print '\nid: %s name: %s: Not Match' % (id, name)
                print myoldData
                print mynewData

                for name in myoldData.keys():
                    compare(name, myoldData[name], mynewData[name])
                bad[id]=name
        else:
            oldmiss[id]=name

    for id in newData.keys():
        if id not in oldData.keys():
            newAdd[id]=newData[id]

    if len(bad):
        print '\nrules are changed %s:\n' % len(bad)
        for item in bad.keys():
            print '%s: %s' %(item, bad[item])

    if update:
        myClass=dbDataHandler(db)
        for item in bad.keys():
            if item!='PH_Rule_Degraded_Ping_Net':
                newItem=item+'_Upgrade_'+getTime()
                myClass.updateRule(item, newItem)
                print 'natural id '+item+' changed to '+newItem

        myClass.close()


    if len(oldmiss):
        print '\nOld rules not showing up in new version: %s\n' % len(oldmiss)
        for item in oldmiss.keys():
            print '%s: %s' %(item, oldmiss[item])
    else:
        print '\nNo old rule removed.'

    if len(newAdd):
        print '\nNew rules add in new version: %s\n' % len(newAdd)
        for item in newAdd.keys():
            print '%s: %s' %(item, newAdd[item])
    else:
        print '\nNo new rule added.'


def getType(obj):
    p=str(obj.__class__)
    p=p.replace("<", "")
    p=p.replace(">", "")
    p=p.replace("'", "")
    if 'class' in p:
        p=p.replace("class", "")
    if 'type' in p:
        p=p.replace("type", "")
    p=p.split(".")[-1]

    return p.strip()

def _getElementChilds(node):
    return [(no.nodeName, no) for no in node.childNodes if no.nodeType!=no.TEXT_NODE and no.nodeName!='#comment']

def unpickle(node, type=False):
    if type:
        typeName=type
    else:
        typeName=node.tagName

    if typeName=="list":
        return _unpickleList(node)
    elif typeName=="dict":
        return _unpickleDict(node)
    else:
        obj=getClassInstance(typeName)
        nameList=[name for name in dir(obj) if not name.startswith("__")]
        if 'attribute' in nameList:
            name='attribute'
            map={}
            keys=obj.attribute.keys()
            keyList=node.attributes.keys()
            for item in keys:
                if item in keyList:
                    value=node.attributes.getNamedItem(item).nodeValue
                    map[item]=str(value).strip()
            setattr(obj, name, map)
        childs=_getElementChilds(node)
        for name, element in childs:
            subs=_getElementChilds(element)
            if not element.attributes and (len(subs)==0 or subs[0][0]=="#cdata-section"):
                if name in nameList:
                    if len(element.childNodes):
                        value=element.childNodes[0].nodeValue
                        setattr(obj, name, str(value).strip())
            elif element.attributes:
                subobj=unpickle(element)
                if _isSpecial(typeName, name):
                    myList=getattr(obj, name)
                    myList.append(subobj)
                    setattr(obj, name, myList)
                else:
                    setattr(obj, name, subobj)

            else:
                subobj=unpickle(element)
                setattr(obj, name, subobj)

    return obj



class XMLUnpicklingException(Exception): pass

def _unpickleList(nodelist):
    li=[]
    for name, element in nodelist:
        subobj=unpickle(element)
        li.append(subobj)

    return li

def _unpickleTuple(node):
    return tuple(_unpickleList(node))

def _unpickleDict(node):
    dd=dict()
    childList=_getElementChilds(node)
    for name, element in childList:
        text=element.childNodes[0].data
        dd[name]=text
    return dd

def _isSpecial(parent, child):
    if parent in SPECIAL.keys() and child in SPECIAL[parent]:
        return True
    else:
        return False




def getClassInstance(classType):
    myObj=''
    if classType=='Rule':
        myObj=rule()
    elif classType=='CustomerScope':
        myObj=CustomerScope()
    elif classType=='Include':
        myObj=Include()
    elif classType=='IncidentDef':
        myObj=IncidentDef()
    elif classType=='PatternClause':
        myObj=PatternClause()
    elif classType=='SubPattern':
        myObj=SubPattern()
    elif classType=='Operator':
        myObj=Operator()
    elif classType=='TriggerEventDisplay':
        myObj=TriggerEventDisplay()
    elif classType=='ClearCondition':
        myObj=ClearCondition()
    elif classType=='ClearIncidentDef':
        myObj=ClearIncidentDef()

    return myObj

class rule:
    def __init__(self):
        self.attribute={}
        self.attribute['group']=''
        self.attribute['id']=''
        self.Name=''
        self.active=''
        self.Description=''
        self.CustomerScope=''
        self.IncidentDef=''
        self.PatternClause=''
        self.TriggerEventDisplay=''
        self.ClearCondition=''

class CustomerScope:
    def __init__(self):
        self.attribute={}
        self.attribute['groupByEachCustomer']=''
        self.Include=''
        self.Exclude=''

class Include:
    def __init__(self):
        self.attribute={}
        self.attribute['all']=''

class IncidentDef:
    def __init__(self):
        self.attribute={}
        self.attribute['eventType']=''
        self.attribute['severity']=''
        self.ArgList=''

class PatternClause:
    def __init__(self):
        self.attribute={}
        self.attribute['window']=''
        self.SubPattern=[]
        self.Operator=[]
        self.GlobalConstr=''


class SubPattern:
    def __init__(self):
        self.attribute={}
        self.attribute['displayName']=''
        self.attribute['name']=''
        self.SingleEvtConstr=''
        self.GroupEvtConstr=''
        self.GroupByAttr=''

class Operator:
    def __init__(self):
        self.attribute={}
        self.attribute['rank']=''
        self.attribute['type']=''

class TriggerEventDisplay:
    def __init__(self):
        self.AttrList=''

class ClearCondition:
    def __init__(self):
        self.attribute={}
        self.attribute['method']=''
        self.attribute['type']=''
        self.ClearIncidentDef=''
        self.ClearConstr=''
        self.PatternClause=''
        self.QuietPeriod=''

class ClearIncidentDef:
    def __init__(self):
        self.attribute={}
        self.attribute['name']=''
        self.ArgList=''


if __name__=='__main__':
    host=socket.gethostbyname(socket.gethostname())
    myXML=getXML()
    myDB=getData(host)
    output(myXML, myDB['rule'], host)

    print 'Done'



