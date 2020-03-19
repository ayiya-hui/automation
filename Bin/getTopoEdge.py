import os
from xml.dom.minidom import parse
import XMLHelper

def getXML(fileName):
    doc=parse(fileName)
    myData=XMLHelper.unpickle(XMLHelper._getElementChilds(doc.childNodes[0]), type='list')

    return myData


def output(oldData, newData, type):
    oldNodeName=getList(oldData)
    newNodeName=getList(newData)
    oldDiff=[]
    newDiff=[]

    for name in oldNodeName:
        if name not in newNodeName:
            oldDiff.append(name)

    for name in newNodeName:
        if name not in oldNodeName:
            newDiff.append(name)

    print 'compare %s' % type
    if len(oldDiff):
        print 'In first, not second:'
        for name in oldDiff:
            oldNode=getNode(name, oldData)
            nameList=[name for name in dir(oldNode) if not name.startswith("__")]
            for item in nameList:
                print '%s: %s' % (item, getattr(oldNode, item))


    if len(newDiff):
        print 'In second, not first:'
        for name in newDiff:
            newNode=getNode(name, newData)
            nameList=[name for name in dir(newNode) if not name.startswith("__")]
            for item in nameList:
                print '%s: %s' % (item, getattr(newNode, item))

def getNode(name, data):
    myNode=''
    for item in data:
        nodeList=item.topoNode
        for node in nodeList:
            if name==node.attribute['name']:
                myNode=node

    return myNode


def getList(oldList):
    newList=[]
    for item in oldList:
        nodeList=item.topoNode
        for node in nodeList:
            newList.append(node.attribute['name'])

    return newList

def prepare(data):
    myData={}
    netList=[]
    hostList=[]
    l2List=[]
    for item in data:
        myType=item.attribute['type']
        if myType=='NetworkEdge':
            netList.append(item)
        elif myType=='HostEdge':
            hostList.append(item)
        elif myType=='L2TrunkEdge':
            l2List.append(item)

    myData['NetworkEdge']=netList
    myData['HostEdge']=hostList
    myData['L2TrunkEdge']=l2List

    return myData








if __name__=='__main__':
    #dbServer='172.16.22.131'
    dbServer='192.168.20.118'
    #print("dbServer in 2.1.4 %s" % dbServer)
    #print("dbServer in 3.1 %s" % dbServerNew)
    myPath='C:/topo/'
    file1='topo1.xml'
    file2='topo2.xml'

    myData1=getXML(myPath+file1)
    myData2=getXML(myPath+file2)

    myOld=prepare(myData1)
    myNew=prepare(myData2)
    output(myOld['NetworkEdge'], myNew['NetworkEdge'], 'NetworkEdge')
    output(myOld['HostEdge'], myNew['HostEdge'], 'HostEdge')
    output(myOld['L2TrunkEdge'], myNew['L2TrunkEdge'], 'L2TrunkEdge')
    print 'Done'



