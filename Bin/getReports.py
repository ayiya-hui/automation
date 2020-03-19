import dbAccess
import os
from xml.dom.minidom import parse, Node

DATA_PATH='../TestData/Reports'

def getParams():
    mapping={}
    files=os.listdir(DATA_PATH)
    for file in files:
        if '.xml' in file:
            doc=parse(DATA_PATH+'/'+file)
            for node1 in doc.getElementsByTagName('Rules'):
                for node2 in node1.getElementsByTagName('Rule'):
                    id=node2.getAttribute('id')
                    map2={}
                    for node3 in node2.getElementsByTagName('Name'):
                        for node4 in node3.childNodes:
                            if node4.nodeType==Node.TEXT_NODE:
                                map2['Name']=node4.data
                    for node5 in node2.getElementsByTagName('active'):
                        for node6 in node5.childNodes:
                            if node6.nodeType==Node.TEXT_NODE:
                                map2['Active']=node6.data
                    mapping[id]=map2

    return mapping

def getReportsFromDB(dbServer):
    myDb=dbAccess.dbUtility(dbServer)
    myDb.connect()
    cmd="Select * from ph_drq_report"
    data=myDb.execute(cmd)
    mapping={}
    for item in data:
        map2={}
        id=item[5]
        map2['Name']=item[11]
        map2['Active']=item[8]
        mapping[id]=map2

    return mapping



