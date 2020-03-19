import os
import time, datetime
import socket
from xml.dom.minidom import parse, parseString
import httplib2, ssl, re


DEFAULT_USER='super/admin'
DEFAULT_PASSWORD='admin*1'
RULE_URL='dataRequest/rule'
KEYS=['displayName', 'id']
SIMPLE=['int','float','str','bool','dict','unicode']
SPECIAL={'PatternClause':['SubPattern','Operator']}
XML_PATH='/opt/phoenix/data-definition/rules'
#XML_PATH='C:/dataCompare/312/rule'

class appHandler:
    def __init__(self, appServer, user=False, password=False):
        self.appServer=appServer
        if user:
            self.user=user
        else:
            self.user=DEFAULT_USER
        if password:
            self.password=password
        else:
            self.password=DEFAULT_PASSWORD

    def getEvent(self, method, urlString=False, xml=False):
        self.xml=SendQuery(self.appServer, self.user, self.password, method, inputString=urlString, inputXML=xml)

    def setSecure(self):
        self.appServer+=':443'

def SendQuery(appServer, user, password, method, inputString=False, inputXML=False):
    top_url="https://"+appServer+"/phoenix/rest/"
    h=httplib2.Http()
    h.add_credentials(user, password)
    outXML=[]

    if method == "POST" and inputXML==False:
        print "Missing input XML for PUT and POST methods. Exit."
        exit()

    if inputString:
        input=inputString
    else:
        input="query/eventQuery"

    if method=="GET":
        url1=top_url+input
        resp, content=h.request(url1, "GET")
        outXML.append(content.decode("utf-8"))
    elif method=="PUT":
        url1=top_url+input
        resp, content=h.request(url1, "PUT", inputXML)
        outXML.append(content.decode("utf-8"))
    elif method=="POST":
        header={'Content-Type': 'text/xml'}
        url1=top_url+input
        resp, content1=h.request(url1, "POST", inputXML, header)
        queryId=content1.decode("utf-8")
        if 'error code="255"' in queryId:
            print "Query Error, check sending XML file."
            exit()

        url2=top_url+"query/progress/"+queryId

        if(resp['status']=="200"):
            response1, content2=h.request(url2)
        else:
            print("DataCollector doesn't return query. Test failed. Error code is %s" % resp['status'])
            exit()

        while (content2.decode("utf-8")!="100"):
            response1, content2=h.request(url2)

        content3=''
        if (content2.decode("utf-8")=="100"):
            url3=top_url+"query/events/"+queryId+"/0/1000"
            response2, content3=h.request(url3)

        if content3!='':
            outXML.append(content3.decode("utf-8"))
            p=re.compile('totalCount="\d+"')
            mlist=p.findall(content3)
            if mlist[0]!='':
                mm=mlist[0].replace('"', '')
                m=mm.split("=")[-1]
                num=0
                if int(m)>1000:
                    num=int(m)/1000
                    if int(m)%1000>0:
                        num+=1
                if num>0:
                    for i in range(num):
                        url3=top_url+'query/events/'+queryId+'/'+str(i*1000+1)+'/1000'
                        resp4, content4=h.request(url3)
                        if content4!='':
                            outXML.append(content4.decode("utf-8"))

    return outXML


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


class dataHandler:
    def __init__(self, dbServer):
        self.dataHandler=appHandler(dbServer)

    def getRuleData(self):
        self.dataHandler.getEvent('GET', urlString=RULE_URL)
        myXml=self.dataHandler.xml[0].replace('DataRequest', 'Rule')
        doc=parseString(myXml.encode('ascii','xmlcharrefreplace'))
        myNode=doc.getElementsByTagName("Rules")[0]
        rules=unpickle(_getElementChilds(myNode), type='list')
        myRules={}
        for rule in rules:
            ruleType=rule.IncidentDef.attribute['eventType']
            myHash=classToHash(rule)
            myRules[ruleType]=myHash

        return myRules



def getData():
    myClass=dataHandler(socket.gethostbyname(socket.gethostname()))
    myClass.getRuleData()
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
                myHash=classToHash(rule)
                myData[rule.IncidentDef.attribute['eventType']]=myHash

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

def output(oldData, newData):
    bad={}
    newAdd={}
    oldmiss={}
    print 'XML: total rules %s' % str(len(oldData))
    print 'DB: total rules %s' % str(len(newData))
    for id in oldData.keys():
        if id in newData.keys():
            myoldData=oldData[id]
            mynewData=newData[id]
            naturalId=myoldData['attribute']['id']
            triggerEvent=myoldData['TriggerEventDisplay']
            all=myoldData['CustomerScope']['Include']
            mynewData['CustomerScope']['Include']=all
            mynewData['TriggerEventDisplay']=triggerEvent
            mynewData['attribute']['id']=naturalId
            incidentName=myoldData['Name']
            if str(myoldData).replace(" ", "")!=str(mynewData).replace(" ", ""):
                print '\nid: %s name: %s: Not Match' % (id, incidentName)
                print myoldData
                print mynewData

                for name in myoldData.keys():
                    compare(name, myoldData[name], mynewData[name])
                bad[naturalId]=incidentName
        else:
            oldmiss[naturalId]=incidentName

    for id in newData.keys():
        if id not in oldData.keys():
            newAdd[id]=newData[id]

    if len(bad):
        print '\nrules are changed %s:\n' % len(bad)
        for item in bad.keys():
            print '%s: %s' %(item, bad[item])

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
        myObj=Rule()
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

class Rule:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.Name=''
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
    myXML=getXML()
    myDB=getData()
    output(myXML, myDB['rule'])

    print 'Done'




