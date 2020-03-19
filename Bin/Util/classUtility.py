def getType(obj):

    return obj.__class__.__name__

def getAttrList(obj):
    nameList=[]
    for name in [name for name in dir(obj) if not name.startswith("__")]:
        subobj=getattr(obj, name)
        if not hasattr(subobj, '__class__'):
            nameList.append(name)
        elif subobj.__class__.__name__!='instancemethod':
            nameList.append(name)

    return nameList

def getMethodList(obj):
    return [method for method in dir(obj) if not name.startswith("__") and callable(getattr(obj, method))]

def getAllAttrList(obj):
    return [name for name in dir(obj) if not name.startswith("__")]

def getIndexValue(obj, indexKey):
    indexValue=''
    if getType(indexKey)=='list':
        valueList=[]
        for key in indexKey:
            if 'Attribute-' in key:
                valueList.append(obj.attribute[key.split('-')[-1]])
            else:
                valueList.append(getattr(obj, key))
        indexValue='-'.join(valueList)
    else:
        if 'Attribute-' in indexKey:
            indexValue=obj.attribute[indexKey.split('-')[-1]]
        else:
            indexValue=getattr(obj, indexKey)

    return indexValue

def hashToClass(hash, obj):
    for item in getAttrList(obj):
        if item in hash.keys():
            setattr(obj, item, hash[item])

    return obj

def removeIndex(hash={}):
    myList=[]
    for key in hash.keys():
        myList.append(hash[key])

    return myList

def addIndex(index, list=[]):
    hash={}
    for item in list:
        value=getattr(item, index)
        hash[value]=item

    return hash

def compareList(list1, list2, mapKey, errorMsg, skip):
    map1={}
    map2={}
    for item in list1:
        value=getattr(item, mapKey)
        map1[value]=item
    for item in list2:
        value=getattr(item, mapKey)
        map2[value]=item
    oriAttrs=getAttrList(list1[0])
    for key in map1.keys():
        if key in map2.keys():
            errorMsg=compare(map1[key], map2[key], None, errorMsg, skip)
        else:
            errorMsg+='EXECT: %s from List, RETURN: Only have %s\n' % (key, map2.keys())

    return errorMsg

def compareDict(dict1, dict2, errorMsg, skip):
    for key in dict1.keys():
        doSkip=False
        if skip and key in skip:
            doSkip=True
        if not doSkip:
            if getType(dict2)=='dict':
                if key in dict2.keys():
                    if str(dict1[key]).lower()!=str(dict2[key]).lower():
                        errorMsg+='%s: EXPECT: %s, RETURN: %s\n' % (key, dict1[key], dict2[key])
                else:
                    errorMsg+='%s: EXPECT: %s, RETURN: None\n' % (key, dict1[key])
            else:
                errorMsg+='%s: EXPECT: %s, RETURN: None\n' % (key, dict1[key])

    return errorMsg

def compare(class1, class2, listKey, errorMsg, skip):
    oriAttrs=getAttrList(class1)
    for attr in oriAttrs:
        oriValue=getattr(class1, attr)
        if hasattr(class2, attr):
            retValue=getattr(class2, attr)
        else:
            retValue=''
        if listKey:
            myVal=listKey
        else:
            myVal=None
        if retValue:
            if getType(oriValue)=='list':
                errorMsg=compareList(oriValue, retValue, myVal, errorMsg, skip)
            elif getType(oriValue)=='dict':
                errorMsg=compareDict(oriValue, retValue, errorMsg, skip)
            elif getType(oriValue) in DATA_TYPES:
                doSkip=False
                if skip and attr in skip:
                    doSkip=True
                if not doSkip:
                    if oriValue.lower()!=retValue.lower():
                        if oriValue.strip()!=retValue.strip():
                            if oriValue.replace(' ', '')!=retValue.replace(' ', ''):
                                errorMsg+='%s: EXPECT: %s, RETURN %s\n' % (attr, oriValue, retValue)
            else:
                errorMsg=compare(oriValue, retValue, None, errorMsg, skip)
        else:
            if oriValue:
                errorMsg+='%s: EXPECT: %s, RETURN: None\n' % (attr, oriValue.strip())

    return errorMsg

DATA_TYPES=['int', 'long', 'unicode', 'float', 'bool', 'list', 'dict', 'str', 'double']
