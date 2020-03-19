#from optparse import OptionParser

#parser=OptionParser()
#parser.add_option('-n', '--name', dest='name', help='name of task', metavar='NAME')
#options, args=parser.parse_args()

from Libs.appHandler import appHandler
from Libs.XmlHandler import XmlHandler

appServer='192.168.1.113'

path='../TestData/restApi/orgNoCollector.xml'
#path='../TestData/restApi/organization.xml'
#path='../TestData/restApi/accessConfigs.xml'
#path='../TestData/restApi/discoverRequest.xml'
#path='../TestData/restApi/MaintSchedule.xml'
#path='../TestData/restApi/systemMonitor.xml'
param='organization/add'
myFile=open(path)
rawXml=myFile.read()
myFile.close()
#orgs=XmlHandler().XmlFileToObj(path, keyword='organizations')
#for org in orgs:
    #user=org.name+'/'+org.adminUser
    #password=org.adminPwd
tag='<organizations>%s</organizations>'
for i in range(100):
    myFinalXml=''
    myXml=''
    myXml=rawXml % ('AutoCust'+str(i+1), 'AutoCust'+str(i+1), 'AutoCust'+str(i+1), '192.168.1.'+str(i+1))
    myFinalXml=tag % myXml
    print myFinalXml
    myApp=appHandler(appServer)
    id=myApp.putData(param, myFinalXml)
    print 'id: %s' % id

#param='organization/delete?organization=organization222'
#param='deviceMon/updateCredential'
#param='deviceMaint/update'
#param='deviceMon/updateMonitor'










