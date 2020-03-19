import dbAccess
import ruleDataClass
import reportDataClass
import roleDataClass
import eventtypeDataClass
import classToHash
import XMLHelper
from xml.dom.minidom import parseString

RULE='Select id, natural_id, active, name, description, cust_inclusive, trigger_window, raw_fo_str, global_constr, trigger_event_attr, indent_type_id, incident_attr from ph_drq_rule'
RULE_FILTER_ID='Select event_filter_id from ph_drq_rule2event_filter where rule_id = '
FILTER='Select name, single_constr, group_constr, group_by from ph_drq_filter where id = '
CLEAR='Select id, clear_option, clear_time_window, clear_incident_name, clear_incident_attrs, clear_constraints, clear_global_constraints, clear_filter_operator from ph_drq_clear_condition where rule_id ='
CLEAR_FILTER_ID='Select event_filter_id from ph_drq_clear_condition2event_filter where clear_condition_id = '
EVENT='Select name, severity from ph_event_type where id ='
REPORT='Select id, natural_id, name, description, trigger_window, orderby_clause, select_clause, relevant_filter_attr, report_window, report_window_unit from ph_drq_report'
REPORT_FILTER_ID='Select event_filter_id from ph_drq_report2event_filter where report_id = '
GROUP_ITEM='Select group_id from ph_group_item where item_id = '
GROUP='Select natural_id from ph_group where id = '
ROLE='Select name, description, config, event_filter_id from ph_rbac_profile'
ROLE_FILTER='Select single_constr from ph_drq_filter where id = '
ROLE_ID={'Full Admin':'PH_Role_Full_Admin', 'Read-Only Admin':'PH_Role_Read_Only_Admin', 'Network Admin':'PH_Role_Network_Admin', 'Server Admin':'PH_Role_Server_Admin', 'Storage Admin':'PH_Role_Storage_Admin', 'Windows Server Admin':'PH_Role_Windows_Admin', 'Unix Server Admin':'PH_Role_Unix_Admin', 'Help Desk':'PH_Role_HelpDesk', 'Executive':'PH_Role_Executive', 'System Admin':'PH_Role_System_Admin', 'Security Admin':'PH_Role_Security_Admin', 'DB Admin':'PH_Role_DB_Admin'}
EVENT_TYPE='Select id, name, description, severity, cve_codes, device_type_id from ph_event_type'
DEVICE='Select model, vendor, version from ph_device_type where id ='

class dbDataHandler:
    def __init__(self, dbServer):
        self.db=dbAccess.dbUtility(dbServer)
        self.db.connect()

    def close(self):
        self.db.close()

    def getEventtypeData(self, naturalId=False):
        if naturalId:
            cmd=EVENT_TYPE+" where name = '"+naturalId+"'"
        else:
            cmd=EVENT_TYPE
        events=self.__getEvent(cmd)

        return events

    def getRuleData(self, naturalId=False):
        if naturalId:
            cmd=RULE+" where natural_id = '"+naturalId+"'"
        else:
            cmd=RULE
        rules=self.__getRule(cmd)

        return rules

    def getReportData(self, naturalId=False):
        if naturalId:
            cmd=REPORT+" where natural_id = '"+naturalId+"'"
        else:
            cmd=REPORT
        reports=self.__getReport(cmd)

        return reports

    def getRoleData(self, naturalId=False):
        if naturalId:
            cmd=ROLE+" where name = '"+naturalId+"'"
        else:
            cmd=ROLE
        roles=self.__getRole(cmd)

        return roles

    def __getEvent(self, cmd):
        event={}
        data=self.db.execute(cmd)
        #Select id, name, description, severity, cve_codes, device_type_id
        for item in data:
            id=item[0]
            deviceId=item[5]
            myEvent=eventtypeDataClass.eventtype()
            myEvent.eventType=item[1]
            if item[2]!=None:
                myEvent.eventName=item[2].strip()
            if item[3]!=None:
                if item[3]!=0:
                    myEvent.severity=str(item[3]).strip()
                else:
                    myEvent.severity=''
            if item[4]!=None:
                myEvent.cve=item[4]
            myEvent.eventGroup=self.__getGroupName(id)
            if deviceId!=None:
                myDevice=self.__getDeviceInfo(deviceId)
                myEvent.model=myDevice['model']
                myEvent.vendor=myDevice['vendor']
                myEvent.version=myDevice['version']
            myHash=classToHash.classToHash(myEvent)
            event[myEvent.eventType]=myHash

        return event


    def __getDeviceInfo(self, id):
        map={}
        cmd=DEVICE+str(id)
        data=self.db.execute(cmd)
        if len(data)!=0:
            map['model']=data[0][0]
            map['vendor']=data[0][1]
            map['version']=data[0][2]

        return map

    def __getRule(self, cmd):
        rule={}
        data=self.db.execute(cmd)
        for item in data:
            id=item[0]
            naturalId=item[1]
            myRule=ruleDataClass.rule()
            myRule.attribute['id']=naturalId
            myRule.attribute['group']=self.__getGroupName(id)
            myRule.active=str(item[2]).lower()
            myRule.Name=item[3]
            myRule.Description=item[4]
            eventId=item[10]
            incident_attr=item[11].replace(' ','').strip()

            myCustScope=ruleDataClass.CustomerScope()
            myCustScope.attribute['groupByEachCustomer']=str(item[5]).lower()
            myInclude=ruleDataClass.Include()
            myInclude.attribute['all']=str(item[5]).lower()
            myCustScope.Include=myInclude
            myRule.CustomerScope=myCustScope
            myIncidentDef=self.__getIncidentDef(eventId)
            myIncidentDef.ArgList=incident_attr
            if myIncidentDef!='':
                myRule.IncidentDef=myIncidentDef
            type=XMLHelper.getType(item[8])
            if type!='NoneType':
                globalConstr=item[8].replace(' ','').strip()
            else:
                globalConstr=''
            myPattern=self.__getRulePattern(str(item[6]), RULE_FILTER_ID, id, item[7], globalConstr)
            myRule.PatternClause=myPattern
            myTrigger=ruleDataClass.TriggerEventDisplay()
            myTrigger.AttrList=item[9].replace(' ','').strip()
            myRule.TriggerEventDisplay=myTrigger
            myClear=self.__getClear(id)
            if myClear!='':
                myRule.ClearCondition=myClear
            myHash=classToHash.classToHash(myRule)
            rule[naturalId]=myHash

        return rule

    def __getGroupName(self, id):
        groupNameList=[]
        groupId=self.__getGroupId(id)
        for item in groupId:
            cmd=GROUP+str(item)
            data=self.db.execute(cmd)
            if len(data)!=0:
                groupNameList.append(data[0][0])
        groupNameList.sort()
        groupName=','.join(groupNameList).replace(' ','')
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
        myIncidentDef=ruleDataClass.IncidentDef()
        if len(data)!=0:
            myIncidentDef.attribute['eventType']=data[0][0]
            myIncidentDef.attribute['severity']=str(data[0][1])

        return myIncidentDef

    def __getRulePattern(self, window, filterId, id, oper, constr):
        myPattern=ruleDataClass.PatternClause()
        myPattern.attribute['window']=window
        myPattern.SubPattern=self.__getFilter(self.__getFilterIds(filterId, id))
        if oper!='' and oper!=None:
            myOper=ruleDataClass.Operator()
            operList=oper.split(":")
            myOper.attribute['type']=operList[0]
            myOper.attribute['rank']=operList[1]
            myPattern.Operator=myOper
        if constr!='':
            myPattern.GlobalConstr=constr

        return myPattern

    def __getClear(self, id):
        cmd=CLEAR+str(id)
        data=self.db.execute(cmd)
        myClear=''
        if len(data)!=0:
            myClear=ruleDataClass.ClearCondition()
            item=data[0]
            clearId=item[0]
            myClear.attribute['method']="Auto"
            myClear.attribute['type']=item[1]
            if myClear.attribute['type']=='timebased':
                myClear.QuietPeriod=str(item[2])
            elif myClear.attribute['type']=='patternbased':
                myClearDef=ruleDataClass.ClearIncidentDef()
                myClearDef.attribute['name']=item[3]
                if item[4]!=None:
                    myClearDef.ArgList=item[4].replace(' ','').strip()
                myPattern=self.__getRulePattern(str(item[2]), CLEAR_FILTER_ID, clearId, item[7], item[6])
                myClear.ClearIncidentDef=myClearDef
                if item[5]!=None:
                    myClear.ClearConstr=item[5].replace(' ','')
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
                    myClearSub=ruleDataClass.SubPattern()
                    myClearSub.attribute['displayName']=item[0]
                    myClearSub.attribute['name']=item[0]
                    if item[1]!=None:
                        myClearSub.SingleEvtConstr=item[1].replace(' ','').strip()
                    if item[2]!=None:
                        myClearSub.GroupEvtConstr=item[2].replace(' ','').strip()
                    if item[3]!=None:
                        myClearSub.GroupByAttr=item[3].replace(' ','').strip()
                    filters.append(myClearSub)

        return filters

    def __getReport(self, cmd):
        report={}
        data=self.db.execute(cmd)
        for item in data:
            id=item[0]
            naturalId=item[1]
            myReport=reportDataClass.report()
            myReport.attribute['id']=naturalId
            myReport.attribute['group']=self.__getGroupName(id)
            myReport.Name=item[2]
            myReport.Description=item[3]

            myCustScope=reportDataClass.CustomerScope()
            myCustScope.attribute['groupByEachCustomer']="true"
            myInclude=reportDataClass.Include()
            myInclude.attribute['all']="true"
            myCustScope.Include=myInclude
            myReport.CustomerScope=myCustScope
            mySelect=reportDataClass.SelectClause()
            mySelect.attribute['numEntries']='All'
            mySelect.AttrList=item[6].replace(' ','')
            myReport.SelectClause=mySelect
            if item[5]!=None:
                myOrderBy=reportDataClass.OrderByClause()
                myOrderBy.AttrList=item[5].replace(' ','')
                myReport.OrderByClause=myOrderBy
            myInterval=reportDataClass.ReportInterval()
            myWin=reportDataClass.Window()
            if item[9]==0:
                myWin.attribute['unit']='Minute'
            elif item[9]==1:
                myWin.attribute['unit']='Hourly'
            myWin.attribute['val']=str(item[8])
            myInterval.Window=myWin
            myReport.ReportInterval=myInterval
            if item[7]!=None:
                myReport.RelevantFilterAttr=item[7].replace(' ','')
            myPattern=self.__getReportPattern(str(item[4]), REPORT_FILTER_ID, id)
            myReport.PatternClause=myPattern
            myHash=classToHash.classToHash(myReport)
            report[naturalId]=myHash

        return report

    def __getReportPattern(self, window, filterId, id):
        myPattern=reportDataClass.PatternClause()
        myPattern.attribute['window']=window
        myPattern.SubPattern=self.__getFilter(self.__getFilterIds(filterId, id))

        return myPattern

    def __getRole(self, cmd):
        role={}
        data=self.db.execute(cmd)
        for item in data:
            filterId=item[3]
            myRole=roleDataClass.Role()
            myRole.Name=item[0]
            naturalId=ROLE_ID[myRole.Name]
            myRole.attribute['id']=naturalId
            myRole.Description=item[1]
            doc=parseString(item[2])
            myProfile=XMLHelper.unpickle(doc.childNodes[0])
            myConfig=roleDataClass.Config()
            myConfig.profile=myProfile
            myRole.Config=myConfig
            myRole.SingleEvtConstr=self.__getRoleConstr(filterId)
            myHash=classToHash.classToHash(myRole)
            role[naturalId]=myHash

        return role

    def __getRoleConstr(self, id):
        filter=''
        cmd=ROLE_FILTER+str(id)
        data=self.db.execute(cmd)
        if len(data)!=0:
            filter=data[0][0]

        return filter





