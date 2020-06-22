"""This file contains all test related constants."""

default_config_file_path='../ConfigFiles/'
default_result_path='../Results/'
official_result_file='../Results/official_result.dat'
unofficial_result_file='../Results/unofficial_result.dat'

test_path='../TestData/%s'

rest_params={'Discover':{'test':'deviceMon/discover', 'verify':'deviceMon/status'},
             'discoverRequest':{'test':'deviceMon/discover', 'verify':'deviceMon/status'},
             'accessConfigs':{'test':'deviceMon/updateCredential', 'verify':''},
             'MaintSchedule':{'test':'deviceMaint/update', 'verify':''},
             'organization':{'test':['organization/add', 'organization/delete'], 'verify':''},
             'systemMonitor':{'test':'deviceMon/updateMonitor', 'verify':''},
             }

#sql constant
sql_default_port='5432'
sql_default_user='phoenix'
sql_default_password='J23lMBSo5DQ!'
sql_default_database_name='phoenixdb'
sql_query='Select %s from %s'
sql_values={'domain':{'values':['description', 'domain_id', 'name', 'company_name'], 'tableName':'ph_sys_domain', 'param':'name'},
        'ident':{'values':['alg', 'login_id', 'passcode', 'salt'], 'tableName':'ph_sec_ident', 'param':['domain_id','login_id']},
        'group_item':{'values':['item_id', 'group_id'], 'tableName':'ph_group_item'}
        }
sql_trans_names={'domain':'customer', 'company_name':'fullName', 'domain_id':'Attribute-custId'}

report_msg='The Test Report is generated. Please go to test web page to view it.'
test_result_counters=['totalRun', 'totalPass', 'totalNoReturn', 'totalFail']

report_summury_reference=''
report_index_html='../Public/index.html'

#supported tasks
supported_tasks=['DbPopulator','Discover','Incident','EventParsing','RestApi','LogDiscover']

#test result compare
compare_replace={'\n':'', ' ':''}
compare_list_keys={'rule':'index', 'report':'name', 'vulnerability':'osDeviceType', 'default':'name'}
compare_skip_extras=['ownerId', 'custId', 'id', 'Attribute-id', 'xmlId', 'dataChangeType', 'phIncidentCategory', 'lastModified', 'entityVersion', 'creationTime', 'dataCreationType']

#constants for test setup
default_user='admin'
default_cust='super'
default_password='Admin*11'
test_option_check='Check'
test_option_nocheck='NoCheck'
#constants for object index and xml wraper
file_obj_index={'widget':'id', 'eventAttrDesc':['eventAttributeType', 'code'], 'eventAttribByDevice':['deviceType', 'eventType'], 'incidentData':'incidentType', 'default':'name'}
obj_index={'deviceType':['vendor', 'model', 'version'],
           'group':'Attribute-name',
           'rule':'Attribute-naturalId',
           'Rule':'Attribute-id',
           'report':'Attribute-id',
           'query':'Attribute-naturalId',
           'malwareSite':'domainName',
           'widget':'Attribute-naturalId',
           'eventCode':['eventAttributeType', 'code'],
           'deviceEventAttribute':['deviceType', 'eventType'],
           'vulnerability':'vendorBugId',
           'affectedSoftware':'Attribute-id',
           'Role':'Attribute-id',
           'rbacProfile':'Attribute-naturalId',
           'device':'accessIp',
           'application':'accessIp',
           'event':'eventType',
           'eventParser':'Attribute-name',
           'clearCondition':'Attribute-ruleNaturalId',
           'eventFilter':'Attribute-id',
           'entityValue':'Attribute-name',
           'perfObject':'Attribute-id',
           'parsers':'Attribute-name',
           'default':'name'}
obj_xml_wrap={'vulnerability':'vulnerabilitys', 'parsers':'parsers', 'health':'phoenixSystem', 'query':'querys', 'status':'taskResults'}

#rest api param and object
obj_name_trans={'report':'query'}
rest_special_handling=['vulnerability', 'rule', 'domain', 'clearCondition']

#populator test constants
populator_comp_ignore={'eventAttribByDevice':'Microsoft-Windows-ANY-PH_'}
populator_default_path="../TestData/DbPopulator/"
populator_special_path={'eventParser':populator_default_path+'%s/', 'malwareDomainName':populator_default_path+'data-definition/domainName/', 'widget':populator_default_path+'data-definition/dashboard/widgets/'}
populator_normal_path=populator_default_path+'data-definition/%s'
split={'head':'<eventFormatRecognizer>', 'althead':'<patternDefinitions>', 'tail':'</parsingInstructions>'}
regex='<deviceType>\s*<Vendor>(?P<vendorName>[\S\s]+)</Vendor>\s*<Model>(?P<modelName>[\S\s]+)</Model>'
populator_skip_files=['GeneralPatternDefinitions.xml']
populator_special_handling=['eventAttrDesc', 'eventType', 'widget', 'eventAttribByDevice','rule', 'report', 'bizService', 'vulnerability', 'role']
populator_path_change={'rule':'rules', 'role':'roles', 'report':'reports', 'vulnerability':'vulnerabilities'}
class_attr_change={'Name':'name', 'Description':'description', 'RelevantFilterAttr':'relevantFilterAttr'}
populator_class_trans={'Report-query':{'attribute':{'group':'group', 'id':'attribute#naturalId'}, 'Name':'name', 'Description':'description', 'RelevantFilterAttr':'relevantFilterAttr'},
                 'Rule-rule':{'attribute':{'group':'group', 'id':'attribute#naturalId'}, 'Name':'name', 'Description':'description', 'RelevantFilterAttr':'relevantFilterAttr'},
                 'SubPattern-eventFilters':{'attribute':{'displayName':'name'}, 'GroupByAttr':'groupBy', 'GroupEvtConstr':'groupConstraint', 'SingleEvtConstr':'singleConstraint', 'INDEX':'index'},
                 'SelectClause':{'AttrList':'selectClause'},
                 'OrderByClause':{'AttrList':'orderByClause'},
                 'Window':{'attribute':{'unit':'reportWindowUnit', 'val':'reportWindow'}},
                 'PatternClause':{'attribute':{'window':'triggerWindow'}},
                 'TriggerEventDisplay':{'AttrList':'triggerEventAttrList'},
                 'IncidentDef':{'ArgList':'incidentAttrs', 'attribute':{'eventType':'incidentType'}},
                 'OrderByClause':{'AttrList':'orderByClause'},
                 'Role-rbacProfile':{'attribute':{'id':'attribute#naturalId'}, 'Name':'name', 'Description':'description', 'Config':'config', 'SingleEvtConstr':'eventFilter->singleConstraint',},
                 'eventAttrDesc-eventCode':'',
                 'eventAttribByDevice-deviceEventAttribute':''}
attr_titles=['name', 'description']
populator_type_switch={'rule':'Rule', 'role':'Role'}
populator_skip_compare_list=['xmlId', 'id', 'custId', 'ownerId', 'dataCreationType', 'dataChangeType', 'lastModified', 'entityVersion', 'creationTime']

csv_rest_trans={'malwareDomainName':'malwareSite'}
device_type_keys={'eventType':'description', 'deviceEventAttribute':'attrNameList'}
group_index_key={'DeviceGroupDefn':'Device', 'AppGroupDefn':'Application', 'ReportGroupDefn':'Report', 'RuleGroupDefn':'Rule', 'ProtocolGroupDefn':'Service', 'NetworkGroupDefn':'Network', 'EventTypeGroupFinal':'EventType', 'MetricGroupDefn':'Metrics', 'BizSrvcGroupDefn':'BizService', 'DashboardGroupDefn':'Widget'}
special_keys=['priority', 'valueType', 'usedByRbac', 'deprecated', 'eventParsed', 'type']
specialKeys={'eventAttrDesc':'eventAttributeType'}
special_package=['parser', 'eventType', 'eventCode', 'deviceEventAttribute']
value_type={'string':1, 'char':2, 'uchar':3, 'int16':4, 'uint16':5, 'int32':6, 'uint32':7, 'int64':8, 'uint64':9, 'ip':10, 'date':11, 'binary':12, 'double':14}

group_key_trans={'eventType':'EventType', 'bizService':'BizService'}
populator_task_trans={'AppMapping':'applicationPackage', 'ApprovedDeviceVendorList':'deviceType', 'eventAttributeTypes':'eventAttributeType', 'phIpSrvc4':'service', 'parserOrder':'parser', 'malwareDomainName':'malwareSite', 'bizSrvc':'bizService', 'vulnerabilities':['vulnerability', 'affectedSoftware']}
populator_rest_trans={'role':'rbacProfile', 'eventAttrDesc':'eventCode', 'eventAttribByDevice':'deviceEventAttribute'}
data_index={'deviceType':['model', 'vendor'],
            'group':'Attribute-name',
            'rule':'Attribute-naturalId',
            'report':'Attribute-naturalId',
            'malwareSite':'domainName',
            'widget':'Attribute-id',
            'eventCode':['eventAttributeType', 'code'],
            'deviceEventAttribute':'eventType',
            'vulnerability':'vendorBugId',
            }
default_data_index_key='name'
data_structure={'group':{0:'Attribute-name', 1:'parent', 2:'displayName', 3:'displayOrder'},
                'eventAttributeType':{0:'Attribute-attributeId', 1:'displayName', 2:'name', 3:'valueType', 9:'formatType', 14:'deprecated', 22:'usedByRbac', 23:'description'},
                'applicationPackage':{0:'appGroupName', 1:'pkgSignature', 2:'processName', 3:'processParam', 4:'name', 5:'priority', 6:'serviceString', 7:'objectGroup'},
                'service':{0:'name', 1:'portList', 2:'description'},
                'deviceType':{1:'vendor', 2:'model', 3:'version', 4:'type', 5:'objectGroup', 6:'services', 7:'bizSvcGroup', 8:'accessProtocols', 9:'eventParsed', 10:'priority'},
                'parser':{0:'name', 2:'priority'},
                'eventType':{0:['name', 'displayName'], 1:'description', 2:'group', 3:'severity'},
                'malwareSite':{0:'domainName'},
                'deviceEventAttribute':{0:'eventType', 1:'attrNameList'},
                'vulnerability':{0:'bugId', 1:'cveCode', 2:'vendorBugId', 3:'description', 4:'eventType'},
                'affectedSoftware':{5:'osVendor', 6:'osModel', 7:'osVersion', 8:'appVendor', 9:'appModel', 10:'fixVersion', 11:'patches', 12:'fixDate'}}
csv_special_handling=['eventAttrDesc', 'vulnerability']
csv_key_attrs={'eventAttrDesc':'eventAttributeType', 'eventAttribByDevice':'deviceType', 'incidentData':'incidentType'}
csv_device_info=['Vendor', 'Model', 'Version']
csv_class_attrs={'eventAttrDesc':['code', 'description'],
                 'eventAttribByDevice':['eventType', 'attrNameList'],
                 'eventType':['name', 'description', 'group', 'severity']}

#incident test
incident_initial_params={'phEventCategory':1, 'count':1, 'phCustId':'', 'eventName':'', 'phRecvTime':'any', 'eventSeverity':'', 'eventSeverityCat':'','eventType':'', 'hostIpAddr':'', 'incidentClearedTime':'any', 'incidentDetail':'', 'incidentFirstSeen':'any', 'incidentId':'', 'incidentLastSeen':'any', 'incidentRptIp':'', 'incidentStatus':0, 'incidentTarget':'', 'incidentTicketStatus':5, 'incidentViewStatus':1}
incident_aggregate_params={'count':2, 'incidentFirstSeen':'any', 'incidentId':'any', 'incidentStatus':0}
incident_data_path='IncidentMsgs'
incident_data_keys={'eventMsg':'list', 'clearEventMsg':'list'}
incident_query_params={'SingleEvtConstr':'phEventCategory=1 AND (incidentRptIp = %s AND eventType IN ("%s")) AND incidentStatus=0'}
incident_query_advance={'SingleEvtConstr':'phEventCategory=1 AND incidentId=%s AND incidentStatus=%s'}
incident_aggregate={'count':'', 'incidentFirstSeen':''}
incident_clear={'count':'', 'incidentFirstSeen':'', 'incidentLastSeen':''}
incident_debug_params={'SingleEvtConstr':'rawEventMsg = "%s"'}
incident_alter_params={'SingleEvtConstr':'rawEventMsg CONTAIN "%s"'}
approved_device_params=['srcIpAddr', 'destIpAddr', 'hostIpAddr']
incident_debug_query_special={'Important Process Stopped':'PH_DEV_MON_PROC_START',}

#event parsing test
event_query_params={'constr':'reptDevIpAddr IN (%s) AND eventType IN ("%s")'}
event_data_keys={'mapKey':'reptDevIpAddr(key)', 'reptDevIpAddr(key)':'str', 'eventMsg':'str', 'params':'map'}
event_ignore_params=['destName', 'rawEventMsg', 'hostName', 'srcName','destIntName', 'srcGeoCity', 'reptGeoCity', 'destGeoCity']
event_any_params=['eventId', 'phRecvTime', 'deviceTime']
event_replace_symbol=['/', ':']
#create device
create_device_types=['win','symantec','aaa', 'cisco', 'cisco_ips', 'esx', 'linux', 'bind_dns', 'snort_ips', 'fortinet', 'juniper_secure_access']
#create_device_types=['win','symantec','aaa', 'cisco', 'cisco_ips', 'esx', 'linux', 'bind_dns', 'fortinet', 'juniper_secure_access']
create_device_param='discovered/discover?sync=true'
create_device_domain_controller_msg='<13>$time $ip MSWinEventLog\t1\tSecurity\t9162\t$fullTime\t673\tSecurity\tSYSTEM\tUser\tSuccess Audit\tSJQAVWINADS\tAccount Logon\t\tService Ticket Request:   User Name: PARTHA_LAPTOP$@PROSPECT-HILLS.NET     User Domain: PROSPECT-HILLS.NET     Service Name: krbtgt     Service ID: %{S-1-5-21-3383442562-1768178646-255068551-502}     Ticket Options: 0x60810010     Ticket Encryption Type: 0x17     Client Address: 192.168.20.33     Failure Code: -     Logon GUID: {7bf641ec-0dcb-7718-cefa-3ba07f269654}     Transited Services: -        8604'
create_device_addon={'aaa':'win->runningSoftware', 'symantec':'win->swServices', 'bind_dns':'linux->runningSoftware', 'snort_ips':'linux->runningSoftware', 'cisco_ips':'cisco->base'}
create_device_wrap={'patches':'patch', 'runningSoftware':'application', 'interfaces':'networkInterface', 'SubPattern':'SubPattern'}

#create query xml
query_xml_create_delete_attrs=['inline', 'active', 'orderBy', 'PatternClause->GlobalConstr', 'PatternClause->Operator']

#restApi default
restApi_user='super/admin'
restApi_password='Admin*11'
restApi_path='/phoenix/rest'
restApi_query='query/eventQuery'
restApi_event='query/events/%s'
restApi_progress='query/progress/%s'
restApi_header={'Content-Type': 'text/xml'}
restApi_query_default_page=1000

#xml-to-object special handling
xml_2_obj_special={'attribute':{'attr':'name', 'text':'value'}}

#logDiscover test
logDiscover_data_path='LogDiscoverMsgs'
logDiscover_params=['reptDevIpAddr', 'model', 'vendor', 'version', 'creationMethod']
logDiscover_data_key={'eventMsg':'str'}

#perObj
perf_object_list=['sys_uptime_id','sys_cpu_id', 'sys_mem_id', 'sys_stat_id', 'sys_processes_id', 'sys_disk_id']






