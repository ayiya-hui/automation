import deviceDataClass
import XMLHelper
import classUtility
import xml.dom.minidom as dom

def classToXml(type, hash):
    objList=[]
    obj=_typeToClassObj(type)
    for name in classUtility.getAttrList(obj):
        if name in hash.keys():
            setattr(obj, name, hash[name])
    objList.append(obj)
    node=XMLHelper.pickle(root=objList, fabric=dom.Document(), elementName=type)
    myXml=node.toxml()

    return myXml

def _typeToClassObj(type):
    myObj=''
    if type=='ipAccessMappings':
        myObj=deviceDataClass.ipAccessMapping()
    elif type=='discoveryIpRanges':
        myObj=deviceDataClass.discoveryIpRange()

    return myObj

