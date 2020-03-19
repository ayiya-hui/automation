from Libs.queryHandler import queryHandler
from ConfigConstants.TestConstant import event_replace_symbol, event_query_params, incident_query_report_interval, test_path, event_any_params
import Libs.CSVHandler as CSVHandler
import Models.ClassLocator as ClassLocator
import os, socket

Title={'reporter':'[reptDevIpAddr(key)]',
       'msg':'[eventMsg]',
       'param':'[params]'
       }

summary_title='eventType,name,module,reptDevIpAddr,key,method'
summary_line='%s,%s,%s,%s,%s,%s'

def addEventParsingCase(appServer, module, fileName, method):
    myLocal=socket.gethostbyname(socket.gethostname())
    myQuery=queryHandler(appServer)
    myFile=open(fileName)
    data=myFile.readlines()
    myFile.close()
    reporters=[]
    eventtypes=[]
    for line in data:
        reporter,eventtype=line.split(',')
        if reporter not in reporters:
            reporters.append(reporter)
        if eventtype.strip() not in eventtypes:
            eventtypes.append(eventtype.strip())
    reporterStr=','.join(reporters)
    eventStr='","'.join(eventtypes)
    params={}
    params['SingleEvtConstr']=event_query_params['SingleEvtConstr'] % (reporterStr, eventStr)
    retSubData=myQuery.getQuery(params, incident_query_report_interval)
    topPath=test_path % 'EventParsing'
    sumData=CSVHandler.getDataFromFile('eventParsingData', topPath+'/eventParsingData.csv', None, None)
    modifyData={}
    for itemkey in sumData.keys():
        if sumData[itemkey].module not in modifyData.keys():
            modifyData[sumData[itemkey].module]={}
            modifyData[sumData[itemkey].module][itemkey]=sumData[itemkey]
        else:
            modifyData[sumData[itemkey].module][itemkey]=sumData[itemkey]
    if module in modifyData.keys():
        startCaseNum=int(modifyData[module][-1].name.split(module)[-1])
    else:
        startCaseNum=0
    i=1
    summary={}
    detail={}
    for subkey in retSubData.keys():
        obj=ClassLocator.getClassObj('eventParsingData', module='test')
        obj.module=module
        if startCaseNum+i < 10:
            obj.name=module+'0'+str(startCaseNum+i)
        else:
            obj.name=module+str(startCaseNum+i)
        i+=1
        newType,newIp=subkey.split('@')
        subData=retSubData[subkey][-1].attributes
        params={}
        msg=''
        for parKey in subData:
            if parKey=='rawEventMsg':
                msg=subData[parKey]
                if newIp not in msg:
                    newIp='$localhost'
            else:
                if parKey in event_any_params:
                    params[parKey]='any'
                else:
                    params[parKey]=subData[parKey]
        obj.eventType=newType
        obj.reptDevIpAddr=newIp
        obj.method=method
        summary[obj.name]=obj
        map={}
        map['reporter']=newIp
        map['msg']=msg
        map['param']=params
        if newType+'.dat' in detail.keys():
            detail[newType+'.dat'].append(map)
        else:
            detail[newType+'.dat']=[map]
    modulePath=topPath+'/'+module
    if not os.path.exists(modulePath):
        os.mkdir(modulePath)
    files=os.listdir(modulePath)
    if module not in modifyData.keys():
        modifyData[module]=summary
    else:
        for subkey in summary.keys():
            modifyData[module][subkey]=summary[subkey]
    myWrite=open(topPath+'/eventParsingData.csv', 'w')
    myWrite.write(summary_title+'\n')
    for subkey in modifyData.keys():
        for morekey in modifyData[subkey].keys():
            myObj=modifyData[subkey][morekey]
            eventtype=myObj.eventType
            mykey=''
            line=summary_line % (eventtype, myObj.name, myObj.module, myObj.reptDevIpAddr, mykey, myObj.method)
            myWrite.write(line+'\n')
    myWrite.close()
    for itemkey in detail:
        file=itemkey
        for rep in event_replace_symbol:
            if rep in itemkey:
                file=file.replace(rep, '$')
        fullPath=topPath+'/'+module+'/'+file
        if os.path.exists(fullPath):
            myDetail=open(fullPath, 'a')
        else:
            myDetail=open(fullPath, 'w')
        for sub in detail[itemkey]:
            myDetail.write(Title['reporter']+'\n')
            myDetail.write(sub['reporter']+'\n')
            myDetail.write(Title['msg']+'\n')
            myDetail.write(sub['msg']+'\n')
            myDetail.write(Title['param']+'\n')
            sub['param']['phCustId']='$sender'
            sub['param']['relayDevIpAddr']='$localhost'
            if sub['param']['reptDevIpAddr']==myLocal:
                sub['param']['reptDevIpAddr']='$localhost'
            for parkey in sub['param'].keys():
                myDetail.write(parkey+'='+sub['param'][parkey]+'\n')
        myDetail.close()
    print 'Done'

if __name__=='__main__':
    import sys
    if len(sys.argv)!=5:
        print 'Usage: %prog appServer module filePath method'
        exit()
    appServer=sys.argv[1]
    module=sys.argv[2]
    fileName=sys.argv[3]
    method=sys.argv[4]
    addEventParsingCase(appServer, module, fileName, method)

    print 'Task finished.'

