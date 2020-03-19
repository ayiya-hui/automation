import XMLHelper
import queryDataClass
import xml.dom.minidom as dom
from appHandler import appHandler
from hashUtility import hashMethod1
import classToHash
import logging

AUTOMATION='automation'
EVENTRPT='reptDevIpAddr'
INCIDENTRPT='incidentRptIp'

class queryHandler:
    def __init__(self):
        pass

    def getQuery(self, appServer, singleConstr, groups=False, orders=False, outputs=False, timeUnit=False, timeValue=False, filter=False, module=False, absTimes=False, timeLow=False, timeHigh=False):
        inXml=self.createQueryXml(singleConstr, groupBy=groups, orderBy=orders, outputConstr=outputs, timeUnits=timeUnit, timeVal=timeValue, filter=filter, module=module, absolute=absTimes, lowTime=timeLow, highTime=timeHigh)
        logging.debug(inXml)
        myHandler=appHandler(appServer)
        myHandler.getQuery(inXml)
        myQuery=[]
        for data in myHandler.queryXml:
            subQuery=''
            logging.debug(data)
            subQuery=XMLHelper.unpickleXml(data, 'events', objType='list')
            for subData in subQuery:
                myQuery.append(subData)

        myRet=[]
        for data in myQuery:
            resultHash=classToHash.classToHash(data)
            myDic=hashMethod1(resultHash['attributes'])
            myRet.append(myDic)

        self.data=myRet


    def createQueryXml(self, singleConstr, groupBy=False, orderBy=False, outputConstr=False, filter=False, timeUnits=False, timeVal=False, module=False, absolute=False, lowTime=False, highTime=False):
            data={}
            if timeUnits:
                data['unit']=timeUnits
            else:
                data['unit']='Minute'
            if timeVal:
                data['val']=timeVal
            else:
                data['val']='120'
            if lowTime:
                data['low']=lowTime
            if highTime:
                data['high']=highTime
            data['SingleEvtConstr']=singleConstr
            if groupBy:
                data['groupBy']=groupBy
            else:
                data['groupBy']=''
            if orderBy:
                data['orderBy']=orderBy
            else:
                data['orderBy']=''
            if outputConstr:
                data['outputConstr']=outputConstr
            else:
                data['outputConstr']=''
            if module:
                data['numEntries']='1'
                numEntry=True
            else:
                data['numEntries']='All'
                numEntry=False
            if filter:
                data['AttrList']=filter
            xml=self.createQueryTemplate(data, numEntry=numEntry, window=True, absolute=absolute, filter=filter)

            return xml

    def createQueryTemplate(self, data, numEntry=False, window=False, absolute=False, filter=False):
        queryList=[]
        report=queryDataClass.Report()
        report.attribute['group']=AUTOMATION
        report.attribute['id']=AUTOMATION
        report.OrderByClause=data['orderBy']
        custScope=queryDataClass.CustomerScope()
        custScope.attribute['groupByEachCustomer']='true'
        include=queryDataClass.Include()
        include.attribute['all']='true'
        exclude=queryDataClass.Exclude()
        custScope.Include=include
        custScope.Exclude=exclude
        report.CustomerScope=custScope
        select=queryDataClass.SelectClause()
        if numEntry:
            select.attribute['numEntries']=data['numEntries']
        else:
            select.attribute['numEntries']='All'
        if filter:
            select.AttrList=data['AttrList']
        report.SelectClause=select
        reportInterval=queryDataClass.ReportInterval()
        if not absolute:
            delattr(reportInterval, 'Low')
            delattr(reportInterval, 'High')
            myWindow=queryDataClass.Window()
            if window:
                myWindow.attribute['unit']=data['unit']
                myWindow.attribute['val']=data['val']
            else:
                myWindow.attribute['unit']='Minute'
                myWindow.attribute['val']='60'
            reportInterval.Window=myWindow
        else:
            delattr(reportInterval, 'Window')
            reportInterval.Low=data['low']
            reportInterval.High=data['high']
        report.ReportInterval=reportInterval
        pattern=queryDataClass.PatternClause()
        pattern.attribute['window']='3600'
        subPattern=queryDataClass.SubPattern()
        subPattern.attribute['displayName']=AUTOMATION
        subPattern.attribute['name']=AUTOMATION
        subPattern.SingleEvtConstr=data['SingleEvtConstr']
        subPattern.GroupByAttr=data['groupBy']
        pattern.SubPattern.append(subPattern)
        report.PatternClause=pattern
        queryList.append(report)
        node=XMLHelper.pickle(root=queryList, fabric=dom.Document(), elementName='Reports')

        return node.toxml()

if __name__=='__main__':
    data={}
    data['SingleEvtConstr']="reptDevIpAddr IN (Group@PH_SYS_APP_AUTH_SERVRE) AND eventType IN (Group@PH_SYS_EVENT_AAALogonFailure)"
    myXml=createQueryTemplate(data)
    print myXml
