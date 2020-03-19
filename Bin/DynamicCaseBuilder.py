from xml.dom.minidom import parse
import datetime

DATA_PATH='../TestData/'
EVENT_DATA_FILE='EventData.xml'
INCIDENT_DATA_FILE='IncidentData.xml'
REPORT_DATA_FILE='ReportData.xml'
EVENT_PARAM={}
INCIDENT_PARAM={}
REPORT_PARAM={'root':'reportDataSet', 'subroot':'reportDataList', 'node':'reportData', 'type':'reportType'}

def getData(setupTask, className):
    data=[]
    if className=="sentEvent":
        data=getEventData(setupTask.eventList)
    elif className=="sentIncident":
        data=getIncidentData(setupTask.incidentList)

    return data

def getReportData(setupValue, input=REPORT_PARAM):
    reportPath=DATA_PATH+REPORT_DATA_FILE
    param={}
    param['reportType']=setupValue
    doc=parse(reportPath)
    for node in doc.getElementsByTagName(input['root']):
        for node1 in node.getElementsByTagName(input['subroot']):
            for node2 in node1.getElementsByTagName(input['node']):
                type=node2.getAttribute(input['type'])
                if type==setupValue:
                    childList=_getElementChilds(node2)
                    for name, element in childList:
                        text=element.childNodes[0].data
                        param[name]=text

    return param

def getIncidentData(setupValue):
    incidentPath=DATA_PATH+INCIDENT_DATA_FILE
    data=[]
    doc=parse(incidentPath)
    for setup in setupValue:
        map={}
        param=dict()
        for node in doc.getElementsByTagName("incidentDataSet"):
            for node1 in node.getElementsByTagName("commonParam"):
                childList=_getElementChilds(node1)
                for name, element in childList:
                    text=element.childNodes[0].data
                    param[name]=text

            for node2 in node.getElementsByTagName("incidentDataList"):
                for node3 in node2.getElementsByTagName("incidentData"):
                    incidentType=node3.getAttribute("incidentType")
                    if incidentType==setup['incidentType']:
                        map['incidentType']=incidentType
                        map['reporter']=setup['reporter']
                        map['deviceName']=setup['deviceName']
                        childList=_getElementChilds(node3)
                        for name, element in childList:
                            if name!="incidentParam":
                                text=element.childNodes[0].data
                                map[name]=text
                        for node4 in node3.getElementsByTagName("incidentParam"):
                            childList=_getElementChilds(node4)
                            for name, element in childList:
                                text=element.childNodes[0].data
                                param[name]=text
                        map['param']=param
                        eventValue={}
                        eventValue['eventType']=map['eventType']
                        eventValue['reporter']=map['reporter']
                        eventValue['deviceName']=map['deviceName']
                        eventList=[]
                        eventList.append(eventValue)
                        eventData=getEventData(eventList)
                        for event in eventData:
                            map['msg']=event['msg']
                            map['sentMethod']=event['sentMethod']
                        data.append(map)
                    else:
                        map={}
    return data

def getEventData(setupValue):
    dataPath=DATA_PATH+EVENT_DATA_FILE
    data=[]
    doc=parse(dataPath)
    for setup in setupValue:
        map={}
        param=dict()
        for node in doc.getElementsByTagName("eventDataSet"):
            for node1 in node.getElementsByTagName("commomParam"):
                childList=_getElementChilds(node1)
                for name, element in childList:
                    text=element.childNodes[0].data
                    param[name]=text

            for node2 in node.getElementsByTagName("eventDataList"):
                for node3 in node2.getElementsByTagName("eventData"):
                    for node4 in node3.getElementsByTagName("deviceParam"):
                        childList=_getElementChilds(node4)
                        for name, element in childList:
                            text=element.childNodes[0].data
                            param[name]=text

                    for node5 in node3.getElementsByTagName("eventCase"):
                        eventType=node5.getAttribute("eventType")
                        if eventType==setup.eventType:
                            map['sentMethod']=node3.getAttribute("sentMethod")
                            map['eventType']=eventType
                            map['reporter']=setup.reporter
                            if 'deviceName' in dir(setup):
                                map['deviceName']=setup.deviceName
                            if map['reporter']=="$localhost":
                                for node6 in node5.getElementsByTagName("eventMsg"):
                                    for node7 in node6.childNodes:
                                        if node7.nodeType==node.CDATA_SECTION_NODE:
                                            msg=node7.data
                            else:
                                for node6 in node5.getElementsByTagName("syslogMsg"):
                                    for node7 in node6.childNodes:
                                        if node7.nodeType==node.CDATA_SECTION_NODE:
                                            msg=node7.data

                            time=datetime.datetime.now().strftime("%b %d %H:%M:%S")
                            if "$time" in msg:
                                msg=msg.replace("$time", time)
                            if "reporter" in msg:
                                msg=msg.replace("$reporter", map['reporter'])
                            if "$deviceName" in msg:
                                msg=msg.replace("$deviceName", map['deviceName'])
                            map['msg']=msg
                            for node8 in node5.getElementsByTagName("caseParam"):
                                childList=_getElementChilds(node8)
                                for name, element in childList:
                                    text=element.childNodes[0].data
                                    param[name]=text
                            param['eventType']=map['eventType']
                            param['rawEventMsg']=map['msg']
                            param['reptDevIpAddr']=map['reporter']
                            map['param']=param
                            data.append(map)
                        else:
                             map={}

    return data


def _getElementChilds(node):
    return [(no.nodeName, no) for no in node.childNodes if no.nodeType!=no.TEXT_NODE]

