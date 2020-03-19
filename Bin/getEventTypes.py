import ComHandler
from xml.dom.minidom import Node, Document, parseString

DEFAULT_USER='super/admin'
DEFUALT_PASSWORD='admin*1'

def getEventType(appServer,):
    myHandler=ComHandler.comHandler('', appServer, DEFAULT_USER, DEFAULT_PASSWORD)
    queryString='config/eventType'
    myHandler.getEvent("GET", urlString=queryString)
    param=parsingCust(myHandler.xml)

    return param

def parsingCust(xmlList):
    param=[]
    for xml in xmlList:
        doc=parseString(xml.encode('ascii','xmlcharrefreplace'))
        for node in doc.getElementsByTagName("eventTypes"):
            for node1 in node.getElementsByTagName("eventType"):
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
