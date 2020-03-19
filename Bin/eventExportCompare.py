import autoTestResultClass
import bugHandler
import logging

def verifyResult(config, name, eventType, reporter, fileParams, restParams):
    PassDetails=[]
    FailDetails=[]
    for param in restParams:
        mapping={}
        for fileParam in fileParams:
            if param['rawEventMsg'].replace(" ", "")==fileParam['rawEventMsg'].replace(" ",""):
                for key in param.keys():
                    mapping['param']=key
                    mapping['expect']=param[key]
                    mapping['actual']=param[key]
        logging.debug(mapping)
        mapCheck=checkMap(mapping)
        if mapCheck=="true":
            PassDetails.append(mapping)
        else:
            FailDetails.append(mapping)

    status='Pass'
    bugId=''
    if len(PassDetails)==0:
        status='NoReturn'
    elif len(FailDetails)>0:
        status='Fail'
    #get bug ID if it is required
    if config['option']=="SendCheckBug":
        if 'bugZillaId' in config and 'bugZilliaPass' in config:
            bugId=bugHandler.AddBugInfo(name, FailDetails, config['bugZillaId'], config['bugZillaPass'])

    resultCase=autoTestResultClass.TestCaseResult(name, status, eventType, reporter, PassDetails, FailDetails, bugId)

    return resultCase

def checkMap(param):
    check="false"
    if param['expect'].replace(" ", "")==param['actual'].replace(" ", ""):
        check=true

    return check
