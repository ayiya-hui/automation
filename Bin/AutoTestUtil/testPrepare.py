from Libs.XmlHandler import XmlHandler
import ConfigConstants.TestConstant as config_constant
from Util.localhostIp import getLocalhostIp
from Util.timeUtility import getTimeNowFormat, convertTime
from Libs.restApiDataHandler import restApiDataHandler
from checkTimer import checkTimer
import os, sys

def getTestConfig(config, src=None):
    testConfig=XmlHandler().XmlFileToObj(config)
    if testConfig is None:
        print 'testConfig file has problem: %s' % config
        sys.exit()
    testConfig.localhost=getLocalhostIp()
    testConfig.runTime=getTimeNowFormat()
    server=''
    if getattr(testConfig.testServer, 'allInOne'):
        if src:
            server=src
        else:
            server=testConfig.testServer.allInOne
        testConfig.testServer.dbServer=server
        testConfig.testServer.appServer=server
        testConfig.testServer.dataCollector=server
    else:
        server=testConfig.testServer.appServer+'-'+testConfig.testServer.dataCollector
    if hasattr(testConfig, 'noSend') and testConfig.noSend=='true':
        testConfig.noSend=True
    else:
        testConfig.noSend=False
    if os.name=='posix':
        myPass=False
        if hasattr(testConfig, 'rootCredential'):
            myPass=testConfig.rootCredential.password
        print 'pass %s' % myPass
        myCheck=checkTimer(testConfig.testServer.dataCollector, pwd=myPass)
        myCheck.compareTime()
        setattr(testConfig, 'posix', True )
    if hasattr(testConfig, 'credential'):
        my_user=testConfig.credential.user
        my_password=testConfig.credential.password
    else:
        my_user='super/admin'
        my_password='Admin*11'
    setattr(testConfig, 'user', my_user)
    setattr(testConfig, 'password', my_password)
    systemInfo=restApiDataHandler(server.split('-')[0], user=my_user, password=my_password).getData('health', module='cloudStatus')
    if systemInfo:
        try:
          buildDate = convertTime(int(systemInfo.buildDate))
        except ValueError:
          buildDate = systemInfo.buildDate
        testConfig.buildVersion=systemInfo.version+' (build on '+buildDate+')'
        ver_num=int(int(systemInfo.version.replace('.',''))/10000)
        if ver_num>=371:
            setattr(testConfig, 'ruleTestSupport', True)
        else:
            setattr(testConfig, 'ruleTestSupport', False)
    else:
        print 'Cannot get System Info. Exit'
        sys.exit()
    tasks=[]
    for task in testConfig.testTask:
        tasks.append(task.taskName)
        if not task.taskFiles:
            task.taskFiles='all'
        if not task.taskOption:
            task.taskOption=config_constant.test_option_check
        if not task.waitTime:
            task.waitTime=120
    testConfig.name=''.join(tasks)+'-'+testConfig.runTime+'-'+server

    return testConfig


