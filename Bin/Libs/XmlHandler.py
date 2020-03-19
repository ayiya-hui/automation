import xml.dom.minidom
from xml.parsers.expat import ExpatError
import Util.classUtility as classUtility
import Util.generalUtility as generalUtility
from Models.ClassLocator import getClassObj
import os, sys
from ConfigConstants.TestConstant import xml_2_obj_special

class XmlHandler:
    """This class will handle the data translation between class objects and XML format."""
    def __init__(self):
        self.doc=xml.dom.minidom.Document()

    def XmlObjToFile(self, obj, path):
        """This method takes class object and produce a xml file."""
        output=open(path, 'w')
        data=self._ObjToXml(classUtility.getType(obj), obj)
        data.writexml(output)
        output.close()

    def XmlObjToString(self, obj):
        """This method takes clss object and produce a xml string."""
        node=self._ObjToXml(classUtility.getType(obj), obj)

        return node.toxml()

    def _ClassToXml(self, name, obj):
        node=self.doc.createElement(name)
        for attr in classUtility.getAttrList(obj):
            subval=getattr(obj, attr)
            if attr=='attribute':
                for attrVal in subval.keys():
                    node.setAttribute(attrVal, subval[attrVal])
            else:
                subnode=self._ObjToXml(attr, subval)
                node.appendChild(subnode)

        return node

    def _ListToXml(self, name, list):
        node=self.doc.createElement(name)
        for item in list:
            subnode=self._ObjToXml(classUtility.getType(item), item)
            node.appendChild(subnode)

        return node

    def _DictToXml(self, name, dict):
        node=self.doc.createElement(name)
        for item in dict.keys():
            subnode=self._ObjToXml(item, dict[item])
            node.appendChild(subnode)

        return node

    def _IntToXml(self, name, value):
        return self._ValueToXml(name, str(value))

    def _FloatToXml(self, name, value):
        return self._ValueToXml(name, str(value))

    def _NoneToXml(self, name, value):
        return self._ValueToXml(name, 'None')

    def _ValueToXml(self, name, value):
        node=self.doc.createElement(name)
        if value!='None':
            text=self.doc.createTextNode(value.encode('utf-8'))
            node.appendChild(text)

        return node


    toXmlToken={'NoneType':_NoneToXml, 'unicode':_ValueToXml, 'str':_ValueToXml, 'int':_IntToXml, 'float':_FloatToXml, 'dict':_DictToXml, 'list':_ListToXml, 'default':_ClassToXml,}

    def _ObjToXml(self, name, obj):
        type=classUtility.getType(obj)
        if type not in self.toXmlToken.keys():
            type='default'
        return self.toXmlToken[type](self, name, obj)

    def XmlStringToObj(self, xmlString, keyword=None):
        """This method takes a xml string and return a class object."""
        doc=xml.dom.minidom.parseString(xmlString.encode('utf-8', 'xmlcharrefreplace'))
        if keyword:
            return self._XmlToObj(doc, wrapTag=keyword)
        else:
            return self._XmlToObj(self._getElementChilds(doc)[0][1])

    def XmlFileToObj(self, fileName, keyword=None):
        """This method takes a filename and return a class object."""
        try:
            doc=xml.dom.minidom.parse(fileName)
        except ExpatError as e:
            print 'XML grammar error: %s has %s' % (fileName, e)
            sys.exit()

        return self._XmlToObj(self._getElementChilds(doc)[0][1], wrapTag=keyword)

    def _XmlToObj(self, node, wrapTag=None, filter=None):
        if wrapTag:
            subnode=''
            nodes=node.getElementsByTagName(wrapTag)
            if not nodes:
                return None
            else:
                subnode=nodes[0]
                nodelist=self._getElementChilds(subnode)
                if nodelist:
                    if nodelist[0][0]==nodelist[-1][0]:
                        return self._XmlToObjList(nodelist, condition=filter)
                    else:
                        return self._XmlToObj(subnode)
                elif subnode.childNodes:
                    return subnode.childNodes[0].nodeValue.strip()
                else:
                    return None
        else:
            if hasattr(node, 'tagName'):
                tagName=node.tagName
            else:
                tagName=node.nodeName
            obj=getClassObj(tagName)
            objAttrs=classUtility.getAttrList(obj)
            if 'attribute' in objAttrs:
                self._setAttributes(node, obj)
            if 'namedValues' in objAttrs:
                obj=self._setNamedValues(node, obj)
            if tagName in xml_2_obj_special.keys():
                attr=node.attributes.getNamedItem(xml_2_obj_special[tagName]['attr']).nodeValue
                setattr(obj, xml_2_obj_special[tagName]['attr'], attr)
                value=''
                if len(node.childNodes):
                    value=node.childNodes[0].nodeValue.strip()
                    setattr(obj, xml_2_obj_special[tagName]['text'], value)
            else:
                elementChilds=self._getElementChilds(node)
                for name, element in elementChilds:
                    if name in objAttrs:
                        my_type=classUtility.getType(getattr(obj, name))
                        if my_type=='NoneType':
                            if len(element.childNodes):
                                value=element.childNodes[0].nodeValue
                                if value:
                                    setattr(obj, name, value.strip())
                        elif my_type=='list':
                            li=getattr(obj, name)
                            subE=self._getElementChilds(element)
                            subENames=[na[0] for na in subE]
                            subObj=''
                            if subENames:
                                if generalUtility.isWrap(subENames[0], name):
                                    if subE:
                                        subObj=self._XmlToObjList(subE)
                                else:
                                    if subE:
                                        subObj=self._XmlToObj(element)
                            if subObj:
                                if classUtility.getType(subObj)=='list':
                                    li.extend(subObj)
                                else:
                                    li.append(subObj)
                            setattr(obj, name, li)
                        else:
                            subObj=self._XmlToObj(element)
                            setattr(obj, name, subObj)

        return obj

    def _XmlToObjList(self, nodelist, condition=None):
        li=[]
        for name, element in nodelist:
            if condition:
                if condition.name==name:
                    if condition.value==element.attributes.getNamedItem(condition.param).nodeValue.strip():
                        subobj=self._XmlToObj(element)
                        li.append(subobj)
            else:
                subobj=self._XmlToObj(element)
                li.append(subobj)

        return li

    def _setAttributes(self, element, obj):
        map={}
        for key in obj.attribute.keys():
            if key in element.attributes.keys():
                map[key]=element.attributes.getNamedItem(key).nodeValue.strip()

        return setattr(obj, 'attribute', map)

    def _setNamedValues(self, element, obj):
        map={}
        for key in obj.attribute.keys():
            if key in element.attributes.keys():
                map[key]=element.attributes.getNamedItem(key).nodeValue.strip()
        setattr(obj, 'attribute', map)
        li=[]
        elementChilds=self._getElementChilds(element)
        for name, myElement in elementChilds:
            if name=='value':
                li.append(myElement.childNodes[0].nodeValue)
        setattr(obj, 'namedValues', li)

        return obj

    def _getElementChilds(self, node):
        return [(no.nodeName, no) for no in node.childNodes if no.nodeType!=no.TEXT_NODE and no.nodeName!='#comment']



