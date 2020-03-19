import cmdbDataClass
import dataDefinitionDataClass
import testConfigs
import incidentTestClass
import deviceModelDataClass
import autoTestResultClass
import constriantClass
import dbUpgradeDataClass
import notificationDataClass
from Util.classUtility import getAttrList

token={'cmdb':cmdbDataClass,
       'definition':dataDefinitionDataClass,
       'test':testConfigs,
       'device':deviceModelDataClass,
       'incident':incidentTestClass,
       'autoTest':autoTestResultClass,
       'constriant':constriantClass,
       'dbupgrade':dbUpgradeDataClass,
       'notification':notificationDataClass,
       }

def getClassObj(type, module=False):
    """This method will return a class instance object with name specified in type."""
    if module:
        return getattr(token[module], type)()
    else:
        keys=[key for key in token.keys() if key !='device']
        for key in keys:
            if type in getAttrList(token[key]):
                return getattr(token[key], type)()



