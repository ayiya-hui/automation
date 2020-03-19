import XMLHelper
import reportDataClass
import xml.dom.minidom as dom

def createReportTemplate(data):
    reportList=[]
    include=QueryModels.Include()
    exclude=QueryModels.Exclude()
    custScope=QueryModels.CustomerScope(include, exclude)
    attrList=data['attrList']
    select=QueryModels.SelectClause(attrList)
    window=QueryModels.Window()
    interval=QueryModels.ReportInterval(window)
    subPattern=QueryModels.SubPattern(data['displayName'], data['filterName'], data['constr'], groupBy)
    pattern=QueryModels.PatternClause(subPattern)
    report=QueryModels.Report(data['reportType'], data['group'], data['name'], custScope, data['desc'], select, interval, pattern, data['relevantFilter'], order)
    reportList.append(report)
    node=XMLHelper.pickle(root=reportList, fabric=dom.Document(), elementName='Reports')

    return node.toxml()

if __name__=='__main__':
    data={}
    data['reportType']="PH_Report_Auth_Server_4"
    data['name']="Logon: Top Auth Servers,Users By Failed Logon Count"
    data['group']="PH_SYS_REPORT_AAAServer"
    data['desc']="Ranks Auth Servers, Users By Failed Logon Count"
    data['attrList']="reptDevIpAddr,user, COUNT( *)"
    data['orderAttrList']=" COUNT( *) DESC "
    data['displayName']="Filter_Auth_Server_4"
    data['filterName']="Filter_Auth_Server_4"
    data['constr']="reptDevIpAddr IN (Group@PH_SYS_APP_AUTH_SERVRE) AND eventType IN (Group@PH_SYS_EVENT_AAALogonFailure)"
    data['groupBy']="reptDevIpAddr, user"
    data['relevantFilter']="reptDevIpAddr"

    createReportTemplate(data)


