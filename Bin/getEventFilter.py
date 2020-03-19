from configModel import eventFilter


CONFIG={'full':'<?xml version="1.0" encoding="UTF-8"?><profile><groupNodes/><leafNodes/></profile>',
        'readonly':'<?xml version="1.0" encoding="UTF-8"?><profile><groupNodes><groupNode id="Admin_RoleMgmt"><actions><action action="read" target="node" value="false"/><action action="write" target="node" value="false"/><action action="execute" target="node" value="false"/></actions></groupNode><groupNode id="Dashboard_Tab"><actions><action action="read" target="node" value="true"/><action action="write" target="node" value="false"/><action action="execute" target="node" value="false"/></actions></groupNode><groupNode id="Analytics_Tab"><actions><action action="read" target="node" value="true"/><action action="write" target="node" value="false"/><action action="execute" target="node" value="false"/></actions></groupNode><groupNode id="Incidents_Tab"><actions><action action="read" target="node" value="true"/><action action="write" target="node" value="false"/><action action="execute" target="node" value="false"/></actions></groupNode><groupNode id="CMDB_Tab"><actions><action action="read" target="node" value="true"/><action action="write" target="node" value="false"/><action action="execute" target="node" value="false"/></actions></groupNode><groupNode id="Admin_Tab"><actions><action action="read" target="node" value="true"/><action action="write" target="node" value="false"/><action action="execute" target="node" value="false"/></actions></groupNode><groupNode id="Alerts_and_Tasks"><actions><action action="read" target="node" value="true"/><action action="write" target="node" value="false"/><action action="execute" target="node" value="false"/></actions></groupNode><groupNode id="Analytics_Query"><actions><action action="read" target="node" value="true"/><action action="write" target="node" value="false"/><action action="execute" target="node" value="true"/></actions></groupNode><groupNode id="Analytics_AdhocReport"><actions><action action="read" target="node" value="true"/><action action="write" target="node" value="false"/><action action="execute" target="node" value="true"/></actions></groupNode><groupNode id="Analytics_Report"><actions><action action="read" target="node" value="true"/><action action="write" target="node" value="false"/><action action="execute" target="node" value="true"/></actions></groupNode></groupNodes><leafNodes/></profile>',
        'network':'<?xml version="1.0" encoding="UTF-8"?><profile>
<groupNodes>
<groupNode id="CMDB_User">
<actions>
<action action="read" target="node" value="true"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="Admin_RoleMgmt">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DEVICE_Server">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DEVICE_Wkstn">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DEVICE_Storage">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="CMDB_Application">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_REPORT_Server">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_REPORT_Storage">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_REPORT_Application">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_Server">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_All_Devices">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_VMWare">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_NETAPP">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_Apps_All">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_Apps_APACHE">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_Apps_DB">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_Oracle_DB">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_MS_SQL">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_Active_Dir">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_Apps_IIS">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_Apps_DNS">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_Apps_DHCP">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Summary_Apps_EXCHANGE">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Device_Server">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Device_Appl">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Device_VM">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_OverallStatus">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_DASHBOARD_Device_Storage">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_RULE_Avail_Server">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_RULE_Avail_App">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_RULE_Perf_Server">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_RULE_Perf_App">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_RULE_Change_Server">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_RULE_Authen_Server">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_RULE_Authen_App">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_REPORT_DBAdmin">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_REPORT_ServerAdmin">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_REPORT_AppAvail">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_REPORT_AppPerf">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
<groupNode id="PH_SYS_REPORT_Compliance">
<actions>
<action action="read" target="node" value="false"/>
<action action="write" target="node" value="false"/>
<action action="execute" target="node" value="false"/>
</actions>
</groupNode>
 <groupNode id="Dashboard_Vm_View">
 <actions>
 <action action="read" target="node" value="false"/>
 <action action="write" target="node" value="false"/>
 <action action="execute" target="node" value="false"/>
 </actions>
 </groupNode>
</groupNodes>
<leafNodes/>
</profile>',
}

FILTER={'network':'hostIpAddr IN (Group@PH_SYS_DEVICE_Network) OR reptDevIpAddr IN (Group@PH_SYS_DEVICE_Network) OR srcIpAddr IN (Group@PH_SYS_DEVICE_Network) OR destIpAddr IN (Group@PH_SYS_DEVICE_Network)',
    'server':'hostIpAddr IN (Group@PH_SYS_DEVICE_Server) OR reptDevIpAddr IN (Group@PH_SYS_DEVICE_Server) OR srcIpAddr IN (Group@PH_SYS_DEVICE_Server) OR destIpAddr IN (Group@PH_SYS_DEVICE_Server)',
    'storage':'hostIpAddr IN (Group@PH_SYS_DEVICE_Storage) OR reptDevIpAddr IN (Group@PH_SYS_DEVICE_Storage) OR srcIpAddr IN (Group@PH_SYS_DEVICE_Storage) OR destIpAddr IN (Group@PH_SYS_DEVICE_Storage)',
    'windows':'hostIpAddr IN (Group@PH_SYS_DEVICE_WINDOWS_SERVER) OR reptDevIpAddr IN (Group@PH_SYS_DEVICE_WINDOWS_SERVER) OR srcIpAddr IN (Group@PH_SYS_DEVICE_WINDOWS_SERVER) OR destIpAddr IN (Group@PH_SYS_DEVICE_WINDOWS_SERVER)',
    'unix':'hostIpAddr IN (Group@PH_SYS_DEVICE_UNIX_SERVER) OR reptDevIpAddr IN (Group@PH_SYS_DEVICE_UNIX_SERVER) OR srcIpAddr IN (Group@PH_SYS_DEVICE_UNIX_SERVER) OR destIpAddr IN (Group@PH_SYS_DEVICE_UNIX_SERVER)',
    'system':'hostIpAddr IN (Group@PH_SYS_DEVICE_Server, Group@PH_SYS_DEVICE_Storage, Group@PH_SYS_DEVICE_Wkstn)  OR reptDevIpAddr IN (Group@PH_SYS_DEVICE_Server, Group@PH_SYS_DEVICE_Wkstn, Group@PH_SYS_DEVICE_Storage)  OR srcIpAddr IN (Group@PH_SYS_DEVICE_Server, Group@PH_SYS_DEVICE_Wkstn, Group@PH_SYS_DEVICE_Storage)  OR destIpAddr IN (Group@PH_SYS_DEVICE_Server, Group@PH_SYS_DEVICE_Wkstn, Group@PH_SYS_DEVICE_Storage)',
    'db':'hostIpAddr IN (Group@PH_SYS_DEVICE_WINDOWS_SERVER, Group@PH_SYS_DEVICE_UNIX_SERVER)  OR reptDevIpAddr IN (Group@PH_SYS_DEVICE_WINDOWS_SERVER, Group@PH_SYS_DEVICE_UNIX_SERVER)  OR srcIpAddr IN (Group@PH_SYS_DEVICE_WINDOWS_SERVER, Group@PH_SYS_DEVICE_UNIX_SERVER)  OR destIpAddr IN (Group@PH_SYS_DEVICE_WINDOWS_SERVER, Group@PH_SYS_DEVICE_UNIX_SERVER)',
    'full':'', 'readonly':'','helpdesk':'','execute':'', 'security':''}

def getRBACProfile(type):


def getEventFilter(type):
    myFilter=eventFilter()
    myFilter.fillInfo(FILTER[type])

    return myFilter

