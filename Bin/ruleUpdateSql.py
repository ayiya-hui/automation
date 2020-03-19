import os
import time, datetime
from xml.dom.minidom import parse, parseString


KEYS=['name', 'id']
REPLACE=['COUNT (','AND (','AVG (',') >', ') <', ') =', '( ', ' )', ', ', ' ,']
GROUP_SPECIAL=['srcIpAddr', 'destIpAddr', 'destName','AVG(pktLossPct)>= 50']
SIMPLE=['int','float','str','bool','dict','unicode']
SPECIAL={'PatternClause':['SubPattern','Operator']}
PREFIX='psql -h $DB -U phoenix phoenixdb -c "'
RULE='Select id, natural_id, name, cust_inclusive, raw_fo_str, trigger_event_attr, indent_type_id, trigger_window, incident_fire_freq from ph_drq_rule where cust_org_id = 0'
RULE2='Select incident_attr from ph_drq_rule where id = '
RULE3='Select global_constr from ph_drq_rule where id = '
RULE_FILTER_ID='Select event_filter_id from ph_drq_rule2event_filter where rule_id = '
FILTER='Select name, single_constr, group_by from ph_drq_filter where id = '
FILTER1='Select group_constr from ph_drq_filter where id = '
CLEAR='Select id, clear_option, clear_time_window, clear_incident_name, clear_incident_attrs, clear_global_constraints, clear_filter_operator from ph_drq_clear_condition where rule_id ='
CLEAR1='Select clear_constraints from ph_drq_clear_condition where rule_id ='
CLEAR_FILTER_ID='Select event_filter_id from ph_drq_clear_condition2event_filter where clear_condition_id = '
EVENT='Select name, severity from ph_event_type where id ='
XML_PATH='/opt/phoenix/data-definition/rules'
KEYWORDS=['event_filter_id', 'group_constr', 'clear_constraints', 'clear_time_window', 'single_constr', 'group_id', 'natural_id', 'rows','----','1row','1 row','global_constr','incident_attr']

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
    def __init__(self, host=False):
        if host:
            self.host=host
            self.prefix=PREFIX.replace('$DB', self.host)
        else:
            self.prefix=PREFIX.replace('-h $DB ', '')

    def execute(self, cmd):
        myCmd=self.prefix+cmd+'"'
        data=self.__getSQL(myCmd)

        return data

    def __getSQL(self, cmd):
        data=[]
        f=os.popen(cmd)
        lines=f.readlines()

        for line in lines:

            status=''
            for word in KEYWORDS:
                if word in line:
                    status='pass'
            if status!='pass':
                myList=line.strip().split('|')
                final=[]
                for item in myList:
                    if item.strip()=='t':
                        item='true'
                    elif item.strip()=='f':
                            item='false'
                    final.append(item.strip())
                if final!=[''] and final!=[':']:
                    data.append(final)

        return data

class dbDataHandler:
    def __init__(self, db=False):
        if db:
            self.db=dbUtility(host=db)
        else:
            self.db=dbUtility()

    def updateRule(self, name, newId):
        cmd=UPDATE_ID.replace('$VALUE', newId)+"'"+name+"'"
        print cmd
        self.db.execute(cmd)

    def getRuleData(self):
        myRules={}
        data=self.db.execute(RULE)
        for item in data:
            id=item[0]
            naturalId=item[1]
            myRule=rule()
            myRule.attribute['id']=naturalId
            myRule.Name=item[2].title()
            eventId=item[6]

            myCustScope=CustomerScope()
            myCustScope.attribute['groupByEachCustomer']=str(item[3]).lower()
            myInclude=Include()
            myInclude.attribute['all']=str(item[3]).lower()
            myCustScope.Include=myInclude
            myRule.CustomerScope=myCustScope
            myIncidentDef=self.__getIncidentDef(eventId, str(item[8]))
            myIncidentDef.ArgList=self.__replace(self.__getArgList(id))
            if myIncidentDef!='':
                myRule.IncidentDef=myIncidentDef
            globalConstr=self.__getGlobalConstr(id)
            myPattern=self.__getRulePattern(item[7], RULE_FILTER_ID, id, item[4], globalConstr)
            myRule.PatternClause=myPattern
            myTrigger=TriggerEventDisplay()
            myTrigger.AttrList=self.__replace(item[5].strip())
            myRule.TriggerEventDisplay=myTrigger
            myClear=self.__getClear(id)
            if myClear!='':
                myRule.ClearCondition=myClear
            myHash=classToHash(myRule)
            myRules[naturalId]=myHash

        return myRules

    def __getArgList(self, id):
        cmd=RULE2+id

        return self.__getText(cmd)

    def __getGlobalConstr(self, id):
        cmd=RULE3+id

        return self.__getText(cmd)

    def __getText(self, cmd):
        data=self.db.execute(cmd)
        myValue=''
        if len(data)>1:
            for value in data:
                myValue+=' '+value[0].replace(':','').strip()
            myValue=myValue.strip()
        elif len(data)==1:
            myValue=data[0][0]

        return myValue

    def __getIncidentDef(self, id, fireFreq):
        cmd=EVENT+str(id)
        data=self.db.execute(cmd)
        myIncidentDef=IncidentDef()
        myIncidentDef.attribute['fireFreq']=fireFreq
        if len(data)!=0:
            myIncidentDef.attribute['eventType']=data[1][0]
            myIncidentDef.attribute['severity']=data[1][1]

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
                if item[4]!='':
                    myClearDef.ArgList=item[4].strip()
                myPattern=self.__getRulePattern(item[2], CLEAR_FILTER_ID, clearId, item[6], item[5])
                myClear.ClearIncidentDef=myClearDef
                myClear.ClearConstr=self.__getClearConstr(id)
                myClear.PatternClause=myPattern

        return myClear

    def __getClearConstr(self, id):
        cmd=CLEAR1+id

        return self.__getText(cmd)

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
            if len(data)==2:
                myValue=data[1][0].replace(':','').strip()
                myValue1=data[0][-1]+' '+myValue
                data[0][-1]=myValue1
                data.remove(data[1])
            if len(data)!=0:
                for item in data:
                    myClearSub=SubPattern()
                    myClearSub.attribute['displayName']=item[0]
                    myClearSub.attribute['name']=item[0]
                    if item[1]!='':
                        myClearSub.SingleEvtConstr=self.__replace(item[1].strip())
                    if item[2]!='':
                        myClearSub.GroupByAttr=self.__replace(item[2]).strip()
                    myClearSub.GroupEvtConstr=self.__special(self.__replace(self.__getGroupConstr(id)))
                    filters.append(myClearSub)

        return filters

    def __special(self, value):
        value=value.replace('  ',' ')
        for item in GROUP_SPECIAL:
            orgItem='('+item+')'
            if orgItem in value:
                value=value.replace(orgItem,item)
        return value

    def __replace(self, value):
        value=value.replace('  ', ' ')
        for item in REPLACE:
            if item in value:
                place=item.replace(' ','')
                value=value.replace(item, place)
        return value

    def __getGroupConstr(self, id):
        cmd=FILTER1+id

        return self.__getText(cmd)

def getData(db=False):
    if db:
        myClass=dbDataHandler(db=db)
    else:
        myClass=dbDataHandler()
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
                if 'fireFreq' not in rule.IncidentDef.attribute.keys():
                    rule.IncidentDef.attribute['fireFreq']='86400'
                rule.Name=rule.Name.title()
                rule.IncidentDef.ArgList=__replace(__moveNewline(rule.IncidentDef.ArgList))
                for sub in rule.PatternClause.SubPattern:
                    sub.SingleEvtConstr=__replace(__moveNewline(sub.SingleEvtConstr))
                    sub.GroupEvtConstr=__special(__replace(__moveNewline(sub.GroupEvtConstr)))
                    sub.GroupByAttr=__replace(sub.GroupByAttr)
                if hasattr(rule.ClearCondition, 'ClearIncidentDef'):
                    if hasattr(rule.ClearCondition.ClearIncidentDef, 'ArgList'):
                        rule.ClearCondition.ClearIncidentDef.ArgList=__replace(__moveNewline(rule.ClearCondition.ClearIncidentDef.ArgList))
                if hasattr(rule.ClearCondition, 'ClearConstr'):
                    rule.ClearCondition.ClearConstr=__moveNewline(rule.ClearCondition.ClearConstr)
                if hasattr(rule.ClearCondition, 'PatternClause'):
                    if hasattr(rule.ClearCondition.PatternClause, 'SubPattern'):
                        for sub in rule.ClearCondition.PatternClause.SubPattern:
                            sub.SingleEvtConstr=__replace(__moveNewline(sub.SingleEvtConstr))
                            sub.GroupEvtConstr=__special(__replace(__moveNewline(sub.GroupEvtConstr)))
                            sub.GroupByAttr=__replace(sub.GroupByAttr)
                rule.TriggerEventDisplay.AttrList=__replace(rule.TriggerEventDisplay.AttrList)
                myHash=classToHash(rule)
                myData[rule.attribute['id']]=myHash

    return myData

def __special(value):
    value=value.replace('  ',' ')
    for item in GROUP_SPECIAL:
        orgItem='('+item+')'
        if orgItem in value:
            value=value.replace(orgItem,item)
    return value

def __moveNewline(param):
    myList=param.split('\n')
    myValue=''
    for item in myList:
        myValue+=item.strip()

    return myValue

def __replace(value):
    value=value.replace('  ',' ')
    for item in REPLACE:
        if item in value:
            place=item.replace(' ','')
            value=value.replace(item, place)
    return value




class output:
    def __init__(self):
        self.result={}
        self.errorString=''

    def output(self, oldData, newData, db=False):
        for id in oldData.keys():
            if id in newData.keys():
                myoldData=oldData[id]
                mynewData=newData[id]
                myName=mynewData['Name']
                if str(myoldData).replace(" ", "")!=str(mynewData).replace(" ", ""):
                    self.errorString+='\nid: '+id+' name: '+myName+': Not Match'+'\n'+str(myoldData)+'\n'+str(mynewData)
                    for name in myoldData.keys():
                        self.compare(name, myoldData[name], mynewData[name])
                    self.result[id]=myName

    def compare(self, name, old, new):
        if old!=new:
            type=getType(old)
            if type=='dict':
                for subName in old.keys():
                    if subName in new.keys():
                        if old[subName]!='' and new[subName]!='':
                            self.compare(subName, old[subName], new[subName])
            elif type=='list':
                for item in old:
                    for key in new:
                        for myKey in KEYS:
                            if myKey in item['attribute'].keys():
                                if item['attribute'][myKey]==key['attribute'][myKey]:
                                    self.compare(name, item, key)
            else:
                self.errorString+='\n'+name+':'+'\nXML: '+old+'\nDB: '+new

    def printResult(self, detail=False):
        if len(self.result):
            print '\nrules are changed %s:\n' % len(self.result)
            for item in self.result.keys():
                if detail:
                    print '\n%s: %s' %(item, self.result[item])
                else:
                    print '\n%s' % self.result[item]
        else:
            print 'No system rule changed.'

        if detail:
            if self.errorString!='':
                print self.errorString


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
        self.attribute['id']=''
        self.Name=''
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
        self.attribute['fireFreq']=''
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
        self.attribute['name']=''
        self.attribute['displayName']=''
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
    import sys
    usage='Usage: ruleUpdateSql.py [-h host]'
    myXML=getXML()
    if len(sys.argv)==1:
        myDB=getData()
        myOut=output()
        myOut.output(myXML, myDB['rule'])
        myOut.printResult()
    elif len(sys.argv)==3:
        if sys.argv[1]=='-h':
            myHost=sys.argv[2]
            myDB=getData(db=myHost)
            myOut=output()
            myOut.output(myXML, myDB['rule'])
            myOut.printResult()
        else:
            print usage
            exit()
    else:
        print usage
        exit()


    print 'Done'



