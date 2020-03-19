import ComHandler
import datetime, time
from xml.dom.minidom import Node, Document, parseString
import os, os.path

DEFAULT_USER="super/admin"
DEFAULT_PASSWORD="admin*1"
NAMES=['moduleName','hostName']
PARAM=['cpu','physicalMemory','virtualMemory','upTime']

def getPHStatus(appServer, interval, path, user=None, password=None):
    if not user:
        user=DEFAULT_USER

    if not password:
        password=DEFAULT_PASSWORD

    if not os.path.exists(path):
        os.makedirs(path)

    comHandle=ComHandler.comHandler(appServer, appServer, user, password)
    queryString="cloudStatus/health"
    while 1:
    #while 1:
        comHandle.getEvent(queryString, "", "GET")
        status=processStatus(comHandle.xml)
        uTime=datetime.datetime.now().isoformat(" ").split(".")[0]
        for line in status:
            for key in line.keys():

                fileHandle=open(path+'/'+key+'.txt', 'a')
                fileHandle.write(line[key]+','+str(uTime)+'\n')
                fileHandle.close()

        time.sleep(interval)

def processStatus(xml):
    doc=parseString(xml)
    data=[]
    aNode=doc.getElementsByTagName("phoenixSystem")[0]
    superMap=[]
    for name in NAMES:
        bNode=aNode.getElementsByTagName(name)[0]
        for cNode in bNode.childNodes:
            if cNode.nodeType==Node.TEXT_NODE:
                superMap.append(cNode.data)
    dNode=aNode.getElementsByTagName("healthCounter")[0]
    for item in PARAM:
        for eNode in dNode.getElementsByTagName(item):
            for fNode in eNode.childNodes:
                if fNode.nodeType==Node.TEXT_NODE:
                    superMap.append(fNode.data)
    data.append(superMap)

    node=aNode.getElementsByTagName("subSystem")[0]
    for node1 in node.getElementsByTagName("phoenixSystem"):
        mapping=[]
        for name in NAMES:
            node2=node1.getElementsByTagName(name)[0]
            for node3 in node2.childNodes:
                if node3.nodeType==Node.TEXT_NODE:
                    mapping.append(node3.data)

        node4=node1.getElementsByTagName("healthCounter")[0]
        for item in PARAM:
            for node5 in node4.getElementsByTagName(item):
                for node6 in node5.childNodes:
                    if node6.nodeType==Node.TEXT_NODE:
                        mapping.append(node6.data)
        data.append(mapping)

    finalData=packageData(data)

    return finalData

def packageData(data):
    finalData=[]
    topData={}
    bottomData={}
    for item in data:
        if item[0] in ['phMonitorSupervisor','phMonitorWorker']:
            topName=item[1]
            newData=item
            del newData[:2]
            newString=','.join(newData)
            topData[topName]=newString
        else:
            bottomName=item[0]+'-'+item[1]
            newData=item
            del newData[:2]
            newString=','.join(newData)
            bottomData[bottomName]=newString

    finalData.append(topData)
    finalData.append(bottomData)
    return finalData

if __name__=='__main__':
    import sys


    if len(sys.argv)not in [4,6]:
        Usage="""Usage: PHStatusMonitor.py appServer interval path [username password]/
                    appServer -- IP address
                    interval  -- interval in minute
                    path      -- folder where saved the result

                    optional:
                    user      -- in super/admin format
                    password  -- password """
        print Usage
        exit()

    appServer=sys.argv[1]
    interval=int(sys.argv[2])*60
    path=sys.argv[3]

    try:
        pid=os.fork()
        if pid>0:
            sys.exit(0) #exit first parent
    except OSError, e:
        print >>sys.stderr, "for #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    #decouple from parent
    os.setsid()
    os.umask(0)

    #second fork
    try:
        pid=os.fork()
        if pid>0: #exit out second parent, print out eventual PID
            print "Daemon PID %d" % pid
            sys.exit(0)
    except  OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    if len(sys.argv)==4:
        getPHStatus(appServer,float(interval), path)
    else:
        username=sys.argv[4]
        password=sys.argv[5]
        getPHStatus(appServer,float(interval), path, user=username, password=password)

