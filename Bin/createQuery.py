import xml.dom.minidom
from xml.dom.minidom import Node, Document
import logging


def CreateQueryXML(queryString, timeUnit=False, timeValue=False, startTime=False, endTime=False):
    queryMap={}
    if timeUnit and timeValue:
        queryMap['option']="relative"
        queryMap['timeUnit']=timeUnit
        queryMap['timeValue']=timeValue
    elif startTime and endTime:
        queryMap['option']="absolute"
        queryMap['startTime']=startTime
        queryMap['endTime']=endTime
    else:
        queryMap['option']="relative"
        queryMap['timeUnit']="Minute"
        queryMap['timeValue']="60"

    doc=Document()
    reports=doc.createElement("Reports")
    doc.appendChild(reports)

    report=doc.createElement("Report")
    report.setAttribute("id", "automation")
    report.setAttribute("group", "automation")
    reports.appendChild(report)

    name=doc.createElement("Name")
    report.appendChild(name)
    nameText=doc.createTextNode("Automation Query")

    custScope=doc.createElement("CustomerScope")
    custScope.setAttribute("groupByEachCustomer", "true")
    report.appendChild(custScope)
    include=doc.createElement("Include")
    include.setAttribute("all", "true")
    custScope.appendChild(include)
    exclude=doc.createElement("Exclude")
    custScope.appendChild(exclude)

    description=doc.createElement("description")
    report.appendChild(description)

    select=doc.createElement("SelectClause")
    select.setAttribute("numEntries", "All")
    report.appendChild(select)
    attrList=doc.createElement("AttrList")
    select.appendChild(attrList)

    reportInterval=doc.createElement("ReportInterval")
    report.appendChild(reportInterval)

    if queryMap['option']=='relative':
        window=doc.createElement("Window")
        window.setAttribute("unit", queryMap['timeUnit'])
        window.setAttribute("val", queryMap['timeValue'])
        reportInterval.appendChild(window)
    else: #absolute time
        low=doc.createElement("Low")
        reportInterval.appendChild(low)
        lowText=doc.createTextNode(queryMap['startTime'])
        low.appendChild(lowText)
        high=doc.createElement("High")
        reportInterval.appendChild(high)
        highText=doc.createTextNode(queryMap['endTime'])
        high.appendChild(highText)

    pattern=doc.createElement("PatternClause")
    pattern.setAttribute("window", "3600")
    report.appendChild(pattern)
    subPattern=doc.createElement("SubPattern")
    subPattern.setAttribute("displayName", "automation")
    subPattern.setAttribute("name", "automation")
    pattern.appendChild(subPattern)
    single=doc.createElement("SingleEvtConstr")
    subPattern.appendChild(single)

    singleText=doc.createTextNode(queryString)
    single.appendChild(singleText)

    filter=doc.createElement("RelevantFilterAttr")
    report.appendChild(filter)

    return doc.toxml()
