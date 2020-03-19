from runBase import baseTest
from ConfigConstants.TestConstant import rest_params
from Libs.appHandler import appHandler
import time, os

class restApiTest(baseTest):
    def __init__(self, task, testConfig):
        baseTest.__init__(self, task, testConfig)

    def getCommonData(self):
        indexModule={}
        folders=os.listdir(self.path)
        for file in folders:
            myFile=open(self.path+'/'+file)
            rawData=myFile.read()
            myFile.close()
            indexModule[file.split('.')[0]]=rawData

        self.commons=indexModule

        return self.commons

    def getTestList(self, taskFiles):
        if taskFiles.lower()=='all':
            map=self.commons
        else:
            map={}
            for key in taskFiles.split(','):
                map[key]=self.commons[key]

        return map

    def run(self, type, key):
        id=appHandler(self.testConfig.testServer.appServer).putData(rest_params[key]['test'], type)
        #time.sleep(self.task.waitTime)
        #myarg={}
        #myarg['taskId']=id
        #verify=rest_params[self.task.taskName]['verify']
        #moName, type=verify.split('/')
        #data=self.restApiHandler.getData(type, module=moName, arg=myarg)

        print 'done'


#path='../TestData/restApi/organization.xml'
#path='../TestData/restApi/accessConfigs.xml'
#path='../TestData/restApi/discoverRequest.xml'
#path='../TestData/restApi/MaintSchedule.xml'
#path='../TestData/restApi/systemMonitor.xml'
#myFile=open(path)
#rawXml=myFile.read()
#myFile.close()
#orgs=XmlHandler().XmlFileToObj(path, keyword='organizations')
#for org in orgs:
    #user=org.name+'/'+org.adminUser
    #password=org.adminPwd
#param='organization/add'
#param='organization/delete?organization=organization222'
#param='deviceMon/updateCredential'
#param='deviceMaint/update'
#param='deviceMon/updateMonitor'
#appServer='192.168.20.116'
#rawXml=''

#myApp=appHandler(appServer)
#id=myApp.putData(param, rawXml)

#print 'id: %s' % id




