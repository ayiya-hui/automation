import XMLHelper
from classUtility import *

def classToHash(obj, param=False):
    myData={}
    nameList=getAllAttrList(obj)
    for name in nameList:
        subobj=getattr(obj, name)
        if not isClass(subobj):
            if getType(subobj) not in ['NoneType', 'list', 'dict']:
                myData[name]=subobj
            elif XMLHelper.getType(subobj)=='dict':
                myData[name]=subobj
            elif XMLHelper.getType(subobj)=='list':
                subData=[]
                subData=listToHash(subobj)
                myData[name]=subData
            else:
                myData[name]=''
        else:
            if not param:
                subData={}
                subData=classToHash(subobj)
                myData[name]=subData

    return myData

def listToHash(list):
    listData=[]
    for obj in list:
        myData=classToHash(obj)
        listData.append(myData)

    return listData




