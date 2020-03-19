import xml.dom.minidom as dom
from xml.parsers.expat import ExpatError
from xml.dom.minidom import parse, parseString
import locateClassInstance
from pickClass import pickleClass
from classUtility import *

#Pickle
def _pickleDictItems(root, node, fabric):
    for key, value in root.items():
        node.setAttribute(key, value)

def _pickleListItems(root, node, fabric):
    for idx, obj in enumerate(root):
        tempnode=pickle(obj, fabric, getType(obj))
        node.appendChild(tempnode)

_pickleTupleItems=_pickleListItems

def classToXml(object, type):
    objList=[]
    objList.append(object)

    return classListToXml(objList, type)

def classListToXml(objList, type):
    node=pickle(root=objList, fabric=dom.Document(), elementName=type)

    return node

def pickle(root, fabric, elementName):
    if elementName=='dict':
        elementName=PARAM
    node=fabric.createElement(elementName)
    if isinstance(root, pickleClass):
        node=_pickleObject(node, root, fabric, elementName)
    elif isinstance(root, dict):
        _pickleDictItems(root, node, fabric)
    elif isinstance(root, list):
        _pickleListItems(root, node, fabric)
    elif isinstance(root, tuple):
        _pickleTupleItems(root, node, fabric)
    else:
        node.appendChild(fabric.createTextNode(str(root)))

    return node

def _pickleObject(node, root, fabric, elementName):
    attributesToPickle=getAttrList(root)
    for name in attributesToPickle:
        if name=='attribute':
            for key in root.attribute.keys():
                node.attributes[key]=root.attribute[key]
        elif name in SPECIAL.values():
            obj=getattr(root, name)
            _pickleListItems(obj, node, fabric)
        else:
            obj=getattr(root, name)
            node.appendChild(pickle(obj, fabric, name))

    return node


def _getElementChilds(node):
    return [(no.nodeName, no) for no in node.childNodes if no.nodeType!=no.TEXT_NODE and no.nodeName!='#comment']

def _getText(nodeList):
    rc=""
    for node in nodeList:
        if node.nodeType==node.TEXT_NODE:
            rc=rc+node.data
    return rc.strip()

def unpickleXml(inXml, keyword, objType=False):
    doc=parseString(inXml.encode('ascii', 'xmlcharrefreplace'))
    nodes=doc.getElementsByTagName(keyword)
    if len(nodes):
        if objType:
            return unpickle(_getElementChilds(nodes[0]), type=objType)
        else:
            return unpickle(nodes[0])
    else:
        return []

def unpickleFile(fileName, keyword=False, objType=False):
    try:
        doc=parse(fileName)
        if not keyword:
            return unpickel(doc.childNodes[0], type=objType)
        else:
            nodes=doc.getElementsByTagName(keyword)
            if len(nodes):
                if objType:
                    return unpickle(_getElementChilds(nodes[0]), type=objType)
                else:
                    return unpickle(nodes[0])
    except IOError, e:
        print 'Cannot open the file %s for parse. Error: %s' % (fileName, e)
        exit(1)
    except ExpatError, e:
        print 'Error in parsing for file %s. Error: %s' % (fileName, e)
        exit(1)


def unpickle(node, type=False, filter=False):
    if type:
        typeName=type
    else:
        typeName=node.tagName

    if typeName=="list":
        return _unpickleList(node)
    elif typeName=="dict":
        return _unpickleDict(node)
    elif typeName in LIST_TAG:
        return _unpickleList(_getElementChilds(node))
    else:
        obj=locateClassInstance.getClassInstance(typeName)
        nameList=getAttrList(obj)
        if 'attribute' in nameList:
            name='attribute'
            map={}
            keys=obj.attribute.keys()
            keyList=node.attributes.keys()
            for item in keys:
                if item in keyList:
                    value=node.attributes.getNamedItem(item).nodeValue
                    map[item]=str(value).strip()
                setattr(obj, name, map)
            nameList.remove('attribute')
        if getType(obj) == EVENT_CASE:
            obj=_unpickleEvent(obj, node, nameList)
        elif getType(obj) == ENTITY_CASE:
            obj=_unpickleEntity(obj, node, nameList[-1])
        elif getType(obj) == PROPERTY_CASE:
            obj=_unpickleProperty(obj, node, nameList)
        elif getType(obj) == PARSER_CASE:
            obj=_unpickleParser(obj, node, nameList)
        else:
            childs=_getElementChilds(node)
            for name, element in childs:
                if name in nameList or name.title() in nameList:
                    subs=_getElementChilds(element)
                    if name in SPECIAL_HANDLING:
                        if subs:
                            values=__specialHandling(name, obj, element)
                            setattr(obj, name, values)
                    elif not element.attributes and (len(subs)==0 or subs[0][0]=="#cdata-section"):
                        if len(element.childNodes):
                            value=element.childNodes[0].nodeValue
                            setattr(obj, name, value)
                    elif element.attributes:
                        subobj=unpickle(element)
                        if _isSpecial(typeName, name):
                            myList=getattr(obj, name)
                            myList.append(subobj)
                            setattr(obj, name, myList)
                        else:
                            setattr(obj, name, subobj)
                    else:
                        subobj=unpickle(element)
                        setattr(obj, name, subobj)

    return obj



class XMLUnpicklingException(Exception): pass

def _unpickleList(nodelist):
    li=[]
    for name, element in nodelist:
        if 'Case' in name:
            if element.attributes.getNamedItem('run').nodeValue.strip()=="True":
                subobj=unpickle(element)
                li.append(subobj)
        else:

            subobj=unpickle(element)
            li.append(subobj)

    return li

def _unpickleTuple(node):
    return tuple(_unpickleList(node))

def _unpickleDict(node):
    dd=dict()
    childList=_getElementChilds(node)
    for name, element in childList:
        text=element.childNodes[0].data
        dd[name]=text
    return dd

def _unpickleEvent(obj, element, nameList):
    myName=None
    myVal=None
    for name in nameList:
        if name=='name':
            myName=element.attributes.getNamedItem(name).nodeValue
            setattr(obj, name, myName)
            keName=myName
        else:
            if len(element.childNodes):
                myVal=element.childNodes[0].nodeValue.strip()
                setattr(obj, name, myVal)
    if myVal:
         setattr(obj, 'name', myName)
         setattr(obj, 'value', myVal)

    return obj

def _unpickleEntity(obj, element, name):
    values=[]
    childNodes=_getElementChilds(element)
    for subname, subelement in childNodes:
        values.append(subelement.childNodes[0].nodeValue.strip())
    setattr(obj, name, values)

    return obj

def _unpickleProperty(obj, element, name):
    childNodes=_getElementChilds(element)
    properties=[]
    for subName, subelement in childNodes:
        if subName=='property':
            subobj=unpickle(subelement)
            properties.append(subobj)
        else:
            if len(subelement.childNodes):
                value=subelement.childNodes[0].data.strip()
                setattr(obj, subName, value)
    setattr(obj, 'properties', properties)

    return obj

def _unpickleParser(obj, element, name):
    for key in name:
        setattr(obj, key, element.attributes.getNamedItem(key).nodeValue)

    return obj

def _isSpecial(parent, child):
    if parent in SPECIAL.keys() and SPECIAL[parent]==child:
        return True
    else:
        return False

def __specialHandling(name, obj, element):
    subobj=unpickle(element)
    values=getattr(obj, name)
    values.append(subobj)

    return values

SPECIAL={'PatternClause':'SubPattern', 'topoEdge':'topoNode'}
LIST_TAG=['testcases','actions','events', 'conditions', 'attributes', 'collectors', 'CPUs', 'Disks', 'DiskIOs', 'Swaps', 'approvedDevices']
EVENT_CASE='attribute'
ENTITY_CASE='entityValue'
PROPERTY_CASE='deviceProperties'
PARSER_CASE='parser'
PARAM='param'
SPECIAL_HANDLING=['eventFilters']
