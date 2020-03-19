import csv, os
from Models.ClassLocator import getClassObj
import Util.classUtility as classUtility
import Util.testUtility as testUtility
from ConfigConstants.TestConstant import csv_key_attrs, csv_special_handling, csv_device_info, csv_class_attrs

def getDatafromFolder(type, path):
    """This method will read data from a folder that contains CSV files."""
    orderAttrs=csv_class_attrs[type]
    files=os.listdir(path)
    keyAttrs=''
    if type in csv_key_attrs:
        keyAttrs=csv_key_attrs[type]
    objData={}
    fileData={}
    for file in files:
        if '.csv' in file:
            fileData=getDataFromFile(type, path+'/'+file, keyAttrs, orderAttrs)
        for key in fileData.keys():
            objData[key]=fileData[key]

    return objData

def getDataFromFile(type, path, keyAttrs, orderAttrs, asCsv=True):
    """This method will read data from a CSV file."""
    if asCsv:
        if '.csv' not in path:
            path+='.csv'
    objData={}
    reader=csv.DictReader(open(path), fieldnames=orderAttrs, restkey='Extra', restval='Miss')
    keyword=[]
    for line in reader:
        if not orderAttrs:
            orderAttrs=line.keys()
            if 'Extra' in orderAttrs:
                orderAttrs.remove('Extra')
            if 'Miss' in orderAttrs:
                orderAttrs.remove('Miss')
        if 'Extra' in line.keys():
            line[orderAttrs[-1]]+=', '+','.join(line['Extra'])
            del line['Extra']
        if __metCondition(line):
            if '$' in line[orderAttrs[0]]:
                keyword=[]
                keyword.append(line[orderAttrs[0]].split('$')[-1])
            elif line[orderAttrs[0]] in csv_device_info:
                keyword.append(line[orderAttrs[1]])
            else:
                obj=getClassObj(type)
                for key in line.keys():
                    if key in classUtility.getAttrList(obj):
                        setattr(obj, key, line[key])
                map={}
                if keyAttrs and keyword:
                    if classUtility.getType(keyAttrs)=='list':
                        map=testUtility.listToHash(keyAttrs, keyword)
                    elif len(keyword)>1:
                        keyVal='-'.join(keyword)
                        map[keyAttrs]=keyVal
                    else:
                        map[keyAttrs]=keyword[0]
                if map:
                    for newKey in map.keys():
                        setattr(obj, newKey, map[newKey])
                indexKey=testUtility.getKey(type, file=True)
                indexValue=classUtility.getIndexValue(obj, indexKey)
                objData[indexValue]=obj

    return objData


def __eventAttrDescSpecial(obj, addAttrs):
    return obj


token={'eventAttrDesc':__eventAttrDescSpecial}

def __special_handling(type, data):
    addAttrs=[]
    if type in csv_add_attrs:
        addAttrs=csv_add_attrs[type].split(',')
    objData={}
    special_key=''
    for obj in data:
        print line

    return objData

def __metCondition(line):
    cond=True
    values=line.values()
    if None in values:
        values.remove(None)
    valueString=''.join(values)
    if not valueString or '#' in valueString:
        cond=False


    return cond






