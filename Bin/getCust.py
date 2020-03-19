import ComHandler
import logging
from xml.dom.minidom import Node, Document, parseString

def getCust(config):
    myHandler=ComHandler.comHandler(config['dataCollector'], config['appServer'], config['user'], config['password'])
    queryString='config/Domain'
    myHandler.getEvent("GET", urlString=queryString)
    param=parsingCust(myHandler.xml)

    return param

def parsingCust(xmlList):
    param=[]
    for xml in xmlList:
        doc=parseString(xml.encode('ascii','xmlcharrefreplace'))
        for node in doc.getElementsByTagName("domains"):
            for node1 in node.getElementsByTagName("domain"):
                xmlId=node1.getAttribute("xmlId")
                if xmlId in ['Domain$system', 'Domain$service', 'Domain$Super']:
                    pass
                else:
                    mapping={}
                    for node2 in node1.getElementsByTagName("domainId"):
                        for node3 in node2.childNodes:
                            if node3.nodeType==Node.TEXT_NODE:
                                mapping['domainId']=node3.data
                    for node4 in node1.getElementsByTagName("excludeRange"):
                        for node5 in node4.childNodes:
                            if node5.nodeType==Node.TEXT_NODE:
                                mapping['exclude']=node5.data
                    for node6 in node1.getElementsByTagName("includeRange"):
                        for node7 in node6.childNodes:
                            if node7.nodeType==Node.TEXT_NODE:
                                mapping['include']=node7.data
                    for node8 in node1.getElementsByTagName("name"):
                        for node9 in node8.childNodes:
                            if node9.nodeType==Node.TEXT_NODE:
                                mapping['name']=node9.data
                    if 'include' in mapping.keys():
                        param.append(mapping)
    logging.debug(param)
    return param
