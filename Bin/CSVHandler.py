import os, os.path
import eventtypeDataClass
import csv
import classToHash
import locateClassInstance
import math
import classUtility
import TestConstant

myConstant=TestConstant.populatorConfig()

def getDatafromFolder(folder):
    fileList=os.listdir(folder)
    indexData={}
    for file in fileList:
        if file.split('.')[-1]!='csv':
            fileList.remove(file)
    for file in fileList:
        data=getDatafromFile(folder+'/'+file, type=folder.split('/')[-1])
        if data:
            for key in data.keys():
                indexData[key]=data[key]

    return indexData

def getDatafromFile(fileName, type=False):
    myFile=open(fileName, 'r')
    myReader=csv.reader(myFile, delimiter=',')
    data=formatData(myReader, fileName, type=type)
    myFile.close()

    return data

def formatData(reader, fileName, type=False):
    formattedData={}
    specialKey=''
    if type:
        type, objType=retriveType(fileName, type=type)
    else:
        type, objType=retriveType(fileName)
    nameMap=myConstant.data_structure[objType]
    for item in reader:
        if metCondition(item):
            map={}
            for numkey in nameMap.keys():
                if numkey > (len(item)-1):
                    map[nameMap[numkey]]=''
                else:
                    nums=nameMap[numkey]
                    if classUtility.getType(nums)=='list':
                        for subKey in nums:
                            map[subKey]=item[numkey].strip()
                    else:
                        map[nums]=item[numkey].strip()

            myObj=locateClassInstance.getClassInstance(objType)
            for key in map.keys():
                if 'Attribute-' in key:
                    myObj.attribute[key.split('-')[-1].strip()]=map[key].strip()
                else:
                    if key in myConstant.special_keys:
                        value=specialFormat(key, map[key])
                    else:
                        value=map[key]
                    setattr(myObj, key, value)
            if objType=='group':
                myObj.attribute['type']=myConstant.group_tasks[type]
            elif objType=='eventAttributeType':
                myList=item[4:9]
                myList.extend(item[10:14])
                myList.extend(item[15:22])
                myObj.categories=getCategories(myList)
            elif objType=='deviceType':
                myObj.sysDefined='true'
            elif objType=='eventCode':
                if '$' in myObj.code:
                    specialKey=myObj.code.split('$')[-1]
                myObj.eventAttributeType=specialKey
                map['eventAttributeType']=specialKey
            keys=getKeys(objType)
            values=[]
            if classUtility.getType(keys)=='list':
                for key in keys:
                    values.append(map[key])
                value='-'.join(values)
            else:
                value=map[keys]
            formattedData[value]=myObj

    if formattedData:
        if objType in myConstant.special_package:
            finalData=specialProcess(objType, formattedData)
        else:
            finalData=formattedData
    else:
        print '%s has empty file.' % fileName.split('/')[-1]
        finalData=''

    return finalData

def specialProcess(type, data):
    finaldata={}
    if type=='parser':
        numbers=[]
        for key in data.keys():
             numbers.append(int(data[key].priority))
             data[key].name=data[key].name.split('.')[0]
             finaldata[key.split('.')[0]]=data[key]
        numbers.sort()
        sortNums={}
        for i in range(len(numbers)):
            sortNums[str(numbers[i])]=str(i+1)
        for key in finaldata.keys():
            newNum=finaldata[key].priority
            finaldata[key].priority=sortNums[newNum]
    if type in ['eventType', 'deviceEventAttribute']:
        valKey=myConstant.device_type_keys[type]
        deviceTypeKey=getattr(data['Model'], valKey)+'-'+getattr(data['Vendor'], valKey)
        for key in ['Model', 'Vendor', 'Version']:
            del data[key]
        for item in data.keys():
            if type=='eventType':
                data[item].sysDefined='true'
                data[item].systemType='false'
            data[item].deviceType=deviceTypeKey
            finaldata[item]=data[item]
    if type=='eventCode':
        for key in data.keys():
            if "-$" in key or not key.split('-')[-1]:
                del data[key]
        finaldata=data

    return finaldata

def retriveType(fileName, type=False):
    if not type:
        file=fileName.split('/')[-1]
        type=file.split('.')[0]
    transType=''
    if type in myConstant.group_tasks.keys():
        transType='group'
    elif type in myConstant.task_trans.keys():
        transType=myConstant.task_trans[type]
    else:
        transType=type

    return type, transType

def specialFormat(key, value):
    newValue=value
    if key=='valueType':
        newValue=str(myConstant.value_type[value.strip().lower()])
    elif key in ['usedByRbac', 'deprecated', 'eventParsed']:
        if value=='1':
            newValue='true'
        else:
            newValue='false'
    elif key=='type':
        if value=='OS':
            newValue=''
    elif key=='priority':
        if not value:
            value='0'

    return newValue

def getCategories(myList):
    if myList[-4] or myList[-5] or myList[-6]:
        myList.append(1)
    else:
        myList.append(0)
    value=0
    for i in range(len(myList)):
        if not myList[i]:
            myList[i]='0'
        value+=int(myList[i])*int(math.pow(2, i))

    return str(value)

def getKeys(type):
    if type in myConstant.data_index.keys():
        key=myConstant.data_index[type]
    else:
        key=myConstant.default_data_index_key

    return key

def metCondition(item):
    cond=True
    if not len(item):
        cond=False
    elif not ''.join(item):
        cond=False
    elif '#' in item[0]:
        cond=False

    return cond


if __name__=='__main__':
    file="../TestData/DbPopulator/data-definition/vulnerabilities.csv"
    data=getDatafromFile(file, type='vulnerability')

    print 'Done'

