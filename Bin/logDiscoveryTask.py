import logging
import ComHandler
import time
import compareTestResult
from xml.dom.minidom import Node, Document, parseString
import deviceHandler

def runLogDiscovery(config, testSuite):
    option=config['option']
    myHandler=ComHandler.comHandler(config['dataCollector'], config['appServer'], config['user'], config['password'])
    myHandler.udpClient()
    totalParam=[]
    accessIps=[]

    for testcase in testSuite.testcases:
        accessIps.append(testcase.reporter)
        myHandler.sendEvent(testcase.discoverEvent)
        logging.debug(testcase.discoverEvent)

    myHandler.udpClientClose()
    finalResult=None
    if option!="SendOnly":
        #get deviceType
        typeQuery='config/deviceType'
        myHandler.getEvent("GET", urlString=typeQuery)
        deviceTypes=parsingDeviceType(myHandler.xml)
        time.sleep(120)
        queryString='config/device'
        myHandler.getEvent("GET", urlString=queryString)
        deviceXML=myHandler.xml
        queryString='config/application'
        myHandler.getEvent("GET", urlString=queryString)
        applicationXML=myHandler.xml

        param=parsingLogDiscoveryResult(deviceXML, applicationXML, accessIps)
        for item in param:
            for type in deviceTypes:
                if item['deviceType']==type['type']:
                    item['model']=type['model']
                    item['vendor']=type['vendor']

        finalResult=compareTestResult.runCompareResult(config, testSuite, param)

    return finalResult

def parsingDeviceType(xmlList):
    deviceTypes=[]
    for xml in xmlList:
        doc=parseString(xml.encode('ascii', 'xmlcharrefreplace'))
        for node in doc.getElementsByTagName("deviceTypes"):
            for node1 in node.getElementsByTagName("deviceType"):
                mapping={}
                mapping['type']=node1.getAttribute("xmlId")
                for node2 in node1.getElementsByTagName("model"):
                    for node3 in node2.childNodes:
                        if node3.nodeType==Node.TEXT_NODE:
                            mapping['model']=node3.data
                for node4 in node1.getElementsByTagName("vendor"):
                    for node5 in node4.childNodes:
                        if node5.nodeType==Node.TEXT_NODE:
                            mapping['vendor']=node5.data
                deviceTypes.append(mapping)

    return deviceTypes


def parsingLogDiscoveryResult(DevicexmlList, AppxmlList, accessIps):
    param=[]
    for Devicexml in DevicexmlList:
        doc=parseString(Devicexml.encode('ascii', 'xmlcharrefreplace'))
        for node in doc.getElementsByTagName("devices"):
            for node1 in node.getElementsByTagName("device"):
                mapping={}
                for node2 in node1.getElementsByTagName("accessIp"):
                    for node3 in node2.childNodes:
                        if node3.nodeType==Node.TEXT_NODE:
                            accessIp=node3.data
                            if accessIp in accessIps:
                                mapping['accessIp']=accessIp
                if 'accessIp' in mapping:
                    for node4 in node1.getElementsByTagName("creationMethod"):
                        for node5 in node4.childNodes:
                            if node5.nodeType==Node.TEXT_NODE:
                                mapping['creationMethod']=node5.data
                    for node6 in node1.getElementsByTagName("deviceType"):
                        for node7 in node6.childNodes:
                            if node7.nodeType==Node.TEXT_NODE:
                                mapping['deviceType']=node7.data
                    param.append(mapping)

    appParam=[]
    for Appxml in AppxmlList:
        doc=parseString(Appxml.encode('ascii', 'xmlcharrefreplace'))
        for node in doc.getElementsByTagName("applications"):
            for node1 in node.getElementsByTagName("application"):
                mapping={}
                for node2 in node1.getElementsByTagName("accessIp"):
                    for node3 in node2.childNodes:
                        if node3.nodeType==Node.TEXT_NODE:
                            accessIp=node3.data
                            if accessIp in accessIps:
                                mapping['accessIp']=accessIp
                if 'accessIp' in mapping:
                    for node4 in node1.getElementsByTagName("name"):
                        for node5 in node4.childNodes:
                            if node5.nodeType==Node.TEXT_NODE:
                                mapping['name']=node5.data
                    appParam.append(mapping)

    for item in param:
        for entry in appParam:
            if item['accessIp']==entry['accessIp']:
                item['name']=entry['name']

    return param




