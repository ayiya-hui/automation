def getType(obj):
    p=str(obj.__class__)
    p=p.replace("<", "")
    p=p.replace(">", "")
    p=p.replace("'", "")
    if 'class' in p:
        p=p.replace("class", "")
    if 'type' in p:
        p=p.replace("type", "")
    p=p.split(".")[-1]

    return p.strip()

def getAttrList(obj):
    nameList=[]
    for name in [name for name in dir(obj) if not name.startswith("__")]:
        subobj=getattr(obj, name)
        if not isClass(subobj):
            nameList.append(name)

    return nameList

def getAllAttrList(obj):
    return [name for name in dir(obj) if not name.startswith("__")]

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

def compareList(list1, list2, mapKey, skip=False):
    map1={}
    map2={}
    for item in list1:
        value=getattr(item, mapKey)
        if not value:
            print value
        map1[value]=item
    for item in list2:
        value=getattr(item, mapKey)
        map2[value]=item
    oriAttrs=getAttrList(list1[0])
    for key in map1.keys():
        compare(map1[key], map2[key], None, skip=skip)

def compareDict(dict1, dict2, skip=False):
    for key in dict1.keys():
        doSkip=False
        if skip and key in skip:
            doSkip=True
        if not doSkip:
            if getType(dict2)=='dict':
                if key in dict2.keys():
                    if str(dict1[key]).lower()!=str(dict2[key]).lower():
                        print 'attr %s not matched: expect %s, actual %s' % (key, dict1[key], dict2[key])
                else:
                    print 'attr %s not present in actual data.' % key
            else:
                print 'attr %s not matched: expect %s, actual None' % (key, dict1[key])

def compare(class1, class2, listKey, skip=False):
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
                compareList(oriValue, retValue, myVal, skip=skip)
            elif getType(oriValue)=='dict':
                compareDict(oriValue, retValue, skip=skip)
            elif getType(oriValue) in DATA_TYPES:
                doSkip=False
                if skip and attr in skip:
                    doSkip=True
                if not doSkip:
                    if oriValue.lower()!=retValue.lower():
                        if oriValue.strip()!=retValue.strip():
                            if oriValue.replace(' ', '')!=retValue.replace(' ', ''):
                                print 'attr %s values not match: expect %s, actual %s' % (attr, oriValue, retValue)
            else:
                compare(oriValue, retValue, None)
        else:
            if oriValue:
                print '%s: %s in expect, but not exist in actual return.' % (attr, oriValue)

isClass=lambda o: hasattr(o, "__call__")
DATA_TYPES=['int', 'bool', 'list', 'dict', 'string', 'double', 'unicode']
