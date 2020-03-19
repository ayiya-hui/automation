import autoTestResultClass
import bugHandler
import logging


def runCaseCompare(expectParam, actualParams):
    passList=[]
    failList=[]
    missList=[]
    improveList=[]
    actualParam={}
    for actual in actualParams:
        if actual['reptDevIpAddr'] ==expectParam['reptDevIpAddr']:
            actualParam=actual
    for key in expectParam.keys():
        map={}
        map['param']=key
        map['expect']=expectParam[key]
        if key in actualParam.keys():
            map['actual']=actualParam[key]
        else:
            map['actual']="Missing Data"

        if map['expect'].replace(" ", "")==map['actual'].replace(" ", ""):
            passList.append(map)
        elif map['actual']=="Missing Data":
            missList.append(map)
        else:
            failList.append(map)

    for key in actualParam.keys():
        if key not in expectParam.keys():
            map={}
            map['param']=key
            map['expect']="Need to Add"
            map['actual']=actualParam[key]
            improveList.append(map)

    status="NoReturn"
    if len(passList)!=0 and len(failList)==0 and len(missList)==0 and len(improveList)==0:
        status="Pass"
    elif len(failList)!=0:
        status="Fail"
    elif len(missList)!=0:
        status="Miss"
    elif len(improveList)!=0:
        status="Improve"



    resultData={}
    resultData['status']=status
    resultData['passDetail']=passList
    resultData['failDetail']=failList
    resultData['missDetail']=missList
    resultData['improveDetail']=improveList

    return resultData



