import XMLHelper
import xml.dom.minidom as dom
from xml.parsers.expat import ExpatError
from xml.dom.minidom import parse, parseString
import locateClassInstance
from pickClass import pickleClass
from classUtility import *
import TestConstant
import generalUtility

def getDatafromFolder(self, objType, myPath, skipList=[]):
    fileList=os.listdir(myPath)
    newFiles=[]
    for file in fileList:
        if '.xml' in file and file not in skipList:
            newFiles.append(file)
    data=[]
    for file in newFiles:
        name=file.split('.')[0]
        myFile=open(myPath+'/'+file, 'r')
        text=''
        myData=XMLHelper.unpickleXml(data[subkey], types, objType='list')

def getDatafromFile(fileName, objType):
    if '.xml' not in file:
        fileName+='.xml'
    data=[]
    try:
        doc=parse(fileName)
        if objType in TestConstant.objXmlWrap.keys():
            keyword=TestConstant.objXmlWrap[objType]
        else:
            keyword=generalUtility.getPlural(objType)
        nodes=doc.getElementsByTagName(keyword)
        data=XMLHelper.unpickle(nodes[0], type='list')
    except IOError, e:
        print 'Cannot open the file %s for parse. Error: %s' % (fileName, e)
    except ExpatError, e:
        print 'Error in parsing for file %s. Error: %s' % (fileName, e)
    indexData={}
    if data:
        if objType in TestConstant.objIndex.keys():
            index=TestConstant.objIndex[objType]
        else:
            index=TestConstant.objIndex['default']
        for item in data:
            indexData[index]=item

    return indexData
