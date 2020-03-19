from xml.dom.minidom import Node, Document, parseString
import logging

def XMLParsingQueryResult(xml, check=False, filter=False):
    param=[]
    for xmlString in xml:
        doc=parseString(xmlString)
        for node in doc.getElementsByTagName("events"):
            for node1 in node.getElementsByTagName("event"):
                mapping={}
                for node2 in node1.getElementsByTagName("attributes"):
                    for node3 in node2.getElementsByTagName("attribute"):
                        itemName=node3.getAttribute("name")
                        for node4 in node3.childNodes:
                            if node4.nodeType==Node.TEXT_NODE:
                                if filter:
                                    if itemName in filter:
                                        mapping[itemName]=node4.data
                                else:
                                    mapping[itemName]=node4.data
                #check for exiting entry
                exist="false"
                for item in param:
                    if check:
                        if mapping['rawEventMsg']==item['rawEventMsg']:
                            exist="true"
                if exist=="false":
                    param.append(mapping)

    return param
