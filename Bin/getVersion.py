import ComHandler
import logging
from xml.dom.minidom import Node, Document, parseString

def getVersion(config):
    myHandler=ComHandler.comHandler(config['dataCollector'], config['appServer'], config['user'], config['password'])
    queryString='cloudStatus/health'
    myHandler.getEvent("GET", urlString=queryString)
    param=parsingVersion(myHandler.xml)

    return param

def parsingVersion(xmlList):
    for xml in xmlList:
        doc=parseString(xml.encode('ascii', 'xmlcharrefreplace'))
        version=""
        for node in doc.getElementsByTagName("phoenixModuleInfo"):
            for node1 in node.getElementsByTagName("phoenixSystem"):
                for node2 in node1.getElementsByTagName("version"):
                    for node3 in node2.childNodes:
                        if node3.nodeType==Node.TEXT_NODE:
                            version=node3.data

    logging.debug("version is %s:", version)
    return version
