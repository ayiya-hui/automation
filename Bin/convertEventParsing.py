from Libs.XmlHandler import XmlHandler
import os

rootPath='../DataFiles/eventParsing'
folders=os.listdir(rootPath)
target='../TestData/EventParsing/'
targetFile='eventParsingData.csv'
objList=[]
for file in folders:
    if 'EventTest.xml' in file:
        path=rootPath+'/'+file
        myFile=open(path)
        data=myFile.read()
        myFile.close()
        myObj=XmlHandler().XmlStringToObj(data)
        objList.append(myObj)
        name=myObj.name.split('Event')[0]
        if not os.path.exists(target+name):
            os.makedirs(target+name)


allData=[]

allData.append('eventType,name,module,reptDevIpAddr,key,method')

for subObj in objList:
    allTypes=[]
    detailData={}
    dName=subObj.name.split('Event')[0]
    for sub in subObj.testcases:
        if sub.attribute['run']=='True':
            myList=[]
            myList.append(sub.eventType)
            myList.append(sub.name)
            myList.append(dName)
            myList.append(sub.reporter)
            if sub.key:
                myKey=sub.key
            else:
                myKey=''
            myList.append(myKey)
            myList.append(subObj.method)
            mySt=','.join(myList)
            allData.append(mySt)

            if sub.eventType not in allTypes:
                allTypes.append(sub.eventType)
                detail=[]
                detail.append('[reptDevIpAddr(key)]')
                newSt=sub.reporter
                if myKey:
                    newSt+=' ('+myKey+')'
                detail.append(newSt+'')
                detail.append('[eventMsg]')
                detail.append(sub.parseEvent+'')
                detail.append('[params]')
                for item in sub.parameters.split(','):
                    detail.append(item+'')
                detailData[sub.eventType]=detail
            else:
                detail=detailData[sub.eventType]
                detail.append('[reptDevIpAddr(key)]')
                newSt=sub.reporter
                if myKey:
                    newSt+=' ('+myKey+')'
                detail.append(newSt+'')
                detail.append('[eventMsg]')
                detail.append(sub.parseEvent+'')
                detail.append('[params]')
                for item in sub.parameters.split(','):
                    detail.append(item+'')
                detailData[sub.eventType]=detail
    for key in detailData.keys():
        if '/' in key:
            keyName=key.replace('/', '$')
        else:
            keyName=key
        detailFile=open(target+dName+'/'+keyName+'.dat', 'w')
        for item in detailData[key]:
            detailFile.write(item+'\n')
        detailFile.close()

allFile=open(target+targetFile, 'w')
for line in allData:
    allFile.write(line+'\n')
allFile.close()


print 'done'
