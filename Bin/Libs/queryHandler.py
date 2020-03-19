from XmlHandler import XmlHandler
from appHandler import appHandler
import Util.hashToClassHelper as hashToClassHelper
from ConfigConstants.queryTemplate import query_xml
from ConfigConstants.TestConstant import query_xml_create_delete_attrs, obj_index
from Models.ClassLocator import getClassObj
import Util.classUtility as classUtility
from string import Template

class queryHandler:
    """This class will handle Accelops query utility. It will create a query XML then
    using REST API to get query data."""
    def __init__(self, appServer, user=False, password=False):
        self.appHandler=appHandler(appServer, user=user, password=password)

    def getQuery(self, params):
        """This method will get indexed dictinary of query objects."""
        indexData={}
        inXml=self.createQueryXml(params)
        self.appHandler.getQuery(inXml)
        debugInfo=self.appHandler.queryDebug
        if self.appHandler.queryResult:
            for data in self.appHandler.queryXml:
                objList=XmlHandler().XmlStringToObj(data, keyword='events')
                if objList:
                    for subData in objList:
                        attrList=subData.attributes
                        attrMap={}
                        for attr in subData.attributes:
                            attrMap[attr.name]=attr.value
                        delattr(subData, 'attributes')
                        setattr(subData, 'attributes', attrMap)
                        indexValue=classUtility.getIndexValue(subData, obj_index['event'])
                        if subData.attributes.has_key('incidentRptIp'):
                            addKey=subData.attributes['incidentRptIp']
                        else:
                            addKey=subData.attributes['reptDevIpAddr']
                        if indexValue is not None:
                            if addKey is not None:
                                indexValue+='@'+addKey
                        else:
                            indexValue='No EventType(not unknown_type)'
                        if indexValue in indexData.keys():
                            oldValue=indexData[indexValue]
                            oldValue.append(subData)
                            indexData[indexValue]=oldValue
                        else:
                            newValue=[]
                            newValue.append(subData)
                            indexData[indexValue]=newValue

        return indexData, debugInfo

    def createQueryXml(self, params):
        """This method will create a query XML."""
        myTemp=Template(query_xml)
        if 'minute' not in params.keys():
            params['minute']='60'
        inXml=myTemp.substitute(params)

        return inXml



