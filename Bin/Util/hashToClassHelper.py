import classUtility
from ConfigConstants.TestConstant import create_device_wrap
from Models.ClassLocator import getClassObj

def hashToClass(hash, obj, objModule=False):
    attrKeys=hash.keys()
    for key in attrKeys:
        subType=classUtility.getType(hash[key])
        if subType=='list':
            objList=listToClass(key, hash[key], objModule)
            setattr(obj, key, objList)
        elif subType=='dict':
            if key=='attribute':
                setattr(obj, 'attribute', hash[key])
            else:
                subObj=hashToClass(hash[key], getClassObj(key, module=objModule))
                setattr(obj, key, subObj)
        elif subType=='str':
            setattr(obj, key, hash[key])

    return obj

def listToClass(key, list, objModule):
    objList=[]
    if key in create_device_wrap:
        objName=create_device_wrap[key]
    else:
        objName=key[0:-1]
    for item in list:
        if classUtility.getType(item)=='dict':
            subObj=getClassObj(objName, module=objModule)
            subObj=hashToClass(item, subObj)
            objList.append(subObj)

    return objList

