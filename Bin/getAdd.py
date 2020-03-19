import dbAccess
import os
from xml.dom.minidom import parse, Node
import dataClass

RULE_PARAM=['Name', 'active', 'Description', 'CustomerScope', 'IncidentDef', 'PatternClause', 'TriggerEventDisplay']

def getParamsXML(dataPath):
    mapping={}
    files=os.listdir(dataPath)
    for file in files:
        if '.xml' in file:
            doc=parse(dataPath+'/'+file)
            for node1 in doc.getElementsByTagName('Rules'):
                for node2 in node1.getElementsByTagName('Rule'):
                    id=node2.getAttribute('id')
                    map2={}
                    map2['group']=node2.getAttribute('group')
                    for par in RULE_PARAM:
                        for node3 in node2.getElementsByTagName(par):
                            map2=getNodeText(map2, node3)

                    mapping[id]=map2
    return mapping

def getNodeText(map, node):
    for subNode in node.childNodes:
        if subNode.nodeType==Node.TEXT_NODE:
            map[node.tagName]=subNode.data
        else:
            getNodeText(map, subNode)
    return map

def getRuleFromDB():
        pass

def getAllFromDB(dbServer, event=False, rule=False, report=False):
    myDb=dbAccess.dbUtility(dbServer)
    myDb.connect()

    ruleData=[]
    if rule:
        map={}
        cmd="Select * from ph_drq_rule"
        data=myDb.execute(cmd)
        cmd1="Select * from ph_drq_clar_condition"
        data1=myDb.execute(cmd1)
        clearIds=[]
        for item in data1:
            id=item[0]
            filterId=0
            cmd2="Select event_filter_id from ph_drq_clear_condition2event_filter where clear_condition_id = "+str(id)
            data2=myDb.execute(cmd2)
            myClearSub=''
            if len(data2)!=0:
                filterId=data2[0][0]
                cmd3="Select name, single_constr, group_constr, group_by from ph_drq_filter where id = "+str(filterId)
                data3=myDb.execute(cmd3)
                if len(data3)!=0:
                    myClearSub=dataClass.SubPattern()
                    myClearSub.attribute['displayName']=data3[0][0]
                    myClearSub.attribute['name']=data3[0][0]
                    myClearSub.SingleEvtConstr=data3[0][1]
                    myClearSub.groupConstr=data3[0][2]
                    myClearSub.GroupByAttr=data3[0][3]
            ruleId=item[14]
            myClear=dataClass.ClearCondition()
            myClear.attribute['method']="Auto"
            myClear.attribute['type']=item[12]
            if myClear.attribute['type']=='timebased':
                myClear.fillbyTime(item[13])
            elif myClear.attribute['type']=='patternbased':
                myClearDef=dataClass.ClearIncidentDef()
                myClearDef.attribute['name']=item[11]
                myClearDef.ArgList=item[10]
                myClearConstr=item[7]
                myPattern=dataClass.PatternClause()
                myPattern.attribute['window']=item[13]
                myPattern=myClearSubList
                myClear.fillbyPattern(myClearDef, myClearConstr, myPattern)

        for item in data:
            mapId=item[5]
            myRule=dataClass.rule()
            id=item[0]
            typeId=item[22]
            myRule.attribute['id']=mapId
            myRule.active=item[8]
            myRule.Description=item[9]
            myRule.Name=item[10]
            myCustScope=dataClass.CustomerScope()
            myCustScope.attribute['groupByEachCustomer']=item[11]
            myRule.CustomerScope=myCustScope
            myPattern=dataClass.PatternClause()
            myPattern.attribute['window']=item[14]
            myOper=dataClass.Operator()
            oper=item[12].split(":")
            myOper.attribute['type']=oper[0]
            myOper.attribute['rank']=oper[1]
            myPattern.Operator=myOper
            myPattern.GlobalConstr=item[13]
            myRule.PatternClause=myPattern
            myTrigger=dataClass.TriggerEventDisplay()
            myTrigger.AttrList=item[21]
            myRule.TriggerEventDisplay=myTrigger
            if id in clearIds:
                pass







def getAddFromDB(dbServer, event=False, rule=False, report=False):
    myDb=dbAccess.dbUtility(dbServer)
    myDb.connect()

    eventData=''
    ruleData=''
    reportData=''

    if event:
        cmd="Select * from ph_event_type"
        data=myDb.execute(cmd)
        eventData={}
        for item in data:
            map={}
            id=item[9]
            map['Name']=id
            map['Display']=item[7]
            map['Severity']=item[10]
            eventData[id]=map

    if rule:
        cmd="Select * from ph_drq_rule"
        data=myDb.execute(cmd)
        ruleData={}
        for item in data:
            map={}
            id=item[5]
            map['Id']=str(item[0])
            map['Name']=item[10]
            map['Active']=item[8]
            ruleData[id]=map

    if report:
        cmd="Select * from ph_drq_report"
        data=myDb.execute(cmd)
        reptData={}
        for item in data:
            map={}
            id=item[5]
            map['Name']=item[11]
            map['Active']=item[8]
            reptData[id]=map

    return eventData, ruleData, reptData

if __name__=='__main__':
    import sys
    getAddFromDB(sys.argv[1])

