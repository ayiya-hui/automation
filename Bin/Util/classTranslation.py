import ConfigConstants.TestConstant as TestConstant
import classUtility
from Models.ClassLocator import getClassObj

Mapping=TestConstant.populator_class_trans
Mapping_Keys=Mapping.keys()

class classTranslation:
    def __init__(self):
        pass

    def doTranslate(self, obj):
        newObj=self.__getNewObj(classUtility.getType(obj))
        newObj=self.__translate(obj, newObj)

        return newObj

    def __getNewObj(self, type):
        return getClassObj(self.__newType(type))

    def __translate(self, obj, newObj, index=False):
        mainMap=self.__getMap(classUtility.getType(obj))
        if mainMap:
            for attr in classUtility.getAttrList(obj):
                subObj=getattr(obj, attr)
                objType=classUtility.getType(subObj)
                if objType=='dict':
                    newObj=self.__transDict2Attr(attr, subObj, newObj, mainMap)
                elif objType=='list':
                    myObjList=self.__transList(subObj)
                    setattr(newObj, self.__newType(attr), myObjList)
                elif objType in ['unicode', 'str']:
                    if self.__isTranslable(attr, mainMap):
                        newKey=mainMap[attr]
                        if '->' in newKey:
                            exName, exAttr=newKey.split('->')
                            extraObj=getClassObj(exName)
                            setattr(extraObj, exName, subObj)
                        else:
                            setattr(newObj, newKey, subObj)
                else:
                    if self.__isTranslable(objType, Mapping):
                        newType=self.__newType(objType)
                        if newType:
                            subNewObj=self.__getNewObj(objType)
                            subNewObj=self.__translate(subObj, subNewObj)
                        else:
                            newObj=self.__translate(subObj, newObj)
        else:
            for attr in classUtility.getAttrList(obj):
                setattr(newObj, attr, getattr(obj, attr))

        return newObj

    def __transDict2Attr(self, attr, subObj, newObj, map):
        if attr=='attribute':
            if attr in map.keys():
                attrMap=map['attribute']
            else:
                attrMap=map
            for subKey in subObj.keys():
                if subKey in attrMap.keys():
                    newKey=attrMap[subKey]
                    if 'attribute#' in newKey:
                        attrKey=newKey.split('#')[-1]
                        newValue={}
                        newValue[attrKey]=subObj[subKey]
                        setattr(newObj, 'attribute', newValue)
                    else:
                        setattr(newObj, newKey, subObj[subKey])

        return newObj

    def __transList(self, subObj):
        myList=[]
        i=0
        for sub in subObj:
            if classUtility.getType(sub) not in classUtility.DATA_TYPES:
                subNewObj=self.__getNewObj(classUtility.getType(sub))
                subNewObj=self.__translate(sub, subNewObj, index=i)
                i+=1
                myList.append(subNewObj)

        return myList

    def __newType(self, type):
        newType=''
        for key in Mapping_Keys:
            if '-' in key and key.split('-')[0]==type:
                newType=key.split('-')[1]

        return newType

    def __getMap(self, type):
        newKey=''
        for key in Mapping_Keys:
            if '-' in key and key.split('-')[0]==type:
                newKey=key
            elif key==type:
                newKey=key

        return Mapping[newKey]

    def __isTranslable(self, key, mainMap):
        exist=False
        for mapKey in mainMap.keys():
            if key in mapKey:
                exist=True

        return exist




