from runBase import baseTest
from ConfigConstants.TestConstant import rest_params
from Libs.appHandler import appHandler
import time

class discoverTest(baseTest):
    def __init__(self, task, testConfig):
        baseTest.__init__(self, task, testConfig)

    def run(self, type):
        myFile=open(self.path+'/'+type+'.xml')
        rawXml=myFile.read()
        myFile.close()
        id=appHandler(self.testConfig.testServer.appServer).putData(rest_params[self.task.taskName]['test'], rawXml)
        time.sleep(self.task.waitTime)
        myarg={}
        myarg['taskId']=id
        verify=rest_params[self.task.taskName]['verify']
        moName, type=verify.split('/')
        data=self.restApiHandler.getData(type, module=moName, arg=myarg)

        print 'done'


