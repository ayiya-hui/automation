from xml.dom.minidom import parse
import logging, os, os.path
import autoTestClass
import XMLHelper
from configHandler import configHandler
from custHandler import custHandler
import socket, datetime

REPLACE={'localhost':'','reporter':'','dataCollector':'','deviceName':'','sender':''}

def getConfigure(fileName):
    if '.xml' not in fileName:
        fileName+='.xml'
    fileName='../ConfigFiles/'+fileName
    logging.debug("Get config %s", fileName)
    config=XMLHelper.unpickleFile(fileName)
    #check to see if it is all option
    if config['testSuites'].lower()=="all":
        testTask=config['testTask']
        if testTask=="multiCollectors":
            testTask="eventParsing"
        xmlFileList=os.listdir('../DataFiles/'+testTask+'/')
        for file in xmlFileList:
            if 'Test' not in file:
                xmlFileList.remove(file)
        if 'excludeSuites' in config and config['excludeSuites'].lower()!="none":
            exMods=config['excludeSuites'].split(",")
            for ex in exMods:
                xmlFileList.remove(ex+'.xml')
    else:
        xmlFileList=config['testSuites'].split(",")

    config['testSuiteFiles']=xmlFileList

    #adding localhost
    config['localhost']=socket.gethostbyname(socket.gethostname())

    #adding run time
    now=datetime.datetime.now()
    myTime=str(now).replace(" ", "-")
    myTime=myTime.replace(":", "")
    testRunTime=myTime.split(".")
    config['runTime']=testRunTime[0]

    #adding customers info if it has include range, only for eventParsing and incident
    myCust=custHandler(config['appServer'])
    if config['testTask'] in ['eventParsing', 'incident']:
        customers=myCust.getCustomer()
        if len(customers)>0:
            config['customers']=customers

    #adding build version
    myVer=configHandler(config['appServer'])
    version=myVer.getVersion()
    if version!="":
        config['buildVersion']=version

    #if CheckSendBug option set, but no bugZillia user/password supplied, turns the option off
    if 'bugZillaId' not in config and 'bugZillaPass' not in config:
        if config['option']=='SendCheckBug':
            config['option']='SendCheck'

    #prepare test result folder
    directory="../Results/"+config['testTask']
    if not os.path.exists(directory):
        os.mkdir(directory)
    testSever=""
    if config['dataCollector']==config['appServer']:
        testServer=config['dataCollector']
    else:
        if ':' in config['appServer']:
            appServer=config['appServer'].split(':')[0]
        else:
            appServer=config['appServer']
        testServer=config['dataCollector']+"("+appServer+")"
    if 'version' in config:
        folderVersion=config['version']
    else:
        folderVersion=config['buildVersion']

    testFolder=directory+"/"+config['runTime']+"-"+testServer+"-"+folderVersion
    config['testFolder']=testFolder

    logging.debug('config param: %s', config)

    return config

def getTestCases(config):
    testSuiteList=[]
    for xmlFile in config['testSuiteFiles']:
        if '.xml' not in xmlFile:
            xmlFile+=".xml"
        logging.debug("Processing %s", xmlFile)
        testTask=config['testTask']
        if testTask=="multiCollectors":
            testTask="eventParsing"
        fileName="../DataFiles/"+testTask+"/"+xmlFile

        myRawCase=XMLHelper.unpickleFile(fileName)
        if not myRawCase:
            print 'No Test cases presented.'
            exit()

        if hasattr(myRawCase, fileName):
            myRawCase.fileName=xmlFile
        else:
            setattr(myRawCase, 'fileName', xmlFile)

        if config['testTask'] not in ["multiCollectors", "RBAC", "report"]:
            myCase=changeVaribles(myRawCase, config)
        else:
            myCase=myRawCase

        testSuiteList.append(myCase)

    myTestCat=autoTestClass.TestCategory()
    myTestCat.suites=testSuiteList

    return myTestCat

def changeVaribles(raw, config):
    REPLACE['localhost']=config['localhost']
    REPLACE['dataCollector']=config['dataCollector']
    for case in raw.testcases:
        if hasattr(case, 'deviceName'):
            REPLACE['deviceName']=case.deviceName
        if '$localhost' in case.reporter:
            case.reporter=config['localhost']
        if 'customers' in config:
            myCust=custHandler(config['appServer'])
            myCust.customers=config['customers']
            if case.reporter:
                REPLACE['sender']=myCust.getCustIdbyIp(case.reporter, config['dataCollector'])
        else:
            REPLACE['sender']='1'
        REPLACE['reporter']=case.reporter
        if hasattr(case, 'parseEvent'):
            case.parseEvent=replaceAll(case.parseEvent)
        if hasattr(case, 'events'):
            for event in case.events:
                event.incidentMsg=replaceAll(event.incidentMsg)
        if hasattr(case, 'discoverEvent'):
            case.discoverEvent=replaceAll(case.discoverEvent)
        case.parameters=replaceAll(case.parameters)

    return raw

def replaceAll(text):
    for key in REPLACE.keys():
        text=text.replace('$'+key, REPLACE[key])

    return text
