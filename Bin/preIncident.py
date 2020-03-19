import os
from Libs.XmlHandler import XmlHandler

path='../DataFiles/Incident'
files=os.listdir(path)
configpath='../TestData/Incident/incidentData.csv'
rawpath='../TestData/Incident/IncidentMsgs/'
eD='[eventMsg]'
cD='[clearEventMsg]'
dataList=[]

for file in files:
    if '.xml' in file:
        data=XmlHandler().XmlFileToObj(path+'/'+file)
        dataList.append(data)
outFile=open(configpath, 'w')
outFile.write('incidentType,name,reptDevIpAddr,createDevice,deviceName,deviceType,domainController,count,method')
outFile.write('\n')
for item in dataList:
    case=item.testcases[0]
    output=[]
    output.append(case.eventType)
    output.append(item.name)
    output.append(case.reporter)
    reporter=case.reporter
    if case.createDevice!=None:
        output.append(case.createDevice)
    else:
        output.append('')
    if case.deviceName!=None:
        output.append(case.deviceName)
        name=case.deviceName
    else:
        output.append('')
        name=''
    if case.deviceType!=None:
        output.append(case.deviceType)
    else:
        output.append('')
    if case.domainController!=None:
        output.append(case.domainController)
    else:
        output.append('')
    output.append(case.repeatCount)
    output.append(item.method)
    print output
    str=','.join(output)
    outFile.write(str+'\n')
    dataFile=open(rawpath+case.eventType+'.dat', 'w')
    dataFile.write(eD+'\n')
    for event in case.events:
        print name, reporter
        dataFile.write(event.incidentMsg.replace('$deviceName', name).replace('$reporter', reporter))
    if len(item.testcases)==3:
        dataFile.write('\n\n')
        dataFile.write(cD+'\n')
        clearCase=item.testcases[2]
        for event in clearCase.events:
            dataFile.write(event.incidentMsg.replace('$deviceName', name).replace('$reporter', reporter))
    dataFile.close()

outFile.close()



print 'done'
