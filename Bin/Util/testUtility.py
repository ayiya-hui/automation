import ConfigConstants.TestConstant as TestConstant
import classUtility

xml_escapes={'"':'&quot;', "'":'&apos;', '<':'&lt;', '>':'&gt;', '&':'&amp;'}

def getKey(type, file=False):
    if file:
        keyMap=TestConstant.file_obj_index
    else:
        keyMap=TestConstant.obj_index
    if type in keyMap.keys():
        key=keyMap[type]
    else:
        key=keyMap['default']

    return key

def getListKey(type):
    key=''
    if type in TestConstant.list_keys.keys():
        key=TestConstant.list_keys[type]

    return key

def rekeyData(keyName, data):
    newData={}
    for key in data.keys():
        if 'Attribute-' in keyName:
            newKey=data[key].attribute[keyName.split('-')[-1]]
        else:
            newKey=getattr(data[key], keyName)
        newData[newKey]=data[key]

    return newData

def rekeyKey(keyName, data):
    newData={}
    for key in data.keys():
        if classUtility.getType(data[key])=='list':
            for sub in data[key]:
                if 'Attribute-' in keyName:
                    newKey=sub.attribute[keyName.split('-')[-1]]
                else:
                    newKey=getattr(sub, keyName)
                newData[newKey]=key
        else:
            if 'Attribute-' in keyName:
                newKey=data[key].attribute[keyName.split('-')[-1]]
            else:
                newKey=getattr(data[key], keyName)
            newData[newKey]=key

    return newData

def listToHash(list1, list2):
    map={}
    for i in range(len(list1)):
        map[list1[i]]=list2[i]

    return map

def processList(list1, list2):
    missKey=[]
    extraKey=[]
    commKey=[]
    for key in list1:
        if key in list2:
            commKey.append(key)
        else:
            missKey.append(key)
    for key in list2:
        if key not in commKey:
            extraKey.append(key)
    if None in missKey:
        missKey.remove(None)
    if None in extraKey:
        extraKey.remove(None)
    if None in commKey:
        commKey.remove(None)

    return missKey, extraKey, commKey

def processClassAttrs(class1, class2):
    return processList(classUtility.getAttrList(class1), classUtility.getAttrList(class2))

def processDictKeys(dict1, dict2):
    return processList(dict1.keys(), dict2.keys())

def changeString(value, map):
    for key in map.keys():
        value=value.replace(key, map[key])

    return value

def xmlEscape(text):
    for item in xml_escapes.keys():
        text=text.replace(item, xml_escapes[item])

    return text

